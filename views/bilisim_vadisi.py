"""
Bilişim Vadisi — Streamlit UI
===============================
Bilim Laboratuvarı + Kodlama Adası birleşik premium modül.
"""
from __future__ import annotations
import streamlit as st
import math
from datetime import datetime

from utils.ui_common import inject_common_css, styled_header, styled_section, _render_html
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("steam_merkezi")
except Exception:
    pass
from models.bilisim_vadisi import (
    get_store, BilisimDataStore,
    FIZIK_DENEYLERI, KIMYA_DENEYLERI, BIYOLOJI_DENEYLERI,
    UNLU_BILIM_INSANLARI, PROGRAMLAMA_DILLERI,
    KODLAMA_KAVRAMLARI, KODLAMA_SORULARI,
    PERIYODIK_TABLO, KODLAMA_DERSLERI, KODLAMA_SORULARI_EK,
    BILIM_TARIHI, EGLENCELI_BILIM, BILIM_OYUN_SORULARI,
    KODLAMA_OYUNLARI, VUCUT_SISTEMLERI, GUNES_SISTEMI, UZAY_BILGISI,
    BILIM_SENLIGI_PROJELERI, PROJE_KATEGORILERI, BilimQuizGenerator,
    get_bilim_ipucu,
)


def render_bilisim_vadisi():
    """Ana giriş noktası."""
    inject_common_css("bv")
    styled_header("Bilişim Vadisi", "💻")
    # XP bar gecici olarak devre disi
    # from utils.gamification_ui import render_xp_bar
    # render_xp_bar()

    store = get_store()

    _render_html("""
    <style>
    .bv-hero {
        background: linear-gradient(135deg, #0c1222 0%, #1e3a5f 40%, #0ea5e9 100%);
        border-radius: 24px; padding: 32px; margin-bottom: 24px;
        border: 2px solid rgba(14,165,233,0.4); text-align: center;
        position: relative; overflow: hidden;
    }
    .bv-card {
        background: linear-gradient(145deg, #0a1628, #1e3a5f);
        border-radius: 18px; padding: 22px; margin-bottom: 14px;
        border: 1px solid rgba(14,165,233,0.2); transition: all 0.3s;
    }
    .bv-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(14,165,233,0.2); }
    .bv-code {
        background: #0f172a; border-radius: 12px; padding: 16px;
        border: 1px solid #1e293b; font-family: 'Courier New', monospace;
        color: #10b981 !important; font-size: 0.85rem; line-height: 1.6;
        overflow-x: auto;
    }
    </style>
    """)

    # -- Tab Gruplama (34 tab -> 5 grup) --
    _GRP_40896 = {
        "📋 Grup A": [("🏠 Vadi Meydanı", 0), ("⚗️ Fizik Lab", 1), ("🧪 Kimya Lab", 2), ("🔬 Biyoloji Lab", 3), ("⚛️ Periyodik Tablo", 4), ("🧑‍🔬 Bilim İnsanları", 5), ("📜 Bilim Tarihi", 6)],
        "📊 Grup B": [("🎪 Eğlenceli Bilim", 7), ("🎮 Bilim Quizi", 8), ("🫀 İnsan Vücudu", 9), ("🪐 Uzay & Evren", 10), ("🐍 Kodlamaya Giriş", 11), ("📖 Kodlama Dersleri", 12), ("📚 Kavramlar", 13)],
        "🔧 Grup C": [("💻 Kod Yaz & Çalıştır", 14), ("🏆 Kodlama Soruları", 15), ("🐛 Kodlama Oyunları", 16), ("🎪 Bilim Şenliği", 17), ("🤖 AI Bilim Koçu", 18), ("📊 İlerleme", 19), ("🌐 Web Geliştirme", 20)],
        "📈 Grup D": [("🤖 Robot Programlama", 21), ("🛡️ Siber Güvenlik", 22), ("🔬 Deney Simulasyonu", 23), ("🧩 Blok Kodlama", 24), ("🧠 Yapay Zeka", 25), ("⚡ Elektronik Lab", 26), ("🖨️ 3D Yazici", 27)],
        "🎯 Grup E": [("🐍 Python Lab", 28), ("🧮 Algoritma Lab", 29), ("🔭 Bilim Studyosu", 30), ("🏅 Proje Vitrini", 31), ("📊 Ogrenci Raporu", 32), ("🤖 Smarti", 33)],
    }
    _sg_40896 = st.radio("", list(_GRP_40896.keys()), horizontal=True, label_visibility="collapsed", key="rg_40896")
    _gt_40896 = _GRP_40896[_sg_40896]
    _aktif_idx_40896 = set(t[1] for t in _gt_40896)
    _tab_names_40896 = [t[0] for t in _gt_40896]
    tabs = st.tabs(_tab_names_40896)
    _tab_real_40896 = {idx: t for idx, t in zip((t[1] for t in _gt_40896), tabs)}

    if 0 in _aktif_idx_40896:
      with _tab_real_40896[0]:
        _render_meydan(store)
    if 1 in _aktif_idx_40896:
      with _tab_real_40896[1]:
        _render_fizik(store)
    if 2 in _aktif_idx_40896:
      with _tab_real_40896[2]:
        _render_kimya(store)
    if 3 in _aktif_idx_40896:
      with _tab_real_40896[3]:
        _render_biyoloji(store)
    if 4 in _aktif_idx_40896:
      with _tab_real_40896[4]:
        _render_periyodik_tablo()
    if 5 in _aktif_idx_40896:
      with _tab_real_40896[5]:
        _render_bilim_insanlari()
    if 6 in _aktif_idx_40896:
      with _tab_real_40896[6]:
        _render_bilim_tarihi()
    if 7 in _aktif_idx_40896:
      with _tab_real_40896[7]:
        _render_eglenceli_bilim()
    if 8 in _aktif_idx_40896:
      with _tab_real_40896[8]:
        _render_bilim_quizi()
    if 9 in _aktif_idx_40896:
      with _tab_real_40896[9]:
        _render_insan_vucudu()
    if 10 in _aktif_idx_40896:
      with _tab_real_40896[10]:
        _render_uzay_evren()
    if 11 in _aktif_idx_40896:
      with _tab_real_40896[11]:
        _render_kodlama_giris()
    if 12 in _aktif_idx_40896:
      with _tab_real_40896[12]:
        _render_kodlama_dersleri()
    if 13 in _aktif_idx_40896:
      with _tab_real_40896[13]:
        _render_kavramlar()
    if 14 in _aktif_idx_40896:
      with _tab_real_40896[14]:
        _render_kod_yaz()
    if 15 in _aktif_idx_40896:
      with _tab_real_40896[15]:
        _render_kodlama_sorulari()
    if 16 in _aktif_idx_40896:
      with _tab_real_40896[16]:
        _render_kodlama_oyunlari()
    if 17 in _aktif_idx_40896:
      with _tab_real_40896[17]:
        _render_bilim_senligi()
    if 18 in _aktif_idx_40896:
      with _tab_real_40896[18]:
        _render_ai_bilim_kocu()
    if 19 in _aktif_idx_40896:
      with _tab_real_40896[19]:
        _render_ilerleme(store)
    if 20 in _aktif_idx_40896:
      with _tab_real_40896[20]:
        _render_web_gelistirme()
    if 21 in _aktif_idx_40896:
      with _tab_real_40896[21]:
        _render_robot_programlama()
    if 22 in _aktif_idx_40896:
      with _tab_real_40896[22]:
        _render_siber_guvenlik()
    if 23 in _aktif_idx_40896:
      with _tab_real_40896[23]:
        _render_deney_simulasyonu()
    if 24 in _aktif_idx_40896:
      with _tab_real_40896[24]:
        _render_blok_kodlama()
    if 25 in _aktif_idx_40896:
      with _tab_real_40896[25]:
        _render_yapay_zeka()
    if 26 in _aktif_idx_40896:
      with _tab_real_40896[26]:
        _render_elektronik_lab()
    if 27 in _aktif_idx_40896:
      with _tab_real_40896[27]:
        _render_3d_yazici()
    if 28 in _aktif_idx_40896:
      with _tab_real_40896[28]:
        _render_python_lab()
    if 29 in _aktif_idx_40896:
      with _tab_real_40896[29]:
        _render_algoritma_lab()
    if 30 in _aktif_idx_40896:
      with _tab_real_40896[30]:
        _render_bilim_studyosu()
    if 31 in _aktif_idx_40896:
      with _tab_real_40896[31]:
        _render_proje_vitrini()
    if 32 in _aktif_idx_40896:
      with _tab_real_40896[32]:
        from views.modul_rapor_ui import render_ogretmen_rapor
        render_ogretmen_rapor(modul_filter="bilisim", key_prefix="mr_bv")

    if 33 in _aktif_idx_40896:
      with _tab_real_40896[33]:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="bilisim_vadisi")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_bilisim_vadisi")
            if st.button("Gönder", key="smarti_send_bilisim_vadisi"):
                if user_q.strip():
                    try:
                        from openai import OpenAI
                        import os
                        api_key = os.environ.get("OPENAI_API_KEY", "")
                        if api_key:
                            client = OpenAI(api_key=api_key)
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. bilisim_vadisi modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")


def _render_meydan(store):
    styled_section("🏠 Bilişim Vadisi", "#0ea5e9")

    _render_html("""
    <div class="bv-hero">
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:10px">🔬💻⚡🧬🐍</div>
            <h2 style="color:#e0f2fe !important;font-size:1.6rem;margin:0 0 8px !important">Bilişim Vadisi'ne Hoş Geldin!</h2>
            <p style="color:#bae6fd !important;font-size:0.9rem;margin:0 !important">
                Fizik, Kimya, Biyoloji deneyleri + Python programlama — bilim ve teknolojiyi keşfet!
            </p>
        </div>
    </div>
    """)

    # Günlük ipucu
    ipucu = get_bilim_ipucu()
    _render_html(f"""
    <div style="background:linear-gradient(135deg,#0ea5e915,#0ea5e908);border-radius:14px;padding:14px 18px;
                 margin-bottom:16px;border:1px solid rgba(14,165,233,0.3)">
        <div style="font-weight:700;color:#7dd3fc !important;font-size:0.9rem">🔬 Günün Bilim İpucu</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">{ipucu}</div>
    </div>
    """)

    # İstatistik kartları
    cols = st.columns(4)
    stats = [
        ("⚗️", str(len(FIZIK_DENEYLERI)), "Fizik Deneyi"),
        ("🧪", str(len(KIMYA_DENEYLERI)), "Kimya Deneyi"),
        ("🔬", str(len(BIYOLOJI_DENEYLERI)), "Biyoloji Deneyi"),
        ("🐍", str(len(PROGRAMLAMA_DILLERI)), "Programlama Dili"),
    ]
    for col, (ikon, deger, etiket) in zip(cols, stats):
        with col:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:14px;padding:14px;text-align:center;
                         border:1px solid rgba(14,165,233,0.15)">
                <div style="font-size:1.5rem">{ikon}</div>
                <div style="font-weight:800;color:#0ea5e9 !important;font-size:1.4rem">{deger}</div>
                <div style="font-size:0.7rem;color:#94a3b8 !important">{etiket}</div>
            </div>
            """)


def _render_lab(deneyler, baslik, renk, ikon_lab):
    """Genel deney lab render."""
    styled_section(f"{ikon_lab} {baslik}", renk)
    for d in deneyler:
        with st.expander(f"{d['ikon']} {d['ad']} ({d['zorluk']}) — Sınıf {d['sinif']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Açıklama:** {d['aciklama']}")
                st.markdown(f"**Malzeme:** {d['malzeme']}")
                _render_html(f"""
                <div style="background:rgba(99,102,241,0.08);border-radius:10px;padding:12px;margin:8px 0;
                             text-align:center;border:1px dashed rgba(99,102,241,0.2)">
                    <div style="font-size:0.7rem;color:#94a3b8 !important;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Formül</div>
                    <div style="font-size:1.1rem;font-weight:700;color:#818cf8 !important;font-family:'Cambria Math',serif">{d['formul']}</div>
                </div>
                """)
            with col2:
                _render_html(f"""
                <div style="background:#0f172a;border-radius:12px;padding:12px;text-align:center;border:1px solid rgba(99,102,241,0.1)">
                    <div style="font-size:2.5rem;margin-bottom:4px">{d['ikon']}</div>
                    <div style="font-size:0.7rem;color:#94a3b8 !important">⏱️ {d['sure']}</div>
                </div>
                """)
            st.info(f"💡 {d['bilgi']}")


def _render_fizik(store):
    _render_lab(FIZIK_DENEYLERI, "Fizik Laboratuvarı", "#3b82f6", "⚗️")

def _render_kimya(store):
    _render_lab(KIMYA_DENEYLERI, "Kimya Laboratuvarı", "#10b981", "🧪")

def _render_biyoloji(store):
    _render_lab(BIYOLOJI_DENEYLERI, "Biyoloji Laboratuvarı", "#8b5cf6", "🔬")


def _render_bilim_insanlari():
    styled_section("🧑‍🔬 Ünlü Bilim İnsanları", "#f59e0b")
    for b in UNLU_BILIM_INSANLARI:
        img = f'<img src="{b["portre_url"]}" style="width:70px;height:70px;border-radius:50%;object-fit:cover;border:2px solid #0ea5e9" onerror="this.style.display=\'none\'">' if b.get("portre_url") else f'<div style="font-size:2.5rem">{b["ikon"]}</div>'
        _render_html(f"""
        <div class="bv-card" style="display:flex;gap:16px;align-items:center">
            <div style="min-width:70px;text-align:center">{img}</div>
            <div style="flex:1">
                <div style="font-weight:700;color:#e0f2fe !important;font-size:1rem">{b['ad']} {b['ikon']}</div>
                <div style="font-size:0.75rem;color:#7dd3fc !important">{b['alan']} • {b['yasam']} • {b['ulke']}</div>
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:4px">{b['bilgi']}</div>
            </div>
        </div>
        """)


def _render_kodlama_giris():
    styled_section("🐍 Kodlamaya Giriş", "#10b981")

    _render_html("""
    <div class="bv-card" style="text-align:center;border-color:rgba(16,185,129,0.3)">
        <div style="font-size:2rem;margin-bottom:6px">🐍💻🌐</div>
        <div style="font-weight:700;color:#bbf7d0 !important;font-size:1.1rem">Kodlamak = Süper Güç!</div>
        <div style="color:#86efac !important;font-size:0.85rem">Bilgisayara ne yapması gerektiğini sen söylüyorsun!</div>
    </div>
    """)

    for dil in PROGRAMLAMA_DILLERI:
        with st.expander(f"{dil['ikon']} {dil['ad']} ({dil['seviye']}) — {dil['yil']}", expanded=(dil['ad']=='Python')):
            st.markdown(dil['aciklama'])
            st.markdown(f"**Özellik:** {dil['ozellik']}")
            st.markdown("**Merhaba Dünya:**")
            st.code(dil['merhaba'], language="python" if dil['ad']=='Python' else 'javascript' if dil['ad']=='JavaScript' else None)


def _render_kavramlar():
    styled_section("📚 Programlama Kavramları", "#8b5cf6")

    for k in KODLAMA_KAVRAMLARI:
        with st.expander(f"{k['ikon']} {k['ad']}", expanded=False):
            st.markdown(k['aciklama'])
            st.code(k['ornek'], language="python")


def _render_kod_yaz():
    styled_section("💻 Kod Yaz & Test Et", "#0ea5e9")

    _render_html("""
    <div class="bv-card" style="text-align:center;border-color:rgba(14,165,233,0.3)">
        <div style="font-size:2rem;margin-bottom:6px">💻✨</div>
        <div style="font-weight:700;color:#e0f2fe !important;font-size:1.1rem">Python Kod Editörü</div>
        <div style="color:#bae6fd !important;font-size:0.85rem">Kodunu yaz ve çalıştır!</div>
    </div>
    """)

    default_code = '''# Merhaba Dünya!
print("Bilişim Vadisi'ne hoş geldin! 🐍")

# Değişkenler
isim = "Ali"
yas = 12
print(f"{isim} {yas} yaşında!")

# Döngü
for i in range(1, 6):
    print(f"⭐ {'*' * i}")
'''

    kod = st.text_area("Python Kodu:", value=default_code, height=250, key="bv_kod")

    if st.button("▶️ Çalıştır!", key="bv_run", type="primary"):
        try:
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            # Güvenli çalıştırma (sınırlı)
            safe_globals = {"__builtins__": {"print": print, "range": range, "len": len,
                                              "int": int, "float": float, "str": str,
                                              "list": list, "dict": dict, "abs": abs,
                                              "max": max, "min": min, "sum": sum,
                                              "sorted": sorted, "enumerate": enumerate,
                                              "zip": zip, "map": map, "filter": filter,
                                              "round": round, "type": type, "input": lambda p="": "test"}}
            exec(kod, safe_globals)
            sys.stdout = old_stdout
            output = buffer.getvalue()
            if output:
                _render_html(f"""
                <div style="background:#052e16;border-radius:12px;padding:16px;margin-top:8px;
                             border:1px solid rgba(16,185,129,0.3)">
                    <div style="font-size:0.75rem;color:#86efac !important;margin-bottom:4px">✅ Çıktı:</div>
                    <pre style="color:#10b981 !important;font-family:'Courier New',monospace;font-size:0.85rem;margin:0;white-space:pre-wrap">{output}</pre>
                </div>
                """)
            else:
                st.success("✅ Kod çalıştı — çıktı yok.")
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ Hata: {e}")


def _render_kodlama_sorulari():
    styled_section("🏆 Kodlama Soruları", "#eab308")

    zorluk_f = st.selectbox("Zorluk Filtresi", ["Tümü", "Kolay", "Orta", "Zor"], key="bv_soru_z")
    tum_sorular = KODLAMA_SORULARI + KODLAMA_SORULARI_EK

    if zorluk_f != "Tümü":
        tum_sorular = [s for s in tum_sorular if s["seviye"] == zorluk_f]

    st.caption(f"📋 {len(tum_sorular)} soru gösteriliyor")

    for i, s in enumerate(tum_sorular):
        seviye_ikon = {"Kolay": "🌱", "Orta": "🌿", "Zor": "🌳"}.get(s["seviye"], "📝")
        with st.expander(f"{seviye_ikon} Soru {i+1}: {s['soru'][:60]}... ({s['seviye']})", expanded=False):
            st.markdown(f"**Soru:** {s['soru']}")
            st.text_area("Çözümünü yaz:", key=f"bv_soru_{i}", height=150, placeholder="# Kodunu buraya yaz...")
            with st.expander("💡 İpucu"):
                st.info(s["ipucu"])
            with st.expander("👁️ Örnek Çözüm"):
                st.code(s["cevap"], language="python")


def _render_periyodik_tablo():
    """Tam periyodik tablo — 3D efektli, tıkla-gör bilgi kartlı."""
    import streamlit.components.v1 as components
    styled_section("⚛️ Periyodik Tablo — İnteraktif 3D", "#0ea5e9")

    # 3D Periyodik Tablo — tam 118 element JavaScript ile
    html_code = """
    <style>
    #ptContainer { perspective: 1200px; margin: 10px auto; max-width: 900px; }
    #ptTable {
        display: grid; grid-template-columns: repeat(18, 1fr); gap: 2px;
        transform: rotateX(5deg) rotateY(-2deg);
        transition: transform 0.5s;
        transform-style: preserve-3d;
    }
    #ptTable:hover { transform: rotateX(0deg) rotateY(0deg); }
    .pt-cell {
        padding: 3px 2px; text-align: center; border-radius: 4px;
        cursor: pointer; transition: all 0.2s; position: relative;
        transform-style: preserve-3d; min-height: 44px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .pt-cell:hover {
        transform: translateZ(20px) scale(1.3);
        z-index: 10; box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        border-color: white;
    }
    .pt-cell .pt-no { font-size: 0.45rem; color: rgba(255,255,255,0.5); }
    .pt-cell .pt-sym { font-size: 0.85rem; font-weight: 900; color: white; text-shadow: 0 1px 3px rgba(0,0,0,0.5); }
    .pt-cell .pt-name { font-size: 0.35rem; color: rgba(255,255,255,0.6); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .pt-empty { min-height: 44px; }
    #ptInfo {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 16px; padding: 20px; margin-top: 12px;
        border: 2px solid #334155; min-height: 80px;
        display: flex; gap: 16px; align-items: center;
    }
    #ptInfo .info-sym { font-size: 3rem; font-weight: 900; min-width: 70px; text-align: center; }
    #ptInfo .info-name { font-size: 1.2rem; font-weight: 700; color: #e0e7ff; }
    #ptInfo .info-detail { font-size: 0.8rem; color: #94a3b8; margin-top: 4px; }
    #ptInfo .info-desc { font-size: 0.8rem; color: #7dd3fc; margin-top: 6px; line-height: 1.5; }
    </style>

    <div id="ptContainer">
        <div id="ptTable"></div>
    </div>
    <div id="ptInfo">
        <div class="info-sym" id="infoSym" style="color:#0ea5e9">⚛️</div>
        <div>
            <div class="info-name" id="infoName">Bir elemente tıkla!</div>
            <div class="info-detail" id="infoDetail">118 element keşfedildi</div>
            <div class="info-desc" id="infoDesc">Periyodik tabloda elementler atom numarasına göre sıralanır. Aynı sütundakiler benzer özellik gösterir.</div>
        </div>
    </div>

    <script>
    (function(){
        // Tam 118 element verisi — [no, sembol, ad, kütle, grup, renk, satır, sütun, bilgi]
        const elements = [
            [1,"H","Hidrojen",1.008,"Ametal","#ef4444",1,1,"Evrendeki en yaygın element! Güneş'in %75'i."],
            [2,"He","Helyum",4.003,"Soygaz","#8b5cf6",1,18,"Balonları uçuran gaz. Sesi inceltir!"],
            [3,"Li","Lityum",6.941,"Alkali","#f59e0b",2,1,"Pil teknolojisi. Suya atınca yanar!"],
            [4,"Be","Berilyum",9.012,"Toprak Alk.","#10b981",2,2,"X-ray pencerelerinde kullanılır."],
            [5,"B","Bor",10.81,"Yarı Metal","#06b6d4",2,13,"Türkiye dünya bor rezervinin %73'ü!"],
            [6,"C","Karbon",12.011,"Ametal","#ef4444",2,14,"Yaşamın temeli! Elmas ve grafit."],
            [7,"N","Azot",14.007,"Ametal","#ef4444",2,15,"Havanın %78'i azot."],
            [8,"O","Oksijen",15.999,"Ametal","#ef4444",2,16,"Nefes aldığımız gaz!"],
            [9,"F","Flor",18.998,"Halojen","#3b82f6",2,17,"En reaktif element!"],
            [10,"Ne","Neon",20.180,"Soygaz","#8b5cf6",2,18,"Neon tabelalar!"],
            [11,"Na","Sodyum",22.990,"Alkali","#f59e0b",3,1,"Sofra tuzu = NaCl."],
            [12,"Mg","Magnezyum",24.305,"Toprak Alk.","#10b981",3,2,"Klorofilin merkezinde."],
            [13,"Al","Alüminyum",26.982,"Metal","#94a3b8",3,13,"Uçaklar, kutular. Geri dönüşüm!"],
            [14,"Si","Silisyum",28.086,"Yarı Metal","#06b6d4",3,14,"Bilgisayar çipleri! Silikon Vadisi."],
            [15,"P","Fosfor",30.974,"Ametal","#ef4444",3,15,"DNA ve ATP'nin bileşeni."],
            [16,"S","Kükürt",32.065,"Ametal","#ef4444",3,16,"Barut yapımında. Volkanlar kükürt püskürtür."],
            [17,"Cl","Klor",35.453,"Halojen","#3b82f6",3,17,"Havuz dezenfektanı."],
            [18,"Ar","Argon",39.948,"Soygaz","#8b5cf6",3,18,"Ampul içi gaz."],
            [19,"K","Potasyum",39.098,"Alkali","#f59e0b",4,1,"Muz potasyum açısından zengin!"],
            [20,"Ca","Kalsiyum",40.078,"Toprak Alk.","#10b981",4,2,"Kemik ve dişler."],
            [21,"Sc","Skandiyum",44.956,"Geçiş","#94a3b8",4,3,"Hafif alaşımlarda."],
            [22,"Ti","Titanyum",47.867,"Geçiş","#94a3b8",4,4,"Uçak ve implant. Çelikten güçlü, %45 hafif!"],
            [23,"V","Vanadyum",50.942,"Geçiş","#94a3b8",4,5,"Çelik alaşımları."],
            [24,"Cr","Krom",51.996,"Geçiş","#94a3b8",4,6,"Paslanmaz çelik. Parlak kaplama."],
            [25,"Mn","Mangan",54.938,"Geçiş","#94a3b8",4,7,"Pil üretiminde kritik."],
            [26,"Fe","Demir",55.845,"Geçiş","#94a3b8",4,8,"En çok kullanılan metal. Kanın rengi!"],
            [27,"Co","Kobalt",58.933,"Geçiş","#94a3b8",4,9,"Mavi renk pigmenti. Li-ion piller."],
            [28,"Ni","Nikel",58.693,"Geçiş","#94a3b8",4,10,"Paslanmaz çelik. Madeni paralar."],
            [29,"Cu","Bakır",63.546,"Geçiş","#94a3b8",4,11,"Elektrik iletkenliği mükemmel!"],
            [30,"Zn","Çinko",65.38,"Geçiş","#94a3b8",4,12,"Bağışıklık sistemi. Galvaniz."],
            [31,"Ga","Galyum",69.723,"Metal","#94a3b8",4,13,"Elde erir (29.8°C)! LED'lerde."],
            [32,"Ge","Germanyum",72.630,"Yarı Metal","#06b6d4",4,14,"İlk transistörlerde kullanıldı."],
            [33,"As","Arsenik",74.922,"Yarı Metal","#06b6d4",4,15,"Zehirlerin kralı! Dedektif romanları."],
            [34,"Se","Selenyum",78.971,"Ametal","#ef4444",4,16,"Fotokopi makinelerinde."],
            [35,"Br","Brom",79.904,"Halojen","#3b82f6",4,17,"Oda sıcaklığında sıvı (cıva ile birlikte tek)."],
            [36,"Kr","Kripton",83.798,"Soygaz","#8b5cf6",4,18,"Süpermen'in gezegeni! Flaş ışıklarında."],
            [47,"Ag","Gümüş",107.87,"Geçiş","#94a3b8",5,11,"En iyi elektrik iletkeni!"],
            [50,"Sn","Kalay",118.71,"Metal","#94a3b8",5,14,"Lehim. Teneke kutular."],
            [53,"I","İyot",126.90,"Halojen","#3b82f6",5,17,"Tiroit bezi için hayati. Antiseptik."],
            [54,"Xe","Ksenon",131.29,"Soygaz","#8b5cf6",5,18,"Uzay iyonik motorlarında yakıt!"],
            [74,"W","Tungsten",183.84,"Geçiş","#94a3b8",6,6,"En yüksek erime noktası (3422°C)! Ampul teli."],
            [78,"Pt","Platin",195.08,"Geçiş","#94a3b8",6,10,"Altından değerli! Katalitik konvertör."],
            [79,"Au","Altın",196.97,"Geçiş","#94a3b8",6,11,"Paslanmaz! Elektronik devrelerde."],
            [80,"Hg","Cıva",200.59,"Geçiş","#94a3b8",6,12,"Sıvı metal! Termometre (eski)."],
            [82,"Pb","Kurşun",207.2,"Metal","#94a3b8",6,14,"Radyasyon kalkanı. Zehirli!"],
            [92,"U","Uranyum",238.03,"Aktinit","#ec4899",7,6,"Nükleer enerji yakıtı!"],
            [94,"Pu","Plütonyum",244,"Aktinit","#ec4899",7,8,"Atom bombası. Voyager'ın pili!"],
            [118,"Og","Oganesson",294,"Soygaz","#8b5cf6",7,18,"Son keşfedilen element (2006)!"],
        ];

        const table = document.getElementById('ptTable');
        const grid = {};
        elements.forEach(e => { grid[e[6]+','+e[7]] = e; });

        for(let r=1; r<=7; r++){
            for(let c=1; c<=18; c++){
                const el = grid[r+','+c];
                const cell = document.createElement('div');
                if(el){
                    cell.className = 'pt-cell';
                    cell.style.background = el[5] + '25';
                    cell.innerHTML = `<div class="pt-no">${el[0]}</div><div class="pt-sym">${el[1]}</div><div class="pt-name">${el[2]}</div>`;
                    cell.onclick = () => {
                        document.getElementById('infoSym').textContent = el[1];
                        document.getElementById('infoSym').style.color = el[5];
                        document.getElementById('infoName').textContent = el[0] + '. ' + el[2] + ' (' + el[1] + ')';
                        document.getElementById('infoDetail').textContent = el[4] + ' • Kütle: ' + el[3] + ' • Periyot: ' + el[6] + ' • Grup: ' + el[7];
                        document.getElementById('infoDesc').textContent = el[8];
                        document.getElementById('ptInfo').style.borderColor = el[5];
                    };
                    cell.onmouseenter = () => { cell.style.boxShadow = '0 0 15px ' + el[5] + '80'; };
                    cell.onmouseleave = () => { cell.style.boxShadow = 'none'; };
                } else {
                    cell.className = 'pt-empty';
                }
                table.appendChild(cell);
            }
        }
    })();
    </script>
    """
    components.html(html_code, height=520)

    # Streamlit element seçici (yedek)
    st.markdown("---")
    styled_section("🔍 Element Detay Arama", "#0ea5e9")
    secilen = st.selectbox("Element Seç", [f"{e['no']}. {e['sembol']} — {e['ad']}" for e in PERIYODIK_TABLO], key="bv_el_sec")
    idx = next(i for i, e in enumerate(PERIYODIK_TABLO) if str(e['no']) == secilen.split(".")[0])
    el = PERIYODIK_TABLO[idx]

    _render_html(f"""
    <div style="background:#0f172a;border-radius:16px;padding:20px;margin:12px 0;border:2px solid {el['renk']}40;
                 display:flex;gap:20px;align-items:center">
        <div style="min-width:90px;text-align:center;background:{el['renk']}15;border-radius:14px;padding:18px;
                     border:2px solid {el['renk']}30">
            <div style="font-size:0.7rem;color:#94a3b8 !important">{el['no']}</div>
            <div style="font-size:2.8rem;font-weight:900;color:{el['renk']} !important">{el['sembol']}</div>
            <div style="font-size:0.7rem;color:#94a3b8 !important">{el['kutle']}</div>
        </div>
        <div>
            <div style="font-weight:800;color:#e0e7ff !important;font-size:1.3rem">{el['ad']}</div>
            <div style="font-size:0.85rem;color:{el['renk']} !important;margin-bottom:6px">{el['grup']} • Atom Kütlesi: {el['kutle']}</div>
            <div style="font-size:0.88rem;color:#94a3b8 !important;line-height:1.6">{el['bilgi']}</div>
        </div>
    </div>
    """)


def _render_bilim_tarihi():
    """Bilim tarihi kilometre taşları."""
    styled_section("📜 Bilim Tarihi — Kilometre Taşları", "#f59e0b")

    for i, bt in enumerate(BILIM_TARIHI):
        _render_html(f"""
        <div style="display:flex;gap:16px;align-items:center;margin-bottom:6px;padding:10px 16px;
                     background:#0f172a;border-radius:12px;
                     border-left:4px solid {'#0ea5e9' if i%2==0 else '#f59e0b'}">
            <div style="font-size:1.8rem;min-width:35px">{bt['ikon']}</div>
            <div style="min-width:70px;font-weight:700;color:#0ea5e9 !important;font-size:0.85rem">{bt['yil']}</div>
            <div style="font-size:0.83rem;color:#94a3b8 !important">{bt['olay']}</div>
        </div>
        """)


def _render_kodlama_dersleri():
    """Adım adım Python dersleri."""
    styled_section("📖 Python Kodlama Dersleri", "#10b981")

    _render_html("""
    <div class="bv-card" style="text-align:center;border-color:rgba(16,185,129,0.3)">
        <div style="font-size:2rem;margin-bottom:6px">🐍📖</div>
        <div style="font-weight:700;color:#bbf7d0 !important;font-size:1rem">Sıfırdan Python — Adım Adım</div>
        <div style="color:#86efac !important;font-size:0.85rem">Her ders bir öncekinin üzerine inşa edilir. Sırayla ilerle!</div>
    </div>
    """)

    for d in KODLAMA_DERSLERI:
        seviye_renk = "#10b981" if d['seviye'] == 'Başlangıç' else "#f59e0b"
        with st.expander(f"📖 Ders {d['ders']}: {d['ad']} ({d['seviye']})", expanded=(d['ders'] <= 2)):
            st.markdown(d['icerik'])

            st.markdown("**Örnek Kod:**")
            st.code(d['kod'], language="python")

            _render_html(f"""
            <div style="background:rgba(16,185,129,0.08);border-radius:10px;padding:12px;margin-top:8px;
                         border-left:3px solid {seviye_renk}">
                <div style="font-weight:700;color:#bbf7d0 !important;font-size:0.85rem">🎯 Görev:</div>
                <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">{d['gorev']}</div>
            </div>
            """)

            st.text_area(f"Çözümünü yaz (Ders {d['ders']}):", key=f"bv_ders_{d['ders']}",
                          height=100, placeholder="# Kodunu buraya yaz...")


def _render_eglenceli_bilim():
    """Çocuklar için wow faktörlü bilim gerçekleri — her seferde 10 yeni."""
    import random as _r
    styled_section("🎪 Eğlenceli Bilim — Bunu Biliyor Muydun?", "#ec4899")

    _render_html(f"""
    <div class="bv-card" style="text-align:center;border-color:rgba(236,72,153,0.3)">
        <div style="font-size:2.5rem;margin-bottom:6px">🤯🔬✨</div>
        <div style="font-weight:700;color:#fce7f3 !important;font-size:1.1rem">Bilim Hic Bu Kadar Eglenceli Olmamisti!</div>
        <div style="color:#94a3b8 !important;font-size:0.78rem;margin-top:4px">Havuzda {len(EGLENCELI_BILIM)} ilginc bilgi — her seferde 10 yenisi!</div>
    </div>
    """)

    # Rastgele 10 bilgi sec (butona basinca yenile)
    if "bv_eglenceli_seed" not in st.session_state:
        st.session_state["bv_eglenceli_seed"] = _r.randint(0, 999999)

    if st.button("Yeni 10 Ilginc Bilgi Uret", key="bv_eglenceli_yenile", type="primary", use_container_width=True):
        st.session_state["bv_eglenceli_seed"] = _r.randint(0, 999999)
        st.rerun()

    rng = _r.Random(st.session_state["bv_eglenceli_seed"])
    secilen = rng.sample(EGLENCELI_BILIM, min(10, len(EGLENCELI_BILIM)))

    for i, bilgi in enumerate(secilen, 1):
        _render_html(f"""
        <div class="bv-card" style="border-left:4px solid #ec4899">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                <span style="background:#ec489920;color:#ec4899;padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:700">{i}/10</span>
                <span style="font-weight:700;color:#e0f2fe !important;font-size:1rem">{bilgi['baslik']}</span>
            </div>
            <div style="color:#94a3b8 !important;font-size:0.85rem;line-height:1.6">{bilgi['bilgi']}</div>
        </div>
        """)


def _render_bilim_quizi():
    """Bilim bilgi yarışması — sınırsız sorulu."""
    import random as _r
    styled_section("🎮 Bilim & Kodlama Quizi", "#eab308")

    sk = "bv_quiz"
    if sk not in st.session_state:
        st.session_state[sk] = {"skor": 0, "toplam": 0}

    # Hem sabit havuz hem generator'dan sınırsız soru
    tum_sorular = BILIM_OYUN_SORULARI + BilimQuizGenerator.uret(10)
    if st.button("🎲 Yeni Soru!", key="bv_quiz_new", type="primary"):
        st.session_state["bv_quiz_soru"] = _r.choice(tum_sorular)

    if "bv_quiz_soru" in st.session_state:
        s = st.session_state["bv_quiz_soru"]

        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:28px;text-align:center;margin:12px 0;
                     border:2px solid rgba(234,179,8,0.3)">
            <div style="font-size:1.2rem;font-weight:700;color:#e0e7ff !important">{s['soru']}</div>
        </div>
        """)

        cols = st.columns(2)
        for idx, opt in enumerate(s.get("secenekler", [])):
            with cols[idx % 2]:
                if st.button(opt, key=f"bv_quiz_opt_{idx}", use_container_width=True):
                    st.session_state[sk]["toplam"] += 1
                    if opt == s["cevap"]:
                        st.session_state[sk]["skor"] += 1
                        st.success(f"🎉 Doğru! {s.get('aciklama', '')}")
                    else:
                        st.error(f"❌ Yanlış! Doğru: **{s['cevap']}** — {s.get('aciklama', '')}")

    skor = st.session_state[sk]
    if skor["toplam"] > 0:
        _render_html(f"""
        <div style="text-align:center;margin-top:12px;font-weight:700;color:#eab308 !important">
            🏆 Skor: {skor['skor']}/{skor['toplam']}
        </div>
        """)


def _render_insan_vucudu():
    """Insan vucudu sistemleri — her seferde 5 yeni bilgi."""
    import random as _r
    styled_section("Insan Vucudu Sistemleri", "#ef4444")

    # Sistem kartlari
    for sistem in VUCUT_SISTEMLERI:
        with st.expander(f"{sistem['ad']}", expanded=False):
            _render_html(f"""
            <div style="background:#0f172a;border-radius:14px;padding:16px;border-left:4px solid #ef4444">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:6px">Organlar:</div>
                <div style="color:#94a3b8 !important;font-size:0.85rem;margin-bottom:10px">{sistem['organlar']}</div>
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:4px">Ilginc Bilgi:</div>
                <div style="color:#fca5a5 !important;font-size:0.85rem;line-height:1.6">{sistem['bilgi']}</div>
            </div>
            """)

    # Ek ilginc bilgiler havuzu
    _VUCUT_BILGILERI = [
        ("Kalp", "Kalp gunde 100.000 kez atar, yilda 36.5 milyon. Bir omurde 2.5 milyar kez!"),
        ("Kan", "Vucut 5 litre kan icerir. Kan hucresi 120 gunde yenilenir. Gunde 200 milyar yeni kirmizi hucre uretilir."),
        ("Beyin", "Beyin vucut agirliginin %2'si ama enerjinin %20'sini kullanir. Uyanikken 20 watt uretir."),
        ("Kemik", "Bebekler 300 kemikle dogar, yetiskinlerde 206'ya duser. Kemik celikten 4 kat guclu!"),
        ("Akciger", "Akciger acilsa 70 m2 — tenis kortu! Gunde 20.000 nefes. Sag akciger soldan buyuk."),
        ("Goz", "Goz 10 milyon renk ayirt eder. Goz kaslari gunde 100.000+ hareket yapar. Goz kirpma 0.1 sn surer."),
        ("Kulak", "Kulak kemikleri vucudun en kucuk kemikleri. Ic kulak denge saglar. Kulak kireci 6 ayda yenilenir."),
        ("Deri", "Deri en buyuk organ — 1.5-2 m2. Gunde 30.000-40.000 olu hucre dokulur. 7 yilda tamamen yenilenir."),
        ("Mide", "Mide asidi pH 1-2, metali eritecek gucte! Mide kendini 3-4 gunde yeniler."),
        ("Karaciger", "Karaciger 500+ gorev yapar. Kendini yenileyebilen tek organ! %25'i kalsa bile tam boyutuna buyur."),
        ("Bobrek", "Bobrekler gunde 180 litre kan filtreler ama 1.5 litre idrar uretir — %99 geri emilir!"),
        ("Sinir", "Sinir sinyalleri 430 km/s hizla iletilir. Vucut 75 km sinir icerir."),
        ("Kas", "Vucutta 600+ kas var. En guclu kas: cigneme kasi. Gulmek 17, somurtmak 43 kas kullanir."),
        ("Dis", "Dis minesi vucudun en sert maddesi. Yetiskinde 32 dis. Dis celikten bile sert!"),
        ("Tirnak", "Tirnak ayda 3mm uzar. El tirnaklari ayak tirnaklarindan hizli. Orta parmak tirnak en hizli."),
        ("Sac", "Sac gunde 0.35 mm uzar. Kafa derisinde 100.000 tel sac var. Gunde 50-100 tel dokulur."),
        ("Ter", "Vucut 2-4 milyon ter bezi icerir. Ter %99 sudur. Stres teri farkli koklu!"),
        ("Bagisiklik", "Bagisiklik sistemi her gun milyonlarca mikrobu yok eder. Ates aslinda savunma mekanizmasi!"),
        ("DNA", "Her hucrede 2 metre DNA var. Tum vucut DNA'si gunes'e 600 kez gidip gelir."),
        ("Hormon", "100+ hormon var. Adrenalin 3 saniyede etki gosterir. Oksitosin 'sevgi hormonu' sarildikca salgalanir."),
        ("Nefes", "Hapsirik 160 km/s hizla cikar! Bir omurde 500 milyon nefes. Oflersen soguk, ufflersen sicak hava cikar."),
        ("Parmak Izi", "Hic kimsenin parmak izi ayni degil — ikizlerin bile! Koalalar insana benzer parmak izine sahip."),
        ("Ses", "Ses telleri saniyede 100-1000 kez titresir. Kadinlarda daha ince — kisa ses telleri."),
        ("Uyku", "Bir omurde 25 yil uyuruz. REM uykusunda kaslar felc olur. Beyin uykuda ogreniyor!"),
        ("Tukuruk", "Bir omurde 35.000 litre tukuruk uretilir — 2 yuzme havuzu! Tukuruk agri kesici icerir."),
        ("Burun", "Burun 1 trilyon koku ayirt edebilir. Tat almamin %80'i koklamadan gelir."),
        ("Hickirik", "Hickirik diyafram spazmdir. Fetusler anne karninda hickirir! En uzun hickirik 68 yil surmus."),
        ("Goz Yasi", "3 cesit goz yasi var: bazal, refleks, duygusal. Duygusal yaslar farkli kimyasal icerir."),
        ("Dirsek", "Dirsek vurunca karincalanma — ulnar sinir yuzeysel gectigindan. 'Komik kemik' aslinda sinir!"),
        ("Iskelet", "Iskelet 10 yilda tamamen yenilenir. Yeni dogan bebeklerin diz kapagi yok — 2-6 yasinda olusur."),
        ("Alyuvar", "Kirmizi kan hucreleri cekirdeksiz — daha fazla oksijen tasisin. 120 gun yasar, dalakta yok edilir."),
        ("Akyuvar", "Beyaz kan hucreleri bakterileri yutar! Iltihap olustugunda bolgeye kosar — cerahat aslinda olu akyuvar."),
        ("Lenf", "Lenf sistemi vucudun 'kanalizasyonu'. 600+ lenf dugumu var. Bogaz sismesi = lenf dugumleri calisiyor."),
        ("Tiroid", "Tiroid kelebek seklinde, boyunda. Metabolizmayi kontrol eder. Az calisirsa kilo alinir, cok calisirsa zayiflanir."),
        ("Pankreas", "Pankreas hem sindirim enzimi hem insulin uretir. Diyabet = insulin eksikligi. Gunde 1 litre sindirim suyu."),
        ("Dalak", "Dalak eski kan hucrelerini yok eder ve yenilerini depolar. Dalak cikarilsa yasanir ama enfeksiyona acik kalir."),
        ("Apandis", "Apandis eskiden gereksiz saniliyordu ama faydali bakteriler icin depo gorevi goruyor!"),
        ("Safra", "Safra kesesi yaglari sindirmek icin safra depolar. Safra tasi olusursa siddetli agri yapar. Cikarilabilir."),
        ("Adrenal", "Adrenal bezler bobrek ustunde. Adrenalin 3 saniyede etki gosterir — kalp hizlanir, kaslar gerilir, goz bebeyi buyur."),
        ("Hipofiz", "Hipofiz bezi bezelye buyuklugunde ama 'hormonlarin sefi'. Buyume, ureme, stres — hepsini yonetir."),
        ("Epifiz", "Epifiz bezi melatonin salgilar — uyku duzeni! Karanlikta aktif, isikta durur. 'Ucuncu goz' de denir."),
        ("Timus", "Timus cocuklukta buyuk, yetiskinlikte kuculur. T hucreleri burada egitilir — bagisikligin okulu!"),
        ("Korti̇zol", "Kortizol stres hormonu. Sabah en yuksek, gece en dusuk. Kronik stres = yuksek kortizol = saglik sorunlari."),
        ("Melatonin", "Melatonin karanlikta salgilanir. Mavi isik (telefon) melatonini bastir — bu yuzden gece telefon uyku bozar."),
        ("Endorfin", "Endorfin dogal agri kesici — morfinten 40 kat guclu! Spor, gulme, cikolata salgilatir. 'Mutluluk hormonu'."),
        ("Serotonin", "Serotoninon %95'i bagirsklarda uretilir, beyinde degil! Mutluluk, istah, uyku — hepsini etkiler."),
        ("Dopamin", "Dopamin odul hormonu. Bir hedef tamamladiginda beyni odullendirir. Sosyal medya 'like' dopamin patlamasi yaratir."),
        ("Oksitosin", "Oksitosin sarildikca, dokundukca salgilanir. 'Bag kurma hormonu'. Annelerde dogumda zirvede."),
        ("Testosteron", "Testosteron erkeklerde fazla ama kadinlarda da var. Kas, kemik, ses kalinligi, enerji — hepsini etkiler."),
        ("Ostrojen", "Ostrojen kadinlarda ana hormon. Kemik sagligi, cilt, hafiza — yuzlerce gorevi var."),
        ("Insulin", "Insulin kan sekerini duzenler. Tip 1 diyabet: vucut insulin uretmez. Tip 2: insulin direnci gelisir."),
        ("Hemoglobin", "Hemoglobin kanda oksijen tasir — demir icerir, bu yuzden kan kirmizi! 1 alyuvarda 270 milyon hemoglobin."),
        ("Miyelin", "Miyelin kilifi sinirleri kaplar — elektrik yalitimi gibi. MS hastaliginda miyelin hasar gorur."),
        ("Kollajen", "Kollajen vucuttaki en bol protein — %30! Deri, kemik, kirdalak hep kollajen. Yaslandikca azalir — kirisiklik."),
        ("Keratin", "Sac, tirnak, dis minesi keratin icerir. Keratin cok dayankli — asit ve alkaliye direncli!"),
        ("Melanin", "Melanin cilt rengini belirler. Gunes melanin uretimini artirir = bronzlasma. Albinizmde melanin yok."),
        ("Vitamin D", "Vitamin D gunes isigiyla ciltte uretilir. Kemik sagligi icin sart. Eksikligi depresyon yapabilir."),
        ("Vitamin C", "Insanlar vitamin C uretemez — meyve yemelisiniz! Eksikligi skorbut (dis eti kanamasi) yapar. Guineadan kesfedildi."),
        ("Demir", "Vucut 3-4 gram demir icerir — civi yapacak kadar! %70'i hemoglobinde. Eksikligi kansizlik yapar."),
        ("Kalsiyum", "Vucuttaki kalsiyumun %99'u kemiklerde. Kas kasilmasi, sinir iletimi, kan pihtilasmasi — kalsiyum sart."),
        ("Magnezyum", "Magnezyum 300+ enzim reaksiyonunda gorev yapar! Kas krampi genellikle magnezyum eksikligi."),
        ("Cinko", "Cinko bagisiklik, yara iyilesmesi, tat alma — hepsinde gorevli. Eksikligi tat ve koku kaybina yol acar."),
        ("Antibiyotik Direnci", "Gereksiz antibiyotik kullanimi direncli bakteri yaratir. 2050'de antibiyotik direnci #1 olum nedeni olabilir."),
        ("Mikrobiom", "Bagirsaklarda 100 trilyon bakteri yasar — insan hucrelerinden fazla! 2 kg agirliginda. 'Ikinci beyin' denir."),
        ("Probiyotik", "Yogurt, kefir, tursu icindeki canli bakteriler bagirsak sagligini destekler. Her gün farkli probiyotik iyi."),
        ("Otoimmun", "Otoimmun hastalikte bagisiklik sistemi kendi vucuduna saldiri. 80+ cesidi var: MS, lupus, tip 1 diyabet."),
        ("Alerji", "Alerji bagisiklik sisteminin zararsiz seylere asiri tepkisi. Polen, findik, kedi tuyu — hep ayni mekanizma."),
        ("Ates", "37.5°C ustu ates. Ates aslinda savunma — virusler sicakta zayiflar! 40°C ustu tehlikeli."),
        ("Opsonizasyon", "Antikorlar mikrobu 'isaretler', fagositler onu bulup yutar. Asiler bu sistemi egitir."),
        ("Stem Hucre", "Kok hucreler herhangi hucreye donusebilir! Kemik iligi, gobe kordonu — tip devrimi potansiyeli."),
        ("Telomer", "Telomerler kromozom ucundaki koruyucu kapak. Her bolunmede kisalir — yaslanmanin saati! Stres kisaltir."),
        ("Epigenetik", "Genler degismeden gen ifadesi degisebilir — diet, stres, cevre genleri acar/kapar. Nesiller arasi aktarilir."),
        ("REM Uykusu", "REM'de gozler hizla hareket eder, beyin aktif ama vucut felc. Ruya burada gorulur. Hafiza islenir."),
        ("Circadian Ritim", "Vucut saati 24 saat dongusu. Isik reseptörleri gozde. Jet lag = bozulmus circadian ritim."),
        ("Bagisiklik Hafizasi", "Bagisiklik sistemi hastaliklari hatirlari! Ikinci kez ayni virus geldiginde hizla yok eder — asi mantigi."),
        ("Fagosit", "Fagositler mikroplari yutar ve sindirir. Norofiller (en yaygin) 5 saat yasar — surekli yenisi uretilir."),
        ("Histamin", "Histamin alerjik tepkide salgilanir — kasinti, sislik, hapsirik. Antihistaminikler bunu engeller."),
        ("Kolagraf", "EKG kalbin elektrik aktivitesini olcer. P dalgasi, QRS kompleksi, T dalgasi — her biri farkli asama."),
        ("Tansiyon", "120/80 mmHg normal. Ust: sistolik (kalp kasilduginda). Alt: diastolik (kalp gevsediginde)."),
        ("Nabiz", "Istirahat nabzi 60-100/dk. Sporcularda 40 olabilir — kalp guclu pompaldigindan. Bebeklerde 120-160."),
        ("Oksijen", "Beyin 3 dakika oksijensiz kalirsa hasar baslar. 5 dakikada geri donulemez hasar. Kalp 20 dakika dayanir."),
        ("Karbondioksit", "CO2 fazlasi kani asitlesitirir. Solunumun asil tetikleyicisi O2 azalmasi degil, CO2 artisi!"),
        ("Embriyoloji", "Bebek 9 ayda tek hucreden 37 trilyon hucreye buyur! Ilk 8 hafta tum organlar sekilenir."),
        ("Puberte", "Ergenlik hipofiz-gonad ekseninin aktive olmasiyla baslar. Kizlarda 8-13, erkeklerde 9-14 yas."),
        ("Dogum", "Dogumda bebegin kafatasi kemikleri birbirine binebilir — dogum kanalindan gecmek icin! Sonra duzzelir."),
        ("Yas Alma", "Yaslanma = telomer kisalmasi + oksidatif stres + hucre hasar birikimi. 120 yas biyolojik sinir."),
        ("Refleks", "Diz refleksi omurilikten yonetilir — beyin karar vermez! En hizli refleks 0.01 saniye."),
        ("Agri", "Agri uyari sistemi. Konjenital analjezi = agri hissetmemek — tehlikeli cunku yaralanma fark edilmez!"),
        ("Fantom Agri", "Ampute edilmis uzuvda agri hissedilir! Beyin hala o uzvu 'gorur'. %80 amputede olur."),
        ("Sinestezi", "Bazi insanlarda duyular karisir — sayilari renkli gorur, muzigi tadar! 100 kisiden 4'unde var."),
        ("Deja Vu", "Insanlarin %70'i deja vu yasamisdir! Beyin hafiza ve algi arasinda kisa devre yapar."),
        ("Plasebo", "Seker hap bile iyilestirmis olabilir — plasebo etkisi %30-40! Beyin inanirsa vucut tepki verir."),
        ("Nosebo", "Plasebonun tersi — zararli olacagina inanirsan yan etki yasarsin. Beklenti vucudu etkiler!"),
        ("Cift Beyin", "Beyin sag ve sol yarikure. Sol: mantik, dil. Sag: yaraticilik, muzik. Corpus callosum baglar."),
        ("Hipokampus", "Hipokampus hafiza merkezi — denizati seklinde! Hasar gorurse yeni ani olusturulamaz (amnezi)."),
        ("Amigdala", "Amigdala korku ve duygusal tepki merkezi. PTSD'de asiri aktif. Meditasyon amigdalayi kucultur!"),
        ("Noropastisite", "Beyin surekli degisir — yeni sinir baglantilari olusur! Ogrenme = yeni sinaps. 'Kullan ya da kaybet'."),
        ("Biyoritim", "Vucut sicakligi gunde 1°C degisir — sabah dusuk, aksam yuksek. Performans ogleden sonra zirve yapar."),
        ("Gozyasi Turleri", "Bazal goz yasi goz nemlendirir, refleks goz yasi sogan keserken cikar, duygusal goz yasi ozel protein icerir."),
        ("Vucut Suyu", "Yetiskin vucut %60 sudur. Beyin %75, kan %83, kemik %22 su. Gunde 2.5 litre su kaybederiz."),
    ]

    # Her seferde 5 yeni bilgi
    if "bv_vucut_seed" not in st.session_state:
        st.session_state["bv_vucut_seed"] = _r.randint(0, 999999)

    st.markdown("---")
    if st.button("Yeni 5 Ilginc Vucut Bilgisi Uret", key="bv_vucut_yenile", type="primary", use_container_width=True):
        st.session_state["bv_vucut_seed"] = _r.randint(0, 999999)
        st.rerun()

    rng = _r.Random(st.session_state["bv_vucut_seed"])
    secilen = rng.sample(_VUCUT_BILGILERI, min(5, len(_VUCUT_BILGILERI)))

    _render_html(f'<div style="text-align:center;color:#94a3b8;font-size:0.75rem;margin-bottom:8px">Havuzda {len(_VUCUT_BILGILERI)} bilgi — her seferde 5 yenisi</div>')

    for i, (baslik, bilgi) in enumerate(secilen, 1):
        _render_html(f"""
        <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;border-left:4px solid #ef4444">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
                <span style="background:#ef444420;color:#ef4444;padding:2px 8px;border-radius:10px;font-size:0.68rem;font-weight:700">{i}/5</span>
                <span style="font-weight:700;color:#fca5a5 !important;font-size:0.95rem">{baslik}</span>
            </div>
            <div style="color:#94a3b8 !important;font-size:0.83rem;line-height:1.5">{bilgi}</div>
        </div>
        """)


def _render_uzay_evren():
    """Uzay & Evren — güneş sistemi, galaksiler, kara delikler, uzay tarihi."""
    styled_section("🪐 Uzay & Evren", "#6366f1")

    _render_html("""
    <div style="background:linear-gradient(135deg,#0c0024,#1a0a3e,#000033);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid rgba(99,102,241,0.4);text-align:center;position:relative;overflow:hidden">
        <div style="position:absolute;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at 30% 30%,rgba(99,102,241,0.05),transparent 50%)"></div>
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:10px">🌌🪐🔭🚀🌍</div>
            <h2 style="color:#e0e7ff !important;font-size:1.5rem;margin:0 0 8px !important">Evrenin Sonsuz Derinliklerini Keşfet!</h2>
            <p style="color:#a5b4fc !important;font-size:0.85rem;margin:0 !important">Güneş Sistemi, galaksiler, kara delikler, meteorlar, uzay tarihi — hepsi burada!</p>
        </div>
    </div>
    """)

    sub = st.tabs(["🪐 3D Güneş Sistemi", "📋 Gezegen Detayları", "🌌 Evrenin Sırları"])

    with sub[0]:
        styled_section("🪐 3D İnteraktif Güneş Sistemi", "#f59e0b")
        st.caption("Gezegenler yörüngede dönüyor! Bir gezegene tıkla bilgi kartını gör.")
        import streamlit.components.v1 as components

        solar_html = """
        <style>
        #solarCanvas { display:block; margin:0 auto; border-radius:20px; border:2px solid #1e293b; cursor:pointer; }
        #solarInfo {
            background:linear-gradient(135deg,#0f172a,#1e293b); border-radius:16px;
            padding:18px; margin-top:10px; border:2px solid #334155;
            display:flex; gap:16px; align-items:center; min-height:70px;
        }
        #solarInfo .si-emoji { font-size:2.5rem; min-width:50px; text-align:center; }
        #solarInfo .si-name { font-size:1.1rem; font-weight:700; color:#e0e7ff; }
        #solarInfo .si-detail { font-size:0.75rem; color:#7dd3fc; margin-top:2px; }
        #solarInfo .si-desc { font-size:0.78rem; color:#94a3b8; margin-top:4px; line-height:1.5; }
        </style>
        <canvas id="solarCanvas" width="750" height="420"></canvas>
        <div id="solarInfo">
            <div class="si-emoji">🪐</div>
            <div>
                <div class="si-name">Bir gezegene tıkla!</div>
                <div class="si-detail">Güneş Sistemi — 8 gezegen + Güneş</div>
                <div class="si-desc">Gezegenler elips yörüngede Güneş etrafında döner. İç gezegenler kayaç, dış gezegenler gaz devidir.</div>
            </div>
        </div>
        <script>
        (function(){
            const c = document.getElementById('solarCanvas');
            const ctx = c.getContext('2d');
            const cx = c.width/2, cy = c.height/2;
            const info = document.getElementById('solarInfo');

            // Gezegen verileri: [ad, emoji, yörünge_r, boyut, renk, hız, tip, çap, uzaklık, bilgi]
            const planets = [
                ["Güneş","☀️",0,22,"#fbbf24",0,"Yıldız","1.392.000 km","0","Her saniye 600M ton hidrojeni helyuma çevirir. 4.6 milyar yaşında!"],
                ["Merkür","☿",45,4,"#94a3b8",4.15,"Kayaç","4.879 km","58M km","Güneş'e en yakın. Gündüz 430°C, gece -180°C!"],
                ["Venüs","♀",65,6,"#f59e0b",1.62,"Kayaç","12.104 km","108M km","En sıcak gezegen (465°C)! Ters döner — güneş batıdan doğar."],
                ["Dünya","🌍",88,6,"#3b82f6",1.0,"Kayaç","12.742 km","150M km","Bilinen tek yaşam barındıran gezegen. %71 su."],
                ["Mars","♂",110,5,"#ef4444",0.53,"Kayaç","6.779 km","228M km","Kızıl gezegen. Olympus Mons 21.9 km — en yüksek dağ!"],
                ["Jüpiter","♃",145,14,"#f97316",0.084,"Gaz Devi","139.820 km","778M km","En büyük gezegen. Büyük Kırmızı Leke 350 yıllık fırtına!"],
                ["Satürn","♄",178,12,"#eab308",0.034,"Gaz Devi","116.460 km","1.4Mr km","Halkaları buz ve kayadan. Yoğunluğu sudan az — yüzer!"],
                ["Uranüs","♅",200,8,"#06b6d4",0.012,"Buz Devi","50.724 km","2.9Mr km","Yan yatık döner (98°). Bir mevsim 21 yıl!"],
                ["Neptün","♆",218,7,"#3b82f6",0.006,"Buz Devi","49.244 km","4.5Mr km","En hızlı rüzgarlar: 2100 km/s! Matematikle keşfedildi."],
            ];

            let time = 0;
            let selectedPlanet = null;

            function draw(){
                ctx.fillStyle = '#000011';
                ctx.fillRect(0,0,c.width,c.height);

                // Yıldızlar
                if(!draw.stars){
                    draw.stars = [];
                    for(let i=0;i<120;i++) draw.stars.push([Math.random()*c.width, Math.random()*c.height, Math.random()*1.5+0.3]);
                }
                draw.stars.forEach(s => {
                    ctx.beginPath();
                    ctx.arc(s[0],s[1],s[2]*((Math.sin(time*0.02+s[0])*0.3)+0.7),0,Math.PI*2);
                    ctx.fillStyle='rgba(255,255,255,'+(0.3+Math.random()*0.5)+')';
                    ctx.fill();
                });

                planets.forEach((p,i) => {
                    const orbitR = p[2];
                    const size = p[3];
                    const color = p[4];
                    const speed = p[5];

                    if(orbitR > 0){
                        // Yörünge çizgisi
                        ctx.beginPath();
                        ctx.ellipse(cx,cy,orbitR,orbitR*0.35,0,0,Math.PI*2);
                        ctx.strokeStyle = 'rgba(99,102,241,0.12)';
                        ctx.lineWidth = 1;
                        ctx.stroke();

                        // Gezegen konumu
                        const angle = time * speed * 0.01;
                        const px = cx + Math.cos(angle) * orbitR;
                        const py = cy + Math.sin(angle) * orbitR * 0.35;

                        p._x = px; p._y = py;

                        // Satürn halkası
                        if(p[0] === "Satürn"){
                            ctx.beginPath();
                            ctx.ellipse(px,py,size*1.8,size*0.4,0.3,0,Math.PI*2);
                            ctx.strokeStyle = '#eab30888';
                            ctx.lineWidth = 3;
                            ctx.stroke();
                        }

                        // Gezegen
                        ctx.beginPath();
                        ctx.arc(px,py,size,0,Math.PI*2);
                        const grad = ctx.createRadialGradient(px-size*0.3,py-size*0.3,0,px,py,size);
                        grad.addColorStop(0, color);
                        grad.addColorStop(1, color+'88');
                        ctx.fillStyle = grad;
                        ctx.fill();

                        // Seçili gezegen vurgu
                        if(selectedPlanet === i){
                            ctx.beginPath();
                            ctx.arc(px,py,size+4,0,Math.PI*2);
                            ctx.strokeStyle = '#fff';
                            ctx.lineWidth = 2;
                            ctx.stroke();
                        }

                        // İsim
                        ctx.fillStyle = '#94a3b8';
                        ctx.font = '9px Inter, sans-serif';
                        ctx.textAlign = 'center';
                        ctx.fillText(p[0], px, py + size + 12);
                    } else {
                        // Güneş
                        p._x = cx; p._y = cy;
                        const glow = 28 + Math.sin(time*0.05)*4;
                        const sunGrad = ctx.createRadialGradient(cx,cy,0,cx,cy,glow);
                        sunGrad.addColorStop(0,'#fef08a');
                        sunGrad.addColorStop(0.4,'#fbbf24');
                        sunGrad.addColorStop(0.7,'#f59e0b');
                        sunGrad.addColorStop(1,'#f59e0b00');
                        ctx.beginPath();
                        ctx.arc(cx,cy,glow,0,Math.PI*2);
                        ctx.fillStyle = sunGrad;
                        ctx.fill();

                        ctx.beginPath();
                        ctx.arc(cx,cy,size,0,Math.PI*2);
                        ctx.fillStyle = '#fbbf24';
                        ctx.fill();

                        if(selectedPlanet === 0){
                            ctx.beginPath();ctx.arc(cx,cy,size+5,0,Math.PI*2);
                            ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
                        }
                        ctx.fillStyle='#92400e';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
                        ctx.fillText('☀️',cx,cy+4);
                    }
                });

                time++;
                requestAnimationFrame(draw);
            }

            // Tıklama — en yakın gezegeni bul
            c.addEventListener('click', e => {
                const rect = c.getBoundingClientRect();
                const mx = e.clientX - rect.left;
                const my = e.clientY - rect.top;

                let closest = -1, minDist = Infinity;
                planets.forEach((p,i) => {
                    if(p._x !== undefined){
                        const d = Math.sqrt((mx-p._x)**2 + (my-p._y)**2);
                        if(d < p[3]+15 && d < minDist){ minDist = d; closest = i; }
                    }
                });

                if(closest >= 0){
                    selectedPlanet = closest;
                    const p = planets[closest];
                    info.innerHTML = `
                        <div class="si-emoji">${p[1]}</div>
                        <div>
                            <div class="si-name">${p[0]}</div>
                            <div class="si-detail">${p[6]} • Çap: ${p[7]} • Uzaklık: ${p[8]}</div>
                            <div class="si-desc">${p[9]}</div>
                        </div>
                    `;
                    info.style.borderColor = p[4];
                }
            });

            draw();
        })();
        </script>
        """
        components.html(solar_html, height=560)

    with sub[1]:
        styled_section("📋 Gezegen Detay Kartları", "#0ea5e9")
        for g in GUNES_SISTEMI:
            emoji = g['ad'].split(' ')[0]
            with st.expander(f"{emoji} {g['ad'].split(' ',1)[1] if ' ' in g['ad'] else g['ad']}", expanded=False):
                _render_html(f"""
                <div style="display:flex;gap:16px;align-items:center">
                    <div style="font-size:3rem;min-width:60px;text-align:center">{emoji}</div>
                    <div>
                        <div style="font-weight:700;color:#e0f2fe !important;font-size:1.1rem">{g['ad']}</div>
                        <div style="font-size:0.8rem;color:#7dd3fc !important">{g['tip']} • Çap: {g['cap']} • Güneş'e Uzaklık: {g['uzaklik']}</div>
                        <div style="font-size:0.85rem;color:#94a3b8 !important;margin-top:6px;line-height:1.6">{g['bilgi']}</div>
                    </div>
                </div>
                """)

    with sub[2]:
        import random as _ruz
        styled_section("Evrenin Sirlari", "#8b5cf6")

        _UZAY_EK = [
            ("Karadelik", "Karadelik o kadar yogun ki 1 cay kasigi maddesi 6 milyar ton! Isik bile kacamaz. Zaman olay ufkunda neredeyse durur."),
            ("Samanyolu", "Samanyolu galaksisinde 200-400 milyar yildiz var. Merkezinde 4 milyon gunes kutleli dev karadelik Sagittarius A* var."),
            ("Isik Yili", "1 isik yili = 9.46 trilyon km! En yakin yildiz Proxima Centauri 4.24 isik yili. Mevcut teknolojiyle 70.000 yil surer."),
            ("Notrino", "Her saniye milyarlarca notrino vucudundan geciyor — hic birsey olmadan! Gunes'ten gelirler, maddeyle neredeyse hic etkilesmezler."),
            ("Kozmik Fon", "Evrenin her yerinde 2.7 Kelvin sicaklikta mikrodalga isini var — Buyuk Patlama'nin 'yankilari'. 1965'te kesfedildi."),
            ("Voyager 1", "Voyager 1 insanligin en uzak nesnesi — 24 milyar km uzakta! 1977'de firlatildi. Hala sinyal gonderiyor."),
            ("ISS", "Uluslararasi Uzay Istasyonu 90 dakikada Dunya'nin cevresini doner — gunde 16 gun dogumu ve batimi!"),
            ("Gunes Ruzgari", "Gunes saniyede 1 milyon ton parcacik firlatir. Dunya'nin manyetik alani bizi korur — yoksa atmosfer ucardi."),
            ("Ay Depremleri", "Ay'da depremler olur! Apollo astronotlari sismometre birakti. Ay depremleri saatlerce surebilir."),
            ("Pluto", "Pluto 2006'da gezegen statüsünü kaybetti. Yuzeyi -230°C. Kalp seklinde buzul alan var (Sputnik Planitia)."),
            ("Europa", "Jupiter'in uydusu Europa'nin buzlu kabugunun altinda okyanus var! Yasam icin en umut verici yer."),
            ("Titan", "Saturn'un uydusu Titan'da metan golleri var! Atmosferi Dunya'dan kalin. Yagmur yagar ama su degil, metan."),
            ("Galaksi Carpismasi", "Samanyolu ve Andromeda galaksisi 4.5 milyar yil sonra carpisacak! Ama yildizlar arasi mesafe o kadar buyuk ki hicbir yildiz carpismaz."),
            ("Pulsar", "Pulsarlar saniyede 716 kez donebilen notr yildizlardir! Bir cay kasigi maddesi 1 milyar ton agirliginda."),
            ("Gama Isinlari", "Gama isin patlamalari evrendeki en guclu olaylar — birkaç saniyede Gunes'in 10 milyar yilda urettigi enerjiyi acar!"),
            ("Uzay Coplugu", "Dunya yoreungesinde 34.000+ izlenen uzay coplugu var. 1 cm'lik parca kursuun hizinda gider — uyduyu yok edebilir."),
            ("Karanlik Madde", "Evrenin %27'si karanlik madde, %68'i karanlik enerji. Gorebiledigimiz madde sadece %5! Gerisini bilmiyoruz."),
            ("Mars Helikopteri", "Ingenuity Mars'ta ucan ilk hava araci! 72 ucus yapti. Mars atmosferi Dunya'nin %1'i kadar ince — ucmak cok zor."),
            ("Exogezegen", "5.000+ exogezegen kesfedildi! Bazilari 'sicak Jupiter' — yildizina cok yakin gaz devleri. Bazilari elmas gezegenler."),
            ("Ozon", "Ozon tabakasi 15-35 km yukseklikte. Ultraviyole isinlari %99 engeller. Montreal Protokolu ile korunuyor — 2066'da iyilesecek."),
            ("Yildiz Olumu", "Buyuk yildizlar supernova ile patlar — notr yildizi veya karadelik olusur. Kucuk yildizlar beyaz cuce olur."),
            ("Big Bang", "Evren 13.8 milyar yil once bir noktadan genislemeye basladi. Hala genisliyor — ve hizlaniyor!"),
            ("Uzay Yuruyusu", "Ilk uzay yuruyusu Alexei Leonov (1965). 12 dakika surdu. Giysisi sisti, zar zor geri dondu!"),
            ("Asteroid Kusagi", "Mars ile Jupiter arasinda milyonlarca asteroid var. En buyugu Ceres — cuce gezegen. Toplam kutlesi Ay'in %4'u."),
            ("Kuyrukluyildiz", "Kuyrukluyildizlar buz ve tozdan olusur — 'kirli kartopu'. Gunes'e yaklasinca kuyruk olusur, milyonlarca km uzar."),
            ("Nebula", "Nebula gaz ve toz bulutu — yildizlarin dogum yeri! Kartal Nebulasi'ndaki 'Yaratilis Sutunlari' 5 isik yili uzunlugunda."),
            ("Beyaz Cuce", "Gunes 5 milyar yil sonra beyaz cuce olacak — Dunya buyuklugunde ama Gunes kutlesinde. 1 cay kasigi 5 ton!"),
            ("Notr Yildiz", "Notr yildiz 20 km capinda ama Gunes'ten agir! 1 cay kasigi 1 milyar ton. Saniyede 716 kez donebilir."),
            ("Supernova", "Supernova patlamasi birkaç hafta tum galaksiden parlak olabilir! Vucudumuzdaki agir elementler supernovalardan gelir."),
            ("Magnetar", "Magnetar en guclu manyetik alana sahip nesne. Ay mesafesinden kredi kartini siler! Nadir — galakside 30 kadar."),
            ("Quasar", "Quasarlar evrendeki en parlak nesneler — tek galaksi trilyonlarca yildiz kadar parlak! Merkezdeki dev karadelik besler."),
            ("Oort Bulutu", "Gunes Sistemini saran Oort Bulutu 1 isik yili uzaklikta! Trilyonlarca buzlu cisim. Uzun periyotlu kuyrukluyildizlarin kaynagi."),
            ("Kuiper Kusagi", "Neptun otesinde Kuiper Kusagi var. Pluto burada. 100.000+ cisim. New Horizons 2015'te Pluto'yu ziyaret etti."),
            ("Hubble Sabiti", "Evren genisliyor — her megaparsek basina 70 km/s hizlaniyor! Hubble 1929'da kesfetti."),
            ("Kozmik Enflasyon", "Big Bang'den 10^-36 saniye sonra evren 10^26 kat genisledi! Gozlenebilir evren bu enflasyonun sonucu."),
            ("Coklu Evren", "Bazi fizikçiler sonsuz paralel evren oldugunu dusunur. Her kuantum kararda evren dallanir — Many Worlds yorumu."),
            ("Zaman Genisleme", "GPS uydulari Einstein'in zaman genislemesini hesaba katar! Yoksa konum 10 km sapardi. Yercekim zamani yavaslatir."),
            ("Gravitasyonel Dalga", "Einstein 1916'da ongordu, LIGO 2015'te olctu! Iki karadelik birlesince uzay-zaman titresir."),
            ("Hawking Isinimasi", "Karadelikler yavas yavas buharlasir! Stephen Hawking 1974'te kesfetti. Cok kucuk karadelikler patlayabilir."),
            ("Fermion Bozon", "Evren 2 parcaciktan olusur: fermionlar (madde) ve bozonlar (kuvvet). Higgs bozonu kutleyi verir."),
            ("Antimadde", "Her parcacigin anti-parcacigi var. Madde+antimadde = saf enerji! 1 gram antimadde = Hiroshima bombasi."),
            ("Sicim Teorisi", "Evren 10 veya 11 boyutlu olabilir — 7 boyut katlanmis gorunmez! Sicim teorisi tum kuvvetleri birlestirmeye calisir."),
            ("Kara Enerji", "Evrenin %68'i kara enerji — evrenin genislemesini hizlandiran gizemli kuvvet. Ne oldugunu bilmiyoruz!"),
            ("Kara Madde", "Evrenin %27'si kara madde — gormeyiz ama yercekimini hissederiz. Normal madde sadece %5!"),
            ("Gunes Lekesi", "Gunes lekeleri 3500°C — cevresinden 2000°C soguk. 11 yillik dongulerle artar/azalir. Dunyadaki iklimi etkiler."),
            ("Gunes Patlamasi", "Gunes patlamalari milyarlarca ton plazma firlattir. Buyugu elektrik sebekelerini cokertebilir! 1859 Carrington olayı."),
            ("Van Allen", "Dunya'nin etrafinda Van Allen radyasyon kusaklari var. Astronotlari korumak icin ozel kalkan gerekir."),
            ("Magnetosfer", "Dunya'nin manyetik alani gunes ruzgarindan korur. Olmasa atmosfer ucardi — Mars basina gelen bu."),
            ("Kuzey Isiklari", "Aurora gunes parcaciklari atmosferdeki gazlari uyarinca olusur. Yesil = oksijen, mor = nitrojen."),
            ("Merkur Gecisi", "Merkur Gunes onunden gecer — bir sonraki 2032'de. Cok nadir — yuzyilda 13-14 kez."),
            ("Venus Gecisi", "Venus gecisi ciftler halinde olur, arada 100+ yil. Son: 2012. Sonraki: 2117! Kimse goremeyecek."),
            ("Mars Gunu", "Mars'ta 1 gun = 24 saat 37 dakika. 1 yil = 687 Dunya gunu. Mevsimler var — Dunya'ya en benzer gezegen."),
            ("Jupiter Firtinasi", "Buyuk Kirmizi Leke 350 yildir devam eden dev firtina. Dunya'dan buyuk! Son yillarda kuculuyor."),
            ("Saturn Halkalari", "Saturn halkalari %99 buzdan olusur. Halka sistemi 280.000 km genislikte ama sadece 10 metre kalinliginda!"),
            ("Uranüs Egimi", "Uranüs 98 derece egik — yan yatiyor! Muhtemelen dev bir carpismadan. Mevsimler 21 yil surer."),
            ("Neptun Ruzgari", "Neptun'de 2.100 km/s ruzgar eser — Gunes Sistemi'nin en hizlisi! Neden bu kadar hizli bilmiyoruz."),
            ("Ceres", "Ceres Mars-Jupiter arasindaki en buyuk cisim. Cuce gezegen. Yuzeyinde buz ve tuz var. Yasam potansiyeli!"),
            ("Enceladus", "Saturn'un uydusu Enceladus'un buz catlarisindan su fiskiyeleri cikir! Altinda sicak okyanus. Yasam icin umut."),
            ("Ganymede", "Jupiter'in uydusu Ganymede Gunes Sistemi'nin en buyuk uydusu — Merkur'den bile buyuk! Manyetik alani var."),
            ("Io", "Jupiter'in uydusu Io en volkanik cisim! 400+ aktif yanardag. Jupiter'in cekimi ic isiyi uretir."),
            ("Triton", "Neptun'un uydusu Triton ters yonde doner — yakalanmis Kuiper cismi! Yuzeyinde nitrojen buzullari."),
            ("Haumea", "Haumea cuce gezegen — futbol topu seklinde! 4 saatte kendi etrafinda doner. 2 uydusu var."),
            ("Makemake", "Makemake Kuiper Kusagi'nin 2. en buyuk cuce gezegeni. Paskalya Adasi tanrisi adini tasir."),
            ("Eris", "Eris Pluto'dan buyuk cuce gezegen — Pluto'nun gezegenlikten cikarilmasina neden oldu! 96 AU uzakta."),
            ("Sedna", "Sedna en uzak bilinen cisimlerden — Gunes'e en yakin noktasi 76 AU! Yillik periyodu 11.400 yil."),
            ("Oumuamua", "2017'de ilk yildizlararasi ziyaretci goruldu! Puro seklinde, hiz alarak uzaklasti. Yabancilar mi?"),
            ("Borisov", "2I/Borisov ikinci yildizlararasi cisim (2019). Kuyrukluyildiz — baska bir yildiz sisteminden geldi."),
            ("JWST", "James Webb Uzay Teleskopu 2021'de firlatildi. Kizilotesi ile evrenin ilk yildizlarini goruyor!"),
            ("Starship", "SpaceX Starship insanlik tarihinin en buyuk roketi. Mars kolonisi hedefi. Tamamen yeniden kullanilabilir."),
            ("Artemis", "NASA Artemis programi insanlari tekrar Ay'a goturecek — bu sefer kalinacak! Ay ussu planlaniyor."),
            ("Mars Koloni", "Elon Musk 2030'larda Mars kolonisi hedefliyor. 1 yolculuk 6-9 ay. Donmek cok zor — tek yonlu bilet!"),
            ("Uzay Asansoru", "Uzay asansoru konsepti: 36.000 km kablo ile yeryuzunden yoreungeye. Karbon nanotup gerekli. Gelecek yuzyil?"),
            ("Dyson Kuresi", "Dyson Kuresi bir yildizi saran dev enerji toplayici. Tip II medeniyet bunu yapabilir. Henuz teorik."),
            ("Drake Denklemi", "Galaksideki iletisim kurabilecek medeniyet sayisini tahmin eder. Sonuc: 1 ile milyonlar arasi!"),
            ("Fermi Paradoksu", "Evren bu kadar buyukse neden hic uzayli goremedik? 200+ cozum onerisi var. En populer: Buyuk Filtre."),
            ("SETI", "SETI 60 yildir uzaydan akilli sinyal ariyor. Henuz bulunamadi. Ama evrendeki yildiz sayisi kumdan fazla!"),
            ("Goldilocks Bolgesi", "Yasanabilir bolge — ne cok sicak ne soguk. Su sivisi halinde kalabilir. Dunya tam ortasinda!"),
            ("TRAPPIST-1", "39 isik yili uzaktaki TRAPPIST-1 yildizinin 7 kayac gezegeni var — 3'u yasanabilir bolgede!"),
            ("Kepler-22b", "Kepler-22b ilk kesfedilen yasanabilir bolge gezegeni. Dunya'nin 2.4 kati buyuk. Su okyanuslari olabilir."),
            ("Proxima b", "En yakin yildizin gezegeni Proxima b yasanabilir bolgede! 4.24 isik yili. Ama yildiz patlamalari tehlikeli."),
            ("Uzay Turizmi", "Blue Origin ve Virgin Galactic uzay turizmi baslatttl. 11 dakikalik ucus $250.000-$450.000."),
            ("Uzay Madenciligi", "Asteroitlerde platin, altin, demir var. 16 Psyche asteroitinin degeri: $10 kentilyon! NASA 2029'da ziyaret edecek."),
            ("Uzay Coplugu Temizligi", "ESA 2025'te ilk uzay cop toplama misyonu: ClearSpace-1. Robotik kol ile eski uydu yakalayacak."),
            ("Radyo Teleskop", "FAST (Cin) dunyanin en buyuk radyo teleskopu — 500 metre cap! Uzayli sinyali arayabilir."),
            ("Kozmik Isinlar", "Kozmik isinlar uzaydan gelen yuksek enerjili parcaciklar. Bazilari supernova, bazilari karadeliklerden."),
            ("Uzay Elbisesi", "Uzay elbisesi 14 katman, 120 kg, 12 milyon dolar. Ic basinci korur, -150 ile +120°C arasi dayanir."),
            ("Uzayda Yemek", "ISS'te yemekler vakumlu paket veya konserve. Pizza bile var! Sivi kurecik seklinde suzulur."),
            ("Mikrogravite", "ISS'te astronotlar gunde 2 saat spor yapmali — kaslari ve kemikleri erir! 6 ayda %1-2 kemik kaybi."),
            ("Uzayda Yakit", "Roket yakiti agirlgin %90'i! Tsiolkovsky denklemi: delta-v = Isp * g * ln(m0/m1). Her km/s cok pahali."),
            ("Uzay Istasyonu Yoreungesi", "ISS 408 km yukseklikte, 27.600 km/s hizla doner. 90 dakikada Dunya turu. Gece uzerinden gecebildinizi gorebilirsiniz!"),
            ("Laika", "1957'de Laika kopek uzaya giden ilk canli oldu. Sputnik 2 ile firlatildi. Maalesef geri donemedi."),
            ("Gagarin", "Yuri Gagarin 1961'de uzaya cikan ilk insan. 108 dakikalik ucus. 'Dunya mavi!' dedi."),
            ("Apollo 11", "Neil Armstrong 1969'da Ay'a ayak basan ilk insan. 'Insan icin kucuk bir adim, insanlik icin dev bir sicirayis.'"),
            ("Challenger", "1986 Challenger faciasi — kalkistan 73 saniye sonra patladi. 7 astronot hayatini kaybetti. O-ring donmustu."),
            ("Hubble Teleskop", "Hubble 1990'dan beri 1.5 milyon gozlem yapti. 13.4 milyar isik yili uzagi gorebilir. Servis icin 5 kez ziyaret edildi."),
            ("Pluto Kalbi", "New Horizons 2015'te Pluto'yu yakindan goruntuledi. Yuzeyinde dev kalp seklinde buzul alan kesfedildi!"),
            ("Gunes Sistemi Yasi", "Gunes Sistemi 4.6 milyar yasinda. Bir gaz ve toz bulutunun cokmesindenolustu. Hala Gunes'in %99.8 kutlesini tasir."),
            ("Evren Yasi", "Evren 13.8 milyar yasinda. Gozlenebilir evren 93 milyar isik yili capinda — genisleme yuzunden."),
            ("Uzay Sessizligi", "Uzayda ses duyulmaz — ses dalgsalari vakumda yayilmaz! Astronotlar radyo ile konusur. Filmlerdeki patlamalar gercekte sessiz."),
            ("Yildiz Sayisi", "Gozlenebilir evrende 200 milyar galaksi, her birinde 200 milyar yildiz var. Toplam: Dunyadaki kum tanelerinden fazla!"),
        ]

        if "bv_uzay_seed" not in st.session_state:
            st.session_state["bv_uzay_seed"] = _ruz.randint(0, 999999)

        # Mevcut UZAY_BILGISI + ek bilgiler
        for u in UZAY_BILGISI:
            with st.expander(f"{u.get('ikon','')} {u['ad']}", expanded=False):
                st.markdown(u["bilgi"])

        st.markdown("---")
        if st.button("Yeni 5 Uzay Bilgisi Uret", key="bv_uzay_yenile", type="primary", use_container_width=True):
            st.session_state["bv_uzay_seed"] = _ruz.randint(0, 999999)
            st.rerun()

        rng = _ruz.Random(st.session_state["bv_uzay_seed"])
        secilen = rng.sample(_UZAY_EK, min(5, len(_UZAY_EK)))

        _render_html(f'<div style="text-align:center;color:#94a3b8;font-size:0.72rem;margin-bottom:6px">Havuzda {len(_UZAY_EK)} uzay bilgisi — her seferde 5 yenisi</div>')

        for i, (baslik, bilgi) in enumerate(secilen, 1):
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;border-left:4px solid #8b5cf6">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
                    <span style="background:#8b5cf620;color:#8b5cf6;padding:2px 8px;border-radius:10px;font-size:0.68rem;font-weight:700">{i}/5</span>
                    <span style="font-weight:700;color:#c4b5fd !important;font-size:0.95rem">{baslik}</span>
                </div>
                <div style="color:#94a3b8 !important;font-size:0.83rem;line-height:1.5">{bilgi}</div>
            </div>
            """)


def _render_kodlama_oyunlari():
    """Kodlama oyunları — bug bul, çıktı tahmin, eksik parça."""
    import random as _r
    styled_section("🐛 Kodlama Oyunları", "#10b981")

    sub = st.tabs(["🐛 Bug Avcısı", "🔀 Çıktı Tahmini", "🧩 Eksik Parça"])

    with sub[0]:
        styled_section("🐛 Kodda Hatayı Bul!", "#ef4444")
        bug_sorulari = [o for o in KODLAMA_OYUNLARI if o["ad"] == "🐛 Bug Avcısı"]
        if bug_sorulari:
            s = bug_sorulari[0]
            st.markdown("**Hatali Kod:**")
            st.code(s["hatali_kod"], language="python")
            ans = st.text_input("Hata ne?", key="bv_bug_ans", placeholder="Eksik olan...")
            if ans:
                st.success(f"💡 Hata: {s['hata']}")
                st.markdown("**Düzeltilmiş:**")
                st.code(s["duzeltilmis"], language="python")

    with sub[1]:
        styled_section("🔀 Bu Kodun Çıktısı Ne?", "#f59e0b")
        cikti_sorulari = [o for o in KODLAMA_OYUNLARI if o["ad"] == "🔀 Çıktı Tahmini"]
        if cikti_sorulari:
            s = cikti_sorulari[0]
            st.code(s["kod"], language="python")
            ans = st.text_input("Çıktı:", key="bv_cikti_ans")
            if ans:
                if ans.strip() == s["cevap"]:
                    st.success(f"🎉 Doğru! {s['aciklama_detay']}")
                else:
                    st.error(f"❌ Doğru: {s['cevap']} — {s['aciklama_detay']}")

    with sub[2]:
        styled_section("🧩 Eksik Kodu Tamamla!", "#8b5cf6")
        eksik_sorulari = [o for o in KODLAMA_OYUNLARI if o["ad"] == "🧩 Eksik Parça"]
        if eksik_sorulari:
            s = eksik_sorulari[0]
            st.code(s["kod"], language="python")
            ans = st.text_input("___ yerine ne gelir?", key="bv_eksik_ans")
            if ans:
                if ans.strip() == s["cevap"]:
                    st.success(f"🎉 Doğru! {s['aciklama_detay']}")
                else:
                    st.error(f"❌ Doğru: {s['cevap']} — {s['aciklama_detay']}")


def _render_bilim_senligi():
    """Bilim Şenliği — 150 proje, adım adım rehber."""
    styled_section("🎪 Bilim Şenliği Projeleri", "#ec4899")

    _render_html("""
    <div style="background:linear-gradient(135deg,#831843,#be185d,#ec4899);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid rgba(236,72,153,0.5);text-align:center;position:relative;overflow:hidden">
        <div style="font-size:3rem;margin-bottom:8px">🎪🔬🧪🐍✨</div>
        <h2 style="color:white !important;font-size:1.5rem;margin:0 0 8px !important">Bilim Şenliği Proje Rehberi</h2>
        <p style="color:#fce7f3 !important;font-size:0.9rem;margin:0 !important">
            Evde yapılabilir, güvenli, adım adım anlatımlı bilim projeleri!<br>
            Her proje: malzeme listesi + adımlar + sonuç + bilimsel açıklama
        </p>
    </div>
    """)

    # Kategori filtresi
    col1, col2, col3 = st.columns(3)
    with col1:
        kat_filtre = st.selectbox("Kategori", ["Tümü"] + list(PROJE_KATEGORILERI.keys()),
                                   key="bv_senlik_kat")
    with col2:
        zorluk_f = st.selectbox("Zorluk", ["Tümü", "Kolay", "Orta", "Zor"], key="bv_senlik_zor")
    with col3:
        sinif_f = st.selectbox("Sınıf", ["Tümü", "3-6", "5-8", "7-10", "9-12"], key="bv_senlik_sinif")

    # Filtrele
    projeler = BILIM_SENLIGI_PROJELERI
    if kat_filtre != "Tümü":
        projeler = [p for p in projeler if p.get("kategori") == kat_filtre]
    if zorluk_f != "Tümü":
        projeler = [p for p in projeler if p.get("zorluk") == zorluk_f]

    # Kategori istatistikleri
    kat_sayim = {}
    for p in BILIM_SENLIGI_PROJELERI:
        k = p.get("kategori", "?")
        kat_sayim[k] = kat_sayim.get(k, 0) + 1

    cols = st.columns(len(PROJE_KATEGORILERI))
    for col, (kat, info) in zip(cols, PROJE_KATEGORILERI.items()):
        with col:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:10px;text-align:center;
                         border:1px solid {info['renk']}30">
                <div style="font-size:1.3rem">{info['ikon']}</div>
                <div style="font-weight:700;color:{info['renk']} !important;font-size:1.1rem">{kat_sayim.get(kat,0)}</div>
                <div style="font-size:0.65rem;color:#94a3b8 !important">{kat}</div>
            </div>
            """)

    st.caption(f"📋 {len(projeler)} proje gösteriliyor (toplam {len(BILIM_SENLIGI_PROJELERI)})")

    # Proje listesi
    for p in projeler:
        kat_info = PROJE_KATEGORILERI.get(p.get("kategori", ""), {"ikon": "🔬", "renk": "#6366f1"})
        zorluk_renk = {"Kolay": "#10b981", "Orta": "#f59e0b", "Zor": "#ef4444"}.get(p.get("zorluk", ""), "#6366f1")

        with st.expander(f"{p.get('ikon','')} #{p.get('no',0)} {p['ad']} ({p.get('kategori','')}, {p.get('zorluk','')}) — Sınıf {p.get('sinif','')}", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                # Malzeme
                _render_html(f"""
                <div style="background:rgba(99,102,241,0.08);border-radius:10px;padding:10px;margin-bottom:8px;
                             border:1px solid rgba(99,102,241,0.15)">
                    <div style="font-weight:700;color:#818cf8 !important;font-size:0.8rem;margin-bottom:4px">🧰 Malzemeler:</div>
                    <div style="color:#94a3b8 !important;font-size:0.83rem">{p.get('malzeme','')}</div>
                </div>
                """)

                # Adımlar
                st.markdown("**📋 Yapılışı:**")
                for i, adim in enumerate(p.get("adimlar", []), 1):
                    st.markdown(f"**{i}.** {adim}")

                # Sonuç
                _render_html(f"""
                <div style="background:rgba(16,185,129,0.08);border-radius:10px;padding:10px;margin:8px 0;
                             border:1px solid rgba(16,185,129,0.15)">
                    <div style="font-weight:700;color:#10b981 !important;font-size:0.8rem;margin-bottom:4px">🔬 Bilimsel Sonuç:</div>
                    <div style="color:#94a3b8 !important;font-size:0.83rem">{p.get('sonuc','')}</div>
                </div>
                """)

            with col2:
                _render_html(f"""
                <div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
                             border:1px solid {kat_info['renk']}20">
                    <div style="font-size:2.5rem;margin-bottom:6px">{p.get('ikon','')}</div>
                    <div style="font-size:0.7rem;color:{zorluk_renk} !important;font-weight:700">{p.get('zorluk','')}</div>
                    <div style="font-size:0.65rem;color:#94a3b8 !important;margin-top:2px">⏱️ {p.get('sure','')}</div>
                </div>
                """)

            # İlginç bilgi
            if p.get("bilgi"):
                st.info(f"💡 {p['bilgi']}")


def _render_ai_bilim_kocu():
    """AI destekli bilim ve kodlama koçu."""
    styled_section("🤖 AI Bilim & Kodlama Koçu", "#ec4899")

    _render_html("""
    <div class="bv-card" style="text-align:center;border-color:rgba(236,72,153,0.3)">
        <div style="font-size:2rem;margin-bottom:6px">🤖🔬💻</div>
        <div style="font-weight:700;color:#fce7f3 !important;font-size:1rem">Bilim ve Kodlama Hakkında Her Şeyi Sor!</div>
    </div>
    """)

    soru = st.text_input("🤖 Sorunuzu yazın:", key="bv_koc_soru",
                          placeholder="Ör: Newton yasaları nedir? Python'da döngü nasıl yazılır?")

    if soru:
        soru_l = soru.lower()
        cevap = None

        # Fizik
        if any(k in soru_l for k in ["newton", "kuvvet", "hareket", "ivme"]):
            cevap = "**Newton Yasaları:**\n1. **Eylemsizlik:** Cisim hareket halindeyse hareket eder, durmak için kuvvet gerekir.\n2. **F = m × a:** Kuvvet = Kütle × İvme\n3. **Etki-Tepki:** Her kuvvetin eşit ve zıt yönde bir tepkisi vardır."
        elif any(k in soru_l for k in ["ohm", "direnç", "akım", "gerilim"]):
            cevap = "**Ohm Yasası:** V = I × R\n- V = Gerilim (Volt)\n- I = Akım (Amper)\n- R = Direnç (Ohm)\n\nGerilim artarsa akım artar. Direnç artarsa akım azalır."
        elif any(k in soru_l for k in ["enerji", "e=mc", "einstein"]):
            cevap = "**E = mc²** — Einstein'ın ünlü formülü!\n- E = Enerji\n- m = Kütle\n- c = Işık hızı (300.000 km/s)\n\n1 gram madde = 90 trilyon joule enerji! Atom bombasının gücü buradan gelir."
        # Kimya
        elif any(k in soru_l for k in ["asit", "baz", "ph"]):
            cevap = "**Asit-Baz:**\n- pH < 7: Asit (limon, sirke, mide asidi)\n- pH = 7: Nötr (saf su)\n- pH > 7: Baz (sabun, çamaşır suyu)\n\nTurnusol kağıdı: asitte kırmızı, bazda mavi olur."
        elif any(k in soru_l for k in ["atom", "proton", "nötron", "elektron"]):
            cevap = "**Atom Yapısı:**\n- **Çekirdek:** Proton (+) ve Nötron (nötr)\n- **Yörünge:** Elektron (−)\n- Atom numarası = proton sayısı\n- Kütle numarası = proton + nötron\n\nHer şey atomlardan oluşur — sen bile!"
        # Kodlama
        elif any(k in soru_l for k in ["döngü", "for", "while", "tekrar"]):
            cevap = "**Python Döngüler:**\n```python\n# for döngüsü\nfor i in range(5):\n    print(i)  # 0,1,2,3,4\n\n# while döngüsü\nn = 0\nwhile n < 5:\n    print(n)\n    n += 1\n```\n`range(5)` = 0'dan 4'e kadar."
        elif any(k in soru_l for k in ["fonksiyon", "def", "return"]):
            cevap = "**Python Fonksiyon:**\n```python\ndef topla(a, b):\n    return a + b\n\nsonuc = topla(3, 5)\nprint(sonuc)  # 8\n```\n`def` ile tanımla, `return` ile değer döndür."
        elif any(k in soru_l for k in ["liste", "list", "dizi"]):
            cevap = "**Python Liste:**\n```python\nmeyveler = ['elma', 'armut', 'muz']\nmeyveler.append('çilek')  # ekle\nprint(meyveler[0])  # elma\nprint(len(meyveler))  # 4\n```"
        elif any(k in soru_l for k in ["if", "koşul", "şart", "else"]):
            cevap = "**Python Koşul:**\n```python\nyas = 15\nif yas >= 18:\n    print('Yetişkin')\nelif yas >= 13:\n    print('Ergen')\nelse:\n    print('Çocuk')\n```"
        else:
            cevap = "🤖 Bu konuda **Bilim Lab** sekmelerinde deneyler, **Kodlama Dersleri**'nde adım adım eğitim ve **Kavramlar** sekmesinde detaylı açıklamalar bulabilirsin!"

        _render_html(f"""
        <div style="background:#0f172a;border-radius:14px;padding:16px;margin-top:8px;
                     border-left:4px solid #ec4899;border:1px solid rgba(236,72,153,0.15)">
            <div style="font-size:0.85rem;color:#e0e7ff !important;line-height:1.6">{cevap}</div>
        </div>
        """)


def _render_ilerleme(store):
    styled_section("📊 Bilişim Vadisi İlerleme", "#6366f1")

    auth_user = st.session_state.get("auth_user", {})
    user_name = auth_user.get("ad_soyad", auth_user.get("username", "Kullanıcı"))

    profil_data = store.get_profil(auth_user.get("username", "misafir"))

    _render_html(f"""
    <div style="background:linear-gradient(135deg,#0c1222,#1e3a5f);border-radius:20px;padding:24px;margin-bottom:16px;
                 border:2px solid rgba(14,165,233,0.3);text-align:center">
        <div style="font-size:2.5rem;margin-bottom:8px">🔬💻</div>
        <div style="font-size:1.2rem;font-weight:700;color:#e0f2fe !important">{user_name}</div>
        <div style="font-size:0.85rem;color:#94a3b8 !important">Bilişim Vadisi Yolcusu</div>
    </div>
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        styled_section("⚗️ Bilim Lab", "#3b82f6")
        st.markdown(f"- {len(FIZIK_DENEYLERI)} Fizik deneyi")
        st.markdown(f"- {len(KIMYA_DENEYLERI)} Kimya deneyi")
        st.markdown(f"- {len(BIYOLOJI_DENEYLERI)} Biyoloji deneyi")
    with col2:
        styled_section("💻 Kodlama", "#10b981")
        st.markdown(f"- {len(PROGRAMLAMA_DILLERI)} dil tanıtımı")
        st.markdown(f"- {len(KODLAMA_KAVRAMLARI)} kavram")
        st.markdown(f"- {len(KODLAMA_SORULARI)} soru")
    with col3:
        styled_section("🧑‍🔬 Bilim İnsanları", "#f59e0b")
        st.markdown(f"- {len(UNLU_BILIM_INSANLARI)} ünlü bilim insanı")
        st.markdown("- Portreli biyografiler")

    if not profil_data:
        st.info("Henüz ilerleme kaydın yok. Deneyleri yap, kodları çöz — ilerleme otomatik kaydedilecek!")


# ---------------------------------------------------------------------------
# FEATURE 1 – Web Gelistirme (JavaScript / HTML / CSS Live Editor)
# ---------------------------------------------------------------------------

_WEB_TEMPLATES = {
    "Merhaba Dunya": {
        "html": '<h1 id="baslik">Merhaba Dunya!</h1>\n<p>Bu benim ilk web sayfam.</p>',
        "css": "body { font-family: Arial, sans-serif; text-align: center; padding: 40px; background: #0f172a; color: #e2e8f0; }\nh1 { color: #38bdf8; }",
        "js": 'document.getElementById("baslik").addEventListener("click", function() {\n  this.style.color = "#f472b6";\n  this.textContent = "Tikladin!";\n});',
    },
    "Renkli Sayfa": {
        "html": '<div id="kutu" class="kutu">Renk Degistir</div>\n<button id="btn">Tikla</button>',
        "css": "body { background: #1e293b; display: flex; flex-direction: column; align-items: center; padding: 40px; gap: 20px; }\n.kutu { width: 200px; height: 200px; background: #3b82f6; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 1.1rem; font-weight: bold; transition: all 0.4s; }\nbutton { padding: 10px 28px; border: none; border-radius: 8px; background: #10b981; color: #fff; font-size: 1rem; cursor: pointer; }",
        "js": 'const renkler = ["#ef4444","#f59e0b","#10b981","#8b5cf6","#ec4899"];\nlet idx = 0;\ndocument.getElementById("btn").addEventListener("click", function() {\n  idx = (idx + 1) % renkler.length;\n  document.getElementById("kutu").style.background = renkler[idx];\n});',
    },
    "Buton Oyunu": {
        "html": '<h2>Butona Kac Kez Basabilirsin?</h2>\n<p>Skor: <span id="skor">0</span></p>\n<button id="btn">Bas!</button>',
        "css": "body { background: #0f172a; color: #e2e8f0; text-align: center; padding: 30px; font-family: Arial; }\nbutton { padding: 14px 36px; font-size: 1.2rem; border: none; border-radius: 10px; background: #6366f1; color: #fff; cursor: pointer; margin-top: 10px; }\nbutton:hover { background: #818cf8; }",
        "js": 'let skor = 0;\ndocument.getElementById("btn").addEventListener("click", function() {\n  skor++;\n  document.getElementById("skor").textContent = skor;\n  if (skor % 10 === 0) alert("Harika! " + skor + " tiklamaya ulastin!");\n});',
    },
    "Saat Uygulamasi": {
        "html": '<h2>Canli Saat</h2>\n<div id="saat" class="saat"></div>',
        "css": "body { background: #0f172a; color: #e2e8f0; text-align: center; padding: 40px; font-family: Arial; }\n.saat { font-size: 3rem; font-weight: bold; color: #38bdf8; margin-top: 20px; text-shadow: 0 0 20px rgba(56,189,248,0.4); }",
        "js": 'function guncelle() {\n  const simdi = new Date();\n  const s = String(simdi.getHours()).padStart(2,"0");\n  const d = String(simdi.getMinutes()).padStart(2,"0");\n  const sn = String(simdi.getSeconds()).padStart(2,"0");\n  document.getElementById("saat").textContent = s + ":" + d + ":" + sn;\n}\nsetInterval(guncelle, 1000);\nguncelle();',
    },
    "Yapilacaklar Listesi": {
        "html": '<h2>Yapilacaklar</h2>\n<input id="girdi" placeholder="Gorev yaz..." />\n<button id="ekle">Ekle</button>\n<ul id="liste"></ul>',
        "css": "body { background: #0f172a; color: #e2e8f0; padding: 30px; font-family: Arial; max-width: 400px; margin: auto; }\ninput { padding: 10px; width: 60%; border-radius: 8px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0; }\nbutton { padding: 10px 20px; border: none; border-radius: 8px; background: #10b981; color: #fff; cursor: pointer; margin-left: 8px; }\nli { padding: 8px 0; border-bottom: 1px solid #1e293b; cursor: pointer; }\nli.done { text-decoration: line-through; color: #64748b; }",
        "js": 'document.getElementById("ekle").addEventListener("click", function() {\n  const v = document.getElementById("girdi").value.trim();\n  if (!v) return;\n  const li = document.createElement("li");\n  li.textContent = v;\n  li.addEventListener("click", function() { this.classList.toggle("done"); });\n  document.getElementById("liste").appendChild(li);\n  document.getElementById("girdi").value = "";\n});',
    },
}


def _render_web_gelistirme():
    """Web Gelistirme - HTML/CSS/JS canli editor."""
    import streamlit.components.v1 as components

    styled_section("Web Gelistirme Ortami", "#0ea5e9")

    _render_html("""
    <div class="bv-card">
        <div style="color:#7dd3fc !important;font-weight:700;font-size:1rem">HTML + CSS + JavaScript Editoru</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            Asagidaki alanlara kodlarini yaz, Calistir butonuna bas ve sonucu canli izle.
        </div>
    </div>
    """)

    template_names = list(_WEB_TEMPLATES.keys())
    selected = st.selectbox("Sablon Sec", ["-- Bos --"] + template_names, key="bv_web_template_sel")

    if selected != "-- Bos --":
        tpl = _WEB_TEMPLATES[selected]
        default_html = tpl["html"]
        default_css = tpl["css"]
        default_js = tpl["js"]
    else:
        default_html = ""
        default_css = ""
        default_js = ""

    # Store template values in session state for persistence
    tpl_key = f"bv_web_tpl_loaded_{selected}"
    if tpl_key not in st.session_state:
        st.session_state["bv_web_html_val"] = default_html
        st.session_state["bv_web_css_val"] = default_css
        st.session_state["bv_web_js_val"] = default_js
        st.session_state[tpl_key] = True

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**HTML**")
        html_code = st.text_area("HTML kodu", value=st.session_state.get("bv_web_html_val", default_html), height=200, key="bv_web_html")
    with c2:
        st.markdown("**CSS**")
        css_code = st.text_area("CSS kodu", value=st.session_state.get("bv_web_css_val", default_css), height=200, key="bv_web_css")
    with c3:
        st.markdown("**JavaScript**")
        js_code = st.text_area("JS kodu", value=st.session_state.get("bv_web_js_val", default_js), height=200, key="bv_web_js")

    if st.button("Calistir", key="bv_web_run", type="primary"):
        srcdoc_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{css_code}</style></head>
<body>{html_code}<script>{js_code}</script></body></html>"""
        srcdoc_escaped = srcdoc_content.replace('"', '&quot;')
        iframe_html = f'<iframe srcdoc="{srcdoc_escaped}" style="width:100%;height:580px;border:2px solid #1e293b;border-radius:12px;background:#0f172a;" sandbox="allow-scripts"></iframe>'
        components.html(iframe_html, height=600)


# ---------------------------------------------------------------------------
# FEATURE 2 – Robot Programlama (Visual Robot Programming on Canvas)
# ---------------------------------------------------------------------------

def _render_robot_programlama():
    """Robot Programlama - Grid tabanli gorsel robot oyunu."""
    import streamlit.components.v1 as components

    styled_section("Robot Programlama", "#10b981")

    _render_html("""
    <div class="bv-card">
        <div style="color:#6ee7b7 !important;font-weight:700;font-size:1rem">Robotu Hedefe Gotür</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            Komut ekle, Calistir'a bas, robotun yildiza ulasmasini izle!
        </div>
    </div>
    """)

    level = st.selectbox("Seviye Sec", ["Seviye 1 - Baslangic", "Seviye 2 - Kolay", "Seviye 3 - Orta", "Seviye 4 - Zor", "Seviye 5 - Uzman"], key="bv_robot_level")
    level_idx = int(level.split(" ")[1]) - 1

    robot_html = r"""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:10px}
canvas{border:2px solid #1e293b;border-radius:8px;margin:8px 0}
.panel{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:6px 0}
button{padding:8px 18px;border:none;border-radius:8px;font-size:0.9rem;cursor:pointer;font-weight:600}
.cmd{background:#1e293b;color:#38bdf8;border:1px solid #334155}
.cmd:hover{background:#334155}
.run{background:#10b981;color:#fff}
.clr{background:#ef4444;color:#fff}
#queue{color:#94a3b8;font-size:0.85rem;margin:4px 0;min-height:22px}
#status{color:#fbbf24;font-size:0.9rem;margin:4px 0;font-weight:600;min-height:22px}
#stats{color:#64748b;font-size:0.82rem}
</style>
</head><body>
<div id="status"></div>
<canvas id="c" width="400" height="400"></canvas>
<div class="panel">
  <button class="cmd" onclick="addCmd('F')">Ileri</button>
  <button class="cmd" onclick="addCmd('L')">Sola Don</button>
  <button class="cmd" onclick="addCmd('R')">Saga Don</button>
  <button class="run" onclick="runCmds()">Calistir</button>
  <button class="clr" onclick="clearCmds()">Temizle</button>
</div>
<div id="queue">Komutlar: -</div>
<div id="stats">Adim: 0 | Komut: 0</div>

<script>
const CELL=40,G=10;
const levels=[
  {sx:0,sy:0,sd:0,gx:4,gy:0,walls:[]},
  {sx:0,sy:0,sd:0,gx:5,gy:3,walls:[[2,0],[2,1],[2,2]]},
  {sx:0,sy:9,sd:0,gx:7,gy:2,walls:[[1,9],[1,8],[3,5],[3,6],[3,7],[5,3],[5,4]]},
  {sx:0,sy:0,sd:0,gx:9,gy:9,walls:[[1,0],[1,1],[1,2],[3,2],[3,3],[3,4],[5,4],[5,5],[5,6],[7,6],[7,7],[7,8]]},
  {sx:0,sy:4,sd:0,gx:9,gy:5,walls:[[1,3],[1,4],[1,5],[3,1],[3,2],[3,6],[3,7],[5,3],[5,4],[5,5],[7,2],[7,3],[7,6],[7,7],[7,8]]}
];
const DIRS=[[1,0],[0,1],[-1,0],[0,-1]];
const DNAME=["Sag","Asagi","Sol","Yukari"];
let lv=LEVEL_IDX,cmds=[],robot,running=false,steps=0;
const cv=document.getElementById("c"),cx=cv.getContext("2d");

function init(){
  const l=levels[lv];robot={x:l.sx,y:l.sy,d:l.sd};steps=0;running=false;cmds=[];
  updQueue();updStats();draw();document.getElementById("status").textContent="";
}
function draw(){
  const l=levels[lv];
  cx.fillStyle="#0f172a";cx.fillRect(0,0,400,400);
  for(let i=0;i<=G;i++){cx.strokeStyle="#1e293b";cx.beginPath();cx.moveTo(i*CELL,0);cx.lineTo(i*CELL,400);cx.stroke();cx.beginPath();cx.moveTo(0,i*CELL);cx.lineTo(400,i*CELL);cx.stroke();}
  l.walls.forEach(w=>{cx.fillStyle="#334155";cx.fillRect(w[0]*CELL+1,w[1]*CELL+1,CELL-2,CELL-2);});
  cx.fillStyle="#fbbf24";cx.font="24px Arial";cx.textAlign="center";cx.textBaseline="middle";
  cx.fillText("\u2605",l.gx*CELL+CELL/2,l.gy*CELL+CELL/2);
  const rx=robot.x*CELL+CELL/2,ry=robot.y*CELL+CELL/2;
  cx.save();cx.translate(rx,ry);cx.rotate(robot.d*Math.PI/2);
  cx.fillStyle="#10b981";cx.beginPath();cx.moveTo(14,0);cx.lineTo(-10,-10);cx.lineTo(-10,10);cx.closePath();cx.fill();
  cx.restore();
}
function addCmd(c){if(running)return;cmds.push(c);updQueue();}
function clearCmds(){if(running)return;cmds=[];updQueue();init();}
function updQueue(){
  const m={"F":"Ileri","L":"Sola","R":"Saga"};
  document.getElementById("queue").textContent="Komutlar: "+(cmds.length?cmds.map(c=>m[c]).join(" > "):"-");
}
function updStats(){document.getElementById("stats").textContent="Adim: "+steps+" | Komut: "+cmds.length;}
async function runCmds(){
  if(running||cmds.length===0)return;running=true;
  document.getElementById("status").textContent="Calisiyor...";
  for(let i=0;i<cmds.length;i++){
    const c=cmds[i];
    if(c==="L"){robot.d=(robot.d+3)%4;}
    else if(c==="R"){robot.d=(robot.d+1)%4;}
    else if(c==="F"){
      const nd=DIRS[robot.d],nx=robot.x+nd[0],ny=robot.y+nd[1];
      const l=levels[lv];
      if(nx>=0&&nx<G&&ny>=0&&ny<G&&!l.walls.some(w=>w[0]===nx&&w[1]===ny)){robot.x=nx;robot.y=ny;}
    }
    steps++;updStats();draw();
    await new Promise(r=>setTimeout(r,350));
    const l=levels[lv];
    if(robot.x===l.gx&&robot.y===l.gy){document.getElementById("status").textContent="Tebrikler! Hedefe "+steps+" adimda ulastin!";running=false;return;}
  }
  const l=levels[lv];
  if(robot.x===l.gx&&robot.y===l.gy){document.getElementById("status").textContent="Tebrikler! Hedefe "+steps+" adimda ulastin!";}
  else{document.getElementById("status").textContent="Hedefe ulasilamadi. Tekrar dene!";}
  running=false;
}
init();
</script></body></html>
""".replace("LEVEL_IDX", str(level_idx))

    components.html(robot_html, height=620)


# ---------------------------------------------------------------------------
# FEATURE 3 – Siber Guvenlik (Cyber Security)
# ---------------------------------------------------------------------------

def _render_siber_guvenlik():
    """Siber Guvenlik - Sifre guc olcer, phishing quiz, ipuclari."""
    import streamlit.components.v1 as components

    styled_section("Siber Guvenlik", "#ef4444")

    _render_html("""
    <div class="bv-card">
        <div style="color:#fca5a5 !important;font-weight:700;font-size:1rem">Siber Guvenlik Egitim Merkezi</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            Sifre gucunu test et, sahte e-postalari bul ve guvenlik ipuclarini ogren.
        </div>
    </div>
    """)

    sub = st.radio("Bolum Sec", ["Sifre Guc Olcer", "Phishing Testi", "Guvenlik Ipuclari"], key="bv_cyber_section", horizontal=True)

    if sub == "Sifre Guc Olcer":
        cyber_password_html = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:30px;display:flex;flex-direction:column;align-items:center}
h2{margin-bottom:16px;color:#f87171}
input{width:320px;padding:12px;border-radius:8px;border:1px solid #334155;background:#1e293b;color:#e2e8f0;font-size:1rem;margin-bottom:12px}
.bar-bg{width:320px;height:18px;background:#1e293b;border-radius:9px;overflow:hidden;margin-bottom:10px}
.bar{height:100%;border-radius:9px;transition:width 0.4s,background 0.4s}
.info{font-size:0.85rem;color:#94a3b8;width:320px}
.info span{display:block;margin:3px 0}
.check{color:#10b981}.cross{color:#ef4444}
#lbl{font-weight:700;font-size:0.95rem;margin-bottom:10px}
</style></head><body>
<h2>Sifre Guc Olcer</h2>
<input id="pw" type="text" placeholder="Sifreni buraya yaz..." oninput="analyze()">
<div class="bar-bg"><div class="bar" id="bar" style="width:0%;background:#ef4444"></div></div>
<div id="lbl" style="color:#ef4444">-</div>
<div class="info" id="info"></div>
<script>
function analyze(){
  const p=document.getElementById("pw").value;
  const bar=document.getElementById("bar"),lbl=document.getElementById("lbl"),info=document.getElementById("info");
  if(!p){bar.style.width="0%";bar.style.background="#ef4444";lbl.textContent="-";lbl.style.color="#ef4444";info.innerHTML="";return;}
  let score=0;
  const hasLen=p.length>=8,hasUp=/[A-Z]/.test(p),hasLow=/[a-z]/.test(p),hasNum=/[0-9]/.test(p),hasSym=/[^A-Za-z0-9]/.test(p),hasLong=p.length>=12;
  if(hasLen)score+=20;if(hasUp)score+=20;if(hasLow)score+=10;if(hasNum)score+=20;if(hasSym)score+=20;if(hasLong)score+=10;
  let color,label;
  if(score<=20){color="#ef4444";label="Cok Zayif";}
  else if(score<=40){color="#f97316";label="Zayif";}
  else if(score<=60){color="#eab308";label="Orta";}
  else if(score<=80){color="#22c55e";label="Guclu";}
  else{color="#10b981";label="Cok Guclu";}
  bar.style.width=score+"%";bar.style.background=color;lbl.textContent=label+" ("+score+"/100)";lbl.style.color=color;
  const mk=(ok,t)=>'<span class="'+(ok?"check":"cross")+'">'+(ok?"\u2713":"\u2717")+" "+t+"</span>";
  info.innerHTML=mk(hasLen,"En az 8 karakter")+mk(hasUp,"Buyuk harf iceriyor")+mk(hasLow,"Kucuk harf iceriyor")+mk(hasNum,"Rakam iceriyor")+mk(hasSym,"Ozel karakter iceriyor")+mk(hasLong,"12+ karakter (bonus)");
}
</script></body></html>
"""
        components.html(cyber_password_html, height=550)

    elif sub == "Phishing Testi":
        cyber_phishing_html = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:20px;display:flex;flex-direction:column;align-items:center}
h2{margin-bottom:12px;color:#f87171}
.email{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:16px;width:480px;margin-bottom:10px}
.from{color:#38bdf8;font-weight:700;font-size:0.9rem}
.subj{color:#e2e8f0;font-weight:600;margin:6px 0}
.body-text{color:#94a3b8;font-size:0.85rem;line-height:1.5}
.btns{display:flex;gap:10px;margin:8px 0 16px}
button{padding:8px 22px;border:none;border-radius:8px;font-size:0.9rem;cursor:pointer;font-weight:600}
.real{background:#10b981;color:#fff}
.fake{background:#ef4444;color:#fff}
#result{font-weight:700;margin:6px 0;min-height:22px}
#score{color:#fbbf24;font-weight:700;margin-bottom:10px}
.correct{color:#10b981}.wrong{color:#ef4444}
</style></head><body>
<h2>Phishing Testi</h2>
<div id="score">Skor: 0 / 0</div>
<div id="emailBox"></div>
<div class="btns">
  <button class="real" onclick="answer(true)">Gercek E-posta</button>
  <button class="fake" onclick="answer(false)">Sahte (Phishing)</button>
</div>
<div id="result"></div>

<script>
const emails=[
  {from:"destek@okulportal.edu.tr",subj:"Karne Bilgileriniz Hazir",body:"Sayın veli, 2025-2026 egitim yili karne bilgilerinize e-Okul sistemi uzerinden ulasabilirsiniz. Iyi gunler dileriz.",real:true},
  {from:"guvenlik@bankaa-turkiye.com.ru",subj:"ACIL: Hesabiniz Askiya Alindi!!",body:"Hesabiniz supheli islem nedeniyle donduruldu. 24 saat icinde asagidaki linke tiklayarak dogrulayin yoksa hesabiniz KALICI olarak KAPATILACAKTIR! http://banka-giris-dogrula.xyz/login",real:false},
  {from:"info@kargo-takip.com",subj:"Kargonuz teslim edilemedi",body:"Kargonuz adrese teslim edilemedi. Teslimat ucretini odemek icin tiklayin: http://karg0-odeme.tk/pay Odenmezse kargonuz iade edilecektir.",real:false},
  {from:"no-reply@google.com",subj:"Yeni cihazdan giris yapildi",body:"Hesabiniza yeni bir Windows cihazindan giris yapildi. Bu siz degilseniz hesap ayarlarinizi kontrol edin. - Google Guvenlik Ekibi",real:true},
  {from:"kampanya@super-firsat99.net",subj:"TEBRIKLER! 10.000 TL Kazandiniz!",body:"Cekilis sonucunda 10.000 TL kazandiniz! Odulunuzu almak icin TC kimlik no, banka hesap no ve telefon bilgilerinizi yanitlayin. Bu firsat 1 saat icinde sona eriyor!",real:false}
];
let idx=0,correct=0,total=0;
function show(){
  if(idx>=emails.length){document.getElementById("emailBox").innerHTML='<div class="email"><div class="subj">Test bitti!</div><div class="body-text">Skorun: '+correct+' / '+total+'</div></div>';document.getElementById("result").textContent="";return;}
  const e=emails[idx];
  document.getElementById("emailBox").innerHTML='<div class="email"><div class="from">Gonderen: '+e.from+'</div><div class="subj">'+e.subj+'</div><div class="body-text">'+e.body+'</div></div>';
  document.getElementById("result").textContent="";
}
function answer(isReal){
  if(idx>=emails.length)return;
  total++;
  const e=emails[idx],ok=(isReal===e.real);
  if(ok){correct++;document.getElementById("result").innerHTML='<span class="correct">Dogru! '+(e.real?"Bu gercek bir e-posta.":"Bu sahte (phishing) e-posta!")+'</span>';}
  else{document.getElementById("result").innerHTML='<span class="wrong">Yanlis! '+(e.real?"Bu aslinda gercek bir e-postaydı.":"Bu sahte bir e-postaydı! Dikkat!")+'</span>';}
  document.getElementById("score").textContent="Skor: "+correct+" / "+total;
  idx++;setTimeout(show,1800);
}
show();
</script></body></html>
"""
        components.html(cyber_phishing_html, height=550)

    else:  # Guvenlik Ipuclari
        tips = [
            ("Guclu Sifre Kullan", "En az 12 karakter, buyuk-kucuk harf, rakam ve ozel karakter iceren sifreler olustur."),
            ("Her Hesaba Farkli Sifre", "Ayni sifreyi birden fazla hesapta kullanma. Bir hesap ele gecirilirse digerlerinin guvenligini riske atarsin."),
            ("Iki Adimli Dogrulama", "Mumkun olan her yerde iki faktorlu kimlik dogrulamayi (2FA) etkinlestir."),
            ("Supheli Linklere Tiklama", "E-posta veya mesajdaki linklere tiklamadan once gonderen adresini kontrol et."),
            ("Yazilimlarini Guncelle", "Isletim sistemi, tarayici ve uygulamalarini her zaman guncel tut."),
            ("Herkese Acik Wi-Fi", "Kafeler ve havaalanlari gibi yerlerdeki acik Wi-Fi aglarinda onemli islemler yapma."),
            ("Kisisel Bilgilerini Paylasma", "Sosyal medyada dogum tarihi, adres, telefon numarasi gibi bilgileri paylasma."),
            ("Yedekleme Yap", "Onemli dosyalarini duzenli olarak harici disk veya bulut depolamaya yedekle."),
            ("Bilinmeyen Dosyalari Acma", "E-posta eki veya indirilen dosyalarin guvenilir kaynaktan geldiginden emin ol."),
            ("Ekranini Kilitle", "Bilgisayarindan veya telefonundan uzaklasirken ekrani her zaman kilitle."),
        ]
        _render_html("""
        <div style="background:#1e293b;border-radius:14px;padding:20px;margin:10px 0;border:1px solid #334155">
            <div style="color:#f87171 !important;font-weight:700;font-size:1.1rem;margin-bottom:14px">
                Cocuklar Icin 10 Siber Guvenlik Ipucu
            </div>
        """)
        tip_html_parts = []
        for i, (title, desc) in enumerate(tips, 1):
            tip_html_parts.append(f"""
            <div style="margin-bottom:12px;padding:10px 14px;background:#0f172a;border-radius:10px;border:1px solid #1e293b">
                <div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem">{i}. {title}</div>
                <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">{desc}</div>
            </div>
            """)
        _render_html("".join(tip_html_parts) + "</div>")


def _render_deney_simulasyonu():
    """Deney Simulasyonu — 6 interaktif premium deney."""
    styled_section("Deney Simulasyonu — Premium Lab", "#10b981")
    import streamlit.components.v1 as components

    sub_tabs = st.tabs([
        "Elektrik Devresi",
        "Kimya Lab",
        "Serbest Dusus",
        "Optik Lab",
        "Dalga Havuzu",
        "Termodinamik",
    ])

    # ── SUB-TAB 1: Elektrik Devresi ──
    with sub_tabs[0]:
        preset = st.selectbox("Devre Sablonu", [
            "Basit Devre", "Seri Devre", "Paralel Devre", "Direnc + LED", "Coklu LED Seri"
        ], key="bv_deney_circuit_preset")
        circuit_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow:hidden}
canvas{display:block;margin:0 auto;cursor:pointer}
.toolbar{display:flex;gap:6px;justify-content:center;padding:8px;background:linear-gradient(135deg,#1e293b,#0f172a);flex-wrap:wrap;border-bottom:1px solid #334155}
.toolbar button{padding:7px 14px;border:1px solid #334155;border-radius:8px;background:#0f172a;color:#e2e8f0;cursor:pointer;font-size:0.8rem;transition:all .2s}
.toolbar button:hover{background:#334155;transform:translateY(-1px)}
.toolbar button.active{border-color:#10b981;color:#10b981;box-shadow:0 0 8px rgba(16,185,129,.3)}
.info{text-align:center;padding:6px;color:#94a3b8;font-size:0.78rem;background:#1e293b}
.meters{display:flex;gap:12px;justify-content:center;padding:8px;background:#1e293b;border-top:1px solid #334155}
.meter{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:6px 14px;text-align:center;min-width:110px}
.meter .val{font-size:1.1rem;font-weight:700;color:#10b981}
.meter .lbl{font-size:0.65rem;color:#94a3b8;margin-top:2px}
.edu{text-align:center;padding:6px 12px;color:#94a3b8;font-size:0.75rem;background:#0f172a;border-top:1px solid #1e293b;min-height:32px}
</style></head><body>
<div class="toolbar">
  <button onclick="selectComp('battery')" id="btn_battery">Pil (9V)</button>
  <button onclick="selectComp('led')" id="btn_led">LED</button>
  <button onclick="selectComp('resistor')" id="btn_resistor">Direnc</button>
  <button onclick="selectComp('switch')" id="btn_switch">Anahtar</button>
  <button onclick="selectComp('buzzer')" id="btn_buzzer">Buzzer</button>
  <button onclick="selectComp('wire')" id="btn_wire">Kablo</button>
  <button onclick="clearBoard()" style="border-color:#ef4444;color:#ef4444">Temizle</button>
</div>
<div class="info" id="info">Bir bilesen secip kanvasa tiklayin. Bilesenleri surukleyerek tasiyabilirsiniz. Anahtara tiklayarak acip kapatabilirsiniz.</div>
<canvas id="cv" width="700" height="340"></canvas>
<div class="meters">
  <div class="meter"><div class="val" id="mVolt">0.0 V</div><div class="lbl">Gerilim</div></div>
  <div class="meter"><div class="val" id="mAmp">0.0 mA</div><div class="lbl">Akim</div></div>
  <div class="meter"><div class="val" id="mRes">0 Ohm</div><div class="lbl">Toplam Direnc</div></div>
  <div class="meter"><div class="val" id="mPow">0.0 mW</div><div class="lbl">Guc</div></div>
</div>
<div class="edu" id="edu"></div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let comps=[],selectedComp="battery",dragging=null,dragOff={x:0,y:0};
let switchOn=false,frame=0;
const PRESET='""" + preset + r"""';
const EDU_TEXTS={"Basit Devre":"Basit devre: Pil + Anahtar + LED. Anahtar kapatildiginda devre tamamlanir ve LED yanar.","Seri Devre":"Seri baglanti: Akim her noktada aynidir. Toplam direnc = R1+R2+... Gerilim paylasilir.","Paralel Devre":"Paralel baglanti: Gerilim her kolda aynidir. 1/Rtop = 1/R1+1/R2. Akim dallara bolunur.","Direnc + LED":"Direnc, LED uzerinden gecen akimi sinirlar. V=IR ile akim hesaplanir. LED'i asiri akimdan korur.","Coklu LED Seri":"Seri LED'lerde her LED uzerinde gerilim dusumu olusur. 3 LED icin: V_led = (9V - V_kayip) / 3"};
let electrons=[];
function selectComp(t){selectedComp=t;document.querySelectorAll(".toolbar button").forEach(b=>b.classList.remove("active"));let btn=document.getElementById("btn_"+t);if(btn)btn.classList.add("active");document.getElementById("info").textContent="Secili: "+t+" — kanvasa tiklayin"}
function clearBoard(){comps=[];switchOn=false;electrons=[];draw()}
function loadPreset(){
  comps=[];switchOn=false;electrons=[];
  if(PRESET==="Basit Devre")comps.push({t:"battery",x:100,y:170},{t:"wire",x:200,y:170},{t:"switch",x:300,y:170},{t:"wire",x:400,y:170},{t:"led",x:520,y:170});
  else if(PRESET==="Seri Devre")comps.push({t:"battery",x:70,y:170},{t:"wire",x:150,y:170},{t:"resistor",x:230,y:170},{t:"wire",x:310,y:170},{t:"led",x:390,y:170},{t:"wire",x:470,y:170},{t:"led",x:550,y:170});
  else if(PRESET==="Paralel Devre")comps.push({t:"battery",x:100,y:170},{t:"wire",x:200,y:100},{t:"led",x:340,y:100},{t:"wire",x:200,y:240},{t:"led",x:340,y:240},{t:"switch",x:500,y:170});
  else if(PRESET==="Direnc + LED")comps.push({t:"battery",x:80,y:170},{t:"wire",x:170,y:170},{t:"switch",x:260,y:170},{t:"wire",x:350,y:170},{t:"resistor",x:440,y:170},{t:"wire",x:530,y:170},{t:"led",x:620,y:170});
  else comps.push({t:"battery",x:60,y:170},{t:"wire",x:140,y:170},{t:"switch",x:220,y:170},{t:"wire",x:300,y:170},{t:"led",x:380,y:170},{t:"wire",x:440,y:170},{t:"led",x:500,y:170},{t:"wire",x:560,y:170},{t:"led",x:630,y:170});
  document.getElementById("edu").textContent=EDU_TEXTS[PRESET]||"";
  draw();
}
function calcCircuit(){
  let hasBat=false,hasLed=false,hasSw=false,hasBuz=false,resCount=0,ledCount=0;
  comps.forEach(c=>{if(c.t==="battery")hasBat=true;if(c.t==="led"){hasLed=true;ledCount++}if(c.t==="switch")hasSw=true;if(c.t==="buzzer")hasBuz=true;if(c.t==="resistor")resCount++});
  let on=hasBat&&(hasLed||hasBuz)&&(hasSw?switchOn:true)&&comps.length>=2;
  let V=on?9:0,R=resCount*220+ledCount*50+(hasBuz?100:0);if(R<1)R=50;
  let I=on?V/R*1000:0,P=on?V*I:0;
  document.getElementById("mVolt").textContent=V.toFixed(1)+" V";
  document.getElementById("mAmp").textContent=I.toFixed(1)+" mA";
  document.getElementById("mRes").textContent=R+" Ohm";
  document.getElementById("mPow").textContent=P.toFixed(1)+" mW";
  return{on,V,I,R};
}
function spawnElectrons(){
  if(electrons.length>60)return;
  for(let i=0;i<comps.length-1;i++){
    if(Math.random()<0.3){
      let a=comps[i],b=comps[i+1];
      electrons.push({x:a.x,y:a.y,tx:b.x,ty:b.y,t:0,spd:0.02+Math.random()*0.015});
    }
  }
}
function draw(){
  frame++;
  ctx.clearRect(0,0,700,340);
  ctx.strokeStyle="#1e293b";ctx.lineWidth=0.5;
  for(let i=0;i<700;i+=25){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,340);ctx.stroke()}
  for(let i=0;i<340;i+=25){ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(700,i);ctx.stroke()}
  let ci=calcCircuit();
  // wires
  ctx.lineWidth=2.5;
  for(let i=0;i<comps.length-1;i++){
    let a=comps[i],b=comps[i+1];
    ctx.strokeStyle=ci.on?"#475569":"#334155";
    ctx.beginPath();ctx.moveTo(a.x+22,a.y);ctx.lineTo(b.x-22,b.y);ctx.stroke();
    if(ci.on){ctx.strokeStyle="rgba(16,185,129,0.08)";ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(a.x+22,a.y);ctx.lineTo(b.x-22,b.y);ctx.stroke();ctx.lineWidth=2.5}
  }
  // electrons
  if(ci.on){spawnElectrons();electrons.forEach(el=>{el.t+=el.spd;let x=el.x+(el.tx-el.x)*el.t,y=el.y+(el.ty-el.y)*el.t;ctx.beginPath();ctx.arc(x,y,2.5,0,Math.PI*2);ctx.fillStyle="rgba(16,185,129,"+(0.8-el.t*0.5)+")";ctx.fill()});electrons=electrons.filter(el=>el.t<1)}
  // components
  comps.forEach(c=>{
    ctx.save();ctx.translate(c.x,c.y);
    if(c.t==="battery"){
      ctx.fillStyle="#1e293b";ctx.strokeStyle="#facc15";ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(-22,-28,44,56,6);ctx.fill();ctx.stroke();
      ctx.fillStyle="#facc15";ctx.font="bold 14px Arial";ctx.textAlign="center";ctx.fillText("+",0,-10);ctx.fillText("-",0,18);
      ctx.fillStyle="#94a3b8";ctx.font="bold 9px Arial";ctx.fillText("9V",0,38);
    }else if(c.t==="led"){
      let glow=ci.on;
      if(glow){ctx.shadowColor="#10b981";ctx.shadowBlur=25+Math.sin(frame*0.1)*8}
      ctx.beginPath();ctx.moveTo(0,-18);ctx.lineTo(-14,14);ctx.lineTo(14,14);ctx.closePath();
      ctx.fillStyle=glow?"#10b981":"#334155";ctx.fill();ctx.strokeStyle="#e2e8f0";ctx.lineWidth=1;ctx.stroke();
      if(glow){ctx.globalAlpha=0.15+Math.sin(frame*0.08)*0.1;ctx.beginPath();ctx.arc(0,0,30,0,Math.PI*2);ctx.fillStyle="#10b981";ctx.fill();ctx.globalAlpha=1}
      ctx.shadowBlur=0;ctx.fillStyle="#94a3b8";ctx.font="9px Arial";ctx.textAlign="center";ctx.fillText("LED",0,30);
    }else if(c.t==="resistor"){
      ctx.strokeStyle="#8b5cf6";ctx.lineWidth=2.5;ctx.beginPath();ctx.moveTo(-20,0);
      [[-15,-10],[-10,10],[-5,-10],[0,10],[5,-10],[10,10],[15,0],[20,0]].forEach(p=>ctx.lineTo(p[0],p[1]));ctx.stroke();
      ctx.fillStyle="#1e293b";ctx.strokeStyle="#8b5cf6";ctx.lineWidth=1;ctx.beginPath();ctx.roundRect(-16,-6,32,12,3);ctx.fill();ctx.stroke();
      let colors=["#ef4444","#ef4444","#854d0e","#facc15"];colors.forEach((col,i)=>{ctx.fillStyle=col;ctx.fillRect(-12+i*7,-4,5,8)});
      ctx.fillStyle="#94a3b8";ctx.font="9px Arial";ctx.textAlign="center";ctx.fillText("220\u03A9",0,22);
    }else if(c.t==="switch"){
      ctx.strokeStyle=switchOn?"#10b981":"#ef4444";ctx.lineWidth=3;
      ctx.beginPath();ctx.arc(-15,0,6,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.arc(15,0,6,0,Math.PI*2);ctx.stroke();
      if(switchOn){ctx.beginPath();ctx.moveTo(-9,0);ctx.lineTo(9,0);ctx.stroke()}else{ctx.beginPath();ctx.moveTo(-9,0);ctx.lineTo(9,-16);ctx.stroke()}
      ctx.fillStyle=switchOn?"#10b981":"#ef4444";ctx.font="bold 9px Arial";ctx.textAlign="center";ctx.fillText(switchOn?"ACIK":"KAPALI",0,22);
    }else if(c.t==="buzzer"){
      let bOn=ci.on;
      let bx=bOn?Math.sin(frame*0.5)*2:0;
      ctx.translate(bx,0);
      ctx.fillStyle="#1e293b";ctx.strokeStyle=bOn?"#f59e0b":"#334155";ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,16,0,Math.PI*2);ctx.fill();ctx.stroke();
      if(bOn){ctx.strokeStyle="rgba(245,158,11,0.3)";ctx.lineWidth=1;for(let r=20;r<35;r+=6){ctx.beginPath();ctx.arc(0,-10,r,Math.PI*1.2,Math.PI*1.8);ctx.stroke()}}
      ctx.fillStyle=bOn?"#f59e0b":"#64748b";ctx.font="bold 9px Arial";ctx.textAlign="center";ctx.fillText("BUZ",0,4);ctx.fillStyle="#94a3b8";ctx.font="9px Arial";ctx.fillText("Buzzer",0,30);
    }else if(c.t==="wire"){
      ctx.fillStyle="#475569";ctx.fillRect(-15,-2,30,4);ctx.beginPath();ctx.arc(-15,0,4,0,Math.PI*2);ctx.fillStyle="#64748b";ctx.fill();ctx.beginPath();ctx.arc(15,0,4,0,Math.PI*2);ctx.fill();
    }
    ctx.restore();
  });
  requestAnimationFrame(draw);
}
cv.addEventListener("mousedown",e=>{
  const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  for(let c of comps){if(c.t==="switch"&&Math.hypot(mx-c.x,my-c.y)<25){switchOn=!switchOn;return}}
  for(let i=comps.length-1;i>=0;i--){if(Math.hypot(mx-comps[i].x,my-comps[i].y)<25){dragging=comps[i];dragOff={x:mx-comps[i].x,y:my-comps[i].y};return}}
  comps.push({t:selectedComp,x:mx,y:my});
});
cv.addEventListener("mousemove",e=>{if(!dragging)return;const r=cv.getBoundingClientRect();dragging.x=e.clientX-r.left-dragOff.x;dragging.y=e.clientY-r.top-dragOff.y});
cv.addEventListener("mouseup",()=>{dragging=null});
loadPreset();
</script></body></html>"""
        components.html(circuit_html, height=600)

    # ── SUB-TAB 2: Kimya Lab ──
    with sub_tabs[1]:
        chem_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow:hidden}
canvas{display:block;margin:0 auto}
.top{display:flex;gap:8px;justify-content:center;padding:8px 12px;background:linear-gradient(135deg,#1e293b,#0f172a);flex-wrap:wrap;align-items:center;border-bottom:1px solid #334155}
.top select{padding:6px 10px;border:1px solid #334155;border-radius:6px;background:#0f172a;color:#e2e8f0;font-size:0.82rem;min-width:130px}
.top button{padding:7px 16px;border:1px solid #334155;border-radius:8px;background:#0f172a;color:#e2e8f0;cursor:pointer;font-size:0.82rem;transition:all .2s}
.top button:hover{background:#334155}
.top button.mix{border-color:#10b981;color:#10b981;font-weight:700}
.result{text-align:center;padding:8px 12px;font-size:0.85rem;min-height:48px;background:#1e293b;border-top:1px solid #334155}
.eq{color:#10b981;font-weight:700;font-size:0.95rem}
.thermo{position:absolute;right:20px;top:80px;width:30px;height:200px;background:#1e293b;border:1px solid #334155;border-radius:15px;overflow:hidden}
.thermo-fill{position:absolute;bottom:0;width:100%;background:linear-gradient(to top,#3b82f6,#ef4444);transition:height .5s}
.thermo-val{position:absolute;top:-22px;width:100%;text-align:center;font-size:0.7rem;color:#94a3b8}
</style></head><body>
<div class="top">
  <label style="color:#94a3b8;font-size:0.8rem">Sol Tup:</label>
  <select id="chem1"><option value="HCl">HCl (Hidroklorik Asit)</option><option value="NaOH">NaOH (Sodyum Hidroksit)</option><option value="H2SO4">H2SO4 (Sulfurik Asit)</option><option value="CuSO4">CuSO4 (Bakir Sulfat)</option><option value="AgNO3">AgNO3 (Gumus Nitrat)</option><option value="NaCl">NaCl (Sodyum Klorur)</option><option value="KMnO4">KMnO4 (Potasyum Permanganat)</option><option value="FeCl3">FeCl3 (Demir(III) Klorur)</option></select>
  <label style="color:#94a3b8;font-size:0.8rem">Sag Tup:</label>
  <select id="chem2"><option value="NaOH" selected>NaOH (Sodyum Hidroksit)</option><option value="HCl">HCl (Hidroklorik Asit)</option><option value="H2SO4">H2SO4 (Sulfurik Asit)</option><option value="CuSO4">CuSO4 (Bakir Sulfat)</option><option value="AgNO3">AgNO3 (Gumus Nitrat)</option><option value="NaCl">NaCl (Sodyum Klorur)</option><option value="KMnO4">KMnO4 (Potasyum Permanganat)</option><option value="FeCl3">FeCl3 (Demir(III) Klorur)</option></select>
  <button class="mix" onclick="doMix()">Karistir</button>
  <button onclick="doReset()">Sifirla</button>
</div>
<canvas id="cv" width="700" height="420"></canvas>
<div class="result" id="result"></div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
const COLORS={HCl:"#ef4444",NaOH:"#3b82f6",H2SO4:"#f97316",CuSO4:"#0ea5e9",AgNO3:"#94a3b8",NaCl:"#f5f5f4",KMnO4:"#a855f7",FeCl3:"#f59e0b"};
const RX={
  "HCl+NaOH":{color:"#e2e8f0",eq:"HCl + NaOH \u2192 NaCl + H\u2082O",desc:"Notrlesme reaksiyonu: Asit ve baz birlesiyor, tuz ve su olusur. Ekzotermik reaksiyon — isi aciga cikar!",temp:45,bubbles:true},
  "HCl+AgNO3":{color:"#f5f5f4",eq:"HCl + AgNO3 \u2192 AgCl\u2193 + HNO\u2083",desc:"Beyaz gumus klorur cokeltisi olusur. Bu reaksiyon klorur iyonu testinde kullanilir.",temp:22,bubbles:false},
  "NaOH+CuSO4":{color:"#0ea5e9",eq:"2NaOH + CuSO4 \u2192 Cu(OH)\u2082\u2193 + Na\u2082SO\u2084",desc:"Mavi bakir hidroksit cokeltisi olusur. Biuret testinde protein tespitinde kullanilir.",temp:24,bubbles:false},
  "H2SO4+NaOH":{color:"#e2e8f0",eq:"H\u2082SO\u2084 + 2NaOH \u2192 Na\u2082SO\u2084 + 2H\u2082O",desc:"Kuvvetli asit-baz notrlesme reaksiyonu. Buyuk miktarda isi aciga cikar!",temp:60,bubbles:true},
  "AgNO3+NaCl":{color:"#f5f5f4",eq:"AgNO\u2083 + NaCl \u2192 AgCl\u2193 + NaNO\u2083",desc:"Beyaz AgCl cokeltisi olusur. Isikta kararir (fotokimyasal reaksiyon).",temp:22,bubbles:false},
  "KMnO4+HCl":{color:"#fbbf24",eq:"2KMnO\u2084 + 16HCl \u2192 2KCl + 2MnCl\u2082 + 5Cl\u2082 + 8H\u2082O",desc:"Mor permanganat renksizlesir. Klor gazi olusur — cok tehlikeli reaksiyon!",temp:35,bubbles:true},
  "FeCl3+NaOH":{color:"#92400e",eq:"FeCl\u2083 + 3NaOH \u2192 Fe(OH)\u2083\u2193 + 3NaCl",desc:"Kahverengi-kirmizi demir(III) hidroksit cokeltisi olusur. Pas'in kimyasal benzeri!",temp:23,bubbles:false},
  "CuSO4+NaCl":{color:"#06b6d4",eq:"CuSO\u2084 + 2NaCl \u2192 CuCl\u2082 + Na\u2082SO\u2084",desc:"Cift yer degistirme reaksiyonu. Cozelti rengi hafifce degisir. Cokelti olusmaz.",temp:22,bubbles:false},
  "H2SO4+CuSO4":{color:"#0284c7",eq:"Belirgin reaksiyon yok",desc:"Her iki madde de sulu cozeltide — onemli bir reaksiyon gozlenmez.",temp:22,bubbles:false},
  "KMnO4+NaOH":{color:"#581c87",eq:"Bazik ortamda MnO\u2084\u207B rengi koyulasir",desc:"Permanganat bazik ortamda daha koyu mor renk alir. Redoks kimyasinda onemlidir.",temp:23,bubbles:false}
};
let mixed=false,pourStep=0,bubbles=[],temp=22,mixColor="#1e293b",mixLevel=0,frame=0;
function getKey(a,b){if(RX[a+"+"+b])return a+"+"+b;if(RX[b+"+"+a])return b+"+"+a;return null}
function drawTube(x,y,w,h,color,lbl,level){
  ctx.save();ctx.fillStyle="#0f172a";ctx.strokeStyle="#334155";ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(x,y,w,h,10);ctx.fill();ctx.stroke();
  ctx.beginPath();ctx.roundRect(x-4,y-6,w+8,14,4);ctx.fillStyle="#334155";ctx.fill();
  let lh=h*level*0.65;if(lh>0){ctx.fillStyle=color;ctx.globalAlpha=0.8;ctx.beginPath();ctx.roundRect(x+3,y+h-lh-3,w-6,lh,4);ctx.fill();ctx.globalAlpha=1;
    for(let i=0;i<3;i++){let ry=y+h-lh+i*(lh/3);ctx.strokeStyle="rgba(255,255,255,0.08)";ctx.beginPath();ctx.moveTo(x+6,ry);ctx.lineTo(x+w-6,ry);ctx.stroke()}}
  ctx.fillStyle="#e2e8f0";ctx.font="bold 11px 'Segoe UI'";ctx.textAlign="center";ctx.fillText(lbl,x+w/2,y+h+20);ctx.restore();
}
function drawFlask(x,y,w,h,color,level){
  ctx.save();ctx.fillStyle="#0f172a";ctx.strokeStyle="#475569";ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(x+w*0.35,y);ctx.lineTo(x,y+h*0.4);ctx.lineTo(x,y+h);ctx.lineTo(x+w,y+h);ctx.lineTo(x+w,y+h*0.4);ctx.lineTo(x+w*0.65,y);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.beginPath();ctx.roundRect(x+w*0.3,y-10,w*0.4,14,3);ctx.fillStyle="#334155";ctx.fill();
  let lh=h*level*0.55;if(lh>0){
    ctx.fillStyle=color;ctx.globalAlpha=0.75;
    ctx.beginPath();
    let by=y+h-lh,bw=w-(y+h-lh-y-h*0.4>0?0:(y+h*0.4-(y+h-lh))/(h*0.6)*w*0.35*2);
    ctx.fillRect(x+4,by,w-8,lh-4);ctx.globalAlpha=1}
  ctx.fillStyle="#94a3b8";ctx.font="11px 'Segoe UI'";ctx.textAlign="center";ctx.fillText("Erlenmayer",x+w/2,y+h+20);ctx.restore();
}
function doMix(){
  let c1=document.getElementById("chem1").value,c2=document.getElementById("chem2").value;
  if(c1===c2){document.getElementById("result").innerHTML='<span style="color:#f59e0b">Ayni kimyasali sectiniz! Farkli iki kimyasal secin.</span>';return}
  mixed=true;pourStep=60;
  let key=getKey(c1,c2);
  if(key&&RX[key]){let r=RX[key];mixColor=r.color;temp=r.temp;
    setTimeout(()=>{mixLevel=1;document.getElementById("result").innerHTML='<div class="eq">'+r.eq+'</div><div style="color:#94a3b8;margin-top:4px">'+r.desc+'</div>';},800);
    if(r.bubbles)for(let i=0;i<20;i++)setTimeout(()=>addBubble(),i*80);
  }else{mixColor=blendColors(COLORS[c1],COLORS[c2]);temp=22;mixLevel=1;
    setTimeout(()=>{document.getElementById("result").innerHTML='<span style="color:#94a3b8">Bu iki madde arasinda belirgin bir reaksiyon gozlenmedi.</span>';},800);}
}
function blendColors(a,b){let pa=hexToRgb(a),pb=hexToRgb(b);return"rgb("+(Math.round((pa.r+pb.r)/2))+","+(Math.round((pa.g+pb.g)/2))+","+(Math.round((pa.b+pb.b)/2))+")";}
function hexToRgb(h){let r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);return{r,g,b}}
function addBubble(){bubbles.push({x:295+Math.random()*110,y:330,r:2+Math.random()*5,vy:-0.8-Math.random()*2,vx:(Math.random()-0.5)*0.5,life:80+Math.random()*40})}
function doReset(){mixed=false;pourStep=0;mixLevel=0;mixColor="#1e293b";temp=22;bubbles=[];document.getElementById("result").textContent=""}
function draw(){
  frame++;ctx.clearRect(0,0,700,420);
  let c1=document.getElementById("chem1").value,c2=document.getElementById("chem2").value;
  drawTube(80,100,55,180,COLORS[c1]||"#64748b",c1,mixed?0.3:1);
  drawTube(560,100,55,180,COLORS[c2]||"#64748b",c2,mixed?0.3:1);
  drawFlask(280,120,140,200,mixed?mixColor:"#0f172a",mixLevel);
  if(pourStep>0){pourStep--;let t=1-pourStep/60;
    ctx.strokeStyle=COLORS[c1];ctx.lineWidth=3;ctx.globalAlpha=0.6*(1-t);
    ctx.beginPath();ctx.moveTo(135,190);ctx.quadraticCurveTo(210,100+t*40,350,120+t*80);ctx.stroke();
    ctx.strokeStyle=COLORS[c2];ctx.beginPath();ctx.moveTo(560,190);ctx.quadraticCurveTo(490,100+t*40,350,120+t*80);ctx.stroke();ctx.globalAlpha=1}
  bubbles=bubbles.filter(b=>{b.y+=b.vy;b.x+=b.vx;b.life--;b.r*=0.998;ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fillStyle="rgba(255,255,255,"+(b.life/120)*0.6+")";ctx.fill();return b.life>0&&b.r>0.5});
  // thermometer
  ctx.fillStyle="#1e293b";ctx.strokeStyle="#334155";ctx.lineWidth=1;ctx.beginPath();ctx.roundRect(650,80,24,180,12);ctx.fill();ctx.stroke();
  let tH=Math.min(170,Math.max(10,(temp/100)*170));let tCol=temp>40?"#ef4444":temp>25?"#f59e0b":"#3b82f6";
  ctx.fillStyle=tCol;ctx.globalAlpha=0.8;ctx.beginPath();ctx.roundRect(654,260-tH,16,tH,6);ctx.fill();ctx.globalAlpha=1;
  ctx.beginPath();ctx.arc(662,268,10,0,Math.PI*2);ctx.fillStyle=tCol;ctx.fill();
  ctx.fillStyle="#e2e8f0";ctx.font="bold 11px Arial";ctx.textAlign="center";ctx.fillText(temp+"\u00B0C",662,72);
  requestAnimationFrame(draw);
}
draw();
</script></body></html>"""
        components.html(chem_html, height=600)

    # ── SUB-TAB 3: Serbest Dusus ──
    with sub_tabs[2]:
        col1, col2, col3 = st.columns(3)
        with col1:
            height_val = st.slider("Yukseklik (m)", 1, 200, 50, key="bv_deney_fall_height")
        with col2:
            grav_name = st.selectbox("Gezegen", ["Dunya (9.8)", "Ay (1.6)", "Mars (3.7)", "Jupiter (24.8)", "Saturn (10.4)"], key="bv_deney_fall_grav")
        with col3:
            air_res = st.checkbox("Hava Direnci", value=False, key="bv_deney_air")
        grav_map = {"Dunya (9.8)": 9.8, "Ay (1.6)": 1.6, "Mars (3.7)": 3.7, "Jupiter (24.8)": 24.8, "Saturn (10.4)": 10.4}
        grav_val = grav_map[grav_name]
        bounce_coeff = st.slider("Sekme Katsayisi", 0.0, 0.95, 0.5, 0.05, key="bv_deney_bounce")
        fall_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow:hidden}
canvas{display:block;margin:0 auto}
.panel{display:flex;gap:12px;justify-content:center;padding:8px;background:linear-gradient(135deg,#1e293b,#0f172a);flex-wrap:wrap;align-items:center;border-bottom:1px solid #334155}
.panel button{padding:8px 24px;border:none;border-radius:8px;background:#10b981;color:#fff;cursor:pointer;font-size:0.9rem;font-weight:700;transition:all .2s}
.panel button:hover{background:#059669;transform:translateY(-1px)}
.panel label{font-size:0.8rem;color:#94a3b8;display:flex;align-items:center;gap:4px}
.stats{display:flex;gap:10px;justify-content:center;padding:6px;flex-wrap:wrap}
.stat{background:#1e293b;border-radius:8px;padding:8px 14px;text-align:center;border:1px solid #334155;min-width:100px}
.stat .val{font-size:1rem;font-weight:700;color:#0ea5e9}
.stat .lbl{font-size:0.65rem;color:#94a3b8;margin-top:1px}
</style></head><body>
<div class="panel">
  <button onclick="dropBall()">Birak</button>
  <button onclick="resetSim()" style="background:#64748b">Sifirla</button>
  <label><input type="checkbox" id="showTrail" checked> Iz goster</label>
</div>
<div style="display:flex">
  <canvas id="cv" width="480" height="380"></canvas>
  <canvas id="graph" width="220" height="380" style="border-left:1px solid #334155"></canvas>
</div>
<div class="stats">
  <div class="stat"><div class="val" id="sTime">0.00 s</div><div class="lbl">Zaman</div></div>
  <div class="stat"><div class="val" id="sVel">0.00 m/s</div><div class="lbl">Hiz</div></div>
  <div class="stat"><div class="val" id="sAcc">0.00 m/s2</div><div class="lbl">Ivme</div></div>
  <div class="stat"><div class="val" id="sKE">0.00 J</div><div class="lbl">Kinetik E.</div></div>
  <div class="stat"><div class="val" id="sPE">0.00 J</div><div class="lbl">Potansiyel E.</div></div>
  <div class="stat"><div class="val" id="sH">0.00 m</div><div class="lbl">Yukseklik</div></div>
</div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
const gv=document.getElementById("graph"),gctx=gv.getContext("2d");
const H=""" + str(height_val) + """,G=""" + str(grav_val) + """,AIR=""" + ("true" if air_res else "false") + """,BOUNCE=""" + str(bounce_coeff) + """;
const groundY=350,startY=30,scale=(groundY-startY)/H;
let ballY=startY,velY=0,time=0,running=false,bounceVel=0,landed=false,mass=1,trail=[],velHistory=[];
const dragCoeff=AIR?0.005:0;

function drawScene(){
  ctx.clearRect(0,0,480,380);
  let grd=ctx.createLinearGradient(0,0,0,380);grd.addColorStop(0,"#0c1222");grd.addColorStop(1,"#1e293b");ctx.fillStyle=grd;ctx.fillRect(0,0,480,380);
  ctx.fillStyle="#334155";ctx.fillRect(0,groundY,480,30);ctx.fillStyle="#475569";for(let i=0;i<480;i+=30){ctx.fillRect(i,groundY,15,3)}
  ctx.strokeStyle="#475569";ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(40,startY);ctx.lineTo(40,groundY);ctx.stroke();
  for(let m=0;m<=H;m+=Math.max(1,Math.ceil(H/10))){let y=groundY-(m*scale);ctx.beginPath();ctx.moveTo(32,y);ctx.lineTo(48,y);ctx.stroke();ctx.fillStyle="#94a3b8";ctx.font="9px Arial";ctx.textAlign="right";ctx.fillText(m+"m",28,y+3)}
  if(document.getElementById("showTrail").checked){ctx.strokeStyle="rgba(249,115,22,0.15)";ctx.lineWidth=2;ctx.beginPath();trail.forEach((p,i)=>{if(i===0)ctx.moveTo(p.x,p.y);else ctx.lineTo(p.x,p.y)});ctx.stroke();trail.forEach((p,i)=>{if(i%3===0){ctx.beginPath();ctx.arc(p.x,p.y,2,0,Math.PI*2);ctx.fillStyle="rgba(249,115,22,"+(i/trail.length*0.4)+")";ctx.fill()}})}
  // shadow
  let sh=Math.max(2,(ballY-startY)/(groundY-startY)*20);ctx.beginPath();ctx.ellipse(240,groundY-2,sh,3,0,0,Math.PI*2);ctx.fillStyle="rgba(0,0,0,"+(0.5-sh/50)+")";ctx.fill();
  // motion blur
  if(running&&Math.abs(velY)>2){let blurH=Math.min(20,Math.abs(velY)*0.8);ctx.beginPath();ctx.ellipse(240,ballY-blurH/2,12,blurH,0,0,Math.PI*2);ctx.fillStyle="rgba(249,115,22,0.15)";ctx.fill()}
  // ball
  ctx.beginPath();ctx.arc(240,ballY,14,0,Math.PI*2);ctx.fillStyle="#f97316";ctx.shadowColor="#f97316";ctx.shadowBlur=running?18:6;ctx.fill();ctx.shadowBlur=0;
  ctx.beginPath();ctx.arc(235,ballY-5,4,0,Math.PI*2);ctx.fillStyle="rgba(255,255,255,0.3)";ctx.fill();
  ctx.fillStyle="#64748b";ctx.font="11px Arial";ctx.textAlign="center";ctx.fillText("g = "+G+" m/s\u00B2"+(AIR?" | Hava Direnci ACIK":""),240,groundY+22);
}
function drawGraph(){
  gctx.clearRect(0,0,220,380);gctx.fillStyle="#0f172a";gctx.fillRect(0,0,220,380);
  gctx.fillStyle="#94a3b8";gctx.font="bold 10px Arial";gctx.textAlign="center";gctx.fillText("Hiz-Zaman Grafigi",110,16);
  gctx.strokeStyle="#1e293b";gctx.lineWidth=0.5;for(let i=30;i<370;i+=30){gctx.beginPath();gctx.moveTo(30,i);gctx.lineTo(210,i);gctx.stroke()}
  gctx.strokeStyle="#475569";gctx.lineWidth=1;gctx.beginPath();gctx.moveTo(30,30);gctx.lineTo(30,360);gctx.lineTo(210,360);gctx.stroke();
  gctx.fillStyle="#94a3b8";gctx.font="8px Arial";gctx.textAlign="center";gctx.fillText("t(s)",120,375);gctx.save();gctx.translate(10,200);gctx.rotate(-Math.PI/2);gctx.fillText("v(m/s)",0,0);gctx.restore();
  if(velHistory.length<2)return;
  let maxV=Math.max(10,...velHistory.map(v=>Math.abs(v.v)));let maxT=Math.max(1,...velHistory.map(v=>v.t));
  gctx.strokeStyle="#0ea5e9";gctx.lineWidth=2;gctx.beginPath();
  velHistory.forEach((p,i)=>{let x=30+(p.t/maxT)*175,y=360-(Math.abs(p.v)/maxV)*325;if(i===0)gctx.moveTo(x,y);else gctx.lineTo(x,y)});gctx.stroke();
}
function update(){
  if(!running)return;let dt=0.016,acc=G;
  if(!landed){
    if(AIR){let drag=dragCoeff*velY*velY*(velY>0?1:-1);acc=G-drag}
    velY+=acc*dt;let posM=H-(ballY-startY)/scale;posM-=velY*dt;
    if(posM<=0){posM=0;landed=true;bounceVel=-velY*BOUNCE;velY=0}
    ballY=groundY-posM*scale;time+=dt;trail.push({x:240,y:ballY});
    velHistory.push({t:time,v:velY});
  }else{
    bounceVel+=G*dt;let posM=(groundY-ballY)/scale;posM-=bounceVel*dt;
    if(posM<=0){posM=0;bounceVel=-bounceVel*BOUNCE;if(Math.abs(bounceVel)<0.3){running=false;bounceVel=0}}
    ballY=groundY-posM*scale;time+=dt;velY=Math.abs(bounceVel);trail.push({x:240,y:ballY});velHistory.push({t:time,v:bounceVel});}
  let curH=(groundY-ballY)/scale,v=landed?Math.abs(bounceVel):velY;
  document.getElementById("sTime").textContent=time.toFixed(2)+" s";
  document.getElementById("sVel").textContent=v.toFixed(2)+" m/s";
  document.getElementById("sAcc").textContent=G.toFixed(2)+" m/s\u00B2";
  document.getElementById("sKE").textContent=(0.5*mass*v*v).toFixed(2)+" J";
  document.getElementById("sPE").textContent=(mass*G*curH).toFixed(2)+" J";
  document.getElementById("sH").textContent=curH.toFixed(2)+" m";
}
function dropBall(){if(running)return;running=true;landed=false;velY=0;time=0;ballY=startY;bounceVel=0;trail=[];velHistory=[]}
function resetSim(){running=false;landed=false;ballY=startY;velY=0;time=0;bounceVel=0;trail=[];velHistory=[];
  ["sTime","sVel","sAcc","sKE","sPE","sH"].forEach(id=>{document.getElementById(id).textContent="0.00"})}
function loop(){update();drawScene();drawGraph();requestAnimationFrame(loop)}
loop();
</script></body></html>"""
        components.html(fall_html, height=600)

    # ── SUB-TAB 4: Optik Lab ──
    with sub_tabs[3]:
        optik_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow:hidden}
canvas{display:block;margin:0 auto;cursor:crosshair}
.bar{display:flex;gap:6px;justify-content:center;padding:8px;background:linear-gradient(135deg,#1e293b,#0f172a);flex-wrap:wrap;border-bottom:1px solid #334155}
.bar button{padding:6px 14px;border:1px solid #334155;border-radius:8px;background:#0f172a;color:#e2e8f0;cursor:pointer;font-size:0.8rem;transition:all .2s}
.bar button:hover{background:#334155}
.bar button.active{border-color:#10b981;color:#10b981}
.info{text-align:center;padding:6px;color:#94a3b8;font-size:0.75rem;background:#1e293b;border-top:1px solid #334155;min-height:28px}
</style></head><body>
<div class="bar">
  <button onclick="setPreset(0)" class="active" id="p0">Duz Ayna</button>
  <button onclick="setPreset(1)" id="p1">Cift Ayna</button>
  <button onclick="setPreset(2)" id="p2">Prizma (Gokkusagi)</button>
  <button onclick="setPreset(3)" id="p3">Yakinsak Mercek</button>
  <button onclick="setPreset(4)" id="p4">Tam Ic Yansima</button>
  <button onclick="clearAll()" style="border-color:#ef4444;color:#ef4444">Temizle</button>
</div>
<canvas id="cv" width="700" height="480"></canvas>
<div class="info" id="info">Fare ile lazer kaynagini yonlendirin. Snell Yasasi: n1 sin(a1) = n2 sin(a2)</div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let objects=[],laserX=50,laserY=240,mouseX=350,mouseY=240,preset=0;
const PRESETS=[
  [{type:"mirror",x:400,y:140,x2:400,y2:340}],
  [{type:"mirror",x:400,y:100,x2:400,y2:300},{type:"mirror",x:250,y:350,x2:550,y2:350}],
  [{type:"prism",cx:350,cy:240,size:80}],
  [{type:"lens",cx:400,cy:240,r:120,f:100,converging:true}],
  [{type:"glass",x:350,y:140,w:200,h:200,n:1.5}]
];
const PRESET_INFO=["Duz ayna: Gelis acisi = Yansima acisi. Isik aynadan esit aciyla yansir.","Cift ayna: Isik birden fazla aynadan yansiabilir. Her yansimada acilar korunur.","Prizma: Beyaz isik farkli dalga boylarinda kirilarak gokkusagi renklerine ayrisir (dispersiyon).","Yakinsak mercek: Paralel isik mercekten gectiginde odak noktasinda toplanir. f = odak uzakligi.","Tam ic yansima: Isik yogun ortamdan seyrek ortama gecerken kritik aciyi asarsa geri yansir."];
function setPreset(i){preset=i;objects=JSON.parse(JSON.stringify(PRESETS[i]));document.getElementById("info").textContent=PRESET_INFO[i];document.querySelectorAll(".bar button[id]").forEach((b,j)=>{b.classList.toggle("active",j===i)})}
function clearAll(){objects=[];document.getElementById("info").textContent="Temizlendi. Bir preset secin veya fare ile yonlendirin."}
function reflect(dx,dy,nx,ny){let dot=dx*nx+dy*ny;return{x:dx-2*dot*nx,y:dy-2*dot*ny}}
function refract(dx,dy,nx,ny,n1,n2){let cosi=-(nx*dx+ny*dy);let ratio=n1/n2;let sin2t=ratio*ratio*(1-cosi*cosi);if(sin2t>1)return null;let cost=Math.sqrt(1-sin2t);return{x:ratio*dx+(ratio*cosi-cost)*nx,y:ratio*dy+(ratio*cosi-cost)*ny}}
function lineIntersect(x1,y1,x2,y2,x3,y3,x4,y4){let d=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4);if(Math.abs(d)<1e-10)return null;let t=((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/d;let u=-((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/d;if(t>0.001&&t<1&&u>0&&u<1)return{x:x1+t*(x2-x1),y:y1+t*(y2-y1),t};return null}
function traceRay(ox,oy,dx,dy,color,depth){
  if(depth>8)return;
  let minT=Infinity,hit=null,hitObj=null,hitNx=0,hitNy=0;
  let ex=ox+dx*2000,ey=oy+dy*2000;
  for(let obj of objects){
    if(obj.type==="mirror"){
      let p=lineIntersect(ox,oy,ex,ey,obj.x,obj.y,obj.x2,obj.y2);
      if(p&&p.t<minT){minT=p.t;hit=p;hitObj=obj;let mx=obj.x2-obj.x,my=obj.y2-obj.y,ml=Math.hypot(mx,my);hitNx=-my/ml;hitNy=mx/ml}
    }else if(obj.type==="glass"){
      let sides=[[obj.x,obj.y,obj.x+obj.w,obj.y],[obj.x+obj.w,obj.y,obj.x+obj.w,obj.y+obj.h],[obj.x+obj.w,obj.y+obj.h,obj.x,obj.y+obj.h],[obj.x,obj.y+obj.h,obj.x,obj.y]];
      let normals=[[0,-1],[1,0],[0,1],[-1,0]];
      for(let si=0;si<4;si++){let s=sides[si];let p=lineIntersect(ox,oy,ex,ey,s[0],s[1],s[2],s[3]);if(p&&p.t<minT){minT=p.t;hit=p;hitObj=obj;hitNx=normals[si][0];hitNy=normals[si][1]}}
    }else if(obj.type==="lens"){
      let topY=obj.cy-obj.r,botY=obj.cy+obj.r;
      let p1=lineIntersect(ox,oy,ex,ey,obj.cx,topY,obj.cx,botY);
      if(p1&&p1.t<minT){minT=p1.t;hit=p1;hitObj=obj;hitNx=-1;hitNy=0}
    }else if(obj.type==="prism"){
      let s=obj.size,cx=obj.cx,cy=obj.cy;
      let pts=[[cx,cy-s*0.7],[cx-s*0.6,cy+s*0.4],[cx+s*0.6,cy+s*0.4]];
      let pNormals=[];
      for(let i=0;i<3;i++){let j=(i+1)%3;let ex2=pts[j][0]-pts[i][0],ey2=pts[j][1]-pts[i][1],el=Math.hypot(ex2,ey2);pNormals.push([-ey2/el,ex2/el])}
      for(let i=0;i<3;i++){let j=(i+1)%3;let p=lineIntersect(ox,oy,ex,ey,pts[i][0],pts[i][1],pts[j][0],pts[j][1]);if(p&&p.t<minT){minT=p.t;hit=p;hitObj=obj;hitNx=pNormals[i][0];hitNy=pNormals[i][1]}}
    }
  }
  ctx.strokeStyle=color;ctx.lineWidth=2;ctx.shadowColor=color;ctx.shadowBlur=4;ctx.globalAlpha=0.9;ctx.beginPath();ctx.moveTo(ox,oy);
  if(hit){
    ctx.lineTo(hit.x,hit.y);ctx.stroke();ctx.shadowBlur=0;ctx.globalAlpha=1;
    if(hitObj.type==="mirror"){let r=reflect(dx,dy,hitNx,hitNy);traceRay(hit.x,hit.y,r.x,r.y,color,depth+1)}
    else if(hitObj.type==="glass"){
      let entering=dx*hitNx+dy*hitNy<0;let n1=entering?1:hitObj.n,n2=entering?hitObj.n:1;
      let nx=entering?hitNx:-hitNx,ny=entering?hitNy:-hitNy;
      let r=refract(dx,dy,nx,ny,n1,n2);
      if(r){traceRay(hit.x+r.x*2,hit.y+r.y*2,r.x,r.y,color,depth+1)}else{let rf=reflect(dx,dy,nx,ny);traceRay(hit.x,hit.y,rf.x,rf.y,color,depth+1)}
    }else if(hitObj.type==="prism"){
      let entering=dx*hitNx+dy*hitNy<0;let n1=entering?1:1.52,n2=entering?1.52:1;
      let nx=entering?hitNx:-hitNx,ny=entering?hitNy:-hitNy;
      if(!entering){
        let rainbow=["#ef4444","#f97316","#facc15","#10b981","#3b82f6","#6366f1","#8b5cf6"];
        rainbow.forEach((c,i)=>{let nn=1.50+i*0.006;let r=refract(dx,dy,nx,ny,nn,1);if(r)traceRay(hit.x+r.x*2,hit.y+r.y*2,r.x,r.y,c,depth+1);else{let rf=reflect(dx,dy,nx,ny);traceRay(hit.x,hit.y,rf.x,rf.y,c,depth+1)}});
      }else{let r=refract(dx,dy,nx,ny,n1,n2);if(r)traceRay(hit.x+r.x*2,hit.y+r.y*2,r.x,r.y,color,depth+1)}
    }else if(hitObj.type==="lens"){
      if(hitObj.converging){let fy=hit.y-hitObj.cy;let angle=Math.atan2(fy,-hitObj.f*0.8);traceRay(hit.x,hit.y,Math.cos(angle)*Math.sign(dx),Math.sin(angle)+dy*0.1,"#ef4444",depth+1)}
    }
  }else{ctx.lineTo(ex,ey);ctx.stroke()}
  ctx.shadowBlur=0;ctx.globalAlpha=1;
}
function draw(){
  ctx.clearRect(0,0,700,480);ctx.fillStyle="#0f172a";ctx.fillRect(0,0,700,480);
  ctx.strokeStyle="#1e293b";ctx.lineWidth=0.5;for(let i=0;i<700;i+=30){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,480);ctx.stroke()}for(let i=0;i<480;i+=30){ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(700,i);ctx.stroke()}
  // draw objects
  for(let obj of objects){
    if(obj.type==="mirror"){ctx.strokeStyle="#e2e8f0";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(obj.x,obj.y);ctx.lineTo(obj.x2,obj.y2);ctx.stroke();ctx.strokeStyle="#475569";ctx.lineWidth=1;let dx=obj.x2-obj.x,dy=obj.y2-obj.y,l=Math.hypot(dx,dy);for(let i=0;i<l;i+=12){let px=obj.x+dx*i/l,py=obj.y+dy*i/l;ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px-dy/l*8,py+dx/l*8);ctx.stroke()}}
    else if(obj.type==="glass"){ctx.fillStyle="rgba(59,130,246,0.1)";ctx.strokeStyle="rgba(59,130,246,0.4)";ctx.lineWidth=2;ctx.fillRect(obj.x,obj.y,obj.w,obj.h);ctx.strokeRect(obj.x,obj.y,obj.w,obj.h);ctx.fillStyle="#94a3b8";ctx.font="10px Arial";ctx.textAlign="center";ctx.fillText("n="+obj.n,obj.x+obj.w/2,obj.y+obj.h/2)}
    else if(obj.type==="prism"){let s=obj.size,cx=obj.cx,cy=obj.cy;ctx.beginPath();ctx.moveTo(cx,cy-s*0.7);ctx.lineTo(cx-s*0.6,cy+s*0.4);ctx.lineTo(cx+s*0.6,cy+s*0.4);ctx.closePath();ctx.fillStyle="rgba(99,102,241,0.15)";ctx.fill();ctx.strokeStyle="rgba(99,102,241,0.5)";ctx.lineWidth=2;ctx.stroke();ctx.fillStyle="#94a3b8";ctx.font="10px Arial";ctx.textAlign="center";ctx.fillText("Prizma",cx,cy+s*0.4+16)}
    else if(obj.type==="lens"){ctx.strokeStyle=obj.converging?"#10b981":"#ef4444";ctx.lineWidth=2;ctx.beginPath();let cx=obj.cx,cy=obj.cy,r=obj.r;ctx.ellipse(cx,cy,8,r,0,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(cx,cy-r-8);ctx.lineTo(cx-6,cy-r);ctx.moveTo(cx,cy-r-8);ctx.lineTo(cx+6,cy-r);ctx.moveTo(cx,cy+r+8);ctx.lineTo(cx-6,cy+r);ctx.moveTo(cx,cy+r+8);ctx.lineTo(cx+6,cy+r);ctx.stroke();ctx.fillStyle="#94a3b8";ctx.font="10px Arial";ctx.textAlign="center";ctx.fillText("f="+obj.f+"px",cx,cy+r+24)}
  }
  // laser source
  ctx.beginPath();ctx.arc(laserX,laserY,8,0,Math.PI*2);ctx.fillStyle="#ef4444";ctx.shadowColor="#ef4444";ctx.shadowBlur=12;ctx.fill();ctx.shadowBlur=0;
  ctx.fillStyle="#ef4444";ctx.font="bold 9px Arial";ctx.textAlign="center";ctx.fillText("LAZER",laserX,laserY+20);
  // trace
  let dx=mouseX-laserX,dy=mouseY-laserY,dl=Math.hypot(dx,dy);if(dl>0){dx/=dl;dy/=dl}
  traceRay(laserX,laserY,dx,dy,"#ef4444",0);
  requestAnimationFrame(draw);
}
cv.addEventListener("mousemove",e=>{let r=cv.getBoundingClientRect();mouseX=e.clientX-r.left;mouseY=e.clientY-r.top});
cv.addEventListener("click",e=>{let r=cv.getBoundingClientRect();let mx=e.clientX-r.left,my=e.clientY-r.top;if(Math.hypot(mx-laserX,my-laserY)<20){return}laserX=mx;laserY=my});
setPreset(0);draw();
</script></body></html>"""
        components.html(optik_html, height=600)

    # ── SUB-TAB 5: Dalga Havuzu ──
    with sub_tabs[4]:
        dalga_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow:hidden}
canvas{display:block;margin:0 auto;cursor:crosshair}
.bar{display:flex;gap:6px;justify-content:center;padding:8px;background:linear-gradient(135deg,#1e293b,#0f172a);flex-wrap:wrap;align-items:center;border-bottom:1px solid #334155}
.bar button{padding:6px 14px;border:1px solid #334155;border-radius:8px;background:#0f172a;color:#e2e8f0;cursor:pointer;font-size:0.78rem;transition:all .2s}
.bar button:hover{background:#334155}
.bar button.act{border-color:#10b981;color:#10b981}
.bar label{font-size:0.75rem;color:#94a3b8}
.bar input[type=range]{width:80px;accent-color:#10b981}
.vals{display:flex;gap:12px;justify-content:center;padding:6px;background:#1e293b;border-top:1px solid #334155;font-size:0.8rem}
.vals span{color:#10b981;font-weight:700}
</style></head><body>
<div class="bar">
  <label>Frekans: <input type="range" id="freq" min="1" max="10" value="4" step="0.5"><span id="fv">4.0 Hz</span></label>
  <label>Genlik: <input type="range" id="amp" min="1" max="10" value="5"><span id="av">5</span></label>
  <button onclick="setPreset(0)" class="act" id="pb0">Tek Kaynak</button>
  <button onclick="setPreset(1)" id="pb1">Cift Yarik</button>
  <button onclick="setPreset(2)" id="pb2">Girisim</button>
  <button onclick="setPreset(3)" id="pb3">Kirinım</button>
  <button onclick="clearSrc()" style="border-color:#ef4444;color:#ef4444">Temizle</button>
</div>
<canvas id="cv" width="700" height="460"></canvas>
<div class="vals">
  Dalga boyu: <span id="wl">50 px</span> | Frekans: <span id="fr">4.0 Hz</span> | Kaynaklar: <span id="sc">1</span> | Tikla = yeni kaynak ekle
</div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
const W=700,H=460,RES=3;
const cols=Math.floor(W/RES),rows=Math.floor(H/RES);
let sources=[],time=0,preset=0;
let freq=4,amp=5;
document.getElementById("freq").oninput=function(){freq=parseFloat(this.value);document.getElementById("fv").textContent=freq.toFixed(1)+" Hz"};
document.getElementById("amp").oninput=function(){amp=parseInt(this.value);document.getElementById("av").textContent=amp};
function setPreset(i){
  preset=i;sources=[];
  document.querySelectorAll(".bar button[id^=pb]").forEach((b,j)=>b.classList.toggle("act",j===i));
  if(i===0)sources=[{x:350,y:230}];
  else if(i===1){sources=[{x:320,y:230},{x:380,y:230}]}
  else if(i===2){sources=[{x:250,y:200},{x:450,y:260},{x:350,y:350}]}
  else{sources=[{x:340,y:230},{x:360,y:230}]}
  document.getElementById("sc").textContent=sources.length;
}
function clearSrc(){sources=[];document.getElementById("sc").textContent="0"}
cv.addEventListener("click",e=>{let r=cv.getBoundingClientRect();sources.push({x:e.clientX-r.left,y:e.clientY-r.top});document.getElementById("sc").textContent=sources.length});
let imgData=ctx.createImageData(W,H);
function draw(){
  time+=0.05;
  let wl=200/freq;
  document.getElementById("wl").textContent=Math.round(wl)+" px";
  document.getElementById("fr").textContent=freq.toFixed(1)+" Hz";
  let data=imgData.data;
  for(let py=0;py<rows;py++){
    for(let px=0;px<cols;px++){
      let wx=px*RES,wy=py*RES;
      let val=0;
      for(let s of sources){
        let d=Math.hypot(wx-s.x,wy-s.y);
        let phase=d/wl*Math.PI*2-time*freq;
        let atten=amp/(1+d*0.008);
        val+=Math.sin(phase)*atten;
      }
      let norm=val/amp;
      let r,g,b;
      if(norm>0){r=Math.min(255,Math.floor(norm*200)+30);g=30;b=30}
      else{r=30;g=30;b=Math.min(255,Math.floor(-norm*200)+30)}
      let w=Math.abs(norm)<0.08?20:0;r+=w;g+=w;b+=w;
      for(let dy=0;dy<RES;dy++){for(let dx=0;dx<RES;dx++){let idx=((py*RES+dy)*W+(px*RES+dx))*4;data[idx]=r;data[idx+1]=g;data[idx+2]=b;data[idx+3]=255}}
    }
  }
  ctx.putImageData(imgData,0,0);
  // draw source markers
  sources.forEach((s,i)=>{ctx.beginPath();ctx.arc(s.x,s.y,6,0,Math.PI*2);ctx.fillStyle="#10b981";ctx.shadowColor="#10b981";ctx.shadowBlur=10;ctx.fill();ctx.shadowBlur=0;ctx.fillStyle="#e2e8f0";ctx.font="bold 8px Arial";ctx.textAlign="center";ctx.fillText("S"+(i+1),s.x,s.y+16)});
  requestAnimationFrame(draw);
}
setPreset(0);draw();
</script></body></html>"""
        components.html(dalga_html, height=600)

    # ── SUB-TAB 6: Termodinamik ──
    with sub_tabs[5]:
        termo_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow:hidden}
canvas{display:block;margin:0 auto}
.bar{display:flex;gap:8px;justify-content:center;padding:8px;background:linear-gradient(135deg,#1e293b,#0f172a);flex-wrap:wrap;align-items:center;border-bottom:1px solid #334155}
.bar label{font-size:0.78rem;color:#94a3b8;display:flex;align-items:center;gap:4px}
.bar input[type=range]{width:100px;accent-color:#10b981}
.bar span{color:#10b981;font-weight:700;font-size:0.85rem;min-width:50px}
.meters{display:flex;gap:10px;justify-content:center;padding:8px;background:#1e293b;border-top:1px solid #334155;flex-wrap:wrap}
.meter{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:6px 12px;text-align:center;min-width:100px}
.meter .v{font-size:1rem;font-weight:700;color:#10b981}
.meter .l{font-size:0.65rem;color:#94a3b8;margin-top:1px}
.eq{text-align:center;padding:4px;font-size:0.85rem;color:#0ea5e9;background:#0f172a;border-top:1px solid #1e293b}
</style></head><body>
<div class="bar">
  <label>Sicaklik: <input type="range" id="temp" min="-30" max="200" value="25"><span id="tv">25 C</span></label>
  <label>Hacim: <input type="range" id="vol" min="20" max="100" value="60"><span id="vv">60%</span></label>
  <label>Mol: <input type="range" id="mol" min="1" max="5" value="2"><span id="mv">2</span></label>
</div>
<canvas id="cv" width="700" height="400"></canvas>
<div class="meters">
  <div class="meter"><div class="v" id="mT">298 K</div><div class="l">Sicaklik</div></div>
  <div class="meter"><div class="v" id="mP">0 kPa</div><div class="l">Basinc</div></div>
  <div class="meter"><div class="v" id="mV">0 L</div><div class="l">Hacim</div></div>
  <div class="meter"><div class="v" id="mN">2 mol</div><div class="l">Mol Sayisi</div></div>
  <div class="meter"><div class="v" id="mPhase">Gaz</div><div class="l">Faz</div></div>
</div>
<div class="eq" id="eq">PV = nRT</div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
const R_CONST=8.314;
let particles=[],tempC=25,volPct=60,nMol=2,frame=0,collCount=0;
const maxP=80;
function initParticles(){
  particles=[];let n=nMol*25;
  let bx=100,by=40,bw=getBoxW(),bh=320;
  for(let i=0;i<n;i++){particles.push({x:bx+20+Math.random()*(bw-40),y:by+20+Math.random()*(bh-40),vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*4,r:4,color:getParticleColor()})}
}
function getBoxW(){return 200+(volPct/100)*300}
function getParticleColor(){
  if(tempC<0)return"#60a5fa";if(tempC<50)return"#10b981";if(tempC<100)return"#f59e0b";return"#ef4444";
}
function getSpeed(){return Math.max(0.3,Math.sqrt((tempC+273)/300)*4)}
document.getElementById("temp").oninput=function(){tempC=parseInt(this.value);document.getElementById("tv").textContent=tempC+" C";let spd=getSpeed();particles.forEach(p=>{let a=Math.atan2(p.vy,p.vx);p.vx=Math.cos(a)*spd*(0.8+Math.random()*0.4);p.vy=Math.sin(a)*spd*(0.8+Math.random()*0.4);p.color=getParticleColor()})};
document.getElementById("vol").oninput=function(){volPct=parseInt(this.value);document.getElementById("vv").textContent=volPct+"%"};
document.getElementById("mol").oninput=function(){nMol=parseInt(this.value);document.getElementById("mv").textContent=nMol;initParticles()};
function updatePhysics(){
  let bx=100,by=40,bw=getBoxW(),bh=320;
  let spd=getSpeed();collCount=0;
  let phase="Gaz";if(tempC<0)phase="Kati (Buz)";else if(tempC>=100)phase="Buhar";
  // crystal lattice for solid
  if(tempC<0){
    let cols=Math.ceil(Math.sqrt(particles.length));
    let spacing=Math.min(bw/(cols+1),bh/(cols+1));
    particles.forEach((p,i)=>{
      let tx=bx+30+(i%cols)*spacing,ty=by+bh-30-Math.floor(i/cols)*spacing;
      p.vx+=(tx-p.x)*0.05;p.vy+=(ty-p.y)*0.05;p.vx*=0.85;p.vy*=0.85;
      p.x+=p.vx*0.3;p.y+=p.vy*0.3;
    });
  }else{
    particles.forEach(p=>{
      if(tempC>=100&&Math.random()<0.02){p.vy-=0.5}
      p.x+=p.vx;p.y+=p.vy;
      if(p.x-p.r<bx){p.x=bx+p.r;p.vx=Math.abs(p.vx);collCount++}
      if(p.x+p.r>bx+bw){p.x=bx+bw-p.r;p.vx=-Math.abs(p.vx);collCount++}
      if(p.y-p.r<by){if(tempC>=100){p.y=by+bh-20;p.x=bx+20+Math.random()*(bw-40)}else{p.y=by+p.r;p.vy=Math.abs(p.vy);collCount++}}
      if(p.y+p.r>by+bh){p.y=by+bh-p.r;p.vy=-Math.abs(p.vy);collCount++}
      // random thermal jiggle
      p.vx+=(Math.random()-0.5)*spd*0.1;p.vy+=(Math.random()-0.5)*spd*0.1;
      let s=Math.hypot(p.vx,p.vy);if(s>spd*2){p.vx*=spd*2/s;p.vy*=spd*2/s}
    });
  }
  // calc PV=nRT
  let T=tempC+273.15;let V=(volPct/100)*22.4*nMol;let P=nMol*R_CONST*T/V;
  document.getElementById("mT").textContent=Math.round(T)+" K";
  document.getElementById("mP").textContent=P.toFixed(1)+" kPa";
  document.getElementById("mV").textContent=V.toFixed(1)+" L";
  document.getElementById("mN").textContent=nMol+" mol";
  document.getElementById("mPhase").textContent=phase;document.getElementById("mPhase").style.color=tempC<0?"#60a5fa":tempC>=100?"#ef4444":"#10b981";
  document.getElementById("eq").textContent="PV = nRT  |  "+P.toFixed(1)+" x "+V.toFixed(1)+" = "+nMol+" x 8.314 x "+Math.round(T)+" = "+(nMol*R_CONST*T).toFixed(0);
}
function draw(){
  frame++;ctx.clearRect(0,0,700,400);
  ctx.fillStyle="#0a0f1e";ctx.fillRect(0,0,700,400);
  let bx=100,by=40,bw=getBoxW(),bh=320;
  // container
  ctx.fillStyle="#0f172a";ctx.strokeStyle="#475569";ctx.lineWidth=2;
  ctx.fillRect(bx,by,bw,bh);ctx.strokeRect(bx,by,bw,bh);
  // piston on right wall
  ctx.fillStyle="#334155";ctx.fillRect(bx+bw-4,by,8,bh);
  ctx.fillStyle="#475569";for(let yy=by;yy<by+bh;yy+=20){ctx.fillRect(bx+bw-2,yy,4,10)}
  // arrows showing volume change
  ctx.fillStyle="#64748b";ctx.font="10px Arial";ctx.textAlign="center";ctx.fillText("\u2190 Hacim: "+volPct+"% \u2192",bx+bw/2,by-8);
  // particles
  particles.forEach(p=>{
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=p.color;
    if(tempC>=100){ctx.globalAlpha=0.5+Math.sin(frame*0.1+p.x)*0.3}
    ctx.shadowColor=p.color;ctx.shadowBlur=tempC>50?8:3;ctx.fill();ctx.shadowBlur=0;ctx.globalAlpha=1;
    // velocity trail
    if(tempC>0){ctx.strokeStyle=p.color;ctx.globalAlpha=0.15;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x-p.vx*3,p.y-p.vy*3);ctx.stroke();ctx.globalAlpha=1}
  });
  // steam effect
  if(tempC>=100){
    for(let i=0;i<2;i++){let sx=bx+Math.random()*bw,sy=by-Math.random()*20;ctx.beginPath();ctx.arc(sx,sy,2+Math.random()*3,0,Math.PI*2);ctx.fillStyle="rgba(148,163,184,"+(Math.random()*0.3)+")";ctx.fill()}
  }
  // ice crystal lines
  if(tempC<0){
    ctx.strokeStyle="rgba(96,165,250,0.15)";ctx.lineWidth=1;
    for(let i=0;i<particles.length;i++){for(let j=i+1;j<particles.length;j++){let d=Math.hypot(particles[i].x-particles[j].x,particles[i].y-particles[j].y);if(d<40){ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);ctx.lineTo(particles[j].x,particles[j].y);ctx.stroke()}}}
  }
  // pressure gauge
  let T=tempC+273.15,V=(volPct/100)*22.4*nMol,P=nMol*R_CONST*T/V;
  let gx=30,gy=100,gr=30;
  ctx.beginPath();ctx.arc(gx,gy,gr,0,Math.PI*2);ctx.fillStyle="#1e293b";ctx.strokeStyle="#475569";ctx.lineWidth=2;ctx.fill();ctx.stroke();
  let angle=-Math.PI*0.75+Math.min(P/500,1)*Math.PI*1.5;
  ctx.strokeStyle="#ef4444";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(gx,gy);ctx.lineTo(gx+Math.cos(angle)*22,gy+Math.sin(angle)*22);ctx.stroke();
  ctx.fillStyle="#94a3b8";ctx.font="8px Arial";ctx.textAlign="center";ctx.fillText("Basinc",gx,gy+gr+12);ctx.fillText(P.toFixed(0)+" kPa",gx,gy+gr+22);
  updatePhysics();requestAnimationFrame(draw);
}
initParticles();draw();
</script></body></html>"""
        components.html(termo_html, height=600)


def _render_blok_kodlama():
    """Blok Kodlama — gorsel kodlama ortami."""
    styled_section("Blok Kodlama", "#8b5cf6")
    import streamlit.components.v1 as components

    level = st.selectbox(
        "Seviye Sec",
        ["1 - Ilerle", "2 - Kare Ciz", "3 - Zig-Zag", "4 - Spiral", "5 - Labirent"],
        key="bv_blok_level"
    )
    level_num = int(level[0])

    block_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;font-family:Arial,sans-serif;color:#e2e8f0;overflow:hidden;display:flex;flex-direction:column;height:100vh}
.top{display:flex;flex:1;overflow:hidden}
.blocks-panel{width:170px;background:#1e293b;padding:10px;overflow-y:auto;border-right:1px solid #334155}
.blocks-panel h3{font-size:0.8rem;color:#94a3b8;margin:8px 0 4px;text-transform:uppercase;letter-spacing:1px}
.block-btn{display:block;width:100%;padding:8px 10px;margin:3px 0;border:none;border-radius:6px;cursor:pointer;font-size:0.78rem;text-align:left;color:#fff;font-weight:600}
.block-btn:hover{opacity:0.85;transform:scale(1.03)}
.bm{background:#3b82f6}.bc{background:#f59e0b}.bg{background:#10b981}
.workspace{flex:1;display:flex;flex-direction:column;background:#0c1222;border-right:1px solid #334155}
.ws-header{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:#1e293b;border-bottom:1px solid #334155}
.ws-header span{font-size:0.85rem;font-weight:700}
.ws-body{flex:1;padding:10px;overflow-y:auto;display:flex;flex-direction:column;gap:4px}
.ws-block{padding:7px 12px;border-radius:6px;font-size:0.78rem;font-weight:600;color:#fff;opacity:0.95;display:flex;align-items:center;gap:6px}
.ws-block .remove{cursor:pointer;margin-left:auto;opacity:0.5;font-size:0.7rem}
.ws-block .remove:hover{opacity:1}
.preview-panel{width:240px;display:flex;flex-direction:column;background:#1e293b}
.preview-header{padding:8px 12px;font-size:0.85rem;font-weight:700;border-bottom:1px solid #334155}
canvas{background:#0a0a1a;margin:8px;border-radius:8px}
.pv-info{padding:6px 12px;font-size:0.75rem;color:#94a3b8;text-align:center}
.bottom{display:flex;gap:8px;padding:8px 12px;background:#1e293b;border-top:1px solid #334155;align-items:center;justify-content:center}
.bottom button{padding:8px 22px;border:none;border-radius:8px;cursor:pointer;font-size:0.85rem;font-weight:700;color:#fff}
.btn-run{background:#10b981}.btn-run:hover{background:#059669}
.btn-clear{background:#64748b}.btn-clear:hover{background:#475569}
.step-counter{color:#0ea5e9;font-weight:700;font-size:0.9rem}
.level-desc{padding:6px 12px;font-size:0.75rem;color:#94a3b8;background:#0f172a;border-bottom:1px solid #1e293b}
.success-msg{color:#10b981;font-weight:700;font-size:0.9rem;text-align:center;padding:4px}
</style></head><body>
<div class="top">
  <div class="blocks-panel">
    <h3>Hareket</h3>
    <button class="block-btn bm" onclick="addBlock('forward')">Ileri Git</button>
    <button class="block-btn bm" onclick="addBlock('backward')">Geri Git</button>
    <button class="block-btn bm" onclick="addBlock('right')">Saga Don</button>
    <button class="block-btn bm" onclick="addBlock('left')">Sola Don</button>
    <h3>Kontrol</h3>
    <button class="block-btn bc" onclick="addBlock('repeat3')">Tekrarla 3 kez</button>
    <button class="block-btn bc" onclick="addBlock('endrepeat')">Tekrar Sonu</button>
    <h3>Gorunum</h3>
    <button class="block-btn bg" onclick="addBlock('color')">Renk Degistir</button>
    <button class="block-btn bg" onclick="addBlock('grow')">Boyut Buyut</button>
    <button class="block-btn bg" onclick="addBlock('toggle')">Gizle/Goster</button>
  </div>
  <div class="workspace">
    <div class="ws-header"><span>Kod Alani</span><span class="step-counter" id="stepCount">Adim: 0</span></div>
    <div class="level-desc" id="levelDesc"></div>
    <div class="ws-body" id="wsBody"></div>
    <div class="success-msg" id="successMsg"></div>
  </div>
  <div class="preview-panel">
    <div class="preview-header">Onizleme</div>
    <canvas id="pv" width="200" height="200"></canvas>
    <div class="pv-info" id="pvInfo">Calistir butonuna basin</div>
  </div>
</div>
<div class="bottom">
  <button class="btn-run" onclick="runCode()">Calistir</button>
  <button class="btn-clear" onclick="clearWs()">Temizle</button>
</div>
<script>
const LEVEL=""" + str(level_num) + r""";
const cv=document.getElementById("pv"),ctx=cv.getContext("2d");
let blocks=[],charX=20,charY=180,charAngle=-90,charSize=10,charColor="#0ea5e9",charVisible=true;
let stepCount=0,trail=[];
const COLORS=["#0ea5e9","#f97316","#10b981","#a855f7","#ef4444","#facc15"];
let colorIdx=0;
let starX=0,starY=0,targetReached=false;

const LEVEL_DESC={
  1:"Karakteri yildiza ulastir (Ileri Git komutlarini kullan)",
  2:"Kare seklinde bir yol ciz (Ileri + Saga Don)",
  3:"Zig-zag cizerek ilerle (Ileri + Saga/Sola Don)",
  4:"Spiral ciz (Tekrarla + Ileri + Saga Don)",
  5:"Labirentte yolu bul (Haritayi incele)"
};

const MAZES={
  5:[
    [1,1,1,1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,0,0,1],
    [1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0],
    [1,0,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1]
  ]
};

function setupLevel(){
  charX=20;charY=180;charAngle=-90;charSize=10;charColor="#0ea5e9";charVisible=true;
  trail=[];targetReached=false;
  if(LEVEL===1){starX=180;starY=180}
  else if(LEVEL===2){starX=20;starY=180}
  else if(LEVEL===3){starX=180;starY=20}
  else if(LEVEL===4){starX=100;starY=100}
  else{charX=10;charY=30;charAngle=0;starX=190;starY=150}
  document.getElementById("levelDesc").textContent="Seviye "+LEVEL+": "+LEVEL_DESC[LEVEL];
}

function drawScene(){
  ctx.clearRect(0,0,200,200);
  ctx.fillStyle="#0a0a1a";ctx.fillRect(0,0,200,200);
  // grid
  ctx.strokeStyle="#1e293b";ctx.lineWidth=0.5;
  for(let i=0;i<=200;i+=20){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,200);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(200,i);ctx.stroke()}

  // maze for level 5
  if(LEVEL===5&&MAZES[5]){
    let m=MAZES[5],cs=20;
    for(let r=0;r<m.length;r++)for(let c=0;c<m[r].length;c++){
      if(m[r][c]===1){ctx.fillStyle="#334155";ctx.fillRect(c*cs,r*cs,cs,cs)}
    }
  }

  // trail
  ctx.strokeStyle="rgba(14,165,233,0.3)";ctx.lineWidth=2;
  if(trail.length>1){ctx.beginPath();ctx.moveTo(trail[0].x,trail[0].y);
    trail.forEach(p=>ctx.lineTo(p.x,p.y));ctx.stroke()}

  // star target
  ctx.save();ctx.translate(starX,starY);ctx.fillStyle="#facc15";
  for(let i=0;i<5;i++){
    ctx.beginPath();ctx.moveTo(0,-8);ctx.lineTo(2,-3);ctx.lineTo(7,-3);ctx.lineTo(3,1);ctx.lineTo(5,7);
    ctx.lineTo(0,3);ctx.lineTo(-5,7);ctx.lineTo(-3,1);ctx.lineTo(-7,-3);ctx.lineTo(-2,-3);ctx.closePath();ctx.fill();
  }
  ctx.restore();

  // character
  if(charVisible){
    ctx.save();ctx.translate(charX,charY);ctx.rotate(charAngle*Math.PI/180);
    ctx.beginPath();ctx.moveTo(charSize,0);ctx.lineTo(-charSize,-charSize*0.7);ctx.lineTo(-charSize,charSize*0.7);ctx.closePath();
    ctx.fillStyle=charColor;ctx.shadowColor=charColor;ctx.shadowBlur=8;ctx.fill();ctx.shadowBlur=0;
    ctx.restore();
  }
}

function addBlock(type){
  const names={forward:"Ileri Git",backward:"Geri Git",right:"Saga Don",left:"Sola Don",
    repeat3:"Tekrarla 3 kez",endrepeat:"Tekrar Sonu",color:"Renk Degistir",grow:"Boyut Buyut",toggle:"Gizle/Goster"};
  const cls={forward:"bm",backward:"bm",right:"bm",left:"bm",repeat3:"bc",endrepeat:"bc",color:"bg",grow:"bg",toggle:"bg"};
  blocks.push(type);
  let el=document.createElement("div");
  el.className="ws-block "+cls[type];
  el.innerHTML=names[type]+'<span class="remove" onclick="removeBlock(this)">X</span>';
  el.dataset.idx=blocks.length-1;
  document.getElementById("wsBody").appendChild(el);
  document.getElementById("stepCount").textContent="Adim: "+blocks.length;
}

function removeBlock(el){
  let p=el.parentElement;
  let idx=[...document.getElementById("wsBody").children].indexOf(p);
  blocks.splice(idx,1);p.remove();
  document.getElementById("stepCount").textContent="Adim: "+blocks.length;
}

function clearWs(){
  blocks=[];document.getElementById("wsBody").innerHTML="";
  document.getElementById("stepCount").textContent="Adim: 0";
  document.getElementById("successMsg").textContent="";
  setupLevel();drawScene();
}

async function runCode(){
  setupLevel();drawScene();
  document.getElementById("successMsg").textContent="";
  let expanded=[];
  let i=0;
  while(i<blocks.length){
    if(blocks[i]==="repeat3"){
      let inner=[];i++;
      while(i<blocks.length&&blocks[i]!=="endrepeat"){inner.push(blocks[i]);i++}
      i++; // skip endrepeat
      for(let r=0;r<3;r++)expanded.push(...inner);
    } else {expanded.push(blocks[i]);i++}
  }
  stepCount=0;trail.push({x:charX,y:charY});
  for(let cmd of expanded){
    await new Promise(r=>setTimeout(r,200));
    let step=20;
    if(cmd==="forward"){
      charX+=Math.cos(charAngle*Math.PI/180)*step;
      charY+=Math.sin(charAngle*Math.PI/180)*step;
    } else if(cmd==="backward"){
      charX-=Math.cos(charAngle*Math.PI/180)*step;
      charY-=Math.sin(charAngle*Math.PI/180)*step;
    } else if(cmd==="right"){charAngle+=90}
    else if(cmd==="left"){charAngle-=90}
    else if(cmd==="color"){colorIdx=(colorIdx+1)%COLORS.length;charColor=COLORS[colorIdx]}
    else if(cmd==="grow"){charSize=Math.min(charSize+2,20)}
    else if(cmd==="toggle"){charVisible=!charVisible}
    charX=Math.max(0,Math.min(200,charX));
    charY=Math.max(0,Math.min(200,charY));
    trail.push({x:charX,y:charY});
    stepCount++;
    drawScene();
    // check star
    if(Math.hypot(charX-starX,charY-starY)<20){
      targetReached=true;
      document.getElementById("successMsg").textContent="Tebrikler! Hedefe ulastin! ("+stepCount+" adim)";
      document.getElementById("pvInfo").textContent="Basarili!";
      break;
    }
  }
  if(!targetReached){
    document.getElementById("pvInfo").textContent="Toplam "+stepCount+" adim — hedefe ulasilamadi";
  }
}

setupLevel();drawScene();
</script></body></html>"""
    components.html(block_html, height=620)


# ---------------------------------------------------------------------------
# FEATURE – Yapay Zeka Tanitimi (AI Introduction / ML Playground)
# ---------------------------------------------------------------------------

def _render_yapay_zeka():
    """Yapay Zeka - AI/ML egitim, siniflandirma oyunu, sinir agi gorsellestirme."""
    import streamlit.components.v1 as components

    styled_section("Yapay Zeka Dunyasi", "#8b5cf6")

    _render_html("""
    <div class="bv-card">
        <div style="color:#c4b5fd !important;font-weight:700;font-size:1rem">Yapay Zeka Egitim Merkezi</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            Yapay zekayi ogren, siniflandirma oyunu oyna ve sinir aglarini kesfet.
        </div>
    </div>
    """)

    sub = st.radio("Bolum Sec", ["AI Nedir?", "Siniflandirma Oyunu", "Yapay Sinir Agi"], key="bv_yz_section", horizontal=True)

    if sub == "AI Nedir?":
        ai_edu_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:20px;overflow-y:auto}
h2{text-align:center;color:#c4b5fd;margin-bottom:18px;font-size:1.3rem}
.section{background:#1e293b;border-radius:14px;padding:18px;margin-bottom:14px;border:1px solid #334155}
.section h3{color:#a78bfa;font-size:1rem;margin-bottom:8px}
.section p{color:#cbd5e1;font-size:0.85rem;line-height:1.5}
.timeline{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
.tcard{background:#0f172a;border:1px solid #6d28d9;border-radius:10px;padding:12px;min-width:140px;flex:1;text-align:center}
.tcard .yr{color:#a78bfa;font-weight:700;font-size:1.1rem}
.tcard .desc{color:#94a3b8;font-size:0.78rem;margin-top:4px}
.fun{background:linear-gradient(135deg,#1e1b4b,#312e81);border:1px solid #6366f1;border-radius:12px;padding:14px;margin-top:10px}
.fun h3{color:#818cf8;margin-bottom:8px}
.fun li{color:#c7d2fe;font-size:0.83rem;margin:5px 0;list-style:none}
.fun li::before{content:">> ";color:#a78bfa}
</style></head><body>
<h2>Yapay Zeka Nedir?</h2>
<div class="section">
<h3>Yapay Zeka (AI)</h3>
<p>Bilgisayarlarin insan gibi dusunmesini, ogrenmesini ve karar vermesini saglayan teknoloji. Ornegin: sesli asistanlar, otonom araclar, yuz tanima sistemleri.</p>
</div>
<div class="section">
<h3>Makine Ogrenimi (ML)</h3>
<p>Bilgisayarlarin acikca programlanmadan verilerden ogrenmesi. Ornekler gosterirsin, bilgisayar kurali kendisi bulur. Ornek: Spam filtresi binlerce e-postadan "spam" ve "normal" ayirmayi ogrenir.</p>
</div>
<div class="section">
<h3>Derin Ogrenme (Deep Learning)</h3>
<p>Insan beynindeki sinir aglarindan esinlenen cok katmanli yapay sinir aglari. Goruntu tanima, dil ceviri ve ses sentezi gibi karmasik gorevlerde kullanilir.</p>
</div>
<div class="section">
<h3>Tarihsel Kilometre Taslari</h3>
<div class="timeline">
<div class="tcard"><div class="yr">1950</div><div class="desc">Turing Testi onerisi</div></div>
<div class="tcard"><div class="yr">1956</div><div class="desc">"Yapay Zeka" terimi dogdu</div></div>
<div class="tcard"><div class="yr">1997</div><div class="desc">Deep Blue satranc sampiyonunu yendi</div></div>
<div class="tcard"><div class="yr">2011</div><div class="desc">Watson Jeopardy kazandi</div></div>
<div class="tcard"><div class="yr">2016</div><div class="desc">AlphaGo Go sampiyonunu yendi</div></div>
<div class="tcard"><div class="yr">2022</div><div class="desc">ChatGPT dunyayi degistirdi</div></div>
<div class="tcard"><div class="yr">2024</div><div class="desc">GPT-4 cok modlu AI</div></div>
</div></div>
<div class="fun">
<h3>Eglenceli Bilgiler</h3>
<ul>
<li>AI satranc dunya sampiyonunu 1997'de yendi (IBM Deep Blue vs Kasparov)</li>
<li>Bir AI sistemi 1 gunde 10.000 yillik Go deneyimi kazanabilir</li>
<li>Netflix onerilerinin %80'i yapay zeka tarafindan yapilir</li>
<li>Dunya uzerinde her gun 2.5 kentilyon bayt veri uretilir — AI bunlari isler</li>
<li>Ilk yapay sinir agi 1958'de Mark I Perceptron ile olusturuldu</li>
</ul>
</div>
</body></html>"""
        components.html(ai_edu_html, height=600)

    elif sub == "Siniflandirma Oyunu":
        classify_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:20px;display:flex;flex-direction:column;align-items:center}
h2{color:#c4b5fd;margin-bottom:10px;font-size:1.2rem}
.info{font-size:0.82rem;color:#94a3b8;margin-bottom:12px;text-align:center}
canvas{border:2px solid #6d28d9;border-radius:12px;cursor:crosshair;background:#0f172a}
.controls{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap;justify-content:center}
button{padding:8px 18px;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem;transition:all 0.2s}
.btn-p{background:#7c3aed;color:#fff}.btn-p:hover{background:#6d28d9}
.btn-s{background:#334155;color:#e2e8f0}.btn-s:hover{background:#475569}
#result{margin-top:10px;font-size:0.95rem;font-weight:700;min-height:22px}
.legend{display:flex;gap:16px;margin-top:8px;font-size:0.8rem;color:#94a3b8}
.legend span{display:flex;align-items:center;gap:4px}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block}
</style></head><body>
<h2>Siniflandirma Oyunu</h2>
<div class="info">Iki kategoriyi birbirinden ayiran bir cizgi ciz. Tikla-surekle-birak.</div>
<div class="legend">
<span><span class="dot" style="background:#f472b6"></span> Meyve</span>
<span><span class="dot" style="background:#38bdf8"></span> Hayvan</span>
<span><span class="dot" style="border:2px solid #22c55e"></span> Dogru</span>
<span><span class="dot" style="border:2px solid #ef4444"></span> Yanlis</span>
</div>
<canvas id="cv" width="500" height="400"></canvas>
<div class="controls">
<button class="btn-s" onclick="setLevel(0)">Seviye 1 (Kolay)</button>
<button class="btn-s" onclick="setLevel(1)">Seviye 2 (Orta)</button>
<button class="btn-s" onclick="setLevel(2)">Seviye 3 (Zor)</button>
<button class="btn-p" onclick="evaluate()">Degerlendir</button>
<button class="btn-s" onclick="resetLine()">Cizgiyi Sil</button>
</div>
<div id="result"></div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let items=[],lineStart=null,lineEnd=null,dragging=false,level=0;
const names=["Elma","Armut","Muz","Cilek","Uzum","Portakal","Karpuz","Kiraz","Seftali","Kivi",
"Kedi","Kopek","Kus","Balik","Tavsan","At","Inek","Koyun","Fil","Aslan"];
const cats=[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1];
function genItems(lv){
  items=[];let rng=seedRng(lv*1000+42);
  for(let i=0;i<20;i++){
    let x,y;
    if(lv===0){x=cats[i]===0?80+rng()*150:280+rng()*150;y=60+rng()*280;}
    else if(lv===1){x=cats[i]===0?60+rng()*200:240+rng()*200;y=60+rng()*280;}
    else{x=50+rng()*400;y=50+rng()*300;}
    items.push({x,y,cat:cats[i],name:names[i],correct:null});
  }
}
function seedRng(s){return function(){s=Math.sin(s)*10000;return s-Math.floor(s)};}
function draw(){
  ctx.clearRect(0,0,500,400);
  ctx.fillStyle="#0f172a";ctx.fillRect(0,0,500,400);
  for(let it of items){
    ctx.beginPath();ctx.arc(it.x,it.y,14,0,Math.PI*2);
    ctx.fillStyle=it.cat===0?"#f472b6":"#38bdf8";ctx.fill();
    if(it.correct===true){ctx.strokeStyle="#22c55e";ctx.lineWidth=3;ctx.stroke();}
    else if(it.correct===false){ctx.strokeStyle="#ef4444";ctx.lineWidth=3;ctx.stroke();}
    ctx.fillStyle="#fff";ctx.font="9px Arial";ctx.textAlign="center";ctx.fillText(it.name,it.x,it.y+3);
  }
  if(lineStart&&lineEnd){
    ctx.beginPath();ctx.moveTo(lineStart.x,lineStart.y);ctx.lineTo(lineEnd.x,lineEnd.y);
    ctx.strokeStyle="#a78bfa";ctx.lineWidth=2;ctx.setLineDash([6,4]);ctx.stroke();ctx.setLineDash([]);
  }
}
cv.addEventListener("mousedown",e=>{let r=cv.getBoundingClientRect();lineStart={x:e.clientX-r.left,y:e.clientY-r.top};lineEnd=null;dragging=true;});
cv.addEventListener("mousemove",e=>{if(!dragging)return;let r=cv.getBoundingClientRect();lineEnd={x:e.clientX-r.left,y:e.clientY-r.top};draw();});
cv.addEventListener("mouseup",()=>{dragging=false;});
function evaluate(){
  if(!lineStart||!lineEnd){document.getElementById("result").textContent="Once bir cizgi ciz!";return;}
  let dx=lineEnd.x-lineStart.x,dy=lineEnd.y-lineStart.y,correct=0;
  for(let it of items){
    let cross=(it.x-lineStart.x)*dy-(it.y-lineStart.y)*dx;
    let predicted=cross>0?0:1;
    it.correct=(predicted===it.cat);
    if(it.correct)correct++;
  }
  let pct=Math.round(correct/items.length*100);
  let lbl=pct>=90?"Muhtesem!":pct>=70?"Iyi!":pct>=50?"Fena degil":"Tekrar dene";
  document.getElementById("result").innerHTML="<span style='color:"+(pct>=70?"#22c55e":"#f59e0b")+"'>Dogruluk: %"+pct+" — "+lbl+"</span>";
  draw();
}
function resetLine(){lineStart=null;lineEnd=null;items.forEach(it=>it.correct=null);document.getElementById("result").textContent="";draw();}
function setLevel(lv){level=lv;resetLine();genItems(lv);draw();}
genItems(0);draw();
</script></body></html>"""
        components.html(classify_html, height=600)

    else:  # Yapay Sinir Agi
        nn_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:20px;display:flex;flex-direction:column;align-items:center}
h2{color:#c4b5fd;margin-bottom:6px;font-size:1.2rem}
.info{font-size:0.82rem;color:#94a3b8;margin-bottom:12px;text-align:center}
canvas{border:2px solid #6d28d9;border-radius:12px;background:#0f172a}
.controls{display:flex;gap:12px;margin-top:14px;flex-wrap:wrap;align-items:center;justify-content:center}
.tog{display:flex;align-items:center;gap:6px;font-size:0.85rem}
.tog label{color:#94a3b8}
.sw{position:relative;width:44px;height:24px}
.sw input{opacity:0;width:0;height:0}
.slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:#334155;border-radius:12px;transition:0.3s}
.slider::before{content:"";position:absolute;height:18px;width:18px;left:3px;bottom:3px;background:#e2e8f0;border-radius:50%;transition:0.3s}
.sw input:checked+.slider{background:#7c3aed}
.sw input:checked+.slider::before{transform:translateX(20px)}
select{background:#1e293b;color:#e2e8f0;border:1px solid #334155;border-radius:8px;padding:6px 12px;font-size:0.85rem}
#output{margin-top:10px;font-size:1.1rem;font-weight:700;color:#a78bfa;min-height:28px}
</style></head><body>
<h2>Yapay Sinir Agi</h2>
<div class="info">Girisleri degistir ve sinir aginin nasil calistigini izle.</div>
<canvas id="cv" width="500" height="340"></canvas>
<div class="controls">
<div class="tog"><label>Giris A:</label><label class="sw"><input type="checkbox" id="inA" onchange="update()"><span class="slider"></span></label></div>
<div class="tog"><label>Giris B:</label><label class="sw"><input type="checkbox" id="inB" onchange="update()"><span class="slider"></span></label></div>
<label style="color:#94a3b8;font-size:0.85rem">Islem:</label>
<select id="op" onchange="update()"><option value="AND">AND</option><option value="OR">OR</option><option value="XOR">XOR</option></select>
</div>
<div id="output">Cikis: 0</div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
const layers=[[{x:70,y:100,v:0},{x:70,y:240,v:0}],[{x:250,y:80,v:0},{x:250,y:170,v:0},{x:250,y:260,v:0}],[{x:430,y:170,v:0}]];
const connections=[];
for(let i=0;i<2;i++)for(let j=0;j<3;j++)connections.push({from:[0,i],to:[1,j],w:0.5,active:false});
for(let j=0;j<3;j++)connections.push({from:[1,j],to:[2,0],w:0.5,active:false});
let animFrame=0,particles=[];
function compute(){
  let a=document.getElementById("inA").checked?1:0;
  let b=document.getElementById("inB").checked?1:0;
  let op=document.getElementById("op").value;
  layers[0][0].v=a;layers[0][1].v=b;
  let out;
  if(op==="AND")out=a&b;
  else if(op==="OR")out=a|b;
  else out=a^b;
  // hidden layer activation
  let h0=Math.min(1,a*0.6+b*0.3),h1=Math.min(1,a*0.4+b*0.6),h2=Math.min(1,Math.abs(a-b)*0.8);
  if(op==="XOR"){h0=a*0.3;h1=b*0.3;h2=Math.abs(a-b)*0.9;}
  else if(op==="AND"){h0=a*0.8;h1=b*0.8;h2=(a&b)*0.7;}
  else{h0=a*0.7;h1=b*0.7;h2=(a|b)*0.6;}
  layers[1][0].v=h0;layers[1][1].v=h1;layers[1][2].v=h2;
  layers[2][0].v=out;
  connections.forEach(c=>{
    let fromN=layers[c.from[0]][c.from[1]];
    c.active=fromN.v>0.3;
  });
  return out;
}
function draw(){
  ctx.clearRect(0,0,500,340);
  // connections
  connections.forEach(c=>{
    let f=layers[c.from[0]][c.from[1]],t=layers[c.to[0]][c.to[1]];
    ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(t.x,t.y);
    ctx.strokeStyle=c.active?"rgba(167,139,250,0.7)":"rgba(51,65,85,0.5)";
    ctx.lineWidth=c.active?2.5:1;ctx.stroke();
  });
  // particles
  particles.forEach(p=>{
    ctx.beginPath();ctx.arc(p.cx,p.cy,3,0,Math.PI*2);
    ctx.fillStyle="#c4b5fd";ctx.fill();
  });
  // neurons
  const labels=[["A","B"],["H1","H2","H3"],["Out"]];
  for(let li=0;li<layers.length;li++){
    for(let ni=0;ni<layers[li].length;ni++){
      let n=layers[li][ni];
      let bright=n.v>0.3;
      ctx.beginPath();ctx.arc(n.x,n.y,22,0,Math.PI*2);
      let grad=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,22);
      if(bright){grad.addColorStop(0,"#a78bfa");grad.addColorStop(1,"#6d28d9");}
      else{grad.addColorStop(0,"#334155");grad.addColorStop(1,"#1e293b");}
      ctx.fillStyle=grad;ctx.fill();
      ctx.strokeStyle=bright?"#c4b5fd":"#475569";ctx.lineWidth=2;ctx.stroke();
      ctx.fillStyle=bright?"#fff":"#64748b";ctx.font="bold 11px Arial";ctx.textAlign="center";
      ctx.fillText(labels[li][ni],n.x,n.y-6);
      ctx.fillText(n.v.toFixed(1),n.x,n.y+10);
    }
  }
  // layer labels
  ctx.fillStyle="#64748b";ctx.font="12px Arial";ctx.textAlign="center";
  ctx.fillText("Giris",70,30);ctx.fillText("Gizli Katman",250,30);ctx.fillText("Cikis",430,30);
}
function spawnParticles(){
  particles=[];
  connections.forEach(c=>{
    if(!c.active)return;
    let f=layers[c.from[0]][c.from[1]],t=layers[c.to[0]][c.to[1]];
    let p={sx:f.x,sy:f.y,ex:t.x,ey:t.y,t:Math.random()*0.6};
    particles.push(p);
  });
}
function animate(){
  particles.forEach(p=>{
    p.t+=0.015;if(p.t>1)p.t=0;
    p.cx=p.sx+(p.ex-p.sx)*p.t;
    p.cy=p.sy+(p.ey-p.sy)*p.t;
  });
  draw();animFrame=requestAnimationFrame(animate);
}
function update(){
  let out=compute();
  document.getElementById("output").textContent="Cikis: "+out;
  document.getElementById("output").style.color=out?"#22c55e":"#ef4444";
  spawnParticles();
}
compute();spawnParticles();animate();
</script></body></html>"""
        components.html(nn_html, height=600)


# ---------------------------------------------------------------------------
# FEATURE – Elektronik Devre Lab (Electronics Lab)
# ---------------------------------------------------------------------------

def _render_elektronik_lab():
    """Elektronik Lab - Sanal devre calismasi."""
    import streamlit.components.v1 as components

    styled_section("Elektronik Devre Lab", "#f59e0b")

    _render_html("""
    <div class="bv-card">
        <div style="color:#fcd34d !important;font-weight:700;font-size:1rem">Sanal Elektronik Calisma Masasi</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            Breadboard uzerine parcalari yerlestir, kabloyla bagla ve devreyi calistir.
        </div>
    </div>
    """)

    elab_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:16px;display:flex;flex-direction:column;align-items:center}
h2{color:#fcd34d;margin-bottom:8px;font-size:1.2rem}
.info{font-size:0.82rem;color:#94a3b8;margin-bottom:10px;text-align:center}
.main{display:flex;gap:14px;width:100%;max-width:700px}
.panel{background:#1e293b;border-radius:12px;padding:12px;width:160px;border:1px solid #334155}
.panel h3{color:#fbbf24;font-size:0.85rem;margin-bottom:8px}
.comp{padding:8px;margin:4px 0;border-radius:8px;cursor:pointer;font-size:0.8rem;text-align:center;transition:all 0.2s;border:2px solid transparent}
.comp:hover{transform:scale(1.05)}
.comp.sel{border-color:#fbbf24}
canvas{border:2px solid #f59e0b;border-radius:12px;background:#1a1208;cursor:crosshair}
.btns{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;justify-content:center}
button{padding:7px 16px;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.82rem;transition:all 0.2s}
.btn-y{background:#f59e0b;color:#0f172a}.btn-y:hover{background:#d97706}
.btn-g{background:#334155;color:#e2e8f0}.btn-g:hover{background:#475569}
.btn-r{background:#dc2626;color:#fff}.btn-r:hover{background:#b91c1c}
#msg{margin-top:8px;font-size:0.9rem;font-weight:600;min-height:22px;color:#fbbf24}
.projects{background:#1e293b;border-radius:12px;padding:12px;margin-top:10px;width:100%;max-width:700px;border:1px solid #334155}
.projects h3{color:#fbbf24;font-size:0.9rem;margin-bottom:8px}
.plist{display:flex;flex-wrap:wrap;gap:8px}
.pbtn{padding:6px 12px;border-radius:8px;background:#292524;color:#fcd34d;border:1px solid #78350f;cursor:pointer;font-size:0.78rem;transition:all 0.2s}
.pbtn:hover{background:#431407}
.pinfo{margin-top:8px;font-size:0.8rem;color:#94a3b8;line-height:1.5;display:none}
</style></head><body>
<h2>Elektronik Devre Lab</h2>
<div class="info">Sol panelden parca sec, breadboard'a tikla. Kablo araci ile baglanti yap.</div>
<div class="main">
<div class="panel">
<h3>Parcalar</h3>
<div class="comp" style="background:#7f1d1d" onclick="selComp('led_red')" id="c_led_red">LED (Kirmizi)</div>
<div class="comp" style="background:#14532d" onclick="selComp('led_green')" id="c_led_green">LED (Yesil)</div>
<div class="comp" style="background:#1e3a5f" onclick="selComp('led_blue')" id="c_led_blue">LED (Mavi)</div>
<div class="comp" style="background:#44403c" onclick="selComp('resistor')" id="c_resistor">Direnc</div>
<div class="comp" style="background:#4a1d96" onclick="selComp('buzzer')" id="c_buzzer">Buzzer</div>
<div class="comp" style="background:#3f3f46" onclick="selComp('motor')" id="c_motor">Motor</div>
<div class="comp" style="background:#1c1917" onclick="selComp('button')" id="c_button">Buton</div>
<div class="comp" style="background:#713f12" onclick="selComp('battery')" id="c_battery">Pil (+/-)</div>
<hr style="border-color:#334155;margin:8px 0">
<div class="comp" style="background:#0c4a6e" onclick="selComp('wire')" id="c_wire">Kablo Araci</div>
</div>
<canvas id="cv" width="500" height="420"></canvas>
</div>
<div class="btns">
<button class="btn-y" onclick="simulate()">Calistir</button>
<button class="btn-r" onclick="clearBoard()">Temizle</button>
</div>
<div id="msg"></div>
<div class="projects">
<h3>Proje Sablonlari</h3>
<div class="plist">
<div class="pbtn" onclick="loadProject(0)">LED Yak</div>
<div class="pbtn" onclick="loadProject(1)">Trafik Lambasi</div>
<div class="pbtn" onclick="loadProject(2)">Alarm Sistemi</div>
<div class="pbtn" onclick="loadProject(3)">Fan Kontrolu</div>
<div class="pbtn" onclick="loadProject(4)">RGB LED</div>
</div>
<div class="pinfo" id="pinfo"></div>
</div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let selected=null,placed=[],wires=[],wireStart=null,simRunning=false,simFrame=0;
const GRID=20,COLS=25,ROWS=21;
const COMP_COLORS={led_red:"#ef4444",led_green:"#22c55e",led_blue:"#3b82f6",resistor:"#a8a29e",buzzer:"#8b5cf6",motor:"#6b7280",button:"#f5f5f4",battery:"#eab308"};
const COMP_LABELS={led_red:"LED",led_green:"LED",led_blue:"LED",resistor:"R",buzzer:"BZ",motor:"M",button:"BTN",battery:"BAT"};
function selComp(c){
  selected=c;
  document.querySelectorAll(".comp").forEach(el=>el.classList.remove("sel"));
  let el=document.getElementById("c_"+c);if(el)el.classList.add("sel");
}
function toGrid(px){return Math.round(px/GRID)*GRID;}
function drawBoard(){
  ctx.clearRect(0,0,500,420);
  ctx.fillStyle="#1a1208";ctx.fillRect(0,0,500,420);
  // grid holes
  for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++){
    ctx.beginPath();ctx.arc(c*GRID+10,r*GRID+10,2,0,Math.PI*2);
    ctx.fillStyle="#3f3f46";ctx.fill();
  }
  // center rails
  ctx.fillStyle="#292524";ctx.fillRect(0,GRID*5,500,2);ctx.fillRect(0,GRID*15,500,2);
  // wires
  wires.forEach(w=>{
    ctx.beginPath();ctx.moveTo(w.x1,w.y1);ctx.lineTo(w.x2,w.y2);
    ctx.strokeStyle="#fbbf24";ctx.lineWidth=2.5;ctx.stroke();
  });
  // placed components
  placed.forEach(p=>{
    let glow=simRunning&&p.active;
    if(glow&&(p.type.startsWith("led_"))){
      ctx.beginPath();ctx.arc(p.x,p.y,16,0,Math.PI*2);
      ctx.fillStyle=COMP_COLORS[p.type]+"80";ctx.fill();
    }
    ctx.beginPath();ctx.arc(p.x,p.y,10,0,Math.PI*2);
    let col=COMP_COLORS[p.type]||"#888";
    if(glow&&p.type.startsWith("led_")){ctx.shadowColor=col;ctx.shadowBlur=20;}
    else{ctx.shadowBlur=0;}
    ctx.fillStyle=col;ctx.fill();
    ctx.shadowBlur=0;
    ctx.strokeStyle=glow?"#fbbf24":"#555";ctx.lineWidth=1.5;ctx.stroke();
    ctx.fillStyle="#fff";ctx.font="bold 8px Arial";ctx.textAlign="center";
    ctx.fillText(COMP_LABELS[p.type]||"?",p.x,p.y+3);
    // motor spin
    if(glow&&p.type==="motor"){
      let a=simFrame*0.15;
      for(let i=0;i<3;i++){
        let aa=a+i*Math.PI*2/3;
        ctx.beginPath();ctx.moveTo(p.x,p.y);
        ctx.lineTo(p.x+Math.cos(aa)*12,p.y+Math.sin(aa)*12);
        ctx.strokeStyle="#e2e8f0";ctx.lineWidth=2;ctx.stroke();
      }
    }
    // buzzer vibrate
    if(glow&&p.type==="buzzer"){
      let off=Math.sin(simFrame*0.5)*3;
      ctx.beginPath();ctx.arc(p.x+off,p.y,13,0,Math.PI*2);
      ctx.strokeStyle="#c4b5fd";ctx.lineWidth=1;ctx.setLineDash([2,2]);ctx.stroke();ctx.setLineDash([]);
    }
  });
  // wire in progress
  if(wireStart){
    ctx.beginPath();ctx.arc(wireStart.x,wireStart.y,4,0,Math.PI*2);
    ctx.fillStyle="#fbbf24";ctx.fill();
  }
}
cv.addEventListener("click",e=>{
  let r=cv.getBoundingClientRect();
  let mx=toGrid(e.clientX-r.left),my=toGrid(e.clientY-r.top);
  if(!selected)return;
  if(selected==="wire"){
    if(!wireStart){wireStart={x:mx,y:my};}
    else{wires.push({x1:wireStart.x,y1:wireStart.y,x2:mx,y2:my});wireStart=null;}
  } else {
    placed.push({type:selected,x:mx,y:my,active:false});
  }
  drawBoard();
});
function simulate(){
  // simple connectivity: find battery, see what's connected via wires
  let batts=placed.filter(p=>p.type==="battery");
  if(batts.length===0){document.getElementById("msg").textContent="Pil yerlestirmelisin!";return;}
  placed.forEach(p=>p.active=false);
  // BFS from battery through wires
  let connected=new Set();
  function near(x1,y1,x2,y2){return Math.hypot(x1-x2,y1-y2)<25;}
  let queue=[...batts];
  batts.forEach(b=>{b.active=true;connected.add(b);});
  while(queue.length){
    let cur=queue.shift();
    wires.forEach(w=>{
      let touchA=near(cur.x,cur.y,w.x1,w.y1),touchB=near(cur.x,cur.y,w.x2,w.y2);
      if(touchA||touchB){
        let ox=touchA?w.x2:w.x1,oy=touchA?w.y2:w.y1;
        placed.forEach(p=>{
          if(!connected.has(p)&&near(p.x,p.y,ox,oy)){
            p.active=true;connected.add(p);queue.push(p);
          }
        });
      }
    });
  }
  simRunning=true;
  let activeNames=placed.filter(p=>p.active&&p.type!=="battery").map(p=>COMP_LABELS[p.type]);
  document.getElementById("msg").textContent=activeNames.length?"Devre calisiyor: "+activeNames.join(", ")+" aktif!":"Bagli parca bulunamadi. Kablo ile bagla.";
  animateSim();
}
function animateSim(){
  if(!simRunning)return;
  simFrame++;drawBoard();requestAnimationFrame(animateSim);
}
function clearBoard(){
  placed=[];wires=[];wireStart=null;simRunning=false;simFrame=0;
  document.getElementById("msg").textContent="";document.getElementById("pinfo").style.display="none";
  drawBoard();
}
const PROJECTS=[
  {name:"LED Yak",desc:"1. Pil yerlestir\n2. Kirmizi LED yerlestir\n3. Pil ve LED'i kablo ile bagla\n4. Calistir butonuna bas",
   parts:[{type:"battery",x:100,y:210},{type:"led_red",x:300,y:210}],
   wires:[{x1:100,y1:210,x2:300,y2:210}]},
  {name:"Trafik Lambasi",desc:"1. Pil yerlestir\n2. Kirmizi, Sari (direnc), Yesil LED'leri dik yerlestir\n3. Hepsini pile bagla\n4. Calistir",
   parts:[{type:"battery",x:80,y:210},{type:"led_red",x:260,y:110},{type:"led_green",x:260,y:210},{type:"led_blue",x:260,y:310}],
   wires:[{x1:80,y1:210,x2:260,y2:110},{x1:260,y1:110,x2:260,y2:210},{x1:260,y1:210,x2:260,y2:310}]},
  {name:"Alarm Sistemi",desc:"1. Pil yerlestir\n2. Buton ve Buzzer yerlestir\n3. Pil->Buton->Buzzer seklinde bagla\n4. Calistir",
   parts:[{type:"battery",x:80,y:210},{type:"button",x:200,y:210},{type:"buzzer",x:340,y:210}],
   wires:[{x1:80,y1:210,x2:200,y2:210},{x1:200,y1:210,x2:340,y2:210}]},
  {name:"Fan Kontrolu",desc:"1. Pil yerlestir\n2. Buton ve Motor yerlestir\n3. Seri olarak bagla\n4. Calistir ve motoru izle",
   parts:[{type:"battery",x:80,y:210},{type:"button",x:200,y:210},{type:"motor",x:360,y:210}],
   wires:[{x1:80,y1:210,x2:200,y2:210},{x1:200,y1:210,x2:360,y2:210}]},
  {name:"RGB LED",desc:"1. Pil yerlestir\n2. Uc farkli renk LED yerlestir\n3. Hepsini pile bagla\n4. Renk karisimini gor",
   parts:[{type:"battery",x:80,y:210},{type:"led_red",x:280,y:130},{type:"led_green",x:280,y:210},{type:"led_blue",x:280,y:290}],
   wires:[{x1:80,y1:210,x2:280,y2:130},{x1:80,y1:210,x2:280,y2:210},{x1:80,y1:210,x2:280,y2:290}]}
];
function loadProject(idx){
  clearBoard();
  let p=PROJECTS[idx];
  p.parts.forEach(pp=>placed.push({type:pp.type,x:pp.x,y:pp.y,active:false}));
  p.wires.forEach(w=>wires.push({...w}));
  document.getElementById("pinfo").style.display="block";
  document.getElementById("pinfo").textContent=p.name+": "+p.desc.replace(/\n/g," | ");
  drawBoard();
}
drawBoard();
</script></body></html>"""
    components.html(elab_html, height=620)


# ---------------------------------------------------------------------------
# FEATURE – 3D Yazici Tanitimi (3D Printing Introduction)
# ---------------------------------------------------------------------------

def _render_3d_yazici():
    """3D Yazici - 3D baski egitimi ve basit modelleyici."""
    import streamlit.components.v1 as components

    styled_section("3D Yazici Dunyasi", "#10b981")

    _render_html("""
    <div class="bv-card">
        <div style="color:#6ee7b7 !important;font-weight:700;font-size:1rem">3D Baski Egitim ve Modelleme</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            3D baski teknolojisini ogren, basit sekiller olustur ve yazdir simule et.
        </div>
    </div>
    """)

    sub = st.radio("Bolum Sec", ["3D Baski Nedir?", "Sekil Olusturucu", "Proje Fikirleri"], key="bv_3d_section", horizontal=True)

    if sub == "3D Baski Nedir?":
        edu_3d_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:20px;overflow-y:auto}
h2{text-align:center;color:#6ee7b7;margin-bottom:16px;font-size:1.3rem}
.sec{background:#1e293b;border-radius:14px;padding:18px;margin-bottom:14px;border:1px solid #334155}
.sec h3{color:#34d399;font-size:1rem;margin-bottom:8px}
.sec p{color:#cbd5e1;font-size:0.85rem;line-height:1.5}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}
.mcard{flex:1;min-width:180px;background:#0f172a;border:1px solid #065f46;border-radius:12px;padding:14px;text-align:center}
.mcard h4{color:#6ee7b7;font-size:0.95rem;margin-bottom:6px}
.mcard .temp{color:#fbbf24;font-weight:700;font-size:1.1rem}
.mcard p{color:#94a3b8;font-size:0.78rem;margin-top:4px}
.steps{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}
.step{background:#064e3b;border-radius:10px;padding:12px;flex:1;min-width:100px;text-align:center}
.step .num{background:#10b981;color:#fff;width:28px;height:28px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:0.9rem;margin-bottom:6px}
.step .txt{color:#a7f3d0;font-size:0.8rem}
</style></head><body>
<h2>3D Baski Nasil Calisir?</h2>
<div class="sec">
<h3>FDM (Erimis Malzeme Biriktirme)</h3>
<p>En yaygin 3D baski yontemi. Plastik filament eritilir ve katman katman biriktirilerek 3 boyutlu nesne olusturulur. Evde kullanilan yazicilarin cogu bu teknolojiyi kullanir.</p>
<div class="steps">
<div class="step"><div class="num">1</div><div class="txt">3D model tasarla (STL dosyasi)</div></div>
<div class="step"><div class="num">2</div><div class="txt">Dilimleme yazilimi ile katmanlara bol</div></div>
<div class="step"><div class="num">3</div><div class="txt">Yazici filamenti eritir</div></div>
<div class="step"><div class="num">4</div><div class="txt">Katman katman biriktirir</div></div>
<div class="step"><div class="num">5</div><div class="txt">Soguyunca parca hazir!</div></div>
</div>
</div>
<div class="sec">
<h3>SLA (Stereolitografi)</h3>
<p>UV lazer kullanarak sivi recineyi katilastiran yontem. FDM'den cok daha detayli ve puruzsuz yuzeyli parcalar uretir. Mucevherat, dis hekimligi gibi hassas alanlarda kullanilir.</p>
</div>
<div class="sec">
<h3>Malzeme Karsilastirmasi</h3>
<div class="cards">
<div class="mcard">
<h4>PLA</h4>
<div class="temp">190-220C</div>
<p>En kolay malzeme. Bitkisel bazli, cevre dostu. Yeni baslayanlar icin ideal.</p>
<p style="color:#6ee7b7;margin-top:6px">Zorluk: Kolay</p>
</div>
<div class="mcard">
<h4>ABS</h4>
<div class="temp">230-260C</div>
<p>Dayanikli ve esnek. Lego parcalari ABS'den yapilir. Kapali ortam gerektirir.</p>
<p style="color:#fbbf24;margin-top:6px">Zorluk: Orta</p>
</div>
<div class="mcard">
<h4>PETG</h4>
<div class="temp">220-250C</div>
<p>PLA kolayligi + ABS dayanikliligi. Su siselerindeki malzeme. Gida guvenli.</p>
<p style="color:#fbbf24;margin-top:6px">Zorluk: Orta</p>
</div>
</div>
</div>
</body></html>"""
        components.html(edu_3d_html, height=650)

    elif sub == "Sekil Olusturucu":
        builder_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:16px;display:flex;flex-direction:column;align-items:center}
h2{color:#6ee7b7;margin-bottom:8px;font-size:1.2rem}
.info{font-size:0.82rem;color:#94a3b8;margin-bottom:10px;text-align:center}
.row{display:flex;gap:14px;width:100%;max-width:680px}
.panel{background:#1e293b;border-radius:12px;padding:14px;width:200px;border:1px solid #334155}
.panel h3{color:#34d399;font-size:0.85rem;margin-bottom:8px}
.field{margin-bottom:10px}
.field label{display:block;color:#94a3b8;font-size:0.78rem;margin-bottom:3px}
.field select,.field input{width:100%;padding:6px;border-radius:6px;border:1px solid #334155;background:#0f172a;color:#e2e8f0;font-size:0.82rem}
canvas{border:2px solid #10b981;border-radius:12px;background:#0a1208;cursor:pointer}
.btns{display:flex;gap:8px;margin-top:10px}
button{padding:7px 16px;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.82rem;transition:all 0.2s}
.btn-g{background:#10b981;color:#fff}.btn-g:hover{background:#059669}
.btn-s{background:#334155;color:#e2e8f0}.btn-s:hover{background:#475569}
.btn-a{background:#7c3aed;color:#fff}.btn-a:hover{background:#6d28d9}
#status{margin-top:8px;font-size:0.85rem;color:#6ee7b7;min-height:20px}
</style></head><body>
<h2>3D Sekil Olusturucu</h2>
<div class="info">Sekil sec, boyutlari ayarla ve yapi plakasina ekle. Yazdir simule et.</div>
<div class="row">
<div class="panel">
<h3>Sekil Ayarlari</h3>
<div class="field"><label>Sekil</label><select id="shape"><option value="cube">Kup</option><option value="cylinder">Silindir</option><option value="sphere">Kure</option><option value="pyramid">Piramit</option></select></div>
<div class="field"><label>Genislik (X): <span id="xv">40</span></label><input type="range" id="sx" min="20" max="100" value="40" oninput="document.getElementById('xv').textContent=this.value"></div>
<div class="field"><label>Derinlik (Y): <span id="yv">40</span></label><input type="range" id="sy" min="20" max="100" value="40" oninput="document.getElementById('yv').textContent=this.value"></div>
<div class="field"><label>Yukseklik (Z): <span id="zv">40</span></label><input type="range" id="sz" min="20" max="100" value="40" oninput="document.getElementById('zv').textContent=this.value"></div>
<div class="field"><label>Renk</label><input type="color" id="scolor" value="#10b981"></div>
<button class="btn-g" onclick="addShape()" style="width:100%;margin-top:6px">Ekle</button>
</div>
<canvas id="cv" width="440" height="440"></canvas>
</div>
<div class="btns">
<button class="btn-a" onclick="printSim()">Yazdir Simulasyonu</button>
<button class="btn-s" onclick="clearPlate()">Temizle</button>
</div>
<div id="status"></div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let shapes=[],printing=false,printLayer=0,printTotal=0;
const PW=440,PH=440,PLATE_Y=380,PLATE_X=40,PLATE_W=360;
function drawPlate(){
  ctx.clearRect(0,0,PW,PH);
  ctx.fillStyle="#0a1208";ctx.fillRect(0,0,PW,PH);
  // grid
  ctx.strokeStyle="#1a2e1a";ctx.lineWidth=0.5;
  for(let x=PLATE_X;x<=PLATE_X+PLATE_W;x+=20){ctx.beginPath();ctx.moveTo(x,PLATE_Y-300);ctx.lineTo(x,PLATE_Y);ctx.stroke();}
  for(let y=PLATE_Y;y>=PLATE_Y-300;y-=20){ctx.beginPath();ctx.moveTo(PLATE_X,y);ctx.lineTo(PLATE_X+PLATE_W,y);ctx.stroke();}
  // plate
  ctx.fillStyle="#1e3a2e";ctx.fillRect(PLATE_X-5,PLATE_Y,PLATE_W+10,12);
  ctx.strokeStyle="#10b981";ctx.lineWidth=1;ctx.strokeRect(PLATE_X-5,PLATE_Y,PLATE_W+10,12);
  ctx.fillStyle="#94a3b8";ctx.font="11px Arial";ctx.textAlign="center";
  ctx.fillText("Yapi Plakasi (Ust Gorunum + Yan Gorunum)",PW/2,PLATE_Y+24);
}
function drawShapes(){
  drawPlate();
  // draw shapes as pseudo-3D (top-down on left, side view)
  shapes.forEach((s,i)=>{
    let cx=s.px,boty=PLATE_Y;
    // side view (height shown going up from plate)
    ctx.globalAlpha=0.85;
    if(s.shape==="cube"){
      ctx.fillStyle=s.color;
      ctx.fillRect(cx-s.w/2,boty-s.h,s.w,s.h);
      ctx.strokeStyle="#fff";ctx.lineWidth=0.5;ctx.strokeRect(cx-s.w/2,boty-s.h,s.w,s.h);
      // top face (parallelogram)
      ctx.beginPath();ctx.moveTo(cx-s.w/2,boty-s.h);ctx.lineTo(cx-s.w/2+s.d*0.3,boty-s.h-s.d*0.3);
      ctx.lineTo(cx+s.w/2+s.d*0.3,boty-s.h-s.d*0.3);ctx.lineTo(cx+s.w/2,boty-s.h);ctx.closePath();
      ctx.fillStyle=s.color;ctx.fill();ctx.stroke();
      // right face
      ctx.beginPath();ctx.moveTo(cx+s.w/2,boty);ctx.lineTo(cx+s.w/2+s.d*0.3,boty-s.d*0.3);
      ctx.lineTo(cx+s.w/2+s.d*0.3,boty-s.h-s.d*0.3);ctx.lineTo(cx+s.w/2,boty-s.h);ctx.closePath();
      ctx.fillStyle=darken(s.color,0.7);ctx.fill();ctx.stroke();
    } else if(s.shape==="cylinder"){
      ctx.fillStyle=s.color;
      ctx.fillRect(cx-s.w/2,boty-s.h,s.w,s.h);
      ctx.strokeStyle="#fff";ctx.lineWidth=0.5;ctx.strokeRect(cx-s.w/2,boty-s.h,s.w,s.h);
      // top ellipse
      ctx.beginPath();ctx.ellipse(cx,boty-s.h,s.w/2,s.d*0.2,0,0,Math.PI*2);
      ctx.fillStyle=darken(s.color,1.2);ctx.fill();ctx.stroke();
      // bottom ellipse
      ctx.beginPath();ctx.ellipse(cx,boty,s.w/2,s.d*0.2,0,0,Math.PI*2);
      ctx.fillStyle=darken(s.color,0.6);ctx.fill();ctx.stroke();
    } else if(s.shape==="sphere"){
      let r=Math.min(s.w,s.h)/2;
      ctx.beginPath();ctx.arc(cx,boty-r,r,0,Math.PI*2);
      let grad=ctx.createRadialGradient(cx-r*0.3,boty-r-r*0.3,r*0.1,cx,boty-r,r);
      grad.addColorStop(0,lighten(s.color,1.4));grad.addColorStop(1,s.color);
      ctx.fillStyle=grad;ctx.fill();ctx.strokeStyle="#fff";ctx.lineWidth=0.5;ctx.stroke();
    } else if(s.shape==="pyramid"){
      ctx.beginPath();ctx.moveTo(cx,boty-s.h);ctx.lineTo(cx-s.w/2,boty);ctx.lineTo(cx+s.w/2,boty);ctx.closePath();
      ctx.fillStyle=s.color;ctx.fill();ctx.strokeStyle="#fff";ctx.lineWidth=0.5;ctx.stroke();
      // right face
      ctx.beginPath();ctx.moveTo(cx,boty-s.h);ctx.lineTo(cx+s.w/2,boty);
      ctx.lineTo(cx+s.w/2+s.d*0.2,boty-s.d*0.15);ctx.closePath();
      ctx.fillStyle=darken(s.color,0.7);ctx.fill();ctx.stroke();
    }
    ctx.globalAlpha=1;
    // label
    ctx.fillStyle="#fff";ctx.font="9px Arial";ctx.textAlign="center";
    let lbl=s.shape==="cube"?"Kup":s.shape==="cylinder"?"Silindir":s.shape==="sphere"?"Kure":"Piramit";
    ctx.fillText(lbl,cx,boty-s.h-8);
  });
  // print layer animation
  if(printing&&printLayer<printTotal){
    let ly=PLATE_Y-printLayer*(300/printTotal);
    ctx.strokeStyle="#22c55e";ctx.lineWidth=2;ctx.setLineDash([4,4]);
    ctx.beginPath();ctx.moveTo(PLATE_X,ly);ctx.lineTo(PLATE_X+PLATE_W,ly);ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle="#22c55e";ctx.font="bold 11px Arial";ctx.textAlign="left";
    ctx.fillText("Katman "+(printLayer+1)+"/"+printTotal,PLATE_X,ly-6);
  }
}
function darken(hex,f){let r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
  return"#"+[r,g,b].map(c=>Math.max(0,Math.min(255,Math.round(c*f))).toString(16).padStart(2,"0")).join("");}
function lighten(hex,f){return darken(hex,f);}
function addShape(){
  let shape=document.getElementById("shape").value;
  let w=+document.getElementById("sx").value,d=+document.getElementById("sy").value,h=+document.getElementById("sz").value;
  let color=document.getElementById("scolor").value;
  let px=PLATE_X+40+shapes.length*90;
  if(px>PLATE_X+PLATE_W-40)px=PLATE_X+60+Math.random()*200;
  shapes.push({shape,w,d,h,color,px});
  document.getElementById("status").textContent=shape+" eklendi ("+shapes.length+" parca)";
  drawShapes();
}
function clearPlate(){shapes=[];printing=false;printLayer=0;document.getElementById("status").textContent="";drawShapes();}
function printSim(){
  if(shapes.length===0){document.getElementById("status").textContent="Once sekil ekle!";return;}
  printing=true;printLayer=0;
  let maxH=Math.max(...shapes.map(s=>s.h));
  printTotal=Math.max(10,Math.round(maxH/2));
  document.getElementById("status").textContent="Yazdiriliyor... Katman 0/"+printTotal;
  function step(){
    if(printLayer>=printTotal){
      document.getElementById("status").textContent="Yazdir tamamlandi! "+shapes.length+" parca, "+printTotal+" katman.";
      printing=false;return;
    }
    printLayer++;
    document.getElementById("status").textContent="Yazdiriliyor... Katman "+printLayer+"/"+printTotal;
    drawShapes();
    requestAnimationFrame(()=>setTimeout(step,120));
  }
  step();
}
drawShapes();
</script></body></html>"""
        components.html(builder_html, height=650)

    else:  # Proje Fikirleri
        proj_html = r"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;padding:20px;overflow-y:auto}
h2{text-align:center;color:#6ee7b7;margin-bottom:16px;font-size:1.3rem}
.grid{display:flex;flex-wrap:wrap;gap:14px;justify-content:center}
.pcard{background:#1e293b;border:1px solid #065f46;border-radius:14px;padding:18px;width:280px;transition:all 0.3s}
.pcard:hover{transform:translateY(-4px);box-shadow:0 8px 25px rgba(16,185,129,0.2)}
.pcard h3{color:#6ee7b7;font-size:1rem;margin-bottom:8px}
.pcard p{color:#94a3b8;font-size:0.82rem;line-height:1.4;margin-bottom:10px}
.meta{display:flex;gap:8px;flex-wrap:wrap}
.tag{padding:3px 10px;border-radius:6px;font-size:0.72rem;font-weight:600}
.tag-time{background:#1e3a5f;color:#7dd3fc}
.tag-mat{background:#3b1d06;color:#fdba74}
.tag-diff{border:1px solid #334155}
.diff-easy{color:#22c55e;border-color:#22c55e}
.diff-med{color:#eab308;border-color:#eab308}
.diff-hard{color:#ef4444;border-color:#ef4444}
.icon{font-size:2rem;margin-bottom:8px;display:block;text-align:center}
</style></head><body>
<h2>3D Baski Proje Fikirleri</h2>
<div class="grid">
<div class="pcard">
<div class="icon">&#9998;</div>
<h3>Kalemlik</h3>
<p>Masani toparlayan cok gozlu kalemlik. Isim yazdirabilirsin. Koseleri yuvarlak tasarla.</p>
<div class="meta">
<span class="tag tag-time">~2 saat</span>
<span class="tag tag-mat">~30g PLA</span>
<span class="tag tag-diff diff-easy">Kolay</span>
</div>
</div>
<div class="pcard">
<div class="icon">&#9743;</div>
<h3>Telefon Standi</h3>
<p>Telefonunu dik tutacak stand. Sarj kablosu icin aciklik birak. Aci ayarli tasarla.</p>
<div class="meta">
<span class="tag tag-time">~1.5 saat</span>
<span class="tag tag-mat">~25g PLA</span>
<span class="tag tag-diff diff-easy">Kolay</span>
</div>
</div>
<div class="pcard">
<div class="icon">&#9919;</div>
<h3>Anahtarlik</h3>
<p>Kendi tasarimin olan anahtarlik. Isim, logo veya sembol ekleyebilirsin. Kucuk ve hizli basim.</p>
<div class="meta">
<span class="tag tag-time">~30 dk</span>
<span class="tag tag-mat">~5g PLA</span>
<span class="tag tag-diff diff-easy">Kolay</span>
</div>
</div>
<div class="pcard">
<div class="icon">&#9832;</div>
<h3>Vazo</h3>
<p>Spiral veya geometrik desenli dekoratif vazo. Ince duvar (vazo modu) ile yazdir. Su gecirmez icin PETG kullan.</p>
<div class="meta">
<span class="tag tag-time">~4 saat</span>
<span class="tag tag-mat">~80g PETG</span>
<span class="tag tag-diff diff-med">Orta</span>
</div>
</div>
<div class="pcard">
<div class="icon">&#9881;</div>
<h3>Robot Parcasi</h3>
<p>Hareketli eklemli robot kol veya govde. Birden fazla parca basip birlestirilir. Vida delikleri eklemeyi unutma.</p>
<div class="meta">
<span class="tag tag-time">~6 saat</span>
<span class="tag tag-mat">~120g PLA/ABS</span>
<span class="tag tag-diff diff-hard">Zor</span>
</div>
</div>
</div>
</body></html>"""
        components.html(proj_html, height=650)


# ---------------------------------------------------------------------------
# FEATURE 1 : Python Lab (Gelismis Python Editoru)
# ---------------------------------------------------------------------------

_PYTHON_ALISTIRMALAR = [
    {"baslik": "Merhaba Dunya", "aciklama": "Ekrana 'Merhaba Dunya!' yazdirin.", "baslangic_kodu": "# Cozumunuzu yazin\n", "beklenen_cikti": "Merhaba Dunya!", "ipucu": "print() fonksiyonunu kullanin."},
    {"baslik": "Toplama Islemi", "aciklama": "a=5, b=3 icin toplamlarini yazdirin.", "baslangic_kodu": "a = 5\nb = 3\n# Toplami yazdirin\n", "beklenen_cikti": "8", "ipucu": "print(a + b)"},
    {"baslik": "Degisken Turu", "aciklama": "x = 3.14 icin type(x).__name__ yazdirin.", "baslangic_kodu": "x = 3.14\n# Turunu yazdirin\n", "beklenen_cikti": "float", "ipucu": "print(type(x).__name__)"},
    {"baslik": "String Birlestirme", "aciklama": "ad='Ali', soyad='Veli' icin 'Ali Veli' yazdirin.", "baslangic_kodu": "ad = 'Ali'\nsoyad = 'Veli'\n# Birlesik yazdirin\n", "beklenen_cikti": "Ali Veli", "ipucu": "print(ad + ' ' + soyad)"},
    {"baslik": "Tek mi Cift mi", "aciklama": "sayi=7 icin 'Tek' veya 'Cift' yazdirin.", "baslangic_kodu": "sayi = 7\n# Tek mi Cift mi?\n", "beklenen_cikti": "Tek", "ipucu": "% operatoru ile kalan hesaplayin."},
    {"baslik": "1-10 Toplami", "aciklama": "1'den 10'a kadar (dahil) toplami yazdirin.", "baslangic_kodu": "# 1-10 toplami\n", "beklenen_cikti": "55", "ipucu": "range(1,11) ve sum() kullanin."},
    {"baslik": "Liste Uzunlugu", "aciklama": "liste = [3,1,4,1,5,9] icin uzunlugu yazdirin.", "baslangic_kodu": "liste = [3,1,4,1,5,9]\n# Uzunlugu yazdirin\n", "beklenen_cikti": "6", "ipucu": "len() fonksiyonu."},
    {"baslik": "Maksimum Eleman", "aciklama": "liste = [12,7,3,19,5] icin en buyugu yazdirin.", "baslangic_kodu": "liste = [12,7,3,19,5]\n# En buyugu yazdirin\n", "beklenen_cikti": "19", "ipucu": "max() fonksiyonu."},
    {"baslik": "String Ters Cevirme", "aciklama": "'Python' kelimesini tersten yazdirin.", "baslangic_kodu": "kelime = 'Python'\n# Tersten yazdirin\n", "beklenen_cikti": "nohtyP", "ipucu": "Dilimleme: kelime[::-1]"},
    {"baslik": "Cift Sayilar", "aciklama": "1-10 arasi cift sayilari boslukla ayirarak yazdirin.", "baslangic_kodu": "# Cift sayilar\n", "beklenen_cikti": "2 4 6 8 10", "ipucu": "range(2,11,2) kullanin."},
    {"baslik": "Kare Alma", "aciklama": "[1,2,3,4,5] listesinin karelerini yazdirin.", "baslangic_kodu": "liste = [1,2,3,4,5]\n# Kareleri yazdirin\n", "beklenen_cikti": "[1, 4, 9, 16, 25]", "ipucu": "List comprehension: [x**2 for x in liste]"},
    {"baslik": "Harf Sayma", "aciklama": "'programlama' kelimesinde kac 'a' harfi var yazdirin.", "baslangic_kodu": "kelime = 'programlama'\n# 'a' sayisini yazdirin\n", "beklenen_cikti": "3", "ipucu": "kelime.count('a')"},
    {"baslik": "Faktoriyel", "aciklama": "5! (faktoriyel) degerini yazdirin.", "baslangic_kodu": "# 5 faktoriyel\n", "beklenen_cikti": "120", "ipucu": "Dongu veya math.factorial kullanin."},
    {"baslik": "Fonksiyon Yaz", "aciklama": "Iki sayiyi carpan bir fonksiyon yazin ve carp(4,5) sonucunu yazdirin.", "baslangic_kodu": "# carp fonksiyonunu yazin\n", "beklenen_cikti": "20", "ipucu": "def carp(a,b): return a*b"},
    {"baslik": "Sozluk Erisimi", "aciklama": "ogrenci = {'ad':'Ece','yas':15} icin adi yazdirin.", "baslangic_kodu": "ogrenci = {'ad':'Ece','yas':15}\n# Adi yazdirin\n", "beklenen_cikti": "Ece", "ipucu": "ogrenci['ad']"},
    {"baslik": "FizzBuzz (1-15)", "aciklama": "1-15 arasi: 3'e bolunuyorsa Fizz, 5'e bolunuyorsa Buzz, ikisine de bolunuyorsa FizzBuzz, degilse sayiyi yazdirin.", "baslangic_kodu": "# FizzBuzz\n", "beklenen_cikti": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz", "ipucu": "if/elif/else kullanin."},
    {"baslik": "Liste Siralama", "aciklama": "[5,2,8,1,9] listesini kucukten buyuge siralayin ve yazdirin.", "baslangic_kodu": "liste = [5,2,8,1,9]\n# Siralayin ve yazdirin\n", "beklenen_cikti": "[1, 2, 5, 8, 9]", "ipucu": "sorted() fonksiyonu."},
    {"baslik": "Asal Sayi Kontrolu", "aciklama": "17 sayi icin 'Asal' veya 'Asal Degil' yazdirin.", "baslangic_kodu": "sayi = 17\n# Asal mi?\n", "beklenen_cikti": "Asal", "ipucu": "2'den sayi-1'e kadar bolenleri kontrol edin."},
    {"baslik": "Kelime Listesi", "aciklama": "'Python cok eglenceli' cumlesindeki kelime sayisini yazdirin.", "baslangic_kodu": "cumle = 'Python cok eglenceli'\n# Kelime sayisi\n", "beklenen_cikti": "3", "ipucu": "split() ile ayirin, len() ile sayin."},
    {"baslik": "Fibonacci (ilk 8)", "aciklama": "Fibonacci serisinin ilk 8 elemanini boslukla ayirarak yazdirin (0'dan baslayarak).", "baslangic_kodu": "# Fibonacci\n", "beklenen_cikti": "0 1 1 2 3 5 8 13", "ipucu": "Her eleman onceki ikisinin toplamdir."},
]

_PYTHON_ORNEKLER = [
    {"baslik": "Fibonacci Serisi", "kod": "def fibonacci(n):\n    a, b = 0, 1\n    sonuc = []\n    for _ in range(n):\n        sonuc.append(a)\n        a, b = b, a + b\n    return sonuc\n\nprint('Fibonacci (10):', fibonacci(10))"},
    {"baslik": "Asal Sayi Bulucu", "kod": "def asal_mi(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nasallar = [x for x in range(2, 50) if asal_mi(x)]\nprint('2-50 arasi asallar:', asallar)"},
    {"baslik": "Faktoriyel Hesaplama", "kod": "def faktoriyel(n):\n    if n <= 1:\n        return 1\n    return n * faktoriyel(n - 1)\n\nfor i in range(1, 8):\n    print(f'{i}! = {faktoriyel(i)}')"},
    {"baslik": "Palindrom Kontrolu", "kod": "def palindrom_mu(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]\n\nkelimeler = ['kayak', 'python', 'aba', 'racecar', 'merhaba']\nfor k in kelimeler:\n    sonuc = 'Evet' if palindrom_mu(k) else 'Hayir'\n    print(f'{k} -> Palindrom: {sonuc}')"},
    {"baslik": "Sezar Sifreleme", "kod": "def sifre(metin, kaydirma):\n    sonuc = ''\n    for c in metin:\n        if c.isalpha():\n            base = ord('A') if c.isupper() else ord('a')\n            sonuc += chr((ord(c) - base + kaydirma) % 26 + base)\n        else:\n            sonuc += c\n    return sonuc\n\norijinal = 'Merhaba Dunya'\nsifrelenmis = sifre(orijinal, 3)\nprint('Orijinal:', orijinal)\nprint('Sifreli:', sifrelenmis)\nprint('Cozulmus:', sifre(sifrelenmis, -3))"},
    {"baslik": "Basit Hesap Makinesi", "kod": "def hesapla(a, op, b):\n    if op == '+':\n        return a + b\n    elif op == '-':\n        return a - b\n    elif op == '*':\n        return a * b\n    elif op == '/':\n        return 'Hata: Sifira bolme!' if b == 0 else a / b\n    return 'Bilinmeyen islem'\n\nislemler = [(10, '+', 5), (20, '-', 8), (6, '*', 7), (15, '/', 4), (10, '/', 0)]\nfor a, op, b in islemler:\n    print(f'{a} {op} {b} = {hesapla(a, op, b)}')"},
    {"baslik": "Tahmin Oyunu Mantigi", "kod": "import random\ngizli = random.randint(1, 100)\nprint(f'Gizli sayi: {gizli}')\n\n# Simule edilmis tahminler\ntahminler = [50, 25, 75, gizli]\nfor t in tahminler:\n    if t < gizli:\n        print(f'Tahmin {t}: Daha buyuk!')\n    elif t > gizli:\n        print(f'Tahmin {t}: Daha kucuk!')\n    else:\n        print(f'Tahmin {t}: DOGRU! Tebrikler!')"},
    {"baslik": "Liste Siralama (Bubble Sort)", "kod": "def bubble_sort(lst):\n    arr = lst.copy()\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n        print(f'Adim {i+1}: {arr}')\n    return arr\n\nliste = [64, 34, 25, 12, 22, 11, 90]\nprint('Baslangic:', liste)\nsonuc = bubble_sort(liste)\nprint('Sirali:', sonuc)"},
    {"baslik": "Kelime Sayaci", "kod": "metin = 'python programlama cok eglenceli python ile kod yazmak cok guzel python harika'\nkelimeler = metin.split()\nsayac = {}\nfor k in kelimeler:\n    sayac[k] = sayac.get(k, 0) + 1\n\nprint('Kelime Frekanslari:')\nfor kelime, adet in sorted(sayac.items(), key=lambda x: -x[1]):\n    print(f'  {kelime}: {adet}')"},
    {"baslik": "Dijital Saat", "kod": "from datetime import datetime\n\nsu_an = datetime.now()\nprint(f'Tarih: {su_an.strftime(\"%d/%m/%Y\")}')\nprint(f'Saat: {su_an.strftime(\"%H:%M:%S\")}')\nprint(f'Gun: {[\"Pazartesi\",\"Sali\",\"Carsamba\",\"Persembe\",\"Cuma\",\"Cumartesi\",\"Pazar\"][su_an.weekday()]}')\nprint(f'Yilin {su_an.timetuple().tm_yday}. gunu')"},
]


def _render_python_lab():
    """Gelismis Python Editoru: Kod Yaz, Alistirmalar, Ornekler."""
    import math
    import io
    import sys
    import signal
    import threading
    import contextlib

    styled_section("Python Lab", "#10b981")

    sub = st.tabs(["Kod Yaz", "Alistirmalar", "Ornekler"])

    # --- Ortak: guvenli calistirma ---
    _SAFE_BUILTINS = {
        "print": print, "range": range, "len": len, "int": int, "float": float,
        "str": str, "list": list, "dict": dict, "tuple": tuple, "set": set,
        "sorted": sorted, "reversed": reversed, "enumerate": enumerate,
        "zip": zip, "map": map, "filter": filter, "sum": sum, "min": min,
        "max": max, "abs": abs, "round": round, "bool": bool, "type": type,
        "isinstance": isinstance, "chr": chr, "ord": ord, "hex": hex,
        "bin": bin, "oct": oct, "any": any, "all": all, "hasattr": hasattr,
        "getattr": getattr, "repr": repr, "format": format, "pow": pow,
        "divmod": divmod, "__import__": None,
    }

    _ERROR_MAP = {
        "SyntaxError": "Yazim Hatasi",
        "NameError": "Tanimlanmamis Degisken",
        "TypeError": "Tip Hatasi",
        "IndexError": "Indeks Hatasi",
        "ZeroDivisionError": "Sifira Bolme Hatasi",
        "IndentationError": "Girinti Hatasi",
        "ValueError": "Deger Hatasi",
        "KeyError": "Anahtar Hatasi",
        "AttributeError": "Ozellik Hatasi",
        "RecursionError": "Sonsuz Dongu / Ozyineleme Hatasi",
        "OverflowError": "Tasma Hatasi",
        "FileNotFoundError": "Dosya Bulunamadi Hatasi",
        "ImportError": "Iceaktarma Hatasi",
        "RuntimeError": "Calisma Zamani Hatasi",
    }

    def _mock_input(prompt=""):
        return ""

    def _safe_exec(code_str, timeout_sec=5):
        """Kodu guvenli calistir, ciktiyi dondur."""
        import math as _math
        import random as _random
        import datetime as _dt
        safe_globals = {"__builtins__": {}}
        safe_globals["__builtins__"].update(_SAFE_BUILTINS)
        safe_globals["__builtins__"]["input"] = _mock_input
        safe_globals["math"] = _math
        safe_globals["random"] = _random
        safe_globals["datetime"] = _dt.datetime

        buf = io.StringIO()
        err_msg = None
        timed_out = False

        def _run():
            nonlocal err_msg
            try:
                with contextlib.redirect_stdout(buf):
                    exec(code_str, safe_globals)
            except Exception as e:
                etype = type(e).__name__
                tr_name = _ERROR_MAP.get(etype, etype)
                detail = str(e)
                err_msg = f"{tr_name}: {detail}"

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        t.join(timeout=timeout_sec)
        if t.is_alive():
            return None, "Zaman Asimi: Kod 5 saniye icinde tamamlanamadi. Sonsuz dongu olabilir."
        output = buf.getvalue()
        return output, err_msg

    # ---- Sub-tab A: Kod Yaz ----
    with sub[0]:
        st.markdown("#### Kod Yazin ve Calistirin")
        st.caption("Guvenli ortamda Python kodu calistirin. Maksimum calisma suresi: 5 saniye.")

        if "pylab_code" not in st.session_state:
            st.session_state["pylab_code"] = "# Python kodunuzu buraya yazin\nprint('Merhaba Dunya!')\n"

        code = st.text_area(
            "Python Kodu",
            value=st.session_state.get("pylab_code", ""),
            height=300,
            key="pylab_editor",
            help="Python 3 kodu yazin",
        )
        st.session_state["pylab_code"] = code

        # satir numaralari
        if code.strip():
            lines = code.split("\n")
            numbered = "\n".join(f"{i+1:3d} | {ln}" for i, ln in enumerate(lines))
            _render_html(f"""<div style="background:#0f172a;border-radius:10px;padding:12px;
                font-family:'Courier New',monospace;font-size:0.78rem;color:#64748b;
                border:1px solid #1e293b;white-space:pre;overflow-x:auto;margin-bottom:8px;line-height:1.5">
{numbered}</div>""")

        if st.button("Calistir", key="pylab_run", type="primary"):
            output, error = _safe_exec(code)
            if error:
                _render_html(f"""<div style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.4);
                    border-radius:10px;padding:14px;margin-top:8px">
                    <div style="color:#fca5a5;font-weight:700;font-size:0.85rem">Hata</div>
                    <div style="color:#f87171;font-family:'Courier New',monospace;font-size:0.82rem;margin-top:4px;white-space:pre-wrap">{error}</div>
                </div>""")
            else:
                display = output if output else "(Cikti yok)"
                _render_html(f"""<div style="background:rgba(16,185,129,0.10);border:1px solid rgba(16,185,129,0.4);
                    border-radius:10px;padding:14px;margin-top:8px">
                    <div style="color:#6ee7b7;font-weight:700;font-size:0.85rem">Cikti</div>
                    <div style="color:#a7f3d0;font-family:'Courier New',monospace;font-size:0.82rem;margin-top:4px;white-space:pre-wrap">{display}</div>
                </div>""")

    # ---- Sub-tab B: Alistirmalar ----
    with sub[1]:
        st.markdown("#### Kodlama Alistirmalari (20 Soru)")

        if "pylab_progress" not in st.session_state:
            st.session_state["pylab_progress"] = set()

        tamamlanan = len(st.session_state["pylab_progress"])
        st.progress(tamamlanan / 20, text=f"Ilerleme: {tamamlanan}/20 tamamlandi")

        for idx, al in enumerate(_PYTHON_ALISTIRMALAR):
            tamamlandi = idx in st.session_state["pylab_progress"]
            ikon = "checkmark" if tamamlandi else ""
            badge = " [Tamamlandi]" if tamamlandi else ""
            with st.expander(f"{'[OK] ' if tamamlandi else ''}{idx+1}. {al['baslik']}{badge}", expanded=False):
                st.markdown(f"**Gorev:** {al['aciklama']}")
                with st.popover("Ipucu"):
                    st.markdown(al["ipucu"])

                user_code = st.text_area(
                    "Cozumunuz",
                    value=al["baslangic_kodu"],
                    height=150,
                    key=f"pylab_al_{idx}",
                )

                if st.button("Kontrol Et", key=f"pylab_check_{idx}"):
                    output, error = _safe_exec(user_code)
                    if error:
                        st.error(f"Hata: {error}")
                    else:
                        cikti = (output or "").strip()
                        beklenen = al["beklenen_cikti"].strip()
                        if cikti == beklenen:
                            st.session_state["pylab_progress"].add(idx)
                            _render_html("""<div style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.5);
                                border-radius:10px;padding:12px;text-align:center;margin-top:6px">
                                <span style="color:#6ee7b7;font-weight:700;font-size:1rem">Dogru! Tebrikler!</span>
                            </div>""")
                            st.rerun()
                        else:
                            _render_html(f"""<div style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.4);
                                border-radius:10px;padding:12px;margin-top:6px">
                                <span style="color:#fca5a5;font-weight:700">Yanlis</span><br/>
                                <span style="color:#f87171;font-size:0.82rem">Beklenen: <code>{beklenen}</code></span><br/>
                                <span style="color:#f87171;font-size:0.82rem">Senin ciktin: <code>{cikti}</code></span>
                            </div>""")

    # ---- Sub-tab C: Ornekler ----
    with sub[2]:
        st.markdown("#### Hazir Ornekler (10 Program)")
        st.caption("Bir ornegi secin, kodu duzenleyin ve calistirin.")

        for idx, ornek in enumerate(_PYTHON_ORNEKLER):
            with st.expander(f"{idx+1}. {ornek['baslik']}", expanded=False):
                _render_html(f"""<div style="background:#0f172a;border-radius:10px;padding:14px;
                    font-family:'Courier New',monospace;font-size:0.8rem;color:#10b981;
                    border:1px solid #1e293b;white-space:pre-wrap;line-height:1.5;margin-bottom:8px">
{ornek['kod']}</div>""")
                if st.button("Kodu Yukle", key=f"pylab_load_{idx}"):
                    st.session_state["pylab_code"] = ornek["kod"]
                    st.toast(f"'{ornek['baslik']}' kodu yuklendi! 'Kod Yaz' sekmesine gecin.")


# ---------------------------------------------------------------------------
# FEATURE 2 : Algoritma Lab (Algoritma Gorsellestirme)
# ---------------------------------------------------------------------------

def _render_algoritma_lab():
    """Algoritma gorsellestirme: Siralama, Arama, Veri Yapilari, Labirent."""
    import streamlit.components.v1 as components

    styled_section("Algoritma Lab", "#8b5cf6")

    sub = st.tabs(["Siralama", "Arama", "Veri Yapilari", "Labirent"])

    # ---- Sub-tab A: Siralama ----
    with sub[0]:
        st.markdown("#### Siralama Algoritmalari Gorsellestirmesi")

        algo_info = {
            "Bubble Sort": "O(n^2) - En basit siralama. Yan yana elemanlari karsilastirir ve yer degistirir.",
            "Selection Sort": "O(n^2) - Her adimda en kucuk elemani bulup basa koyar.",
            "Insertion Sort": "O(n^2) - Elemanlari teker teker dogru yerine yerlestirir. Kucuk dizilerde hizlidir.",
            "Quick Sort": "O(n log n) ort. - Pivot eleman secip diziyi ikiye boler. En hizli genel amacli siralama.",
        }
        c1, c2 = st.columns([1, 1])
        with c1:
            algo = st.selectbox("Algoritma", list(algo_info.keys()), key="sort_algo")
        with c2:
            speed = st.select_slider("Hiz", options=["Yavas", "Orta", "Hizli"], value="Orta", key="sort_speed")

        speed_map = {"Yavas": 300, "Orta": 100, "Hizli": 30}
        delay = speed_map[speed]

        st.info(f"**{algo}:** {algo_info[algo]}")

        sort_html = f"""<!DOCTYPE html><html><head><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#0f172a; font-family:Arial,sans-serif; overflow:hidden; }}
canvas {{ display:block; margin:10px auto; }}
.info {{ color:#94a3b8; text-align:center; font-size:14px; padding:8px; }}
.info span {{ color:#0ea5e9; font-weight:700; margin:0 12px; }}
button {{ background:linear-gradient(135deg,#0ea5e9,#8b5cf6); color:#fff; border:none;
    padding:10px 28px; border-radius:8px; font-size:15px; cursor:pointer; display:block;
    margin:8px auto; font-weight:700; }}
button:hover {{ opacity:0.9; }}
</style></head><body>
<div class="info">Adim: <span id="steps">0</span> Karsilastirma: <span id="comps">0</span></div>
<canvas id="cv" width="700" height="300"></canvas>
<button id="btn">Baslat</button>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
const N=40, DELAY={delay}, ALGO='{algo}';
let arr=[],colors=[],steps=0,comps=0,running=false;
function init(){{ arr=[];colors=[];for(let i=0;i<N;i++){{ arr.push(Math.floor(Math.random()*280)+10); colors.push('#0ea5e9'); }} steps=0;comps=0;update(); draw(); }}
function update(){{ document.getElementById('steps').textContent=steps; document.getElementById('comps').textContent=comps; }}
function draw(){{ ctx.clearRect(0,0,700,300); const w=700/N-2; for(let i=0;i<N;i++){{ ctx.fillStyle=colors[i]; ctx.fillRect(i*(w+2),300-arr[i],w,arr[i]); }} }}
function sleep(ms){{ return new Promise(r=>setTimeout(r,ms)); }}
async function bubbleSort(){{ for(let i=0;i<N-1;i++){{ for(let j=0;j<N-i-1;j++){{ colors[j]='#ef4444';colors[j+1]='#ef4444';comps++;draw();update();await sleep(DELAY); if(arr[j]>arr[j+1]){{ [arr[j],arr[j+1]]=[arr[j+1],arr[j]];steps++; }} colors[j]='#0ea5e9';colors[j+1]='#0ea5e9';draw(); }} colors[N-i-1]='#10b981';draw(); }} colors[0]='#10b981';draw();update(); }}
async function selectionSort(){{ for(let i=0;i<N-1;i++){{ let mi=i;colors[i]='#eab308'; for(let j=i+1;j<N;j++){{ colors[j]='#ef4444';comps++;draw();update();await sleep(DELAY); if(arr[j]<arr[mi]) mi=j; colors[j]='#0ea5e9'; }} if(mi!==i){{ [arr[i],arr[mi]]=[arr[mi],arr[i]];steps++; }} colors[i]='#10b981';draw();update(); }} colors[N-1]='#10b981';draw();update(); }}
async function insertionSort(){{ colors[0]='#10b981';draw(); for(let i=1;i<N;i++){{ let key=arr[i],j=i-1;colors[i]='#eab308';draw();await sleep(DELAY); while(j>=0&&arr[j]>key){{ comps++;colors[j]='#ef4444';draw();await sleep(DELAY); arr[j+1]=arr[j];j--;steps++;colors[j+1]='#0ea5e9'; }} arr[j+1]=key;steps++;colors[i]='#10b981';draw();update(); }} for(let i=0;i<N;i++) colors[i]='#10b981';draw();update(); }}
async function quickSort(lo=0,hi=N-1){{ if(lo>=hi){{ if(lo>=0&&lo<N) colors[lo]='#10b981';draw();return; }} let pivot=arr[hi],idx=lo;colors[hi]='#eab308';draw(); for(let j=lo;j<hi;j++){{ colors[j]='#ef4444';comps++;draw();update();await sleep(DELAY); if(arr[j]<pivot){{ [arr[idx],arr[j]]=[arr[j],arr[idx]];steps++;idx++; }} colors[j]='#0ea5e9'; }} [arr[idx],arr[hi]]=[arr[hi],arr[idx]];steps++;colors[idx]='#10b981';colors[hi]='#0ea5e9';draw();update(); await quickSort(lo,idx-1);await quickSort(idx+1,hi); }}
document.getElementById('btn').onclick=async function(){{ if(running) return; running=true;this.textContent='Calisiyor...';init(); if(ALGO==='Bubble Sort') await bubbleSort(); else if(ALGO==='Selection Sort') await selectionSort(); else if(ALGO==='Insertion Sort') await insertionSort(); else await quickSort(); for(let i=0;i<N;i++) colors[i]='#10b981';draw();update();this.textContent='Tekrar Baslat';running=false; }};
init();
</script></body></html>"""
        components.html(sort_html, height=420)

    # ---- Sub-tab B: Arama ----
    with sub[1]:
        st.markdown("#### Arama Algoritmalari Gorsellestirmesi")

        c1, c2 = st.columns([1, 1])
        with c1:
            search_algo = st.selectbox("Algoritma", ["Linear Search", "Binary Search"], key="search_algo")
        with c2:
            target = st.number_input("Hedef Sayi (1-100)", min_value=1, max_value=100, value=42, key="search_target")

        if search_algo == "Linear Search":
            st.info("**Linear Search:** O(n) - Diziyi bastan sona tek tek tarar. Sirasiz dizilerde kullanilir.")
        else:
            st.info("**Binary Search:** O(log n) - Sirali dizide ortadan bolerek arar. Cok hizlidir.")

        search_html = f"""<!DOCTYPE html><html><head><style>
* {{ margin:0;padding:0;box-sizing:border-box; }}
body {{ background:#0f172a;font-family:Arial,sans-serif;overflow:hidden; }}
canvas {{ display:block;margin:10px auto; }}
.info {{ color:#94a3b8;text-align:center;font-size:14px;padding:6px; }}
.info span {{ color:#0ea5e9;font-weight:700;margin:0 10px; }}
.ptrs {{ color:#eab308;text-align:center;font-size:13px;padding:4px; }}
button {{ background:linear-gradient(135deg,#0ea5e9,#8b5cf6);color:#fff;border:none;
    padding:10px 28px;border-radius:8px;font-size:15px;cursor:pointer;display:block;
    margin:6px auto;font-weight:700; }}
</style></head><body>
<div class="info">Adim: <span id="steps">0</span> Durum: <span id="status">Hazir</span></div>
<div class="ptrs" id="ptrs"></div>
<canvas id="cv" width="700" height="200"></canvas>
<button id="btn">Ara</button>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
const ALGO='{search_algo}',TARGET={int(target)};
let arr=[],colors=[],steps=0;
const N=25;
function init(){{ arr=[];colors=[];let s=new Set();while(s.size<N) s.add(Math.floor(Math.random()*100)+1); arr=Array.from(s).sort((a,b)=>a-b);for(let i=0;i<N;i++) colors.push('#0ea5e9');draw(); }}
function draw(){{ ctx.clearRect(0,0,700,200);const w=700/N-4; for(let i=0;i<N;i++){{ ctx.fillStyle=colors[i];ctx.fillRect(i*(w+4)+2,40,w,100);ctx.fillStyle='#e2e8f0';ctx.font='bold 12px Arial';ctx.textAlign='center';ctx.fillText(arr[i],i*(w+4)+2+w/2,100); }} }}
function sleep(ms){{ return new Promise(r=>setTimeout(r,ms)); }}
async function linearSearch(){{ for(let i=0;i<N;i++){{ colors[i]='#ef4444';steps++;document.getElementById('steps').textContent=steps;document.getElementById('status').textContent='Araniyor: '+arr[i];draw();await sleep(200); if(arr[i]===TARGET){{ colors[i]='#10b981';draw();document.getElementById('status').textContent='BULUNDU! Index: '+i;return; }} colors[i]='#64748b'; }} document.getElementById('status').textContent='Bulunamadi!';draw(); }}
async function binarySearch(){{ let lo=0,hi=N-1; document.getElementById('ptrs').textContent=''; while(lo<=hi){{ let mid=Math.floor((lo+hi)/2);for(let i=0;i<N;i++) colors[i]=(i>=lo&&i<=hi)?'#0ea5e9':'#64748b'; colors[mid]='#ef4444';steps++;document.getElementById('steps').textContent=steps; document.getElementById('ptrs').textContent='Sol: '+lo+' | Orta: '+mid+' | Sag: '+hi; document.getElementById('status').textContent='Kontrol: '+arr[mid];draw();await sleep(500); if(arr[mid]===TARGET){{ colors[mid]='#10b981';draw();document.getElementById('status').textContent='BULUNDU! Index: '+mid;return; }} else if(arr[mid]<TARGET) lo=mid+1; else hi=mid-1; }} document.getElementById('status').textContent='Bulunamadi!';for(let i=0;i<N;i++) colors[i]='#64748b';draw(); }}
document.getElementById('btn').onclick=async function(){{ this.disabled=true;this.textContent='Araniyor...';steps=0;init(); if(ALGO==='Linear Search') await linearSearch(); else await binarySearch(); this.textContent='Tekrar Ara';this.disabled=false; }};
init();
</script></body></html>"""
        components.html(search_html, height=310)

    # ---- Sub-tab C: Veri Yapilari ----
    with sub[2]:
        st.markdown("#### Veri Yapilari Gorsellestirmesi")

        ds_html = """<!DOCTYPE html><html><head><style>
* { margin:0;padding:0;box-sizing:border-box; }
body { background:#0f172a;font-family:Arial,sans-serif;color:#e2e8f0; }
.container { display:flex;gap:12px;padding:10px; }
.panel { flex:1;background:#1e293b;border-radius:12px;padding:12px;border:1px solid #334155; }
.panel h3 { color:#8b5cf6;font-size:14px;margin-bottom:8px;text-align:center; }
canvas { display:block;margin:0 auto 8px; background:#0f172a;border-radius:8px; }
.btns { text-align:center; }
.btns button { background:linear-gradient(135deg,#8b5cf6,#6366f1);color:#fff;border:none;
    padding:6px 14px;border-radius:6px;font-size:12px;cursor:pointer;margin:3px;font-weight:600; }
.btns button:hover { opacity:0.85; }
.btns input { background:#0f172a;border:1px solid #334155;color:#e2e8f0;padding:5px 8px;
    border-radius:6px;width:60px;font-size:12px;text-align:center; }
</style></head><body>
<div class="container">
<!-- STACK -->
<div class="panel">
<h3>Stack (Yigin)</h3>
<canvas id="sc" width="180" height="220"></canvas>
<div class="btns"><input id="sv" type="number" value="5" min="1" max="99"/>
<button onclick="sPush()">Ekle (Push)</button><button onclick="sPop()">Cikar (Pop)</button></div>
</div>
<!-- QUEUE -->
<div class="panel">
<h3>Queue (Kuyruk)</h3>
<canvas id="qc" width="180" height="220"></canvas>
<div class="btns"><input id="qv" type="number" value="5" min="1" max="99"/>
<button onclick="qEnq()">Ekle (Enqueue)</button><button onclick="qDeq()">Cikar (Dequeue)</button></div>
</div>
<!-- TREE -->
<div class="panel">
<h3>Binary Tree (Agac)</h3>
<canvas id="tc" width="220" height="220"></canvas>
<div class="btns"><input id="tv" type="number" value="5" min="1" max="99"/>
<button onclick="tAdd()">Ekle</button><button onclick="tRem()">Cikar</button></div>
</div>
</div>
<script>
// Stack
let stack=[];const scv=document.getElementById('sc'),sctx=scv.getContext('2d');
function drawStack(){sctx.clearRect(0,0,180,220);const h=30,max=6;for(let i=0;i<stack.length&&i<max;i++){const y=220-(i+1)*h-5;sctx.fillStyle=i===stack.length-1?'#10b981':'#0ea5e9';sctx.fillRect(20,y,140,h-4);sctx.fillStyle='#0f172a';sctx.font='bold 14px Arial';sctx.textAlign='center';sctx.fillText(stack[i],90,y+20);}sctx.strokeStyle='#334155';sctx.strokeRect(18,5,144,215);}
function sPush(){let v=parseInt(document.getElementById('sv').value)||0;if(stack.length<6){stack.push(v);drawStack();}}
function sPop(){if(stack.length>0){stack.pop();drawStack();}}
drawStack();
// Queue
let queue=[];const qcv=document.getElementById('qc'),qctx=qcv.getContext('2d');
function drawQueue(){qctx.clearRect(0,0,180,220);const h=30,max=6;for(let i=0;i<queue.length&&i<max;i++){const y=5+i*h;qctx.fillStyle=i===0?'#eab308':'#8b5cf6';qctx.fillRect(20,y,140,h-4);qctx.fillStyle='#0f172a';qctx.font='bold 14px Arial';qctx.textAlign='center';qctx.fillText(queue[i],90,y+20);}qctx.strokeStyle='#334155';qctx.strokeRect(18,3,144,215);qctx.fillStyle='#64748b';qctx.font='11px Arial';qctx.textAlign='left';qctx.fillText('On (Cikar)',22,220);qctx.textAlign='right';qctx.fillText('Arka (Ekle)',160,220);}
function qEnq(){let v=parseInt(document.getElementById('qv').value)||0;if(queue.length<6){queue.push(v);drawQueue();}}
function qDeq(){if(queue.length>0){queue.shift();drawQueue();}}
drawQueue();
// Tree
let treeRoot=null;
function TN(v){return{v:v,l:null,r:null};}
function tIns(node,v){if(!node) return TN(v);if(v<node.v) node.l=tIns(node.l,v);else if(v>node.v) node.r=tIns(node.r,v);return node;}
function tMin(node){while(node.l) node=node.l;return node;}
function tDel(node,v){if(!node) return null;if(v<node.v) node.l=tDel(node.l,v);else if(v>node.v) node.r=tDel(node.r,v);else{if(!node.l) return node.r;if(!node.r) return node.l;let m=tMin(node.r);node.v=m.v;node.r=tDel(node.r,m.v);}return node;}
const tcv=document.getElementById('tc'),tctx=tcv.getContext('2d');
function drawTree(){tctx.clearRect(0,0,220,220);if(treeRoot) drawNode(treeRoot,110,25,50,1);}
function drawNode(n,x,y,off,dep){if(!n) return;if(n.l){tctx.strokeStyle='#334155';tctx.beginPath();tctx.moveTo(x,y);tctx.lineTo(x-off,y+40);tctx.stroke();drawNode(n.l,x-off,y+40,off/1.8,dep+1);}if(n.r){tctx.strokeStyle='#334155';tctx.beginPath();tctx.moveTo(x,y);tctx.lineTo(x+off,y+40);tctx.stroke();drawNode(n.r,x+off,y+40,off/1.8,dep+1);}tctx.fillStyle='#8b5cf6';tctx.beginPath();tctx.arc(x,y,15,0,Math.PI*2);tctx.fill();tctx.fillStyle='#fff';tctx.font='bold 11px Arial';tctx.textAlign='center';tctx.textBaseline='middle';tctx.fillText(n.v,x,y);}
function tAdd(){let v=parseInt(document.getElementById('tv').value)||0;treeRoot=tIns(treeRoot,v);drawTree();}
function tRem(){let v=parseInt(document.getElementById('tv').value)||0;treeRoot=tDel(treeRoot,v);drawTree();}
drawTree();
</script></body></html>"""
        components.html(ds_html, height=320)

    # ---- Sub-tab D: Labirent ----
    with sub[3]:
        st.markdown("#### Labirent Cozucu")

        maze_algo = st.selectbox("Algoritma", ["BFS (Genislik Oncelikli)", "DFS (Derinlik Oncelikli)"], key="maze_algo")
        algo_key = "bfs" if "BFS" in maze_algo else "dfs"

        if "BFS" in maze_algo:
            st.info("**BFS:** En kisa yolu garanti eder. Katman katman ilerler.")
        else:
            st.info("**DFS:** Bir yolu sonuna kadar dener, cikmaza girince geri doner. En kisa yolu garanti etmez.")

        maze_html = f"""<!DOCTYPE html><html><head><style>
* {{ margin:0;padding:0;box-sizing:border-box; }}
body {{ background:#0f172a;font-family:Arial,sans-serif;overflow:hidden; }}
canvas {{ display:block;margin:10px auto; }}
.info {{ color:#94a3b8;text-align:center;font-size:14px;padding:6px; }}
.info span {{ color:#0ea5e9;font-weight:700;margin:0 10px; }}
button {{ background:linear-gradient(135deg,#0ea5e9,#8b5cf6);color:#fff;border:none;
    padding:10px 28px;border-radius:8px;font-size:15px;cursor:pointer;display:block;
    margin:6px auto;font-weight:700; }}
</style></head><body>
<div class="info">Adim: <span id="ms">0</span> Durum: <span id="mst">Hazir</span></div>
<canvas id="mc" width="450" height="450"></canvas>
<button id="mbtn">Coz</button>
<script>
const S=15,CS=30,cv=document.getElementById('mc'),ctx=cv.getContext('2d');
const ALGO='{algo_key}';
let grid=[],visited=[],path=[];
// maze generation (recursive backtracker)
function initMaze(){{
  grid=[];visited=[];path=[];
  for(let r=0;r<S;r++){{ grid[r]=[];visited[r]=[];for(let c=0;c<S;c++){{ grid[r][c]=1;visited[r][c]=false; }} }}
  // carve
  function carve(r,c){{ grid[r][c]=0;const dirs=[[0,2],[0,-2],[2,0],[-2,0]].sort(()=>Math.random()-0.5);
    for(const[dr,dc] of dirs){{ const nr=r+dr,nc=c+dc;if(nr>=0&&nr<S&&nc>=0&&nc<S&&grid[nr][nc]===1){{ grid[r+dr/2][c+dc/2]=0;carve(nr,nc); }} }} }}
  carve(1,1);grid[1][1]=0;grid[S-2][S-2]=0;
}}
function draw(){{ ctx.clearRect(0,0,450,450);for(let r=0;r<S;r++) for(let c=0;c<S;c++){{ if(grid[r][c]===1) ctx.fillStyle='#ef4444'; else if(visited[r][c]) ctx.fillStyle='#065f46'; else ctx.fillStyle='#1e293b'; ctx.fillRect(c*CS,r*CS,CS-1,CS-1); }}
  for(const[r,c] of path){{ ctx.fillStyle='#eab308';ctx.fillRect(c*CS,r*CS,CS-1,CS-1); }}
  // start/end
  ctx.fillStyle='#10b981';ctx.fillRect(1*CS,1*CS,CS-1,CS-1);
  ctx.fillStyle='#8b5cf6';ctx.fillRect((S-2)*CS,(S-2)*CS,CS-1,CS-1);
}}
function sleep(ms){{ return new Promise(r=>setTimeout(r,ms)); }}
async function solveBFS(){{
  let q=[[1,1,[]]];visited[1][1]=true;let steps=0;
  while(q.length){{ const[r,c,p]=q.shift();steps++;document.getElementById('ms').textContent=steps;
    if(r===S-2&&c===S-2){{ path=p.concat([[r,c]]);draw();document.getElementById('mst').textContent='Cozuldu! Yol: '+path.length+' adim';return; }}
    for(const[dr,dc] of [[0,1],[0,-1],[1,0],[-1,0]]){{ const nr=r+dr,nc=c+dc;if(nr>=0&&nr<S&&nc>=0&&nc<S&&!visited[nr][nc]&&grid[nr][nc]===0){{ visited[nr][nc]=true;q.push([nr,nc,p.concat([[r,c]])]); }} }}
    if(steps%3===0){{ draw();await sleep(20); }} }}
  document.getElementById('mst').textContent='Yol bulunamadi!';draw();
}}
async function solveDFS(){{
  let st=[[1,1,[]]];let steps=0;
  while(st.length){{ const[r,c,p]=st.pop();if(visited[r][c]) continue;visited[r][c]=true;steps++;document.getElementById('ms').textContent=steps;
    if(r===S-2&&c===S-2){{ path=p.concat([[r,c]]);draw();document.getElementById('mst').textContent='Cozuldu! Yol: '+path.length+' adim';return; }}
    for(const[dr,dc] of [[0,1],[0,-1],[1,0],[-1,0]]){{ const nr=r+dr,nc=c+dc;if(nr>=0&&nr<S&&nc>=0&&nc<S&&!visited[nr][nc]&&grid[nr][nc]===0){{ st.push([nr,nc,p.concat([[r,c]])]); }} }}
    if(steps%3===0){{ draw();await sleep(20); }} }}
  document.getElementById('mst').textContent='Yol bulunamadi!';draw();
}}
initMaze();draw();
document.getElementById('mbtn').onclick=async function(){{ this.disabled=true;this.textContent='Cozuluyor...';initMaze();draw();await sleep(300); if(ALGO==='bfs') await solveBFS(); else await solveDFS(); this.textContent='Yeni Labirent & Coz';this.disabled=false; }};
</script></body></html>"""
        components.html(maze_html, height=530)


# ---------------------------------------------------------------------------
# FEATURE 1: Bilim Simulasyon Studyosu
# ---------------------------------------------------------------------------

_BILIM_DENEYLER = {
    "Bitki Buyumesi ve Isik": {
        "aciklama": "Isik miktarinin bitki buyumesine etkisini inceleyin.",
        "bagimsiz": "Isik suresi (saat/gun)",
        "bagimli": "Bitki boyu (cm)",
        "kontrol": "Su miktari, toprak turu, sicaklik",
        "birim_bag": "saat/gun",
        "birim_dep": "cm",
        "slider_min": 2, "slider_max": 16, "slider_step": 2,
        "formul_label": "Boy = 1.8 * isik_suresi + 3 + rastgele(-0.5, 0.5)",
    },
    "Sicaklik ve Cozunme": {
        "aciklama": "Su sicakliginin seker cozunme suresine etkisini inceleyin.",
        "bagimsiz": "Su sicakligi (C)",
        "bagimli": "Cozunme suresi (sn)",
        "kontrol": "Seker miktari, karistirma hizi, su hacmi",
        "birim_bag": "C",
        "birim_dep": "sn",
        "slider_min": 20, "slider_max": 100, "slider_step": 10,
        "formul_label": "Sure = 300 / (sicaklik * 0.15 + 1)",
    },
    "Egik Duzlem ve Surtunme": {
        "aciklama": "Egik duzlem acisinin cisim kayma hizina etkisini inceleyin.",
        "bagimsiz": "Egim acisi (derece)",
        "bagimli": "Kayma hizi (m/s)",
        "kontrol": "Cisim kutlesi, yuzey turu, mesafe",
        "birim_bag": "derece",
        "birim_dep": "m/s",
        "slider_min": 5, "slider_max": 60, "slider_step": 5,
        "formul_label": "Hiz = sqrt(2 * 9.81 * sin(aci) * 1.0)",
    },
    "Sarkac Periyodu": {
        "aciklama": "Sarkac ip uzunlugunun sallanma periyoduna etkisini inceleyin.",
        "bagimsiz": "Ip uzunlugu (cm)",
        "bagimli": "Periyot (sn)",
        "kontrol": "Kutle, baslangic acisi (kucuk), hava direnci",
        "birim_bag": "cm",
        "birim_dep": "sn",
        "slider_min": 10, "slider_max": 200, "slider_step": 10,
        "formul_label": "T = 2 * pi * sqrt(L / g)",
    },
    "Miknatais ve Mesafe": {
        "aciklama": "Mesafenin miknatislanma cekim kuvvetine etkisini inceleyin.",
        "bagimsiz": "Mesafe (cm)",
        "bagimli": "Cekim kuvveti (N)",
        "kontrol": "Miknatis gucu, cisim malzemesi",
        "birim_bag": "cm",
        "birim_dep": "N",
        "slider_min": 1, "slider_max": 10, "slider_step": 1,
        "formul_label": "F = 50 / mesafe^2",
    },
}


def _bilim_hesapla(deney_adi: str, deger: float, olcum_no: int) -> float:
    """Deney formulune gore sonuc hesapla. olcum_no ile kucuk varyasyon ekler."""
    import random
    rng = random.Random(int(deger * 1000) + olcum_no * 7)
    varyasyon = rng.uniform(-0.3, 0.3)

    if deney_adi == "Bitki Buyumesi ve Isik":
        return round(1.8 * deger + 3 + varyasyon, 2)
    elif deney_adi == "Sicaklik ve Cozunme":
        return round(300.0 / (deger * 0.15 + 1) + varyasyon * 5, 2)
    elif deney_adi == "Egik Duzlem ve Surtunme":
        rad = math.radians(deger)
        return round(math.sqrt(abs(2 * 9.81 * math.sin(rad) * 1.0)) + varyasyon * 0.2, 2)
    elif deney_adi == "Sarkac Periyodu":
        L = deger / 100.0
        return round(2 * math.pi * math.sqrt(L / 9.81) + varyasyon * 0.02, 3)
    elif deney_adi == "Miknatais ve Mesafe":
        return round(50.0 / (deger ** 2) + varyasyon * 0.1, 3)
    return 0.0


def _render_bilim_studyosu():
    """Bilim Simulasyon Studyosu - bilimsel yontem adimlari ile deney."""
    styled_section("Bilim Simulasyon Studyosu", "#0ea5e9")

    _render_html("""
    <div style="background:linear-gradient(135deg,#0c1222,#1e3a5f);border-radius:18px;padding:22px;
                 margin-bottom:18px;border:1px solid rgba(14,165,233,0.3);text-align:center">
        <div style="font-size:2.2rem;margin-bottom:6px">🔭🧪🔬</div>
        <h3 style="color:#7dd3fc !important;margin:0 0 6px !important;font-size:1.2rem">
            Bilim Simulasyon Studyosu</h3>
        <p style="color:#94a3b8 !important;font-size:0.82rem;margin:0 !important">
            Bilimsel yontemi 7 adimda uygula: Hipotez &rarr; Degisken &rarr; Deney &rarr; Veri &rarr; Grafik &rarr; Sonuc &rarr; Rapor
        </p>
    </div>
    """)

    deney_adlari = list(_BILIM_DENEYLER.keys())
    secili = st.selectbox("Deney Sec", deney_adlari, key="bv_studyo_deney")
    deney = _BILIM_DENEYLER[secili]

    _render_html(f"""
    <div class="bv-card">
        <div style="font-weight:700;color:#7dd3fc !important;font-size:0.95rem;margin-bottom:6px">
            {secili}</div>
        <div style="color:#94a3b8 !important;font-size:0.82rem">{deney['aciklama']}</div>
        <div style="color:#64748b !important;font-size:0.75rem;margin-top:6px">
            Formul: {deney['formul_label']}</div>
    </div>
    """)

    # Step state
    ss_key = "bv_studyo_step"
    if ss_key not in st.session_state:
        st.session_state[ss_key] = 1

    adim_labels = [
        "1. Hipotez Kur",
        "2. Degiskenleri Sec",
        "3. Deney Yap",
        "4. Veri Topla",
        "5. Grafik Ciz",
        "6. Sonuc Yaz",
        "7. Rapor",
    ]
    mevcut_adim = st.session_state[ss_key]

    # Progress bar
    ilerleme_pct = int((mevcut_adim / 7) * 100)
    _render_html(f"""
    <div style="margin-bottom:14px">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
            <span style="color:#7dd3fc !important;font-size:0.78rem;font-weight:600">
                Adim {mevcut_adim}/7: {adim_labels[mevcut_adim - 1]}</span>
            <span style="color:#64748b !important;font-size:0.75rem">%{ilerleme_pct}</span>
        </div>
        <div style="background:#1e293b;border-radius:8px;height:10px;overflow:hidden">
            <div style="background:linear-gradient(90deg,#0ea5e9,#38bdf8);width:{ilerleme_pct}%;
                         height:100%;border-radius:8px;transition:width 0.3s"></div>
        </div>
    </div>
    """)

    # ---------- STEP 1: Hipotez ----------
    if mevcut_adim >= 1:
        _render_html("""<div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem;
                        margin-bottom:6px">1. Hipotez Kur</div>""")
        hipotez = st.text_input(
            "Hipotezinizi yazin (ornek: Isik suresi arttikca bitki daha hizli buyur)",
            key="bv_studyo_hipotez",
        )

    # ---------- STEP 2: Degiskenler ----------
    if mevcut_adim >= 2:
        _render_html("""<div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem;
                        margin:12px 0 6px">2. Degiskenleri Sec</div>""")
        c1, c2, c3 = st.columns(3)
        with c1:
            bag_sec = st.selectbox("Bagimsiz Degisken", [deney["bagimsiz"]], key="bv_studyo_bagimsiz")
        with c2:
            dep_sec = st.selectbox("Bagimli Degisken", [deney["bagimli"]], key="bv_studyo_bagimli")
        with c3:
            kon_sec = st.selectbox("Kontrol Degiskenleri", [deney["kontrol"]], key="bv_studyo_kontrol")

    # ---------- STEP 3: Deney Yap ----------
    if mevcut_adim >= 3:
        _render_html("""<div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem;
                        margin:12px 0 6px">3. Deney Yap</div>""")
        slider_val = st.slider(
            f"{deney['bagimsiz']} degerini ayarla",
            min_value=deney["slider_min"],
            max_value=deney["slider_max"],
            step=deney["slider_step"],
            value=deney["slider_min"] + deney["slider_step"] * 2,
            key="bv_studyo_slider",
        )
        if st.button("Deneyi Calistir", key="bv_studyo_run"):
            st.session_state["bv_studyo_run_val"] = slider_val
            st.session_state["bv_studyo_data"] = []
            step_size = (deney["slider_max"] - deney["slider_min"]) / 4
            for i in range(5):
                x = deney["slider_min"] + step_size * i
                y = _bilim_hesapla(secili, x, i)
                st.session_state["bv_studyo_data"].append((round(x, 1), y))
            if mevcut_adim < 4:
                st.session_state[ss_key] = 4
                st.rerun()

    # ---------- STEP 4: Veri Topla ----------
    if mevcut_adim >= 4 and "bv_studyo_data" in st.session_state:
        _render_html("""<div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem;
                        margin:12px 0 6px">4. Veri Topla</div>""")
        data = st.session_state["bv_studyo_data"]
        rows_html = ""
        for idx, (x, y) in enumerate(data):
            bg = "rgba(14,165,233,0.08)" if idx % 2 == 0 else "transparent"
            rows_html += f"""<tr style="background:{bg}">
                <td style="padding:6px 12px;color:#cbd5e1 !important;border-bottom:1px solid #1e293b">{idx+1}</td>
                <td style="padding:6px 12px;color:#38bdf8 !important;border-bottom:1px solid #1e293b;font-weight:600">{x} {deney['birim_bag']}</td>
                <td style="padding:6px 12px;color:#10b981 !important;border-bottom:1px solid #1e293b;font-weight:600">{y} {deney['birim_dep']}</td>
            </tr>"""
        _render_html(f"""
        <div style="overflow-x:auto;margin-bottom:12px">
            <table style="width:100%;border-collapse:collapse;background:#0f172a;border-radius:12px;overflow:hidden">
                <thead><tr style="background:rgba(14,165,233,0.15)">
                    <th style="padding:8px 12px;color:#7dd3fc !important;font-size:0.8rem;text-align:left">Olcum</th>
                    <th style="padding:8px 12px;color:#7dd3fc !important;font-size:0.8rem;text-align:left">{deney['bagimsiz']}</th>
                    <th style="padding:8px 12px;color:#7dd3fc !important;font-size:0.8rem;text-align:left">{deney['bagimli']}</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """)

    # ---------- STEP 5: Grafik Ciz (CSS bars) ----------
    if mevcut_adim >= 5 and "bv_studyo_data" in st.session_state:
        _render_html("""<div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem;
                        margin:12px 0 6px">5. Grafik Ciz</div>""")
        data = st.session_state["bv_studyo_data"]
        max_y = max(d[1] for d in data) if data else 1
        bars_html = ""
        for idx, (x, y) in enumerate(data):
            pct = int((y / max_y) * 100) if max_y > 0 else 0
            bars_html += f"""
            <div style="display:flex;align-items:center;margin-bottom:6px">
                <div style="width:70px;color:#94a3b8 !important;font-size:0.75rem;text-align:right;
                             padding-right:8px">{x}</div>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden">
                    <div style="background:linear-gradient(90deg,#0ea5e9,#38bdf8);width:{pct}%;
                                 height:100%;border-radius:6px;transition:width 0.5s"></div>
                </div>
                <div style="width:60px;color:#10b981 !important;font-size:0.75rem;padding-left:8px;
                             font-weight:600">{y}</div>
            </div>"""
        _render_html(f"""
        <div style="background:#0f172a;border-radius:14px;padding:16px;border:1px solid #1e293b;
                     margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="color:#64748b !important;font-size:0.72rem">{deney['bagimsiz']}</span>
                <span style="color:#64748b !important;font-size:0.72rem">{deney['bagimli']}</span>
            </div>
            {bars_html}
        </div>
        """)

    # ---------- STEP 6: Sonuc Yaz ----------
    if mevcut_adim >= 6:
        _render_html("""<div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem;
                        margin:12px 0 6px">6. Sonuc Yaz</div>""")
        sonuc = st.text_area(
            "Deney sonuclarinizi yazin",
            placeholder="Ornek: Hipotezim dogrulandi. Isik suresi arttikca bitki boyu belirgin sekilde artti.",
            key="bv_studyo_sonuc",
            height=100,
        )

    # ---------- STEP 7: Rapor ----------
    if mevcut_adim >= 7:
        _render_html("""<div style="color:#38bdf8 !important;font-weight:700;font-size:0.9rem;
                        margin:12px 0 6px">7. Deney Raporu</div>""")
        hipotez_val = st.session_state.get("bv_studyo_hipotez", "-")
        sonuc_val = st.session_state.get("bv_studyo_sonuc", "-")
        data = st.session_state.get("bv_studyo_data", [])
        veri_ozet = ", ".join([f"{x}->{y}" for x, y in data]) if data else "-"
        _render_html(f"""
        <div style="background:linear-gradient(135deg,#0c1222,#1e3a5f);border-radius:18px;padding:22px;
                     border:2px solid rgba(14,165,233,0.3);margin-bottom:12px">
            <div style="text-align:center;margin-bottom:14px">
                <div style="font-size:1.8rem">📋</div>
                <div style="color:#7dd3fc !important;font-weight:800;font-size:1.1rem">DENEY RAPORU</div>
                <div style="color:#64748b !important;font-size:0.75rem">{datetime.now().strftime('%d.%m.%Y %H:%M')}</div>
            </div>
            <div style="border-top:1px solid rgba(14,165,233,0.2);padding-top:12px">
                <div style="margin-bottom:10px">
                    <div style="color:#38bdf8 !important;font-weight:700;font-size:0.8rem">Deney Adi</div>
                    <div style="color:#cbd5e1 !important;font-size:0.85rem">{secili}</div>
                </div>
                <div style="margin-bottom:10px">
                    <div style="color:#38bdf8 !important;font-weight:700;font-size:0.8rem">Hipotez</div>
                    <div style="color:#cbd5e1 !important;font-size:0.85rem">{hipotez_val}</div>
                </div>
                <div style="margin-bottom:10px">
                    <div style="color:#38bdf8 !important;font-weight:700;font-size:0.8rem">Degiskenler</div>
                    <div style="color:#cbd5e1 !important;font-size:0.82rem">
                        Bagimsiz: {deney['bagimsiz']} | Bagimli: {deney['bagimli']} | Kontrol: {deney['kontrol']}
                    </div>
                </div>
                <div style="margin-bottom:10px">
                    <div style="color:#38bdf8 !important;font-weight:700;font-size:0.8rem">Olcum Verileri</div>
                    <div style="color:#cbd5e1 !important;font-size:0.82rem">{veri_ozet}</div>
                </div>
                <div>
                    <div style="color:#38bdf8 !important;font-weight:700;font-size:0.8rem">Sonuc</div>
                    <div style="color:#cbd5e1 !important;font-size:0.85rem">{sonuc_val}</div>
                </div>
            </div>
        </div>
        """)
        st.success("Deney raporu basariyla olusturuldu!")

    # Navigation buttons
    st.markdown("---")
    nc1, nc2, nc3 = st.columns([1, 2, 1])
    with nc1:
        if mevcut_adim > 1:
            if st.button("Onceki Adim", key="bv_studyo_prev"):
                st.session_state[ss_key] = mevcut_adim - 1
                st.rerun()
    with nc3:
        if mevcut_adim < 7:
            if st.button("Sonraki Adim", key="bv_studyo_next"):
                st.session_state[ss_key] = mevcut_adim + 1
                st.rerun()
    with nc2:
        if st.button("Bastan Basla", key="bv_studyo_reset"):
            st.session_state[ss_key] = 1
            for k in list(st.session_state.keys()):
                if k.startswith("bv_studyo_") and k != ss_key:
                    del st.session_state[k]
            st.rerun()


# ---------------------------------------------------------------------------
# FEATURE 2: Proje Vitrini
# ---------------------------------------------------------------------------

_PROJE_KATEGORILER = ["Kodlama", "Bilim Deneyi", "Robotik", "Web Tasarim", "Yapay Zeka", "Oyun", "Mobil Uygulama"]
_PROJE_TEKNOLOJILER = ["Python", "JavaScript", "HTML/CSS", "Arduino", "Scratch", "Micro:bit"]
_PROJE_ZORLUK = ["Baslangic", "Orta", "Ileri"]

_DEMO_PROJELER = [
    {"ad": "Hava Durumu Botu", "kategori": "Kodlama", "teknoloji": ["Python"], "aciklama": "OpenWeatherMap API ile hava durumu sorgulayan terminal botu.", "zorluk": "Baslangic", "begeni": 12, "tarih": "2026-03-20"},
    {"ad": "Kedi Kopek Siniflandirici", "kategori": "Yapay Zeka", "teknoloji": ["Python"], "aciklama": "Transfer learning ile kedi/kopek resimlerini siniflandiran model.", "zorluk": "Ileri", "begeni": 25, "tarih": "2026-03-18"},
    {"ad": "Akilli Sera Sistemi", "kategori": "Robotik", "teknoloji": ["Arduino", "Python"], "aciklama": "Sicaklik ve nem sensoru ile otomatik sulama yapan sera projesi.", "zorluk": "Orta", "begeni": 18, "tarih": "2026-03-15"},
    {"ad": "Portfolyo Web Sitesi", "kategori": "Web Tasarim", "teknoloji": ["HTML/CSS", "JavaScript"], "aciklama": "Kisisel portfolyo web sitesi: animasyonlar, responsive tasarim.", "zorluk": "Baslangic", "begeni": 9, "tarih": "2026-03-22"},
    {"ad": "Yilan Oyunu", "kategori": "Oyun", "teknoloji": ["Python"], "aciklama": "Pygame ile klasik yilan oyunu, skor tablosu ve seviye sistemi.", "zorluk": "Orta", "begeni": 31, "tarih": "2026-03-10"},
    {"ad": "Scratch Labirent", "kategori": "Oyun", "teknoloji": ["Scratch"], "aciklama": "Scratch ile yapilmis labirent oyunu, 5 farkli seviye.", "zorluk": "Baslangic", "begeni": 7, "tarih": "2026-03-23"},
    {"ad": "Deprem Uyari Sistemi", "kategori": "Robotik", "teknoloji": ["Arduino", "Micro:bit"], "aciklama": "Titresim sensoru ile deprem algilayan ve uyari veren sistem.", "zorluk": "Ileri", "begeni": 22, "tarih": "2026-03-12"},
    {"ad": "Hesap Makinesi App", "kategori": "Mobil Uygulama", "teknoloji": ["JavaScript", "HTML/CSS"], "aciklama": "PWA olarak calisan bilimsel hesap makinesi uygulamasi.", "zorluk": "Orta", "begeni": 14, "tarih": "2026-03-19"},
]

_PROJE_FIKIRLERI = [
    # Baslangic (5)
    {"ad": "Dijital Saat", "aciklama": "HTML/CSS ile canli dijital saat tasarimi.", "teknoloji": "HTML/CSS", "sure": "2 saat", "zorluk": "Baslangic"},
    {"ad": "Kelime Tahmin Oyunu", "aciklama": "Python ile terminal bazli kelime tahmin oyunu.", "teknoloji": "Python", "sure": "3 saat", "zorluk": "Baslangic"},
    {"ad": "Scratch Animasyon", "aciklama": "Scratch ile kisa bir animasyon hikayesi.", "teknoloji": "Scratch", "sure": "2 saat", "zorluk": "Baslangic"},
    {"ad": "Renk Paleti Olusturucu", "aciklama": "Rastgele renk paleti ureten web uygulamasi.", "teknoloji": "JavaScript", "sure": "2 saat", "zorluk": "Baslangic"},
    {"ad": "LED Yanip Sonme", "aciklama": "Arduino ile LED yakip sondurme ve desen olusturma.", "teknoloji": "Arduino", "sure": "1 saat", "zorluk": "Baslangic"},
    # Orta (5)
    {"ad": "Todo Uygulamasi", "aciklama": "LocalStorage kullanan yapilacaklar listesi.", "teknoloji": "JavaScript", "sure": "4 saat", "zorluk": "Orta"},
    {"ad": "Sicaklik Logger", "aciklama": "Arduino ile sicaklik olcup grafik cizen sistem.", "teknoloji": "Arduino", "sure": "5 saat", "zorluk": "Orta"},
    {"ad": "Quiz Uygulamasi", "aciklama": "Python Flask ile web tabanli quiz uygulamasi.", "teknoloji": "Python", "sure": "6 saat", "zorluk": "Orta"},
    {"ad": "Pixel Art Editoru", "aciklama": "Canvas API ile piksel piksel cizim yapan editor.", "teknoloji": "JavaScript", "sure": "5 saat", "zorluk": "Orta"},
    {"ad": "Micro:bit Pusula", "aciklama": "Micro:bit manyetometre ile dijital pusula.", "teknoloji": "Micro:bit", "sure": "3 saat", "zorluk": "Orta"},
    # Ileri (5)
    {"ad": "Chatbot", "aciklama": "NLP kutuphanesi ile basit soru-cevap chatbotu.", "teknoloji": "Python", "sure": "8 saat", "zorluk": "Ileri"},
    {"ad": "Multiplayer Oyun", "aciklama": "WebSocket ile gercek zamanli cok oyunculu oyun.", "teknoloji": "JavaScript", "sure": "12 saat", "zorluk": "Ileri"},
    {"ad": "Otonom Robot", "aciklama": "Ultrasonik sensoru ile engelden kacan robot.", "teknoloji": "Arduino", "sure": "10 saat", "zorluk": "Ileri"},
    {"ad": "Goruntu Isleme", "aciklama": "OpenCV ile yuz tanima ve filtre uygulama.", "teknoloji": "Python", "sure": "8 saat", "zorluk": "Ileri"},
    {"ad": "E-Ticaret Sitesi", "aciklama": "Sepet, odeme ve urun yonetimi olan web sitesi.", "teknoloji": "JavaScript", "sure": "15 saat", "zorluk": "Ileri"},
]


def _render_proje_vitrini():
    """Proje Vitrini - proje paylasim ve sergileme platformu."""
    styled_section("Proje Vitrini", "#0ea5e9")

    _render_html("""
    <div style="background:linear-gradient(135deg,#0c1222,#1e3a5f);border-radius:18px;padding:22px;
                 margin-bottom:18px;border:1px solid rgba(14,165,233,0.3);text-align:center">
        <div style="font-size:2.2rem;margin-bottom:6px">🏅🚀💡</div>
        <h3 style="color:#7dd3fc !important;margin:0 0 6px !important;font-size:1.2rem">
            Proje Vitrini</h3>
        <p style="color:#94a3b8 !important;font-size:0.82rem;margin:0 !important">
            Projeni paylas, baskalarinin projelerini incele ve ilham al!
        </p>
    </div>
    """)

    # Initialize session state
    if "bv_vitrin_projeler" not in st.session_state:
        import copy
        st.session_state["bv_vitrin_projeler"] = copy.deepcopy(_DEMO_PROJELER)
    if "bv_vitrin_begeniler" not in st.session_state:
        st.session_state["bv_vitrin_begeniler"] = {}

    # ===================== PROJE PAYLAS =====================
    _render_html("""
    <div style="color:#38bdf8 !important;font-weight:800;font-size:1rem;margin-bottom:10px;
                 padding-bottom:6px;border-bottom:2px solid rgba(14,165,233,0.2)">
        Proje Paylas</div>
    """)

    with st.expander("Yeni Proje Ekle", expanded=False):
        p_ad = st.text_input("Proje Adi", key="bv_vitrin_ad", placeholder="Projene bir isim ver")
        pc1, pc2 = st.columns(2)
        with pc1:
            p_kat = st.selectbox("Kategori", _PROJE_KATEGORILER, key="bv_vitrin_kat")
        with pc2:
            p_zor = st.radio("Zorluk", _PROJE_ZORLUK, key="bv_vitrin_zor", horizontal=True)
        p_tek = st.multiselect("Kullanilan Teknoloji", _PROJE_TEKNOLOJILER, key="bv_vitrin_tek")
        p_ack = st.text_area("Aciklama", key="bv_vitrin_ack", placeholder="Projeni kisaca anlat...", height=100)

        if st.button("Projeyi Paylas", key="bv_vitrin_paylas"):
            if p_ad and p_ack and p_tek:
                yeni = {
                    "ad": p_ad,
                    "kategori": p_kat,
                    "teknoloji": p_tek,
                    "aciklama": p_ack,
                    "zorluk": p_zor,
                    "begeni": 0,
                    "tarih": datetime.now().strftime("%Y-%m-%d"),
                }
                st.session_state["bv_vitrin_projeler"].insert(0, yeni)
                st.success(f"'{p_ad}' projesi basariyla paylasild!")
                st.rerun()
            else:
                st.warning("Lutfen proje adi, en az bir teknoloji ve aciklama girin.")

    # ===================== HAFTANIN PROJESI =====================
    projeler = st.session_state["bv_vitrin_projeler"]
    if projeler:
        en_begenilen = max(projeler, key=lambda p: p.get("begeni", 0))
        if en_begenilen.get("begeni", 0) > 0:
            tek_tags = "".join([
                f'<span style="background:rgba(14,165,233,0.15);color:#38bdf8 !important;'
                f'padding:2px 8px;border-radius:10px;font-size:0.7rem;margin-right:4px">{t}</span>'
                for t in en_begenilen.get("teknoloji", [])
            ])
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#1a0f00,#3d2800);border-radius:18px;padding:22px;
                         margin:18px 0;border:2px solid rgba(255,193,7,0.4)">
                <div style="text-align:center;margin-bottom:10px">
                    <span style="font-size:1.5rem">🏆</span>
                    <span style="color:#ffc107 !important;font-weight:800;font-size:1rem;margin-left:6px">
                        Haftanin Projesi</span>
                </div>
                <div style="text-align:center">
                    <div style="color:#ffd54f !important;font-weight:700;font-size:1.1rem;margin-bottom:6px">
                        {en_begenilen['ad']}</div>
                    <div style="margin-bottom:6px">{tek_tags}</div>
                    <div style="color:#bbb !important;font-size:0.82rem;margin-bottom:6px">
                        {en_begenilen['aciklama']}</div>
                    <div style="color:#ffc107 !important;font-size:0.85rem;font-weight:600">
                        {en_begenilen.get('begeni', 0)} begeni</div>
                </div>
            </div>
            """)

    # ===================== VITRIN =====================
    _render_html("""
    <div style="color:#38bdf8 !important;font-weight:800;font-size:1rem;margin:16px 0 10px;
                 padding-bottom:6px;border-bottom:2px solid rgba(14,165,233,0.2)">
        Vitrin</div>
    """)

    fc1, fc2 = st.columns(2)
    with fc1:
        filtre_kat = st.selectbox("Kategoriye Gore Filtrele", ["Tumu"] + _PROJE_KATEGORILER,
                                   key="bv_vitrin_filtre_kat")
    with fc2:
        siralama = st.selectbox("Siralama", ["En Yeni", "En Begenilen"], key="bv_vitrin_siralama")

    gosterilecek = list(projeler)
    if filtre_kat != "Tumu":
        gosterilecek = [p for p in gosterilecek if p.get("kategori") == filtre_kat]
    if siralama == "En Begenilen":
        gosterilecek.sort(key=lambda p: p.get("begeni", 0), reverse=True)
    else:
        gosterilecek.sort(key=lambda p: p.get("tarih", ""), reverse=True)

    if not gosterilecek:
        st.info("Bu kategoride henuz proje yok.")
    else:
        for row_i in range(0, len(gosterilecek), 2):
            cols = st.columns(2)
            for col_i in range(2):
                idx = row_i + col_i
                if idx >= len(gosterilecek):
                    break
                proje = gosterilecek[idx]
                with cols[col_i]:
                    zorluk_renk = {"Baslangic": "#10b981", "Orta": "#f59e0b", "Ileri": "#ef4444"}.get(
                        proje.get("zorluk", "Orta"), "#64748b")
                    kat_emoji = {"Kodlama": "💻", "Bilim Deneyi": "🔬", "Robotik": "🤖",
                                  "Web Tasarim": "🌐", "Yapay Zeka": "🧠", "Oyun": "🎮",
                                  "Mobil Uygulama": "📱"}.get(proje.get("kategori", ""), "📦")
                    tek_html = "".join([
                        f'<span style="background:rgba(14,165,233,0.12);color:#38bdf8 !important;'
                        f'padding:1px 7px;border-radius:8px;font-size:0.68rem;margin-right:3px">{t}</span>'
                        for t in proje.get("teknoloji", [])
                    ])
                    aciklama_kisa = proje.get("aciklama", "")[:100]
                    _render_html(f"""
                    <div class="bv-card" style="min-height:180px">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                            <div style="color:#e0f2fe !important;font-weight:700;font-size:0.9rem">
                                {kat_emoji} {proje['ad']}</div>
                            <span style="background:{zorluk_renk}22;color:{zorluk_renk} !important;
                                          padding:2px 8px;border-radius:8px;font-size:0.68rem;font-weight:600">
                                {proje.get('zorluk', '')}</span>
                        </div>
                        <div style="margin-bottom:6px">{tek_html}</div>
                        <div style="color:#94a3b8 !important;font-size:0.8rem;margin-bottom:8px;
                                     line-height:1.4">{aciklama_kisa}</div>
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <span style="color:#64748b !important;font-size:0.7rem">{proje.get('tarih', '')}</span>
                            <span style="color:#f59e0b !important;font-size:0.78rem;font-weight:600">
                                {proje.get('begeni', 0)} begeni</span>
                        </div>
                    </div>
                    """)
                    # Like button - find actual index in main list
                    proje_key = f"bv_vitrin_like_{proje['ad']}_{proje.get('tarih','')}"
                    if st.button(f"Harika! ({proje.get('begeni', 0)})", key=proje_key):
                        if proje_key not in st.session_state.get("bv_vitrin_begeniler", {}):
                            # Find and update in main list
                            for p in st.session_state["bv_vitrin_projeler"]:
                                if p["ad"] == proje["ad"] and p.get("tarih") == proje.get("tarih"):
                                    p["begeni"] = p.get("begeni", 0) + 1
                                    break
                            st.session_state["bv_vitrin_begeniler"][proje_key] = True
                            st.rerun()

    # ===================== PROJE FIKIRLERI =====================
    _render_html("""
    <div style="color:#38bdf8 !important;font-weight:800;font-size:1rem;margin:20px 0 10px;
                 padding-bottom:6px;border-bottom:2px solid rgba(14,165,233,0.2)">
        Proje Fikirleri</div>
    """)

    fikir_filtre = st.selectbox("Zorluk Seviyesi", ["Tumu", "Baslangic", "Orta", "Ileri"],
                                 key="bv_vitrin_fikir_filtre")

    fikirler = _PROJE_FIKIRLERI
    if fikir_filtre != "Tumu":
        fikirler = [f for f in fikirler if f["zorluk"] == fikir_filtre]

    for row_i in range(0, len(fikirler), 3):
        cols = st.columns(3)
        for col_i in range(3):
            idx = row_i + col_i
            if idx >= len(fikirler):
                break
            fikir = fikirler[idx]
            with cols[col_i]:
                z_renk = {"Baslangic": "#10b981", "Orta": "#f59e0b", "Ileri": "#ef4444"}.get(
                    fikir["zorluk"], "#64748b")
                _render_html(f"""
                <div class="bv-card" style="min-height:140px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                        <div style="color:#e0f2fe !important;font-weight:700;font-size:0.85rem">{fikir['ad']}</div>
                        <span style="background:{z_renk}22;color:{z_renk} !important;
                                      padding:1px 7px;border-radius:8px;font-size:0.65rem;font-weight:600">
                            {fikir['zorluk']}</span>
                    </div>
                    <div style="color:#94a3b8 !important;font-size:0.78rem;margin-bottom:6px;line-height:1.4">
                        {fikir['aciklama']}</div>
                    <div style="display:flex;justify-content:space-between">
                        <span style="color:#38bdf8 !important;font-size:0.7rem">{fikir['teknoloji']}</span>
                        <span style="color:#64748b !important;font-size:0.7rem">{fikir['sure']}</span>
                    </div>
                </div>
                """)
