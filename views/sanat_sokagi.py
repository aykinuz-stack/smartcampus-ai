"""
Sanat Sokağı (Art Street) — Streamlit UI
==========================================
Çocukların sanat yeteneğini keşfedip geliştiren kapsamlı sanat modülü.
"""
from __future__ import annotations
import random
import streamlit as st
from datetime import datetime

from utils.ui_common import inject_common_css, styled_header, styled_section, _render_html
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("steam_merkezi")
except Exception:
    pass
from models.sanat_sokagi import (
    get_store, SanatDataStore,
    UNLU_RESSAMLAR, SANAT_AKIMLARI, RENKLER,
    ORIGAMI_PROJELERI, SANAT_SOZLUGU, SANAT_FESTIVALI,
    get_gunluk_sanat_ipucu,
)


def render_sanat_sokagi():
    """Ana giriş noktası."""
    inject_common_css("snt")
    styled_header("Sanat Sokağı (Art Street)", "🎨")
    # XP bar gecici olarak devre disi
    # from utils.gamification_ui import render_xp_bar
    # render_xp_bar()

    store = get_store()

    # Sanat Sokağı özel CSS
    _render_html("""
    <style>
    .snt-hero {
        background: linear-gradient(135deg, #1a0a2e 0%, #4c1d95 40%, #7c3aed 70%, #a78bfa 100%);
        border-radius: 24px; padding: 32px; margin-bottom: 24px;
        border: 2px solid rgba(167,139,250,0.4);
        text-align: center; position: relative; overflow: hidden;
    }
    .snt-hero::before {
        content: '🎨🎵✍️🎭✂️📸'; position: absolute; bottom: 8px; right: 16px;
        font-size: 1.5rem; opacity: 0.15; letter-spacing: 8px;
    }
    .snt-card {
        background: linear-gradient(145deg, #1a0a2e, #2d1b69);
        border-radius: 18px; padding: 22px; margin-bottom: 14px;
        border: 1px solid rgba(167,139,250,0.2);
        transition: all 0.3s ease;
    }
    .snt-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(139,92,246,0.2); }
    .snt-gallery-item {
        background: #0f172a; border-radius: 14px; padding: 14px;
        border: 1px solid rgba(99,102,241,0.1);
        text-align: center; min-height: 180px;
        transition: all 0.2s;
    }
    .snt-gallery-item:hover { border-color: #6366f1; }
    </style>
    """)

    # Sayfa secimi — session_state ile, sadece 1 sayfa render edilir
    _PAGES = [
        "Sanat Meydani", "Boyama", "Ebru", "Renk", "Desen",
        "Muzik", "Nostalji", "Besteci", "Yazarlik", "Kompozisyon",
        "Muze", "El Sanatlari", "Sinema", "Mimari", "Dans",
        "Dunya Sanatlari", "Kaligrafi", "Tiyatro", "Fotograf",
        "Animasyon", "Heykel", "Renk Testi", "Analiz",
        "Gunluk", "Festival", "Ilerleme", "Yetenek",
        "Degerlendirme", "Yarisma", "Ogrenci Raporu",
        "Smarti",
    ]
    cur = st.session_state.get("_snt_page", "Sanat Meydani")
    if cur not in _PAGES:
        cur = "Sanat Meydani"

    # Navigasyon — 3 satir buton
    for r in range(0, len(_PAGES), 9):
        chunk = _PAGES[r:r+9]
        cc = st.columns(len(chunk))
        for i, pg in enumerate(chunk):
            with cc[i]:
                if st.button(pg, key=f"_sn_{pg}", type="primary" if pg == cur else "secondary", use_container_width=True):
                    st.session_state["_snt_page"] = pg
                    st.rerun()

    # Sadece secili sayfayi render et (1 iframe)
    if cur == "Sanat Meydani": _render_meydan(store)
    elif cur == "Boyama": _render_boyama(store)
    elif cur == "Ebru": _render_ebru_sanati()
    elif cur == "Renk": _render_renk_dunyasi()
    elif cur == "Desen": _render_desen_fabrikasi()
    elif cur == "Muzik": _render_muzik()
    elif cur == "Nostalji": _render_nostalji_kosesi()
    elif cur == "Besteci": _render_muzik_bestecisi()
    elif cur == "Yazarlik": _render_yazarlik()
    elif cur == "Kompozisyon": _render_kompozisyon()
    elif cur == "Muze": _render_muze()
    elif cur == "El Sanatlari": _render_el_sanatlari()
    elif cur == "Sinema": _render_sinema()
    elif cur == "Mimari": _render_mimari()
    elif cur == "Dans": _render_dans()
    elif cur == "Dunya Sanatlari": _render_dunya_sanatlari()
    elif cur == "Kaligrafi": _render_kaligrafi()
    elif cur == "Tiyatro": _render_tiyatro()
    elif cur == "Fotograf": _render_fotograf_studyosu()
    elif cur == "Animasyon": _render_animasyon_studyosu()
    elif cur == "Heykel": _render_heykel_studyosu()
    elif cur == "Renk Testi": _render_renk_algi_testi()
    elif cur == "Analiz": _render_sanat_analizi()
    elif cur == "Gunluk": _render_sanat_gunlugu(store)
    elif cur == "Festival": _render_sanat_festivali()
    elif cur == "Ilerleme": _render_ilerleme_rapor(store)
    elif cur == "Yetenek": _render_yetenek_testi()
    elif cur == "Degerlendirme": _render_cizim_degerlendirme()
    elif cur == "Yarisma": _render_sanat_yarismasi()
    elif cur == "Ogrenci Raporu":
        from views.modul_rapor_ui import render_ogretmen_rapor
        render_ogretmen_rapor(modul_filter="sanat", key_prefix="mr_snt")
    elif cur == "Smarti":
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="sanat_sokagi")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_sanat_sokagi")
            if st.button("Gönder", key="smarti_send_sanat_sokagi"):
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
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. sanat_sokagi modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")


# ═══════════════════════════════════════════════════════════════
# 1) SANAT MEYDANI
# ═══════════════════════════════════════════════════════════════

def _render_meydan(store: SanatDataStore):
    styled_section("🏠 Sanat Meydanı", "#8b5cf6")

    _render_html("""
    <div class="snt-hero">
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:10px" class="mat-grow">🎨✨</div>
            <h2 style="color:#e9d5ff !important;font-size:1.6rem;margin:0 0 8px !important">Sanat Sokağı'na Hoş Geldin!</h2>
            <p style="color:#c4b5fd !important;font-size:0.9rem;margin:0 !important">
                Boyama, müzik, yazarlık, origami, fotoğraf — sanatın her dalını keşfet!
            </p>
        </div>
    </div>
    """)

    # Günlük ipucu
    ipucu = get_gunluk_sanat_ipucu()
    _render_html(f"""
    <div style="background:linear-gradient(135deg,#f59e0b15,#f59e0b08);border-radius:14px;padding:14px 18px;
                 margin-bottom:16px;border:1px solid rgba(245,158,11,0.3)">
        <div style="font-weight:700;color:#fde68a !important;font-size:0.9rem">💡 Günün Sanat İpucu</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">{ipucu}</div>
    </div>
    """)

    # Sanat dalları grid
    dallar = [
        ("🎨", "Boyama", "Dijital fırça ile çiz!", "#ef4444"),
        ("🌈", "Renkler", "Renk çarkını keşfet!", "#f59e0b"),
        ("📐", "Desenler", "Simetrik motifler oluştur!", "#10b981"),
        ("🎵", "Müzik", "Piyano çal, ritim tut!", "#3b82f6"),
        ("✍️", "Yazarlık", "Şiir yaz, hikaye anlat!", "#8b5cf6"),
        ("✂️", "El Sanatları", "Origami, kolaj, seramik!", "#ec4899"),
    ]
    cols = st.columns(6)
    for col, (ikon, ad, aciklama, renk) in zip(cols, dallar):
        with col:
            _render_html(f"""
            <div class="snt-gallery-item" style="border-left:3px solid {renk}">
                <div style="font-size:2.5rem;margin-bottom:6px">{ikon}</div>
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</div>
                <div style="font-size:0.7rem;color:#94a3b8 !important;margin-top:4px">{aciklama}</div>
            </div>
            """)

    # Rastgele ressam
    st.markdown("---")
    styled_section("🖼️ Bugünün Ressamı", "#ec4899")
    import random as _r
    ressam = _r.choice(UNLU_RESSAMLAR)
    img_html = f'<img src="{ressam["portre_url"]}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #8b5cf6" onerror="this.style.display=\'none\'">' if ressam.get("portre_url") else f'<div style="font-size:3rem">{ressam["ikon"]}</div>'
    _render_html(f"""
    <div class="snt-card" style="display:flex;gap:20px;align-items:center">
        <div style="min-width:80px;text-align:center">{img_html}</div>
        <div>
            <div style="font-weight:700;color:#e9d5ff !important;font-size:1.1rem">{ressam['ad']}</div>
            <div style="font-size:0.8rem;color:#c084fc !important">{ressam['akım']} • {ressam['yasam']} • {ressam['ulke']}</div>
            <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:4px">🖼️ {ressam['eser']}</div>
            <div style="font-size:0.8rem;color:#a5b4fc !important;margin-top:4px;font-style:italic">{ressam['bilgi']}</div>
        </div>
    </div>
    """)


# ═══════════════════════════════════════════════════════════════
# 2) BOYAMA ATÖLYESİ
# ═══════════════════════════════════════════════════════════════

def _render_boyama(store: SanatDataStore):
    styled_section("🎨 Boyama Atölyesi — 6 Teknik", "#ef4444")
    import streamlit.components.v1 as components

    boyama_html = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
#BA{max-width:860px;margin:0 auto;font-family:'Segoe UI',sans-serif;user-select:none}
/* TUVAL ÇERÇEVESİ — gerçek ahşap */
#BFR{background:linear-gradient(180deg,#5d4037,#4e342e,#3e2723);border-radius:10px;padding:18px;position:relative;
box-shadow:0 12px 40px rgba(0,0,0,.6),inset 0 2px 4px rgba(255,255,255,.06),inset 0 -2px 4px rgba(0,0,0,.3);
border:1px solid #2e1b0e}
#BFR::before{content:'';position:absolute;inset:0;border-radius:10px;
background:repeating-linear-gradient(90deg,transparent,transparent 22px,rgba(0,0,0,.02) 22px,rgba(0,0,0,.02) 23px);pointer-events:none}
/* İç passepartout */
#BPP{background:#0f172a;padding:4px;border-radius:3px;box-shadow:inset 0 2px 8px rgba(0,0,0,.35)}
#BCV{display:block;width:100%;border-radius:2px;cursor:none;background:#1e293b}
/* TEKNİK ÇUBUĞU */
#BTR{display:flex;gap:0;margin-top:10px;border-radius:10px;overflow:hidden;
background:#1a1a2e;border:1px solid #16213e}
.btab{flex:1;padding:8px 4px;text-align:center;cursor:pointer;font-size:.62rem;font-weight:700;
color:#546e8a;border:none;background:transparent;transition:all .2s;letter-spacing:.3px;
border-right:1px solid rgba(22,33,62,.5)}
.btab:last-child{border-right:none}
.btab:hover{background:rgba(233,69,96,.1);color:#e94560}
.btab.on{background:linear-gradient(180deg,#e94560,#c62a40);color:#fff;
box-shadow:0 2px 12px rgba(233,69,96,.3)}
.btab-icon{display:block;font-size:1.1rem;margin-bottom:2px}
/* ARAÇ KUTUSU */
#BAR{display:flex;gap:6px;align-items:center;justify-content:center;margin-top:8px;
padding:8px 14px;background:linear-gradient(180deg,#263238,#1e272e);border-radius:8px;
border:1px solid #37474f;flex-wrap:wrap}
.abtn{padding:5px 12px;border-radius:6px;border:1px solid #455a64;
background:linear-gradient(180deg,#37474f,#263238);color:#90a4ae;cursor:pointer;
font-size:.68rem;font-weight:600;transition:all .15s}
.abtn:hover{background:linear-gradient(180deg,#455a64,#37474f);color:#cfd8dc;transform:translateY(-1px)}
.abtn.on{background:linear-gradient(180deg,#e94560,#c62a40);color:#fff;border-color:#e94560}
.abtn-save{padding:6px 16px;border-radius:6px;border:2px solid #ffc107;
background:linear-gradient(180deg,#ffc107,#ff9800);color:#1a1a2e;cursor:pointer;
font-size:.72rem;font-weight:800;box-shadow:0 3px 10px rgba(255,193,7,.4);letter-spacing:.5px}
.abtn-save:hover{background:linear-gradient(180deg,#ffd54f,#ffc107);transform:translateY(-1px)}
#BSZ{width:90px;accent-color:#e94560;vertical-align:middle}
.alab{color:#546e8a;font-size:.6rem;font-weight:600}
#BST{text-align:center;margin-top:6px;font-size:.7rem;color:#78909c;font-style:italic}
/* RENK PALETİ — gerçek boya paleti */
#BPL{display:flex;align-items:center;justify-content:center;gap:6px;margin-top:8px;
padding:10px 16px;position:relative;
background:radial-gradient(ellipse at 50% 50%,#d7ccc8,#bcaaa4,#a1887f);
border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;border:2px solid #8d6e63;
box-shadow:0 4px 12px rgba(0,0,0,.3),inset 0 2px 4px rgba(255,255,255,.2)}
#BPL::before{content:'';position:absolute;width:28px;height:28px;border-radius:50%;
background:radial-gradient(circle,#efebe9,#d7ccc8);border:2px solid #a1887f;
right:12px;top:50%;transform:translateY(-50%);box-shadow:inset 0 2px 4px rgba(0,0,0,.15)}
.pdot{width:26px;height:26px;border-radius:50%;cursor:pointer;border:2px solid rgba(0,0,0,.2);
transition:all .15s;position:relative;
box-shadow:0 2px 4px rgba(0,0,0,.3),inset 0 -3px 6px rgba(0,0,0,.15),inset 0 2px 3px rgba(255,255,255,.2)}
.pdot:hover{transform:scale(1.2);z-index:2}
.pdot.on{border-color:#ffd700;box-shadow:0 0 10px rgba(255,215,0,.5),0 2px 4px rgba(0,0,0,.3);transform:scale(1.25);z-index:2}
/* Aktif renk göstergesi */
#BAC{display:flex;align-items:center;gap:6px;justify-content:center;margin-top:6px}
#BAC-box{width:36px;height:36px;border-radius:8px;border:2px solid #455a64;
box-shadow:0 2px 6px rgba(0,0,0,.3),inset 0 -4px 8px rgba(0,0,0,.15)}
#BAC-name{font-size:.7rem;color:#90a4ae;font-weight:600}
/* 3D İMLEÇ */
#BCUR{position:fixed;pointer-events:none;z-index:99999;display:none;transition:none}
</style>

<div id="BA">
<div id="BFR">
<div id="BPP"><canvas id="BCV" width="780" height="480"></canvas></div>
</div>
<div id="BTR">
<button class="btab on" data-t="kuruboya"><span class="btab-icon">&#9997;</span>Kuru Boya</button>
<button class="btab" data-t="pastel"><span class="btab-icon">&#127912;</span>Pastel</button>
<button class="btab" data-t="suluboya"><span class="btab-icon">&#128167;</span>Suluboya</button>
<button class="btab" data-t="yagliboya"><span class="btab-icon">&#127912;</span>Yagliboya</button>
<button class="btab" data-t="karakalem"><span class="btab-icon">&#9999;</span>Karakalem</button>
<button class="btab" data-t="serbest"><span class="btab-icon">&#127752;</span>Serbest</button>
</div>
<div id="BPL"></div>
<div id="BAC"><div id="BAC-box"></div><span id="BAC-name">Kirmizi</span></div>
<div id="BAR">
<span class="alab">Boyut:</span><input type="range" id="BSZ" min="1" max="50" value="8">
<button class="abtn on" data-a="draw">Ciz</button>
<button class="abtn" data-a="eraser">Silgi</button>
<button class="abtn" data-a="blend">Karistir</button>
<span class="alab">|</span>
<button class="abtn" onclick="BUn()">Geri Al</button>
<button class="abtn" onclick="BCl()">Temizle</button>
<span class="alab">|</span>
<button class="abtn-save" id="BSAV">KAYDET (PNG)</button>
</div>
<div id="BST">Kuru Boya Kalemi secili. Renk sec, tuvale ciz!</div>
</div>
<div id="BCUR"></div>

<script>
(function(){
var cv=document.getElementById('BCV'),X=cv.getContext('2d');
var ST=document.getElementById('BST'),SZ=document.getElementById('BSZ');
var cur=document.getElementById('BCUR');
var acBox=document.getElementById('BAC-box'),acName=document.getElementById('BAC-name');
var tech='kuruboya',atl='draw',col='#e74c3c',colN='Kirmizi';
var drag=false,lx=0,ly=0,hist=[],pressure=1,lastTime=0;

var PALS={
kuruboya:[['#e74c3c','Kirmizi'],['#e67e22','Turuncu'],['#f1c40f','Sari'],['#27ae60','Yesil'],['#2980b9','Mavi'],
['#1a237e','Lacivert'],['#8e44ad','Mor'],['#e91e63','Pembe'],['#795548','Kahve'],['#d4a017','Oksit'],['#212121','Siyah'],['#ecf0f1','Beyaz']],
pastel:[['#f8a5a5','Gul'],['#f7c59f','Seftali'],['#ffe6a7','Limon'],['#b5ead7','Nane'],['#a0c4ff','Buz'],
['#c3b1e1','Lavanta'],['#ffc8dd','Sakura'],['#fde4cf','Krem'],['#cdb4db','Leylak'],['#bde0fe','Gok'],['#e8d5b7','Kum'],['#f0e6ef','Inci']],
suluboya:[['#c0392b','Kizil'],['#e67e22','Turuncu'],['#f39c12','Safran'],['#27ae60','Zumrut'],['#2980b9','Kobalt'],
['#8e44ad','Ametist'],['#e91e63','Magenta'],['#1abc9c','Deniz'],['#d35400','Bakir'],['#2c3e50','Gece'],['#16a085','Okyanus'],['#f1c40f','Altin']],
yagliboya:[['#b71c1c','Kadmiyum K.'],['#e65100','Turuncu'],['#f9a825','Sari Ok.'],['#1b5e20','Zeytin'],['#0d47a1','Ultramarin'],
['#4a148c','Dioxazine'],['#880e4f','Alizarin'],['#004d40','Viridian'],['#bf360c','Sienna'],['#263238','Paynes G.'],['#ff6f00','Kadm. Sar.'],['#fafafa','Titan Bey.']],
karakalem:[['#0a0a0a','8B'],['#1a1a1a','6B'],['#333','4B'],['#4d4d4d','2B'],['#666','B'],['#808080','HB'],['#999','H'],['#b3b3b3','2H'],['#ccc','4H']],
serbest:[['#e74c3c','Kirmizi'],['#e67e22','Turuncu'],['#f1c40f','Sari'],['#2ecc71','Yesil'],['#3498db','Mavi'],
['#8e44ad','Mor'],['#e91e63','Pembe'],['#1abc9c','Turkuaz'],['#795548','Kahve'],['#212121','Siyah'],['#f39c12','Altin'],['#ecf0f1','Beyaz']]};

function h2r(h){return{r:parseInt(h.slice(1,3),16),g:parseInt(h.slice(3,5),16),b:parseInt(h.slice(5,7),16)}}

// Kağıt dokusu
function drawPaper(){
var bgs={kuruboya:'#fefefe',pastel:'#f5f0e8',suluboya:'#fefce8',yagliboya:'#fef9ef',karakalem:'#fefefe',serbest:'#fefefe'};
X.fillStyle=bgs[tech];X.fillRect(0,0,cv.width,cv.height);
// Kağıt dokusu — gerçekçi lif + pürüz
X.globalAlpha=.025;
for(var i=0;i<500;i++){
var fx=Math.random()*cv.width,fy=Math.random()*cv.height;
X.beginPath();X.moveTo(fx,fy);X.lineTo(fx+Math.random()*5-2.5,fy+Math.random()*3-1.5);
X.strokeStyle=Math.random()>.5?'#c8b890':'#a09070';X.lineWidth=.2+Math.random()*.3;X.stroke()}
// Tuval ise doku farklı
if(tech==='yagliboya'){
X.globalAlpha=.04;
for(var y=0;y<cv.height;y+=3){for(var x=0;x<cv.width;x+=3){
if(Math.random()<.3){X.fillStyle=Math.random()>.5?'#d8d0c0':'#e8e0d0';
X.fillRect(x,y,2,2)}}}}
if(tech==='suluboya'){
X.globalAlpha=.02;
for(var y=0;y<cv.height;y+=8){X.beginPath();X.moveTo(0,y);
for(var x=0;x<cv.width;x+=4)X.lineTo(x,y+Math.sin(x*.02)*1.5);
X.strokeStyle='#d0c8b0';X.lineWidth=.3;X.stroke()}}
X.globalAlpha=1}

// Palet
function buildPal(){
var pl=document.getElementById('BPL');pl.innerHTML='';
var cs=PALS[tech]||PALS.serbest;
cs.forEach(function(c,i){
var d=document.createElement('div');d.className='pdot'+(i===0?' on':'');
d.style.background=c[0];d.title=c[1];
d.onclick=function(){document.querySelectorAll('.pdot').forEach(function(x){x.classList.remove('on')});
d.classList.add('on');col=c[0];colN=c[1];acBox.style.background=col;acName.textContent=c[1];
atl='draw';document.querySelectorAll('.abtn[data-a]').forEach(function(x){x.classList.remove('on')});
document.querySelector('.abtn[data-a="draw"]').classList.add('on');
updCur();ST.textContent=c[1]+' secildi'};
pl.appendChild(d)});
col=cs[0][0];colN=cs[0][1];acBox.style.background=col;acName.textContent=colN;
// Başparmak deliği (palet)
var hole=document.createElement('div');
hole.style.cssText='width:0;height:0;flex-shrink:0'; // placeholder for ::before
pl.appendChild(hole)}

// 3D İMLEÇ
function updCur(){
var sz=+SZ.value;var s='position:fixed;pointer-events:none;z-index:99999;';
if(atl==='eraser'){
s+='width:'+(sz+14)+'px;height:'+(sz+8)+'px;border-radius:3px;'+
'background:linear-gradient(180deg,#475569,#334155,#1e293b);'+
'border:1.5px solid #64748b;box-shadow:2px 3px 8px rgba(0,0,0,.5),inset 0 1px 2px rgba(100,116,139,.4),inset 0 -2px 3px rgba(0,0,0,.2);'
}else if(atl==='blend'){
s+='width:'+(sz+10)+'px;height:'+(sz+10)+'px;border-radius:50%;'+
'background:radial-gradient(circle at 40% 35%,#fce4ec,#f8bbd0,#f48fb1);'+
'border:1px solid #ec407a;box-shadow:2px 3px 8px rgba(0,0,0,.3);'
}else if(tech==='kuruboya'){
var w=Math.max(7,sz*.5);
s+='width:'+w+'px;height:'+(sz*3.5+25)+'px;border-radius:1px 1px 0 0;overflow:hidden;'+
'background:linear-gradient(180deg,'+col+' 0%,'+col+' 75%,#333 92%,#222 100%);'+
'border:1px solid rgba(0,0,0,.25);'+
'box-shadow:3px 4px 10px rgba(0,0,0,.4),inset -2px 0 3px rgba(0,0,0,.15),inset 2px 0 3px rgba(255,255,255,.12);'+
'transform:rotate(-32deg);transform-origin:bottom center;';
}else if(tech==='pastel'){
var w=sz*1.1+12;
s+='width:'+w+'px;height:'+(sz*1.8+22)+'px;border-radius:5px 5px 10px 10px;'+
'background:linear-gradient(90deg,rgba(0,0,0,.08) 0%,transparent 15%,rgba(255,255,255,.2) 40%,transparent 85%,rgba(0,0,0,.06) 100%);'+
'background-color:'+col+';border:1px solid rgba(0,0,0,.12);'+
'box-shadow:3px 4px 12px rgba(0,0,0,.3),inset 0 -6px 12px rgba(0,0,0,.1),inset 0 2px 4px rgba(255,255,255,.15);'+
'transform:rotate(-20deg);transform-origin:bottom center;';
}else if(tech==='suluboya'){
s+='width:7px;height:'+(sz*3+40)+'px;border-radius:2px 2px 50% 50%;'+
'background:linear-gradient(180deg,#c9a96e 0%,#b8860b 8%,#a67c00 12%,#c9a96e 60%,#deb887 65%,'+col+' 80%,'+col+' 100%);'+
'border:1px solid rgba(0,0,0,.2);'+
'box-shadow:2px 3px 8px rgba(0,0,0,.35),inset -1px 0 2px rgba(0,0,0,.1),inset 1px 0 2px rgba(255,255,255,.1);'+
'transform:rotate(-35deg);transform-origin:bottom center;';
}else if(tech==='yagliboya'){
s+='width:'+(sz+16)+'px;height:'+(sz*1.8+22)+'px;border-radius:2px 2px 4px 4px;'+
'background:linear-gradient(180deg,#6d4c41 0%,#5d4037 35%,#795548 40%,'+col+' 65%,'+col+' 100%);'+
'border:1px solid rgba(0,0,0,.2);'+
'box-shadow:3px 4px 12px rgba(0,0,0,.35);transform:rotate(-18deg);';
}else if(tech==='karakalem'){
s+='width:6px;height:'+(sz*4+40)+'px;border-radius:1px;'+
'background:linear-gradient(180deg,#f5deb3 0%,#deb887 5%,#f5deb3 8%,#faebd7 50%,#deb887 55%,#8B8B00 58%,#333 90%,#1a1a1a 100%);'+
'border:1px solid rgba(0,0,0,.15);'+
'box-shadow:2px 3px 8px rgba(0,0,0,.35),inset -1px 0 1px rgba(0,0,0,.1);'+
'transform:rotate(-30deg);transform-origin:bottom center;';
}else{
s+='width:'+Math.max(6,sz*.5)+'px;height:'+(sz*2.5+20)+'px;border-radius:3px;'+
'background:'+col+';border:1px solid rgba(0,0,0,.2);box-shadow:2px 3px 8px rgba(0,0,0,.35);'+
'transform:rotate(-28deg);';}
cur.style.cssText=s+'display:none;'}

// ÇİZİM — teknik bazlı gerçekçi fırça
// STAMP TABANLI FIRÇA MOTORU — Procreate/Photoshop kalitesi
// Her teknik için path üzerinde stamp basarak çizim
function paint(x1,y1,x2,y2){
var sz=+SZ.value;
var dx=x2-x1,dy=y2-y1;
var dist=Math.sqrt(dx*dx+dy*dy);
var angle=Math.atan2(dy,dx);
var spd=dist;
var prs=Math.min(1,Math.max(.15,1-spd*.012));

if(atl==='eraser'){
X.save();X.globalCompositeOperation='destination-out';
var steps=Math.max(1,Math.floor(dist/2));
for(var i=0;i<=steps;i++){var t=i/steps;
var px=x1+dx*t,py=y1+dy*t;
X.globalAlpha=.9;X.beginPath();X.arc(px,py,sz*.7+4,0,6.28);X.fill()}
X.restore();return}

if(atl==='blend'){
try{var r=Math.round(sz+8);
var steps=Math.max(1,Math.floor(dist/3));
for(var i=0;i<=steps;i++){var t=i/steps;
var px=x1+dx*t,py=y1+dy*t;
var ix=Math.max(0,Math.round(px-r)),iy=Math.max(0,Math.round(py-r));
var iw=Math.min(cv.width-ix,r*2),ih=Math.min(cv.height-iy,r*2);
if(iw>0&&ih>0){var img=X.getImageData(ix,iy,iw,ih);
X.globalAlpha=.35;X.putImageData(img,Math.round(ix+dx*.15),Math.round(iy+dy*.15));X.globalAlpha=1}}
}catch(e){}return}

var rgb=h2r(col);
var R=rgb.r,G=rgb.g,B=rgb.b;

if(tech==='kuruboya'){
// KURU BOYA — stamp: küçük elips, kağıt pürüzünden geçen kalem izi
// Spacing: her 1.5px bir stamp
var spacing=Math.max(1,sz*.15);
var steps=Math.max(1,Math.floor(dist/spacing));
for(var i=0;i<=steps;i++){
var t=i/steps;
var px=x1+dx*t,py=y1+dy*t;
// Ana pigment stamp — küçük elipsler
for(var j=0;j<3;j++){
var jx=px+(Math.random()-.5)*sz*.6;
var jy=py+(Math.random()-.5)*sz*.6;
var jr=sz*.15+Math.random()*sz*.2;
// Kağıt pürüzü: bazı noktalar boş kalır
if(Math.random()<.7){
X.globalAlpha=(.15+Math.random()*.25)*prs;
X.fillStyle=col;
X.beginPath();X.ellipse(jx,jy,jr,jr*.6,angle+Math.random()*.5,0,6.28);X.fill()}}
// Koyu tanecik
if(Math.random()<.3){
X.globalAlpha=.08*prs;X.fillStyle='rgba('+Math.max(0,R-40)+','+Math.max(0,G-40)+','+Math.max(0,B-40)+',1)';
X.beginPath();X.arc(px+(Math.random()-.5)*sz*.4,py+(Math.random()-.5)*sz*.4,.3+Math.random()*.5,0,6.28);X.fill()}
}
}else if(tech==='pastel'){
// PASTEL — stamp: geniş, yumuşak daire, toz serpintili
// Pastelin kenarı düzensiz, kağıda toz bırakır
var spacing=Math.max(1,sz*.12);
var steps=Math.max(1,Math.floor(dist/spacing));
for(var i=0;i<=steps;i++){
var t=i/steps;
var px=x1+dx*t+(Math.random()-.5)*2;
var py=y1+dy*t+(Math.random()-.5)*2;
// Ana yumuşak stamp
var sr=sz*.5+Math.random()*sz*.3;
var g=X.createRadialGradient(px,py,0,px,py,sr);
g.addColorStop(0,'rgba('+R+','+G+','+B+','+((.2+Math.random()*.15)*prs)+')');
g.addColorStop(.6,'rgba('+R+','+G+','+B+','+((.08+Math.random()*.06)*prs)+')');
g.addColorStop(1,'rgba('+R+','+G+','+B+',0)');
X.fillStyle=g;X.fillRect(px-sr,py-sr,sr*2,sr*2);
// Toz parçacıkları — pastel etrafa toz bırakır
for(var j=0;j<3;j++){
if(Math.random()<.4){
X.globalAlpha=.04*prs;X.fillStyle=col;
X.beginPath();X.arc(px+(Math.random()-.5)*sz*2,py+(Math.random()-.5)*sz*2,.2+Math.random()*.8,0,6.28);X.fill()}}
}
}else if(tech==='suluboya'){
// SULUBOYA — stamp: çok şeffaf büyük daire, ıslak yayılma, pigment toplanma
X.save();X.globalCompositeOperation='multiply';
var spacing=Math.max(2,sz*.25);
var steps=Math.max(1,Math.floor(dist/spacing));
for(var i=0;i<=steps;i++){
var t=i/steps;
var px=x1+dx*t+(Math.random()-.5)*sz*.2;
var py=y1+dy*t+(Math.random()-.5)*sz*.2;
// Dış su hale — çok geniş, çok şeffaf
var outerR=sz*1.2+Math.random()*sz*.4;
var og=X.createRadialGradient(px,py,0,px,py,outerR);
og.addColorStop(0,'rgba('+R+','+G+','+B+','+((.04+Math.random()*.02)*prs)+')');
og.addColorStop(.5,'rgba('+R+','+G+','+B+','+((.02)*prs)+')');
og.addColorStop(1,'rgba('+R+','+G+','+B+',0)');
X.fillStyle=og;X.fillRect(px-outerR,py-outerR,outerR*2,outerR*2);
// İç pigment — yoğun merkez
var innerR=sz*.4;
var ig=X.createRadialGradient(px,py,0,px,py,innerR);
ig.addColorStop(0,'rgba('+R+','+G+','+B+','+((.08+Math.random()*.04)*prs)+')');
ig.addColorStop(1,'rgba('+R+','+G+','+B+',0)');
X.fillStyle=ig;X.fillRect(px-innerR,py-innerR,innerR*2,innerR*2);
}
// Kenar pigment birikimi — suluboya kenarında renk toplanır
if(dist>5&&Math.random()<.15){
X.globalAlpha=.03;X.strokeStyle=col;X.lineWidth=sz*.1;X.lineCap='round';
X.beginPath();X.arc(x2,y2,sz*.6+Math.random()*sz*.3,0,6.28);X.stroke()}
// Su damlacığı
if(Math.random()<.05){
var bx=x2+(Math.random()-.5)*sz*2,by=y2+(Math.random()-.5)*sz*2;
var br=1+Math.random()*3;
var bg=X.createRadialGradient(bx,by,0,bx,by,br);
bg.addColorStop(0,'rgba('+R+','+G+','+B+','+(Math.random()*.04)+')');
bg.addColorStop(1,'rgba('+R+','+G+','+B+',0)');
X.fillStyle=bg;X.fillRect(bx-br,by-br,br*2,br*2)}
X.restore();
}else if(tech==='yagliboya'){
// YAGLIBOYA — stamp: kalın opak dikdörtgen, spatula izleri, kabartma
var spacing=Math.max(1,sz*.18);
var steps=Math.max(1,Math.floor(dist/spacing));
var perpX=-Math.sin(angle),perpY=Math.cos(angle);
for(var i=0;i<=steps;i++){
var t=i/steps;
var px=x1+dx*t,py=y1+dy*t;
// Kalın opak boya yığını
X.save();X.translate(px,py);X.rotate(angle);
var w=sz*.7,h=sz*1.2;
// Ana boya — opak
X.globalAlpha=(.5+Math.random()*.3)*prs;
X.fillStyle=col;
X.fillRect(-w/2,-h/2,w,h);
// Işık kenarı — kabartma
X.globalAlpha=.1;X.fillStyle='rgba(255,255,255,.4)';
X.fillRect(-w/2,-h/2,w,2);X.fillRect(-w/2,-h/2,2,h);
// Gölge kenarı
X.fillStyle='rgba(0,0,0,.15)';
X.fillRect(-w/2,h/2-2,w,2);X.fillRect(w/2-2,-h/2,2,h);
// Spatula çizikleri
X.globalAlpha=.06;
for(var j=0;j<3;j++){var sy=-h/2+Math.random()*h;
X.fillStyle=j%2?'rgba(255,255,255,.2)':'rgba(0,0,0,.1)';
X.fillRect(-w/2,sy,w,.5+Math.random())}
X.restore();
}
}else if(tech==='karakalem'){
// KARAKALEM — stamp: ince noktalar, basınç hassas, kağıt tanesi görünür
var spacing=Math.max(.5,sz*.08);
var steps=Math.max(1,Math.floor(dist/spacing));
for(var i=0;i<=steps;i++){
var t=i/steps;
var px=x1+dx*t,py=y1+dy*t;
// Grafit stamp — çok küçük noktalar, bazıları boş (kağıt pürüzü)
for(var j=0;j<2;j++){
var jx=px+(Math.random()-.5)*sz*.5;
var jy=py+(Math.random()-.5)*sz*.5;
// Kağıt pürüzü: %30 boş
if(Math.random()<.7*prs){
X.globalAlpha=(.2+Math.random()*.35)*prs;
X.fillStyle=col;
var gr=.3+Math.random()*sz*.12;
X.beginPath();X.arc(jx,jy,gr,0,6.28);X.fill()}}
// Çapraz tarama doku
if(Math.random()<.08*prs){
X.globalAlpha=.04;X.strokeStyle=col;X.lineWidth=.3;
X.beginPath();X.moveTo(px-2,py-2);X.lineTo(px+2,py+2);X.stroke()}
}
}else{
// SERBEST — stamp tabanlı pürüzsüz
var spacing=Math.max(1,sz*.15);
var steps=Math.max(1,Math.floor(dist/spacing));
for(var i=0;i<=steps;i++){
var t=i/steps;
var px=x1+dx*t,py=y1+dy*t;
var sr=sz*.5;
var g=X.createRadialGradient(px,py,0,px,py,sr);
g.addColorStop(0,'rgba('+R+','+G+','+B+','+((.5+Math.random()*.2)*prs)+')');
g.addColorStop(.7,'rgba('+R+','+G+','+B+','+((.15)*prs)+')');
g.addColorStop(1,'rgba('+R+','+G+','+B+',0)');
X.fillStyle=g;X.fillRect(px-sr,py-sr,sr*2,sr*2)}}
X.globalAlpha=1}

// Teknik değiştir
document.querySelectorAll('.btab').forEach(function(b){b.onclick=function(){
tech=b.dataset.t;
document.querySelectorAll('.btab').forEach(function(x){x.classList.remove('on')});b.classList.add('on');
buildPal();drawPaper();hist=[];atl='draw';
document.querySelectorAll('.abtn[data-a]').forEach(function(x){x.classList.remove('on')});
document.querySelector('.abtn[data-a="draw"]').classList.add('on');
updCur();
var desc={kuruboya:'Kuru Boya Kalemi',pastel:'Pastel Boya',suluboya:'Suluboya Fircasi',
yagliboya:'Yagliboya + Spatula',karakalem:'Karakalem (Kursun)',serbest:'Serbest Cizim'};
ST.textContent=desc[tech]+' secildi'}});

// Araç butonları
document.querySelectorAll('.abtn[data-a]').forEach(function(b){b.onclick=function(){
atl=b.dataset.a;
document.querySelectorAll('.abtn[data-a]').forEach(function(x){x.classList.remove('on')});
b.classList.add('on');updCur()}});
SZ.addEventListener('input',updCur);

// Mouse
function gp(e){var r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(cv.width/r.width),y:(e.clientY-r.top)*(cv.height/r.height)}}
function tp(e){var t=e.touches[0],r=cv.getBoundingClientRect();return{x:(t.clientX-r.left)*(cv.width/r.width),y:(t.clientY-r.top)*(cv.height/r.height)}}
cv.addEventListener('mouseenter',function(){cur.style.display='block'});
cv.addEventListener('mouseleave',function(){cur.style.display='none';drag=false});
cv.addEventListener('mousemove',function(e){cur.style.left=(e.clientX+10)+'px';cur.style.top=(e.clientY-25)+'px'});
cv.addEventListener('mousedown',function(e){sav();var p=gp(e);drag=true;lx=p.x;ly=p.y;paint(p.x,p.y,p.x+.1,p.y+.1)});
cv.addEventListener('mousemove',function(e){if(!drag)return;var p=gp(e);paint(lx,ly,p.x,p.y);lx=p.x;ly=p.y});
cv.addEventListener('mouseup',function(){drag=false});
cv.addEventListener('touchstart',function(e){e.preventDefault();sav();var p=tp(e);drag=true;lx=p.x;ly=p.y},{passive:false});
cv.addEventListener('touchmove',function(e){e.preventDefault();if(!drag)return;var p=tp(e);paint(lx,ly,p.x,p.y);lx=p.x;ly=p.y},{passive:false});
cv.addEventListener('touchend',function(){drag=false});

// Undo/Clear/Save
function sav(){if(hist.length>25)hist.shift();hist.push(cv.toDataURL())}
window.BUn=function(){if(hist.length>0){var img=new Image();img.onload=function(){X.clearRect(0,0,cv.width,cv.height);X.drawImage(img,0,0)};img.src=hist.pop()}};
window.BCl=function(){sav();drawPaper();ST.textContent='Tuval temizlendi'};
document.getElementById('BSAV').addEventListener('click',function(){
var a=document.createElement('a');a.download='boyama_'+tech+'_'+Date.now()+'.png';a.href=cv.toDataURL('image/png');a.click();
ST.textContent='Eser kaydedildi!'});

buildPal();drawPaper();updCur();
})();
</script>
        """
    components.html(boyama_html, height=820)


# ═══════════════════════════════════════════════════════════════
# 2b) EBRU SANATI
# ═══════════════════════════════════════════════════════════════

def _render_ebru_sanati():
    """Profesyonel Ebru Sanatı — interaktif dijital ebru."""
    import streamlit.components.v1 as components
    styled_section("🌊 Ebru Sanatı — UNESCO Kültürel Miras", "#06b6d4")

    _render_html("""
    <div style="background:linear-gradient(135deg,#0a1628,#164e63,#0891b2);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid rgba(6,182,212,0.5);text-align:center;position:relative;overflow:hidden">
        <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                     background:radial-gradient(circle at 30% 40%,rgba(6,182,212,0.1),transparent 50%)"></div>
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:10px">🌊🎨✨</div>
            <h2 style="color:#ecfeff !important;font-size:1.5rem;margin:0 0 8px !important">Ebru — Suyun Üzerinde Dans Eden Boya</h2>
            <p style="color:#a5f3fc !important;font-size:0.85rem;margin:0 !important">
                UNESCO Somut Olmayan Kültürel Miras. 600+ yıllık Türk sanatı. Her ebru benzersiz — tekrarlanamaz!
            </p>
        </div>
    </div>
    """)

    sub = st.tabs(["🎨 Dijital Ebru", "📖 Ebru Eğitimi", "🏛️ Ebru Tarihi"])

    with sub[0]:
        styled_section("🎨 Dijital Ebru Atölyesi", "#0891b2")
        st.caption("Renk paletinden boya seç → Tekneye tıkla = damla | Sürükle = taraka | 🗑️ Temizle")

        ebru_html = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
#ew{position:relative;max-width:840px;margin:0 auto;font-family:Georgia,serif}
#ef{background:linear-gradient(180deg,#4e342e 0%,#5d4037 3%,#795548 10%,#6d4c41 94%,#4e342e 100%);
border-radius:10px;padding:16px 18px 20px;position:relative;
box-shadow:0 8px 16px rgba(0,0,0,.5),0 20px 60px rgba(0,0,0,.35),inset 0 2px 3px rgba(255,255,255,.08);border:1px solid #3e2723}
#ef::before{content:'';position:absolute;inset:0;border-radius:10px;
background:repeating-linear-gradient(92deg,transparent,transparent 18px,rgba(0,0,0,.025) 18px,rgba(0,0,0,.025) 19px);pointer-events:none}
.cm{position:absolute;width:13px;height:13px;border-radius:50%;
background:radial-gradient(circle at 40% 35%,#d4a850,#8b6914,#5a4410);
box-shadow:0 1px 3px rgba(0,0,0,.5);z-index:2}
.cm.tl{top:7px;left:7px}.cm.tr{top:7px;right:7px}.cm.bl{bottom:7px;left:7px}.cm.br{bottom:7px;right:7px}
#ec{display:block;width:100%;border-radius:4px;cursor:crosshair;
box-shadow:inset 0 6px 20px rgba(0,0,0,.2),inset 0 -3px 10px rgba(0,0,0,.12);border:1px solid rgba(78,52,46,.6)}
#eo{display:none;position:absolute;top:16px;left:18px;right:18px;bottom:20px;pointer-events:none;z-index:10;border-radius:4px}
#etec{display:flex;gap:4px;justify-content:center;margin-top:8px;flex-wrap:wrap;
padding:6px 10px;background:linear-gradient(135deg,#1a237e,#283593);border-radius:8px;border:1px solid #3949ab}
.tb{padding:4px 9px;border-radius:5px;border:1px solid #5c6bc0;background:linear-gradient(180deg,#3949ab,#303f9f);
color:#c5cae9;cursor:pointer;font-size:.68rem;font-weight:600;transition:all .15s}
.tb:hover{background:linear-gradient(180deg,#5c6bc0,#3949ab);transform:translateY(-1px)}
.tb.on{background:linear-gradient(180deg,#7986cb,#5c6bc0);border-color:#e8eaf6;color:#fff;box-shadow:0 0 8px rgba(121,134,203,.4)}
#edc{display:flex;gap:8px;justify-content:center;align-items:center;margin-top:6px;
padding:5px 12px;background:linear-gradient(180deg,#263238,#37474f);border-radius:6px;border:1px solid #455a64;font-size:.63rem;color:#90a4ae}
.cbox{width:24px;height:24px;border-radius:50%;border:2.5px solid #607d8b;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.3);transition:all .15s}
.cbox.on{border-color:#ffd700;box-shadow:0 2px 8px rgba(255,215,0,.4)}
#epal{display:flex;gap:3px;justify-content:center;margin-top:8px;flex-wrap:wrap;
padding:8px 10px;background:linear-gradient(180deg,#3e2723,#4e342e);border-radius:8px;border:1px solid #5d4037}
.pj{display:flex;flex-direction:column;align-items:center;cursor:pointer;transition:all .15s}
.pj:hover{transform:translateY(-4px)}.pj.on{transform:translateY(-6px)}
.pj.on .jb{border-color:#ffd700;box-shadow:0 3px 10px rgba(255,215,0,.35)}
.jc{width:16px;height:5px;border-radius:2px 2px 0 0;background:#5d4037;border:1px solid rgba(0,0,0,.3);border-bottom:none}
.jb{width:22px;height:28px;border-radius:3px 3px 9px 9px;border:2px solid rgba(0,0,0,.3);
box-shadow:0 2px 4px rgba(0,0,0,.3),inset 0 -8px 12px rgba(0,0,0,.15);position:relative;overflow:hidden}
.jb::after{content:'';position:absolute;top:2px;left:2px;width:5px;height:7px;background:rgba(255,255,255,.2);border-radius:50%;transform:rotate(-20deg)}
.jl{font-size:.48rem;color:#8d6e63;margin-top:1px;max-width:26px;text-align:center;line-height:1}
#etool{display:flex;gap:5px;justify-content:center;align-items:center;margin-top:6px;flex-wrap:wrap;
padding:6px 12px;background:linear-gradient(180deg,#5d4037,#4e342e);border-radius:8px;border:1px solid #3e2723}
.tbn{padding:4px 10px;border-radius:5px;border:1px solid #795548;background:linear-gradient(180deg,#6d4c41,#5d4037);
color:#d7ccc8;cursor:pointer;font-size:.68rem;font-weight:600;transition:all .15s;box-shadow:0 2px 4px rgba(0,0,0,.2)}
.tbn:hover{background:linear-gradient(180deg,#795548,#6d4c41);transform:translateY(-1px)}
.tbn.on{background:linear-gradient(180deg,#8d6e63,#795548);border-color:#d7ccc8}
.fbtn{padding:5px 13px;border-radius:6px;border:1px solid #c62828;background:linear-gradient(180deg,#e53935,#c62828);
color:#fff;cursor:pointer;font-size:.7rem;font-weight:700;box-shadow:0 2px 8px rgba(198,40,40,.3);transition:all .15s}
.fbtn:hover{background:linear-gradient(180deg,#ef5350,#e53935);transform:translateY(-1px)}
.fbtn.ok{background:linear-gradient(180deg,#2e7d32,#1b5e20);border-color:#43a047}
.sbtn{padding:5px 14px;border-radius:6px;border:1px solid #b8860b;background:linear-gradient(180deg,#daa520,#b8860b);
color:#fff;cursor:pointer;font-size:.72rem;font-weight:700;box-shadow:0 2px 8px rgba(218,165,32,.35);transition:all .15s}
.sbtn:hover{background:linear-gradient(180deg,#f0c040,#daa520);transform:translateY(-1px);box-shadow:0 4px 12px rgba(218,165,32,.5)}
#est{text-align:center;margin-top:6px;font-size:.73rem;color:#a1887f;font-style:italic;min-height:1.2em}
.tl{color:#8d6e63;font-size:.63rem}
#esz{width:80px;accent-color:#8d6e63;vertical-align:middle}
</style>
<div id="ew">
<div id="ef">
<div class="cm tl"></div><div class="cm tr"></div><div class="cm bl"></div><div class="cm br"></div>
<canvas id="ec" width="760" height="480"></canvas>
<canvas id="eo" width="760" height="480"></canvas>
</div>
<div id="etec">
<span class="tl" style="color:#9fa8da;align-self:center">Teknik:</span>
<button class="tb on" data-t="battal">Battal</button>
<button class="tb" data-t="gelgit">Gel-Git</button>
<button class="tb" data-t="hatip">Hatip</button>
<button class="tb" data-t="tarakli">Tarakli</button>
<button class="tb" data-t="bulbul">Bulbul Yuvasi</button>
<button class="tb" data-t="cicek">Cicek</button>
<button class="tb" data-t="lale">Lale</button>
<button class="tb" data-t="gul">Gul</button>
<button class="tb" data-t="serbest">Serbest</button>
</div>
<div id="edc">
<span>1. Renk:</span><div class="cbox on" id="cb1"></div>
<span>2. Renk:</span><div class="cbox" id="cb2"></div>
<span style="color:#607d8b;font-size:.55rem">(Kutuya tikla, paletten renk sec)</span>
</div>
<div id="epal"></div>
<div id="etool">
<span class="tl">Boyut:</span><input type="range" id="esz" min="8" max="55" value="22">
<button class="tbn on" data-l="drop">Damla</button>
<button class="tbn" data-l="serpme">Serpme</button>
<button class="tbn" data-l="comb">Tarak</button>
<button class="tbn" data-l="needle">Biz</button>
<span class="tl">|</span>
<button class="tbn" onclick="EU()">Geri Al</button>
<button class="tbn" onclick="EC()">Temizle</button>
<span class="tl">|</span>
<button class="fbtn" id="bfin" onclick="EF()">Kagida Aktar (Bitir)</button>
</div>
<div style="display:flex;justify-content:center;margin-top:8px">
<button id="bsave" style="width:100%;max-width:500px;padding:12px 24px;border-radius:8px;border:2px solid #b8860b;
background:linear-gradient(180deg,#ffc107,#daa520,#b8860b);color:#fff;cursor:pointer;font-size:1rem;font-weight:800;
box-shadow:0 4px 16px rgba(218,165,32,.5);text-shadow:0 1px 3px rgba(0,0,0,.4);letter-spacing:1px">ESERI KAYDET (PNG)</button>
</div>
<div id="est">Kitreli su teknede hazir. Teknik sec, boya sec, damlatmaya basla!</div>
</div>
<script>
(function(){
var cv=document.getElementById('ec'),X=cv.getContext('2d');
var ov=document.getElementById('eo'),OX=ov.getContext('2d');
var ST=document.getElementById('est'),SZ=document.getElementById('esz');
var COLS=[{h:'#c0392b',n:'Kirmizi'},{h:'#e74c3c',n:'Acik Kirmizi'},{h:'#e67e22',n:'Turuncu'},
{h:'#f39c12',n:'Sari'},{h:'#f1c40f',n:'Altin'},{h:'#27ae60',n:'Yesil'},
{h:'#2ecc71',n:'Acik Yesil'},{h:'#1abc9c',n:'Turkuaz'},{h:'#2980b9',n:'Mavi'},
{h:'#3498db',n:'Gok Mavi'},{h:'#1a237e',n:'Lacivert'},{h:'#8e44ad',n:'Mor'},
{h:'#9b59b6',n:'Eflatun'},{h:'#e91e63',n:'Pembe'},{h:'#795548',n:'Kahve'},
{h:'#d4a017',n:'Oksit Sari'},{h:'#212121',n:'Siyah'},{h:'#fafafa',n:'Beyaz'}];
var C1=COLS[0].h,C1N=COLS[0].n,C2=COLS[6].h,C2N=COLS[6].n;
var cT=1,tool='drop',tech='battal';
var drops=[],ripples=[],trails=[],hist=[];
var drag=false,lx=0,ly=0,T=0,done=false;
function h2r(h){return{r:parseInt(h.slice(1,3),16),g:parseInt(h.slice(3,5),16),b:parseInt(h.slice(5,7),16)}}
function rs(c,a){return'rgba('+c.r+','+c.g+','+c.b+','+a+')'}
function lit(c,a){return{r:Math.min(255,c.r+a),g:Math.min(255,c.g+a),b:Math.min(255,c.b+a)}}
function drk(c,a){return{r:Math.max(0,c.r-a),g:Math.max(0,c.g-a),b:Math.max(0,c.b-a)}}
function drkH(h,a){var r=drk(h2r(h),a);return'#'+[r.r,r.g,r.b].map(function(v){return v.toString(16).padStart(2,'0')}).join('')}
// Palet
var pal=document.getElementById('epal');
COLS.forEach(function(col,i){
var j=document.createElement('div');j.className='pj'+(i===0?' on':'');j.title=col.n;
j.innerHTML='<div class="jc"></div><div class="jb" style="background:'+col.h+'"></div><div class="jl">'+col.n+'</div>';
j.onclick=function(){if(done)return;
document.querySelectorAll('.pj').forEach(function(b){b.classList.remove('on')});j.classList.add('on');
if(cT===2){C2=col.h;C2N=col.n;document.getElementById('cb2').style.background=col.h;ST.textContent='2. Renk: '+col.n}
else{C1=col.h;C1N=col.n;document.getElementById('cb1').style.background=col.h;ST.textContent='1. Renk: '+col.n}};
pal.appendChild(j)});
var cb1=document.getElementById('cb1'),cb2=document.getElementById('cb2');
cb1.style.background=C1;cb2.style.background=C2;
cb1.onclick=function(){cT=1;cb1.classList.add('on');cb2.classList.remove('on');ST.textContent='1. renk seciliyor'};
cb2.onclick=function(){cT=2;cb2.classList.add('on');cb1.classList.remove('on');ST.textContent='2. renk seciliyor'};
// Teknik
document.querySelectorAll('.tb').forEach(function(b){b.onclick=function(){if(done)return;tech=b.dataset.t;
document.querySelectorAll('.tb').forEach(function(x){x.classList.remove('on')});b.classList.add('on');
if(tech==='battal')setT('serpme');else setT('drop');
ST.textContent='Teknik: '+tech}});
function setT(t){if(done)return;tool=t;
document.querySelectorAll('.tbn').forEach(function(b){b.classList.remove('on')});
document.querySelectorAll('.tbn[data-l="'+t+'"]').forEach(function(b){b.classList.add('on')});
cv.style.cursor={drop:'crosshair',serpme:'cell',comb:'grab',needle:'cell'}[t]||'crosshair'}
document.querySelectorAll('.tbn[data-l]').forEach(function(b){b.onclick=function(){setT(b.dataset.l)}});
// SU
function drawW(){
var g=X.createLinearGradient(0,0,cv.width,cv.height);
g.addColorStop(0,'#f0e8c8');g.addColorStop(.3,'#ebe0b8');g.addColorStop(.6,'#e5d8ae');g.addColorStop(1,'#dbc89c');
X.fillStyle=g;X.fillRect(0,0,cv.width,cv.height);
if(done)return;
X.globalAlpha=.025;for(var i=0;i<200;i++){
var px=(Math.sin(i*7.3+T*.0008)*.5+.5)*cv.width,py=(Math.cos(i*11.1+T*.0006)*.5+.5)*cv.height;
X.beginPath();X.arc(px,py,.5+Math.abs(Math.sin(i*3.7))*1.5,0,6.28);X.fillStyle=i%3?'#b8a060':'#c8b070';X.fill()}
for(var L=0;L<3;L++){X.globalAlpha=.018+L*.008;
for(var y=0;y<cv.height;y+=9+L*4){X.beginPath();X.moveTo(0,y);
for(var x=0;x<cv.width;x+=4)X.lineTo(x,y+Math.sin(x*(.01+L*.007)+y*.005+T*(.002+L*.001))*(2.2-L*.5));
X.strokeStyle=['#fff8dc','#efe0b0','#d8c890'][L];X.lineWidth=.3+L*.1;X.stroke()}}
X.globalAlpha=.03;var rx=cv.width*.2+Math.sin(T*.0015)*30,ry=cv.height*.25+Math.cos(T*.0012)*20;
var lg=X.createRadialGradient(rx,ry,0,rx,ry,140);lg.addColorStop(0,'#fffde8');lg.addColorStop(1,'transparent');
X.fillStyle=lg;X.fillRect(0,0,cv.width,cv.height);
X.globalAlpha=1;
var gT=X.createLinearGradient(0,0,0,25);gT.addColorStop(0,'rgba(62,39,35,.15)');gT.addColorStop(1,'rgba(62,39,35,0)');X.fillStyle=gT;X.fillRect(0,0,cv.width,25);
var gB=X.createLinearGradient(0,cv.height-20,0,cv.height);gB.addColorStop(0,'rgba(62,39,35,0)');gB.addColorStop(1,'rgba(62,39,35,.12)');X.fillStyle=gB;X.fillRect(0,cv.height-20,cv.width,20);
X.globalAlpha=1}
// DAMLA ANİMASYON
function animD(){if(done)return;drops.forEach(function(d,di){d.age=(d.age||0)+1;var s=di*137.5;
var dx=Math.sin(T*.003+s)*.12,dy=Math.cos(T*.0025+s*.7)*.08;d.x+=dx;d.y+=dy;
d.bs=1+Math.sin(T*.008+s)*.015+Math.sin(T*.013+s*1.3)*.008;
if(d.pts)d.pts.forEach(function(p,pi){var ps=s+pi*23.7,wa=d.r*.025;
p.x+=Math.sin(T*.006+ps)*wa*p.ox+dx;p.y+=Math.cos(T*.005+ps*.8)*wa*p.oy+dy;
var tx=p.x-d.x,ty=p.y-d.y,cd=Math.sqrt(tx*tx+ty*ty);
if(cd>0){var df=(cd*d.bs-cd)*.02;p.x+=(tx/cd)*df;p.y+=(ty/cd)*df}})})}
// DAMLA ÇİZİM
function drawD(d,di){var rgb=h2r(d.color),s=di*137.5;
var ts=Math.sin(s)*18;
var rM={r:Math.min(255,Math.max(0,rgb.r+ts)),g:Math.min(255,Math.max(0,rgb.g+ts*.6)),b:Math.min(255,Math.max(0,rgb.b-ts*.3))};
var rL=lit(rM,35+Math.sin(s*2)*15),rD=drk(rM,30+Math.cos(s*3)*10),rE=drk(rgb,50);
var tf=done?0:1,bA=.78+Math.sin(T*.004*tf+s)*.06*tf;
if(d.pts&&d.pts.length>2){var p=d.pts;
X.save();X.globalAlpha=.06;X.beginPath();
X.moveTo((p[0].x+p[p.length-1].x)/2,(p[0].y+p[p.length-1].y)/2);
for(var i=0;i<p.length;i++){var a=p[i],b=p[(i+1)%p.length];X.quadraticCurveTo(a.x,a.y,(a.x+b.x)/2,(a.y+b.y)/2)}
X.closePath();var gr=d.r*1.5;var gg=X.createRadialGradient(d.x,d.y,d.r*.3,d.x,d.y,gr);
gg.addColorStop(0,rs(rM,.2));gg.addColorStop(.6,rs(rM,.05));gg.addColorStop(1,rs(rM,0));X.fillStyle=gg;X.fill();X.restore();
X.save();X.globalAlpha=bA;X.beginPath();X.moveTo((p[0].x+p[1].x)/2,(p[0].y+p[1].y)/2);
for(var i=0;i<p.length;i++){var a=p[i],b=p[(i+1)%p.length];X.quadraticCurveTo(a.x,a.y,(a.x+b.x)/2,(a.y+b.y)/2)}
X.closePath();
var hx=d.x+Math.sin(T*.004*tf+s)*d.r*.2*tf,hy=d.y+Math.cos(T*.003*tf+s)*d.r*.15*tf;
var ig=X.createRadialGradient(hx,hy,0,d.x,d.y,d.r*1.15);
ig.addColorStop(0,rs(rL,.95));ig.addColorStop(.15,rs(rM,.9));ig.addColorStop(.45,rs(rM,.75));
ig.addColorStop(.7,rs(rD,.55));ig.addColorStop(.9,rs(rE,.25));ig.addColorStop(1,rs(rE,.02));
X.fillStyle=ig;X.fill();
X.globalAlpha=.06;for(var i=0;i<8;i++){X.beginPath();
X.arc(d.x+Math.sin(s+i*41)*d.r*.7,d.y+Math.cos(s+i*67)*d.r*.7,Math.abs(d.r*(.06+Math.sin(i*13+s)*.04)),0,6.28);
X.fillStyle=i%2?rs(rD,.35):rs(rL,.3);X.fill()}
X.globalAlpha=.28;X.beginPath();X.moveTo((p[0].x+p[1].x)/2,(p[0].y+p[1].y)/2);
for(var i=0;i<p.length;i++){var a=p[i],b=p[(i+1)%p.length];X.quadraticCurveTo(a.x,a.y,(a.x+b.x)/2,(a.y+b.y)/2)}
X.closePath();X.strokeStyle=rs(rE,.5);X.lineWidth=.7;X.stroke();
X.globalAlpha=.14;X.beginPath();X.ellipse(d.x-d.r*.2,d.y-d.r*.26,d.r*.25,d.r*.1,-.35,0,6.28);
X.fillStyle='#fffef0';X.fill();X.restore()}
else{X.save();X.globalAlpha=bA;X.beginPath();X.arc(d.x,d.y,d.r,0,6.28);
var g=X.createRadialGradient(d.x-d.r*.2,d.y-d.r*.2,0,d.x,d.y,d.r);
g.addColorStop(0,rs(rL,.9));g.addColorStop(.4,rs(rM,.7));g.addColorStop(.8,rs(rD,.35));g.addColorStop(1,rs(rE,.02));
X.fillStyle=g;X.fill();X.restore()}}
function drawR(){ripples=ripples.filter(function(r){return r.life>0});
ripples.forEach(function(r){X.globalAlpha=r.life*.18;X.beginPath();X.arc(r.x,r.y,r.rad,0,6.28);
X.strokeStyle=r.col||'#d4c090';X.lineWidth=1.8*r.life;X.stroke();r.rad+=1.2+(1-r.life)*.8;r.life-=.012});X.globalAlpha=1}
function drawTr(){trails=trails.filter(function(t){return t.life>0});
trails.forEach(function(t){X.globalAlpha=t.life*.25;X.beginPath();X.moveTo(t.x1,t.y1);X.lineTo(t.x2,t.y2);
X.strokeStyle='rgba(180,160,120,.4)';X.lineWidth=t.w||1;X.stroke();t.life-=.006});X.globalAlpha=1}
function frame(){T++;drawW();drawTr();animD();drops.forEach(drawD);drawR();requestAnimationFrame(frame)}
// FİZİK
function mkP(x,y,r){var pts=[],seg=Math.max(16,20+Math.floor(r/2));
for(var i=0;i<seg;i++){var a=(i/seg)*6.28,n=.82+Math.random()*.36;
pts.push({x:x+Math.cos(a)*r*n,y:y+Math.sin(a)*r*n,ox:Math.cos(a),oy:Math.sin(a),phase:Math.random()*6.28})}return pts}
function puD(x,y,sz){var pr=sz*4.5;drops.forEach(function(d){var dx=d.x-x,dy=d.y-y,dist=Math.sqrt(dx*dx+dy*dy);
if(dist<pr&&dist>0){var str=Math.pow((pr-dist)/pr,1.5)*sz*.45;d.x+=(dx/dist)*str;d.y+=(dy/dist)*str;
if(d.pts)d.pts.forEach(function(p){var pd=Math.sqrt((p.x-x)*(p.x-x)+(p.y-y)*(p.y-y));
if(pd<pr&&pd>0){var pf=Math.pow((pr-pd)/pr,2)*sz*.4;p.x+=(p.x-x)/pd*pf;p.y+=(p.y-y)/pd*pf}});d.r*=1+str*.002}})}
function mk(x,y,r,col){puD(x,y,r);var sv=r*(.9+Math.random()*.2);
drops.push({x:x,y:y,r:sv,color:col||C1,pts:mkP(x,y,r),age:0,bs:1});
for(var i=0;i<3;i++)ripples.push({x:x,y:y,rad:sv*.4+i*6,life:1-i*.2,col:(col||C1)+'44'})}
// TEKNİKLER
function sav(){if(hist.length>30)hist.shift();hist.push(JSON.parse(JSON.stringify(drops)))}
function battal(x,y){sav();var n=6+Math.floor(Math.random()*10);
for(var i=0;i<n;i++){var a=Math.random()*6.28,d=Math.random()*100;
var sx=x+Math.cos(a)*d,sy=y+Math.sin(a)*d;if(sx>8&&sx<cv.width-8&&sy>8&&sy<cv.height-8)mk(sx,sy,3+Math.random()*10)}
ST.textContent='Battal — '+drops.length+' damla'}
function gelgit(){sav();for(var i=0;i<30;i++)mk(40+Math.random()*(cv.width-80),40+Math.random()*(cv.height-80),4+Math.random()*8,COLS[Math.floor(Math.random()*COLS.length)].h);
setTimeout(function(){for(var y=30;y<cv.height-30;y+=25)drops.forEach(function(d){if(Math.abs(d.y-y)<40){var f=(40-Math.abs(d.y-y))/40*12;d.x+=f;if(d.pts)d.pts.forEach(function(p){p.x+=f*.8})}});
setTimeout(function(){for(var x=30;x<cv.width-30;x+=25)drops.forEach(function(d){if(Math.abs(d.x-x)<40){var f=(40-Math.abs(d.x-x))/40*12;d.y-=f;if(d.pts)d.pts.forEach(function(p){p.y-=f*.8})}});ST.textContent='Gel-Git olustu!'},200)},200);ST.textContent='Gel-Git...'}
function hatip(x,y){sav();var bs=+SZ.value;for(var ring=0;ring<5;ring++){var rr=bs*.8+ring*bs*.6,segs=8+ring*4,col=ring%2?C2:C1;
for(var i=0;i<segs;i++){var a=(i/segs)*6.28;mk(x+Math.cos(a)*rr,y+Math.sin(a)*rr,4+ring*1.5,col)}}ST.textContent='Hatip deseni!'}
function tarakli(){sav();for(var i=0;i<25;i++)mk(40+Math.random()*(cv.width-80),40+Math.random()*(cv.height-80),4+Math.random()*7,COLS[Math.floor(Math.random()*COLS.length)].h);
var dir=Math.random()>.5?1:-1;for(var row=0;row<Math.floor(cv.height/20);row++){var ry=20+row*20,rd=row%2?-dir:dir;
drops.forEach(function(d){if(Math.abs(d.y-ry)<15){var f=(15-Math.abs(d.y-ry))/15*10*rd;d.x+=f;if(d.pts)d.pts.forEach(function(p){p.x+=f*.8})}})}ST.textContent='Tarakli desen!'}
function bulbul(x,y){sav();var bs=+SZ.value;for(var ring=0;ring<6;ring++){var r=bs*.3+ring*bs*.35,col=ring%2?C2:C1,cnt=6+ring*3;
for(var i=0;i<cnt;i++){var a=(i/cnt)*6.28;mk(x+Math.cos(a)*r,y+Math.sin(a)*r,3+ring,col)}}
var ang=0;for(var s=0;s<40;s++){ang+=.25;var sr=bs*.2+s*bs*.05,sx=x+Math.cos(ang)*sr,sy=y+Math.sin(ang)*sr,mx=Math.cos(ang+1.57)*3,my=Math.sin(ang+1.57)*3;
drops.forEach(function(d){var dist=Math.sqrt((d.x-sx)*(d.x-sx)+(d.y-sy)*(d.y-sy));if(dist<25&&dist>0){var f=Math.pow((25-dist)/25,2)*.4;d.x+=mx*f;d.y+=my*f;if(d.pts)d.pts.forEach(function(p){p.x+=mx*f*.7;p.y+=my*f*.7})}})}ST.textContent='Bulbul Yuvasi!'}
function cicek(x,y){sav();var bs=+SZ.value;mk(x,y,bs*.35,'#f39c12');
for(var i=0;i<6;i++)mk(x+Math.cos(i/6*6.28)*bs*.4,y+Math.sin(i/6*6.28)*bs*.4,bs*.2,C1);
var pc=5+Math.floor(Math.random()*2);for(var i=0;i<pc;i++){var a=i/pc*6.28-1.57;
for(var s=0;s<4;s++){var sz=bs*.25-s*2;if(sz>2)mk(x+Math.cos(a)*bs*(.6+s*.35),y+Math.sin(a)*bs*(.6+s*.35),sz,C1)}}
for(var s=0;s<5;s++)mk(x+Math.sin(s*.3)*3,y+bs*1.5+s*bs*.5,3,'#27ae60');mk(x+15,y+bs*2.2,8,'#2ecc71');ST.textContent='Cicek ebru!'}
function lale(x,y){sav();var bs=+SZ.value;
for(var ring=0;ring<4;ring++){var r=bs*.15+ring*bs*.12,col=ring%2?C2:C1,cnt=6+ring*2;
for(var i=0;i<cnt;i++){var a=(i/cnt)*6.28;mk(x+Math.cos(a)*r,y-bs*.3+Math.sin(a)*r*.7,3+ring,col)}}
[-1.97,-1.57,-1.17].forEach(function(a,pi){var col=pi===1?C1:C2;
for(var s=0;s<4;s++){var sz=bs*.22-s*2;if(sz>2)mk(x+Math.cos(a)*bs*(.4+s*.35),y-bs*.3+Math.sin(a)*bs*(.4+s*.35),sz,col)}
// Hafif biz sivriltme
for(var s=0;s<8;s++){var d=bs*(.5+s*.2),sx=x+Math.cos(a)*d,sy=y-bs*.3+Math.sin(a)*d,mmx=Math.cos(a)*4,mmy=Math.sin(a)*4;
for(var di=0;di<drops.length;di++){var dd=drops[di],dist=Math.sqrt((dd.x-sx)*(dd.x-sx)+(dd.y-sy)*(dd.y-sy));
if(dist<18&&dist>0){var f=Math.pow((18-dist)/18,2)*.3;dd.x+=mmx*f;dd.y+=mmy*f}}}});
for(var s=0;s<5;s++)mk(x+Math.sin(s*.15)*2,y+bs*.3+s*bs*.5,2.5,'#27ae60');
mk(x+10,y+bs*1.8,5,'#2ecc71');mk(x-10,y+bs*1.5,5,'#2ecc71');
ST.textContent='Osmanli Lalesi!'}
function gul(x,y){sav();var bs=+SZ.value;
// Merkez
mk(x,y,bs*.25,C1);
// İç yapraklar — 2 halka
for(var ring=0;ring<2;ring++){var cnt=4+ring*2,r=bs*(.35+ring*.3);
for(var i=0;i<cnt;i++){var a=i/cnt*6.28+ring*.5;mk(x+Math.cos(a)*r,y+Math.sin(a)*r,bs*.18-ring*3,ring<1?C1:C2)}}
// Dış yapraklar — büyük
for(var i=0;i<5;i++){var a=i/5*6.28+.2;mk(x+Math.cos(a)*bs*1.05,y+Math.sin(a)*bs*1.05,bs*.22,C2)}
// Spiral kıvrım (hafif)
var sa=0;for(var s=0;s<15;s++){sa+=.4;var sr=bs*.2+s*bs*.06;
var sx=x+Math.cos(sa)*sr,sy=y+Math.sin(sa)*sr,mmx=Math.cos(sa+1.57)*3,mmy=Math.sin(sa+1.57)*3;
for(var di=0;di<drops.length;di++){var d=drops[di],dist=Math.sqrt((d.x-sx)*(d.x-sx)+(d.y-sy)*(d.y-sy));
if(dist<20&&dist>0){var f=Math.pow((20-dist)/20,2)*.3;d.x+=mmx*f;d.y+=mmy*f}}}
// Sap
for(var s=0;s<4;s++)mk(x,y+bs*1.2+s*bs*.4,2.5,'#27ae60');
mk(x+12,y+bs*1.8,6,'#2ecc71');mk(x-10,y+bs*1.5,5,'#2ecc71');
ST.textContent='Gul deseni!'}
// BİTİR
var finPh=0;
window.EF=function(){if(drops.length===0){ST.textContent='Once boya damlatin!';return}
if(!done){done=true;var btn=document.getElementById('bfin');btn.textContent='Tekrar Basla';btn.classList.add('ok');cv.style.cursor='default';
ov.style.display='block';finPh=0;
(function af(){finPh+=.012;if(finPh>1)finPh=1;OX.clearRect(0,0,ov.width,ov.height);
var cy=-ov.height+ov.height*finPh;OX.fillStyle='rgba(255,253,245,'+(finPh*.15)+')';OX.fillRect(0,Math.max(0,cy),ov.width,ov.height);
if(finPh>=1){OX.globalAlpha=.04;for(var i=0;i<150;i++){OX.beginPath();var fx=Math.random()*ov.width,fy=Math.random()*ov.height;
OX.moveTo(fx,fy);OX.lineTo(fx+Math.random()*8-4,fy+Math.random()*3-1.5);OX.strokeStyle='#b0a080';OX.lineWidth=.3;OX.stroke()}
OX.globalAlpha=1;OX.strokeStyle='rgba(180,160,120,.15)';OX.lineWidth=2;OX.strokeRect(8,8,ov.width-16,ov.height-16);
OX.fillStyle='rgba(120,100,70,.25)';OX.font='italic 11px Georgia';OX.fillText('Dijital Ebru - SmartCampusAI',ov.width-220,ov.height-15);
ST.textContent='Kagida aktarildi! Kaydet ile indir.';return}
ST.textContent=finPh<.5?'Kagit indiriliyor %'+Math.floor(finPh*200):'Boya yapisiyor %'+Math.floor((finPh-.5)*200);requestAnimationFrame(af)})()}
else{done=false;finPh=0;ov.style.display='none';OX.clearRect(0,0,ov.width,ov.height);drops=[];trails=[];ripples=[];hist=[];
var btn=document.getElementById('bfin');btn.textContent='Kagida Aktar (Bitir)';btn.classList.remove('ok');cv.style.cursor='crosshair';ST.textContent='Yeni tekne hazir!'}};
// UNDO/CLEAR/SAVE
window.EU=function(){if(done)return;if(hist.length>0){drops=hist.pop();ST.textContent='Geri — '+drops.length+' damla'}else ST.textContent='Geri alinacak yok'};
window.EC=function(){if(done)return;sav();drops=[];trails=[];ripples=[];ST.textContent='Tekne temizlendi'};
function doSave(){var tmp=document.createElement('canvas');tmp.width=cv.width;tmp.height=cv.height;var tx=tmp.getContext('2d');tx.drawImage(cv,0,0);
if(done&&ov.style.display!=='none')tx.drawImage(ov,0,0);var a=document.createElement('a');a.download='ebru_'+Date.now()+'.png';a.href=tmp.toDataURL('image/png');a.click();ST.textContent='PNG kaydedildi!'}
window.ES=doSave;
document.getElementById('bsave').addEventListener('click',doSave);
// MOUSE/TOUCH
function gp(e){var r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)*(cv.width/r.width),y:(e.clientY-r.top)*(cv.height/r.height)}}
function tp(e){var t=e.touches[0],r=cv.getBoundingClientRect();return{x:(t.clientX-r.left)*(cv.width/r.width),y:(t.clientY-r.top)*(cv.height/r.height)}}
function dn(px,py){if(done)return;
if(tech!=='serbest'&&(tool==='drop'||tool==='serpme')){
if(tech==='battal'){battal(px,py);return}if(tech==='gelgit'){gelgit();return}
if(tech==='hatip'){hatip(px,py);return}if(tech==='tarakli'){tarakli();return}
if(tech==='bulbul'){bulbul(px,py);return}if(tech==='cicek'){cicek(px,py);return}
if(tech==='lale'){lale(px,py);return}if(tech==='gul'){gul(px,py);return}}
if(tool==='drop'){sav();mk(px,py,+SZ.value);ST.textContent=drops.length+' damla'}
else if(tool==='serpme')battal(px,py);drag=true;lx=px;ly=py}
function mv(px,py){if(done||!drag)return;var mx=px-lx,my=py-ly;
if(tool==='comb'){var len=Math.sqrt(mx*mx+my*my)||1;
for(var t=-3;t<=3;t++){var tx2=lx+(-my/len)*t*18,ty2=ly+(mx/len)*t*18;
drops.forEach(function(d){var dist=Math.sqrt((d.x-tx2)*(d.x-tx2)+(d.y-ty2)*(d.y-ty2));if(dist<65&&dist>0){var f=Math.pow((65-dist)/65,1.5)*.4;d.x+=mx*f;d.y+=my*f;if(d.pts)d.pts.forEach(function(p){p.x+=mx*f*.75;p.y+=my*f*.75})}})}
trails.push({x1:lx,y1:ly,x2:px,y2:py,life:1,w:2.5})}
else if(tool==='needle'){drops.forEach(function(d){var dist=Math.sqrt((d.x-lx)*(d.x-lx)+(d.y-ly)*(d.y-ly));if(dist<32&&dist>0){var f=Math.pow((32-dist)/32,2)*.65;d.x+=mx*f;d.y+=my*f;
if(d.pts)d.pts.forEach(function(p){var pd=Math.sqrt((p.x-lx)*(p.x-lx)+(p.y-ly)*(p.y-ly));if(pd<32){var pf=Math.pow((32-pd)/32,2)*.6;p.x+=mx*pf;p.y+=my*pf}})}});
trails.push({x1:lx,y1:ly,x2:px,y2:py,life:1,w:.9})}
else if(tool==='serpme'&&Math.random()<.3)mk(px+Math.random()*20-10,py+Math.random()*20-10,2+Math.random()*5);
lx=px;ly=py}
cv.onmousedown=function(e){var p=gp(e);dn(p.x,p.y)};cv.onmousemove=function(e){var p=gp(e);mv(p.x,p.y)};
cv.onmouseup=cv.onmouseleave=function(){drag=false};
cv.addEventListener('touchstart',function(e){e.preventDefault();var p=tp(e);dn(p.x,p.y)},{passive:false});
cv.addEventListener('touchmove',function(e){e.preventDefault();var p=tp(e);mv(p.x,p.y)},{passive:false});
cv.addEventListener('touchend',function(){drag=false});
frame()})();
</script>
        """
        components.html(ebru_html, height=880)

    with sub[1]:
        styled_section("📖 Ebru Eğitimi — Adım Adım", "#0891b2")

        dersler = [
            {"ders": 1, "ad": "Malzemeler", "ikon": "🧰",
             "icerik": "**Tekne:** Dikdörtgen sığ kap (40×50 cm)\n**Kitre:** Geven bitkisinden — suyu kıvamlandırır\n**Boyalar:** Doğal toprak pigmentler + öd (sığır safra kesesi)\n**Biz/Tarak:** İnce metal çubuklar, şekillendirme için\n**Kağıt:** Ebru kağıdı veya kalın çizim kağıdı"},
            {"ders": 2, "ad": "Kitre Hazırlama", "ikon": "💧",
             "icerik": "1. 10g kitre tozunu 1L soğuk suya ekle\n2. 12-24 saat beklet (şişsin)\n3. Süz — pürüzsüz kıvamlı su elde et\n4. Tekneye dök — boya yüzeyinde yüzmeli\n5. Test: bir damla boya damlatıp yüzüyor mu kontrol et"},
            {"ders": 3, "ad": "Boya Hazırlama", "ikon": "🎨",
             "icerik": "1. Pigment tozunu havanda ez (ince toz)\n2. Birkaç damla öd (sığır safra) ekle — yüzey gerilimini düşürür\n3. Su ekleyerek kıvam ayarla\n4. Test: tekneye damla — yayılıyorsa hazır\n5. Yayılmıyorsa öd ekle, çok yayılıyorsa pigment ekle"},
            {"ders": 4, "ad": "Battal Ebru (Temel)", "ikon": "🌀",
             "icerik": "En temel teknik — boyaları rastgele serpme:\n1. Fırçayı boyaya batır\n2. Teknenin üzerinde hafifçe vur — damlalar düşer\n3. Farklı renkleri üst üste serp\n4. Boyalar birbirini iter — doğal desen oluşur\n5. Kağıdı yüzeye yavaşça koy, kaldır — eser hazır!"},
            {"ders": 5, "ad": "Gel-Git Ebru", "ikon": "🌊",
             "icerik": "Tarakla yatay-dikey çekme:\n1. Battal ebru ile zemin hazırla\n2. Tarakı yatay olarak bir yönde çek\n3. Sonra dikey olarak ters yönde çek\n4. Gel-git deseni oluşur — dalga gibi!\n5. İstersen çapraz da çekebilirsin"},
            {"ders": 6, "ad": "Çiçek Ebru (Lale/Karanfil)", "ikon": "🌷",
             "icerik": "Ebru'nun en zor ve gösterişli tekniği:\n1. İç içe daireler damlatarak çiçek tabanı oluştur\n2. Biz ile merkeze doğru çek — yaprak şekli\n3. Sap için aşağı doğru uzun çek\n4. Yapraklar için yanlara kısa çekişler\n5. Lale, karanfil, sümbül — Osmanlı çiçek geleneği"},
            {"ders": 7, "ad": "Hatip Ebru", "ikon": "📐",
             "icerik": "Geometrik desenler — hatip = vaiz:\n1. Merkezden dışa doğru eş merkezli daireler damlatır\n2. Her dairenin arası farklı renk\n3. Biz ile köşelere çekerek yıldız/geometrik form oluştur\n4. Genellikle hat sanatı altlığı olarak kullanılır"},
            {"ders": 8, "ad": "Kağıda Aktarma", "ikon": "📄",
             "icerik": "Son adım — en kritik an:\n1. Kağıdı bir köşesinden tutup hafif kıvırarak suya değdir\n2. Yavaşça bırak — hava kabarcığı kalmasın!\n3. 5-10 saniye bekle — boya kağıda yapışsın\n4. Bir köşesinden yavaşça kaldır\n5. Düz bir yüzeye bırakıp kurut — DOKUNMA!\n6. Kuruyunca üstüne ağırlık koy (düzleşsin)"},
        ]

        for d in dersler:
            with st.expander(f"{d['ikon']} Ders {d['ders']}: {d['ad']}", expanded=(d['ders'] <= 2)):
                st.markdown(d["icerik"])

    with sub[2]:
        styled_section("🏛️ Ebru Tarihi & Ustalar", "#f59e0b")

        tarih = [
            ("🏛️ Köken", "8-9. yy", "Orta Asya Türkleri. 'Ebri' = bulut — boyalar bulut gibi yayılır."),
            ("📜 Osmanlı", "15-16. yy", "Saray sanatı. Kitap ciltleri, hat sanatı altlığı."),
            ("🌸 Altın Çağ", "17-18. yy", "Necmeddin Okyay: modern ebrunun babası. Çiçek ebru tekniği."),
            ("🌍 UNESCO", "2014", "Türk Ebru Sanatı UNESCO Somut Olmayan Kültürel Miras listesine alındı!"),
            ("🎨 Günümüz", "21. yy", "Dijital ebru, kumaş ebru, 3D ebru. Dünya çapında atölyeler."),
        ]

        for ad, yil, bilgi in tarih:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;
                         border-left:4px solid #f59e0b">
                <div style="display:flex;gap:12px;align-items:center">
                    <span style="font-size:1.3rem">{ad.split(' ')[0]}</span>
                    <div>
                        <span style="font-weight:700;color:#fde68a !important">{ad.split(' ',1)[1] if ' ' in ad else ad} ({yil})</span>
                        <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:2px">{bilgi}</div>
                    </div>
                </div>
            </div>
            """)

        st.markdown("---")
        styled_section("🏆 Ünlü Ebru Ustaları", "#8b5cf6")
        ustalar = [
            ("Necmeddin Okyay", "1883-1976", "Modern ebrunun babası. Çiçek ebru tekniğini geliştirdi. Hat, tezhip ve cilt sanatında da usta."),
            ("Mustafa Düzgünman", "1920-1990", "Necmeddin Okyay'ın öğrencisi. Ebru'yu dünyaya tanıtan isim. 'Ebrunun efendisi' lakabı."),
            ("Hikmet Barutçugil", "1950-", "Çağdaş ebrunun öncüsü. 50+ ülkede atölye verdi. Yeni teknikler geliştirdi."),
            ("Fuat Başar", "1962-", "İstanbul'da Ebru Vakfı kurucusu. UNESCO başvurusunu yönetti. Dünya çapında tanıtım."),
        ]
        for ad, yasam, bilgi in ustalar:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;
                         border-left:4px solid #8b5cf6">
                <div style="font-weight:700;color:#e9d5ff !important;font-size:0.95rem">{ad} <span style="color:#94a3b8;font-weight:400">({yasam})</span></div>
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:2px">{bilgi}</div>
            </div>
            """)


# ═══════════════════════════════════════════════════════════════
# 3) RENK DÜNYASI
# ═══════════════════════════════════════════════════════════════

def _render_renk_dunyasi():
    styled_section("🌈 Renk Dünyası", "#f59e0b")

    sub = st.tabs(["🎨 Renk Çarkı", "🔬 Karıştır & Keşfet", "🎯 Renk Oyunu"])

    with sub[0]:
        for kategori, bilgi in RENKLER.items():
            styled_section(f"🎨 {kategori}", "#f59e0b")
            st.caption(bilgi["aciklama"])
            cols = st.columns(len(bilgi["renkler"]))
            for col, (ad, kod, aciklama) in zip(cols, bilgi["renkler"]):
                with col:
                    _render_html(f"""
                    <div style="background:{kod};border-radius:14px;padding:20px;text-align:center;min-height:100px;
                                 display:flex;flex-direction:column;align-items:center;justify-content:center">
                        <div style="font-weight:700;color:white !important;font-size:1rem;text-shadow:1px 1px 3px rgba(0,0,0,0.5)">{ad}</div>
                        <div style="font-size:0.7rem;color:rgba(255,255,255,0.8) !important;margin-top:4px">{kod}</div>
                        <div style="font-size:0.7rem;color:rgba(255,255,255,0.7) !important;margin-top:2px">{aciklama}</div>
                    </div>
                    """)

    with sub[1]:
        styled_section("🔬 Renk Karıştırıcı", "#10b981")
        col1, col2, col3 = st.columns(3)
        with col1:
            r1 = st.color_picker("Renk 1", "#ef4444", key="snt_mix1")
        with col2:
            st.markdown("<div style='text-align:center;font-size:2rem;padding-top:20px'>➕</div>", unsafe_allow_html=True)
        with col3:
            r2 = st.color_picker("Renk 2", "#3b82f6", key="snt_mix2")

        # Basit karışım
        c1 = tuple(int(r1.lstrip('#')[i:i+2], 16) for i in (0,2,4))
        c2 = tuple(int(r2.lstrip('#')[i:i+2], 16) for i in (0,2,4))
        mixed = tuple((a+b)//2 for a,b in zip(c1,c2))
        mixed_hex = f"#{mixed[0]:02x}{mixed[1]:02x}{mixed[2]:02x}"
        _render_html(f"""
        <div style="text-align:center;margin:16px 0">
            <div style="font-size:1rem;color:#94a3b8 !important;margin-bottom:8px">Sonuç:</div>
            <div style="background:{mixed_hex};width:120px;height:120px;border-radius:50%;margin:0 auto;
                         border:4px solid #334155;display:flex;align-items:center;justify-content:center">
                <span style="color:white !important;font-weight:700;text-shadow:1px 1px 3px rgba(0,0,0,0.5)">{mixed_hex}</span>
            </div>
        </div>
        """)

    with sub[2]:
        styled_section("🎯 Renk Eşleştirme Oyunu", "#6366f1")
        hedef_r, hedef_g, hedef_b = random.randint(50,220), random.randint(50,220), random.randint(50,220)

        if st.button("🎲 Yeni Renk!", key="snt_renk_oyun", type="primary"):
            st.session_state["snt_hedef"] = (random.randint(50,220), random.randint(50,220), random.randint(50,220))

        if "snt_hedef" in st.session_state:
            hr, hg, hb = st.session_state["snt_hedef"]
            hedef_hex = f"#{hr:02x}{hg:02x}{hb:02x}"
            _render_html(f"""
            <div style="display:flex;justify-content:center;gap:40px;margin:16px 0">
                <div style="text-align:center">
                    <div style="font-size:0.8rem;color:#94a3b8 !important;margin-bottom:4px">🎯 Hedef Renk</div>
                    <div style="background:{hedef_hex};width:100px;height:100px;border-radius:16px;border:3px solid #334155"></div>
                </div>
            </div>
            """)
            tahmin = st.color_picker("Tahminin:", "#808080", key="snt_renk_tahmin")
            if st.button("Karşılaştır!", key="snt_renk_karsilastir"):
                tc = tuple(int(tahmin.lstrip('#')[i:i+2], 16) for i in (0,2,4))
                fark = sum(abs(a-b) for a,b in zip((hr,hg,hb), tc))
                skor = max(0, 100 - fark // 3)
                if skor >= 90:
                    st.success(f"🎉 Mükemmel! %{skor} benzerlik!")
                    st.balloons()
                elif skor >= 60:
                    st.warning(f"👍 İyi! %{skor} benzerlik")
                else:
                    st.error(f"🎨 %{skor} benzerlik — daha yakın dene!")


# ═══════════════════════════════════════════════════════════════
# 4) DESEN FABRİKASI
# ═══════════════════════════════════════════════════════════════

def _render_desen_fabrikasi():
    styled_section("📐 Desen & Motif Fabrikası", "#10b981")
    import streamlit.components.v1 as components

    col1, col2, col3 = st.columns(3)
    with col1:
        simetri = st.selectbox("Simetri", [4, 6, 8, 12], key="snt_sim", format_func=lambda x: f"{x}-kat simetri")
    with col2:
        renk = st.color_picker("Çizgi Rengi", "#8b5cf6", key="snt_desen_renk")
    with col3:
        kalinlik = st.slider("Kalınlık", 1, 8, 2, key="snt_desen_k")

    html = f"""
    <canvas id="sntDesen" width="500" height="500" style="border-radius:50%;border:3px solid #334155;cursor:crosshair;display:block;margin:0 auto;background:#0B0F19"></canvas>
    <div style="text-align:center;margin-top:8px">
        <button onclick="document.getElementById('sntDesen').getContext('2d').clearRect(0,0,500,500)" style="padding:6px 16px;border-radius:8px;border:1px solid #475569;background:#1e293b;color:#e0e7ff;cursor:pointer">🗑️ Temizle</button>
    </div>
    <script>
    (function(){{
        const c=document.getElementById('sntDesen'),ctx=c.getContext('2d');
        const cx=250,cy=250,sym={simetri};
        let drawing=false,lx=0,ly=0;
        ctx.lineCap='round';

        function drawSym(x1,y1,x2,y2){{
            for(let i=0;i<sym;i++){{
                let angle=2*Math.PI*i/sym;
                let cos=Math.cos(angle),sin=Math.sin(angle);
                let rx1=(x1-cx)*cos-(y1-cy)*sin+cx;
                let ry1=(x1-cx)*sin+(y1-cy)*cos+cy;
                let rx2=(x2-cx)*cos-(y2-cy)*sin+cx;
                let ry2=(x2-cx)*sin+(y2-cy)*cos+cy;
                ctx.beginPath();ctx.moveTo(rx1,ry1);ctx.lineTo(rx2,ry2);
                ctx.strokeStyle='{renk}';ctx.lineWidth={kalinlik};ctx.stroke();
                // Ayna
                ctx.beginPath();ctx.moveTo(2*cx-rx1,ry1);ctx.lineTo(2*cx-rx2,ry2);
                ctx.strokeStyle='{renk}';ctx.lineWidth={kalinlik};ctx.stroke();
            }}
        }}

        c.addEventListener('mousedown',e=>{{drawing=true;lx=e.offsetX;ly=e.offsetY;}});
        c.addEventListener('mousemove',e=>{{
            if(!drawing)return;
            drawSym(lx,ly,e.offsetX,e.offsetY);
            lx=e.offsetX;ly=e.offsetY;
        }});
        c.addEventListener('mouseup',()=>{{drawing=false;}});
        c.addEventListener('mouseleave',()=>{{drawing=false;}});
    }})();
    </script>
    """
    components.html(html, height=560)
    st.info("🎨 Çizdiğin her çizgi otomatik olarak simetrik yansıtılır! Mandala oluştur!")


# ═══════════════════════════════════════════════════════════════
# 5) MÜZİK ATÖLYESİ
# ═══════════════════════════════════════════════════════════════

def _render_muzik():
    styled_section("🎵 Müzik Atölyesi", "#3b82f6")
    import streamlit.components.v1 as components

    sub = st.tabs(["Grand Piyano", "Nota Egitimi", "Ogretim Programi", "Piyano Dersleri", "Unlu Besteciler", "Nota Okuma Oyunu", "Ritim Oyunu"])

    with sub[0]:
        styled_section("🎹 Grand Piyano — Profesyonel", "#3b82f6")

        col1, col2, col3 = st.columns(3)
        with col1:
            ses_tipi = st.selectbox("Ses Tipi", ["grand", "upright", "electric", "organ", "harpsichord"],
                                     key="snt_ses", format_func=lambda x: {
                                         "grand":"🎹 Kuyruklu Piyano","upright":"🎹 Duvar Piyanosu",
                                         "electric":"⚡ Elektro Piyano","organ":"⛪ Org",
                                         "harpsichord":"🏰 Klavsen"}.get(x,x))
        with col2:
            oktav = st.selectbox("Oktav Aralığı", ["2 Oktav (C4-C6)", "3 Oktav (C3-C6)", "4 Oktav (C3-C7)"],
                                  key="snt_oktav")
        with col3:
            reverb = st.selectbox("Efekt", ["Kuru (Dry)", "Salon (Hall)", "Kilise (Cathedral)"],
                                   key="snt_reverb")

        st.caption("⌨️ Klavye: Z-M (alt oktav beyaz) • A-K (üst oktav beyaz) • S,D,G,H,J (üst siyah)")

        okt_count = int(str(oktav)[0]) if oktav else 2
        wave_map = {"grand":"triangle","upright":"triangle","electric":"square","organ":"sawtooth","harpsichord":"square"}
        decay_map = {"grand":2.0,"upright":1.5,"electric":1.0,"organ":3.0,"harpsichord":0.5}
        wave = wave_map.get(ses_tipi, "triangle")
        decay = decay_map.get(ses_tipi, 1.5)

        html = f"""
        <style>
        /* Grand Piyano Gövdesi */
        #pianoBody {{
            background: linear-gradient(180deg, #3e2723 0%, #4e342e 20%, #5d4037 50%, #4e342e 80%, #3e2723 100%);
            border-radius: 16px 16px 8px 8px;
            padding: 20px 16px 12px;
            box-shadow: 0 12px 40px rgba(0,0,0,0.6), inset 0 2px 4px rgba(255,255,255,0.05);
            border: 3px solid #2c1810;
            position: relative;
            max-width: 850px; margin: 0 auto;
        }}
        /* Piyano üst kapak */
        #pianoBody::before {{
            content: '🎹 GRAND PIANO';
            display: block; text-align: center;
            font-size: 0.7rem; font-weight: 700; letter-spacing: 3px;
            color: #d4a574; margin-bottom: 12px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }}
        /* Nota çubuğu */
        #pianoLed {{
            background: #1a1a2e; border-radius: 8px; padding: 6px 12px;
            margin-bottom: 10px; text-align: center;
            border: 1px solid #2c1810;
            font-family: 'Courier New', monospace;
        }}
        #pianoLed .led-note {{ font-size: 1.6rem; font-weight: 900; color: #fbbf24; }}
        #pianoLed .led-freq {{ font-size: 0.7rem; color: #94a3b8; }}
        /* Tuş alanı */
        #pianoKeys {{
            display: flex; justify-content: center;
            position: relative;
            background: linear-gradient(180deg, #1a1208, #0d0a06);
            border-radius: 4px; padding: 4px 6px 8px;
            border: 1px solid #2c1810;
        }}
        /* Beyaz tuşlar */
        .pk-w {{
            width: 42px; height: 180px;
            background: linear-gradient(180deg, #334155 0%, #1e293b 70%, #0f172a 85%, #0b1120 100%);
            border-radius: 0 0 5px 5px;
            cursor: pointer; margin: 0 1px;
            position: relative; z-index: 1;
            border: 1px solid #475569;
            border-top: none;
            box-shadow: 0 2px 3px rgba(0,0,0,0.3), inset 0 -2px 3px rgba(0,0,0,0.15);
            display: flex; align-items: flex-end; justify-content: center;
            padding-bottom: 6px;
            font-size: 0.55rem; font-weight: 600; color: #94a3b8;
            transition: all 0.06s;
            user-select: none;
        }}
        .pk-w:active, .pk-w.active {{
            background: linear-gradient(180deg, #1e293b, #0f172a) !important;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1) !important;
            height: 178px !important;
        }}
        /* Siyah tuşlar */
        .pk-b {{
            width: 26px; height: 115px;
            background: linear-gradient(180deg, #222 0%, #111 60%, #1a1a1a 100%);
            border-radius: 0 0 3px 3px;
            cursor: pointer;
            position: absolute; z-index: 2;
            border: 1px solid #000;
            box-shadow: 0 3px 5px rgba(0,0,0,0.4), inset 0 -1px 2px rgba(255,255,255,0.05);
            display: flex; align-items: flex-end; justify-content: center;
            padding-bottom: 4px;
            font-size: 0.45rem; font-weight: 600; color: #666;
            transition: all 0.06s;
            user-select: none;
        }}
        .pk-b:active, .pk-b.active {{
            background: linear-gradient(180deg, #333, #222) !important;
            height: 113px !important;
        }}
        /* Tabure */
        #pianoStool {{
            width: 120px; height: 16px; margin: 16px auto 0;
            background: linear-gradient(180deg, #5d4037, #4e342e);
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            position: relative;
        }}
        #pianoStool::before, #pianoStool::after {{
            content: '';
            position: absolute; bottom: -20px;
            width: 6px; height: 20px;
            background: linear-gradient(180deg, #4e342e, #3e2723);
            border-radius: 0 0 3px 3px;
        }}
        #pianoStool::before {{ left: 15px; }}
        #pianoStool::after {{ right: 15px; }}
        /* Pedal */
        #pianoPedals {{
            display: flex; justify-content: center; gap: 12px;
            margin-top: 8px;
        }}
        .pedal {{
            width: 20px; height: 8px; background: #b8860b;
            border-radius: 2px; border: 1px solid #8b6914;
            box-shadow: 0 2px 3px rgba(0,0,0,0.3);
        }}
        </style>

        <div id="pianoBody">
            <div id="pianoLed">
                <span class="led-note" id="ledNote">🎵</span>
                <span class="led-freq" id="ledFreq">Bir tuşa bas!</span>
            </div>
            <div id="pianoKeys"></div>
            <div id="pianoPedals"><div class="pedal"></div><div class="pedal"></div><div class="pedal"></div></div>
        </div>
        <div id="pianoStool"></div>
        <script>
        (function(){{
            const keys=document.getElementById('pianoKeys');
            const ledNote=document.getElementById('ledNote');
            const ledFreq=document.getElementById('ledFreq');
            const ctx=new(window.AudioContext||window.webkitAudioContext)();
            const waveType='{wave}';
            const decayTime={decay};

            // Nota isimleri ve frekanslar — {okt_count} oktav
            const noteNames=['Do','Do#','Re','Re#','Mi','Fa','Fa#','Sol','Sol#','La','La#','Si'];
            const isBlack=[0,1,0,1,0,0,1,0,1,0,1,0];
            const kbWhite='zxcvbnm,asdfghjkl'.split('');
            const kbBlack='sdghjwetyuo'.split('');
            const startOctave = {okt_count} >= 3 ? 3 : 4;
            const octaves = {okt_count};
            const allNotes=[];
            for(let o=startOctave;o<startOctave+octaves;o++){{
                for(let i=0;i<12;i++){{
                    const freq=440*Math.pow(2,(o-4)+(i-9)/12);
                    const name=noteNames[i]+(o>4?'⁺':'');
                    allNotes.push({{n:name,f:freq,w:!isBlack[i],o:o}});
                }}
            }}

            function playNote(freq,name){{
                ledNote.textContent=name;
                ledFreq.textContent=freq.toFixed(1)+' Hz';

                // Zengin ses üretimi (2 osilatör + harmonik)
                const osc1=ctx.createOscillator(), osc2=ctx.createOscillator();
                const gain=ctx.createGain();
                osc1.connect(gain); osc2.connect(gain); gain.connect(ctx.destination);
                osc1.frequency.value=freq;
                osc1.type=waveType;
                osc2.frequency.value=freq*2.01; // hafif detune harmonik
                osc2.type='sine';
                const now=ctx.currentTime;
                gain.gain.setValueAtTime(0.35,now);
                gain.gain.exponentialRampToValueAtTime(0.001,now+decayTime);
                osc1.start(now); osc1.stop(now+decayTime);
                osc2.start(now); osc2.stop(now+decayTime);
            }}

            const keyMap={{}};
            let wIdx=0, bIdx=0;
            const whiteW=44;

            // Beyaz tuşlar
            allNotes.filter(n=>n.w).forEach((n,i)=>{{
                const k=document.createElement('div');
                k.className='pk-w';
                k.textContent=n.n;
                k.addEventListener('mousedown',()=>{{k.classList.add('active');playNote(n.f,n.n);}});
                k.addEventListener('mouseup',()=>k.classList.remove('active'));
                k.addEventListener('mouseleave',()=>k.classList.remove('active'));
                keys.appendChild(k);
                if(kbWhite[i]) {{ keyMap[kbWhite[i]]=k; k._freq=n.f; k._name=n.n; }}
            }});

            // Siyah tuşlar
            allNotes.forEach((n,idx)=>{{
                if(!n.w){{
                    let wBefore=allNotes.slice(0,idx).filter(x=>x.w).length;
                    let left=wBefore*whiteW-12+6;
                    const k=document.createElement('div');
                    k.className='pk-b';
                    k.style.left=left+'px';
                    k.addEventListener('mousedown',()=>{{k.classList.add('active');playNote(n.f,n.n);}});
                    k.addEventListener('mouseup',()=>k.classList.remove('active'));
                    k.addEventListener('mouseleave',()=>k.classList.remove('active'));
                    keys.appendChild(k);
                    if(kbBlack[bIdx]) {{ keyMap[kbBlack[bIdx]]=k; k._freq=n.f; k._name=n.n; }}
                    bIdx++;
                }}
            }});

            // Klavye desteği
            document.addEventListener('keydown',e=>{{
                if(e.repeat)return;
                const k=keyMap[e.key.toLowerCase()];
                if(k){{k.classList.add('active');playNote(k._freq,k._name);}}
            }});
            document.addEventListener('keyup',e=>{{
                const k=keyMap[e.key.toLowerCase()];
                if(k)k.classList.remove('active');
            }});
        }})();
        </script>
        """
        components.html(html, height=600)

    with sub[1]:
        styled_section("🎼 Nota Eğitimi", "#8b5cf6")

        _render_html("""
        <div style="background:#0f172a;border-radius:16px;padding:20px;margin-bottom:16px;border:1px solid rgba(99,102,241,0.15)">
            <div style="font-weight:700;color:#e0e7ff !important;font-size:1rem;margin-bottom:12px">🎼 Porte Üzerinde Notalar</div>
            <div style="color:#94a3b8 !important;font-size:0.85rem;line-height:1.6">
                <b>Porte:</b> 5 yatay çizgiden oluşan nota yazım sistemi.<br>
                <b>Sol Anahtarı (𝄞):</b> İkinci çizgiye Sol notasını yerleştirir.<br>
                <b>Fa Anahtarı (𝄢):</b> Dördüncü çizgiye Fa notasını yerleştirir.
            </div>
        </div>
        """)

        notalar = [
            ("Do", "C", "🔴", "261 Hz", "İlk nota. Piyanoda ortadaki beyaz tuş."),
            ("Re", "D", "🟠", "294 Hz", "Do'dan bir tam ses yukarı."),
            ("Mi", "E", "🟡", "330 Hz", "Re'den bir tam ses yukarı. Mi-Fa arası yarım ses!"),
            ("Fa", "F", "🟢", "349 Hz", "Mi'den yarım ses yukarı. Dikkat: yarım ses!"),
            ("Sol", "G", "🔵", "392 Hz", "Fa'dan bir tam ses yukarı. Sol anahtarının notası."),
            ("La", "A", "🟣", "440 Hz", "Akort notası! Tüm orkestra buna göre akort olur."),
            ("Si", "B", "🟤", "494 Hz", "La'dan bir tam ses yukarı. Si-Do arası yarım ses!"),
            ("Do²", "C²", "⚪", "523 Hz", "Bir oktav yukarıdaki Do. Frekans tam 2 katı!"),
        ]

        for nota_tr, nota_en, emoji, frekans, aciklama in notalar:
            _render_html(f"""
            <div style="display:flex;align-items:center;gap:14px;background:#0f172a;border-radius:12px;padding:10px 16px;
                         margin-bottom:4px;border:1px solid rgba(99,102,241,0.08)">
                <div style="font-size:1.5rem;min-width:30px">{emoji}</div>
                <div style="min-width:50px;font-weight:800;color:#e0e7ff !important;font-size:1.1rem">{nota_tr}</div>
                <div style="min-width:30px;color:#6366f1 !important;font-size:0.8rem">{nota_en}</div>
                <div style="min-width:60px;color:#94a3b8 !important;font-size:0.75rem">{frekans}</div>
                <div style="flex:1;color:#94a3b8 !important;font-size:0.8rem">{aciklama}</div>
            </div>
            """)

        st.markdown("---")
        styled_section("🎵 Aralıklar", "#10b981")
        araliklar = [
            ("Tam Ses", "Do→Re, Re→Mi, Fa→Sol, Sol→La, La→Si", "Piyanoda 1 beyaz tuş atlama"),
            ("Yarım Ses", "Mi→Fa, Si→Do", "Piyanoda komşu tuşlar (siyah tuş arası yok!)"),
            ("Oktav", "Do→Do², La→La²", "Aynı nota, frekans 2 katı"),
        ]
        for ad, ornekler, aciklama in araliklar:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:4px;border-left:3px solid #10b981">
                <span style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</span>
                <span style="color:#94a3b8 !important;font-size:0.8rem;margin-left:8px">{ornekler}</span>
                <div style="font-size:0.75rem;color:#6366f1 !important;margin-top:2px">{aciklama}</div>
            </div>
            """)

    with sub[2]:
        styled_section("📖 Piyano Öğretim Programı — Seviye Sistemi", "#ec4899")

        _render_html("""
        <div style="background:linear-gradient(135deg,#831843,#be185d);border-radius:16px;padding:20px;margin-bottom:16px;
                     border:2px solid rgba(236,72,153,0.4);text-align:center">
            <div style="font-size:2rem;margin-bottom:6px">🎹📖🎓</div>
            <div style="font-weight:700;color:white !important;font-size:1.1rem">Profesyonel Piyano Eğitim Yol Haritası</div>
            <div style="color:#fce7f3 !important;font-size:0.85rem">Seviye 1'den 8'e — uluslararası standartlara uygun müfredat</div>
        </div>
        """)

        seviyeler = [
            {"seviye": 1, "ad": "Hazırlık", "sure": "1-3 ay", "renk": "#10b981", "ikon": "🌱",
             "konular": ["Piyanoda oturuş ve el pozisyonu", "Parmak numaraları (1-5)", "Orta Do (C4) tanıma",
                          "Beyaz tuşlar: Do-Re-Mi-Fa-Sol", "Basit ritim: tam nota, yarım nota",
                          "İlk melodi: Mary Had a Little Lamb", "Sağ el 5 parmak pozisyonu"],
             "hedef": "5 notalık basit melodileri sağ elle çalabilir."},
            {"seviye": 2, "ad": "Başlangıç 1", "sure": "3-6 ay", "renk": "#3b82f6", "ikon": "🌿",
             "konular": ["Tüm beyaz tuşlar (Do-Si)", "Sol el tanıtımı", "İki el koordinasyonu (basit)",
                          "Çeyrek nota ve sekizlik nota", "f (forte) ve p (piano) dinamikleri",
                          "Legato (bağlı) çalış", "Twinkle Twinkle Little Star"],
             "hedef": "İki elle basit melodiler çalabilir, nota değerlerini bilir."},
            {"seviye": 3, "ad": "Başlangıç 2", "sure": "6-12 ay", "renk": "#8b5cf6", "ikon": "🌳",
             "konular": ["Siyah tuşlar ve diyezler/bemoller", "Do Majör ve Sol Majör gamları",
                          "Basit akorlar: C, F, G", "Staccato (kesik) çalış",
                          "Pedal kullanımına giriş", "Ode to Joy (Beethoven)", "Basit eşlik kalıpları"],
             "hedef": "Gam ve basit akorlari çalabilir. Pedal kullanmaya başlar."},
            {"seviye": 4, "ad": "Orta 1", "sure": "1-2 yıl", "renk": "#f59e0b", "ikon": "⭐",
             "konular": ["Tüm majör gamlar", "Minör gamlar (doğal, armonik, melodik)",
                          "Akor yürüyüşleri (I-IV-V-I)", "Arpejler", "Noktalı ritimler",
                          "Für Elise (Beethoven) — basitleştirilmiş", "Crescendo & diminuendo"],
             "hedef": "Majör/minör gamlar, akorlar ve orta zorlukta parçalar çalabilir."},
            {"seviye": 5, "ad": "Orta 2", "sure": "2-3 yıl", "renk": "#ef4444", "ikon": "🔥",
             "konular": ["Kromatik gam", "Oktav çalışları", "Triller ve süslemeler",
                          "Sonatina formuna giriş", "Chopin Vals (basit)", "Bach İki Sesli Envansiyonlar",
                          "Sight reading (ilk görüşte çalma)"],
             "hedef": "Teknik zorlukları aşar, müzikal ifade gelişir."},
            {"seviye": 6, "ad": "İleri 1", "sure": "3-5 yıl", "renk": "#ec4899", "ikon": "💎",
             "konular": ["Sonat formları", "Bach: İyi Düzenlenmiş Klavye", "Mozart/Haydn Sonatları",
                          "Chopin Noktürnler", "Pedal teknikleri (yarım pedal)", "Transpozisyon",
                          "Eşlik ve doğaçlama"],
             "hedef": "Klasik repertuarı yorumlayabilir, müzikal olgunluk."},
            {"seviye": 7, "ad": "İleri 2", "sure": "5-8 yıl", "renk": "#6366f1", "ikon": "👑",
             "konular": ["Beethoven Sonatları (Pathetique, Moonlight)", "Chopin Etütler",
                          "Liszt: Konsolasyon", "Debussy: Clair de Lune", "Romantik dönem yorumu",
                          "Konçerto hazırlığı", "Sahne performansı"],
             "hedef": "Konser repertuarı çalabilir, sahne deneyimi kazanır."},
            {"seviye": 8, "ad": "Virtüöz", "sure": "8+ yıl", "renk": "#eab308", "ikon": "🏆",
             "konular": ["Rachmaninoff Konçertoları", "Liszt Macar Rapsodileri",
                          "Chopin Balladlar", "Prokofiev Sonatları", "Konser piyanisti tekniği",
                          "Oda müziği ve eşlik", "Müzik teorisi ve analiz"],
             "hedef": "Profesyonel düzeyde performans. Konser piyanisti yetkinliği."},
        ]

        for s in seviyeler:
            with st.expander(f"{s['ikon']} Seviye {s['seviye']}: {s['ad']} ({s['sure']})", expanded=(s['seviye'] <= 2)):
                _render_html(f"""
                <div style="background:{s['renk']}10;border-radius:14px;padding:16px;border-left:4px solid {s['renk']}">
                    <div style="font-weight:700;color:#e0e7ff !important;font-size:1rem;margin-bottom:8px">
                        {s['ikon']} Seviye {s['seviye']} — {s['ad']}
                    </div>
                    <div style="font-size:0.8rem;color:{s['renk']} !important;margin-bottom:8px">⏱️ Tahmini Süre: {s['sure']}</div>
                </div>
                """)
                st.markdown("**📋 Konular:**")
                for konu in s["konular"]:
                    st.markdown(f"- {konu}")
                _render_html(f"""
                <div style="background:rgba(16,185,129,0.08);border-radius:10px;padding:10px;margin-top:8px;border-left:3px solid #10b981">
                    <div style="font-weight:700;color:#10b981 !important;font-size:0.85rem">🎯 Hedef:</div>
                    <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">{s['hedef']}</div>
                </div>
                """)

    with sub[3]:
        styled_section("🎹 Piyano Dersleri", "#f59e0b")

        dersler = [
            {"ders": 1, "ad": "İlk Dokunuş", "seviye": "Başlangıç",
             "icerik": "Piyanoda oturuş pozisyonu, el duruşu, parmak numaraları (1=baş parmak, 5=serçe). Orta Do'yu (C4) bul ve bas.",
             "pratik": "Sağ elin 5 parmağıyla Do-Re-Mi-Fa-Sol'u sırayla çal. Her nota 1 saniye."},
            {"ders": 2, "ad": "İlk Melodi — Mary Had a Little Lamb", "seviye": "Başlangıç",
             "icerik": "Mi-Re-Do-Re-Mi-Mi-Mi (sağ el). Sadece 3 nota ile ilk melodin!",
             "pratik": "Yavaş başla, tekrarla, hız artır. Notaları söyleyerek çal."},
            {"ders": 3, "ad": "Sol El Tanıtımı", "seviye": "Başlangıç",
             "icerik": "Sol elin 5. parmağı Do'ya (C3), 1. parmağı Sol'a. Aynı egzersizi sol elle yap.",
             "pratik": "Sol el: Do-Re-Mi-Fa-Sol, sonra geri: Sol-Fa-Mi-Re-Do."},
            {"ders": 4, "ad": "Siyah Tuşlar", "seviye": "Başlangıç",
             "icerik": "Diyez (#) = yarım ses yukarı, Bemol (♭) = yarım ses aşağı. Piyanoda siyah tuşlar bunlardır.",
             "pratik": "Do# - Re# - Fa# - Sol# - La# siyah tuşlarını sırayla çal."},
            {"ders": 5, "ad": "İlk Akor — Do Majör", "seviye": "Orta",
             "icerik": "Do Majör akor: Do-Mi-Sol (C-E-G). 3 notayı aynı anda bas!",
             "pratik": "Do Majör (Do-Mi-Sol), Fa Majör (Fa-La-Do), Sol Majör (Sol-Si-Re) akorlarını sırayla çal."},
            {"ders": 6, "ad": "Ritim & Süre", "seviye": "Orta",
             "icerik": "Tam nota (4 vuruş ○), Yarım nota (2 vuruş 𝅗𝅥), Çeyrek nota (1 vuruş ♩), Sekizlik (½ vuruş ♪)",
             "pratik": "Metronom eşliğinde: Do(4)-Re(2)-Mi(2)-Fa(1)-Sol(1)-La(1)-Si(1)-Do²(4)"},
        ]

        for d in dersler:
            with st.expander(f"📚 Ders {d['ders']}: {d['ad']} ({d['seviye']})", expanded=(d['ders'] <= 2)):
                st.markdown(d["icerik"])
                _render_html(f"""
                <div style="background:rgba(245,158,11,0.08);border-radius:10px;padding:12px;margin-top:8px;border-left:3px solid #f59e0b">
                    <div style="font-weight:700;color:#fde68a !important;font-size:0.85rem">🎯 Pratik:</div>
                    <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">{d['pratik']}</div>
                </div>
                """)

    with sub[4]:
        styled_section("🎶 Ünlü Besteciler", "#ec4899")

        besteciler = [
            {"ad": "Ludwig van Beethoven", "yasam": "1770-1827", "ulke": "Almanya 🇩🇪",
             "portre_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/330px-Beethoven.jpg",
             "eserler": "9. Senfoni, Ay Işığı Sonatı, Für Elise",
             "bilgi": "28 yaşında sağır olmaya başladı ama en büyük eserlerini sağırken besteledi! 9. Senfoni'yi hiç duymadan yazdı.",
             "ikon": "🎵"},
            {"ad": "Wolfgang Amadeus Mozart", "yasam": "1756-1791", "ulke": "Avusturya 🇦🇹",
             "portre_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Wolfgang-amadeus-mozart_1.jpg/330px-Wolfgang-amadeus-mozart_1.jpg",
             "eserler": "Sihirli Flüt, Requiem, Küçük Gece Müziği",
             "bilgi": "5 yaşında besteler yapıyordu! 35 yıllık ömründe 600+ eser bıraktı. Müziğin Mozart'ı — adı efsane oldu.",
             "ikon": "🎼"},
            {"ad": "Johann Sebastian Bach", "yasam": "1685-1750", "ulke": "Almanya 🇩🇪",
             "portre_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Johann_Sebastian_Bach.jpg/330px-Johann_Sebastian_Bach.jpg",
             "eserler": "Tokkata ve Füg, Brandenburg Konçertoları, Matthäus Passioni",
             "bilgi": "Batı müziğinin babası. Müziğin matematiğini kurdu — füg formunu mükemmelleştirdi. 20 çocuğu vardı!",
             "ikon": "🎹"},
            {"ad": "Pyotr Tchaikovsky", "yasam": "1840-1893", "ulke": "Rusya 🇷🇺",
             "portre_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Portr%C3%A4t_des_Komponisten_Pjotr_I._Tschaikowski_%281840-1893%29.jpg/330px-Portr%C3%A4t_des_Komponisten_Pjotr_I._Tschaikowski_%281840-1893%29.jpg",
             "eserler": "Kuğu Gölü, Fındıkkıran, 1812 Uvertürü",
             "bilgi": "Bale müziğinin kralı. Kuğu Gölü ve Fındıkkıran dünyanın en çok sahnelenen baleleridir.",
             "ikon": "🩰"},
            {"ad": "Frédéric Chopin", "yasam": "1810-1849", "ulke": "Polonya 🇵🇱",
             "portre_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Chopin%2C_by_Wodzinska.JPG/330px-Chopin%2C_by_Wodzinska.JPG",
             "eserler": "Noktürnler, Balladlar, Polonezler",
             "bilgi": "Piyano şairi. Neredeyse tüm eserleri piyano içindir. 39 yaşında tüberkülozdan öldü.",
             "ikon": "🎹"},
            {"ad": "Antonio Vivaldi", "yasam": "1678-1741", "ulke": "İtalya 🇮🇹",
             "portre_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Vivaldi.jpg/330px-Vivaldi.jpg",
             "eserler": "Dört Mevsim, Gloria",
             "bilgi": "Kızıl rahip — kızıl saçları yüzünden bu lakabı aldı. Dört Mevsim tarihin en çok dinlenen klasik eseridir.",
             "ikon": "🎻"},
        ]

        for b in besteciler:
            img = f'<img src="{b["portre_url"]}" style="width:70px;height:70px;border-radius:50%;object-fit:cover;border:2px solid #ec4899" onerror="this.style.display=\'none\'">' if b.get("portre_url") else f'<div style="font-size:2.5rem">{b["ikon"]}</div>'
            _render_html(f"""
            <div class="snt-card" style="display:flex;gap:16px;align-items:center">
                <div style="min-width:70px;text-align:center">{img}</div>
                <div style="flex:1">
                    <div style="font-weight:700;color:#e9d5ff !important;font-size:1rem">{b['ad']}</div>
                    <div style="font-size:0.75rem;color:#c084fc !important">{b['yasam']} • {b['ulke']}</div>
                    <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:4px">🎵 {b['eserler']}</div>
                </div>
            </div>
            """)
            with st.expander(f"📖 {b['ad']}"):
                st.markdown(b["bilgi"])

    # ── GAME 1: Nota Okuma Oyunu ──────────────────────────────
    with sub[5]:
        styled_section("Nota Okuma Oyunu", "#10b981")
        nota_okuma_html = """
        <style>
          #notaGame * { box-sizing: border-box; margin: 0; padding: 0; }
          #notaGame {
            background: #0f172a; border-radius: 16px; padding: 18px;
            font-family: 'Segoe UI', sans-serif; color: #e2e8f0;
            max-width: 700px; margin: 0 auto;
          }
          #notaGame .ng-hdr {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 12px;
          }
          #notaGame .ng-hdr h3 { font-size: 1.1rem; color: #86efac; }
          #notaGame .ng-stats {
            display: flex; gap: 14px; font-size: 0.8rem;
          }
          #notaGame .ng-stats span { padding: 3px 10px; border-radius: 8px; background: #1e293b; }
          #notaGame .ng-stats .s-ok { color: #4ade80; }
          #notaGame .ng-stats .s-err { color: #f87171; }
          #notaGame .ng-stats .s-time { color: #fbbf24; }
          #notaGame canvas {
            display: block; margin: 0 auto 14px; border-radius: 10px;
            border: 1px solid #334155;
          }
          #notaGame .ng-btns {
            display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;
          }
          #notaGame .ng-btns button {
            padding: 10px 18px; border: 2px solid #334155; border-radius: 10px;
            background: #1e293b; color: #e2e8f0; font-size: 0.95rem;
            font-weight: 700; cursor: pointer; transition: all 0.15s;
            min-width: 56px;
          }
          #notaGame .ng-btns button:hover { border-color: #6366f1; background: #312e81; }
          #notaGame .ng-msg {
            text-align: center; margin-top: 10px; font-size: 0.9rem;
            min-height: 24px; font-weight: 600;
          }
          #notaGame .ng-replay {
            display: none; margin: 10px auto 0; padding: 10px 28px;
            border: none; border-radius: 10px; cursor: pointer;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white; font-size: 0.95rem; font-weight: 700;
          }
          #notaGame .ng-level {
            text-align: center; font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px;
          }
        </style>
        <div id="notaGame">
          <div class="ng-hdr">
            <h3>Nota Okuma Oyunu</h3>
            <div class="ng-stats">
              <span class="s-ok" id="ngOk">Dogru: 0</span>
              <span class="s-err" id="ngErr">Yanlis: 0</span>
              <span class="s-time" id="ngTime">Sure: 60</span>
            </div>
          </div>
          <div class="ng-level" id="ngLevel">Seviye 1 - Temel Notalar (Do-Sol)</div>
          <canvas id="ngCanvas" width="660" height="200"></canvas>
          <div class="ng-btns" id="ngBtns"></div>
          <div class="ng-msg" id="ngMsg"></div>
          <button class="ng-replay" id="ngReplay" onclick="ngStart()">Tekrar Oyna</button>
        </div>
        <script>
        (function(){
          const noteNames = ['Do','Re','Mi','Fa','Sol','La','Si'];
          // staff positions: Do=below staff (ledger), Re=below 1st line, Mi=1st line, Fa=1st space, Sol=2nd line, La=2nd space, Si=3rd line
          // y positions on canvas (top=40 staff starts, line spacing=24)
          const staffTop = 55, ls = 24;
          // positions relative to staff bottom (line 1=bottom line index 0)
          // Do=ledger below, Re=space below line1, Mi=line1, Fa=space1, Sol=line2, La=space2, Si=line3
          const noteYMap = {
            'Do': staffTop + 5*ls,       // ledger line below
            'Re': staffTop + 4*ls + ls/2, // space below line 1
            'Mi': staffTop + 4*ls,        // line 1
            'Fa': staffTop + 3*ls + ls/2, // space 1-2
            'Sol': staffTop + 3*ls,       // line 2
            'La': staffTop + 2*ls + ls/2, // space 2-3
            'Si': staffTop + 2*ls         // line 3
          };
          const sharpNotes = ['Do#','Re#','Fa#','Sol#','La#'];
          const sharpYMap = {
            'Do#': noteYMap['Do'] - ls/2,
            'Re#': noteYMap['Re'] - ls/2,
            'Fa#': noteYMap['Fa'] - ls/2,
            'Sol#': noteYMap['Sol'] - ls/2,
            'La#': noteYMap['La'] - ls/2
          };

          let correct=0, wrong=0, timer=60, level=1, currentNote='', running=false, interval=null;
          const canvas = document.getElementById('ngCanvas');
          const ctx = canvas.getContext('2d');
          const btnBox = document.getElementById('ngBtns');
          const msgEl = document.getElementById('ngMsg');
          const replayBtn = document.getElementById('ngReplay');
          const okEl = document.getElementById('ngOk');
          const errEl = document.getElementById('ngErr');
          const timeEl = document.getElementById('ngTime');
          const levelEl = document.getElementById('ngLevel');

          function getPool() {
            if (level >= 3) return noteNames.concat(sharpNotes);
            if (level >= 2) return noteNames.slice();
            return noteNames.slice(0, 5); // Do-Sol
          }

          function drawStaff() {
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            // treble clef symbol
            ctx.fillStyle = '#94a3b8';
            ctx.font = '64px serif';
            ctx.fillText('\\u{1D11E}', 10, staffTop + 4*ls + 4);
            // staff lines
            ctx.strokeStyle = '#475569'; ctx.lineWidth = 1.5;
            for (let i = 0; i < 5; i++) {
              let y = staffTop + i * ls;
              ctx.beginPath(); ctx.moveTo(60, y); ctx.lineTo(640, y); ctx.stroke();
            }
          }

          function drawNote(name) {
            let isSharp = name.includes('#');
            let y = isSharp ? sharpYMap[name] : noteYMap[name];
            if (!y) y = staffTop + 2*ls;
            let x = 350;
            // ledger line for Do
            if (name === 'Do' || name === 'Do#') {
              ctx.strokeStyle = '#475569'; ctx.lineWidth = 1.5;
              ctx.beginPath(); ctx.moveTo(x-22, noteYMap['Do']); ctx.lineTo(x+22, noteYMap['Do']); ctx.stroke();
            }
            // note head
            ctx.fillStyle = '#fbbf24';
            ctx.beginPath(); ctx.ellipse(x, y, 14, 10, -0.2, 0, Math.PI*2); ctx.fill();
            // stem
            ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2.5;
            ctx.beginPath(); ctx.moveTo(x+13, y); ctx.lineTo(x+13, y-50); ctx.stroke();
            // sharp symbol
            if (isSharp) {
              ctx.fillStyle = '#f87171'; ctx.font = 'bold 22px serif';
              ctx.fillText('#', x - 30, y + 7);
            }
          }

          function pickNote() {
            let pool = getPool();
            let n;
            do { n = pool[Math.floor(Math.random()*pool.length)]; } while(n === currentNote && pool.length > 1);
            currentNote = n;
            drawStaff();
            drawNote(n);
          }

          function updateStats() {
            okEl.textContent = 'Dogru: ' + correct;
            errEl.textContent = 'Yanlis: ' + wrong;
            timeEl.textContent = 'Sure: ' + timer;
          }

          function buildBtns() {
            btnBox.innerHTML = '';
            let pool = getPool();
            pool.forEach(function(name) {
              let b = document.createElement('button');
              b.textContent = name;
              b.onclick = function() { guess(name); };
              btnBox.appendChild(b);
            });
          }

          function flashCanvas(color) {
            ctx.fillStyle = color;
            ctx.globalAlpha = 0.18;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.globalAlpha = 1.0;
            setTimeout(function(){ drawStaff(); drawNote(currentNote); }, 200);
          }

          function guess(name) {
            if (!running) return;
            if (name === currentNote) {
              correct++;
              msgEl.style.color = '#4ade80';
              msgEl.textContent = 'Dogru! ' + currentNote;
              flashCanvas('rgba(74,222,128,0.3)');
              // level up
              if (correct === 8 && level < 2) { level = 2; levelEl.textContent = 'Seviye 2 - Tum Notalar (Do-Si)'; buildBtns(); }
              if (correct === 18 && level < 3) { level = 3; levelEl.textContent = 'Seviye 3 - Diyezler Eklendi'; buildBtns(); }
              setTimeout(pickNote, 350);
            } else {
              wrong++;
              msgEl.style.color = '#f87171';
              msgEl.textContent = 'Yanlis! Dogru cevap: ' + currentNote;
              flashCanvas('rgba(248,113,113,0.3)');
              // shake
              canvas.style.transform = 'translateX(-4px)';
              setTimeout(function(){ canvas.style.transform = 'translateX(4px)'; }, 60);
              setTimeout(function(){ canvas.style.transform = ''; }, 120);
            }
            updateStats();
          }

          function endGame() {
            running = false;
            clearInterval(interval);
            msgEl.style.color = '#fbbf24';
            let total = correct + wrong;
            let pct = total > 0 ? Math.round(correct/total*100) : 0;
            msgEl.textContent = 'Oyun Bitti! ' + correct + '/' + total + ' dogru (%' + pct + ') - Seviye ' + level;
            replayBtn.style.display = 'block';
          }

          window.ngStart = function() {
            correct = 0; wrong = 0; timer = 60; level = 1;
            running = true;
            replayBtn.style.display = 'none';
            msgEl.textContent = '';
            levelEl.textContent = 'Seviye 1 - Temel Notalar (Do-Sol)';
            updateStats();
            buildBtns();
            pickNote();
            clearInterval(interval);
            interval = setInterval(function(){
              timer--;
              updateStats();
              if (timer <= 0) endGame();
            }, 1000);
          };

          // auto-start
          ngStart();
        })();
        </script>
        """
        components.html(nota_okuma_html, height=580)

    # ── GAME 2: Ritim Oyunu ───────────────────────────────────
    with sub[6]:
        styled_section("Ritim Oyunu", "#f59e0b")

        ritim_html = """
        <style>
          #ritmGame * { box-sizing: border-box; margin: 0; padding: 0; }
          #ritmGame {
            background: #0f172a; border-radius: 16px; padding: 14px;
            font-family: 'Segoe UI', sans-serif; color: #e2e8f0;
            max-width: 700px; margin: 0 auto; position: relative;
          }
          #ritmGame .rg-hdr {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 8px;
          }
          #ritmGame .rg-hdr h3 { font-size: 1.05rem; color: #fbbf24; }
          #ritmGame .rg-stats {
            display: flex; gap: 10px; font-size: 0.78rem;
          }
          #ritmGame .rg-stats span { padding: 3px 10px; border-radius: 8px; background: #1e293b; }
          #ritmGame canvas {
            display: block; margin: 0 auto 8px; border-radius: 10px;
            border: 1px solid #334155;
          }
          #ritmGame .rg-keys {
            display: flex; justify-content: center; gap: 16px; margin-bottom: 6px;
          }
          #ritmGame .rg-keys button {
            width: 64px; height: 48px; border: 2px solid #334155; border-radius: 10px;
            font-size: 1rem; font-weight: 800; cursor: pointer;
            transition: all 0.1s; color: #fff;
          }
          #ritmGame .rg-keys button:active, #ritmGame .rg-keys button.hit {
            transform: scale(0.92); filter: brightness(1.5);
          }
          #ritmGame .rg-keys .k0 { background: #dc2626; }
          #ritmGame .rg-keys .k1 { background: #2563eb; }
          #ritmGame .rg-keys .k2 { background: #16a34a; }
          #ritmGame .rg-keys .k3 { background: #ca8a04; }
          #ritmGame .rg-msg {
            text-align: center; font-size: 0.85rem; min-height: 22px; font-weight: 600;
          }
          #ritmGame .rg-ctrl {
            display: flex; justify-content: center; gap: 10px; margin-bottom: 8px;
          }
          #ritmGame .rg-ctrl button {
            padding: 6px 16px; border-radius: 8px; border: 1px solid #475569;
            background: #1e293b; color: #e2e8f0; font-size: 0.8rem;
            cursor: pointer; font-weight: 600;
          }
          #ritmGame .rg-ctrl button.active { border-color: #fbbf24; color: #fbbf24; }
          #ritmGame .rg-replay {
            display: none; margin: 8px auto 0; padding: 10px 28px;
            border: none; border-radius: 10px; cursor: pointer;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white; font-size: 0.95rem; font-weight: 700;
          }
        </style>
        <div id="ritmGame">
          <div class="rg-hdr">
            <h3>Ritim Oyunu</h3>
            <div class="rg-stats">
              <span id="rgScore" style="color:#fbbf24">Puan: 0</span>
              <span id="rgCombo" style="color:#a78bfa">Kombo: 0</span>
              <span id="rgAcc" style="color:#4ade80">Isabetlilik: -</span>
            </div>
          </div>
          <div class="rg-ctrl">
            <button id="rgSlow" class="active" onclick="rgSetTempo(0)">Yavas</button>
            <button id="rgMed" onclick="rgSetTempo(1)">Orta</button>
            <button id="rgFast" onclick="rgSetTempo(2)">Hizli</button>
          </div>
          <canvas id="rgCanvas" width="660" height="360"></canvas>
          <div class="rg-keys" id="rgKeys">
            <button class="k0" onmousedown="rgHit(0)" ontouchstart="rgHit(0)">A</button>
            <button class="k1" onmousedown="rgHit(1)" ontouchstart="rgHit(1)">S</button>
            <button class="k2" onmousedown="rgHit(2)" ontouchstart="rgHit(2)">D</button>
            <button class="k3" onmousedown="rgHit(3)" ontouchstart="rgHit(3)">F</button>
          </div>
          <div class="rg-msg" id="rgMsg">A, S, D, F tuslarina bas veya butonlara tikla!</div>
          <button class="rg-replay" id="rgReplay" onclick="rgStart()">Tekrar Oyna</button>
        </div>
        <script>
        (function(){
          const W = 660, H = 360;
          const canvas = document.getElementById('rgCanvas');
          const ctx = canvas.getContext('2d');
          const msgEl = document.getElementById('rgMsg');
          const scoreEl = document.getElementById('rgScore');
          const comboEl = document.getElementById('rgCombo');
          const accEl = document.getElementById('rgAcc');
          const replayBtn = document.getElementById('rgReplay');
          const laneColors = ['#dc2626','#2563eb','#16a34a','#ca8a04'];
          const laneX = [132, 264, 396, 528]; // center x of 4 lanes
          const hitY = H - 40;
          const noteR = 18;

          let score=0, combo=0, maxCombo=0, perfects=0, goods=0, misses=0;
          let notes=[], running=false, animId=null, tempoIdx=0;
          let spawnTimer=0, patternIdx=0, songTime=0, totalNotes=0;

          // Patterns: arrays of [lane(0-3)] per beat, null=rest
          const patterns = [
            // simple 4/4
            [[0],[1],[2],[3],[0],[1],[2],[3],
             [0,2],[1,3],[0],[2],[1],[3],[0,2],[1,3]],
            // syncopated
            [[0],[null],[1],[0],[null],[2],[3],[null],
             [0,1],[null],[2,3],[null],[0],[1],[2],[3]],
            // complex
            [[0],[1],[0,2],[3],[1],[2,3],[0],[1,3],
             [0],[2],[1],[3],[0,1,2],[null],[3],[0,1,2,3]]
          ];

          const tempos = [1.8, 2.6, 3.6]; // pixels per frame speed
          const spawnIntervals = [48, 36, 26]; // frames between spawns

          function getSpeed() { return tempos[tempoIdx]; }
          function getInterval() { return spawnIntervals[tempoIdx]; }

          window.rgSetTempo = function(idx) {
            tempoIdx = idx;
            document.getElementById('rgSlow').className = idx===0?'active':'';
            document.getElementById('rgMed').className = idx===1?'active':'';
            document.getElementById('rgFast').className = idx===2?'active':'';
            if (!running) rgStart();
          };

          function spawnBeat() {
            let pat = patterns[Math.min(tempoIdx, patterns.length-1)];
            let beat = pat[patternIdx % pat.length];
            patternIdx++;
            if (!beat) return;
            beat.forEach(function(lane){
              notes.push({ lane: lane, y: -noteR, hit: false, missed: false });
              totalNotes++;
            });
          }

          function draw() {
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(0, 0, W, H);

            // lane lines
            ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1;
            for (let i = 0; i < 4; i++) {
              ctx.beginPath();
              ctx.moveTo(laneX[i], 0);
              ctx.lineTo(laneX[i], H);
              ctx.stroke();
            }

            // hit zone
            ctx.fillStyle = 'rgba(255,255,255,0.04)';
            ctx.fillRect(0, hitY - 24, W, 48);
            ctx.strokeStyle = '#475569'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(0, hitY); ctx.lineTo(W, hitY); ctx.stroke();

            // lane labels at bottom
            ctx.font = 'bold 14px sans-serif'; ctx.textAlign = 'center';
            for (let i = 0; i < 4; i++) {
              ctx.fillStyle = laneColors[i] + '60';
              ctx.fillText(['A','S','D','F'][i], laneX[i], H - 6);
            }

            // notes
            notes.forEach(function(n){
              if (n.hit || n.missed) return;
              ctx.beginPath();
              ctx.arc(laneX[n.lane], n.y, noteR, 0, Math.PI*2);
              ctx.fillStyle = laneColors[n.lane];
              ctx.fill();
              // glow
              ctx.shadowColor = laneColors[n.lane];
              ctx.shadowBlur = 12;
              ctx.beginPath();
              ctx.arc(laneX[n.lane], n.y, noteR-4, 0, Math.PI*2);
              ctx.fillStyle = laneColors[n.lane] + 'aa';
              ctx.fill();
              ctx.shadowBlur = 0;
            });
          }

          function showHitFx(lane, text, color) {
            msgEl.style.color = color;
            msgEl.textContent = text + (combo > 1 ? ' (x' + combo + ' Kombo!)' : '');
            // glow on button
            let btns = document.querySelectorAll('#rgKeys button');
            btns[lane].classList.add('hit');
            setTimeout(function(){ btns[lane].classList.remove('hit'); }, 120);
          }

          window.rgHit = function(lane) {
            if (!running) return;
            let best = null, bestDist = 999;
            notes.forEach(function(n){
              if (n.hit || n.missed || n.lane !== lane) return;
              let d = Math.abs(n.y - hitY);
              if (d < bestDist) { bestDist = d; best = n; }
            });
            if (best && bestDist < 50) {
              best.hit = true;
              if (bestDist < 20) {
                score += 100 * (1 + combo * 0.1);
                combo++; perfects++;
                showHitFx(lane, 'Mukemmel!', '#4ade80');
              } else {
                score += 50 * (1 + combo * 0.05);
                combo++; goods++;
                showHitFx(lane, 'Iyi!', '#fbbf24');
              }
              if (combo > maxCombo) maxCombo = combo;
            } else {
              combo = 0;
              showHitFx(lane, 'Bos!', '#64748b');
            }
            updateUI();
          };

          function updateUI() {
            scoreEl.textContent = 'Puan: ' + Math.round(score);
            comboEl.textContent = 'Kombo: ' + combo;
            let total = perfects + goods + misses;
            let pct = total > 0 ? Math.round((perfects+goods)/total*100) : 0;
            accEl.textContent = 'Isabetlilik: %' + pct;
          }

          function update() {
            if (!running) return;
            spawnTimer++;
            if (spawnTimer >= getInterval()) {
              spawnTimer = 0;
              spawnBeat();
            }
            songTime++;

            let speed = getSpeed();
            notes.forEach(function(n){
              if (n.hit || n.missed) return;
              n.y += speed;
              if (n.y > hitY + 50) {
                n.missed = true; misses++; combo = 0;
                msgEl.style.color = '#f87171';
                msgEl.textContent = 'Kacirdin!';
                // shake
                canvas.style.transform = 'translateX(-3px)';
                setTimeout(function(){ canvas.style.transform = 'translateX(3px)'; }, 50);
                setTimeout(function(){ canvas.style.transform = ''; }, 100);
                updateUI();
              }
            });

            // remove old notes
            notes = notes.filter(function(n){ return !(n.hit && n.y > H+30) && !(n.missed && n.y > H+30); });

            // end after ~200 spawns worth or 60 seconds worth of frames
            if (songTime > 3600) {
              endGame(); return;
            }

            draw();
            animId = requestAnimationFrame(update);
          }

          function endGame() {
            running = false;
            cancelAnimationFrame(animId);
            draw();
            let total = perfects + goods + misses;
            let pct = total > 0 ? Math.round((perfects+goods)/total*100) : 0;
            msgEl.style.color = '#fbbf24';
            msgEl.textContent = 'Oyun Bitti! Puan: ' + Math.round(score) + ' | Maks Kombo: ' + maxCombo + ' | Isabetlilik: %' + pct;
            replayBtn.style.display = 'block';
          }

          // keyboard support
          document.addEventListener('keydown', function(e){
            if (e.repeat) return;
            var map = {a:0, s:1, d:2, f:3};
            var lane = map[e.key.toLowerCase()];
            if (lane !== undefined) rgHit(lane);
          });

          window.rgStart = function() {
            score=0; combo=0; maxCombo=0; perfects=0; goods=0; misses=0;
            notes=[]; spawnTimer=0; patternIdx=0; songTime=0; totalNotes=0;
            running=true;
            replayBtn.style.display='none';
            msgEl.textContent='Hazir ol... Notalar geliyor!';
            updateUI();
            cancelAnimationFrame(animId);
            animId = requestAnimationFrame(update);
          };

          rgStart();
        })();
        </script>
        """
        components.html(ritim_html, height=620)


# ═══════════════════════════════════════════════════════════════
# 6) YARATICI YAZARLIK
# ═══════════════════════════════════════════════════════════════

def _render_yazarlik():
    styled_section("✍️ Yaratıcı Yazarlık Atölyesi", "#8b5cf6")

    sub = st.tabs(["📝 Hikaye Başlatıcı", "🎭 Şiir Atölyesi", "📖 Masal Oluşturucu"])

    with sub[0]:
        styled_section("📝 Hikaye Başlatıcı", "#6366f1")
        baslangiçlar = [
            "Bir sabah uyandığında kendini bambaşka bir dünyada buldu...",
            "Eski bir sandık açtığında içinden parlak bir ışık yayıldı...",
            "Okul bahçesinde kimsenin görmediği gizli bir kapı keşfetti...",
            "Konuşan bir kedi ona yaklaştı ve 'Seni bekliyordum' dedi...",
            "Zaman makinesi çalışmaya başladığında düğmeler kendiliğinden hareket etti...",
            "Denizin altından gelen sesler her gece biraz daha yakınlaşıyordu...",
            "Haritada işaretli X noktasına vardığında gördüğü şey onu şaşırttı...",
            "Büyükbabasının günlüğünün son sayfasında şifreli bir mesaj vardı...",
        ]
        if st.button("🎲 Rastgele Başlangıç!", key="snt_hikaye_rnd", type="primary"):
            st.session_state["snt_hikaye_start"] = random.choice(baslangiçlar)

        baslangic = st.session_state.get("snt_hikaye_start", baslangiçlar[0])
        _render_html(f"""
        <div style="background:#0f172a;border-radius:14px;padding:18px;margin:12px 0;
                     border-left:4px solid #6366f1;font-style:italic;color:#c4b5fd !important;font-size:0.95rem;line-height:1.6">
            "{baslangic}"
        </div>
        """)
        st.text_area("Devamını yaz! ✍️", height=200, key="snt_hikaye_devam",
                      placeholder="Hikayeyi buradan devam ettir...")

    with sub[1]:
        styled_section("🎭 Şiir Atölyesi", "#ec4899")
        tur = st.selectbox("Şiir Türü", ["Serbest", "Kafiyeli (AABB)", "Haiku (5-7-5)"], key="snt_siir_tur")
        if tur == "Haiku (5-7-5)":
            st.info("Haiku: 3 satır — 5 hece, 7 hece, 5 hece. Doğa temalı!")
            st.text_input("1. satır (5 hece):", key="snt_h1", placeholder="Yaprak düşerken")
            st.text_input("2. satır (7 hece):", key="snt_h2", placeholder="Rüzgar fısıldar bana")
            st.text_input("3. satır (5 hece):", key="snt_h3", placeholder="Sonbahar geldi")
        else:
            st.text_area("Şiirini yaz! 🎭", height=200, key="snt_siir",
                          placeholder="Şiirini buraya yaz...")

    with sub[2]:
        styled_section("📖 Masal Oluşturucu", "#f59e0b")
        col1, col2, col3 = st.columns(3)
        with col1:
            kahraman = st.selectbox("Kahraman", ["🧒 Küçük çocuk","🦊 Tilki","🐉 Ejderha","👸 Prenses","🧙 Büyücü","🤖 Robot"], key="snt_masal_k")
        with col2:
            mekan = st.selectbox("Mekan", ["🏰 Kale","🌲 Orman","🌊 Deniz","🚀 Uzay","🏔️ Dağ","🏙️ Şehir"], key="snt_masal_m")
        with col3:
            gorev = st.selectbox("Görev", ["💎 Hazine bul","🗝️ Kapıyı aç","🐲 Canavarı yen","⭐ Yıldızı kurtar","📜 Sırrı çöz"], key="snt_masal_g")

        if st.button("📖 Masal Başlat!", key="snt_masal_go", type="primary"):
            k = kahraman.split(" ", 1)[1]
            m = mekan.split(" ", 1)[1]
            g = gorev.split(" ", 1)[1]
            masal = f"Bir varmış bir yokmuş, uzak diyarlarda bir {k} yaşarmış. {m}'de geçen günlerinde bir gün büyük bir görev almış: {g}! Bu tehlikeli yolculuğa çıkmaya karar vermiş..."
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:16px;padding:20px;margin:12px 0;
                         border:2px solid rgba(245,158,11,0.3)">
                <div style="font-size:1.5rem;margin-bottom:8px;text-align:center">📖✨</div>
                <div style="color:#fde68a !important;font-size:0.9rem;line-height:1.7;font-style:italic">{masal}</div>
            </div>
            """)
            st.text_area("Devamını sen yaz!", height=150, key="snt_masal_devam")


# ═══════════════════════════════════════════════════════════════
# 7) KOMPOZİSYON
# ═══════════════════════════════════════════════════════════════

def _render_kompozisyon():
    styled_section("📸 Fotoğraf & Kompozisyon", "#06b6d4")

    sub = st.tabs(["📐 Altın Oran", "📏 Üçte Bir Kuralı", "🔍 Perspektif"])

    with sub[0]:
        styled_section("📐 Altın Oran (φ = 1.618)", "#eab308")
        _render_html("""
        <div style="background:#0f172a;border-radius:16px;padding:20px;margin:12px 0;border:1px solid rgba(234,179,8,0.2)">
            <div style="font-size:1rem;color:#fde68a !important;font-weight:700;margin-bottom:12px">Altın Oran Nedir?</div>
            <div style="color:#94a3b8 !important;font-size:0.85rem;line-height:1.6">
                φ = 1.618... — Doğanın güzellik formülü! Mona Lisa, Parthenon, deniz kabuğu,
                kredi kartı boyutları — hepsi altın oranı kullanır.<br><br>
                <b>Fotoğrafta kullanımı:</b> Ana konuyu çerçevenin altın oran noktasına yerleştir
                (kenardan %38 mesafe). Tam ortaya koyma!
            </div>
        </div>
        """)

    with sub[1]:
        styled_section("📏 Üçte Bir Kuralı", "#10b981")
        _render_html("""
        <div style="background:#0f172a;border-radius:16px;padding:20px;margin:12px 0;border:1px solid rgba(16,185,129,0.2)">
            <div style="font-size:1rem;color:#86efac !important;font-weight:700;margin-bottom:12px">Üçte Bir Kuralı</div>
            <div style="color:#94a3b8 !important;font-size:0.85rem;line-height:1.6">
                Çerçeveyi yatay ve dikey 3'e böl (9 eşit kare). Ana konuyu kesişim noktalarından birine yerleştir.<br><br>
                <b>Neden işe yarar?</b> İnsan gözü doğal olarak bu noktalara bakar.
                Tam orta sıkıcıdır, üçte bir noktaları dinamik ve çekicidir.
            </div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:12px;max-width:300px">
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
                <div style="background:#1e293b;height:60px;border-radius:4px;border:2px solid #10b981;display:flex;align-items:center;justify-content:center">
                    <span style="color:#10b981 !important;font-weight:700">🎯</span>
                </div>
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
                <div style="background:#1e293b;height:60px;border-radius:4px"></div>
            </div>
        </div>
        """)

    with sub[2]:
        styled_section("🔍 Perspektif", "#8b5cf6")
        _render_html("""
        <div style="background:#0f172a;border-radius:16px;padding:20px;margin:12px 0;border:1px solid rgba(139,92,246,0.2)">
            <div style="font-size:1rem;color:#e9d5ff !important;font-weight:700;margin-bottom:12px">Perspektif Nedir?</div>
            <div style="color:#94a3b8 !important;font-size:0.85rem;line-height:1.6">
                3 boyutlu dünyayı 2 boyutlu yüzeyde gösterme tekniği.<br><br>
                <b>Tek Nokta Perspektifi:</b> Tüm çizgiler ufuk çizgisinde tek bir noktada birleşir (yol, koridor).<br>
                <b>İki Nokta Perspektifi:</b> İki kaçış noktası — köşeden görülen binalar.<br>
                <b>Atmosferik Perspektif:</b> Uzaktaki nesneler daha soluk ve mavimsi görünür.
            </div>
        </div>
        """)


# ═══════════════════════════════════════════════════════════════
# 8) SANAT MÜZESİ
# ═══════════════════════════════════════════════════════════════

def _render_muze():
    styled_section("🏛️ Sanat Müzesi", "#6366f1")

    sub = st.tabs(["🖼️ Ressamlar Galerisi", "📜 Sanat Akımları", "📚 Sanat Sözlüğü", "🧩 Yapboz Oyunu", "⏳ Zaman Cizelgesi", "🏛️ Sanal Galeri Turu"])

    with sub[0]:
        styled_section("🖼️ Ünlü Ressamlar & Eserleri", "#ec4899")
        for r in UNLU_RESSAMLAR:
            img = f'<img src="{r["portre_url"]}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #8b5cf6" onerror="this.style.display=\'none\'">' if r.get("portre_url") else f'<div style="font-size:3rem">{r["ikon"]}</div>'
            _render_html(f"""
            <div class="snt-card" style="display:flex;gap:20px;align-items:center">
                <div style="min-width:80px;text-align:center">{img}</div>
                <div style="flex:1">
                    <div style="font-weight:700;color:#e9d5ff !important;font-size:1.1rem">{r['ad']}</div>
                    <div style="font-size:0.78rem;color:#c084fc !important">{r.get('akım','')} • {r['yasam']} • {r['ulke']}</div>
                    <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:4px;font-style:italic">{r.get('bilgi','')[:100]}...</div>
                </div>
            </div>
            """)
            with st.expander(f"🖼️ {r['ad']} — Eserleri & Biyografi", expanded=False):
                st.markdown(r.get("bilgi", ""))

                # Eserler galerisi
                eserler = r.get("eserler", [])
                if eserler:
                    st.markdown("### 🖼️ Başlıca Eserleri")
                    for eser in eserler:
                        eser_img = ""
                        if eser.get("url"):
                            eser_img = f'<img src="{eser["url"]}" style="width:100%;max-width:400px;border-radius:12px;border:2px solid #334155;margin:8px 0" onerror="this.style.display=\'none\'">'

                        _render_html(f"""
                        <div style="background:#0f172a;border-radius:14px;padding:16px;margin-bottom:12px;
                                     border:1px solid rgba(99,102,241,0.15)">
                            <div style="font-weight:700;color:#e0e7ff !important;font-size:1rem;margin-bottom:4px">{eser['ad']} ({eser['yil']})</div>
                            <div style="font-size:0.75rem;color:#94a3b8 !important;margin-bottom:8px">
                                {eser['tur']} • {eser['boyut']} • 📍 {eser['konum']}
                            </div>
                            {eser_img}
                            <div style="font-size:0.83rem;color:#c4b5fd !important;line-height:1.5;margin-top:6px">{eser['aciklama']}</div>
                        </div>
                        """)

    with sub[1]:
        styled_section("📜 Sanat Akımları Tarihçesi", "#f59e0b")
        for i, a in enumerate(SANAT_AKIMLARI):
            _render_html(f"""
            <div style="display:flex;gap:16px;align-items:center;margin-bottom:8px;padding:10px 16px;
                         background:#0f172a;border-radius:12px;border-left:4px solid {'#eab308' if i%2==0 else '#8b5cf6'}">
                <div style="font-size:1.8rem">{a['ikon']}</div>
                <div>
                    <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{a['ad']} <span style="color:#94a3b8 !important;font-weight:400;font-size:0.75rem">({a['yil']})</span></div>
                    <div style="font-size:0.8rem;color:#94a3b8 !important">{a['ozellik']}</div>
                </div>
            </div>
            """)

    with sub[2]:
        styled_section("📚 Sanat Terimleri Sözlüğü", "#3b82f6")
        arama = st.text_input("🔍 Terim Ara", key="snt_sz_ara")
        for harf, terimler in SANAT_SOZLUGU.items():
            filtered = terimler
            if arama:
                filtered = [t for t in terimler if arama.lower() in t[0].lower() or arama.lower() in t[1].lower()]
            if not filtered:
                continue
            styled_section(f"📖 {harf}", "#3b82f6")
            for ad, aciklama in filtered:
                _render_html(f"""
                <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:4px;border-left:3px solid #3b82f6">
                    <span style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</span>
                    <span style="color:#94a3b8 !important;font-size:0.8rem;margin-left:8px">— {aciklama}</span>
                </div>
                """)

    with sub[3]:
        _render_tablo_puzzle()

    with sub[4]:
        _render_sanat_zamancipizelgesi()

    with sub[5]:
        _render_sanal_muze()


# ═══════════════════════════════════════════════════════════════
# 8b) TABLO PUZZLE OYUNU
# ═══════════════════════════════════════════════════════════════

def _render_tablo_puzzle():
    """Unlu tablolarin parcalara bolunup birlestirildigi yapboz oyunu."""
    styled_section("🧩 Tablo Puzzle Oyunu", "#8b5cf6")

    _render_html("""
    <div style="background:linear-gradient(135deg,#8b5cf615,#8b5cf608);border-radius:14px;padding:14px 18px;
                 margin-bottom:16px;border:1px solid rgba(139,92,246,0.3)">
        <div style="font-weight:700;color:#c4b5fd !important;font-size:0.9rem">Nasil Oynanir?</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            Unlu tablolar 3x3 parcaya bolundu! Iki parcaya tiklayarak yerlerini degistir.
            Tum parcalari dogru siraya koy ve tabloyu tamamla.
        </div>
    </div>
    """)

    import streamlit.components.v1 as components

    puzzle_html = """
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0f172a; font-family: 'Segoe UI', sans-serif; color: #e2e8f0; padding: 12px; }

.top-bar { display: flex; gap: 12px; align-items: center; margin-bottom: 14px; flex-wrap: wrap; }
.top-bar select {
    background: #1e293b; color: #e2e8f0; border: 1px solid #475569; border-radius: 8px;
    padding: 8px 12px; font-size: 0.85rem; cursor: pointer; flex: 1; min-width: 180px;
}
.btn {
    background: linear-gradient(135deg, #7c3aed, #6d28d9); color: #fff; border: none;
    border-radius: 8px; padding: 8px 18px; cursor: pointer; font-size: 0.85rem; font-weight: 600;
    transition: all 0.2s;
}
.btn:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(124,58,237,0.3); }

.stats {
    display: flex; gap: 16px; margin-bottom: 14px; flex-wrap: wrap;
}
.stat-box {
    background: #1e293b; border-radius: 10px; padding: 8px 14px;
    border: 1px solid #334155; flex: 1; min-width: 100px; text-align: center;
}
.stat-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-val { font-size: 1.2rem; font-weight: 700; color: #a78bfa; margin-top: 2px; }

.grid-container {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px;
    width: 330px; height: 330px; margin: 0 auto; border-radius: 12px; overflow: hidden;
    border: 3px solid #475569; background: #1e293b;
}
.cell {
    cursor: pointer; position: relative; transition: all 0.2s;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.75rem; color: rgba(255,255,255,0.4);
}
.cell:hover { opacity: 0.85; transform: scale(0.96); }
.cell.selected { box-shadow: inset 0 0 0 3px #facc15; transform: scale(0.93); }

.win-banner {
    display: none; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px;
    padding: 16px; text-align: center; margin-top: 14px; animation: popIn 0.4s ease;
}
.win-banner.show { display: block; }
@keyframes popIn { from { transform: scale(0.8); opacity:0; } to { transform: scale(1); opacity:1; } }
.win-title { font-size: 1.3rem; font-weight: 700; color: #fff; }
.win-sub { font-size: 0.85rem; color: #d1fae5; margin-top: 4px; }
</style>
</head>
<body>

<div class="top-bar">
    <select id="paintSel" onchange="initPuzzle()">
        <option value="0">Yildizli Gece - Van Gogh</option>
        <option value="1">Mona Lisa - Da Vinci</option>
        <option value="2">Cicekler - Monet</option>
        <option value="3">Gece Nobleti - Hopper</option>
        <option value="4">Kompozisyon - Mondrian</option>
    </select>
    <button class="btn" onclick="shufflePuzzle()">Karistir</button>
    <button class="btn" style="background:linear-gradient(135deg,#10b981,#059669)" onclick="solvePuzzle()">Coz</button>
</div>

<div class="stats">
    <div class="stat-box"><div class="stat-label">Hamle</div><div class="stat-val" id="moveCount">0</div></div>
    <div class="stat-box"><div class="stat-label">Sure</div><div class="stat-val" id="timer">00:00</div></div>
    <div class="stat-box"><div class="stat-label">Durum</div><div class="stat-val" id="status">Basladi</div></div>
</div>

<div class="grid-container" id="grid"></div>
<div class="win-banner" id="winBanner">
    <div class="win-title">Tebrikler! Tabloyu Tamamladin!</div>
    <div class="win-sub" id="winSub"></div>
</div>

<script>
const paintings = [
    { name:"Yildizli Gece", colors:[
        "linear-gradient(135deg,#1e3a5f,#2563eb)","linear-gradient(135deg,#1e40af,#fbbf24)","linear-gradient(135deg,#1e3a5f,#3b82f6)",
        "linear-gradient(135deg,#fbbf24,#1e3a5f)","linear-gradient(135deg,#2563eb,#fbbf24)","linear-gradient(135deg,#1e40af,#eab308)",
        "linear-gradient(135deg,#1a2744,#1e40af)","linear-gradient(135deg,#1a2744,#2563eb)","linear-gradient(135deg,#0f172a,#1e3a5f)"
    ]},
    { name:"Mona Lisa", colors:[
        "linear-gradient(135deg,#5b3a1a,#7c5e3c)","linear-gradient(135deg,#6b4e2a,#8b7355)","linear-gradient(135deg,#4a6741,#5b7a52)",
        "linear-gradient(135deg,#8b6f47,#c9a96e)","linear-gradient(135deg,#d4b896,#e8d5b7)","linear-gradient(135deg,#6b7c5a,#4a6741)",
        "linear-gradient(135deg,#3d2b1a,#5b3a1a)","linear-gradient(135deg,#4a3520,#6b4e2a)","linear-gradient(135deg,#2c1f10,#3d2b1a)"
    ]},
    { name:"Cicekler", colors:[
        "linear-gradient(135deg,#7c3aed,#a855f7)","linear-gradient(135deg,#c084fc,#e879f9)","linear-gradient(135deg,#34d399,#6ee7b7)",
        "linear-gradient(135deg,#a855f7,#f472b6)","linear-gradient(135deg,#10b981,#34d399)","linear-gradient(135deg,#d946ef,#a855f7)",
        "linear-gradient(135deg,#059669,#10b981)","linear-gradient(135deg,#047857,#059669)","linear-gradient(135deg,#064e3b,#047857)"
    ]},
    { name:"Gece Nobleti", colors:[
        "linear-gradient(135deg,#0c1222,#1e293b)","linear-gradient(135deg,#1e293b,#334155)","linear-gradient(135deg,#0c1222,#162032)",
        "linear-gradient(135deg,#162032,#1e293b)","linear-gradient(135deg,#fbbf24,#f59e0b)","linear-gradient(135deg,#1e293b,#0c1222)",
        "linear-gradient(135deg,#0f172a,#162032)","linear-gradient(135deg,#162032,#0c1222)","linear-gradient(135deg,#0a0f1a,#0c1222)"
    ]},
    { name:"Kompozisyon", colors:[
        "linear-gradient(135deg,#ef4444,#dc2626)","linear-gradient(135deg,#f8fafc,#e2e8f0)","linear-gradient(135deg,#2563eb,#1d4ed8)",
        "linear-gradient(135deg,#f8fafc,#e2e8f0)","linear-gradient(135deg,#fbbf24,#f59e0b)","linear-gradient(135deg,#0f172a,#1e293b)",
        "linear-gradient(135deg,#f8fafc,#e2e8f0)","linear-gradient(135deg,#0f172a,#1e293b)","linear-gradient(135deg,#2563eb,#3b82f6)"
    ]}
];

let order = [0,1,2,3,4,5,6,7,8];
let selected = -1;
let moves = 0;
let timerInt = null;
let seconds = 0;
let solved = false;

function initPuzzle() {
    order = [0,1,2,3,4,5,6,7,8];
    selected = -1; moves = 0; seconds = 0; solved = false;
    clearInterval(timerInt);
    document.getElementById('moveCount').textContent = '0';
    document.getElementById('timer').textContent = '00:00';
    document.getElementById('status').textContent = 'Hazir';
    document.getElementById('winBanner').classList.remove('show');
    renderGrid();
}

function renderGrid() {
    const idx = parseInt(document.getElementById('paintSel').value);
    const p = paintings[idx];
    const g = document.getElementById('grid');
    g.innerHTML = '';
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell' + (i === selected ? ' selected' : '');
        cell.style.background = p.colors[order[i]];
        cell.textContent = (order[i]+1);
        cell.onclick = () => clickCell(i);
        g.appendChild(cell);
    }
}

function clickCell(i) {
    if (solved) return;
    if (selected === -1) {
        selected = i;
        renderGrid();
    } else {
        if (selected === i) { selected = -1; renderGrid(); return; }
        [order[selected], order[i]] = [order[i], order[selected]];
        selected = -1;
        moves++;
        if (moves === 1) startTimer();
        document.getElementById('moveCount').textContent = moves;
        renderGrid();
        checkWin();
    }
}

function shufflePuzzle() {
    solved = false;
    document.getElementById('winBanner').classList.remove('show');
    for (let i = 8; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [order[i], order[j]] = [order[j], order[i]];
    }
    if (order.every((v,i) => v===i)) { [order[0], order[8]] = [order[8], order[0]]; }
    moves = 0; seconds = 0; selected = -1;
    clearInterval(timerInt);
    document.getElementById('moveCount').textContent = '0';
    document.getElementById('timer').textContent = '00:00';
    document.getElementById('status').textContent = 'Oynaniyor';
    renderGrid();
}

function solvePuzzle() {
    order = [0,1,2,3,4,5,6,7,8];
    solved = true; selected = -1;
    clearInterval(timerInt);
    document.getElementById('status').textContent = 'Cozuldu';
    renderGrid();
}

function startTimer() {
    clearInterval(timerInt);
    seconds = 0;
    timerInt = setInterval(() => {
        seconds++;
        const m = String(Math.floor(seconds/60)).padStart(2,'0');
        const s = String(seconds%60).padStart(2,'0');
        document.getElementById('timer').textContent = m+':'+s;
    }, 1000);
}

function checkWin() {
    if (order.every((v,i) => v===i)) {
        solved = true;
        clearInterval(timerInt);
        document.getElementById('status').textContent = 'Kazandin!';
        const m = Math.floor(seconds/60);
        const s = seconds%60;
        document.getElementById('winSub').textContent = moves + ' hamle, ' + m + ' dk ' + s + ' sn';
        document.getElementById('winBanner').classList.add('show');
    }
}

initPuzzle();
</script>
</body>
</html>
"""
    components.html(puzzle_html, height=500)


# ═══════════════════════════════════════════════════════════════
# 8c) SANAT TARIHI ZAMAN CIZELGESI
# ═══════════════════════════════════════════════════════════════

def _render_sanat_zamancipizelgesi():
    """Interaktif sanat tarihi zaman cizelgesi."""
    styled_section("⏳ Sanat Tarihi Zaman Cizelgesi", "#f59e0b")

    _render_html("""
    <div style="background:linear-gradient(135deg,#f59e0b15,#f59e0b08);border-radius:14px;padding:14px 18px;
                 margin-bottom:16px;border:1px solid rgba(245,158,11,0.3)">
        <div style="font-weight:700;color:#fde68a !important;font-size:0.9rem">Sanat Tarihinde Yolculuk</div>
        <div style="color:#94a3b8 !important;font-size:0.83rem;margin-top:4px">
            Magara resimlerinden modern sanata: 40.000 yillik sanat yolculugunu kesfedin.
            Saga kaydir ve her donemi incele!
        </div>
    </div>
    """)

    periods = [
        ("Magara Sanati", "MO 40.000", "#b45309", "Ilk insanlar", "Lascaux, Altamira", "Avcilarin duvar resimleri, el izleri ve hayvan figürleri. Insanligin bilinen en eski sanat eserleri."),
        ("Antik Misir", "MO 3000", "#d97706", "Misirlilar", "Piramitler, Sfenks", "Hiyeroglif, anit mezarlar ve tanri heykelleri. Olum sonrasi yasam inancinin sanata yansimasi."),
        ("Antik Yunan", "MO 800", "#ea580c", "Fidias, Praksiteles", "Parthenon, Venüs", "Ideal insan vucudu, heykeltrasilik, seramik. Demokrasi ve felsefenin sanata etkisi."),
        ("Roma", "MO 500 - MS 400", "#dc2626", "Roma ustalari", "Kolezyum, Mozaikler", "Buyuk yapilar, mozaikler, portre busrleri. Yunan sanatinin gelismis devami."),
        ("Bizans", "330 - 1453", "#e11d48", "Anonim ustalar", "Ayasofya, Ikonalar", "Dini ikonalar, altin mozaikler, kubbeii yapilar. Dogu ve Bati sentezi."),
        ("Gotik", "1100 - 1500", "#be185d", "Katedral ustalari", "Notre-Dame", "Sivri kemerler, vitray pencereler, yukselis. Isik ve gogun yeryuzune inisi."),
        ("Ronesans", "1400 - 1600", "#7c3aed", "Da Vinci, Michelangelo", "Mona Lisa, Sistine", "Insan merkezli sanat, perspektif, anatomi. Antik Yunan ideallerinin yeniden dogmasi."),
        ("Barok", "1600 - 1750", "#6d28d9", "Caravaggio, Rembrandt", "Gece Nobleti", "Dramatik isik-golge, hareket, duygu. Kilisenin gucu ve kralik ihtisami."),
        ("Rokoko", "1720 - 1780", "#5b21b6", "Boucher, Fragonard", "Salincak", "Pastel renkler, zarafet, asirilik. Aristokrasinin senligi ve oyunculugu."),
        ("Neoklasizm", "1750 - 1850", "#4338ca", "David, Ingres", "Napolyon", "Antik Yunan/Roma'ya donus, ciddiyet, ahlak. Akil caginin sanata yansimasi."),
        ("Romantizm", "1800 - 1850", "#3b82f6", "Delacroix, Turner", "Ozgurluk", "Duygu, doga, bireysellik. Sanayi devrimine karsi doganin yuceltilmesi."),
        ("Empresyonizm", "1860 - 1900", "#0ea5e9", "Monet, Renoir", "Nilüferler", "Isik ve renk, an'in yakalanmasi, dis mekan. Fotografin sanati donustürmesi."),
        ("Ekspresyonizm", "1905 - 1930", "#06b6d4", "Munch, Kirchner", "Ciglik", "Ic dunya, kaygi, carpitma. Sanayi toplumunun bunalimi ve savas korkusu."),
        ("Kubizm", "1907 - 1920", "#14b8a6", "Picasso, Braque", "Avignonlu Kizlar", "Coklu bakis acisi, geometrik parcalanma. Gercekligin yeniden yapilandirilmasi."),
        ("Modern Sanat", "1900 - Gunumuz", "#10b981", "Warhol, Pollock", "Campbell Corba", "Sinirsiz ifade, kavramsal sanat, dijital. Her sey sanat olabilir mi sorusu."),
    ]

    cards_html = ""
    for i, (name, dates, color, artists, artwork, desc) in enumerate(periods):
        arrow = '<div style="min-width:40px;display:flex;align-items:center;justify-content:center;color:#475569;font-size:1.4rem">&#10132;</div>' if i < len(periods)-1 else ''
        cards_html += f"""
        <div style="display:flex;align-items:stretch;flex-shrink:0">
            <div style="min-width:220px;max-width:220px;background:linear-gradient(180deg,{color}22,#0f172a);
                         border-radius:14px;padding:16px;border:1px solid {color}55;
                         display:flex;flex-direction:column;gap:6px">
                <div style="background:{color};color:#fff;border-radius:8px;padding:4px 10px;
                             font-size:0.7rem;font-weight:700;text-align:center;letter-spacing:0.5px">{dates}</div>
                <div style="font-weight:800;color:#e2e8f0;font-size:1rem;margin-top:4px">{name}</div>
                <div style="font-size:0.75rem;color:#94a3b8;line-height:1.5;flex:1">{desc}</div>
                <div style="border-top:1px solid {color}33;padding-top:6px;margin-top:4px">
                    <div style="font-size:0.7rem;color:{color};font-weight:600">Sanatcilar</div>
                    <div style="font-size:0.75rem;color:#cbd5e1">{artists}</div>
                </div>
                <div>
                    <div style="font-size:0.7rem;color:{color};font-weight:600">Onemli Eser</div>
                    <div style="font-size:0.75rem;color:#cbd5e1">{artwork}</div>
                </div>
            </div>
            {arrow}
        </div>
        """

    timeline_html = f"""
    <div style="position:relative">
        <div style="overflow-x:auto;padding:8px 0 16px 0;scrollbar-width:thin;scrollbar-color:#475569 #0f172a">
            <div style="display:flex;gap:0;align-items:stretch;min-width:max-content;padding:4px">
                {cards_html}
            </div>
        </div>
        <div style="text-align:center;margin-top:8px">
            <span style="color:#64748b;font-size:0.75rem">&#8592; Saga kaydir &#8594;</span>
        </div>
    </div>
    """

    _render_html(timeline_html)


# ═══════════════════════════════════════════════════════════════
# 9) EL SANATLARI
# ═══════════════════════════════════════════════════════════════

def _render_el_sanatlari():
    styled_section("✂️ El Sanatları Rehberi", "#ec4899")

    sub = st.tabs(["📄 Origami", "🎨 Kolaj Fikirleri", "🏺 Seramik Rehberi"])

    with sub[0]:
        styled_section("📄 Origami — Kağıt Katlama Sanatı", "#f97316")
        for proje in ORIGAMI_PROJELERI:
            with st.expander(f"{proje['ikon']} {proje['ad']} ({proje['zorluk']}) — Sınıf {proje['sinif']}"):
                for i, adim in enumerate(proje["adimlar"], 1):
                    st.markdown(f"**{i}.** {adim}")

    with sub[1]:
        styled_section("🎨 Kolaj Fikirleri", "#ec4899")
        fikirler = [
            ("🌍 Doğa Kolajı", "Yaprak, çiçek, dal toplayıp kağıda yapıştır"),
            ("📰 Gazete Kolajı", "Gazete/dergi kesip yeni bir sahne oluştur"),
            ("🎨 Renk Kolajı", "Tek rengin farklı tonlarından parçalar kes ve yapıştır"),
            ("📸 Fotoğraf Kolajı", "Eski fotoğraflardan bir hikaye anlat"),
            ("🧵 Kumaş Kolajı", "Farklı kumaş parçalarıyla doku oluştur"),
        ]
        for ad, aciklama in fikirler:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;
                         border-left:4px solid #ec4899">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</div>
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:2px">{aciklama}</div>
            </div>
            """)

    with sub[2]:
        styled_section("🏺 Seramik & Çömlekçilik", "#f59e0b")
        st.markdown("""
**Seramik Temelleri:**
1. **Kil hazırlama** — yoğurma ve hava kabarcıklarını çıkarma
2. **Şekillendirme** — elle veya çark üzerinde
3. **Kurutma** — yavaş ve eşit kuruma (çatlamasın!)
4. **Bisküvi pişirme** — 900-1000°C
5. **Sırlama** — renkli sır uygulama
6. **İkinci pişirme** — 1200-1300°C
7. **Sonuç** — parlak, renkli seramik! 🏺
        """)


# ═══════════════════════════════════════════════════════════════
# 10) YETENEK TESTİ
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
# 10) SİNEMA & ANİMASYON
# ═══════════════════════════════════════════════════════════════

def _render_sinema():
    styled_section("🎬 Sinema & Animasyon Dünyası", "#ef4444")

    sub = st.tabs(["🎥 Film Türleri", "🎞️ Animasyon", "🎬 Ünlü Yönetmenler"])

    with sub[0]:
        styled_section("🎥 Film Türleri", "#ef4444")
        turler = [
            ("🎭 Drama", "İnsan hikayelerini anlatan, duygu yoğun filmler", "Schindler'in Listesi, Forrest Gump"),
            ("😂 Komedi", "Güldürü amacıyla yapılan filmler", "Hababam Sınıfı, Mr. Bean"),
            ("🦸 Aksiyon", "Hızlı tempo, macera dolu filmler", "Indiana Jones, Matrix"),
            ("👻 Korku", "Gerilim ve korku yaratan filmler", "Psycho, The Shining"),
            ("🚀 Bilim Kurgu", "Gelecek ve teknolojiyi hayal eden filmler", "Yıldız Savaşları, Interstellar"),
            ("📝 Belgesel", "Gerçek olayları anlatan filmler", "Planet Earth, Free Solo"),
            ("🎨 Animasyon", "Çizgi/3D teknikle yapılan filmler", "Toy Story, Ruhun Göçü"),
            ("🤠 Western", "Vahşi Batı hikayeleri", "İyi Kötü Çirkin"),
        ]
        for ikon_ad, aciklama, ornekler in turler:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;border-left:4px solid #ef4444">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ikon_ad}</div>
                <div style="font-size:0.8rem;color:#94a3b8 !important">{aciklama}</div>
                <div style="font-size:0.75rem;color:#6366f1 !important;margin-top:2px">🎬 {ornekler}</div>
            </div>
            """)

    with sub[1]:
        styled_section("🎞️ Animasyon Temelleri", "#f59e0b")
        st.markdown("""
**Animasyon Nasıl Yapılır?**

1. **Geleneksel (2D):** Kare kare elle çizim. Disney klasikleri bu teknikle yapıldı.
2. **Stop Motion:** Nesneleri küçük adımlarla hareket ettirip fotoğraflama. Wallace & Gromit.
3. **3D CGI:** Bilgisayar ile modelleme. Pixar, DreamWorks.
4. **Rotoskopi:** Gerçek video üzerine çizim. A Scanner Darkly.
5. **Motion Capture:** Aktörün hareketini dijitale aktarma. Avatar.

**FPS (Kare/Saniye):**
- Film: 24 FPS
- TV: 30 FPS
- Oyun: 60 FPS
- Her saniyede 24 çizim = akıcı hareket!
        """)

    with sub[2]:
        styled_section("🎬 Ünlü Yönetmenler", "#8b5cf6")
        yonetmenler = [
            ("🎬 Alfred Hitchcock", "1899-1980", "İngiltere/ABD 🇬🇧", "Gerilim ustası. Psycho, Vertigo, Kuşlar. 'Suspense' türünün babası."),
            ("🎬 Stanley Kubrick", "1928-1999", "ABD 🇺🇸", "Mükemmeliyetçi dahi. 2001: Uzay Macerası, The Shining. Her sahneyi yüzlerce kez çekti."),
            ("🎬 Hayao Miyazaki", "1941-", "Japonya 🇯🇵", "Anime'nin efsanesi. Ruhların Kaçışı, Komşum Totoro. Studio Ghibli kurucusu."),
            ("🎬 Nuri Bilge Ceylan", "1959-", "Türkiye 🇹🇷", "Cannes Altın Palmiye! Kış Uykusu, Bir Zamanlar Anadolu'da. Türk sinemasının gururu."),
            ("🎬 Steven Spielberg", "1946-", "ABD 🇺🇸", "Gişe kralı. E.T., Jurassic Park, Schindler'in Listesi. Tarihin en çok hasılat yapan yönetmen."),
            ("🎬 Christopher Nolan", "1970-", "İngiltere 🇬🇧", "Zihin bükücü. Inception, Interstellar, Tenet. Zamanla oynamayı seviyor!"),
        ]
        for ad, yasam, ulke, bilgi in yonetmenler:
            with st.expander(f"{ad} ({yasam}) — {ulke}"):
                st.markdown(bilgi)


# ═══════════════════════════════════════════════════════════════
# 11) MİMARİ & TASARIM
# ═══════════════════════════════════════════════════════════════

def _render_mimari():
    styled_section("🏗️ Mimari & Tasarım", "#10b981")

    sub = st.tabs(["🏛️ Ünlü Yapılar", "👷 Ünlü Mimarlar", "📐 Mimari Akımlar"])

    with sub[0]:
        styled_section("🏛️ Dünyanın Harikası Yapılar", "#10b981")
        yapilar = [
            ("🕌 Ayasofya", "Istanbul, 537", "Bizans, Osmanli, Muze, Cami. 1000 yil dunyanin en buyuk katedraliydi! Kubbesi muhendislik harikasi.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Hagia_Sophia_%28228968325%29.jpeg/400px-Hagia_Sophia_%28228968325%29.jpeg",
             "Mimar: Anthemios & Isidoros | Kubbe capi: 31.87m | UNESCO"),
            ("🏛️ Parthenon", "Atina, MO 447", "Altin oran ile insa edildi. Sutunlari aslinda duz degil, hafifce kavisli (optik yanilsama duzeltmesi).",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/The_Parthenon_in_Athens.jpg/400px-The_Parthenon_in_Athens.jpg",
             "Mimar: Iktinos & Kallikrates | Dorik duzen | Athena tapinagi"),
            ("🗼 Eyfel Kulesi", "Paris, 1889", "Insaatina herkes karsi cikti! Demir canavar dediler. Bugun yilda 7 milyon ziyaretci.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/400px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg",
             "Muhendis: Gustave Eiffel | Yukseklik: 330m | 7.300 ton demir"),
            ("🕌 Selimiye Camii", "Edirne, 1575", "Mimar Sinan'in ustalik eseri. Kubbesi Ayasofya'dan genis! Kalfalik eserim Suleymaniye, ustalik eserim Selimiye dedi.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Selimiye_Mosque_%2815051985908%29_%28cropped%29.jpg/400px-Selimiye_Mosque_%2815051985908%29_%28cropped%29.jpg",
             "Mimar: Sinan | Kubbe capi: 31.28m | 4 minare, 3 serefe | UNESCO"),
            ("🏗️ Sagrada Familia", "Barselona, 1882-devam", "Gaudi basladi, hala bitirilmedi! 140+ yildir insaat. Dogadan ilham alan organik mimari.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/%CE%A3%CE%B1%CE%B3%CF%81%CE%AC%CE%B4%CE%B1_%CE%A6%CE%B1%CE%BC%CE%AF%CE%BB%CE%B9%CE%B1_2941.jpg/400px-%CE%A3%CE%B1%CE%B3%CF%81%CE%AC%CE%B4%CE%B1_%CE%A6%CE%B1%CE%BC%CE%AF%CE%BB%CE%B9%CE%B1_2941.jpg",
             "Mimar: Antoni Gaudi | Planlanan bitis: 2026 | 18 kule | UNESCO"),
            ("🏯 Taj Mahal", "Agra, 1653", "Sah Cihan esi Mumtaz Mahal icin yaptirdi. 22 yil, 20.000 isci. Askin aniti.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/400px-Taj_Mahal_%28Edited%29.jpeg",
             "Beyaz mermer | 4 minare | Mughal mimarisi | UNESCO"),
            ("🏛️ Colosseum", "Roma, 80", "50.000 seyirci kapasiteli amfitiyatro. Gladyator dovusleri icin yapildi. 2000 yillik muhendislik.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Colosseo_2020.jpg/400px-Colosseo_2020.jpg",
             "Eliptik plan: 189x156m | 80 giris | Dunyanin yeni 7 harikasi"),
            ("🌉 Golden Gate", "San Francisco, 1937", "Kirmizi rengi aslinda uluslararasi turuncu, siste gorunurluk icin secildi.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Golden_Gate_Bridge_as_seen_from_Battery_East.jpg/400px-Golden_Gate_Bridge_as_seen_from_Battery_East.jpg",
             "Muhendis: Joseph Strauss | Uzunluk: 2.737m | Art Deco tasarim"),
            ("🏰 Neuschwanstein", "Bavyera, 1886", "Kral II. Ludwig'in peri masali satosu. Disney'in Uyuyan Guzel satosuna ilham verdi!",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Schloss_Neuschwanstein_2013.jpg/400px-Schloss_Neuschwanstein_2013.jpg",
             "Romantik donem | Yilda 1.4 milyon ziyaretci | Almanya'nin en unlu satosu"),
            ("🕌 Sultanahmet Camii", "Istanbul, 1616", "6 minareli tek cami! Mavi cinileriyle unlu. Karsisinda Ayasofya, arasinda At Meydani.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Istanbul_%2834223582516%29_%28cropped%29.jpg/400px-Istanbul_%2834223582516%29_%28cropped%29.jpg",
             "Mimar: Sedefkar Mehmed Aga | 20.000+ Iznik cinisi | Mavi Cami"),
            ("🏗️ Burj Khalifa", "Dubai, 2010", "Dunyanin en yuksek binasi. 828m, 163 kat. Col sicaginda gunde 946.000 litre su kullanir!",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Burj_Khalifa_%28worlds_tallest_building%29_and_the_Dubai_skyline_%2825781049892%29.jpg/400px-Burj_Khalifa_%28worlds_tallest_building%29_and_the_Dubai_skyline_%2825781049892%29.jpg",
             "Mimar: Adrian Smith (SOM) | 57 asansor | En yuksek gozlem terasi: 555m"),
            ("🏯 Buyuk Cin Seddi", "Cin, MO 7. yy-MS 17. yy", "21.196 km! Uzaydan gorulemez (efsane) ama dunyanin en uzun yapisi.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/The_Great_Wall_of_China_at_Jinshanling-edit.jpg/400px-The_Great_Wall_of_China_at_Jinshanling-edit.jpg",
             "2000+ yillik insaat | Milyonlarca isci | UNESCO"),
            ("🎭 Sydney Opera", "Sidney, 1973", "Jorn Utzon'un yelken bicimli tasarimi. Yarismayi kazandiginda 233 projeyi gecti!",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Sydney_Australia._%2821339175489%29.jpg/400px-Sydney_Australia._%2821339175489%29.jpg",
             "Mimar: Jorn Utzon | 1 milyon+ cini kaplama | UNESCO"),
            ("🕌 Suleymaniye Camii", "Istanbul, 1557", "Mimar Sinan'in kalfalik eseri. Istanbul'un 7 tepesinden birinde, sehre hakim konumda.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/S%C3%BCleymaniyeMosqueIstanbul_%28cropped%29.jpg/400px-S%C3%BCleymaniyeMosqueIstanbul_%28cropped%29.jpg",
             "Mimar: Sinan | Kulliye: medrese, hamam, darussifa | Osmanli'nin zirvesi"),
            ("🗽 Ozgurluk Heykeli", "New York, 1886", "Fransa'dan ABD'ye hediye. Ic iskelet Gustave Eiffel'in tasarimi!",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Front_view_of_Statue_of_Liberty_%28cropped%29.jpg/400px-Front_view_of_Statue_of_Liberty_%28cropped%29.jpg",
             "Heykeltrasi: Bartholdi | Yukseklik: 93m (kaide dahil) | Bakir kaplama"),
            ("🏛️ Petra", "Urdun, MO 4. yy", "Kayaya oyulmus antik Nebati sehri. Indiana Jones'un son sahnesinde rol aldi!",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Al_Deir_Petra.JPG/400px-Al_Deir_Petra.JPG",
             "Hazine Binasi (El-Hazne) | Kizil kumtasi | UNESCO | Yeni 7 harika"),
        ]
        for idx_y, (ad, yer, bilgi, img, detay) in enumerate(yapilar):
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;margin-bottom:10px;border:1px solid #1e3a5f;overflow:hidden">
                <div style="display:flex;gap:14px;padding:14px;align-items:flex-start">
                    <img src="{img}" style="width:160px;min-width:160px;height:110px;object-fit:cover;border-radius:8px;
                         box-shadow:0 3px 10px rgba(0,0,0,.4);border:2px solid #1e3a5f" onerror="this.style.display='none'">
                    <div style="flex:1">
                        <div style="font-weight:800;font-size:1rem;color:#e0e7ff !important;margin-bottom:4px">{ad}</div>
                        <div style="font-size:.75rem;color:#60a5fa !important;margin-bottom:6px">{yer}</div>
                        <div style="font-size:.82rem;color:#cbd5e1 !important;line-height:1.4">{bilgi}</div>
                        <div style="font-size:.68rem;color:#64748b !important;margin-top:6px;border-top:1px solid #1e293b;padding-top:4px">{detay}</div>
                    </div>
                </div>
            </div>
            """)

    with sub[1]:
        styled_section("👷 Ünlü Mimarlar", "#3b82f6")
        mimarlar = [
            ("👷 Mimar Sinan", "1489-1588", "Osmanlı 🇹🇷",
             "Osmanlı'nın baş mimarı. 375+ eser: Süleymaniye, Selimiye, Şehzade. 50 yıl boyunca mimar başı.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Mimar_Sinan%2C_Pair_portrait_with_Mausoleum.jpg/200px-Mimar_Sinan%2C_Pair_portrait_with_Mausoleum.jpg",
             "Kalfalık: Süleymaniye | Ustalık: Selimiye | 94 cami, 52 mescit, 55 medrese, 35 saray"),
            ("👷 Antoni Gaudí", "1852-1926", "İspanya 🇪🇸",
             "Doğadan ilham alan organik formlar. Sagrada Familia hayat eseri. Tramvay kazasında öldü, dilenci sanıldı.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Antoni_Gaudi_1878.jpg/200px-Antoni_Gaudi_1878.jpg",
             "Casa Batlló, Casa Milà, Park Güell | Katalonya Modernizmi"),
            ("👷 Zaha Hadid", "1950-2016", "Irak/İngiltere 🇮🇶🇬🇧",
             "İlk kadın Pritzker ödüllü mimar. Akıcı, fütüristik formlar.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Zaha_Hadid_in_Heydar_Aliyev_Cultural_center_in_Baku_nov_2013.jpg/200px-Zaha_Hadid_in_Heydar_Aliyev_Cultural_center_in_Baku_nov_2013.jpg",
             "Heydar Aliyev, MAXXI, Guangzhou Opera | Parametrik mimari öncüsü"),
            ("👷 Frank Lloyd Wright", "1867-1959", "ABD 🇺🇸",
             "Organik mimari. Şelale Evi — şelalenin üzerine inşa! Guggenheim Müzesi.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Frank_Lloyd_Wright_portrait.jpg/200px-Frank_Lloyd_Wright_portrait.jpg",
             "Fallingwater, Guggenheim, Robie House | Prairie School | 500+ proje"),
            ("👷 Le Corbusier", "1887-1965", "İsviçre/Fransa 🇨🇭🇫🇷",
             "Modern mimarinin babası. 'Ev yaşamak için bir makinedir.' Betonarme devrimi.",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Le_Corbusier_%281964%29.jpg/200px-Le_Corbusier_%281964%29.jpg",
             "Villa Savoye, Chandigarh, Unité d'Habitation | 5 mimari ilke"),
            ("👷 Tadao Ando", "1941-", "Japonya 🇯🇵",
             "Beton şairi. Işık ve su ile mekan yaratan minimalist. Eski boksör, kendi kendini eğitmiş mimar!",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Tadao_Ando_2004.jpg/200px-Tadao_Ando_2004.jpg",
             "Church of Light, Naoshima, Punta della Dogana | Pritzker 1995"),
            ("👷 Oscar Niemeyer", "1907-2012", "Brezilya 🇧🇷",
             "Brezilya'nın başkenti Brasília'yı tasarladı. Eğri çizgilerin ustası. 104 yaşına kadar çizim yaptı!",
             "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Oscar_Niemeyer_1968b.jpg/200px-Oscar_Niemeyer_1968b.jpg",
             "Brasília Katedrali, Niterói Müzesi | 'Düz çizgi beni ilgilendirmez'"),
        ]
        for idx_m, (ad, yasam, ulke, bilgi, img, detay) in enumerate(mimarlar):
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;margin-bottom:8px;border:1px solid #1e3a5f;overflow:hidden">
                <div style="display:flex;gap:14px;padding:12px;align-items:flex-start">
                    <img src="{img}" style="width:90px;min-width:90px;height:110px;object-fit:cover;border-radius:8px;
                         box-shadow:0 3px 8px rgba(0,0,0,.4);border:2px solid #1e3a5f" onerror="this.style.display='none'">
                    <div style="flex:1">
                        <div style="font-weight:800;font-size:.95rem;color:#e0e7ff !important">{ad}</div>
                        <div style="font-size:.72rem;color:#60a5fa !important;margin-bottom:4px">{yasam} — {ulke}</div>
                        <div style="font-size:.82rem;color:#cbd5e1 !important;line-height:1.4">{bilgi}</div>
                        <div style="font-size:.65rem;color:#64748b !important;margin-top:4px;border-top:1px solid #1e293b;padding-top:3px">{detay}</div>
                    </div>
                </div>
            </div>
            """)

    with sub[2]:
        styled_section("📐 Mimari Akımlar", "#f59e0b")
        akimlar = [
            ("🏛️ Antik", "MÖ 3000-500", "Sütunlar, simetri, tapınaklar — Mısır, Yunan, Roma"),
            ("⛪ Gotik", "1100-1500", "Sivri kemerler, uçan payandalar, vitray pencereler — Notre Dame"),
            ("🕌 Osmanlı", "1300-1900", "Kubbe, minare, avlu, çini — Mimar Sinan eserleri"),
            ("🏛️ Rönesans", "1400-1600", "Simetri, kubbe, perspektif — Floransa Katedrali"),
            ("✨ Barok", "1600-1750", "Gösterişli, süslü, dramatik — Versailles Sarayı"),
            ("🏗️ Art Nouveau", "1890-1910", "Organik formlar, doğa motifleri — Gaudí"),
            ("⬜ Bauhaus", "1919-1933", "Form fonksiyonu izler. Sade, fonksiyonel, endüstriyel"),
            ("🏙️ Modernizm", "1920-1970", "Cam, çelik, beton. Az çoktur — Mies van der Rohe"),
            ("🔮 Dekonstrüktivizm", "1980-günümüz", "Kırık formlar, asimetri — Zaha Hadid, Frank Gehry"),
        ]
        for ad, yil, ozellik in akimlar:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:4px;border-left:3px solid #f59e0b">
                <span style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</span>
                <span style="color:#94a3b8 !important;font-size:0.75rem;margin-left:8px">({yil})</span>
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:2px">{ozellik}</div>
            </div>
            """)


# ═══════════════════════════════════════════════════════════════
# 12) DANS & HAREKET
# ═══════════════════════════════════════════════════════════════

def _render_dans():
    styled_section("💃 Dans & Hareket Sanatı", "#ec4899")

    dans_turleri = [
        ("🩰 Bale", "Klasik dans. Zarafet, disiplin, teknik. Kuğu Gölü, Fındıkkıran.", "İtalya, 15. yy"),
        ("💃 Tango", "Tutku dansı. İki kişi arasında yoğun bağlantı.", "Arjantin, 19. yy"),
        ("🕺 Hip-Hop", "Sokak dansı. Breakdance, popping, locking.", "ABD, 1970'ler"),
        ("💃 Salsa", "Latin ritmi. Enerji, neşe, partner dansı.", "Küba, 1960'lar"),
        ("🎭 Modern Dans", "Baleye karşı özgür ifade. Martha Graham öncüsü.", "ABD, 20. yy"),
        ("👘 Flamenko", "İspanyol tutkusu. Ayak vuruşları, el çırpmaları.", "İspanya, 18. yy"),
        ("🇹🇷 Türk Halk Dansları", "Halay, horon, zeybek, karşılama. Her bölge farklı.", "Anadolu"),
        ("🪘 Afrika Dansı", "Ritim odaklı, topluluk dansı. Davul eşliğinde.", "Afrika"),
    ]

    for ad, aciklama, koken in dans_turleri:
        _render_html(f"""
        <div style="background:#0f172a;border-radius:14px;padding:14px 18px;margin-bottom:8px;
                     border-left:4px solid #ec4899">
            <div style="font-weight:700;color:#e0e7ff !important;font-size:0.95rem">{ad}</div>
            <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:2px">{aciklama}</div>
            <div style="font-size:0.7rem;color:#c084fc !important;margin-top:2px">📍 {koken}</div>
        </div>
        """)

    st.markdown("---")
    styled_section("🇹🇷 Türk Halk Dansları Detay", "#f59e0b")
    turk_danslari = [
        ("Halay", "Güneydoğu Anadolu", "El ele tutuşarak sıra halinde. Davul-zurna eşliğinde."),
        ("Horon", "Karadeniz", "Hızlı titreşim hareketleri. Kemençe eşliğinde. Dünyanın en hızlı dansı!"),
        ("Zeybek", "Ege", "Ağır, vakur, erkeksi. Kartal gibi kollar açılır."),
        ("Karşılama", "Trakya", "9/8'lik aksak ritim. Karşılıklı oynanır."),
        ("Semah", "Orta Anadolu", "Alevi-Bektaşi geleneği. Dönerek yapılan ruhani dans."),
        ("Bar", "Doğu Anadolu", "Omuz omuza, sıra halinde. Kars, Erzurum."),
    ]
    for ad, bolge, aciklama in turk_danslari:
        with st.expander(f"🇹🇷 {ad} — {bolge}"):
            st.markdown(aciklama)


# ═══════════════════════════════════════════════════════════════
# 13) DÜNYA SANATLARI
# ═══════════════════════════════════════════════════════════════

def _render_dunya_sanatlari():
    styled_section("🎪 Dünya Sanatları — Kültürel Yolculuk", "#6366f1")

    kulturler = [
        {
            "ad": "🇯🇵 Japon Sanatı", "renk": "#ef4444",
            "teknikler": "Ukiyo-e (ahşap baskı), Origami, İkebana (çiçek düzenleme), Kintsugi (altınla tamir), Sumi-e (mürekkep resim)",
            "bilgi": "Japon estetiği: 'Wabi-sabi' — kusurlu güzellik. Kırık bir vazoyu altınla tamir etmek (Kintsugi) kusuru sanata dönüştürür.",
        },
        {
            "ad": "🕌 İslam Sanatı", "renk": "#10b981",
            "teknikler": "Hat sanatı, Çini, Ebru, Minyatür, Geometrik desen, Arabesk, Tezhip",
            "bilgi": "Figür yasağı yaratıcılığı tetikledi! Geometrik desenler sonsuzluğu, hat sanatı ilahi kelamı temsil eder. Ebru 'kağıt üzerinde dans eden mürekkep'tir.",
        },
        {
            "ad": "🌍 Afrika Sanatı", "renk": "#f59e0b",
            "teknikler": "Maske yapımı, Tekstil (Kente kumaş), Boncuk işi, Heykel, Beden boyama, Davul yapımı",
            "bilgi": "Sanat toplumsal kimliğin parçası. Maskeler ruhani güçleri temsil eder. Picasso ve Matisse Afrika masklarından etkilendi!",
        },
        {
            "ad": "🇮🇳 Hint Sanatı", "renk": "#ec4899",
            "teknikler": "Mandala, Rangoli (zemin deseni), Mehndi (kına sanatı), Minyatür, Dans (Bharatanatyam)",
            "bilgi": "Mandalalar evrenin haritası. Rangoli kapının önüne yapılır — misafirpererliğin sembolü. Renkler ve ritüel iç içe.",
        },
        {
            "ad": "🇲🇽 Latin Amerika Sanatı", "renk": "#8b5cf6",
            "teknikler": "Mural (duvar resmi), Aztek motifleri, Tekstil, Seramik, Dia de los Muertos (Ölüler Günü sanatı)",
            "bilgi": "Diego Rivera'nın devasa duvar resimleri sosyal mesaj taşır. Ölüler Günü'nde renkli iskelet figürleri ölümü kutlar!",
        },
        {
            "ad": "🏜️ Aborijin Sanatı", "renk": "#f97316",
            "teknikler": "Nokta boyama (Dot painting), Kaya resimleri, Bumerang süsleme, Didgeridoo",
            "bilgi": "65.000 yıllık dünyanın en eski sanat geleneği! Nokta boyama tekniği kutsal haritaları gizler — uzaktan farklı, yakından farklı görünür.",
        },
        {
            "ad": "🇨🇳 Çin Sanatı", "renk": "#06b6d4",
            "teknikler": "Kaligrafi, İpek boyama, Porselen, Yeşim taş işçiliği, Çin mürekkebi resim",
            "bilgi": "Çin kaligrafisi 'yazılı dans' olarak kabul edilir. Porselen (china) kelimesi Çin'den gelir! 5000 yıllık gelenek.",
        },
        {
            "ad": "🇹🇷 Türk-İslam Sanatı", "renk": "#eab308",
            "teknikler": "Hat, Ebru, Çini (İznik/Kütahya), Minyatür, Tezhip, Kilim, Halı, Gölge oyunu (Karagöz)",
            "bilgi": "İznik çinileri dünya mirası. Ebru (marbling) Türk icadı — UNESCO somut olmayan kültürel miras. Karagöz gölge oyunu 600+ yıllık.",
        },
    ]

    for k in kulturler:
        with st.expander(f"{k['ad']}", expanded=False):
            _render_html(f"""
            <div style="background:{k['renk']}08;border-radius:12px;padding:14px;border-left:4px solid {k['renk']}">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:6px">🎨 Teknikler:</div>
                <div style="color:#94a3b8 !important;font-size:0.83rem;margin-bottom:8px">{k['teknikler']}</div>
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:4px">💡 Bilgi:</div>
                <div style="color:#c4b5fd !important;font-size:0.83rem;line-height:1.6">{k['bilgi']}</div>
            </div>
            """)


# ═══════════════════════════════════════════════════════════════
# 14) KALİGRAFİ & HAT
# ═══════════════════════════════════════════════════════════════

def _render_kaligrafi():
    styled_section("🖌️ Kaligrafi & Hat Sanatı", "#f97316")
    import streamlit.components.v1 as components

    sub = st.tabs(["✍️ Yazı Pratiği", "🕌 Türk Hat Sanatı", "🇯🇵 Dünya Kaligrafisi"])

    with sub[0]:
        styled_section("✍️ Dijital Kaligrafi Pratiği", "#f97316")
        col1, col2 = st.columns(2)
        with col1:
            renk = st.color_picker("Mürekkep", "#1e293b", key="snt_kal_renk")
        with col2:
            kalinlik = st.slider("Kalem", 1, 15, 4, key="snt_kal_k")

        html = f"""
        <canvas id="kalCanvas" width="650" height="300" style="border-radius:14px;border:2px solid #d4a373;cursor:crosshair;display:block;margin:0 auto;background:#1e293b"></canvas>
        <div style="text-align:center;margin-top:8px">
            <button onclick="document.getElementById('kalCanvas').getContext('2d').clearRect(0,0,650,300)" style="padding:5px 14px;border-radius:8px;border:1px solid #d4a373;background:#334155;color:#f59e0b;cursor:pointer">🗑️ Temizle</button>
        </div>
        <script>
        (function(){{const c=document.getElementById('kalCanvas'),ctx=c.getContext('2d');let d=false,lx=0,ly=0;ctx.lineCap='round';
        c.addEventListener('mousedown',e=>{{d=true;lx=e.offsetX;ly=e.offsetY;}});
        c.addEventListener('mousemove',e=>{{if(!d)return;ctx.beginPath();ctx.moveTo(lx,ly);ctx.lineTo(e.offsetX,e.offsetY);ctx.strokeStyle='{renk}';ctx.lineWidth={kalinlik};ctx.stroke();lx=e.offsetX;ly=e.offsetY;}});
        c.addEventListener('mouseup',()=>d=false);c.addEventListener('mouseleave',()=>d=false);}})();
        </script>
        """
        components.html(html, height=360)

    with sub[1]:
        styled_section("🕌 Türk Hat Sanatı", "#eab308")
        st.markdown("""
**Hat Sanatı Nedir?**
Arap harfleriyle güzel yazı yazma sanatı. Osmanlı döneminde zirveye ulaştı.

**Hat Türleri:**
- **Sülüs:** Büyük, gösterişli, cami kitabelerinde
- **Nesih:** Küçük, okunaklı, Kuran yazımında
- **Ta'lik:** Farsça etkili, zarif, şiirlerde
- **Divani:** Osmanlı divanı, resmi belgelerde
- **Rik'a:** Günlük yazı, hızlı ve pratik
- **Kûfi:** En eski stil, geometrik ve köşeli

**Ünlü Hattatlar:**
- 🕌 **Şeyh Hamdullah** (1436-1520) — Osmanlı hat sanatının babası
- 🕌 **Hafız Osman** (1642-1698) — Altın çağ hattatı
- 🕌 **Hamid Aytaç** (1891-1982) — Son büyük Osmanlı hattatı
        """)

    with sub[2]:
        styled_section("🇯🇵 Dünya Kaligrafi Gelenekleri", "#8b5cf6")
        gelenekler = [
            ("🇯🇵 Japonya — Shodō", "Fırça + mürekkep + pirinç kağıdı. Zen felsefesiyle iç içe. 'Bir vuruş, bir nefes.'"),
            ("🇨🇳 Çin — Shūfǎ", "5000 yıllık gelenek. 4 hazine: fırça, mürekkep, kağıt, yun taşı."),
            ("🕌 Arap — Hüsn-ü Hat", "Kuran yazımı ile gelişti. Geometri ve estetik birleşimi."),
            ("🇮🇳 Hindistan — Devanagari", "Sanskrit yazısı. Yukarıdan bir çizgiyle bağlanan harfler."),
            ("🇰🇷 Kore — Seoye", "Hangul alfabesiyle kaligrafi. Kare formlar içinde zarif çizgiler."),
        ]
        for ad, aciklama in gelenekler:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:6px;border-left:3px solid #8b5cf6">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</div>
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:2px">{aciklama}</div>
            </div>
            """)


# ═══════════════════════════════════════════════════════════════
# 15) TİYATRO SAHNESİ
# ═══════════════════════════════════════════════════════════════

def _render_tiyatro():
    styled_section("🎭 Tiyatro Sahnesi", "#f59e0b")

    sub = st.tabs(["🎭 Tiyatro Tarihi", "📝 Sahne Yazarlığı", "🎪 Türk Tiyatrosu"])

    with sub[0]:
        styled_section("🎭 Tiyatro Tarihi", "#8b5cf6")
        donemler = [
            ("🏛️ Antik Yunan", "MÖ 5. yy", "Tiyatronun doğuşu. Tragedya (Sofokles, Euripides) ve Komedya (Aristophanes). Açık hava tiyatroları."),
            ("🏰 Ortaçağ", "5-15. yy", "Dini oyunlar, misterler, moraliteler. Kilise önünde sahneleme."),
            ("🎭 Rönesans", "15-17. yy", "Shakespeare! Hamlet, Romeo ve Juliet. Globe Theatre."),
            ("💃 Barok & Klasik", "17-18. yy", "Molière (komedi), Racine (trajedi). Kral saraylarında tiyatro."),
            ("🎪 Modern", "19-20. yy", "Çehov, Ibsen, Brecht. Realizm ve deneysel tiyatro."),
            ("🔮 Çağdaş", "20-21. yy", "Absürd tiyatro (Beckett), performans sanatı, immersive tiyatro."),
        ]
        for ad, yil, aciklama in donemler:
            with st.expander(f"{ad} ({yil})"):
                st.markdown(aciklama)

    with sub[1]:
        styled_section("📝 Sahne Yazarlığı Atölyesi", "#10b981")
        st.markdown("""
**Bir Sahne Nasıl Yazılır?**

1. **Karakterler:** Kim? Motivasyonu ne? İç çatışması ne?
2. **Çatışma:** Karakter ne istiyor? Engel ne?
3. **Diyalog:** Doğal konuşma, alt metin (söylenmeyen şeyler)
4. **Sahne Yönergesi:** (Sessizce masaya oturur, pencereden dışarı bakar)
5. **Doruk:** Gerilimin en yüksek noktası
6. **Çözüm:** Sonuç — mutlu, trajik, açık uçlu

**Örnek Sahne Formatı:**
        """)
        st.code("""
SAHNE 1 — Okul bahçesi, öğle arası

ELİF: (heyecanla koşarak gelir) Haberi duydun mu?!
CAN: (kitabından başını kaldırmadan) Hangi haberi?
ELİF: Tiyatro kulübü kuruluyormuş!
CAN: (ilgisiz) Hmm.
ELİF: Sen de katılmalısın!
CAN: (kitabı kapatır, ilk kez bakar) Neden ben?
ELİF: Çünkü... (duraksayar) çünkü sen en iyi hikaye anlatıcısısın.
        """, language=None)

        st.text_area("Kendi sahnenizi yazın! 🎭", height=200, key="snt_sahne",
                      placeholder="SAHNE 1 — ...\n\nKARAKTER: (yönerge) Diyalog...")

    with sub[2]:
        styled_section("🇹🇷 Türk Tiyatrosu", "#ef4444")
        turk_tiyatro = [
            ("🎪 Karagöz & Hacivat", "Gölge oyunu. 600+ yıllık gelenek. UNESCO mirası. Karagöz cahil halk, Hacivat aydın."),
            ("🎭 Ortaoyunu", "Açık alanda doğaçlama. Kavuklu ve Pişekar ikilisi. Osmanlı sokak tiyatrosu."),
            ("🎪 Meddah", "Tek kişilik gösteri. Hikaye anlatıcısı. Stand-up comedy'nin atası!"),
            ("🎭 Modern Türk Tiyatrosu", "Muhsin Ertuğrul ile başladı (1920'ler). Devlet Tiyatroları, özel tiyatrolar."),
            ("🌟 Genco Erkal", "Türk tiyatrosunun yaşayan efsanesi. Brecht, Beckett yorumları."),
        ]
        for ad, aciklama in turk_tiyatro:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:6px;border-left:3px solid #ef4444">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</div>
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:2px">{aciklama}</div>
            </div>
            """)


# ═══════════════════════════════════════════════════════════════
# 16) SANAT ANALİZİ
# ═══════════════════════════════════════════════════════════════

def _render_sanat_analizi():
    styled_section("📊 Sanat Eseri Analizi Rehberi", "#3b82f6")

    st.markdown("""
### 🔍 Bir Sanat Eserini Nasıl Analiz Edersin?

Bir tablo, heykel veya fotoğraf gördüğünde şu 6 adımı uygula:
    """)

    adimlar = [
        ("1️⃣ Tanımlama", "Ne görüyorsun? Nesne, figür, manzara, renk, şekil — ilk gördüklerini say.", "#ef4444"),
        ("2️⃣ Kompozisyon", "Öğeler nasıl yerleştirilmiş? Simetrik mi? Üçte bir kuralı uygulanmış mı? Bakış nereye yönleniyor?", "#f59e0b"),
        ("3️⃣ Renk Analizi", "Hangi renkler kullanılmış? Sıcak mı soğuk mu? Kontrast var mı? Renk bir duygu yaratıyor mu?", "#10b981"),
        ("4️⃣ Teknik", "Hangi teknikle yapılmış? Fırça darbeleri görünür mü? Yağlıboya, suluboya, dijital? Işık-gölge nasıl?", "#3b82f6"),
        ("5️⃣ Anlam & Sembol", "Sanatçı ne anlatmak istemiş? Gizli semboller var mı? Tarihsel bağlam ne? Kişisel yorum.", "#8b5cf6"),
        ("6️⃣ Değerlendirme", "Sana ne hissettirdi? Beğendin mi? Neden? Başka eserlerle karşılaştır.", "#ec4899"),
    ]

    for baslik, aciklama, renk in adimlar:
        _render_html(f"""
        <div style="background:{renk}08;border-radius:14px;padding:14px 18px;margin-bottom:10px;border-left:4px solid {renk}">
            <div style="font-weight:700;color:#e0e7ff !important;font-size:0.95rem;margin-bottom:4px">{baslik}</div>
            <div style="color:#94a3b8 !important;font-size:0.83rem;line-height:1.5">{aciklama}</div>
        </div>
        """)

    st.markdown("---")
    styled_section("📝 Analiz Pratiği", "#6366f1")
    st.markdown("**Bir eser seç ve analiz formunu doldur:**")

    eser_sec = st.selectbox("Eser", ["Mona Lisa — Da Vinci", "Yıldızlı Gece — Van Gogh",
                                      "Guernica — Picasso", "Kaplumbağa Terbiyecisi — Osman Hamdi Bey",
                                      "Kendi seçtiğim bir eser"], key="snt_analiz_eser")

    st.text_area("1. Ne görüyorsun? (Tanımlama)", key="snt_a1", height=80, placeholder="Resimde bir kadın oturuyor...")
    st.text_area("2. Kompozisyon nasıl?", key="snt_a2", height=80, placeholder="Figür ortada, arka plan manzara...")
    st.text_area("3. Renkler?", key="snt_a3", height=80, placeholder="Sıcak toprak tonları, yumuşak geçişler...")
    st.text_area("4. Teknik?", key="snt_a4", height=80, placeholder="Yağlıboya, sfumato tekniği...")
    st.text_area("5. Anlam?", key="snt_a5", height=80, placeholder="Gizemli gülümseme, ideal güzellik...")
    st.text_area("6. Değerlendirme?", key="snt_a6", height=80, placeholder="Beni etkileyen şey...")


# ═══════════════════════════════════════════════════════════════
# 17) SANAT GÜNLÜĞÜ
# ═══════════════════════════════════════════════════════════════

def _render_sanat_gunlugu(store):
    styled_section("🌟 Sanat Günlüğü & Portföy", "#eab308")

    sub = st.tabs(["📓 Günlük", "🎯 Hedeflerim", "💡 İlham Panosu"])

    with sub[0]:
        styled_section("📓 Sanat Günlüğüm", "#eab308")
        st.markdown("**Bugün ne yaptın? Sanat yolculuğunu kaydet!**")

        tarih = datetime.now().strftime("%d.%m.%Y")
        _render_html(f'<div style="text-align:right;color:#94a3b8 !important;font-size:0.8rem">📅 {tarih}</div>')

        dal = st.selectbox("Sanat Dalı", ["🎨 Görsel Sanatlar", "🎵 Müzik", "✍️ Yazarlık",
                                            "✂️ El Sanatları", "📸 Fotoğraf", "🎭 Tiyatro/Dans", "🏗️ Mimari"], key="snt_gun_dal")
        aktivite = st.text_input("Ne yaptın?", key="snt_gun_akt", placeholder="Ör: Suluboya ile manzara çizdim")
        sure = st.selectbox("Ne kadar sürdü?", ["5 dk", "15 dk", "30 dk", "1 saat", "1+ saat"], key="snt_gun_sure")
        notlar = st.text_area("Notlar & Düşünceler", key="snt_gun_not", height=100,
                               placeholder="Bugün öğrendiğim şey... Zorlandığım kısım... Keyif aldığım an...")
        mood = st.selectbox("Ruh Halin", options=["Cok Kotü", "Kotu", "Normal", "Iyi", "Cok Iyi", "Harika"], index=4, key="snt_gun_mood")

        if st.button("📓 Günlüğe Kaydet", key="snt_gun_kaydet", type="primary"):
            if aktivite:
                auth_user = st.session_state.get("auth_user", {})
                uid = auth_user.get("username", "misafir")
                uname = auth_user.get("ad_soyad", auth_user.get("username", "Misafir"))
                ugrade = auth_user.get("sinif", "")
                sure_dk = {"5 dk": 5, "15 dk": 15, "30 dk": 30, "1 saat": 60, "1+ saat": 90}.get(sure, 15)
                store.kaydet_aktivite(uid, uname, ugrade, dal.split(" ", 1)[1], aktivite, sure_dk, notlar, mood)
                st.success(f"✅ {tarih} günlüğü veritabanına kaydedildi! {mood}")
                st.balloons()
            else:
                st.warning("Lütfen aktivite alanını doldurun.")

    with sub[1]:
        styled_section("🎯 Sanat Hedeflerim", "#10b981")
        st.markdown("**Bu dönem için sanat hedeflerini belirle:**")

        hedefler = [
            "🎨 Haftada en az 3 çizim yapmak",
            "🎵 Bir enstrüman öğrenmeye başlamak",
            "📖 Bir hikaye/şiir tamamlamak",
            "✂️ Bir origami projesi bitirmek",
            "📸 Bir fotoğraf serisi oluşturmak",
            "🏛️ Bir müze/galeri ziyaret etmek",
            "🎭 Bir tiyatro oyununa gitmek",
            "🌈 Yeni bir teknik denemek",
        ]

        for i, hedef in enumerate(hedefler):
            st.checkbox(hedef, key=f"snt_hedef_{i}")

        ozel_hedef = st.text_input("Kendi hedefini ekle:", key="snt_ozel_hedef", placeholder="Ör: Manga çizmeyi öğrenmek")

    with sub[2]:
        styled_section("💡 İlham Panosu", "#ec4899")

        _render_html("""
        <div style="background:linear-gradient(135deg,#831843,#be185d);border-radius:16px;padding:18px;margin-bottom:16px;text-align:center">
            <div style="font-size:1.8rem;margin-bottom:8px">💡✨🎨</div>
            <div style="font-weight:700;color:white !important;font-size:1rem">Her Gün Bir İlham!</div>
        </div>
        """)

        ilhamlar = [
            "🎨 'Sanat, doğanın insan aracılığıyla ifadesidir.' — Émile Zola",
            "🌟 'Her çocuk bir sanatçıdır. Mesele büyüyünce de öyle kalabilmek.' — Picasso",
            "💪 'Yeteneğe güvenme, pratiğe güven. Günde 15 dakika her şeyi değiştirir.'",
            "🌈 'Renkleri karıştırmaktan korkma — en güzel renkler kazalardan doğar!'",
            "🎵 'Müzik, kelimelerle ifade edilemeyen şeyleri söyler.' — Victor Hugo",
            "📝 'İlk taslak her zaman çöptür. Ama çöp olmadan altın olmaz!' — Anne Lamott",
            "🔍 'Güzellik her yerde — onu görmeyi öğrenmek gerek.' — Rodin",
            "🎭 'Sahne hayattır, hayat sahnedir.' — Shakespeare",
        ]

        import random
        for ilham in random.sample(ilhamlar, min(4, len(ilhamlar))):
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:14px;margin-bottom:8px;
                         border-left:4px solid #ec4899;font-style:italic;color:#c4b5fd !important;font-size:0.85rem;line-height:1.5">
                {ilham}
            </div>
            """)


# ═══════════════════════════════════════════════════════════════
def _render_sanat_festivali():
    """Sanat Festivali — 20 proje fikri."""
    styled_section("🎪 Sanat Festivali Projeleri", "#ec4899")

    _render_html("""
    <div style="background:linear-gradient(135deg,#831843,#be185d,#ec4899);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid rgba(236,72,153,0.5);text-align:center;position:relative;overflow:hidden">
        <div style="position:absolute;top:8px;left:16px;font-size:2rem">🎨</div>
        <div style="position:absolute;top:8px;right:16px;font-size:2rem">🎵</div>
        <div style="position:absolute;bottom:8px;left:20px;font-size:1.5rem">🎭</div>
        <div style="position:absolute;bottom:8px;right:20px;font-size:1.5rem">💃</div>
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:8px">🎪✨🎨🎵🎭</div>
            <h2 style="color:white !important;font-size:1.5rem;margin:0 0 8px !important">Okul Sanat Festivali</h2>
            <p style="color:#fce7f3 !important;font-size:0.9rem;margin:0 !important">
                Sergi, konser, tiyatro, dans, film — okulunu sanat merkezine dönüştür!
            </p>
        </div>
    </div>
    """)

    # Kategori filtresi
    kategoriler = sorted(set(p.get("kategori", "") for p in SANAT_FESTIVALI))
    kat_f = st.selectbox("Kategori", ["Tümü"] + kategoriler, key="snt_fest_kat")

    projeler = SANAT_FESTIVALI
    if kat_f != "Tümü":
        projeler = [p for p in projeler if p.get("kategori") == kat_f]

    st.caption(f"🎪 {len(projeler)} festival projesi")

    # Kategori kartları
    kat_sayim = {}
    for p in SANAT_FESTIVALI:
        k = p.get("kategori", "?")
        kat_sayim[k] = kat_sayim.get(k, 0) + 1

    kat_renkler = {"Görsel": "#ef4444", "Müzik": "#3b82f6", "Tiyatro": "#8b5cf6", "Dans": "#ec4899",
                   "Yazarlık": "#10b981", "El Sanatları": "#f59e0b", "Fotoğraf": "#06b6d4",
                   "Sinema": "#f97316", "Disiplinler Arası": "#6366f1"}

    cols = st.columns(min(len(kat_sayim), 5))
    for col, (kat, cnt) in zip(cols, sorted(kat_sayim.items())):
        renk = kat_renkler.get(kat, "#94a3b8")
        with col:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:10px;padding:8px;text-align:center;border:1px solid {renk}30">
                <div style="font-weight:700;color:{renk} !important;font-size:1.1rem">{cnt}</div>
                <div style="font-size:0.6rem;color:#94a3b8 !important">{kat}</div>
            </div>
            """)

    # Proje listesi
    for p in projeler:
        renk = kat_renkler.get(p.get("kategori", ""), "#6366f1")
        zorluk_renk = {"Kolay": "#10b981", "Orta": "#f59e0b", "Zor": "#ef4444"}.get(p.get("zorluk", ""), "#6366f1")
        _lbl = f"{p.get('ikon','')} #{p.get('no',0)} {p['ad']} ({p.get('kategori','')}) - Sinif {p.get('sinif','')}"
        with st.expander(_lbl, expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                _render_html(f"""
                <div style="background:rgba(99,102,241,0.08);border-radius:10px;padding:10px;margin-bottom:8px;border:1px solid rgba(99,102,241,0.15)">
                    <div style="font-weight:700;color:#818cf8 !important;font-size:0.8rem;margin-bottom:4px">🧰 Malzemeler:</div>
                    <div style="color:#94a3b8 !important;font-size:0.83rem">{p.get('malzeme','')}</div>
                </div>
                """)
                st.markdown("**📋 Adımlar:**")
                for i, adim in enumerate(p.get("adimlar", []), 1):
                    st.markdown(f"**{i}.** {adim}")

                _render_html(f"""
                <div style="background:rgba(16,185,129,0.08);border-radius:10px;padding:10px;margin:8px 0;border:1px solid rgba(16,185,129,0.15)">
                    <div style="font-weight:700;color:#10b981 !important;font-size:0.8rem;margin-bottom:4px">🎯 Sonuç:</div>
                    <div style="color:#94a3b8 !important;font-size:0.83rem">{p.get('sonuc','')}</div>
                </div>
                """)
            with col2:
                _render_html(f"""
                <div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;border:1px solid {renk}20">
                    <div style="font-size:2.5rem;margin-bottom:6px">{p.get('ikon','')}</div>
                    <div style="font-size:0.7rem;color:{zorluk_renk} !important;font-weight:700">{p.get('zorluk','')}</div>
                    <div style="font-size:0.65rem;color:#94a3b8 !important;margin-top:2px">⏱️ {p.get('sure','')}</div>
                </div>
                """)


def _render_ilerleme_rapor(store):
    """İlerleme takibi, veli raporu, öğretmen paneli."""
    styled_section("📈 İlerleme & Rapor Merkezi", "#6366f1")

    auth_user = st.session_state.get("auth_user", {})
    user_id = auth_user.get("username", "misafir")
    user_name = auth_user.get("ad_soyad", auth_user.get("username", "Kullanıcı"))

    sub = st.tabs(["📊 Bireysel İlerleme", "👨‍👩‍👧 Veli Raporu", "👩‍🏫 Öğretmen Paneli"])

    with sub[0]:
        styled_section("📊 Bireysel Sanat İlerleme", "#8b5cf6")

        profil_data = store.get_profil(user_id)
        if not profil_data:
            st.info("Henüz sanat aktiviten kaydedilmemiş. 🌟 Sanat Günlüğü sekmesinden aktivite kaydet!")
            return

        from models.sanat_sokagi import SanatProfili
        p = SanatProfili.from_dict(profil_data)
        genel_puan = p.hesapla_genel_puan()

        # Genel puan kartı
        _render_html(f"""
        <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95);border-radius:24px;padding:28px;margin-bottom:20px;
                     border:2px solid rgba(139,92,246,0.4);text-align:center">
            <div style="font-size:2.5rem;margin-bottom:8px">🎨</div>
            <div style="font-size:2.2rem;font-weight:900;color:#a78bfa !important">{genel_puan:.0f}/100</div>
            <div style="font-size:1rem;font-weight:700;color:#e9d5ff !important">Sanat Gelişim Puanı</div>
            <div style="font-size:0.8rem;color:#94a3b8 !important;margin-top:4px">{user_name} • {p.toplam_aktivite} aktivite • {p.toplam_sure_dk} dk</div>
            <div style="max-width:350px;margin:12px auto;background:#1e1b4b;border-radius:10px;height:12px;overflow:hidden">
                <div style="width:{genel_puan:.0f}%;height:100%;background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981);border-radius:10px"></div>
            </div>
        </div>
        """)

        # Özet kartlar
        cols = st.columns(4)
        stats = [
            ("🎨", str(p.toplam_aktivite), "Aktivite"),
            ("⏱️", f"{p.toplam_sure_dk} dk", "Toplam Süre"),
            ("🔥", str(p.seri_gun), f"Seri ({p.en_iyi_seri} en iyi)"),
            ("📊", str(len(p.dal_skorlari)), "Aktif Dal"),
        ]
        for col, (ikon, deger, etiket) in zip(cols, stats):
            with col:
                _render_html(f"""
                <div style="background:#0f172a;border-radius:14px;padding:14px;text-align:center;
                             border:1px solid rgba(99,102,241,0.15)">
                    <div style="font-size:1.3rem">{ikon}</div>
                    <div style="font-weight:800;color:#818cf8 !important;font-size:1.3rem">{deger}</div>
                    <div style="font-size:0.65rem;color:#94a3b8 !important">{etiket}</div>
                </div>
                """)

        # Dal bazlı performans
        if p.dal_skorlari:
            styled_section("🎭 Dal Bazlı Performans", "#10b981")
            dal_renkler = {"Görsel Sanatlar": "#ef4444", "Müzik": "#3b82f6", "Yazarlık": "#8b5cf6",
                           "El Sanatları": "#10b981", "Fotoğraf": "#06b6d4", "Tiyatro/Dans": "#f59e0b", "Mimari": "#ec4899"}
            for dal, skor in p.dal_skorlari.items():
                puan = skor.get("puan", 0)
                renk = dal_renkler.get(dal, "#6366f1")
                _render_html(f"""
                <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:4px;border-left:4px solid {renk}">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <span style="font-weight:700;color:#e0e7ff !important;font-size:0.85rem">{dal}</span>
                        <span style="color:{renk} !important;font-weight:700;font-size:0.85rem">{skor.get('aktivite',0)} aktivite • {skor.get('sure_dk',0)} dk • {puan}/100</span>
                    </div>
                    <div style="background:#1e1b4b;border-radius:6px;height:8px;overflow:hidden">
                        <div style="width:{puan}%;height:100%;background:{renk};border-radius:6px"></div>
                    </div>
                </div>
                """)

        # İlerleme grafiği
        if p.ilerleme_gecmisi and len(p.ilerleme_gecmisi) > 1:
            styled_section("📈 İlerleme Grafiği", "#f59e0b")
            tarihler = [x.get("tarih", "") for x in p.ilerleme_gecmisi[-14:]]
            puanlar = [x.get("puan", 0) for x in p.ilerleme_gecmisi[-14:]]
            max_p = max(puanlar) if puanlar else 100
            grafik = '<div style="display:flex;align-items:flex-end;gap:4px;height:120px;padding:8px;background:#0f172a;border-radius:12px">'
            for t, pn in zip(tarihler, puanlar):
                h = max(4, (pn / max(max_p, 1)) * 100)
                renk = "#10b981" if pn >= 50 else "#f59e0b" if pn >= 20 else "#ef4444"
                grafik += f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%"><div style="font-size:0.5rem;color:{renk}">{pn:.0f}</div><div style="width:100%;height:{h:.0f}px;background:{renk};border-radius:3px 3px 0 0;min-width:6px"></div><div style="font-size:0.45rem;color:#64748b;margin-top:1px">{t[-5:]}</div></div>'
            grafik += '</div>'
            _render_html(grafik)

    with sub[1]:
        styled_section("👨‍👩‍👧 Veli Raporu", "#ec4899")

        profiller = store.get_all_profiller()
        if not profiller:
            st.info("Henüz öğrenci profili yok.")
            return

        profile_options = {p.get("student_id", ""): p.get("student_name", "?") for p in profiller}
        sel = st.selectbox("Öğrenci Seç", list(profile_options.keys()),
                           format_func=lambda x: profile_options.get(x, x), key="snt_veli_sel")

        rapor = store.veli_raporu(sel)
        if rapor.get("durum") == "veri_yok":
            st.info("Bu öğrenci için henüz veri yok.")
            return

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#831843,#be185d);border-radius:20px;padding:24px;margin-bottom:16px;
                     border:2px solid rgba(236,72,153,0.4);text-align:center">
            <div style="font-size:2rem;margin-bottom:6px">👨‍👩‍👧‍👦</div>
            <div style="font-weight:700;color:white !important;font-size:1.1rem">{rapor['ad']} — Sanat Gelişim Raporu</div>
            <div style="color:#fce7f3 !important;font-size:0.85rem">{rapor.get('sinif','')} • Genel Puan: {rapor['genel_puan']:.0f}/100</div>
        </div>
        """)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Toplam Aktivite", rapor["toplam_aktivite"])
        with col2:
            st.metric("Toplam Süre", f"{rapor['toplam_sure_dk']} dk")
        with col3:
            st.metric("En Güçlü Dal", rapor["en_guclu_dal"])
        with col4:
            st.metric("Çalışma Serisi", f"{rapor['seri_gun']} gün")

        if rapor.get("dal_ozet"):
            styled_section("📊 Dal Bazlı Özet", "#6366f1")
            for dal, ozet in rapor["dal_ozet"].items():
                st.markdown(f"- **{dal}:** {ozet['aktivite']} aktivite, {ozet['sure']} dk, {ozet['puan']}/100 puan")

        # AI Tavsiye
        styled_section("🤖 AI Tavsiye", "#f59e0b")
        if rapor["toplam_aktivite"] < 5:
            st.info("🌱 Çocuğunuz sanat yolculuğuna yeni başlıyor. Farklı dalları denemesi için teşvik edin!")
        elif rapor["genel_puan"] >= 60:
            st.success(f"🌟 Harika ilerleme! En güçlü alan: **{rapor['en_guclu_dal']}**. Bu dalda özel eğitim düşünülebilir.")
        else:
            st.warning(f"💪 Düzenli pratik önemli. Haftada en az 3 gün, günde 15 dk sanat aktivitesi önerilir.")

        # PDF rapor
        rapor_text = f"""SANAT SOKAGI - OGRENCI GELISIM RAPORU
{'='*50}
Ogrenci: {rapor['ad']}
Sinif: {rapor.get('sinif','')}
Genel Puan: {rapor['genel_puan']:.0f}/100
Toplam Aktivite: {rapor['toplam_aktivite']}
Toplam Sure: {rapor['toplam_sure_dk']} dk
Calisma Serisi: {rapor['seri_gun']} gun (en iyi: {rapor['en_iyi_seri']})
En Guclu Dal: {rapor['en_guclu_dal']}
{'='*50}
DAL BAZLI DETAY:
"""
        for dal, ozet in rapor.get("dal_ozet", {}).items():
            rapor_text += f"  {dal}: {ozet['aktivite']} aktivite, {ozet['sure']} dk, {ozet['puan']}/100\n"
        rapor_text += f"\nRapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}"

        st.download_button("📄 Raporu İndir", data=rapor_text,
                            file_name=f"sanat_rapor_{rapor['ad']}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain", key="snt_rapor_indir")

    with sub[2]:
        styled_section("👩‍🏫 Öğretmen Paneli — Sınıf Özeti", "#10b981")

        profiller = store.get_all_profiller()
        if not profiller:
            st.info("Henüz öğrenci verisi yok.")
            return

        st.write(f"**Toplam öğrenci:** {len(profiller)}")

        toplam_akt = sum(p.get("toplam_aktivite", 0) for p in profiller)
        toplam_sure = sum(p.get("toplam_sure_dk", 0) for p in profiller)
        aktif_ogrenci = sum(1 for p in profiller if p.get("toplam_aktivite", 0) > 0)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Toplam Aktivite", toplam_akt)
        with col2:
            st.metric("Toplam Süre", f"{toplam_sure} dk")
        with col3:
            st.metric("Aktif Öğrenci", aktif_ogrenci)

        styled_section("📋 Öğrenci Listesi", "#3b82f6")
        for p in profiller:
            akt = p.get("toplam_aktivite", 0)
            puan = 0
            ds = p.get("dal_skorlari", {})
            if ds:
                puan = round(sum(d.get("puan", 0) for d in ds.values()) / len(ds), 0)
            _render_html(f"""
            <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:4px;
                         border:1px solid rgba(99,102,241,0.1);display:flex;justify-content:space-between;align-items:center">
                <span style="font-weight:600;color:#e0e7ff !important;font-size:0.85rem">{p.get('student_name','?')}</span>
                <span style="color:#94a3b8 !important;font-size:0.8rem">{akt} aktivite • {p.get('toplam_sure_dk',0)} dk • Puan: {puan:.0f}</span>
            </div>
            """)


# ═══════════════════════════════════════════════════════════════
# 19) YETENEK TESTİ
# ═══════════════════════════════════════════════════════════════

def _render_yetenek_testi():
    styled_section("🏆 Sanat Yetenek Keşfi", "#eab308")

    _render_html("""
    <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:20px;padding:24px;margin-bottom:20px;
                 border:2px solid rgba(234,179,8,0.4);text-align:center">
        <div style="font-size:2.5rem;margin-bottom:8px">🏆🎨🎵</div>
        <div style="font-weight:700;color:#fde68a !important;font-size:1.2rem">Hangi Sanat Dalına Yatkınsın?</div>
        <div style="color:#fcd34d !important;font-size:0.85rem">10 soruya cevap ver, sanat profilini keşfet!</div>
    </div>
    """)

    sorular = [
        # Görsel Sanatlar soruları
        ("Boş zamanında ne yaparsın?", {"🎨 Çizim/boyama yaparım": "G", "🎵 Müzik dinler/çalarım": "M", "📖 Okur/yazarım": "Y", "✂️ El işi/maket yaparım": "E", "📸 Fotoğraf çekerim": "F", "🎭 Taklit/oyun oynarım": "T"}),
        ("Bir müzede ne dikkatini çeker?", {"🖼️ Tablolar ve resimler": "G", "🎵 Müzik aletleri": "M", "📜 El yazmaları ve kitaplar": "Y", "🏺 Heykeller ve seramikler": "E", "📸 Fotoğraf sergileri": "F", "🎭 Kostümler ve maskeler": "T"}),
        ("Doğada ne ilgini çeker?", {"🌅 Renk tonları ve ışık": "G", "🎵 Kuş sesleri ve rüzgar": "M", "📝 Hikaye ilhamı": "Y", "🌸 Dokular ve şekiller": "E", "📐 Kompozisyon ve çerçeve": "F", "🎭 Hayvan davranışları": "T"}),
        ("Nasıl daha iyi öğrenirsin?", {"👁️ Görerek ve izleyerek": "G", "👂 Dinleyerek": "M", "✍️ Yazarak ve okuyarak": "Y", "🖐️ Dokunarak ve yaparak": "E", "📸 Fotoğraflayarak": "F", "🎭 Canlandırarak": "T"}),
        # Kişilik soruları
        ("Bir hediye hazırlasan ne yaparsın?", {"🎨 Resim çizerim": "G", "🎵 Şarkı besteylerim": "M", "📝 Şiir/mektup yazarım": "Y", "✂️ El yapımı bir şey yaparım": "E", "📸 Fotoğraf albümü hazırlarım": "F", "🎭 Skeç/video çekerim": "T"}),
        ("Hayalindeki meslek?", {"🎨 Ressam/Tasarımcı": "G", "🎵 Müzisyen/Besteci": "M", "📖 Yazar/Şair": "Y", "🏗️ Mimar/Zanaatkar": "E", "📸 Fotoğrafçı/Yönetmen": "F", "🎭 Oyuncu/Komedyen": "T"}),
        ("Film izlerken neye dikkat edersin?", {"🎨 Görsel efektler ve renkler": "G", "🎵 Film müziği": "M", "📝 Senaryo ve diyaloglar": "Y", "🏗️ Set tasarımı ve kostümler": "E", "📸 Kamera açıları": "F", "🎭 Oyunculuk": "T"}),
        ("Stresli olduğunda ne yaparsın?", {"🎨 Çizim yaparım": "G", "🎵 Müzik dinlerim": "M", "📝 Günlük yazarım": "Y", "✂️ El işi yaparım": "E", "🚶 Yürür ve gözlemlerim": "F", "🎭 Komik videolar izlerim": "T"}),
        # Yetenek soruları
        ("Hangi becerin daha güçlü?", {"👁️ Renkleri ayırt etme": "G", "👂 Ritim tutma": "M", "✍️ Kelimelerle ifade": "Y", "🖐️ El becerisi": "E", "📐 Detay görme": "F", "🗣️ İfade ve jest": "T"}),
        ("Okulda en çok hangi ders?", {"🎨 Görsel Sanatlar": "G", "🎵 Müzik": "M", "📝 Türkçe/Edebiyat": "Y", "🔧 Teknoloji Tasarım": "E", "📐 Matematik (geometri)": "F", "🎭 Drama/Beden Eğitimi": "T"}),
        ("Arkadaşların seni nasıl tanımlar?", {"🎨 Yaratıcı ve renkli": "G", "🎵 Müziksever ve ritimli": "M", "📖 Kitap kurdu ve hayal gücü": "Y", "🖐️ Becerikli ve pratik": "E", "👁️ Detaycı ve gözlemci": "F", "🎭 Eğlenceli ve enerjik": "T"}),
        ("Seni en çok ne mutlu eder?", {"🎨 Güzel bir şey yaratmak": "G", "🎵 Müzikle kaybolmak": "M", "📖 Bir hikaye tamamlamak": "Y", "✂️ Ellerimle bir şey üretmek": "E", "📸 Mükemmel bir kare yakalamak": "F", "🎭 İnsanları güldürmek": "T"}),
        ("Bir süper gücün olsa?", {"👁️ Her şeyi renklerde görmek": "G", "👂 Tüm müzikleri duymak": "M", "📝 Düşünceleri yazmak": "Y", "🖐️ Dokunduğunu şekillendirmek": "E", "📸 Zamanı durdurmak": "F", "🎭 Herkes olmak": "T"}),
        ("Tatilde ne yaparsın?", {"🎨 Eskiz defterime çizerim": "G", "🎵 Yeni müzikler keşfederim": "M", "📖 Roman okurum": "Y", "✂️ Hediyelik eşya yaparım": "E", "📸 Her şeyi fotoğraflarım": "F", "🎭 Yeni insanlarla tanışırım": "T"}),
        ("Geleceğin sanat formu?", {"🎨 Dijital resim/3D": "G", "🎵 Elektronik müzik/AI": "M", "📖 İnteraktif hikaye": "Y", "🖐️ 3D baskı sanat": "E", "📸 VR fotoğrafçılık": "F", "🎭 Hologram performans": "T"}),
    ]

    yt_key = "snt_yetenek"
    if yt_key not in st.session_state:
        st.session_state[yt_key] = {}

    st.progress(len(st.session_state.get(yt_key, {})) / len(sorular),
                text=f"İlerleme: {len(st.session_state.get(yt_key, {}))}/{len(sorular)}")

    for i, (soru, secenekler) in enumerate(sorular):
        ans = st.radio(f"**{i+1}.** {soru}", list(secenekler.keys()), index=None, horizontal=True, key=f"snt_yt_q{i}")

        if ans:
            st.session_state[yt_key][str(i)] = secenekler[ans]

    cevap_sayisi = len(st.session_state.get(yt_key, {}))

    if cevap_sayisi >= 10:
        if st.button("🎯 Sanat Profilimi Göster!", key="snt_yt_sonuc", type="primary"):
            cevaplar = list(st.session_state[yt_key].values())
            skorlar = {"G": 0, "M": 0, "Y": 0, "E": 0, "F": 0, "T": 0}
            for c in cevaplar:
                skorlar[c] = skorlar.get(c, 0) + 1

            dal_adlari = {
                "G": ("🎨 Görsel Sanatlar", "#ef4444", "Çizim, resim, heykel, tasarım — görsel dünyayı şekillendirme yeteneğin var!"),
                "M": ("🎵 Müzik", "#3b82f6", "Ritim, melodi, harmoni — müzikle ifade etme yeteneğin güçlü!"),
                "Y": ("✍️ Yaratıcı Yazarlık", "#8b5cf6", "Kelimelerle dünyalar kurma — hikaye anlatıcısı, şair ruhu!"),
                "E": ("✂️ El Sanatları", "#10b981", "Ellerin altın — dokunarak, yaparak, şekillendirerek yaratıyorsun!"),
                "F": ("📸 Fotoğraf & Tasarım", "#06b6d4", "Kompozisyon, detay, çerçeveleme — görsel hikaye anlatıcısı!"),
                "T": ("🎭 Sahne Sanatları", "#f59e0b", "Drama, tiyatro, performans — sahne senin için!"),
            }

            sonuclar = sorted([(dal_adlari[k][0], v, dal_adlari[k][1], dal_adlari[k][2]) for k, v in skorlar.items()], key=lambda x: -x[1])
            en_guclu = sonuclar[0]
            max_puan = max(s[1] for s in sonuclar)

            _render_html(f"""
            <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95);border-radius:24px;padding:28px;margin:16px 0;
                         border:2px solid {en_guclu[2]}60;text-align:center">
                <div style="font-size:3.5rem;margin-bottom:8px">🏆</div>
                <div style="font-size:1.5rem;font-weight:900;color:#fde68a !important">{en_guclu[0]}</div>
                <div style="font-size:0.9rem;color:#c4b5fd !important;margin-top:8px;max-width:500px;display:inline-block">{en_guclu[3]}</div>
            </div>
            """)

            styled_section("📊 Sanat Profili Analizi", "#6366f1")
            for ad, puan, renk, aciklama in sonuclar:
                bar_w = max(5, (puan / max(max_puan, 1)) * 100)
                _render_html(f"""
                <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;border-left:4px solid {renk}">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <span style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{ad}</span>
                        <span style="font-weight:700;color:{renk} !important;font-size:0.9rem">{puan}/{len(cevaplar)}</span>
                    </div>
                    <div style="background:#1e1b4b;border-radius:6px;height:10px;overflow:hidden">
                        <div style="width:{bar_w:.0f}%;height:100%;background:{renk};border-radius:6px"></div>
                    </div>
                </div>
                """)

            # AI Tavsiye
            styled_section("🤖 AI Sanat Koçu Tavsiyesi", "#ec4899")
            tavsiye_map = {
                "G": "Renk teorisi ve perspektif öğren. Dijital çizim araçlarını (Procreate, Krita) dene. Günde 15 dk eskiz yap!",
                "M": "Bir enstrüman seç ve düzenli pratik yap. Müzik teorisi öğren. Nota okumayı pekiştir!",
                "Y": "Günlük tut, kısa hikayeler yaz. Çok oku — okumak yazmanın yakıtıdır. Şiir dene!",
                "E": "Origami ile başla, seramik dene. Farklı malzemeler keşfet. YouTube'da DIY kanallarını takip et!",
                "F": "Üçte bir kuralını uygula. Işık-gölge fark et. Her gün 1 fotoğraf çek ve analiz et!",
                "T": "Drama kulübüne katıl. Ayna karşısında monolog çalış. Farklı karakterleri gözlemle!",
            }
            en_guclu_key = [k for k, v in skorlar.items() if v == max_puan][0]
            _render_html(f"""
            <div style="background:{en_guclu[2]}10;border-radius:14px;padding:16px;border-left:4px solid {en_guclu[2]}">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:6px">💡 Senin İçin Öneriler:</div>
                <div style="color:#94a3b8 !important;font-size:0.85rem;line-height:1.6">{tavsiye_map.get(en_guclu_key, '')}</div>
            </div>
            """)
    elif cevap_sayisi > 0:
        st.info(f"⏳ En az 10 soruyu cevaplamalısın ({cevap_sayisi}/10). Devam et!")


# ═══════════════════════════════════════════════════════════════
# 22) NOSTALJİ KÖŞESİ — Retro Pikap + Dönem Müzikleri
# ═══════════════════════════════════════════════════════════════
# FOTOGRAF STUDYOSU
# ═══════════════════════════════════════════════════════════════

def _render_fotograf_studyosu():
    """Fotograf Studyosu — interaktif HTML5 Canvas fotograf simulasyonu."""
    import streamlit.components.v1 as components

    foto_html = r"""
    <!DOCTYPE html><html><head><meta charset="utf-8"><style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow-x:hidden}
    .container{display:flex;gap:16px;padding:12px;height:620px}
    .preview-area{flex:1;display:flex;flex-direction:column;gap:8px}
    .controls{width:280px;background:#1e293b;border-radius:14px;padding:16px;overflow-y:auto;border:1px solid rgba(99,102,241,0.2)}
    canvas{border-radius:12px;border:2px solid rgba(99,102,241,0.3);cursor:crosshair}
    .ctrl-group{margin-bottom:14px}
    .ctrl-label{font-size:0.75rem;color:#94a3b8;margin-bottom:4px;display:flex;justify-content:space-between}
    .ctrl-label span{color:#a78bfa;font-weight:600}
    input[type=range]{width:100%;accent-color:#7c3aed;height:6px;-webkit-appearance:none;background:#334155;border-radius:3px;outline:none}
    input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#7c3aed;cursor:pointer}
    select{width:100%;background:#334155;color:#e2e8f0;border:1px solid #475569;border-radius:8px;padding:6px 8px;font-size:0.8rem}
    .btn{display:inline-block;padding:8px 16px;border-radius:10px;border:none;cursor:pointer;font-weight:600;font-size:0.82rem;transition:all 0.2s}
    .btn-shoot{background:linear-gradient(135deg,#7c3aed,#6366f1);color:#fff;width:100%;margin-top:6px;font-size:0.95rem;padding:10px}
    .btn-shoot:hover{transform:scale(1.03);box-shadow:0 4px 20px rgba(124,58,237,0.4)}
    .btn-scene{background:#334155;color:#cbd5e1;padding:5px 10px;margin:2px;font-size:0.72rem;border-radius:6px}
    .btn-scene:hover,.btn-scene.active{background:#7c3aed;color:#fff}
    .btn-grid{background:#334155;color:#cbd5e1;padding:5px 10px;font-size:0.72rem;border-radius:6px}
    .btn-grid.active{background:#6366f1;color:#fff}
    .gallery{display:flex;gap:8px;margin-top:8px}
    .gallery canvas{border-radius:8px;border:1px solid #475569;width:120px;height:90px}
    .flash{position:absolute;top:0;left:0;width:100%;height:100%;background:#fff;opacity:0;pointer-events:none;border-radius:12px;transition:opacity 0.15s}
    .preview-wrap{position:relative;flex:1}
    h3{font-size:0.95rem;color:#a78bfa;margin-bottom:10px;border-bottom:1px solid #334155;padding-bottom:6px}
    .scene-bar{display:flex;gap:4px;margin-bottom:10px;flex-wrap:wrap}
    .gallery-title{font-size:0.8rem;color:#94a3b8;margin-top:4px}
    </style></head><body>
    <div class="container">
      <div class="preview-area">
        <div class="preview-wrap">
          <canvas id="mainCanvas" width="580" height="380"></canvas>
          <div class="flash" id="flash"></div>
        </div>
        <div class="gallery-title">Galeri (Son 3 Cekim)</div>
        <div class="gallery" id="gallery"></div>
      </div>
      <div class="controls">
        <h3>Kamera Kontrolleri</h3>
        <div class="scene-bar">
          <button class="btn btn-scene active" onclick="setScene('manzara')">Manzara</button>
          <button class="btn btn-scene" onclick="setScene('portre')">Portre</button>
          <button class="btn btn-scene" onclick="setScene('gece')">Gece</button>
        </div>
        <div class="ctrl-group">
          <div class="ctrl-label">ISO <span id="isoVal">400</span></div>
          <input type="range" id="iso" min="100" max="6400" value="400" step="100">
        </div>
        <div class="ctrl-group">
          <div class="ctrl-label">Diyafram <span id="apVal">f/5.6</span></div>
          <input type="range" id="aperture" min="0" max="10" value="4" step="1">
        </div>
        <div class="ctrl-group">
          <div class="ctrl-label">Enstantane <span id="shutVal">1/125</span></div>
          <input type="range" id="shutter" min="0" max="10" value="5" step="1">
        </div>
        <div class="ctrl-group">
          <div class="ctrl-label">Beyaz Dengesi</div>
          <select id="wb">
            <option value="daylight">Gun Isigi</option>
            <option value="cloudy">Bulutlu</option>
            <option value="tungsten">Tungsten</option>
            <option value="fluorescent">Floresan</option>
          </select>
        </div>
        <div style="margin:10px 0">
          <button class="btn btn-grid" id="gridBtn" onclick="toggleGrid()">Ucler Kurali Izgara</button>
        </div>
        <button class="btn btn-shoot" onclick="shoot()">Cek!</button>
      </div>
    </div>
    <script>
    const cv=document.getElementById('mainCanvas'),ctx=cv.getContext('2d');
    const W=580,H=380;
    let scene='manzara',showGrid=false,gallery=[];
    const AP_VALS=[1.4,2,2.8,4,5.6,8,11,14,16,18,22];
    const SH_VALS=['1s','1/2','1/4','1/8','1/15','1/125','1/250','1/500','1/1000','1/2000','1/4000'];
    const SH_BRIGHT=[2.0,1.7,1.4,1.2,1.1,1.0,0.9,0.8,0.7,0.6,0.5];
    const WB_TINT={daylight:[0,0,0],cloudy:[12,6,-8],tungsten:[-20,-5,30],fluorescent:[-5,10,-5]};

    function drawScene(){
      ctx.clearRect(0,0,W,H);
      if(scene==='manzara'){
        let sky=ctx.createLinearGradient(0,0,0,H*0.6);
        sky.addColorStop(0,'#1e3a5f');sky.addColorStop(1,'#87ceeb');
        ctx.fillStyle=sky;ctx.fillRect(0,0,W,H*0.6);
        ctx.fillStyle='#f59e0b';ctx.beginPath();ctx.arc(W*0.8,H*0.2,35,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='#4a5568';ctx.beginPath();ctx.moveTo(0,H*0.5);ctx.lineTo(W*0.2,H*0.25);ctx.lineTo(W*0.4,H*0.5);ctx.fill();
        ctx.fillStyle='#374151';ctx.beginPath();ctx.moveTo(W*0.3,H*0.5);ctx.lineTo(W*0.55,H*0.2);ctx.lineTo(W*0.8,H*0.5);ctx.fill();
        ctx.fillStyle='#2d6a4f';ctx.fillRect(0,H*0.5,W,H*0.15);
        ctx.fillStyle='#1a759f';ctx.fillRect(0,H*0.65,W,H*0.35);
        ctx.fillStyle='#2d6a4f';
        for(let i=0;i<6;i++){let tx=60+i*95,ty=H*0.48;ctx.beginPath();ctx.moveTo(tx,ty);ctx.lineTo(tx-18,ty+30);ctx.lineTo(tx+18,ty+30);ctx.fill();ctx.fillStyle='#5c3d2e';ctx.fillRect(tx-3,ty+30,6,12);ctx.fillStyle='#2d6a4f';}
      }else if(scene==='portre'){
        let bg=ctx.createLinearGradient(0,0,W,H);
        bg.addColorStop(0,'#1a1a2e');bg.addColorStop(1,'#16213e');
        ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
        ctx.fillStyle='#d4a574';ctx.beginPath();ctx.ellipse(W/2,H*0.35,50,65,0,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='#1a1a2e';ctx.fillRect(W/2-40,H*0.52,80,4);
        ctx.fillStyle='#d4a574';ctx.fillRect(W/2-25,H*0.55,50,80);
        ctx.fillStyle='#4a3728';ctx.beginPath();ctx.ellipse(W/2,H*0.22,55,35,0,Math.PI,Math.PI*2);ctx.fill();
        ctx.fillStyle='#1a1a2e';ctx.beginPath();ctx.arc(W/2-18,H*0.33,5,0,Math.PI*2);ctx.fill();
        ctx.beginPath();ctx.arc(W/2+18,H*0.33,5,0,Math.PI*2);ctx.fill();
        ctx.strokeStyle='#c4957a';ctx.lineWidth=2;ctx.beginPath();ctx.arc(W/2,H*0.42,8,0.1*Math.PI,0.9*Math.PI);ctx.stroke();
      }else{
        ctx.fillStyle='#0a0a1a';ctx.fillRect(0,0,W,H);
        ctx.fillStyle='#c0c0c0';for(let i=0;i<80;i++){ctx.beginPath();ctx.arc(Math.random()*W,Math.random()*H*0.7,Math.random()*1.5+0.5,0,Math.PI*2);ctx.fill();}
        ctx.fillStyle='#e8e8d0';ctx.beginPath();ctx.arc(W*0.75,H*0.18,40,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='#c8c8b0';ctx.beginPath();ctx.arc(W*0.73,H*0.16,12,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='#1a1a2e';ctx.fillRect(0,H*0.75,W,H*0.25);
        ctx.fillStyle='#f59e0b';for(let i=0;i<8;i++){ctx.beginPath();ctx.arc(40+i*70,H*0.82,3,0,Math.PI*2);ctx.fill();}
      }
    }

    function applyEffects(){
      let iso=+document.getElementById('iso').value;
      let apIdx=+document.getElementById('aperture').value;
      let shIdx=+document.getElementById('shutter').value;
      let wb=document.getElementById('wb').value;
      let imgData=ctx.getImageData(0,0,W,H);
      let d=imgData.data;
      let brightness=(iso/400)*SH_BRIGHT[shIdx];
      let tint=WB_TINT[wb];
      let noiseAmt=Math.max(0,(iso-400)/6000)*60;
      let apVal=AP_VALS[apIdx];
      let dofBlur=apVal<4?1:0;
      for(let i=0;i<d.length;i+=4){
        d[i]=Math.min(255,Math.max(0,d[i]*brightness+tint[0]+(Math.random()-0.5)*noiseAmt));
        d[i+1]=Math.min(255,Math.max(0,d[i+1]*brightness+tint[1]+(Math.random()-0.5)*noiseAmt));
        d[i+2]=Math.min(255,Math.max(0,d[i+2]*brightness+tint[2]+(Math.random()-0.5)*noiseAmt));
      }
      ctx.putImageData(imgData,0,0);
      if(dofBlur){
        let edgeW=Math.round((4-apVal)/4*60);
        ctx.save();ctx.filter='blur(3px)';
        ctx.drawImage(cv,0,0,edgeW,H,0,0,edgeW,H);
        ctx.drawImage(cv,W-edgeW,0,edgeW,H,W-edgeW,0,edgeW,H);
        ctx.filter='none';ctx.restore();
      }
      if(shIdx<3){
        ctx.save();ctx.globalAlpha=0.15*(3-shIdx);ctx.filter='blur(4px)';
        ctx.drawImage(cv,2,0);ctx.filter='none';ctx.globalAlpha=1;ctx.restore();
      }
    }

    function drawGrid(){
      if(!showGrid)return;
      ctx.save();ctx.strokeStyle='rgba(255,255,255,0.35)';ctx.lineWidth=1;ctx.setLineDash([6,4]);
      ctx.beginPath();ctx.moveTo(W/3,0);ctx.lineTo(W/3,H);ctx.stroke();
      ctx.beginPath();ctx.moveTo(2*W/3,0);ctx.lineTo(2*W/3,H);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,H/3);ctx.lineTo(W,H/3);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,2*H/3);ctx.lineTo(W,2*H/3);ctx.stroke();
      ctx.setLineDash([]);ctx.restore();
    }

    function render(){drawScene();applyEffects();drawGrid();}

    function setScene(s){
      scene=s;
      document.querySelectorAll('.btn-scene').forEach(b=>b.classList.remove('active'));
      event.target.classList.add('active');
      render();
    }
    function toggleGrid(){
      showGrid=!showGrid;
      document.getElementById('gridBtn').classList.toggle('active',showGrid);
      render();
    }
    function shoot(){
      let fl=document.getElementById('flash');fl.style.opacity='0.8';
      setTimeout(()=>{fl.style.opacity='0';},120);
      let snap=document.createElement('canvas');snap.width=120;snap.height=90;
      snap.getContext('2d').drawImage(cv,0,0,120,90);
      gallery.unshift(snap);if(gallery.length>3)gallery.pop();
      let gal=document.getElementById('gallery');gal.innerHTML='';
      gallery.forEach(c=>{gal.appendChild(c);});
    }

    document.querySelectorAll('input[type=range],select').forEach(el=>{
      el.addEventListener('input',()=>{
        document.getElementById('isoVal').textContent=document.getElementById('iso').value;
        let ai=+document.getElementById('aperture').value;
        document.getElementById('apVal').textContent='f/'+AP_VALS[ai];
        let si=+document.getElementById('shutter').value;
        document.getElementById('shutVal').textContent=SH_VALS[si];
        render();
      });
    });
    render();
    </script></body></html>
    """
    components.html(foto_html, height=650)


# ═══════════════════════════════════════════════════════════════
# ANIMASYON STUDYOSU
# ═══════════════════════════════════════════════════════════════

def _render_animasyon_studyosu():
    """Animasyon Studyosu — kare kare animasyon araci."""
    import streamlit.components.v1 as components

    anim_html = r"""
    <!DOCTYPE html><html><head><meta charset="utf-8"><style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:#0f172a;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;overflow-x:hidden}
    .main{padding:12px;display:flex;flex-direction:column;gap:10px;height:670px}
    .top-row{display:flex;gap:14px}
    .canvas-area{position:relative;background:#1e293b;border-radius:14px;padding:12px;border:1px solid rgba(99,102,241,0.2)}
    .tools{width:200px;background:#1e293b;border-radius:14px;padding:14px;border:1px solid rgba(99,102,241,0.2)}
    canvas#drawCanvas{background:#1a1a2e;border-radius:10px;cursor:crosshair;display:block}
    canvas#onionCanvas{position:absolute;top:12px;left:12px;border-radius:10px;pointer-events:none;opacity:0.25}
    h3{font-size:0.85rem;color:#a78bfa;margin-bottom:10px;border-bottom:1px solid #334155;padding-bottom:5px}
    .tool-row{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px}
    .tbtn{padding:5px 9px;border-radius:7px;border:1px solid #475569;background:#334155;color:#cbd5e1;cursor:pointer;font-size:0.72rem;transition:all 0.15s}
    .tbtn:hover,.tbtn.active{background:#7c3aed;color:#fff;border-color:#7c3aed}
    .color-btn{width:24px;height:24px;border-radius:6px;border:2px solid transparent;cursor:pointer;transition:all 0.15s}
    .color-btn.active{border-color:#fff;transform:scale(1.15)}
    .size-btn{padding:4px 8px;border-radius:6px;border:1px solid #475569;background:#334155;color:#cbd5e1;cursor:pointer;font-size:0.7rem}
    .size-btn.active{background:#6366f1;color:#fff}
    .timeline{background:#1e293b;border-radius:14px;padding:10px 14px;border:1px solid rgba(99,102,241,0.2);display:flex;align-items:center;gap:8px;overflow-x:auto}
    .frame-thumb{width:60px;height:45px;border-radius:6px;border:2px solid #475569;cursor:pointer;transition:all 0.15s;flex-shrink:0}
    .frame-thumb.active{border-color:#7c3aed;box-shadow:0 0 10px rgba(124,58,237,0.4)}
    .frame-thumb:hover{border-color:#6366f1}
    .playbar{display:flex;align-items:center;gap:8px;background:#1e293b;border-radius:12px;padding:8px 14px;border:1px solid rgba(99,102,241,0.2)}
    .pbtn{padding:6px 14px;border-radius:8px;border:none;cursor:pointer;font-weight:600;font-size:0.78rem;transition:all 0.15s}
    .pbtn-play{background:linear-gradient(135deg,#10b981,#059669);color:#fff}
    .pbtn-stop{background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff}
    .pbtn-add{background:linear-gradient(135deg,#7c3aed,#6366f1);color:#fff}
    .pbtn-dup{background:#334155;color:#cbd5e1}
    .pbtn-del{background:#7f1d1d;color:#fca5a5}
    .pbtn:hover{transform:scale(1.04)}
    .frame-count{font-size:0.8rem;color:#a78bfa;font-weight:600;min-width:80px;text-align:center}
    .fps-ctrl{display:flex;align-items:center;gap:6px;font-size:0.75rem;color:#94a3b8}
    .fps-ctrl input{width:70px;accent-color:#7c3aed}
    .onion-toggle{display:flex;align-items:center;gap:6px;font-size:0.75rem;color:#94a3b8;cursor:pointer}
    .onion-toggle input{accent-color:#7c3aed}
    </style></head><body>
    <div class="main">
      <div class="top-row">
        <div class="canvas-area">
          <canvas id="onionCanvas" width="400" height="300"></canvas>
          <canvas id="drawCanvas" width="400" height="300"></canvas>
        </div>
        <div class="tools">
          <h3>Cizim Araclari</h3>
          <div class="tool-row">
            <button class="tbtn active" onclick="setTool('pencil')" id="tool_pencil">Kalem</button>
            <button class="tbtn" onclick="setTool('eraser')" id="tool_eraser">Silgi</button>
          </div>
          <div style="font-size:0.72rem;color:#94a3b8;margin-bottom:4px">Kalem Boyutu</div>
          <div class="tool-row">
            <button class="size-btn active" onclick="setSize(2)" id="sz2">Ince</button>
            <button class="size-btn" onclick="setSize(5)" id="sz5">Orta</button>
            <button class="size-btn" onclick="setSize(10)" id="sz10">Kalin</button>
          </div>
          <div style="font-size:0.72rem;color:#94a3b8;margin:8px 0 4px">Renkler</div>
          <div class="tool-row" id="colorPalette"></div>
          <div style="margin-top:14px">
            <label class="onion-toggle"><input type="checkbox" id="onionCb" onchange="toggleOnion()"> Onion Skinning</label>
          </div>
        </div>
      </div>
      <div class="playbar">
        <button class="pbtn pbtn-add" onclick="newFrame()">Yeni Kare</button>
        <button class="pbtn pbtn-dup" onclick="dupFrame()">Kopyala</button>
        <button class="pbtn pbtn-del" onclick="delFrame()">Sil</button>
        <div style="width:1px;height:24px;background:#334155"></div>
        <button class="pbtn pbtn-play" onclick="play()" id="playBtn">Oynat</button>
        <button class="pbtn pbtn-stop" onclick="stop()">Durdur</button>
        <div class="fps-ctrl">FPS: <input type="range" id="fps" min="2" max="12" value="6"><span id="fpsVal">6</span></div>
        <div style="flex:1"></div>
        <div class="frame-count" id="frameCount">Kare 1/1</div>
        <button class="pbtn pbtn-play" onclick="exportGif()" style="background:linear-gradient(135deg,#f59e0b,#d97706)">GIF Kaydet</button>
      </div>
      <div class="timeline" id="timeline"></div>
    </div>
    <script>
    const cv=document.getElementById('drawCanvas'),ctx=cv.getContext('2d');
    const ocv=document.getElementById('onionCanvas'),octx=ocv.getContext('2d');
    const COLORS=['#e2e8f0','#ef4444','#f59e0b','#10b981','#3b82f6','#8b5cf6','#ec4899','#1a1a2e'];
    let frames=[],curIdx=0,tool='pencil',penSize=2,penColor=COLORS[0],drawing=false,onion=false,playing=false,playTimer=null;

    function initPalette(){
      let p=document.getElementById('colorPalette');
      COLORS.forEach((c,i)=>{
        let b=document.createElement('div');b.className='color-btn'+(i===0?' active':'');
        b.style.background=c;b.onclick=()=>{penColor=c;document.querySelectorAll('.color-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');};
        p.appendChild(b);
      });
    }

    function clearCanvas(){ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,400,300);}
    function saveFrame(){let d=cv.toDataURL();frames[curIdx]=d;}
    function loadFrame(){let img=new Image();img.onload=()=>{ctx.clearRect(0,0,400,300);ctx.drawImage(img,0,0);};img.src=frames[curIdx];}
    function updateOnion(){
      octx.clearRect(0,0,400,300);
      if(!onion||curIdx===0)return;
      let img=new Image();img.onload=()=>{octx.globalAlpha=1;octx.drawImage(img,0,0);};img.src=frames[curIdx-1];
    }

    function updateTimeline(){
      let tl=document.getElementById('timeline');tl.innerHTML='';
      frames.forEach((f,i)=>{
        let c=document.createElement('canvas');c.width=60;c.height=45;c.className='frame-thumb'+(i===curIdx?' active':'');
        let img=new Image();img.onload=()=>{c.getContext('2d').drawImage(img,0,0,60,45);};img.src=f;
        c.onclick=()=>{saveFrame();curIdx=i;loadFrame();updateOnion();updateTimeline();updateCount();};
        let wrap=document.createElement('div');wrap.style.position='relative';wrap.style.flexShrink='0';
        let num=document.createElement('div');num.style.cssText='position:absolute;top:-2px;left:2px;font-size:0.6rem;color:#7c3aed;font-weight:700';num.textContent=i+1;
        wrap.appendChild(c);wrap.appendChild(num);tl.appendChild(wrap);
      });
    }
    function updateCount(){document.getElementById('frameCount').textContent='Kare '+(curIdx+1)+'/'+frames.length;}

    function newFrame(){saveFrame();clearCanvas();frames.push(cv.toDataURL());curIdx=frames.length-1;updateOnion();updateTimeline();updateCount();}
    function dupFrame(){saveFrame();frames.splice(curIdx+1,0,frames[curIdx]);curIdx++;loadFrame();updateOnion();updateTimeline();updateCount();}
    function delFrame(){
      if(frames.length<=1){clearCanvas();frames[0]=cv.toDataURL();updateTimeline();return;}
      frames.splice(curIdx,1);if(curIdx>=frames.length)curIdx=frames.length-1;
      loadFrame();updateOnion();updateTimeline();updateCount();
    }

    function play(){
      if(playing)return;if(frames.length<2)return;
      playing=true;saveFrame();let fps=+document.getElementById('fps').value;let i=0;
      document.getElementById('playBtn').textContent='Oynuyor...';
      playTimer=setInterval(()=>{
        curIdx=i%frames.length;loadFrame();updateTimeline();updateCount();i++;
      },1000/fps);
    }
    function stop(){playing=false;clearInterval(playTimer);document.getElementById('playBtn').textContent='Oynat';}
    function exportGif(){play();setTimeout(()=>{stop();},frames.length*200+500);}

    function setTool(t){
      tool=t;document.getElementById('tool_pencil').classList.toggle('active',t==='pencil');
      document.getElementById('tool_eraser').classList.toggle('active',t==='eraser');
    }
    function setSize(s){
      penSize=s;document.querySelectorAll('.size-btn').forEach(b=>b.classList.remove('active'));
      document.getElementById('sz'+s).classList.add('active');
    }
    function toggleOnion(){onion=document.getElementById('onionCb').checked;updateOnion();}

    cv.addEventListener('mousedown',e=>{if(playing)return;drawing=true;ctx.beginPath();ctx.moveTo(e.offsetX,e.offsetY);});
    cv.addEventListener('mousemove',e=>{
      if(!drawing||playing)return;
      ctx.lineWidth=tool==='eraser'?penSize*3:penSize;
      ctx.lineCap='round';ctx.lineJoin='round';
      ctx.strokeStyle=tool==='eraser'?'#1a1a2e':penColor;
      ctx.lineTo(e.offsetX,e.offsetY);ctx.stroke();
    });
    cv.addEventListener('mouseup',()=>{drawing=false;});
    cv.addEventListener('mouseleave',()=>{drawing=false;});

    document.getElementById('fps').addEventListener('input',e=>{document.getElementById('fpsVal').textContent=e.target.value;});

    // Init
    initPalette();clearCanvas();frames.push(cv.toDataURL());updateTimeline();updateCount();
    </script></body></html>
    """
    components.html(anim_html, height=700)


# ═══════════════════════════════════════════════════════════════
# 24) RENK ALGI TESTI
# ═══════════════════════════════════════════════════════════════

def _render_renk_algi_testi():
    import streamlit.components.v1 as components
    styled_section("Renk Algi Testi (Ishihara)", "#8b5cf6")
    components.html("""
    <div id="renk-algi-app" style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);border-radius:18px;padding:24px;color:#e2e8f0;font-family:'Segoe UI',sans-serif;min-height:600px;">
      <h3 style="text-align:center;color:#c4b5fd;margin-bottom:8px;">Ishihara Renk Koru Testi</h3>
      <p style="text-align:center;color:#94a3b8;font-size:13px;margin-bottom:18px;">Her plakada gizlenen sayiyi asagidaki kutuya yazin. 8 plaka uzerinden degerlendirileceksiniz.</p>
      <div id="ra-plates" style="display:flex;flex-wrap:wrap;gap:16px;justify-content:center;"></div>
      <div style="text-align:center;margin-top:18px;">
        <button onclick="raCheckAnswers()" style="background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;border:none;border-radius:12px;padding:12px 32px;font-size:15px;cursor:pointer;font-weight:600;">Sonuclari Goster</button>
      </div>
      <div id="ra-result" style="text-align:center;margin-top:16px;font-size:16px;font-weight:600;min-height:24px;"></div>
      <div style="margin-top:24px;background:rgba(139,92,246,0.1);border-radius:14px;padding:18px;border:1px solid rgba(139,92,246,0.2);">
        <h4 style="color:#c4b5fd;margin-bottom:10px;">Renk Koru Turleri</h4>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
          <div style="background:rgba(0,0,0,0.3);border-radius:10px;padding:14px;">
            <div style="font-weight:700;color:#f87171;margin-bottom:6px;">Protanopi</div>
            <div style="font-size:12px;color:#94a3b8;">Kirmizi reseptorlerinde eksiklik. Kirmizi ve yesil tonlari ayirt etmekte zorluk.</div>
          </div>
          <div style="background:rgba(0,0,0,0.3);border-radius:10px;padding:14px;">
            <div style="font-weight:700;color:#4ade80;margin-bottom:6px;">Deuteranopi</div>
            <div style="font-size:12px;color:#94a3b8;">Yesil reseptorlerinde eksiklik. En yaygin renk koru turu (%5 erkeklerde).</div>
          </div>
          <div style="background:rgba(0,0,0,0.3);border-radius:10px;padding:14px;">
            <div style="font-weight:700;color:#60a5fa;margin-bottom:6px;">Tritanopi</div>
            <div style="font-size:12px;color:#94a3b8;">Mavi reseptorlerinde eksiklik. Mavi-sari tonlarini ayirt etmekte zorluk. Nadir gorulur.</div>
          </div>
        </div>
      </div>
      <script>
      (function(){
        const plates = [
          {num:'12', bgH:[0,20,340,350], numH:[100,120,130,140], label:'12'},
          {num:'8',  bgH:[100,110,120,130], numH:[0,10,350,5], label:'8'},
          {num:'5',  bgH:[20,30,40,50], numH:[200,210,220,230], label:'5'},
          {num:'3',  bgH:[0,10,350,355], numH:[90,100,110,115], label:'3'},
          {num:'29', bgH:[30,40,50,55], numH:[270,280,290,300], label:'29'},
          {num:'74', bgH:[180,190,200,170], numH:[0,10,350,340], label:'74'},
          {num:'6',  bgH:[260,270,280,250], numH:[50,60,70,40], label:'6'},
          {num:'15', bgH:[90,100,110,80], numH:[30,40,50,20], label:'15'}
        ];
        const container = document.getElementById('ra-plates');
        plates.forEach((p, idx) => {
          const wrap = document.createElement('div');
          wrap.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:6px;';
          const cvs = document.createElement('canvas');
          cvs.width = 200; cvs.height = 200;
          cvs.style.cssText = 'border-radius:50%;border:3px solid rgba(139,92,246,0.3);cursor:crosshair;';
          const ctx = cvs.getContext('2d');
          // fill background
          ctx.beginPath(); ctx.arc(100,100,100,0,Math.PI*2); ctx.fillStyle='#1e1b4b'; ctx.fill(); ctx.clip();
          // draw bg dots
          for(let i=0;i<600;i++){
            const x=Math.random()*200, y=Math.random()*200;
            const dx=x-100, dy=y-100;
            if(dx*dx+dy*dy>9800) continue;
            const r=3+Math.random()*5;
            const h=p.bgH[Math.floor(Math.random()*p.bgH.length)];
            const s=50+Math.random()*30;
            const l=40+Math.random()*25;
            ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2);
            ctx.fillStyle='hsl('+h+','+s+'%,'+l+'%)'; ctx.fill();
          }
          // draw number with dots
          const numCvs = document.createElement('canvas');
          numCvs.width=200; numCvs.height=200;
          const nctx = numCvs.getContext('2d');
          nctx.font='bold 80px Arial'; nctx.textAlign='center'; nctx.textBaseline='middle';
          nctx.fillStyle='#fff'; nctx.fillText(p.num,100,105);
          const imgData = nctx.getImageData(0,0,200,200).data;
          for(let i=0;i<800;i++){
            const x=20+Math.random()*160, y=30+Math.random()*150;
            const px=Math.floor(x), py=Math.floor(y);
            const off=(py*200+px)*4;
            if(imgData[off+3]>128){
              const r2=3+Math.random()*5;
              const h2=p.numH[Math.floor(Math.random()*p.numH.length)];
              const s2=55+Math.random()*30;
              const l2=45+Math.random()*20;
              ctx.beginPath(); ctx.arc(x,y,r2,0,Math.PI*2);
              ctx.fillStyle='hsl('+h2+','+s2+'%,'+l2+'%)'; ctx.fill();
            }
          }
          const inp = document.createElement('input');
          inp.type='text'; inp.maxLength=3; inp.id='ra-inp-'+idx;
          inp.placeholder='Sayi?';
          inp.style.cssText='width:80px;text-align:center;background:#1e1b4b;color:#e2e8f0;border:1px solid rgba(139,92,246,0.3);border-radius:8px;padding:6px;font-size:14px;';
          wrap.appendChild(cvs); wrap.appendChild(inp);
          container.appendChild(wrap);
        });
        window.raCheckAnswers = function(){
          let correct=0;
          plates.forEach((p,i)=>{
            const v=document.getElementById('ra-inp-'+i).value.trim();
            if(v===p.label) correct++;
          });
          const el=document.getElementById('ra-result');
          if(correct>=6){
            el.innerHTML='<span style="color:#4ade80;">Sonuc: '+correct+'/8 dogru - Normal renk gorusu</span>';
          } else {
            el.innerHTML='<span style="color:#f87171;">Sonuc: '+correct+'/8 dogru - Olasi renk koru - goz doktoruna danisin</span>';
          }
        };
      })();
      </script>
    </div>
    """, height=600)


# ═══════════════════════════════════════════════════════════════
# 25) HEYKEL STUDYOSU
# ═══════════════════════════════════════════════════════════════

def _render_heykel_studyosu():
    import streamlit.components.v1 as components
    styled_section("3D Heykel Studyosu", "#8b5cf6")
    components.html("""
    <div id="heykel-app" style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);border-radius:18px;padding:24px;color:#e2e8f0;font-family:'Segoe UI',sans-serif;min-height:650px;">
      <h3 style="text-align:center;color:#c4b5fd;margin-bottom:16px;">3D Heykel Studyosu</h3>
      <div style="display:flex;gap:20px;flex-wrap:wrap;">
        <!-- Controls -->
        <div style="flex:0 0 220px;display:flex;flex-direction:column;gap:10px;">
          <div style="background:rgba(0,0,0,0.3);border-radius:12px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">Sekil Sec</div>
            <div id="hs-shapes" style="display:flex;flex-wrap:wrap;gap:6px;"></div>
          </div>
          <div style="background:rgba(0,0,0,0.3);border-radius:12px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">Malzeme</div>
            <div id="hs-materials" style="display:flex;flex-wrap:wrap;gap:6px;"></div>
          </div>
          <div style="background:rgba(0,0,0,0.3);border-radius:12px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">Renk</div>
            <input type="color" id="hs-color" value="#a78bfa" style="width:100%;height:32px;border:none;border-radius:6px;cursor:pointer;">
          </div>
          <div style="background:rgba(0,0,0,0.3);border-radius:12px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">Boyut: <span id="hs-size-val">100</span>px</div>
            <input type="range" id="hs-size" min="60" max="200" value="100" style="width:100%;">
          </div>
          <div style="background:rgba(0,0,0,0.3);border-radius:12px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Kendi Yontun</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px;">
              <button class="hs-add-btn" data-shape="cube" style="flex:1;min-width:60px;background:#4c1d95;color:#e2e8f0;border:none;border-radius:6px;padding:6px;cursor:pointer;font-size:11px;">+Kup</button>
              <button class="hs-add-btn" data-shape="sphere" style="flex:1;min-width:60px;background:#4c1d95;color:#e2e8f0;border:none;border-radius:6px;padding:6px;cursor:pointer;font-size:11px;">+Kure</button>
              <button class="hs-add-btn" data-shape="cylinder" style="flex:1;min-width:60px;background:#4c1d95;color:#e2e8f0;border:none;border-radius:6px;padding:6px;cursor:pointer;font-size:11px;">+Silindir</button>
            </div>
            <button id="hs-clear-custom" style="width:100%;margin-top:6px;background:#7f1d1d;color:#fca5a5;border:none;border-radius:6px;padding:6px;cursor:pointer;font-size:11px;">Temizle</button>
          </div>
        </div>
        <!-- 3D Viewport -->
        <div style="flex:1;min-width:300px;">
          <div id="hs-viewport" style="width:100%;height:400px;background:radial-gradient(ellipse at center,#1e1b4b 0%,#0f0a1e 100%);border-radius:16px;border:2px solid rgba(139,92,246,0.2);perspective:800px;display:flex;align-items:center;justify-content:center;overflow:hidden;cursor:grab;position:relative;">
            <div id="hs-scene" style="transform-style:preserve-3d;transition:none;position:relative;"></div>
          </div>
          <div style="text-align:center;margin-top:8px;color:#64748b;font-size:12px;">Fare ile surukleyerek dondur</div>
        </div>
      </div>
      <script>
      (function(){
        const shapes=['Kup','Silindir','Piramit','Kure','Torus','Yildiz','Vazo','Heykel'];
        const materials=[
          {name:'Mermer',bg:'linear-gradient(135deg,#e2e8f0,#f8fafc,#cbd5e1,#f1f5f9)'},
          {name:'Bronz',bg:'linear-gradient(135deg,#b45309,#d97706,#fbbf24,#d97706)'},
          {name:'Tahta',bg:'linear-gradient(135deg,#78350f,#92400e,#a16207,#78350f)'},
          {name:'Cam',bg:'linear-gradient(135deg,rgba(139,92,246,0.3),rgba(99,102,241,0.2),rgba(167,139,250,0.15))'}
        ];
        let rotX=-20, rotY=30, dragging=false, lastX=0, lastY=0;
        let curShape='Kup', curMat=materials[0], curColor='#a78bfa', curSize=100;
        let customParts=[];
        const shapesDiv=document.getElementById('hs-shapes');
        shapes.forEach(s=>{
          const b=document.createElement('button');
          b.textContent=s; b.style.cssText='background:'+(s===curShape?'#7c3aed':'#1e1b4b')+';color:#e2e8f0;border:1px solid rgba(139,92,246,0.3);border-radius:8px;padding:5px 10px;cursor:pointer;font-size:11px;';
          b.onclick=()=>{ curShape=s; customParts=[]; updateShapeButtons(); renderShape(); };
          shapesDiv.appendChild(b);
        });
        function updateShapeButtons(){
          Array.from(shapesDiv.children).forEach((b,i)=>{ b.style.background=shapes[i]===curShape?'#7c3aed':'#1e1b4b'; });
        }
        const matsDiv=document.getElementById('hs-materials');
        materials.forEach((m,i)=>{
          const b=document.createElement('button');
          b.textContent=m.name; b.style.cssText='background:'+(i===0?'#7c3aed':'#1e1b4b')+';color:#e2e8f0;border:1px solid rgba(139,92,246,0.3);border-radius:8px;padding:5px 10px;cursor:pointer;font-size:11px;';
          b.onclick=()=>{ curMat=m; Array.from(matsDiv.children).forEach((bb,j)=>{ bb.style.background=j===i?'#7c3aed':'#1e1b4b'; }); renderShape(); };
          matsDiv.appendChild(b);
        });
        document.getElementById('hs-size').oninput=function(){ curSize=+this.value; document.getElementById('hs-size-val').textContent=curSize; renderShape(); };
        document.getElementById('hs-color').oninput=function(){ curColor=this.value; renderShape(); };

        function getCSSShape(type, sz, mat, clr, offY){
          offY=offY||0;
          const base='position:absolute;left:50%;top:50%;';
          const bg=mat.name==='Cam'?mat.bg.replace(/rgba\\(/g,'rgba(').replace(/0\\.[0-9]+\\)/g,(m)=>m): mat.bg!==materials[0].bg?mat.bg:'linear-gradient(135deg,'+clr+','+lighten(clr)+')';
          const opacity=mat.name==='Cam'?'opacity:0.6;':'';
          if(type==='Kup'||type==='cube'){
            const h=sz/2;
            let faces='';
            const faceStyles=[
              'transform:rotateY(0deg) translateZ('+h+'px);',
              'transform:rotateY(180deg) translateZ('+h+'px);',
              'transform:rotateY(90deg) translateZ('+h+'px);',
              'transform:rotateY(-90deg) translateZ('+h+'px);',
              'transform:rotateX(90deg) translateZ('+h+'px);',
              'transform:rotateX(-90deg) translateZ('+h+'px);'
            ];
            faceStyles.forEach(fs=>{
              faces+='<div style="position:absolute;width:'+sz+'px;height:'+sz+'px;background:'+bg+';border:1px solid rgba(255,255,255,0.15);'+fs+opacity+'"></div>';
            });
            return '<div style="'+base+'transform-style:preserve-3d;width:'+sz+'px;height:'+sz+'px;margin-left:-'+h+'px;margin-top:'+(-h+offY)+'px;">'+faces+'</div>';
          }
          if(type==='Kure'||type==='sphere'){
            return '<div style="'+base+'width:'+sz+'px;height:'+sz+'px;margin-left:-'+sz/2+'px;margin-top:'+(-sz/2+offY)+'px;border-radius:50%;background:'+bg+';box-shadow:inset -'+sz/4+'px -'+sz/4+'px '+sz/2+'px rgba(0,0,0,0.4), 0 0 '+sz/3+'px rgba(139,92,246,0.2);'+opacity+'"></div>';
          }
          if(type==='Silindir'||type==='cylinder'){
            return '<div style="'+base+'width:'+sz*0.7+'px;height:'+sz+'px;margin-left:-'+sz*0.35+'px;margin-top:'+(-sz/2+offY)+'px;border-radius:'+sz*0.35+'px/20px;background:'+bg+';box-shadow:inset -15px 0 30px rgba(0,0,0,0.3);'+opacity+'"></div>';
          }
          if(type==='Piramit'){
            return '<div style="'+base+'width:0;height:0;margin-left:-'+sz/2+'px;margin-top:'+(-sz/2+offY)+'px;border-left:'+sz/2+'px solid transparent;border-right:'+sz/2+'px solid transparent;border-bottom:'+sz+'px solid '+clr+';filter:drop-shadow(0 4px 15px rgba(139,92,246,0.3));'+opacity+'"></div>';
          }
          if(type==='Torus'){
            return '<div style="'+base+'width:'+sz+'px;height:'+sz+'px;margin-left:-'+sz/2+'px;margin-top:'+(-sz/2+offY)+'px;border-radius:50%;border:'+sz/5+'px solid '+clr+';background:transparent;box-shadow:inset 0 0 '+sz/4+'px rgba(0,0,0,0.5), 0 0 20px rgba(139,92,246,0.2);'+opacity+'"></div>';
          }
          if(type==='Yildiz'){
            const pts=5, outer=sz/2, inner=sz/5;
            let d=''; for(let i=0;i<pts*2;i++){ const a=Math.PI/2*3+i*Math.PI/pts; const r=i%2===0?outer:inner; d+=(i===0?'M':'L')+(100+Math.cos(a)*r)+','+(100+Math.sin(a)*r); } d+='Z';
            return '<svg style="'+base+'margin-left:-100px;margin-top:'+(-100+offY)+'px;" width="200" height="200"><path d="'+d+'" fill="'+clr+'" stroke="rgba(255,255,255,0.2)" stroke-width="1" filter="drop-shadow(0 0 10px rgba(139,92,246,0.3))"/></svg>';
          }
          if(type==='Vazo'){
            return '<svg style="'+base+'margin-left:-'+sz/2+'px;margin-top:'+(-sz*0.7+offY)+'px;" width="'+sz+'" height="'+sz*1.4+'"><path d="M'+sz*0.35+' 0 Q'+sz*0.15+' '+sz*0.3+' '+sz*0.1+' '+sz*0.7+' Q'+sz*0.05+' '+sz+' '+sz*0.3+' '+sz*1.3+' L'+sz*0.7+' '+sz*1.3+' Q'+sz*0.95+' '+sz+' '+sz*0.9+' '+sz*0.7+' Q'+sz*0.85+' '+sz*0.3+' '+sz*0.65+' 0 Z" fill="'+clr+'" stroke="rgba(255,255,255,0.15)" stroke-width="1"/></svg>';
          }
          // Heykel (bust-like)
          return '<div style="'+base+'display:flex;flex-direction:column;align-items:center;margin-left:-'+sz*0.3+'px;margin-top:'+(-sz*0.7+offY)+'px;"><div style="width:'+sz*0.4+'px;height:'+sz*0.5+'px;border-radius:50% 50% 45% 45%;background:'+bg+';'+opacity+'"></div><div style="width:'+sz*0.25+'px;height:'+sz*0.15+'px;background:'+bg+';'+opacity+'"></div><div style="width:'+sz*0.6+'px;height:'+sz*0.35+'px;border-radius:10px 10px 0 0;background:'+bg+';'+opacity+'"></div></div>';
        }
        function lighten(c){ const n=parseInt(c.slice(1),16); let r=Math.min(255,(n>>16)+60); let g=Math.min(255,((n>>8)&0xff)+60); let b=Math.min(255,(n&0xff)+60); return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1); }

        const scene=document.getElementById('hs-scene');
        const vp=document.getElementById('hs-viewport');
        function renderShape(){
          if(customParts.length>0){
            let html='';
            customParts.forEach((p,i)=>{ html+=getCSSShape(p, curSize*0.6, curMat, curColor, (i-Math.floor(customParts.length/2))*curSize*0.35); });
            scene.innerHTML=html;
          } else {
            scene.innerHTML=getCSSShape(curShape, curSize, curMat, curColor, 0);
          }
          scene.style.transform='rotateX('+rotX+'deg) rotateY('+rotY+'deg)';
        }
        vp.addEventListener('mousedown',e=>{ dragging=true; lastX=e.clientX; lastY=e.clientY; vp.style.cursor='grabbing'; });
        document.addEventListener('mousemove',e=>{ if(!dragging) return; rotY+=(e.clientX-lastX)*0.5; rotX+=(e.clientY-lastY)*0.5; lastX=e.clientX; lastY=e.clientY; scene.style.transform='rotateX('+rotX+'deg) rotateY('+rotY+'deg)'; });
        document.addEventListener('mouseup',()=>{ dragging=false; vp.style.cursor='grab'; });
        document.querySelectorAll('.hs-add-btn').forEach(b=>{ b.onclick=()=>{ customParts.push(b.dataset.shape); curShape=''; updateShapeButtons(); renderShape(); }; });
        document.getElementById('hs-clear-custom').onclick=()=>{ customParts=[]; curShape='Kup'; updateShapeButtons(); renderShape(); };
        renderShape();
      })();
      </script>
    </div>
    """, height=650)


# ═══════════════════════════════════════════════════════════════
# 26) MUZIK BESTECISI
# ═══════════════════════════════════════════════════════════════

def _render_muzik_bestecisi():
    import streamlit.components.v1 as components
    styled_section("Muzik Bestecisi", "#8b5cf6")
    components.html("""
    <div id="muzik-app" style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);border-radius:18px;padding:24px;color:#e2e8f0;font-family:'Segoe UI',sans-serif;min-height:550px;">
      <h3 style="text-align:center;color:#c4b5fd;margin-bottom:6px;">Melodi Bestecisi</h3>
      <p style="text-align:center;color:#94a3b8;font-size:13px;margin-bottom:16px;">Nota paletinden bir nota sec, sonra zaman cizgisinde bir hucreye tikla. Oynat ile dinle!</p>
      <!-- Controls -->
      <div style="display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;margin-bottom:14px;">
        <div style="display:flex;align-items:center;gap:6px;">
          <span style="font-size:12px;color:#94a3b8;">Tempo:</span>
          <input type="range" id="mb-tempo" min="60" max="180" value="120" style="width:100px;">
          <span id="mb-tempo-val" style="font-size:12px;color:#c4b5fd;">120 BPM</span>
        </div>
        <div style="display:flex;align-items:center;gap:6px;">
          <span style="font-size:12px;color:#94a3b8;">Enstruman:</span>
          <select id="mb-instrument" style="background:#1e1b4b;color:#e2e8f0;border:1px solid rgba(139,92,246,0.3);border-radius:6px;padding:4px 8px;font-size:12px;">
            <option value="sine">Piyano</option>
            <option value="sawtooth">Gitar</option>
            <option value="triangle">Flut</option>
            <option value="square">Org</option>
          </select>
        </div>
        <button onclick="mbPlay()" id="mb-play-btn" style="background:linear-gradient(135deg,#059669,#10b981);color:#fff;border:none;border-radius:8px;padding:8px 20px;cursor:pointer;font-weight:600;font-size:13px;">Oynat</button>
        <button onclick="mbClear()" style="background:linear-gradient(135deg,#7f1d1d,#dc2626);color:#fff;border:none;border-radius:8px;padding:8px 16px;cursor:pointer;font-size:13px;">Temizle</button>
        <button onclick="mbRandom()" style="background:linear-gradient(135deg,#4c1d95,#7c3aed);color:#fff;border:none;border-radius:8px;padding:8px 16px;cursor:pointer;font-size:13px;">Rastgele</button>
      </div>
      <!-- Presets -->
      <div style="display:flex;gap:8px;justify-content:center;margin-bottom:14px;">
        <span style="font-size:12px;color:#94a3b8;line-height:28px;">Hazir:</span>
        <button onclick="mbPreset('kucukyildiz')" style="background:#1e1b4b;color:#c4b5fd;border:1px solid rgba(139,92,246,0.3);border-radius:6px;padding:4px 12px;cursor:pointer;font-size:11px;">Kucuk Yildiz</button>
        <button onclick="mbPreset('jingle')" style="background:#1e1b4b;color:#c4b5fd;border:1px solid rgba(139,92,246,0.3);border-radius:6px;padding:4px 12px;cursor:pointer;font-size:11px;">Jingle Bells</button>
        <button onclick="mbPreset('ode')" style="background:#1e1b4b;color:#c4b5fd;border:1px solid rgba(139,92,246,0.3);border-radius:6px;padding:4px 12px;cursor:pointer;font-size:11px;">Ode to Joy</button>
      </div>
      <!-- Note Palette -->
      <div style="display:flex;gap:6px;justify-content:center;margin-bottom:12px;" id="mb-palette"></div>
      <!-- Timeline -->
      <div style="overflow-x:auto;padding:4px 0;">
        <div style="display:flex;gap:2px;min-width:max-content;margin-bottom:4px;" id="mb-bar-labels"></div>
        <div style="display:flex;gap:2px;min-width:max-content;" id="mb-timeline"></div>
      </div>
      <script>
      (function(){
        const notes=['Do','Re','Mi','Fa','Sol','La','Si','Sus'];
        const freqs=[261.63,293.66,329.63,349.23,392.00,440.00,493.88,0];
        const colors=['#ef4444','#f97316','#eab308','#22c55e','#3b82f6','#8b5cf6','#ec4899','#475569'];
        let selectedNote=-1;
        let timeline=new Array(16).fill(-1);
        let playing=false;
        const palette=document.getElementById('mb-palette');
        notes.forEach((n,i)=>{
          const b=document.createElement('button');
          b.textContent=n;
          b.style.cssText='width:52px;height:42px;border-radius:10px;border:2px solid '+(i<7?colors[i]:'#475569')+';background:'+(i<7?colors[i]+'22':'#1e293b')+';color:'+colors[i]+';cursor:pointer;font-weight:700;font-size:13px;transition:all 0.2s;';
          b.onclick=()=>{ selectedNote=i; palette.querySelectorAll('button').forEach((bb,j)=>{ bb.style.transform=j===i?'scale(1.15)':'scale(1)'; bb.style.boxShadow=j===i?'0 0 12px '+colors[j]:'none'; }); };
          palette.appendChild(b);
        });
        // Bar labels
        const barLabels=document.getElementById('mb-bar-labels');
        for(let b=0;b<4;b++){
          const d=document.createElement('div');
          d.textContent='Olcu '+(b+1);
          d.style.cssText='width:200px;text-align:center;font-size:11px;color:#64748b;flex-shrink:0;';
          if(b<3){ const sp=document.createElement('div'); sp.style.width='2px'; barLabels.appendChild(d); } else barLabels.appendChild(d);
        }
        // Timeline cells
        const tl=document.getElementById('mb-timeline');
        for(let i=0;i<16;i++){
          const cell=document.createElement('div');
          cell.id='mb-cell-'+i;
          cell.style.cssText='width:48px;height:60px;border-radius:8px;background:#1e1b4b;border:1px solid rgba(139,92,246,0.15);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#64748b;transition:all 0.15s;flex-shrink:0;';
          cell.textContent=(i+1);
          cell.onclick=()=>{
            if(selectedNote<0) return;
            timeline[i]=selectedNote;
            renderTimeline();
          };
          cell.oncontextmenu=(e)=>{ e.preventDefault(); timeline[i]=-1; renderTimeline(); };
          tl.appendChild(cell);
          // bar separator
          if((i+1)%4===0 && i<15){ const sep=document.createElement('div'); sep.style.cssText='width:3px;background:rgba(139,92,246,0.2);border-radius:2px;flex-shrink:0;'; tl.appendChild(sep); }
        }
        function renderTimeline(){
          for(let i=0;i<16;i++){
            const cell=document.getElementById('mb-cell-'+i);
            const n=timeline[i];
            if(n>=0){
              cell.style.background=colors[n]+'33';
              cell.style.borderColor=colors[n];
              cell.style.color=colors[n];
              cell.textContent=notes[n];
            } else {
              cell.style.background='#1e1b4b';
              cell.style.borderColor='rgba(139,92,246,0.15)';
              cell.style.color='#64748b';
              cell.textContent=(i+1);
            }
          }
        }
        document.getElementById('mb-tempo').oninput=function(){ document.getElementById('mb-tempo-val').textContent=this.value+' BPM'; };

        window.mbPlay=function(){
          if(playing) return;
          playing=true;
          const btn=document.getElementById('mb-play-btn');
          btn.textContent='Caliniyor...'; btn.style.opacity='0.6';
          const ac=new (window.AudioContext||window.webkitAudioContext)();
          const tempo=+document.getElementById('mb-tempo').value;
          const beatDur=60/tempo;
          const wave=document.getElementById('mb-instrument').value;
          timeline.forEach((n,i)=>{
            const cell=document.getElementById('mb-cell-'+i);
            setTimeout(()=>{
              cell.style.transform='scale(1.2)';
              cell.style.boxShadow=n>=0?'0 0 15px '+colors[n]:'0 0 8px rgba(100,116,139,0.3)';
              setTimeout(()=>{ cell.style.transform='scale(1)'; cell.style.boxShadow='none'; }, beatDur*800);
            }, i*beatDur*1000);
            if(n>=0 && freqs[n]>0){
              const osc=ac.createOscillator();
              const gain=ac.createGain();
              osc.type=wave; osc.frequency.value=freqs[n];
              gain.gain.setValueAtTime(0.3, ac.currentTime+i*beatDur);
              gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime+i*beatDur+beatDur*0.9);
              osc.connect(gain); gain.connect(ac.destination);
              osc.start(ac.currentTime+i*beatDur);
              osc.stop(ac.currentTime+i*beatDur+beatDur);
            }
          });
          setTimeout(()=>{ playing=false; btn.textContent='Oynat'; btn.style.opacity='1'; }, 16*beatDur*1000+200);
        };
        window.mbClear=function(){ timeline.fill(-1); renderTimeline(); };
        window.mbRandom=function(){
          for(let i=0;i<16;i++) timeline[i]=Math.random()<0.2?7:Math.floor(Math.random()*7);
          renderTimeline();
        };
        const presets={
          kucukyildiz:[0,0,4,4,5,5,4,-1,3,3,2,2,1,1,0,-1],
          jingle:[2,2,2,-1,2,2,2,-1,2,4,0,1,2,-1,-1,-1],
          ode:[2,2,3,4,4,3,2,1,0,0,1,2,2,1,1,-1]
        };
        window.mbPreset=function(name){
          const p=presets[name]; if(!p) return;
          for(let i=0;i<16;i++) timeline[i]=p[i];
          renderTimeline();
        };
      })();
      </script>
    </div>
    """, height=550)


# ═══════════════════════════════════════════════════════════════

def _render_nostalji_kosesi():
    """Nostalji Kosesi — retro pikap ile donem muzikleri."""
    import streamlit.components.v1 as components

    # 3D CSS PİKAP MODELİ — st.markdown ile (iframe degil, her zaman yuklenir)
    _render_html("""
    <div style="perspective:800px;max-width:500px;margin:20px auto">
    <!-- ANA GOVDE -->
    <div style="position:relative;width:460px;height:320px;margin:0 auto;
        background:linear-gradient(180deg,#a1887f 0%,#8d6e63 3%,#795548 8%,#6d4c41 50%,#5d4037 92%,#4e342e 100%);
        border-radius:18px 18px 12px 12px;
        box-shadow:0 20px 50px rgba(0,0,0,.6),0 8px 20px rgba(0,0,0,.4),
                   inset 0 2px 4px rgba(255,255,255,.08),inset 0 -3px 6px rgba(0,0,0,.3);
        border:2px solid #3e2723;
        transform:rotateX(5deg)">
        <!-- AHSAP DAMAR DOKUSU -->
        <div style="position:absolute;inset:0;border-radius:18px 18px 12px 12px;
            background:repeating-linear-gradient(88deg,transparent,transparent 15px,rgba(0,0,0,.02) 15px,rgba(0,0,0,.02) 16px),
            repeating-linear-gradient(92deg,transparent,transparent 25px,rgba(139,105,20,.015) 25px,rgba(139,105,20,.015) 26px);
            pointer-events:none"></div>
        <!-- KOSE METAL AKSAMLAR -->
        <div style="position:absolute;top:6px;left:6px;width:12px;height:12px;border-radius:50%;
            background:radial-gradient(circle at 40% 35%,#d4a850,#8b6914);box-shadow:0 1px 3px rgba(0,0,0,.5)"></div>
        <div style="position:absolute;top:6px;right:6px;width:12px;height:12px;border-radius:50%;
            background:radial-gradient(circle at 40% 35%,#d4a850,#8b6914);box-shadow:0 1px 3px rgba(0,0,0,.5)"></div>
        <div style="position:absolute;bottom:6px;left:6px;width:12px;height:12px;border-radius:50%;
            background:radial-gradient(circle at 40% 35%,#d4a850,#8b6914);box-shadow:0 1px 3px rgba(0,0,0,.5)"></div>
        <div style="position:absolute;bottom:6px;right:6px;width:12px;height:12px;border-radius:50%;
            background:radial-gradient(circle at 40% 35%,#d4a850,#8b6914);box-shadow:0 1px 3px rgba(0,0,0,.5)"></div>
        <!-- UST BOLME — PLAK ALANI -->
        <div style="position:absolute;top:10px;left:12px;right:12px;height:55%;
            background:linear-gradient(180deg,#5d4037,#4e342e);border-radius:10px 10px 0 0;
            border:1px solid #3e2723;box-shadow:inset 0 3px 10px rgba(0,0,0,.4)">
            <!-- PLAK -->
            <div style="position:absolute;top:50%;left:40%;width:140px;height:140px;
                transform:translate(-50%,-50%);border-radius:50%;
                background:conic-gradient(#111,#222,#111,#222,#111,#222,#111,#222,#111,#222,#111,#222);
                box-shadow:0 3px 12px rgba(0,0,0,.5),inset 0 0 20px rgba(0,0,0,.3);
                animation:spinPlak 3s linear infinite">
                <!-- PLAK OLUKLAR -->
                <div style="position:absolute;inset:8px;border-radius:50%;
                    border:1px solid rgba(255,255,255,.02);
                    box-shadow:inset 0 0 0 6px rgba(255,255,255,.01),inset 0 0 0 12px rgba(255,255,255,.01),
                    inset 0 0 0 20px rgba(255,255,255,.01),inset 0 0 0 28px rgba(255,255,255,.01)"></div>
                <!-- ALTIN ETİKET -->
                <div style="position:absolute;top:50%;left:50%;width:44px;height:44px;
                    transform:translate(-50%,-50%);border-radius:50%;
                    background:radial-gradient(circle at 40% 35%,#f0d060,#d4a017,#8b6914);
                    border:2px solid #5d4037;box-shadow:inset 0 1px 3px rgba(255,255,255,.3)">
                    <!-- MERKEZ DELIK -->
                    <div style="position:absolute;top:50%;left:50%;width:6px;height:6px;
                        transform:translate(-50%,-50%);border-radius:50%;background:#3e2723"></div>
                </div>
            </div>
            <!-- PİKAP KOLU -->
            <div style="position:absolute;top:10%;right:15%;width:4px;height:85px;
                background:linear-gradient(180deg,#c0c0c0,#999,#777);border-radius:2px;
                transform-origin:top center;transform:rotate(-8deg);
                box-shadow:1px 2px 4px rgba(0,0,0,.3)">
                <!-- KOL PİVOT -->
                <div style="position:absolute;top:-5px;left:-5px;width:14px;height:14px;border-radius:50%;
                    background:radial-gradient(circle at 40% 35%,#d4d4d4,#888);border:1px solid #666;
                    box-shadow:0 1px 4px rgba(0,0,0,.4)"></div>
                <!-- KOL IGNE -->
                <div style="position:absolute;bottom:-10px;left:-4px;width:12px;height:8px;
                    background:linear-gradient(180deg,#888,#555);border-radius:0 0 3px 3px"></div>
            </div>
        </div>
        <!-- ALT BOLME — RADYO PANELİ -->
        <div style="position:absolute;bottom:0;left:0;width:100%;height:40%;
            background:linear-gradient(180deg,#5d4037 0%,#4e342e 40%,#3e2723 100%);
            border-top:2px solid #6d4c41;border-radius:0 0 12px 12px;
            display:flex;align-items:center;justify-content:center;gap:12px;padding:0 20px">
            <!-- SOL HOPARLOR -->
            <div style="width:75px;height:38px;border-radius:4px;border:2px solid #5d4037;
                background:repeating-linear-gradient(90deg,#4e342e 0px,#4e342e 2px,#3e2723 2px,#3e2723 4px);
                box-shadow:inset 0 2px 4px rgba(0,0,0,.3)"></div>
            <!-- SOL DUGME -->
            <div style="width:26px;height:26px;border-radius:50%;
                background:radial-gradient(circle at 40% 35%,#d4a850,#b8860b,#8b6914);
                border:2px solid #5d4037;box-shadow:0 2px 6px rgba(0,0,0,.4),inset 0 1px 2px rgba(255,215,0,.2)">
                <div style="width:2px;height:8px;background:#5d4037;margin:4px auto 0;border-radius:1px"></div>
            </div>
            <!-- LCD RADYO EKRANI -->
            <div style="width:130px;height:30px;border-radius:4px;
                background:linear-gradient(180deg,#2a2a1a,#1a1a0a);border:2px solid #5d4037;
                display:flex;align-items:center;justify-content:center;
                font-family:monospace;font-size:10px;color:#d4a017;letter-spacing:1px;
                box-shadow:inset 0 2px 4px rgba(0,0,0,.5)">
                FM 98.5 MHz
            </div>
            <!-- SAG DUGME -->
            <div style="width:26px;height:26px;border-radius:50%;
                background:radial-gradient(circle at 40% 35%,#d4a850,#b8860b,#8b6914);
                border:2px solid #5d4037;box-shadow:0 2px 6px rgba(0,0,0,.4),inset 0 1px 2px rgba(255,215,0,.2)">
                <div style="width:2px;height:8px;background:#5d4037;margin:4px auto 0;border-radius:1px"></div>
            </div>
            <!-- SAG HOPARLOR -->
            <div style="width:75px;height:38px;border-radius:4px;border:2px solid #5d4037;
                background:repeating-linear-gradient(90deg,#4e342e 0px,#4e342e 2px,#3e2723 2px,#3e2723 4px);
                box-shadow:inset 0 2px 4px rgba(0,0,0,.3)"></div>
        </div>
    </div>
    </div>
    <style>@keyframes spinPlak{to{transform:translate(-50%,-50%) rotate(360deg)}}</style>
    <div style="text-align:center;margin-top:8px">
        <div style="font-size:1.3rem;font-weight:800;color:#fde68a">Nostalji Kosesi</div>
        <div style="font-size:0.8rem;color:#d97706">70ler, 80ler, 90lar... Retro pikap ile muzik zamani!</div>
    </div>
    """)

    # HİBRİT MÜZİK SİSTEMİ — 3 mod
    nost_tabs = st.tabs(["Radyo Modu (YouTube)", "Pikap Modu (Sentez)", "Klasik Muzik (Telifsiz)"])

    # ── MOD 1: RADYO — YouTube Embed ──
    with nost_tabs[0]:
        styled_section("Radyo Modu — Gercek Sarkilar", "#d97706")
        donem = st.radio("Donem Sec", ["70ler", "80ler", "90lar"], horizontal=True, key="nost_donem")

        # YouTube nostalji playlist/video ID'leri
        yt_map = {
            "70ler": [
                ("Baris Manco - Gulpembe", "KmF9YBJ77Vo"),
                ("Baris Manco - Hal Hal", "fa2L-A2sS-4"),
                ("Cem Karaca - Tamirci Ciragi", "388-ZnlMoO4"),
                ("Erkin Koray - Cemalim", "U0gjwpMb-k8"),
                ("Baris Manco - Nick the Chopper", "bGu7-xwcxYE"),
            ],
            "80ler": [
                ("Sezen Aksu - Firuze", "3vNtVJ7dGxg"),
                ("Sezen Aksu - Hadi Bakalim", "m0YLDqIkgb0"),
                ("Kayahan - Gonul Sayfam", "6ZK8Is46A6k"),
                ("Ajda Pekkan - Oyalama Beni", "5DLI4dEllPM"),
            ],
            "90lar": [
                ("Tarkan - Simarik", "cpp69ghR1IM"),
                ("Tarkan - Dudu", "SCZgGVqVsbY"),
                ("Sertab Erener - Everyway That I Can", "J36xlUUEv1U"),
                ("Teoman - Istanbulda Sonbahar", "XFvSd1HDagY"),
                ("Athena - Holigan", "l7MA8kG11rA"),
                ("Mor ve Otesi - Cambaz", "kifhkJIcjpc"),
            ],
        }

        sarkilar = yt_map.get(donem, [])
        for ad, vid in sarkilar:
            with st.expander(ad):
                st.components.v1.html(
                    f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/{vid}" '
                    f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
                    height=220)

    # ── MOD 2: PİKAP — Web Audio Sentez ──
    with nost_tabs[1]:
        styled_section("Pikap Modu — Melodi Sentez", "#8b5cf6")
        st.caption("Telifsiz melodiler — Web Audio ile sentezleniyor")
        components.html("""
<html><body style="margin:0;background:#0B0F19;font-family:Georgia,serif;color:#e2e8f0">
<div style="max-width:820px;margin:0 auto;padding:10px">
<!-- BASLIK -->
<div style="text-align:center;padding:16px;background:linear-gradient(135deg,#1a0a0a,#2d1b0e,#4a2c17);border-radius:16px;border:2px solid rgba(217,119,6,.4);margin-bottom:14px">
<div style="font-size:2.5rem">&#128251;&#127925;&#127926;</div>
<h2 style="color:#fde68a;margin:6px 0">Nostalji Kosesi</h2>
<p style="color:#fbbf24;font-size:13px;margin:0">70ler, 80ler, 90lar... Retro pikap ile muzik zamani!</p>
</div>
<!-- PIKAP -->
<div id="pk" style="position:relative;width:420px;height:280px;margin:0 auto 12px;background:linear-gradient(180deg,#8d6e63,#6d4c41,#4e342e);border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.5);border:2px solid #3e2723;overflow:hidden">
<!-- Ust — plak alani -->
<div style="position:absolute;top:0;left:0;width:100%;height:58%;background:linear-gradient(180deg,#795548,#5d4037);border-bottom:2px solid #4e342e">
<!-- Plak -->
<div id="pl" style="position:absolute;top:50%;left:38%;width:120px;height:120px;transform:translate(-50%,-50%);border-radius:50%;background:conic-gradient(#111,#222,#111,#222,#111,#222,#111,#222);box-shadow:0 2px 10px rgba(0,0,0,.5)">
<div style="position:absolute;top:50%;left:50%;width:32px;height:32px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle at 40% 35%,#f0d060,#d4a017,#8b6914);border:2px solid #5d4037"></div>
</div>
<!-- Kol -->
<div id="kl" style="position:absolute;top:8%;right:18%;width:3px;height:70px;background:linear-gradient(180deg,#bbb,#888);border-radius:2px;transform-origin:top center;transform:rotate(-30deg);transition:transform .5s">
<div style="position:absolute;top:-4px;left:-4px;width:10px;height:10px;border-radius:50%;background:radial-gradient(circle,#ccc,#888);border:1px solid #666"></div>
<div style="position:absolute;bottom:-7px;left:-3px;width:9px;height:6px;background:#666;border-radius:0 0 3px 3px"></div>
</div>
</div>
<!-- Alt — radyo panel -->
<div style="position:absolute;bottom:0;left:0;width:100%;height:42%;background:linear-gradient(180deg,#5d4037,#3e2723);border-top:2px solid #6d4c41;border-radius:0 0 14px 14px;display:flex;align-items:center;justify-content:center;gap:8px;padding:0 14px">
<div style="width:65px;height:32px;background:repeating-linear-gradient(90deg,#4e342e 0px,#4e342e 2px,#3e2723 2px,#3e2723 4px);border:1px solid #5d4037;border-radius:3px"></div>
<div style="width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#d4a850,#8b6914);border:2px solid #5d4037"></div>
<div id="ek" style="width:110px;height:24px;background:#1a1a0a;border:1px solid #5d4037;border-radius:3px;display:flex;align-items:center;justify-content:center;font-family:monospace;font-size:9px;color:#d4a017">FM 98.5</div>
<div style="width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#d4a850,#8b6914);border:2px solid #5d4037"></div>
<div style="width:65px;height:32px;background:repeating-linear-gradient(90deg,#4e342e 0px,#4e342e 2px,#3e2723 2px,#3e2723 4px);border:1px solid #5d4037;border-radius:3px"></div>
</div>
</div>
<!-- DONEM BUTONLARI -->
<div style="display:flex;gap:6px;justify-content:center;margin:10px 0;flex-wrap:wrap">
<button class="db ac" data-d="70">70ler</button>
<button class="db" data-d="80">80ler</button>
<button class="db" data-d="90">90lar</button>
<button class="db" data-d="turk">Turk Pop</button>
<button class="db" data-d="klasik">Klasik</button>
</div>
<!-- KONTROLLER -->
<div style="display:flex;gap:8px;justify-content:center;align-items:center;margin:8px 0">
<button class="ct" id="bp">&#9664;&#9664;</button>
<button class="ct py" id="bpp">&#9654;</button>
<button class="ct" id="bn">&#9654;&#9654;</button>
<span style="color:#78716c;font-size:10px;margin-left:6px">Ses:</span>
<input type="range" id="vs" min="0" max="100" value="60" style="width:80px;accent-color:#d97706">
</div>
<div id="np" style="text-align:center;font-size:12px;color:#94a3b8;font-style:italic;margin:4px 0">Donem sec, oynat bas</div>
<!-- SARKI LISTESI -->
<div id="ls" style="background:#0f172a;border-radius:8px;padding:8px;border:1px solid rgba(217,119,6,.15);max-height:200px;overflow-y:auto;margin:8px 0"></div>
<!-- DONEM BILGILERI -->
<div style="margin-top:10px">
<div style="background:#0f172a;border-radius:8px;padding:8px 12px;margin-bottom:4px;border-left:3px solid #b45309"><b style="color:#fde68a">70ler</b><br><span style="font-size:11px;color:#94a3b8">Baris Manco, Cem Karaca, Erkin Koray. Anadolu Rock altin cagi.</span></div>
<div style="background:#0f172a;border-radius:8px;padding:8px 12px;margin-bottom:4px;border-left:3px solid #7c3aed"><b style="color:#c4b5fd">80ler</b><br><span style="font-size:11px;color:#94a3b8">Arabesk + Turk Pop. Ferdi Tayfur, Sezen Aksu, Kayahan.</span></div>
<div style="background:#0f172a;border-radius:8px;padding:8px 12px;margin-bottom:4px;border-left:3px solid #0891b2"><b style="color:#67e8f9">90lar</b><br><span style="font-size:11px;color:#94a3b8">Tarkan dunyaya acildi. MFO, Ebru Gundes. MTV donemi.</span></div>
<div style="background:#0f172a;border-radius:8px;padding:8px 12px;margin-bottom:4px;border-left:3px solid #dc2626"><b style="color:#fca5a5">Turk Pop</b><br><span style="font-size:11px;color:#94a3b8">Ajda Pekkan, Zeki Muren, Muazzez Ersoy. Klasik isimler.</span></div>
<div style="background:#0f172a;border-radius:8px;padding:8px 12px;border-left:3px solid #16a34a"><b style="color:#86efac">Klasik</b><br><span style="font-size:11px;color:#94a3b8">Beethoven, Mozart, Vivaldi. Yuzyillarin besteleri.</span></div>
</div>
</div>
<style>
.db{padding:7px 14px;border-radius:7px;border:2px solid #5d4037;background:linear-gradient(180deg,#3e2723,#2e1b0e);color:#d4a017;cursor:pointer;font-size:12px;font-weight:700;transition:all .2s;font-family:Georgia}
.db:hover{background:linear-gradient(180deg,#5d4037,#3e2723);transform:translateY(-2px)}
.db.ac{background:linear-gradient(180deg,#d97706,#b45309);color:#fff;border-color:#f59e0b;box-shadow:0 3px 10px rgba(217,119,6,.4)}
.ct{width:36px;height:36px;border-radius:50%;border:2px solid #5d4037;background:linear-gradient(180deg,#3e2723,#2e1b0e);color:#d4a017;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;transition:all .15s}
.ct:hover{background:linear-gradient(180deg,#5d4037,#3e2723);transform:scale(1.1)}
.ct.py{width:44px;height:44px;background:linear-gradient(180deg,#d97706,#b45309);color:#fff;border-color:#f59e0b;font-size:18px}
.sk{display:flex;align-items:center;gap:6px;padding:5px 8px;border-radius:5px;cursor:pointer;transition:all .12s;color:#94a3b8;font-size:12px}
.sk:hover{background:rgba(217,119,6,.06);color:#fde68a}
.sk.pl{background:rgba(217,119,6,.12);color:#fbbf24;font-weight:700}
#pl.sp{animation:ro 2s linear infinite}
@keyframes ro{to{transform:translate(-50%,-50%) rotate(360deg)}}
</style>
<script>
var pk=document.getElementById('pk'),pl=document.getElementById('pl'),kl=document.getElementById('kl');
var np=document.getElementById('np'),ls=document.getElementById('ls'),vs=document.getElementById('vs');
var ek=document.getElementById('ek');
var AC=null,on=false,ci=0,cd='70',tm=null;
var M={'70':[{a:'Yesil Yesil',s:'Baris Manco',n:[[330,300],[370,300],[415,300],[440,600],[370,300],[330,600]]},{a:'Dona Dona',s:'Baris Manco',n:[[262,400],[294,400],[330,400],[349,800],[330,400],[294,400],[262,800]]},{a:'Uzun Ince Bir Yoldayim',s:'Asik Veysel',n:[[440,500],[494,500],[523,500],[587,1000],[523,500],[494,500],[440,1000]]},{a:'Gurbet',s:'Zeki Muren',n:[[349,400],[392,400],[440,400],[523,800],[440,400],[392,800]]},{a:'Sari Gelin',s:'Halk Muzigi',n:[[294,500],[330,500],[349,500],[392,500],[440,1000],[392,500],[349,500],[330,1000]]},{a:'Cemberimde Gul Oya',s:'Baris Manco',n:[[330,300],[370,300],[415,600],[370,300],[330,300],[294,600],[330,800]]}],
'80':[{a:'Seni Seviyorum',s:'Kayahan',n:[[523,400],[587,400],[659,400],[698,800],[659,400],[587,400],[523,800]]},{a:'Firuze',s:'Sezen Aksu',n:[[587,400],[659,400],[698,800],[659,400],[587,400],[523,800]]},{a:'Ask Laftan Anlamaz',s:'Ferdi Tayfur',n:[[294,500],[330,500],[349,800],[392,500],[440,500],[392,800],[349,1000]]},{a:'Islak Islak',s:'Sezen Aksu',n:[[440,400],[523,400],[587,800],[523,400],[440,400],[392,800]]},{a:'Hatasiz Kul Olmaz',s:'Kivircik Ali',n:[[330,500],[349,500],[392,500],[440,500],[523,1000],[440,500],[392,1000]]},{a:'Ahh Istanbul',s:'MFO',n:[[440,300],[494,300],[523,600],[494,300],[440,300],[392,600],[440,800]]}],
'90':[{a:'Simarik',s:'Tarkan',n:[[659,200],[698,200],[784,400],[698,200],[659,200],[587,400],[659,200],[698,200],[784,800]]},{a:'Seni Dusundum',s:'Tarkan',n:[[523,300],[587,300],[659,600],[587,300],[523,300],[494,600],[523,800]]},{a:'Firtinalar',s:'MFO',n:[[440,300],[494,300],[523,300],[587,600],[523,300],[494,300],[440,600]]},{a:'Hani Benim Gencligim',s:'Ibrahim Tatlises',n:[[392,400],[440,400],[494,400],[523,800],[494,400],[440,800]]},{a:'Dokunmayin Bana',s:'Ebru Gundes',n:[[349,400],[392,400],[440,800],[523,400],[440,400],[392,800]]},{a:'Sev Kardesim',s:'Baris Manco',n:[[330,300],[349,300],[392,300],[440,600],[392,300],[349,300],[330,600]]}],
'turk':[{a:'Duydum Ki Unutmussun',s:'Ajda Pekkan',n:[[523,400],[587,400],[659,800],[587,400],[523,400],[494,800]]},{a:'Sorma Kalbim',s:'Zeki Muren',n:[[330,400],[349,400],[392,800],[440,400],[392,400],[349,800]]},{a:'Sevda Yelleri',s:'Selda Bagcan',n:[[294,500],[330,500],[392,500],[440,800],[392,500],[330,500],[294,800]]},{a:'Daglarin Kizi Reyhan',s:'Baris Manco',n:[[440,300],[494,300],[523,300],[587,600],[659,300],[587,300],[523,600]]},{a:'Gel Barissak',s:'Muslum Gurses',n:[[349,500],[392,500],[440,500],[523,800],[440,500],[349,800]]},{a:'Yalnizlik Senfonisi',s:'Muazzez Ersoy',n:[[440,500],[523,500],[587,500],[659,1000],[587,500],[523,1000]]}],
'klasik':[{a:'Fur Elise',s:'Beethoven',n:[[659,200],[622,200],[659,200],[622,200],[659,200],[494,200],[587,200],[523,200],[440,800]]},{a:'Ay Isigi Sonati',s:'Beethoven',n:[[277,600],[330,600],[415,600],[277,600],[330,600],[415,600]]},{a:'Turk Marsi',s:'Mozart',n:[[494,200],[440,200],[415,200],[440,200],[523,400],[0,200],[587,200],[523,200],[494,200],[523,200],[659,400]]},{a:'Canon',s:'Pachelbel',n:[[587,500],[523,500],[494,500],[440,500],[392,500],[349,500],[392,500],[440,500]]},{a:'Bahar',s:'Vivaldi',n:[[659,300],[659,300],[659,300],[587,600],[659,300],[659,300],[659,300],[587,600]]},{a:'Habanera',s:'Bizet',n:[[523,300],[494,300],[466,300],[440,300],[415,300],[440,600],[0,300],[440,300]]}]};
function bld(){var sg=M[cd]||[];ls.innerHTML='';sg.forEach(function(s,i){var d=document.createElement('div');d.className='sk'+(i===ci?' pl':'');d.innerHTML='<span style="color:#64748b;font-size:10px;min-width:16px">'+(i+1)+'</span><span style="flex:1">'+s.a+'</span><span style="color:#78716c;font-size:11px">'+s.s+'</span>';d.onclick=function(){ci=i;go()};ls.appendChild(d)})}
function go(){stp();var sg=M[cd]||[];if(!sg.length)return;if(ci>=sg.length)ci=0;if(ci<0)ci=sg.length-1;
var s=sg[ci];np.textContent=s.s+' - '+s.a;ek.textContent=s.a.substring(0,14);
pl.classList.add('sp');kl.style.transform='rotate(-3deg)';on=true;
document.getElementById('bpp').innerHTML='&#9646;&#9646;';bld();
if(!AC)AC=new(window.AudioContext||window.webkitAudioContext)();
var t=AC.currentTime,v=vs.value/100;
s.n.forEach(function(n){if(n[0]>0){var o=AC.createOscillator(),g=AC.createGain();o.type='triangle';o.frequency.value=n[0];g.gain.setValueAtTime(v*.3,t);g.gain.exponentialRampToValueAtTime(.001,t+n[1]/1000);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+n[1]/1000)}t+=n[1]/1000});
var tot=s.n.reduce(function(a,n){return a+n[1]},0);
tm=setTimeout(function(){if(on){ci++;go()}},tot+400)}
function stp(){on=false;pl.classList.remove('sp');kl.style.transform='rotate(-30deg)';document.getElementById('bpp').innerHTML='&#9654;';if(tm)clearTimeout(tm);if(AC){try{AC.close()}catch(e){}AC=null}}
document.querySelectorAll('.db').forEach(function(b){b.onclick=function(){document.querySelectorAll('.db').forEach(function(x){x.classList.remove('ac')});b.classList.add('ac');cd=b.dataset.d;ci=0;stp();bld();np.textContent=(M[cd]||[]).length+' sarki hazir'}});
document.getElementById('bpp').onclick=function(){if(on)stp();else go()};
document.getElementById('bn').onclick=function(){ci++;if(on)go();else bld()};
document.getElementById('bp').onclick=function(){ci--;if(ci<0)ci=(M[cd]||[]).length-1;if(on)go();else bld()};
bld();
</script>
</body></html>
    """, height=650)

    # ── MOD 3: KLASİK MÜZİK — Telifsiz Public Domain ──
    with nost_tabs[2]:
        styled_section("Klasik Muzik — Tamamen Telifsiz", "#16a34a")
        st.caption("70+ yillik eserler — Public Domain. Tamamen yasal ve ucretsiz.")

        klasik_sarkilar = [
            ("Beethoven - Fur Elise", "wfF0zHeU3Zs"),
            ("Beethoven - Moonlight Sonata", "4Tr0otuiQuU"),
            ("Beethoven - 5. Senfoni", "fOk8Tm815lE"),
            ("Mozart - Kucuk Gece Muzigi", "o1FSN8_pp_o"),
            ("Mozart - Turk Marsi", "quxTnEEETbo"),
            ("Mozart - 40. Senfoni", "JTc1mDieQI8"),
            ("Vivaldi - Dort Mevsim (Bahar)", "l-dYNttdgl0"),
            ("Vivaldi - Dort Mevsim (Yaz)", "Nx5c_JZIM6M"),
            ("Pachelbel - Canon in D", "NlprozGcs80"),
            ("Bach - Air on G String", "GMkmQlfOJDk"),
            ("Bach - Cello Suite No.1", "1prweT95Mo0"),
            ("Chopin - Nocturne Op.9 No.2", "9E6b3swbnWg"),
            ("Debussy - Clair de Lune", "CvFH_6DNRCY"),
            ("Tchaikovsky - Kugu Golu", "9cNQFB0TDfY"),
            ("Dvorak - Yeni Dunya Senfonisi", "ETNoPqYAIPI"),
            ("Grieg - Peer Gynt (Sabah)", "zxflZTTAoIg"),
            ("Strauss - Mavi Tuna", "IDaJ7rFg66A"),
            ("Handel - Messiah (Hallelujah)", "IUZEtVbJT5c"),
            ("Schubert - Ave Maria", "2bosouX_d8Y"),
            ("Satie - Gymnopedie No.1", "S-Xm7s9eGxU"),
        ]

        for ad, vid in klasik_sarkilar:
            with st.expander(ad):
                st.components.v1.html(
                    f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/{vid}" '
                    f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
                    height=220)


# ===============================================================
# FEATURE 1: SANAL MUZE (Virtual 3D Gallery)
# ===============================================================

def _render_sanal_muze():
    """CSS 3D perspektif galeri — 3 oda, 10+ tablo."""
    import streamlit.components.v1 as components
    styled_section("🏛️ Sanal Galeri Turu — 3D Muze", "#6366f1")

    gallery_html = r"""
<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;font-family:'Segoe UI',sans-serif;overflow:hidden}
#app{width:100%;height:530px;position:relative}
#room{width:100%;height:400px;perspective:900px;position:relative;overflow:hidden;
  background:linear-gradient(180deg,#1a1a2e 0%,#16213e 100%)}
.wall-center{position:absolute;width:60%;height:65%;top:8%;left:20%;
  background:linear-gradient(180deg,#2a1a3e,#1e1030);transform:translateZ(0);
  border:3px solid #3d2a5e;box-shadow:inset 0 0 60px rgba(0,0,0,0.4)}
.wall-left{position:absolute;width:22%;height:65%;top:8%;left:0;
  background:linear-gradient(90deg,#150d25,#2a1a3e);
  transform:perspective(600px) rotateY(30deg);transform-origin:left center;
  border:2px solid #3d2a5e}
.wall-right{position:absolute;width:22%;height:65%;top:8%;right:0;
  background:linear-gradient(-90deg,#150d25,#2a1a3e);
  transform:perspective(600px) rotateY(-30deg);transform-origin:right center;
  border:2px solid #3d2a5e}
.floor{position:absolute;bottom:0;width:100%;height:27%;
  background:repeating-linear-gradient(90deg,#3e2723 0px,#3e2723 48px,#4e342e 48px,#4e342e 50px),
  linear-gradient(180deg,#5d4037,#3e2723);border-top:2px solid #2e1b0e}
.ceiling{position:absolute;top:0;width:100%;height:8%;
  background:linear-gradient(180deg,#0f0a1a,#1a1a2e);border-bottom:1px solid #2d1b69}
.painting{position:absolute;cursor:pointer;border:6px solid #8b6914;
  box-shadow:0 4px 20px rgba(0,0,0,0.6),inset 0 0 10px rgba(0,0,0,0.3);
  transition:all 0.3s ease;border-radius:2px}
.painting:hover{transform:scale(1.08);box-shadow:0 8px 40px rgba(139,92,246,0.4);z-index:10}
.painting .label{position:absolute;bottom:-22px;left:50%;transform:translateX(-50%);
  font-size:9px;color:#c4b5fd;white-space:nowrap;text-shadow:0 1px 4px #000}
.light{position:absolute;width:40px;height:6px;background:radial-gradient(ellipse,rgba(255,215,0,0.5),transparent);
  border-radius:50%;filter:blur(2px)}
#info{position:absolute;bottom:0;left:0;width:100%;background:linear-gradient(180deg,rgba(10,10,20,0.95),rgba(26,10,46,0.98));
  padding:14px 20px;display:none;border-top:2px solid #7c3aed;max-height:130px;overflow-y:auto}
#info h3{color:#e9d5ff;font-size:1rem;margin-bottom:4px}
#info .meta{color:#a78bfa;font-size:0.78rem;margin-bottom:4px}
#info .desc{color:#94a3b8;font-size:0.8rem;line-height:1.4}
#info .close{position:absolute;top:8px;right:14px;color:#ef4444;cursor:pointer;font-size:1.2rem}
#nav{display:flex;justify-content:center;gap:12px;padding:10px;background:#0a0a14}
#nav button{padding:8px 20px;border:2px solid #7c3aed;background:linear-gradient(180deg,#2d1b69,#1a0a2e);
  color:#e9d5ff;border-radius:8px;cursor:pointer;font-weight:700;font-size:0.8rem;transition:all 0.2s}
#nav button:hover{background:linear-gradient(180deg,#7c3aed,#4c1d95);color:#fff}
#nav button:disabled{opacity:0.3;cursor:default}
#roomTitle{color:#c4b5fd;font-size:0.85rem;padding:4px 16px;font-weight:600;text-align:center}
</style></head><body>
<div id="app">
  <div id="roomTitle"></div>
  <div id="room">
    <div class="ceiling"></div>
    <div class="wall-left" id="wl"></div>
    <div class="wall-center" id="wc"></div>
    <div class="wall-right" id="wr"></div>
    <div class="floor"></div>
    <div id="info"><span class="close" onclick="document.getElementById('info').style.display='none'">&times;</span>
      <h3 id="iTitle"></h3><div class="meta" id="iMeta"></div><div class="desc" id="iDesc"></div>
    </div>
  </div>
  <div id="nav">
    <button id="prev" onclick="go(-1)">&#9664; Onceki Oda</button>
    <button id="next" onclick="go(1)">Sonraki Oda &#9654;</button>
  </div>
</div>
<script>
var rooms=[
  {name:"Ronesans Odasi",paintings:[
    {t:"Mona Lisa",a:"Leonardo da Vinci",y:"1503-1519",m:"Ronesans",g:"linear-gradient(135deg,#5d4037,#8d6e63,#a1887f,#6d4c41)",
     d:"Dunyanin en unlu portresi. Gizemli golumsemesi yuzyillardir tartisiliyor. Louvre Muzesi'nde sergilenmektedir.",w:90,h:120,wall:"c",pos:0},
    {t:"Son Aksam Yemegi",a:"Leonardo da Vinci",y:"1495-1498",m:"Ronesans",g:"linear-gradient(135deg,#3e2723,#6d4c41,#8d6e63,#4e342e)",
     d:"Hz. Isa'nin havarileriyle son yemegini tasvir eder. Milano'daki Santa Maria delle Grazie manastirinda bulunur.",w:160,h:80,wall:"c",pos:1},
    {t:"Sistine Tavani",a:"Michelangelo",y:"1508-1512",m:"Ronesans",g:"linear-gradient(135deg,#1a237e,#283593,#e8eaf6,#c5cae9)",
     d:"Vatikan'daki Sistine Sapeli'nin tavan freskleri. Ademin Yaratilisi en unlu sahnesidir.",w:130,h:70,wall:"l",pos:0},
    {t:"Venusun Dogusu",a:"Sandro Botticelli",y:"1485",m:"Ronesans",g:"linear-gradient(135deg,#80deea,#b2dfdb,#ffe0b2,#ffccbc)",
     d:"Mitolojik tanrica Venus'un deniz koepuegunden dogusunu betimler. Floransa Uffizi Galerisi'ndedir.",w:140,h:85,wall:"r",pos:0}
  ]},
  {name:"Empresyonizm Odasi",paintings:[
    {t:"Niluferler",a:"Claude Monet",y:"1906",m:"Empresyonizm",g:"linear-gradient(135deg,#1b5e20,#388e3c,#81c784,#4db6ac)",
     d:"Monet'nin Giverny bahcesindeki havuzu tasvir eden serisi. 250'den fazla nilufer tablosu yapti.",w:120,h:100,wall:"c",pos:0},
    {t:"Yildizli Gece",a:"Vincent van Gogh",y:"1889",m:"Post-Empresyonizm",g:"linear-gradient(135deg,#0d47a1,#1565c0,#fdd835,#1976d2)",
     d:"Van Gogh'un akil hastanesinden gordugu gece manzarasi. Girdapli gokyuzu ile meshurdur.",w:110,h:85,wall:"c",pos:1},
    {t:"Balerinler",a:"Edgar Degas",y:"1876",m:"Empresyonizm",g:"linear-gradient(135deg,#f8bbd0,#f48fb1,#fce4ec,#e1bee7)",
     d:"Degas'nin bale danscilarini konu alan eserlerinden biri. Hareket ve isik ustaca yakalanmistir.",w:90,h:110,wall:"l",pos:0},
    {t:"Izlenim: Gundogumu",a:"Claude Monet",y:"1872",m:"Empresyonizm",g:"linear-gradient(135deg,#e65100,#ff6d00,#90a4ae,#546e7a)",
     d:"Empresyonizm akimina adini veren eser. Le Havre limaninda bir gundogumunu tasvir eder.",w:110,h:80,wall:"r",pos:0}
  ]},
  {name:"Modern Sanat Odasi",paintings:[
    {t:"Guernica",a:"Pablo Picasso",y:"1937",m:"Kubizm",g:"linear-gradient(135deg,#212121,#424242,#e0e0e0,#616161)",
     d:"Ispanya Ic Savasi'nda Guernica kasabasinin bombalanmasini protesto eden anti-savas tablosu.",w:160,h:80,wall:"c",pos:0},
    {t:"Bellegin Azmi",a:"Salvador Dali",y:"1931",m:"Surrealizm",g:"linear-gradient(135deg,#ffcc80,#ffe082,#a1887f,#90caf9)",
     d:"Eriyen saatler ikonografiyle tanilanan surrealist basyapit. Zaman algisini sorgular.",w:100,h:75,wall:"c",pos:1},
    {t:"Ciglik",a:"Edvard Munch",y:"1893",m:"Ekspresyonizm",g:"linear-gradient(135deg,#e65100,#ff6d00,#ff8f00,#1565c0)",
     d:"Modern cagi kaygi duygusunun sembolue. Munch'un yasadigi bir panik atagi anini yansitir.",w:75,h:105,wall:"l",pos:0},
    {t:"Kompozisyon VIII",a:"Wassily Kandinsky",y:"1923",m:"Soyut Sanat",g:"linear-gradient(135deg,#fdd835,#e53935,#1e88e5,#f5f5f5)",
     d:"Geometrik soyutlamanin oncue eseri. Daire, ucgen ve cizgilerle muziksel uyum arar.",w:110,h:100,wall:"r",pos:0}
  ]}
];
var cur=0;
function render(){
  var r=rooms[cur];
  document.getElementById('roomTitle').textContent='🏛️ '+r.name+' ('+(cur+1)+'/'+rooms.length+')';
  document.getElementById('prev').disabled=cur===0;
  document.getElementById('next').disabled=cur===rooms.length-1;
  document.getElementById('info').style.display='none';
  ['wl','wc','wr'].forEach(function(id){
    var el=document.getElementById(id);
    while(el.querySelector('.painting'))el.querySelector('.painting').remove();
    while(el.querySelector('.light'))el.querySelector('.light').remove();
  });
  var cIdx=0,lIdx=0,rIdx=0;
  r.paintings.forEach(function(p){
    var div=document.createElement('div');div.className='painting';
    div.style.width=p.w+'px';div.style.height=p.h+'px';
    div.style.background=p.g;
    var lbl=document.createElement('div');lbl.className='label';lbl.textContent=p.t;
    div.appendChild(lbl);
    var light=document.createElement('div');light.className='light';
    if(p.wall==='c'){
      var cx=cIdx===0?'18%':'58%';
      div.style.top='15%';div.style.left=cx;
      light.style.top=(parseInt(div.style.top)-3)+'%';light.style.left=cx;
      document.getElementById('wc').appendChild(div);
      document.getElementById('wc').appendChild(light);cIdx++;
    }else if(p.wall==='l'){
      div.style.top='15%';div.style.left='15%';
      document.getElementById('wl').appendChild(div);lIdx++;
    }else{
      div.style.top='15%';div.style.left='15%';
      document.getElementById('wr').appendChild(div);rIdx++;
    }
    div.onclick=function(){
      document.getElementById('iTitle').textContent=p.t;
      document.getElementById('iMeta').textContent=p.a+' | '+p.y+' | '+p.m;
      document.getElementById('iDesc').textContent=p.d;
      document.getElementById('info').style.display='block';
    };
  });
}
function go(d){cur=Math.max(0,Math.min(rooms.length-1,cur+d));render();}
render();
</script></body></html>
"""
    components.html(gallery_html, height=550)


# ===============================================================
# FEATURE 2: AI CIZIM DEGERLENDIRME
# ===============================================================

def _render_cizim_degerlendirme():
    """AI tabanli (simulasyon) cizim degerlendirme sistemi."""
    styled_section("🤖 AI Cizim Degerlendirme", "#8b5cf6")

    _render_html("""
    <div class="snt-card" style="text-align:center;padding:28px">
        <div style="font-size:2.5rem;margin-bottom:8px">🎨🤖</div>
        <h3 style="color:#e9d5ff !important;margin:0 0 6px !important;font-size:1.2rem">Yapay Zeka Cizim Analizi</h3>
        <p style="color:#94a3b8 !important;font-size:0.82rem;margin:0 !important">
            Cizimini tamamla ve 'Degerlendir' butonuna bas. AI sanal asistan eserini 5 kriterde analiz edecek.
        </p>
    </div>
    """)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        styled_section("✏️ Cizim Bilgileri", "#ec4899")
        eser_adi = st.text_input("Eser Adi", key="snt_dg_eser_adi", placeholder="Orn: Gunbatimi Manzarasi")
        teknik_sec = st.selectbox("Teknik", ["Karakalem", "Suluboya", "Yagliboya", "Pastel", "Dijital", "Kece Kalem"], key="snt_dg_teknik")
        konu_sec = st.selectbox("Konu", ["Manzara", "Portre", "Natumort", "Soyut", "Hayvan", "Fantezi"], key="snt_dg_konu")

    with col2:
        styled_section("📝 Notlar", "#3b82f6")
        aciklama = st.text_area("Eser hakkinda kisa aciklama", key="snt_dg_aciklama", height=120,
                                placeholder="Ciziminde ne anlatmak istedin?")

    if st.button("🤖 Degerlendir", key="snt_dg_btn", type="primary", use_container_width=True):
        if not eser_adi:
            st.warning("Lutfen eser adini girin.")
        else:
            random.seed(hash(eser_adi + teknik_sec + konu_sec + aciklama) % 2**31)

            kompozisyon = random.randint(5, 10)
            renk_kull = random.randint(4, 10)
            teknik_puan = random.randint(5, 10)
            yaraticilik = random.randint(5, 10)
            detay = random.randint(4, 10)

            scores = [kompozisyon, renk_kull, teknik_puan, yaraticilik, detay]
            avg = sum(scores) / len(scores)
            stars = min(5, max(1, round(avg / 2)))

            star_str = "★" * stars + "☆" * (5 - stars)

            olumlu = [
                "Kompozisyon dengesi cok basarili!",
                "Renk paleti uyumlu secilmis.",
                "Teknik acidan olgun bir calisma.",
                "Yaratici bakis acisi takdire deger.",
                "Detay isleme cok iyi seviyede.",
                "Isik-golge kullanimi etkileyici.",
                "Perspektif kullanimi basarili.",
                "Orijinal bir yaklasim sergilenmis.",
            ]
            random.shuffle(olumlu)
            fb_text = " ".join(olumlu[:3])

            labels = ["Kompozisyon", "Renk Kullanimi", "Teknik", "Yaraticilik", "Detay"]
            tavsiyeler_pool = {
                "Kompozisyon": ["Altin oran kuralini daha fazla uygula.", "Odak noktasini netlestir.", "Bosluk dengesine dikkat et."],
                "Renk Kullanimi": ["Complementer renk ciftlerini dene.", "Renk gecislerini yumusatmaya calis.", "Sicak-soguk kontrast ekle."],
                "Teknik": ["Firca darbelerinde tutarlilik sagla.", "Farkli kalinliklarda cizgiler dene.", "Katmanlama teknigini gelistir."],
                "Yaraticilik": ["Farkli perspektiflerden bak.", "Beklenmedik renkler dene.", "Dokuyu yaratici kullan."],
                "Detay": ["Kucuk detaylara daha fazla zaman ayir.", "On plan detaylarini zenginlestir.", "Doku varyasyonlari ekle."],
            }

            en_dusuk_idxs = sorted(range(5), key=lambda i: scores[i])[:3]
            tavsiyeler = []
            for idx in en_dusuk_idxs:
                t_list = tavsiyeler_pool[labels[idx]]
                tavsiyeler.append(random.choice(t_list))

            bars_html = ""
            colors = ["#ec4899", "#f59e0b", "#10b981", "#8b5cf6", "#3b82f6"]
            for i, (lbl, sc) in enumerate(zip(labels, scores)):
                pct = sc * 10
                bars_html += f"""
                <div style="margin-bottom:8px">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                        <span style="color:#c4b5fd;font-size:0.78rem;font-weight:600">{lbl}</span>
                        <span style="color:#e9d5ff;font-size:0.78rem;font-weight:700">{sc}/10</span>
                    </div>
                    <div style="background:#1e1030;border-radius:6px;height:10px;overflow:hidden">
                        <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{colors[i]},
                            {colors[i]}aa);border-radius:6px;transition:width 0.5s"></div>
                    </div>
                </div>"""

            tav_html = ""
            for j, tav in enumerate(tavsiyeler):
                tav_html += f'<div style="color:#94a3b8;font-size:0.8rem;margin-bottom:4px">💡 {tav}</div>'

            _render_html(f"""
            <div style="background:linear-gradient(145deg,#1a0a2e,#2d1b69);border-radius:20px;padding:24px;
                         border:2px solid rgba(139,92,246,0.3);margin-top:16px">
                <div style="text-align:center;margin-bottom:16px">
                    <div style="font-size:2.5rem;color:#fbbf24;letter-spacing:4px">{star_str}</div>
                    <div style="font-size:2rem;font-weight:800;color:#e9d5ff;margin-top:4px">{avg:.1f}/10</div>
                    <div style="font-size:0.78rem;color:#a78bfa;margin-top:2px">Genel Degerlendirme Puani</div>
                </div>
                <div style="background:#0f172a;border-radius:14px;padding:16px;margin-bottom:14px">
                    <div style="font-weight:700;color:#c4b5fd;font-size:0.85rem;margin-bottom:10px">📊 Detayli Analiz</div>
                    {bars_html}
                </div>
                <div style="background:#0f172a;border-radius:14px;padding:16px;margin-bottom:14px">
                    <div style="font-weight:700;color:#c4b5fd;font-size:0.85rem;margin-bottom:6px">💬 AI Yorumu</div>
                    <div style="color:#94a3b8;font-size:0.82rem;line-height:1.5">{fb_text}</div>
                </div>
                <div style="background:#0f172a;border-radius:14px;padding:16px">
                    <div style="font-weight:700;color:#c4b5fd;font-size:0.85rem;margin-bottom:8px">📋 Tavsiyelerin</div>
                    {tav_html}
                </div>
            </div>
            """)


# ===============================================================
# FEATURE 3: SANAT YARISMASI PLATFORMU
# ===============================================================

def _render_sanat_yarismasi():
    """Ogrencilerin eser yukleyip begeni toplayabildigi yarisma platformu."""
    styled_section("🏆 Sanat Yarismasi Platformu", "#f59e0b")

    _render_html("""
    <div class="snt-card" style="text-align:center;padding:28px;border:2px solid rgba(245,158,11,0.3)">
        <div style="font-size:2.5rem;margin-bottom:8px">🏆🎨</div>
        <h3 style="color:#fde68a !important;margin:0 0 6px !important;font-size:1.2rem">Sanat Yarismasi</h3>
        <p style="color:#94a3b8 !important;font-size:0.82rem;margin:0 !important">
            Eserlerini yukle, arkadaslarinin eserlerini incele ve en begenilenler arasindan Haftanin Eseri secilsin!
        </p>
    </div>
    """)

    # Initialize session state
    if "snt_yarisma_eserler" not in st.session_state:
        st.session_state["snt_yarisma_eserler"] = [
            {"ad": "Gunbatiminda Deniz", "sanatci": "Elif Y.", "dal": "Resim", "teknik": "Suluboya",
             "aciklama": "Ege kiyilarinda bir gunbatimi manzarasi.", "tarih": "2026-03-20",
             "begeni": 14, "renk": "linear-gradient(135deg,#e65100,#ff6d00,#0277bd,#01579b)"},
            {"ad": "Soyut Duygu", "sanatci": "Ahmet K.", "dal": "Dijital", "teknik": "Tablet Cizim",
             "aciklama": "Farkli duygu durumlarini renk ve sekillerle ifade ettim.", "tarih": "2026-03-18",
             "begeni": 9, "renk": "linear-gradient(135deg,#8e24aa,#e91e63,#fdd835,#00bcd4)"},
            {"ad": "Kus Portresi", "sanatci": "Zeynep T.", "dal": "Fotograf", "teknik": "Makro",
             "aciklama": "Bahcedeki ispinozun yakin cekim fotograffi.", "tarih": "2026-03-22",
             "begeni": 21, "renk": "linear-gradient(135deg,#2e7d32,#81c784,#a1887f,#4db6ac)"},
            {"ad": "Ebru Cicicegi", "sanatci": "Murat S.", "dal": "Ebru", "teknik": "Battal Ebru",
             "aciklama": "Geleneksel Turk ebru sanatinda cicek motifi.", "tarih": "2026-03-15",
             "begeni": 17, "renk": "linear-gradient(135deg,#c62828,#ef5350,#1565c0,#42a5f5)"},
            {"ad": "Hat Levhasi", "sanatci": "Ayse D.", "dal": "Kaligrafi", "teknik": "Nesih",
             "aciklama": "Bismillah hat calismasi, siyah murekkep.", "tarih": "2026-03-21",
             "begeni": 12, "renk": "linear-gradient(135deg,#1a1a2e,#37474f,#d4af37,#1a1a2e)"},
        ]

    eserler = st.session_state["snt_yarisma_eserler"]

    DALLAR = ["Resim", "Heykel", "Fotograf", "Dijital", "Ebru", "Kaligrafi"]
    TEKNIK_MAP = {
        "Resim": ["Suluboya", "Yagliboya", "Karakalem", "Pastel", "Akrilik", "Guaj"],
        "Heykel": ["Kil", "Alci", "Tas", "Ahsap", "Metal", "Kagit Mase"],
        "Fotograf": ["Manzara", "Portre", "Makro", "Sokak", "Siyah-Beyaz", "Gece"],
        "Dijital": ["Tablet Cizim", "Vektorel", "Piksel Sanat", "3D Modelleme", "Fotomanipulasyon"],
        "Ebru": ["Battal Ebru", "Gelgit Ebru", "Cicekli Ebru", "Hatip Ebru", "Bülbül Yuvasi"],
        "Kaligrafi": ["Nesih", "Sulus", "Talik", "Rika", "Diwani", "Kufi"],
    }

    yrs_tabs = st.tabs(["📤 Eser Yukle", "🖼️ Galeri", "⭐ Haftanin Eseri"])

    with yrs_tabs[0]:
        styled_section("📤 Yeni Eser Gonder", "#10b981")
        c1, c2 = st.columns(2)
        with c1:
            y_ad = st.text_input("Eser Adi", key="snt_yr_ad", placeholder="Eserine bir isim ver")
            y_dal = st.selectbox("Sanat Dali", DALLAR, key="snt_yr_dal")
        with c2:
            y_sanatci = st.text_input("Sanatci Adi", key="snt_yr_sanatci", placeholder="Adiniz Soyadiniz")
            teknikler = TEKNIK_MAP.get(y_dal, ["Diger"])
            y_teknik = st.selectbox("Teknik", teknikler, key="snt_yr_teknik")
        y_aciklama = st.text_area("Aciklama", key="snt_yr_aciklama", height=80,
                                  placeholder="Eserini kisaca anlat...")

        if st.button("🚀 Eseri Gonder", key="snt_yr_gonder", type="primary", use_container_width=True):
            if not y_ad or not y_sanatci:
                st.warning("Lutfen eser adi ve sanatci adini doldurun.")
            else:
                rng = random.Random(hash(y_ad + y_sanatci) % 2**31)
                renk_pairs = [
                    ("#e65100", "#ff6d00", "#0277bd", "#01579b"),
                    ("#8e24aa", "#e91e63", "#fdd835", "#00bcd4"),
                    ("#2e7d32", "#81c784", "#a1887f", "#4db6ac"),
                    ("#c62828", "#ef5350", "#1565c0", "#42a5f5"),
                    ("#1a237e", "#5c6bc0", "#fdd835", "#e91e63"),
                    ("#004d40", "#26a69a", "#ff8f00", "#d84315"),
                ]
                rp = rng.choice(renk_pairs)
                yeni = {
                    "ad": y_ad, "sanatci": y_sanatci, "dal": y_dal, "teknik": y_teknik,
                    "aciklama": y_aciklama, "tarih": datetime.now().strftime("%Y-%m-%d"),
                    "begeni": 0,
                    "renk": f"linear-gradient(135deg,{rp[0]},{rp[1]},{rp[2]},{rp[3]})",
                }
                eserler.insert(0, yeni)
                st.success(f"'{y_ad}' basariyla gonderildi!")
                st.rerun()

    with yrs_tabs[1]:
        styled_section("🖼️ Eser Galerisi", "#6366f1")
        siralama = st.selectbox("Siralama", ["En Yeni", "En Begenilen"], key="snt_yr_sira")
        if siralama == "En Begenilen":
            gosterim = sorted(eserler, key=lambda x: x["begeni"], reverse=True)
        else:
            gosterim = list(eserler)

        if not gosterim:
            st.info("Henuz eser yuklenmemis.")
        else:
            cols = st.columns(2)
            for idx, eser in enumerate(gosterim):
                with cols[idx % 2]:
                    _render_html(f"""
                    <div style="background:linear-gradient(145deg,#1a0a2e,#2d1b69);border-radius:16px;
                                padding:16px;margin-bottom:14px;border:1px solid rgba(99,102,241,0.2)">
                        <div style="width:100%;height:120px;border-radius:10px;margin-bottom:10px;
                                    background:{eser['renk']};display:flex;align-items:center;justify-content:center;
                                    border:2px solid rgba(255,255,255,0.1)">
                            <span style="font-size:2.5rem;opacity:0.3">🎨</span>
                        </div>
                        <div style="font-weight:700;color:#e9d5ff !important;font-size:0.95rem">{eser['ad']}</div>
                        <div style="color:#a78bfa !important;font-size:0.75rem;margin-top:2px">
                            ✍️ {eser['sanatci']} | 🎭 {eser['dal']} — {eser['teknik']}
                        </div>
                        <div style="color:#64748b !important;font-size:0.7rem;margin-top:2px">📅 {eser['tarih']}</div>
                        <div style="color:#94a3b8 !important;font-size:0.78rem;margin-top:6px;line-height:1.4;
                                    font-style:italic">{eser.get('aciklama','')[:120]}</div>
                        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px;
                                    padding-top:8px;border-top:1px solid rgba(99,102,241,0.15)">
                            <span style="color:#f59e0b !important;font-weight:700;font-size:0.85rem">❤️ {eser['begeni']}</span>
                        </div>
                    </div>
                    """)
                    if st.button(f"❤️ Begendim", key=f"snt_yr_like_{idx}_{eser['ad'][:10]}"):
                        # Find the actual eser in list and increment
                        for e in eserler:
                            if e["ad"] == eser["ad"] and e["sanatci"] == eser["sanatci"]:
                                e["begeni"] += 1
                                break
                        st.rerun()

    with yrs_tabs[2]:
        styled_section("⭐ Haftanin Eseri", "#f59e0b")
        if eserler:
            en_populer = max(eserler, key=lambda x: x["begeni"])
            _render_html(f"""
            <div style="background:linear-gradient(145deg,#1a0a2e,#2d1b69);border-radius:20px;padding:24px;
                         border:3px solid #d4af37;box-shadow:0 0 40px rgba(212,175,55,0.15);text-align:center">
                <div style="font-size:1.5rem;color:#fbbf24;margin-bottom:6px">🏆 Haftanin Eseri 🏆</div>
                <div style="width:80%;max-width:320px;height:160px;border-radius:12px;margin:12px auto;
                            background:{en_populer['renk']};display:flex;align-items:center;justify-content:center;
                            border:4px solid #d4af37;box-shadow:0 8px 30px rgba(212,175,55,0.2)">
                    <span style="font-size:3rem;opacity:0.3">🖼️</span>
                </div>
                <div style="font-weight:800;color:#fde68a !important;font-size:1.3rem;margin-top:8px">{en_populer['ad']}</div>
                <div style="color:#a78bfa !important;font-size:0.85rem;margin-top:4px">✍️ {en_populer['sanatci']}</div>
                <div style="color:#94a3b8 !important;font-size:0.8rem;margin-top:2px">
                    🎭 {en_populer['dal']} — {en_populer['teknik']} | 📅 {en_populer['tarih']}
                </div>
                <div style="color:#c4b5fd !important;font-size:0.85rem;margin-top:10px;font-style:italic;
                            line-height:1.5">{en_populer.get('aciklama','')}</div>
                <div style="margin-top:12px;font-size:1.5rem;color:#f59e0b">❤️ {en_populer['begeni']} Begeni</div>
            </div>
            """)
        else:
            st.info("Henuz eser bulunmuyor.")
