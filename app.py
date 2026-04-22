"""
SmartCampus AI - Ana Uygulama Giris Noktasi
============================================
Turk ozel okullari icin akademik yonetim platformu.
"""

import streamlit as st


from config import setup_page_config, init_session_state, apply_theme
from utils.auth import AuthManager, get_user_modules

# ── Plotly template — sadece ilk yüklemede ──
if "_chart_utils_loaded" not in st.session_state:
    import utils.chart_utils  # noqa: F401 — Plotly gold template kaydeder
    st.session_state["_chart_utils_loaded"] = True

# ── Otomatik günlük yedekleme — günde 1 kez ──
if "_backup_done" not in st.session_state:
    try:
        from utils.backup import auto_backup
        auto_backup(max_backups=30)
    except Exception:
        pass
    st.session_state["_backup_done"] = True

# __pycache__ temizleme KALDIRILDI — her render'da tum modulleri yeniden
# derlemek sayfa gecislerini cok agirlatiyordu. Python'un .pyc cache'i
# dosya degistiginde otomatik yenilenir, manuel silmeye gerek yok.

# ── SAYFA YAPISI ─────────────────────────────────────────────────────────────
setup_page_config()
init_session_state()
apply_theme()

# ── PUBLIC TUR REZERVASYONU (login gerektirmez) ─────────────────────────────
_qr_aksiyon_pre = st.query_params.get("aksiyon", "")
if _qr_aksiyon_pre == "tur_rezerve":
    try:
        from utils.kayit_tur_ui import render_public_tur_form
        render_public_tur_form()
    except Exception as _e:
        st.error(f"Tur rezervasyon formu yuklenemedi: {_e}")
    st.stop()

# ── PUBLIC AI MUZAKERE (login gerektirmez) ───────────────────────────────────
if _qr_aksiyon_pre == "ai_pazarlik":
    try:
        from utils.kayit_muzakere_ui import render_public_muzakere
        render_public_muzakere()
    except Exception as _e:
        st.error(f"Pazarlik chat yuklenemedi: {_e}")
    st.stop()

# ── PUBLIC ETKINLIK RSVP (login gerektirmez) ─────────────────────────────────
if _qr_aksiyon_pre == "etkinlik_kayit":
    try:
        from utils.kayit_etkinlik_ui import render_public_rsvp_form
        render_public_rsvp_form()
    except Exception as _e:
        st.error(f"Etkinlik kayit formu yuklenemedi: {_e}")
    st.stop()

# ── QR KOD ILE OGRENCI SINAV GIRISI (login gerektirmez) ──────────────────────
_qr_sinav_kod = st.query_params.get("sinav_kod", "")
_qr_aksiyon = st.query_params.get("aksiyon", "")
if _qr_sinav_kod and _qr_aksiyon == "sinav_giris":
    # QR ile gelen öğrenciyi doğrudan sınava yönlendir
    st.session_state['_qr_erisim_kodu'] = _qr_sinav_kod
    # Kişisel QR'dan öğrenci bilgilerini al
    _qr_oad = st.query_params.get("oad", "")
    _qr_ono = st.query_params.get("ono", "")
    _qr_osb = st.query_params.get("osb", "")
    _qr_oid = st.query_params.get("oid", "")
    if _qr_oad or _qr_ono:
        import urllib.parse as _up
        st.session_state['_qr_ogrenci'] = {
            "ad": _up.unquote(_qr_oad),
            "no": _qr_ono,
            "sube": _qr_osb,
            "id": _qr_oid,
        }
    # Query params temizle
    try:
        for _p in ["sinav_kod", "aksiyon", "modul", "oad", "ono", "osb", "oid"]:
            if _p in st.query_params:
                del st.query_params[_p]
    except Exception:
        pass
    # Ogrenci olarak otomatik giris
    if not AuthManager.is_authenticated():
        st.session_state["auth_user"] = {
            "username": "ogrenci_sinav",
            "name": "Öğrenci",
            "role": "ogrenci",
            "auto_login": True,
        }
    # Olcme degerlendirme modulune yonlendir
    st.session_state["secili_modul"] = "Olcme ve Degerlendirme"
    from views.olcme_degerlendirme_v2 import render_olcme_degerlendirme_v2
    render_olcme_degerlendirme_v2()
    st.stop()

# ── KIMLIK DOGRULAMA ─────────────────────────────────────────────────────────
if not AuthManager.is_authenticated():
    AuthManager.render_login_screen()
    st.stop()

# ── MODUL GRUPLARI (sidebar navigasyonu icin) ─────────────────────────────────
_MODUL_GRUPLARI = [
    {
        "baslik": "GENEL",
        "moduller": [
            ("Ana Sayfa",            "🏠"),
            ("Yonetim Tek Ekran",    "📊"),
        ],
    },
    {
        "baslik": "KURUM",
        "moduller": [
            ("Kurumsal Organizasyon ve Iletisim", "🏢"),
            ("Kayit Modulu",                      "🎯"),
            ("Sosyal Medya Yonetimi",             "📱"),
            ("Insan Kaynaklari Yonetimi",         "👥"),
            ("Butce Gelir Gider",                 "💰"),
            ("Odeme Takip",                       "💳"),
            ("Veli-Ogretmen Gorusme",             "🤝"),
            ("Randevu ve Ziyaretci",           "📅"),
            ("Toplanti ve Kurullar",            "🤝"),
            ("Kurum Hizmetleri",               "🏛️"),
        ],
    },
    {
        "baslik": "AKADEMIK",
        "moduller": [
            ("Ogrenci Zeka Merkezi",           "🧠"),
            ("Okul Oncesi - Ilkokul",          "🎨"),
            ("Akademik Takip",                 "📚"),
            ("Olcme ve Degerlendirme",         "📝"),
            ("Rehberlik",                      "🧠"),
            ("Analitik Dashboard",              "📊"),
            ("Sertifika Uretici",              "🏆"),
            ("Okul Sagligi Takip",             "🏥"),
            ("Sosyal Etkinlik ve Kulupler",    "🎭"),
            ("Kutuphane",                      "📖"),
            ("AI Ogrenme Platformu",           "🎓"),
            ("Yabanci Dil",                    "🌍"),
            ("Kisisel Dil Gelisimi",           "🎓"),
            ("Egitim Koclugu",                 "🏅"),
            ("AI Treni",                       "🚂"),
            ("STEAM Merkezi",                  "🔬"),
        ],
    },
    {
        "baslik": "OPERASYON",
        "moduller": [
            ("Servis GPS Takip",               "🚌"),
            ("Kutuphane Barkod",               "📚"),
            ("Yemek Tercihi ve Alerji",        "🍽️"),
            ("Tesis ve Varlik Yonetimi",       "🏗️"),
            ("Sivil Savunma ve IS Guvenligi",  "⛑️"),
            ("Mezunlar ve Kariyer Yonetimi",   "🎓"),
        ],
    },
    {
        "baslik": "SİSTEM",
        "moduller": [
            ("AI Destek", "🤖"),
        ],
    },
]


def _sidebar_css():
    """Sidebar premium stilleri + global tab wrap fix."""
    if st.session_state.get("_sb_css_done"):
        return
    st.session_state["_sb_css_done"] = True
    st.markdown(
        """
        <style>
        /* ═══ NUCLEAR DARK THEME TEXT FIX ═══
           Tüm modüllerde koyu arka plan üzerinde tüm metinleri
           okunabilir yapar. Inline style override'ları ezer. */

        /* Temel metin rengi — her yerde açık (span/div hariç — BaseWeb iç elemanlarını bozar) */
        html body .stApp p,
        html body .stApp li,
        html body .stApp td,
        html body .stApp th,
        html body .stApp label,
        html body .stApp summary,
        html body .stApp strong,
        html body .stApp b,
        html body .stApp h1, html body .stApp h2,
        html body .stApp h3, html body .stApp h4,
        html body .stApp h5, html body .stApp h6 {
            color: #e2e8f0 !important;
        }

        /* span/div — sadece doğrudan metin taşıyan Streamlit elemanlarını hedefle */
        html body .stApp .stMarkdown span,
        html body .stApp .stMarkdown div,
        html body .stApp [data-testid="stText"] span,
        html body .stApp [data-testid="stMetricValue"] div,
        html body .stApp [data-testid="stCaptionContainer"] span,
        html body .stApp [data-testid="stWidgetLabel"] span,
        html body .stApp [data-testid="stWidgetLabel"] div,
        html body .stApp [data-testid="stWidgetLabel"] p,
        html body .stApp .stAlert span,
        html body .stApp .stAlert div {
            color: #e2e8f0 !important;
        }

        /* Muted/secondary metinler */
        html body .stApp .sc-text-muted,
        html body .stApp [data-testid="stMetricLabel"],
        html body .stApp small {
            color: #94a3b8 !important;
        }

        /* Başlıklar — biraz daha parlak */
        html body .stApp h1,
        html body .stApp h2 {
            color: #f1f5f9 !important;
        }

        /* Linkler */
        html body .stApp a {
            color: #93c5fd !important;
        }
        html body .stApp a:hover {
            color: #bfdbfe !important;
        }

        /* İnline style'larda koyu renk kullanan div'ler için override */
        html body .stApp [style*="color: #0B0F19"],
        html body .stApp [style*="color:#0B0F19"],
        html body .stApp [style*="color: #334155"],
        html body .stApp [style*="color:#334155"],
        html body .stApp [style*="color: #1f2937"],
        html body .stApp [style*="color:#1f2937"],
        html body .stApp [style*="color: #111827"],
        html body .stApp [style*="color:#111827"],
        html body .stApp [style*="color: #0f172a"],
        html body .stApp [style*="color:#0f172a"],
        html body .stApp [style*="color: #1e293b"],
        html body .stApp [style*="color:#1e293b"],
        html body .stApp [style*="color: #374151"],
        html body .stApp [style*="color:#374151"] {
            color: #e2e8f0 !important;
        }

        /* Orta koyu gri metinleri biraz açığa çek */
        html body .stApp [style*="color: #475569"],
        html body .stApp [style*="color:#475569"],
        html body .stApp [style*="color: #4b5563"],
        html body .stApp [style*="color:#4b5563"],
        html body .stApp [style*="color: #64748b"],
        html body .stApp [style*="color:#64748b"],
        html body .stApp [style*="color: #6b7280"],
        html body .stApp [style*="color:#6b7280"] {
            color: #94a3b8 !important;
        }

        /* Beyaz arka planlı kartları koyu yap */
        html body .stApp [style*="background: #fff"],
        html body .stApp [style*="background:#fff"],
        html body .stApp [style*="background: white"],
        html body .stApp [style*="background:white"],
        html body .stApp [style*="background-color: #fff"],
        html body .stApp [style*="background-color:#fff"],
        html body .stApp [style*="background-color: white"],
        html body .stApp [style*="background-color:white"] {
            background: #131825 !important;
        }

        /* Açık gradient arka planları koyu yap */
        html body .stApp [style*="background: linear-gradient"][style*="#f"],
        html body .stApp [style*="background:linear-gradient"][style*="#f"] {
            /* Açık renkli gradient'ler — koyu arka plana çevir */
        }

        /* ═══ RADIO / CHECKBOX NUCLEAR FIX ═══ */
        /* BaseWeb radio inline style override — rgb() formatini ezmek icin */
        html body .stApp .stRadio [role="radiogroup"] label,
        html body .stApp .stRadio [role="radiogroup"] label div,
        html body .stApp .stRadio [role="radiogroup"] label div p,
        html body .stApp .stRadio [role="radiogroup"] label span,
        html body .stApp .stRadio [data-baseweb="radio"] label,
        html body .stApp .stRadio [data-baseweb="radio"] label div,
        html body .stApp .stRadio [data-baseweb="radio"] label span {
            color: #e2e8f0 !important;
        }
        /* Radio soru basligi (en ustteki label) */
        html body .stApp .stRadio > label,
        html body .stApp .stRadio > label div,
        html body .stApp .stRadio > label div p,
        html body .stApp .stRadio > label p,
        html body .stApp .stRadio > label span {
            color: #f1f5f9 !important;
        }
        /* Checkbox metin */
        html body .stApp .stCheckbox label span,
        html body .stApp .stCheckbox [data-baseweb="checkbox"] label span {
            color: #e2e8f0 !important;
        }
        /* Selectbox dropdown secili deger metni */
        html body .stApp .stSelectbox [data-baseweb="select"] > div,
        html body .stApp .stSelectbox [data-baseweb="select"] span,
        html body .stApp .stMultiSelect [data-baseweb="select"] > div,
        html body .stApp .stMultiSelect [data-baseweb="select"] span {
            color: #e2e8f0 !important;
        }

        /* Expander metin rengi */
        html body .stApp [data-testid="stExpander"] summary {
            color: #e2e8f0 !important;
        }
        html body .stApp [data-testid="stExpander"] summary p {
            color: #e2e8f0 !important;
        }
        /* Expander toggle icon — font-size:0 ile ham metni gizle, ikon olarak göster */
        html body .stApp [data-testid="stExpanderToggleIcon"],
        html body .stApp [data-testid="stExpanderToggleIcon"] span {
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
            -webkit-font-feature-settings: 'liga' 1 !important;
            font-feature-settings: 'liga' 1 !important;
            overflow: hidden !important;
            width: 24px !important;
            height: 24px !important;
        }

        /* Tab metinleri — seçili olmayan */
        html body .stApp [role="tab"] p {
            color: #94a3b8 !important;
        }
        html body .stApp [role="tab"][aria-selected="true"] p {
            color: #ffffff !important;
        }

        /* Select/dropdown metin rengi — sadece görünen değer alanı */
        html body .stApp [data-baseweb="select"] [data-testid="stMarkdownContainer"] span,
        html body .stApp [data-baseweb="select"] > div > div:first-child {
            color: #e2e8f0 !important;
        }
        /* Dropdown listesi seçenekleri */
        html body .stApp [data-baseweb="menu"] li,
        html body .stApp [data-baseweb="menu"] [role="option"],
        html body .stApp [data-baseweb="menu"] [role="option"] span {
            color: #e2e8f0 !important;
        }
        /* Seçili değer metni */
        html body .stApp [data-baseweb="select"] [aria-selected="true"],
        html body .stApp [data-baseweb="select"] .st-emotion-cache-1dimb5e {
            color: #e2e8f0 !important;
        }
        /* BaseWeb iç elemanlarındaki gizli metinleri gizle */
        html body .stApp [data-baseweb="select"] [aria-hidden="true"] {
            color: transparent !important;
        }

        /* Input placeholder */
        html body .stApp input::placeholder,
        html body .stApp textarea::placeholder {
            color: #64748b !important;
        }

        /* Font ailesi — emoji desteği dahil */
        * {
            font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, 'Apple Color Emoji',
                         'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji', sans-serif;
        }
        /* Material Icons / Symbols fontunu koru — Streamlit ikonları için zorunlu */
        [data-testid="stExpander"] summary svg,
        [data-testid="stExpanderToggleIcon"],
        [data-testid="stExpanderToggleIcon"] *,
        .material-symbols-rounded,
        .material-icons,
        [class*="Icon"],
        [data-testid="stExpander"] summary > span:first-child,
        [data-testid="stExpander"] summary [style*="font-family"] {
            font-family: 'Material Symbols Rounded', 'Material Icons', 'Material Icons Outlined', sans-serif !important;
            font-size: 24px !important;
            -webkit-font-feature-settings: 'liga' 1 !important;
            font-feature-settings: 'liga' 1 !important;
        }
        /* ═══ END NUCLEAR DARK THEME FIX ═══ */
        /* ─── END EMOJI FONT FIX ─── */

        /* ─── GLOBAL TAB WRAP FIX ─── */
        [role="tablist"] {
            flex-wrap: wrap !important;
            overflow: visible !important;
            overflow-x: visible !important;
            max-width: 100% !important;
        }
        div[data-testid="stTabs"] > div {
            overflow: visible !important;
            overflow-x: visible !important;
        }
        div[data-testid="stTabs"] > div > div {
            overflow: visible !important;
            overflow-x: visible !important;
        }
        [data-baseweb="tab-list"] {
            flex-wrap: wrap !important;
            overflow: visible !important;
            overflow-x: visible !important;
        }
        [role="tablist"] > button,
        [data-baseweb="tab-list"] > button {
            flex-shrink: 0 !important;
        }
        div[data-testid="stTabs"] div[data-testid="stTabs"] [role="tablist"] {
            flex-wrap: wrap !important;
            overflow: visible !important;
        }
        div[data-testid="stTabs"] div[data-testid="stTabs"] > div {
            overflow: visible !important;
        }
        div[data-testid="stTabs"] div[data-testid="stTabs"] div[data-testid="stTabs"] [role="tablist"] {
            flex-wrap: wrap !important;
            overflow: visible !important;
        }
        /* ─── END TAB WRAP FIX ─── */

        /* ─── KRİSTAL BERRAKLIK SIDEBAR NAV ─── */
        [data-testid="stSidebar"] [data-testid="stButton"] > button {
            background: transparent !important;
            color: #4B5563 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 7px 12px !important;
            font-size: .82rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            transition: all .2s ease !important;
            box-shadow: none !important;
            margin: 1px 0 !important;
        }
        [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
            background: rgba(79,70,229,.06) !important;
            color: #4F46E5 !important;
            transform: translateX(2px);
            border-left: 2px solid rgba(79,70,229,.4) !important;
        }
        [data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, rgba(79,70,229,.1), rgba(79,70,229,.04)) !important;
            color: #4F46E5 !important;
            font-weight: 700 !important;
            border-left: 3px solid #4F46E5 !important;
            box-shadow: 0 1px 3px rgba(79,70,229,.1) !important;
        }
        [data-testid="stSidebar"] [data-testid="stButton"] > button[kind="secondary"]:last-of-type {
            margin-top: 4px;
        }

        .sb-group-label {
            font-size: .62rem;
            font-weight: 800;
            letter-spacing: .12em;
            color: #4F46E5 !important;
            text-transform: uppercase;
            padding: 14px 12px 4px 12px;
            display: block;
            position: relative;
        }
        .sb-group-label::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            width: 3px;
            height: 14px;
            transform: translateY(-50%);
            background: linear-gradient(180deg, #4F46E5, transparent);
            border-radius: 2px;
        }

        .sb-user-card {
            background: linear-gradient(135deg, rgba(79,70,229,.06), rgba(79,70,229,.02));
            border: 1px solid rgba(79,70,229,.12);
            border-radius: 12px;
            padding: 12px 14px;
            margin: 8px 0 4px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .sb-avatar {
            width: 40px; height: 40px;
            background: linear-gradient(135deg, #4338CA, #4F46E5);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.05rem; font-weight: 700; color: white;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(79,70,229,.3);
        }
        .sb-user-info { display: flex; flex-direction: column; gap: 2px; }
        .sb-user-name { font-size: .875rem; font-weight: 600; color: #1A1D26 !important; }
        .sb-user-role {
            font-size: .68rem; color: #4F46E5 !important;
            font-weight: 500;
            letter-spacing: .03em;
        }

        /* Logo alani */
        .sb-logo {
            display: flex; align-items: center; gap: 12px;
            padding: 6px 6px 10px 6px;
        }
        .sb-logo-icon-box {
            width: 38px; height: 38px;
            background: linear-gradient(135deg, #4338CA, #4F46E5);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.3rem;
            box-shadow: 0 2px 10px rgba(79,70,229,.2);
        }
        .sb-logo-icon { font-size: 1.3rem; }
        .sb-logo-text { font-size: 1.05rem; font-weight: 700; color: #F1F5F9 !important; line-height: 1.2; }
        .sb-logo-sub  { font-size: .62rem; color: #94A3B8 !important; font-weight: 500; letter-spacing: .04em; }

        /* Versiyon badge */
        .sb-version {
            font-size: .55rem;
            color: #64748B !important;
            text-align: center;
            padding: 8px 0;
            letter-spacing: .05em;
        }
        </style>
        <script>
        // NUCLEAR V2: Tum koyu metinleri acik renge cevir
        (function() {
            function isDark(rgbStr) {
                if (!rgbStr) return false;
                var m = rgbStr.match(/rgb[(]([0-9]+),\\s*([0-9]+),\\s*([0-9]+)[)]/);
                if (!m) return false;
                var r = parseInt(m[1]), g = parseInt(m[2]), b = parseInt(m[3]);
                // Toplam < 380 ise koyu renk (siyah, koyu gri, koyu mavi vb.)
                return (r + g + b) < 380;
            }
            function fixAll() {
                // Radio + Checkbox — tum label, div, span, p
                var sels = [
                    '[data-baseweb="radio"] label', '[data-baseweb="radio"] label *',
                    '[data-baseweb="checkbox"] label', '[data-baseweb="checkbox"] label *',
                    '.stRadio label', '.stRadio label *',
                    '.stRadio p', '.stRadio span', '.stRadio div',
                    '.stCheckbox label', '.stCheckbox label *'
                ];
                document.querySelectorAll(sels.join(',')).forEach(function(el) {
                    if (isDark(window.getComputedStyle(el).color)) {
                        el.style.setProperty('color', '#e2e8f0', 'important');
                    }
                });
                // Genel metin — p, span, label, li, td, th, h1-h6
                document.querySelectorAll('.stApp p, .stApp label, .stApp li, .stApp td, .stApp th, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp strong, .stApp b').forEach(function(el) {
                    if (isDark(window.getComputedStyle(el).color)) {
                        // Inline style rengi varsa ve acik renkse dokunma
                        var inl = el.style.color;
                        if (inl && !isDark(inl)) return;
                        el.style.setProperty('color', '#e2e8f0', 'important');
                    }
                });
            }
            // Tekrarli calisma
            setTimeout(fixAll, 300);
            setTimeout(fixAll, 800);
            setTimeout(fixAll, 1500);
            setTimeout(fixAll, 3000);
            setTimeout(fixAll, 5000);
            // MutationObserver
            var obs = new MutationObserver(function() { setTimeout(fixAll, 150); });
            var wait = setInterval(function() {
                var t = document.querySelector('.stApp');
                if (t) {
                    clearInterval(wait);
                    obs.observe(t, {childList: true, subtree: true, attributes: true, attributeFilter: ['style']});
                }
            }, 500);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    """Sidebar render et — gruplu, ikonlu navigasyon."""
    _sidebar_css()
    auth_user = AuthManager.get_current_user()
    role = auth_user.get("role", "")
    name = auth_user.get("name", "Kullanici")
    initial = name[0].upper() if name else "K"

    with st.sidebar:
        # Logo
        st.markdown(
            """
            <div class="sb-logo">
                <div class="sb-logo-icon-box">
                    <span class="sb-logo-icon">🎓</span>
                </div>
                <div>
                    <div class="sb-logo-text">SmartCampus AI</div>
                    <div class="sb-logo-sub">Akademik Yönetim Platformu</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        # Kurum bilgisi
        tenant_name = st.session_state.get("tenant_name", "")
        tenant_label = tenant_name if tenant_name else ""
        if role == "SuperAdmin":
            tenant_label = "Tüm Kurumlar"

        # Kullanici karti
        _tenant_html = (
            f'<span style="font-size:.6rem;color:#94a3b8;font-weight:400;">'
            f'🏫 {tenant_label}</span>'
        ) if tenant_label else ""
        st.markdown(
            f"""
            <div class="sb-user-card">
                <div class="sb-avatar">{initial}</div>
                <div class="sb-user-info">
                    <span class="sb-user-name">{name}</span>
                    <span class="sb-user-role">{role}</span>
                    {_tenant_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Çıkış Yap", key="logout_btn", use_container_width=True):
            AuthManager.logout()
            st.rerun()

        st.divider()

        # Veli / Ogrenci — izinli_moduller'den dinamik navigasyon
        if role in ("Veli", "Ogrenci"):
            panel_adi = "Veli Paneli" if role == "Veli" else "Ogrenci Paneli"
            izinli = get_user_modules(auth_user.get("username", ""))
            # GUNCEL veli/ogrenci modul listesini her zaman varsayilandan al
            # (eski hesaplarda izinli_moduller bos olabilir veya eski liste olabilir)
            from utils.auth import get_role_default_modules
            varsayilan = get_role_default_modules(role)
            # Birlestir: izinli + varsayilan (varsayilanda olup izinlide olmayanlari ekle)
            if izinli:
                _set = set(izinli)
                for m in varsayilan:
                    if m not in _set:
                        izinli = list(izinli) + [m]
                        _set.add(m)
            else:
                izinli = list(varsayilan)
            # Panel her zaman ilk
            nav_items = [panel_adi]
            # Modül→Sidebar eşlemesi (ikon + Türkçe etiket)
            _modul_ikon = {
                "Dijital Kutuphane":            "📱 Dijital Kütüphane",
                "AI Bireysel Egitim":           "🎓 AI Bireysel Eğitim",
                "Yabanci Dil":                  "🌍 Yabancı Dil",
                "Kisisel Dil Gelisimi":         "🌟 Kişisel Dil Gelişimi",
                "AI Treni":                     "🚂 AI Treni",
                "STEAM Merkezi":                "🔬 STEAM Merkezi",
            }
            for mod in izinli:
                if mod == panel_adi:
                    continue  # Zaten eklendi
                display = _modul_ikon.get(mod, mod)
                nav_items.append(display)
            secim = st.radio("", nav_items, label_visibility="collapsed")
            # Display adından gerçek modül adına çevir
            _ikon_modul = {v: k for k, v in _modul_ikon.items()}
            return _ikon_modul.get(secim, secim)

        # Ogretmen — Dijital Kutuphane ek olarak sidebar'da gorunur
        if role == "Ogretmen":
            # Ogretmen icin Dijital Kutuphane sidebar'a eklenir (izinli_moduller'e bakilmaz)
            pass  # Asagida tum_moduller listesine zaten dahil

        # Yetkili modul listesini al (session cache)
        _um_key = f"_user_modules_{auth_user.get('username', '')}"
        if _um_key not in st.session_state:
            st.session_state[_um_key] = get_user_modules(auth_user.get("username", ""))
        izinli = st.session_state[_um_key]

        # Admin-only moduller
        extra_moduller = []
        if role == "SuperAdmin":
            extra_moduller.append(("Kurum Yonetimi", "🏢"))
        # Veli/Ogrenci panel onizleme kaldirildi — artik kendi sifreleriyle girilecek

        # Tum modul listesini olustur (radio icin)
        tum_moduller = []
        for grup in _MODUL_GRUPLARI:
            for ad, _ in grup["moduller"]:
                tum_moduller.append(ad)
        for ad, _ in extra_moduller:
            tum_moduller.append(ad)

        # Yetki filtresi
        if izinli:
            tum_moduller = [m for m in tum_moduller if m in izinli or m == "Ana Sayfa"]

        # Gosterim icin ikon ekle (radio label)
        _ikon_map: dict[str, str] = {}
        for grup in _MODUL_GRUPLARI:
            for ad, ikon in grup["moduller"]:
                _ikon_map[ad] = ikon
        for ad, ikon in extra_moduller:
            _ikon_map[ad] = ikon

        # Grup basliklarini ara sira ekleyerek radio ciz
        # Streamlit radio tek bir widget — grup etiketlerini markdown olarak veriyoruz
        page = None
        for grup in _MODUL_GRUPLARI:
            grup_listesi = [ad for ad, _ in grup["moduller"] if ad in tum_moduller]
            if not grup_listesi:
                continue
            st.markdown(f'<span class="sb-group-label">{grup["baslik"]}</span>', unsafe_allow_html=True)
            for ad in grup_listesi:
                ikon = _ikon_map.get(ad, "•")
                label = f"{ikon}  {ad}"
                aktif = st.session_state.get("_sidebar_secim") == ad
                if st.button(
                    label,
                    key=f"nav_{ad}",
                    use_container_width=True,
                    type="secondary" if not aktif else "primary",
                ):
                    st.session_state["_sidebar_secim"] = ad
                    page = ad

        # Admin extra moduller
        if extra_moduller:
            filtered_extra = [(ad, ikon) for ad, ikon in extra_moduller if ad in tum_moduller]
            if filtered_extra:
                st.markdown('<span class="sb-group-label">YÖNETİM</span>', unsafe_allow_html=True)
                for ad, ikon in filtered_extra:
                    label = f"{ikon}  {ad}"
                    if st.button(label, key=f"nav_{ad}", use_container_width=True, type="secondary"):
                        st.session_state["_sidebar_secim"] = ad
                        page = ad

        # Secili sayfa (buton basılmadıysa session'dan al)
        if page is None:
            page = st.session_state.get("_sidebar_secim", "Ana Sayfa")

        return page


# ── ANA UYGULAMA ─────────────────────────────────────────────────────────────

def _route(page: str):
    """Sayfa adına göre ilgili view fonksiyonunu çağır."""
    # Tüm modüller için profesyonel CSS enjekte et (ilk çağrıda import)
    if not st.session_state.get("_pro_css_done"):
        from utils.ui_common import inject_pro_css
        inject_pro_css()
        st.session_state["_pro_css_done"] = True
    if page == "Ana Sayfa":
        from views.ana_sayfa import render_ana_sayfa
        render_ana_sayfa()
    elif page == "Veli Paneli":
        from views.ogrenci_veli_panel import render_veli_panel
        render_veli_panel()
    elif page == "Ogrenci Paneli":
        from views.ogrenci_veli_panel import render_ogrenci_panel
        render_ogrenci_panel()
    elif page == "Yonetim Tek Ekran":
        from views.yonetim_ekran import render_yonetim_ekran
        render_yonetim_ekran()
    elif page == "Mezunlar ve Kariyer Yonetimi":
        from views.alumni_career import render_alumni_career
        render_alumni_career()
    elif page == "Kurumsal Organizasyon ve Iletisim":
        from views.kim_organizational import render_kim_organizational
        render_kim_organizational()
    elif page == "Kayit Modulu":
        from views.kayit_modulu import render_kayit_modulu
        render_kayit_modulu()
    elif page == "Veli Gunluk Kapsul":
        from views.veli_gunluk_kapsul import render_veli_gunluk_kapsul
        render_veli_gunluk_kapsul()
    elif page == "Sosyal Medya Yonetimi":
        from views.sosyal_medya import render_sosyal_medya
        render_sosyal_medya()
    # ── BİRLEŞİK MODÜLLER ──
    elif page == "Ogrenci Zeka Merkezi":
        from views.ogrenci_zeka_merkezi import render_ogrenci_zeka_merkezi
        render_ogrenci_zeka_merkezi()
    elif page == "AI Ogrenme Platformu":
        from views.ai_ogrenme_platformu import render_ai_ogrenme_platformu
        auth_user = st.session_state.get("auth_user", {})
        user_role = auth_user.get("role", "")
        readonly = user_role not in ("Yonetici",)
        render_ai_ogrenme_platformu(readonly=readonly)
    elif page == "Tesis ve Varlik Yonetimi":
        from views.tesis_varlik_yonetimi import render_tesis_varlik_yonetimi
        render_tesis_varlik_yonetimi()
    # ── TAŞINAN MODÜLLER (geriye uyumluluk) ──
    elif page in ("Ogrenci 360", "Erken Uyari Sistemi"):
        from views.ogrenci_zeka_merkezi import render_ogrenci_zeka_merkezi
        render_ogrenci_zeka_merkezi()
    elif page in ("Dijital Kutuphane", "AI Bireysel Egitim"):
        from views.ai_ogrenme_platformu import render_ai_ogrenme_platformu
        render_ai_ogrenme_platformu()
    elif page in ("Tuketim ve Demirbas", "Destek Hizmetleri Takip"):
        from views.tesis_varlik_yonetimi import render_tesis_varlik_yonetimi
        render_tesis_varlik_yonetimi()
    elif page == "Veli Gunluk Kapsul":
        from views.veli_gunluk_kapsul import render_veli_gunluk_kapsul
        render_veli_gunluk_kapsul()
    elif page == "Akademik Takvim":
        from views.academic_calendar import render_academic_calendar
        render_academic_calendar()
    elif page == "Gunluk Isler":
        from views.gunluk_isler import render_gunluk_isler
        render_gunluk_isler()
    # ── BAĞIMSIZ MODÜLLER ──
    elif page == "Okul Oncesi - Ilkokul":
        from views.okul_oncesi_ilkokul import render_okul_oncesi_ilkokul
        render_okul_oncesi_ilkokul()
    elif page == "Akademik Takip":
        from views.akademik_takip import render_akademik_takip
        render_akademik_takip()
    elif page == "Olcme ve Degerlendirme":
        from views.olcme_degerlendirme_v2 import render_olcme_degerlendirme_v2
        render_olcme_degerlendirme_v2()
    elif page == "Rehberlik":
        from views.rehberlik import render_rehberlik
        render_rehberlik()
    elif page == "Insan Kaynaklari Yonetimi":
        from views.insan_kaynaklari import render_insan_kaynaklari
        render_insan_kaynaklari()
    elif page == "Okul Sagligi Takip":
        from views.okul_sagligi import render_okul_sagligi
        render_okul_sagligi()
    elif page == "Randevu ve Ziyaretci":
        from views.randevu_ziyaretci import render_randevu_ziyaretci
        render_randevu_ziyaretci()
    elif page == "Sivil Savunma ve IS Guvenligi":
        from views.sivil_savunma_isg import render_sivil_savunma_isg
        render_sivil_savunma_isg()
    elif page == "Toplanti ve Kurullar":
        from views.toplanti_kurullar import render_toplanti_kurullar
        render_toplanti_kurullar()
    elif page == "Sosyal Etkinlik ve Kulupler":
        from views.sosyal_etkinlik import render_sosyal_etkinlik
        render_sosyal_etkinlik()
    elif page == "Butce Gelir Gider":
        from views.butce_gelir_gider import render_butce_gelir_gider
        render_butce_gelir_gider()
    elif page == "Odeme Takip":
        from views.odeme_takip import render_odeme_takip
        render_odeme_takip()
    elif page == "Veli-Ogretmen Gorusme":
        from views.veli_ogretmen_gorusme import render_veli_ogretmen_gorusme
        render_veli_ogretmen_gorusme()
    elif page == "Analitik Dashboard":
        from views.analitik_dashboard import render_analitik_dashboard
        render_analitik_dashboard()
    elif page == "Sertifika Uretici":
        from views.sertifika_uretici import render_sertifika_uretici
        render_sertifika_uretici()
    elif page == "Servis GPS Takip":
        from views.servis_gps_takip import render_servis_gps_takip
        render_servis_gps_takip()
    elif page == "Kutuphane Barkod":
        from views.kutuphane_barkod import render_kutuphane_barkod
        render_kutuphane_barkod()
    elif page == "Yemek Tercihi ve Alerji":
        from views.yemek_tercihi import render_yemek_tercihi
        render_yemek_tercihi()
    elif page == "Kutuphane":
        from views.kutuphane import render_kutuphane
        render_kutuphane()
    elif page == "Yabanci Dil":
        from views.yabanci_dil import render_yabanci_dil
        render_yabanci_dil()
    elif page == "Kisisel Dil Gelisimi":
        from views.kisisel_dil_gelisimi import render_kisisel_dil_gelisimi
        render_kisisel_dil_gelisimi()
    elif page == "Egitim Koclugu":
        from views.egitim_koclugu import render_egitim_koclugu
        render_egitim_koclugu()
    elif page == "AI Treni":
        from views.bilgi_treni import render_bilgi_treni
        render_bilgi_treni()
    elif page == "STEAM Merkezi":
        from views.stem_merkezi import render_stem_merkezi
        render_stem_merkezi()
    elif page == "Kurum Hizmetleri":
        from views.kurum_hizmetleri import render_kurum_hizmetleri
        render_kurum_hizmetleri()
    elif page == "AI Destek":
        from views.ai_destek import render_ai_destek
        render_ai_destek()
    elif page == "Kurum Yonetimi":
        from views.kurum_yonetimi import render_kurum_yonetimi
        render_kurum_yonetimi()
    else:
        from views.ana_sayfa import render_ana_sayfa
        render_ana_sayfa()


def main():
    # QR kod handler — URL parametresi varsa direkt yonlendir
    _qr_params = st.query_params
    if _qr_params.get("sinif") and _qr_params.get("ders"):
        from views.qr_handler import render_qr_handler
        render_qr_handler()
        return

    page = render_sidebar()

    # Komut Paleti — global Cmd+K arama
    try:
        from utils.command_palette import render_command_palette
        render_command_palette(modul_gruplari=_MODUL_GRUPLARI)
    except Exception:
        pass

    # Live Activity Stream — sag altta canli akis
    try:
        from utils.live_activity import render_live_activity
        # Sadece yonetici/admin rollerinde goster
        _user = st.session_state.get("auth_user", {})
        _role = _user.get("role", "")
        if _role in ("admin", "yonetici", "mudur", "mudur_yardimcisi"):
            render_live_activity(visible=True, limit=8)
    except Exception:
        pass

    # Akilli Bildirim Zili — AI verileri analiz edip bildirim verir
    try:
        from utils.smart_bell import render_smart_bell
        _user = st.session_state.get("auth_user", {})
        _role = _user.get("role", "")
        if _role in ("admin", "yonetici", "mudur", "mudur_yardimcisi", "ogretmen"):
            render_smart_bell()
    except Exception:
        pass

    # Komut paleti'nden modul secimi
    if "secili_modul" in st.session_state:
        hedef = st.session_state.pop("secili_modul")
        st.session_state["_sidebar_secim"] = hedef
        page = hedef

    # Ana sayfadan modül kartına tıklanınca yönlendirme
    if "_ana_sayfa_git" in st.session_state:
        hedef = st.session_state.pop("_ana_sayfa_git")
        st.session_state["_sidebar_secim"] = hedef
        page = hedef

    # Sayfa değiştiğinde eski modüle ait geçici state'leri temizle
    _prev_page = st.session_state.get("_active_page", "")
    if page != _prev_page:
        st.session_state["_active_page"] = page
        # e-Kitaplık okuyucu state temizle
        st.session_state.pop("ek_reader_html", None)
        st.session_state.pop("ek_reader_title", None)
        # Geçici modül state'leri — tek geçişte temizle
        _drop_prefixes = ("_prem_", "_kzp_", "_oy_", "_ai_", "ydai_", "ydb_", "masal_mp3_")
        _drop_contains = ("_ai_mode", "_scene_html", "_tts")
        _keys_to_drop = [
            k for k in st.session_state
            if k.startswith(_drop_prefixes) or any(c in k for c in _drop_contains)
        ]
        for k in _keys_to_drop:
            del st.session_state[k]

    _route(page)


if __name__ == "__main__":
    main()