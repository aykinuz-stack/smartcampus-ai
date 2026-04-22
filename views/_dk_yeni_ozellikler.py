"""Dijital Kutuphane - 10 Yeni Ozellik (Part 1: 1-5)"""
import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime, timedelta
import random


# ============================================================
# 1. SESLI KITAP STUDYOSU
# ============================================================
def render_sesli_kitap_studyosu():
    """Sesli Kitap Studyosu - Web Speech API TTS"""
    st.markdown("""
    <style>
    .sks-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a2744 50%, #0d1b36 100%);
        border: 1px solid #c9a84c;
        border-radius: 16px;
        padding: 24px 32px;
        text-align: center;
        margin-bottom: 20px;
    }
    .sks-header h2 {
        color: #c9a84c;
        font-size: 28px;
        margin: 0;
        text-shadow: 0 0 20px rgba(201,168,76,0.3);
    }
    .sks-header p { color: #8899bb; margin: 4px 0 0 0; }
    .sks-card {
        background: linear-gradient(135deg, #0f1d34, #162240);
        border: 1px solid rgba(201,168,76,0.25);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .sks-card h4 { color: #c9a84c; margin: 0 0 12px 0; }
    </style>
    <div class="sks-header">
        <h2>🎙️ Sesli Kitap Studyosu</h2>
        <p>Metninizi profesyonel sesle dinleyin</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        metin = st.text_area(
            "Seslendirilecek Metin",
            height=200,
            placeholder="Metninizi buraya yazin veya yapiştirin...",
            key="sks_metin"
        )
    with col2:
        dil = st.selectbox("Dil", [
            "Turkce", "English", "Deutsch",
            "Francais", "Italiano", "Espanol"
        ], key="sks_dil")
        dil_kodlari = {
            "Turkce": "tr-TR", "English": "en-US", "Deutsch": "de-DE",
            "Francais": "fr-FR", "Italiano": "it-IT", "Espanol": "es-ES"
        }
        hiz = st.slider("Hiz", 0.5, 2.0, 1.0, 0.1, key="sks_hiz")
        st.markdown(f"""
        <div class="sks-card">
            <h4>Ayarlar</h4>
            <p style="color:#aab;">Dil: <b style="color:#c9a84c">{dil}</b></p>
            <p style="color:#aab;">Hiz: <b style="color:#c9a84c">{hiz}x</b></p>
            <p style="color:#aab;">Karakter: <b style="color:#c9a84c">{len(metin) if metin else 0}</b></p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🎙️ Seslendir", key="sks_btn", type="primary"):
        if not metin or not metin.strip():
            st.warning("Lutfen seslendirilecek bir metin girin.")
            return
        safe_text = json.dumps(metin, ensure_ascii=False)
        lang_code = dil_kodlari.get(dil, "tr-TR")

        html_code = f"""
        <div id="tts-player" style="
            background: linear-gradient(135deg, #0a1628, #1a2744);
            border: 1px solid #c9a84c;
            border-radius: 16px;
            padding: 28px;
            font-family: 'Segoe UI', sans-serif;
            color: #ddd;
            text-align: center;
        ">
            <h3 style="color:#c9a84c; margin:0 0 16px 0;">🎧 TTS Oynatici</h3>
            <div id="progress-wrap" style="
                background: #0d1b36;
                border-radius: 8px;
                height: 10px;
                margin: 16px 0;
                border: 1px solid rgba(201,168,76,0.3);
                overflow: hidden;
            ">
                <div id="progress-bar" style="
                    height: 100%;
                    width: 0%;
                    background: linear-gradient(90deg, #c9a84c, #f0d27a);
                    border-radius: 8px;
                    transition: width 0.3s;
                "></div>
            </div>
            <p id="status-text" style="color:#8899bb; margin:8px 0;">Hazir</p>
            <div style="display:flex; justify-content:center; gap:12px; margin:16px 0;">
                <button onclick="doPlay()" style="
                    background: linear-gradient(135deg, #c9a84c, #a3852e);
                    border:none; color:#0a1628; padding:10px 24px;
                    border-radius:8px; cursor:pointer; font-weight:bold; font-size:15px;
                ">▶ Oynat</button>
                <button onclick="doPause()" style="
                    background: #1a2744; border:1px solid #c9a84c;
                    color:#c9a84c; padding:10px 24px;
                    border-radius:8px; cursor:pointer; font-weight:bold; font-size:15px;
                ">⏸ Duraklat</button>
                <button onclick="doStop()" style="
                    background: #1a2744; border:1px solid #c9a84c;
                    color:#c9a84c; padding:10px 24px;
                    border-radius:8px; cursor:pointer; font-weight:bold; font-size:15px;
                ">⏹ Durdur</button>
            </div>
            <div style="margin-top:12px; display:flex; gap:16px; align-items:center; flex-wrap:wrap;">
                <div>
                    <label style="color:#8899bb;">Ses: </label>
                    <select id="voice-select" onchange="" style="
                        background:#1a2744; border:1px solid rgba(201,168,76,0.4);
                        color:#c9a84c; padding:6px 10px; border-radius:8px;
                        font-size:13px; min-width:200px;">
                        <option>Yukleniyor...</option>
                    </select>
                </div>
                <div>
                    <label style="color:#8899bb;">Hiz: </label>
                    <input type="range" id="speed-ctrl" min="0.5" max="2.0" step="0.1"
                           value="{hiz}" onchange="changeSpeed(this.value)"
                           style="width:120px; accent-color:#c9a84c;">
                    <span id="speed-val" style="color:#c9a84c; font-weight:bold;">{hiz}x</span>
                </div>
            </div>
        </div>
        <script>
            var utterance = null;
            var synth = window.speechSynthesis;
            var textContent = {safe_text};
            var langCode = "{lang_code}";
            var currentRate = {hiz};
            var progressInterval = null;
            var bestVoice = null;
            var allVoices = [];

            // En iyi sesi bul — Microsoft/Google neural sesleri tercih et
            function findBestVoice() {{
                allVoices = synth.getVoices();
                var langVoices = allVoices.filter(function(v) {{
                    return v.lang && v.lang.toLowerCase().startsWith(langCode.toLowerCase().substring(0,2));
                }});
                if (langVoices.length === 0) return null;

                // Oncelik sirasi: Microsoft Online (Neural) > Google > Microsoft > diger
                var premium = ['Microsoft.*Online', 'Google.*Natural', 'Google.*Wavenet', 'Neural', 'Premium', 'Enhanced'];
                for (var p = 0; p < premium.length; p++) {{
                    var re = new RegExp(premium[p], 'i');
                    for (var i = 0; i < langVoices.length; i++) {{
                        if (re.test(langVoices[i].name)) return langVoices[i];
                    }}
                }}
                // Google sesleri genelde daha iyi
                for (var i = 0; i < langVoices.length; i++) {{
                    if (/google/i.test(langVoices[i].name)) return langVoices[i];
                }}
                // Microsoft sesleri
                for (var i = 0; i < langVoices.length; i++) {{
                    if (/microsoft/i.test(langVoices[i].name)) return langVoices[i];
                }}
                // Herhangi biri
                return langVoices[0];
            }}

            // Ses listesini doldur
            function populateVoiceSelect() {{
                allVoices = synth.getVoices();
                var sel = document.getElementById('voice-select');
                if (!sel) return;
                var langVoices = allVoices.filter(function(v) {{
                    return v.lang && v.lang.toLowerCase().startsWith(langCode.toLowerCase().substring(0,2));
                }});
                sel.innerHTML = '';
                langVoices.forEach(function(v, i) {{
                    var opt = document.createElement('option');
                    var label = v.name.replace('Microsoft ', '').replace('Google ', '');
                    if (/online|neural|natural|premium/i.test(v.name)) label += ' ★';
                    opt.value = i;
                    opt.text = label;
                    sel.appendChild(opt);
                }});
                // En iyisini sec
                bestVoice = findBestVoice();
                if (bestVoice) {{
                    var idx = langVoices.indexOf(bestVoice);
                    if (idx >= 0) sel.selectedIndex = idx;
                }}
            }}

            if (synth.onvoiceschanged !== undefined) {{
                synth.onvoiceschanged = populateVoiceSelect;
            }}
            setTimeout(populateVoiceSelect, 200);

            function getSelectedVoice() {{
                var sel = document.getElementById('voice-select');
                if (!sel) return bestVoice;
                var langVoices = allVoices.filter(function(v) {{
                    return v.lang && v.lang.toLowerCase().startsWith(langCode.toLowerCase().substring(0,2));
                }});
                return langVoices[parseInt(sel.value)] || bestVoice;
            }}

            function doPlay() {{
                synth.cancel();
                utterance = new SpeechSynthesisUtterance(textContent);
                utterance.lang = langCode;
                utterance.rate = currentRate;
                utterance.pitch = 1.0;
                var voice = getSelectedVoice();
                if (voice) utterance.voice = voice;
                utterance.onstart = function() {{
                    document.getElementById('status-text').innerText = 'Okunuyor... (' + (voice ? voice.name : 'varsayilan') + ')';
                    startProgress();
                }};
                utterance.onend = function() {{
                    document.getElementById('status-text').innerText = 'Tamamlandi';
                    document.getElementById('progress-bar').style.width = '100%';
                    clearInterval(progressInterval);
                }};
                utterance.onpause = function() {{
                    document.getElementById('status-text').innerText = 'Duraklatildi';
                }};
                utterance.onresume = function() {{
                    document.getElementById('status-text').innerText = 'Okunuyor...';
                }};
                synth.speak(utterance);
            }}
            function doPause() {{
                if (synth.speaking && !synth.paused) synth.pause();
                else if (synth.paused) synth.resume();
            }}
            function doStop() {{
                synth.cancel();
                document.getElementById('status-text').innerText = 'Durduruldu';
                document.getElementById('progress-bar').style.width = '0%';
                clearInterval(progressInterval);
            }}
            function changeSpeed(v) {{
                currentRate = parseFloat(v);
                document.getElementById('speed-val').innerText = v + 'x';
            }}
            function startProgress() {{
                var dur = (textContent.length / 15) / currentRate * 1000;
                var start = Date.now();
                clearInterval(progressInterval);
                progressInterval = setInterval(function() {{
                    var elapsed = Date.now() - start;
                    var pct = Math.min((elapsed / dur) * 100, 100);
                    document.getElementById('progress-bar').style.width = pct + '%';
                    if (pct >= 100) clearInterval(progressInterval);
                }}, 200);
            }}
        </script>
        """
        components.html(html_code, height=280)


# ============================================================
# 2. KITAP KULUBU
# ============================================================
def render_kitap_kulubu():
    """Kitap Kulubu - Okuma gruplari ve tartisma"""
    st.markdown("""
    <style>
    .kk-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a2744 50%, #0d1b36 100%);
        border: 1px solid #c9a84c; border-radius: 16px;
        padding: 24px 32px; text-align: center; margin-bottom: 20px;
    }
    .kk-header h2 { color: #c9a84c; font-size: 28px; margin: 0; }
    .kk-header p { color: #8899bb; margin: 4px 0 0 0; }
    .kk-badge {
        display: inline-block; padding: 8px 18px; border-radius: 20px;
        font-weight: bold; font-size: 14px; margin: 4px;
        border: 1px solid rgba(201,168,76,0.3);
    }
    .kk-leader-row {
        background: linear-gradient(135deg, #0f1d34, #162240);
        border: 1px solid rgba(201,168,76,0.15);
        border-radius: 10px; padding: 10px 16px;
        margin: 4px 0; display: flex; justify-content: space-between;
        align-items: center; color: #ccc;
    }
    .kk-leader-row .rank { color: #c9a84c; font-weight: bold; font-size: 18px; }
    .kk-leader-row .pages { color: #f0d27a; font-weight: bold; }
    </style>
    <div class="kk-header">
        <h2>📖 Kitap Kulubu</h2>
        <p>Birlikte okuyun, birlikte tartışın</p>
    </div>
    """, unsafe_allow_html=True)

    if "kk_streak" not in st.session_state:
        st.session_state.kk_streak = 0
    if "kk_badges" not in st.session_state:
        st.session_state.kk_badges = []

    kitaplar = [
        "Suc ve Ceza - Dostoyevski", "1984 - George Orwell",
        "Kucuk Prens - Saint-Exupery", "Kurk Mantolu Madonna - Sabahattin Ali",
        "Calikusu - Resat Nuri Guntekin", "Ince Memed - Yasar Kemal",
        "Sefiller - Victor Hugo", "Don Kisot - Cervantes",
        "Donusum - Franz Kafka", "Hayvan Ciftligi - George Orwell"
    ]

    col1, col2 = st.columns(2)
    with col1:
        kulup_adi = st.text_input("Kulup Adi", placeholder="Ornek: Edebiyat Severler", key="kk_kulup")
        secili_kitap = st.selectbox("Bu Ay Okunan Kitap", kitaplar, key="kk_kitap")
        haftalik_hedef = st.number_input("Haftalik Hedef (sayfa)", 10, 500, 100, 10, key="kk_hedef")

    with col2:
        okunan = st.slider("Bu Hafta Okunan (sayfa)", 0, int(haftalik_hedef), 0, key="kk_okunan")
        ilerleme = min(okunan / max(haftalik_hedef, 1), 1.0)
        st.progress(ilerleme, text=f"Ilerleme: %{int(ilerleme * 100)}")

        if ilerleme >= 1.0:
            st.session_state.kk_streak += 1
            st.success(f"Hedef tamamlandi! Seri: {st.session_state.kk_streak} hafta")

    tartisma = st.text_area(
        "Tartisma Notlari",
        placeholder="Bu haftaki okumalar hakkinda dusuncelerinizi yazin...",
        height=120, key="kk_tartisma"
    )

    # Badge system
    streak = st.session_state.kk_streak
    badges_html = ""
    badge_list = [
        (1, "🌱 Filiz", "#2d5a3d", "1 hafta"),
        (3, "📗 Okur", "#1a5276", "3 hafta"),
        (5, "⭐ Yildiz Okur", "#7d6608", "5 hafta"),
        (10, "🏆 Sampiyon", "#c9a84c", "10 hafta"),
        (20, "👑 Efsane", "#f0d27a", "20 hafta"),
    ]
    for threshold, label, color, desc in badge_list:
        opacity = "1.0" if streak >= threshold else "0.35"
        badges_html += f'<span class="kk-badge" style="background:{color}22; color:{color}; opacity:{opacity};">{label} ({desc})</span>'

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0f1d34, #162240);
        border: 1px solid rgba(201,168,76,0.25); border-radius: 12px;
        padding: 16px; margin: 12px 0; text-align: center;">
        <h4 style="color:#c9a84c; margin:0 0 10px 0;">🏅 Rozetler (Seri: {streak} hafta)</h4>
        {badges_html}
    </div>
    """, unsafe_allow_html=True)

    # Leaderboard
    liderler = [
        ("Elif Yilmaz", 320), ("Ahmet Kaya", 285), ("Zeynep Demir", 270),
        ("Mehmet Oz", 245), ("Ayse Celik", 220), ("Can Turk", 195),
        ("Fatma Aksoy", 180), ("Emre Dogan", 165),
    ]
    st.markdown('<h4 style="color:#c9a84c;">🏆 Haftalik Liderlik Tablosu</h4>', unsafe_allow_html=True)
    medals = ["🥇", "🥈", "🥉"]
    rows_html = ""
    for i, (name, pages) in enumerate(liderler):
        rank_display = medals[i] if i < 3 else f"#{i+1}"
        rows_html += f"""
        <div class="kk-leader-row">
            <span class="rank">{rank_display}</span>
            <span>{name}</span>
            <span class="pages">{pages} sayfa</span>
        </div>"""
    st.markdown(rows_html, unsafe_allow_html=True)


# ============================================================
# 3. YAZARLAR DUNYASI
# ============================================================
def render_yazarlar_dunyasi():
    """Yazarlar Dunyasi - Interaktif yazar kartlari ve quiz"""
    authors = [
        {"name": "William Shakespeare", "flag": "🇬🇧", "years": "1564-1616", "century": 16, "country": "Ingiltere", "works": "Hamlet, Romeo ve Juliet, Othello", "bio": "Ingiliz edebiyatinin en buyuk oyun yazari ve siiri.", "emoji": "🎭"},
        {"name": "Fyodor Dostoyevski", "flag": "🇷🇺", "years": "1821-1881", "century": 19, "country": "Rusya", "works": "Suc ve Ceza, Karamazov Kardesler", "bio": "Insan psikolojisinin derinliklerini arastiran Rus romanci.", "emoji": "📖"},
        {"name": "Lev Tolstoy", "flag": "🇷🇺", "years": "1828-1910", "century": 19, "country": "Rusya", "works": "Savas ve Baris, Anna Karenina", "bio": "Dunyanin en buyuk romancisi olarak kabul edilen Rus yazar.", "emoji": "📚"},
        {"name": "Victor Hugo", "flag": "🇫🇷", "years": "1802-1885", "century": 19, "country": "Fransa", "works": "Sefiller, Notre-Dame'in Kamburu", "bio": "Fransiz romantik edebiyatinin dev ismi.", "emoji": "🏛️"},
        {"name": "Charles Dickens", "flag": "🇬🇧", "years": "1812-1870", "century": 19, "country": "Ingiltere", "works": "Oliver Twist, Buyuk Umutlar", "bio": "Victoria donemi Ingilteresinin en populer romancisi.", "emoji": "🎩"},
        {"name": "Franz Kafka", "flag": "🇨🇿", "years": "1883-1924", "century": 20, "country": "Cekya", "works": "Donusum, Dava", "bio": "Absurd ve varoluşcu edebiyatin oncusu.", "emoji": "🪲"},
        {"name": "Ernest Hemingway", "flag": "🇺🇸", "years": "1899-1961", "century": 20, "country": "ABD", "works": "Yasli Adam ve Deniz, Silahlara Veda", "bio": "Nobel odullu Amerikan romanci ve gazeteci.", "emoji": "🎣"},
        {"name": "George Orwell", "flag": "🇬🇧", "years": "1903-1950", "century": 20, "country": "Ingiltere", "works": "1984, Hayvan Ciftligi", "bio": "Distopya turunun en etkili yazari.", "emoji": "👁️"},
        {"name": "Mark Twain", "flag": "🇺🇸", "years": "1835-1910", "century": 19, "country": "ABD", "works": "Tom Sawyer, Huckleberry Finn", "bio": "Amerikan edebiyatinin babasi olarak anilir.", "emoji": "🚢"},
        {"name": "Jane Austen", "flag": "🇬🇧", "years": "1775-1817", "century": 18, "country": "Ingiltere", "works": "Gurur ve Onyargi, Emma", "bio": "Ingiliz toplumunu zarif ironisiyle anlatan romanci.", "emoji": "💐"},
        {"name": "Charlotte Bronte", "flag": "🇬🇧", "years": "1816-1855", "century": 19, "country": "Ingiltere", "works": "Jane Eyre", "bio": "Victoria donemi Ingiliz edebiyatinin onemli kadin yazari.", "emoji": "🌹"},
        {"name": "Edgar Allan Poe", "flag": "🇺🇸", "years": "1809-1849", "century": 19, "country": "ABD", "works": "Kuzgun, Usher Evinin Cokusu", "bio": "Korku ve gizem turunun kurucusu.", "emoji": "🦅"},
        {"name": "Oscar Wilde", "flag": "🇮🇪", "years": "1854-1900", "century": 19, "country": "Irlanda", "works": "Dorian Gray'in Portresi", "bio": "Zarif uslubu ve keskin zekâsiyla taninan Irlanda'li yazar.", "emoji": "🌻"},
        {"name": "Miguel de Cervantes", "flag": "🇪🇸", "years": "1547-1616", "century": 16, "country": "Ispanya", "works": "Don Kisot", "bio": "Modern romanin kurucusu kabul edilen Ispanyol yazar.", "emoji": "🐴"},
        {"name": "Dante Alighieri", "flag": "🇮🇹", "years": "1265-1321", "century": 13, "country": "Italya", "works": "Ilahi Komedya", "bio": "Italyan edebiyatinin babasi ve ortacag siirinin zirvesi.", "emoji": "🔥"},
        {"name": "Homeros", "flag": "🇬🇷", "years": "MO 8. yuzyil", "century": -8, "country": "Yunanistan", "works": "Ilyada, Odysseia", "bio": "Bati edebiyatinin temeli kabul edilen eski Yunan ozan.", "emoji": "⚔️"},
        {"name": "Johann W. Goethe", "flag": "🇩🇪", "years": "1749-1832", "century": 18, "country": "Almanya", "works": "Faust, Genc Werther'in Acilari", "bio": "Alman edebiyatinin en buyuk ismi.", "emoji": "🎭"},
        {"name": "Anton Chekhov", "flag": "🇷🇺", "years": "1860-1904", "century": 19, "country": "Rusya", "works": "Visne Bahcesi, Marti", "bio": "Modern kisa oykunun ve tiyatronun ustasi.", "emoji": "🌸"},
        {"name": "Honore de Balzac", "flag": "🇫🇷", "years": "1799-1850", "century": 19, "country": "Fransa", "works": "Goriot Baba, Insanlarin Komedyasi", "bio": "Realist romanin kurucularindan Fransiz romanci.", "emoji": "🏠"},
        {"name": "Alexandre Dumas", "flag": "🇫🇷", "years": "1802-1870", "century": 19, "country": "Fransa", "works": "Uc Silahsorler, Monte Kristo Kontu", "bio": "Macera romaninin ustasi.", "emoji": "⚔️"},
        {"name": "Sabahattin Ali", "flag": "🇹🇷", "years": "1907-1948", "century": 20, "country": "Turkiye", "works": "Kurk Mantolu Madonna, Icimideki Seytan", "bio": "Turk edebiyatinin en cok okunan ve sevilen yazarlarindan.", "emoji": "🌙"},
        {"name": "Nazim Hikmet", "flag": "🇹🇷", "years": "1902-1963", "century": 20, "country": "Turkiye", "works": "Memleketimden Insan Manzaralari", "bio": "Dunya capinda taninmis buyuk Turk sairi.", "emoji": "✊"},
        {"name": "Yasar Kemal", "flag": "🇹🇷", "years": "1923-2015", "century": 20, "country": "Turkiye", "works": "Ince Memed, Yer Demir Gok Bakir", "bio": "Nobel adayi, Anadolu destanlarinin buyuk anlaticisi.", "emoji": "🏔️"},
        {"name": "Orhan Pamuk", "flag": "🇹🇷", "years": "1952-", "century": 20, "country": "Turkiye", "works": "Benim Adim Kirmizi, Masumiyet Muzesi", "bio": "Nobel Edebiyat Odulu sahibi Turk romanci.", "emoji": "🖋️"},
        {"name": "Elif Safak", "flag": "🇹🇷", "years": "1971-", "century": 20, "country": "Turkiye", "works": "Ask, 10 Dakika 38 Saniye", "bio": "Dunya capinda okunan cagdas Turk yazari.", "emoji": "🦋"},
    ]

    quiz_questions = [
        {"q": "Suc ve Ceza kimin eseridir?", "opts": ["Tolstoy", "Dostoyevski", "Chekhov", "Gogol"], "ans": 1},
        {"q": "1984 romanini kim yazmistir?", "opts": ["Huxley", "Bradbury", "Orwell", "Kafka"], "ans": 2},
        {"q": "Don Kisot hangi yazarin eseridir?", "opts": ["Cervantes", "Dante", "Hugo", "Dumas"], "ans": 0},
        {"q": "Kurk Mantolu Madonna kimin eseridir?", "opts": ["Yasar Kemal", "Orhan Pamuk", "Nazim Hikmet", "Sabahattin Ali"], "ans": 3},
        {"q": "Ince Memed romaninin yazari kimdir?", "opts": ["Sabahattin Ali", "Yasar Kemal", "Elif Safak", "Orhan Pamuk"], "ans": 1},
        {"q": "Hamlet kimin eseridir?", "opts": ["Dickens", "Shakespeare", "Wilde", "Poe"], "ans": 1},
        {"q": "Sefiller romanini kim yazmistir?", "opts": ["Balzac", "Dumas", "Hugo", "Flaubert"], "ans": 2},
        {"q": "Donusum novellasinin yazari kimdir?", "opts": ["Kafka", "Camus", "Sartre", "Beckett"], "ans": 0},
        {"q": "Ilahi Komedya kimin eseridir?", "opts": ["Homeros", "Vergilius", "Dante", "Petrarca"], "ans": 2},
        {"q": "Faust kimin eseridir?", "opts": ["Schiller", "Goethe", "Heine", "Mann"], "ans": 1},
    ]

    authors_json = json.dumps(authors, ensure_ascii=False)
    quiz_json = json.dumps(quiz_questions, ensure_ascii=False)

    countries = sorted(set(a["country"] for a in authors))
    centuries_raw = sorted(set(a["century"] for a in authors))
    century_labels = {c: (f"MO {abs(c)}. yy" if c < 0 else f"{c}. yy") for c in centuries_raw}

    html_code = f"""
    <div id="yd-app" style="font-family:'Segoe UI',sans-serif;">
    <style>
        #yd-app {{ background: linear-gradient(135deg,#0a1628,#0d1b36); padding:20px; border-radius:16px; border:1px solid #c9a84c; }}
        .yd-title {{ color:#c9a84c; text-align:center; font-size:26px; margin-bottom:6px; }}
        .yd-sub {{ color:#8899bb; text-align:center; margin-bottom:20px; }}
        .yd-filters {{ display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin-bottom:18px; }}
        .yd-filters select {{ background:#162240; color:#c9a84c; border:1px solid #c9a84c44; border-radius:8px; padding:6px 14px; font-size:14px; }}
        .yd-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:14px; max-height:600px; overflow-y:auto; padding:4px; }}
        .yd-card {{
            background: linear-gradient(135deg,#0f1d34,#162240); border:1px solid rgba(201,168,76,0.2);
            border-radius:12px; padding:16px; cursor:pointer; transition:all 0.3s;
        }}
        .yd-card:hover {{ border-color:#c9a84c; transform:translateY(-3px); box-shadow:0 8px 24px rgba(201,168,76,0.15); }}
        .yd-card .emoji {{ font-size:36px; display:block; margin-bottom:8px; }}
        .yd-card .name {{ color:#c9a84c; font-size:16px; font-weight:bold; }}
        .yd-card .meta {{ color:#8899bb; font-size:12px; margin:4px 0; }}
        .yd-card .works {{ color:#aab; font-size:12px; font-style:italic; }}
        .yd-detail {{
            display:none; background:linear-gradient(135deg,#0f1d34,#1a2744);
            border:2px solid #c9a84c; border-radius:14px; padding:24px; margin:16px 0;
            color:#ddd;
        }}
        .yd-detail h3 {{ color:#c9a84c; margin:0 0 8px 0; }}
        .yd-detail .close {{ float:right; color:#c9a84c; cursor:pointer; font-size:20px; }}
        .yd-quiz {{ background:linear-gradient(135deg,#0f1d34,#162240); border:1px solid rgba(201,168,76,0.3); border-radius:14px; padding:20px; margin-top:20px; }}
        .yd-quiz h3 {{ color:#c9a84c; text-align:center; }}
        .quiz-q {{ color:#ddd; margin:14px 0 6px 0; font-weight:bold; }}
        .quiz-opts label {{ display:block; color:#aab; padding:3px 0; cursor:pointer; }}
        .quiz-opts input {{ accent-color:#c9a84c; margin-right:6px; }}
        .quiz-btn {{ background:linear-gradient(135deg,#c9a84c,#a3852e); color:#0a1628; border:none; padding:10px 28px; border-radius:8px; cursor:pointer; font-weight:bold; margin-top:12px; font-size:15px; }}
        .quiz-result {{ color:#c9a84c; font-size:18px; font-weight:bold; margin-top:12px; text-align:center; }}
    </style>
    <h2 class="yd-title">🌍 Yazarlar Dunyasi</h2>
    <p class="yd-sub">25 buyuk yazar, eserleri ve hayatlari</p>
    <div class="yd-filters">
        <select id="f-country" onchange="filterCards()">
            <option value="">Tum Ulkeler</option>
            {"".join(f'<option value="{c}">{c}</option>' for c in countries)}
        </select>
        <select id="f-century" onchange="filterCards()">
            <option value="">Tum Yuzyillar</option>
            {"".join(f'<option value="{c}">{century_labels[c]}</option>' for c in centuries_raw)}
        </select>
    </div>
    <div id="detail-panel" class="yd-detail"></div>
    <div class="yd-grid" id="cards-grid"></div>
    <div class="yd-quiz">
        <h3>🧠 Yazar Quiz (10 Soru)</h3>
        <div id="quiz-area"></div>
        <button class="quiz-btn" onclick="checkQuiz()">Kontrol Et</button>
        <div id="quiz-result" class="quiz-result"></div>
    </div>
    </div>
    <script>
    var authors = {authors_json};
    var quizData = {quiz_json};

    function renderCards(list) {{
        var grid = document.getElementById('cards-grid');
        grid.innerHTML = '';
        list.forEach(function(a, i) {{
            var card = document.createElement('div');
            card.className = 'yd-card';
            card.setAttribute('data-country', a.country);
            card.setAttribute('data-century', a.century);
            card.innerHTML = '<span class="emoji">' + a.emoji + ' ' + a.flag + '</span>'
                + '<span class="name">' + a.name + '</span>'
                + '<div class="meta">' + a.years + '</div>'
                + '<div class="works">' + a.works + '</div>';
            card.onclick = function() {{ showDetail(a); }};
            grid.appendChild(card);
        }});
    }}

    function showDetail(a) {{
        var panel = document.getElementById('detail-panel');
        panel.style.display = 'block';
        panel.innerHTML = '<span class="close" onclick="this.parentElement.style.display=\'none\'">&times;</span>'
            + '<h3>' + a.emoji + ' ' + a.name + ' ' + a.flag + '</h3>'
            + '<p style="color:#8899bb;">' + a.years + ' | ' + a.country + '</p>'
            + '<p style="color:#ddd;">' + a.bio + '</p>'
            + '<p style="color:#c9a84c; font-style:italic;">Eserleri: ' + a.works + '</p>';
        panel.scrollIntoView({{ behavior:'smooth' }});
    }}

    function filterCards() {{
        var fc = document.getElementById('f-country').value;
        var fy = document.getElementById('f-century').value;
        var filtered = authors.filter(function(a) {{
            if (fc && a.country !== fc) return false;
            if (fy && String(a.century) !== fy) return false;
            return true;
        }});
        renderCards(filtered);
    }}

    function renderQuiz() {{
        var area = document.getElementById('quiz-area');
        var html = '';
        quizData.forEach(function(q, i) {{
            html += '<div class="quiz-q">' + (i+1) + '. ' + q.q + '</div><div class="quiz-opts">';
            q.opts.forEach(function(o, j) {{
                html += '<label><input type="radio" name="qq' + i + '" value="' + j + '"> ' + o + '</label>';
            }});
            html += '</div>';
        }});
        area.innerHTML = html;
    }}

    function checkQuiz() {{
        var score = 0;
        quizData.forEach(function(q, i) {{
            var sel = document.querySelector('input[name="qq' + i + '"]:checked');
            if (sel && parseInt(sel.value) === q.ans) score++;
        }});
        document.getElementById('quiz-result').innerText = 'Sonuc: ' + score + ' / ' + quizData.length + ' dogru!';
    }}

    renderCards(authors);
    renderQuiz();
    </script>
    """
    components.html(html_code, height=1100, scrolling=True)


# ============================================================
# 4. OKUMA MARATONU
# ============================================================
def render_okuma_maratonu():
    """Okuma Maratonu - Gamified Reading Tracker"""
    st.markdown("""
    <style>
    .om-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a2744 50%, #0d1b36 100%);
        border: 1px solid #c9a84c; border-radius: 16px;
        padding: 24px 32px; text-align: center; margin-bottom: 20px;
    }
    .om-header h2 { color: #c9a84c; font-size: 28px; margin: 0; }
    .om-header p { color: #8899bb; margin: 4px 0 0 0; }
    .om-stat {
        background: linear-gradient(135deg, #0f1d34, #162240);
        border: 1px solid rgba(201,168,76,0.25); border-radius: 12px;
        padding: 16px; text-align: center;
    }
    .om-stat .val { color: #c9a84c; font-size: 32px; font-weight: bold; }
    .om-stat .lbl { color: #8899bb; font-size: 13px; }
    .om-badge {
        display: inline-block; padding: 10px 18px; border-radius: 24px;
        margin: 4px; font-size: 14px; font-weight: bold;
        border: 1px solid rgba(201,168,76,0.3);
    }
    .om-badge.earned { background: rgba(201,168,76,0.15); color: #f0d27a; border-color: #c9a84c; }
    .om-badge.locked { background: rgba(50,60,80,0.3); color: #556; border-color: #334; }
    .om-quote {
        background: linear-gradient(135deg, #0f1d34, #162240);
        border-left: 4px solid #c9a84c; border-radius: 0 12px 12px 0;
        padding: 16px 20px; margin: 16px 0; font-style: italic; color: #aab;
    }
    .om-quote .author { color: #c9a84c; font-style: normal; font-weight: bold; margin-top: 8px; }
    </style>
    <div class="om-header">
        <h2>🏃 Okuma Maratonu</h2>
        <p>Her gun oku, rekorunu kir!</p>
    </div>
    """, unsafe_allow_html=True)

    # Session state init
    if "om_log" not in st.session_state:
        st.session_state.om_log = {}
    if "om_total" not in st.session_state:
        st.session_state.om_total = 0

    bugun = datetime.now().strftime("%Y-%m-%d")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        sayfa = st.number_input("Bugun kac sayfa okudun?", 0, 1000, 0, 5, key="om_sayfa")
    with col2:
        st.write("")
        st.write("")
        if st.button("📝 Kaydet", key="om_kaydet", type="primary"):
            st.session_state.om_log[bugun] = st.session_state.om_log.get(bugun, 0) + sayfa
            st.session_state.om_total += sayfa
            st.success(f"+{sayfa} sayfa kaydedildi!")
    with col3:
        st.write("")
        st.write("")
        if st.button("🔄 Sifirla", key="om_reset"):
            st.session_state.om_log = {}
            st.session_state.om_total = 0
            st.info("Veriler sifirlandi.")

    # Calculate streak
    streak = 0
    check_date = datetime.now()
    for _ in range(365):
        ds = check_date.strftime("%Y-%m-%d")
        if ds in st.session_state.om_log and st.session_state.om_log[ds] > 0:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    toplam = st.session_state.om_total
    bugun_sayfa = st.session_state.om_log.get(bugun, 0)

    # Stats
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="om-stat"><div class="val">{toplam}</div><div class="lbl">Toplam Sayfa</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="om-stat"><div class="val">{bugun_sayfa}</div><div class="lbl">Bugun</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="om-stat"><div class="val">{streak}</div><div class="lbl">Gun Serisi</div></div>', unsafe_allow_html=True)
    with s4:
        gun_sayisi = max(len(st.session_state.om_log), 1)
        st.markdown(f'<div class="om-stat"><div class="val">{toplam // gun_sayisi}</div><div class="lbl">Ort/Gun</div></div>', unsafe_allow_html=True)

    # Badge system
    badges = [
        (10, "📖 Baslangic", "10 sayfa"),
        (50, "📚 Okur", "50 sayfa"),
        (200, "🏆 Kitap Kurdu", "200 sayfa"),
        (500, "👑 Efsane", "500 sayfa"),
    ]
    badges_html = ""
    for threshold, label, desc in badges:
        cls = "earned" if toplam >= threshold else "locked"
        badges_html += f'<span class="om-badge {cls}">{label} ({desc})</span>'

    st.markdown(f"""
    <div style="text-align:center; margin:16px 0;">
        <h4 style="color:#c9a84c;">🏅 Rozetler</h4>
        {badges_html}
    </div>
    """, unsafe_allow_html=True)

    # Weekly chart
    st.markdown("#### 📊 Haftalik Okuma Grafigi")
    chart_data = {}
    for i in range(6, -1, -1):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        chart_data[d[-5:]] = st.session_state.om_log.get(d, random.randint(5, 45))
    import pandas as pd
    df = pd.DataFrame({"Sayfa": chart_data.values()}, index=chart_data.keys())
    st.bar_chart(df)

    # Leaderboard
    st.markdown("#### 🏆 Liderlik Tablosu")
    liderler = [
        ("Ahmet Yilmaz", 520), ("Elif Kara", 485), ("Zeynep Demir", 430),
        ("Mehmet Can", 395), ("Ayse Turk", 360), ("Burak Oz", 315),
        ("Fatma Aksoy", 280), ("Emre Dogan", 245),
        ("Selin Kaya", 210), ("Cem Celik", 180),
    ]
    rows = ""
    medals = ["🥇", "🥈", "🥉"]
    for i, (name, pages) in enumerate(liderler):
        rank = medals[i] if i < 3 else f"#{i+1}"
        bg = "rgba(201,168,76,0.08)" if i % 2 == 0 else "transparent"
        rows += f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
            padding:8px 16px; background:{bg}; border-radius:6px; color:#ccc; margin:2px 0;">
            <span style="color:#c9a84c; font-weight:bold; width:40px;">{rank}</span>
            <span style="flex:1;">{name}</span>
            <span style="color:#f0d27a; font-weight:bold;">{pages} sayfa</span>
        </div>"""
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f1d34,#162240); border:1px solid rgba(201,168,76,0.2);
        border-radius:12px; padding:12px; margin-top:8px;">
        {rows}
    </div>
    """, unsafe_allow_html=True)

    # Motivational quote
    quotes = [
        ("Bir kitap, butun bir dunyayi degistirebilir.", "Malala Yousafzai"),
        ("Okuyan bir zihin, her yere seyahat eder.", "Paulo Coelho"),
        ("Kitaplar, ruhun en iyi dostlaridir.", "Voltaire"),
        ("Okumak, baskalarinin dusunceleriyle dusunmektir.", "Arthur Schopenhauer"),
        ("Bir oda kitapsiz, bir beden ruhsuz gibidir.", "Cicero"),
        ("Okumak insani doldurur, konusmak hazirlar, yazmak kesinlestirir.", "Francis Bacon"),
        ("Bir kitap, bin ogretmene bedeldir.", "Anonim"),
    ]
    day_index = datetime.now().timetuple().tm_yday % len(quotes)
    q, a = quotes[day_index]
    st.markdown(f"""
    <div class="om-quote">
        "{q}"
        <div class="author">— {a}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 5. KITAP OZET MAKINESI
# ============================================================
def render_kitap_ozet_makinesi():
    """Kitap Ozet Makinesi - 20 unlu kitabin ozeti"""
    st.markdown("""
    <style>
    .ko-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a2744 50%, #0d1b36 100%);
        border: 1px solid #c9a84c; border-radius: 16px;
        padding: 24px 32px; text-align: center; margin-bottom: 20px;
    }
    .ko-header h2 { color: #c9a84c; font-size: 28px; margin: 0; }
    .ko-header p { color: #8899bb; margin: 4px 0 0 0; }
    .ko-card {
        background: linear-gradient(135deg, #0f1d34, #162240);
        border: 1px solid rgba(201,168,76,0.25); border-radius: 12px;
        padding: 16px; margin-bottom: 10px; color: #ddd;
    }
    .ko-card h4 { color: #c9a84c; margin: 0 0 8px 0; }
    .ko-char {
        background: rgba(201,168,76,0.06); border-left: 3px solid #c9a84c;
        border-radius: 0 8px 8px 0; padding: 10px 14px; margin: 6px 0; color: #ccc;
    }
    .ko-char b { color: #f0d27a; }
    .ko-theme {
        display: inline-block; background: rgba(201,168,76,0.12);
        border: 1px solid rgba(201,168,76,0.3); border-radius: 20px;
        padding: 6px 16px; margin: 4px; color: #c9a84c; font-size: 13px;
    }
    .ko-quote {
        border-left: 3px solid #c9a84c; padding: 10px 16px;
        margin: 8px 0; font-style: italic; color: #aab;
        background: rgba(201,168,76,0.04); border-radius: 0 8px 8px 0;
    }
    </style>
    <div class="ko-header">
        <h2>📋 Kitap Ozet Makinesi</h2>
        <p>200 unlu kitabin ozeti, karakterleri, temalari ve alintilari</p>
    </div>
    """, unsafe_allow_html=True)

    from views._kitap_ozetleri import KITAP_OZETLERI
    kitaplar = KITAP_OZETLERI

    # Kategori filtresi
    kategoriler = sorted(set(v.get("kategori", "Diger") for v in kitaplar.values()))
    col_kat, col_ara = st.columns([1, 2])
    with col_kat:
        sec_kat = st.selectbox("Kategori", ["Tumu"] + kategoriler, key="ko_kat")
    with col_ara:
        arama = st.text_input("Kitap veya yazar ara", key="ko_ara", placeholder="Ara...")

    # Filtrele
    filtered = kitaplar
    if sec_kat != "Tumu":
        filtered = {k: v for k, v in filtered.items() if v.get("kategori") == sec_kat}
    if arama:
        q = arama.lower()
        filtered = {k: v for k, v in filtered.items() if q in k.lower()}

    st.caption(f"{len(filtered)} kitap listeleniyor")

    kitap_isimleri = sorted(filtered.keys())
    if not kitap_isimleri:
        st.warning("Filtreye uyan kitap bulunamadi.")
        return
    secili = st.selectbox("Kitap Secin", kitap_isimleri, key="ko_kitap")
    kitap = kitaplar[secili]

    t1, t2, t3, t4 = st.tabs(["📖 Ozet", "👥 Ana Karakterler", "🎯 Temalar", "💬 Onemli Alintilar"])

    with t1:
        st.markdown(f"""
        <div class="ko-card">
            <h4>📖 {secili}</h4>
            <p style="line-height:1.8; font-size:15px;">{kitap["ozet"]}</p>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        for isim, aciklama in kitap["karakterler"]:
            st.markdown(f"""
            <div class="ko-char">
                <b>{isim}</b><br/>
                <span style="font-size:14px;">{aciklama}</span>
            </div>
            """, unsafe_allow_html=True)

    with t3:
        themes_html = ""
        for tema in kitap["temalar"]:
            themes_html += f'<span class="ko-theme">{tema}</span>'
        st.markdown(f"""
        <div style="padding:12px 0;">
            {themes_html}
        </div>
        """, unsafe_allow_html=True)

    with t4:
        for alinti in kitap["alintilar"]:
            st.markdown(f"""
            <div class="ko-quote">
                "{alinti}"
            </div>
            """, unsafe_allow_html=True)
