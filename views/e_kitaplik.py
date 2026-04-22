# -*- coding: utf-8 -*-
"""e-Kitaplık — EPUB & PDF Online Okuyucu (Premium Diamond)."""
import os
import json
import base64
import hashlib
import streamlit as st

_KITAPLAR_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "kutuphane", "kitaplar")
_KATALOG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "kutuphane", "katalog.json")
_SUPPORTED = (".epub", ".pdf")


# ─────────────────── Katalog Yönetimi ───────────────────

def _scan_books() -> list:
    """Kitaplar klasörünü tara, katalog.json oluştur/güncelle."""
    if not os.path.isdir(_KITAPLAR_DIR):
        os.makedirs(_KITAPLAR_DIR, exist_ok=True)
        return []

    existing = _load_katalog()
    existing_map = {b["dosya"]: b for b in existing}

    books = []
    for root, _, files in os.walk(_KITAPLAR_DIR):
        for fn in sorted(files):
            if not fn.lower().endswith(_SUPPORTED):
                continue
            rel = os.path.relpath(os.path.join(root, fn), _KITAPLAR_DIR).replace("\\", "/")
            if rel in existing_map:
                books.append(existing_map[rel])
            else:
                name_no_ext = os.path.splitext(fn)[0]
                ext = os.path.splitext(fn)[1].lower().lstrip(".")
                size_mb = round(os.path.getsize(os.path.join(root, fn)) / (1024 * 1024), 2)
                bid = "k_" + hashlib.md5(rel.encode()).hexdigest()[:8]
                meta = _extract_metadata(os.path.join(root, fn), ext)
                books.append({
                    "id": bid,
                    "baslik": meta.get("title", name_no_ext.replace("_", " ").replace("-", " ").title()),
                    "yazar": meta.get("author", "Bilinmiyor"),
                    "format": ext,
                    "dosya": rel,
                    "kademe": "genel",
                    "tur": "kitap",
                    "etiketler": [],
                    "boyut_mb": size_mb,
                    "kapak": meta.get("cover_b64", ""),
                })

    _save_katalog(books)
    return books


def _extract_metadata(filepath: str, fmt: str) -> dict:
    """EPUB/PDF'den temel metadata çıkar."""
    meta = {}
    if fmt == "epub":
        try:
            import zipfile
            from xml.etree import ElementTree as ET
            with zipfile.ZipFile(filepath, "r") as zf:
                # Find OPF file
                container = zf.read("META-INF/container.xml")
                tree = ET.fromstring(container)
                ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
                rootfile = tree.find(".//c:rootfile", ns)
                if rootfile is not None:
                    opf_path = rootfile.get("full-path", "")
                    opf_data = zf.read(opf_path)
                    opf_tree = ET.fromstring(opf_data)
                    dc = "http://purl.org/dc/elements/1.1/"
                    title_el = opf_tree.find(f".//{{{dc}}}title")
                    if title_el is not None and title_el.text:
                        meta["title"] = title_el.text.strip()
                    creator_el = opf_tree.find(f".//{{{dc}}}creator")
                    if creator_el is not None and creator_el.text:
                        meta["author"] = creator_el.text.strip()
                    # Cover image
                    opf_ns = {"opf": "http://www.idpf.org/2007/opf"}
                    for item in opf_tree.findall(".//{http://www.idpf.org/2007/opf}item"):
                        item_id = item.get("id", "").lower()
                        href = item.get("href", "")
                        media = item.get("media-type", "")
                        if ("cover" in item_id) and media.startswith("image/"):
                            opf_dir = os.path.dirname(opf_path)
                            cover_path = (opf_dir + "/" + href).lstrip("/")
                            try:
                                cover_data = zf.read(cover_path)
                                if len(cover_data) < 500_000:
                                    meta["cover_b64"] = base64.b64encode(cover_data).decode()
                            except KeyError:
                                pass
                            break
        except Exception:
            pass
    elif fmt == "pdf":
        try:
            import fitz
            doc = fitz.open(filepath)
            md = doc.metadata or {}
            if md.get("title"):
                meta["title"] = md["title"]
            if md.get("author"):
                meta["author"] = md["author"]
            # First page as cover thumbnail
            if doc.page_count > 0:
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(0.8, 0.8))
                meta["cover_b64"] = base64.b64encode(pix.tobytes("jpeg")).decode()
            doc.close()
        except Exception:
            pass
    return meta


# ─────────────────── Metin Çıkarma ───────────────────

def _extract_text_epub(filepath: str) -> list:
    """EPUB'dan bölüm bölüm metin çıkar. [{title, text}, ...]"""
    import zipfile
    from xml.etree import ElementTree as ET
    import re

    chapters = []
    try:
        with zipfile.ZipFile(filepath, "r") as zf:
            container = zf.read("META-INF/container.xml")
            tree = ET.fromstring(container)
            ns_c = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
            rootfile = tree.find(".//c:rootfile", ns_c)
            if rootfile is None:
                return chapters
            opf_path = rootfile.get("full-path", "")
            opf_dir = "/".join(opf_path.split("/")[:-1])
            opf_data = zf.read(opf_path)
            opf_tree = ET.fromstring(opf_data)

            ns_opf = "http://www.idpf.org/2007/opf"
            # Build item map
            items = {}
            for item in opf_tree.findall(f".//{{{ns_opf}}}item"):
                items[item.get("id", "")] = item

            # Get spine order
            spine = opf_tree.find(f".//{{{ns_opf}}}spine")
            if spine is None:
                return chapters
            for itemref in spine.findall(f"{{{ns_opf}}}itemref"):
                idref = itemref.get("idref", "")
                item = items.get(idref)
                if item is None:
                    continue
                href = item.get("href", "")
                media = item.get("media-type", "")
                if "html" not in media and "xml" not in media:
                    continue
                full_path = (opf_dir + "/" + href).lstrip("/") if opf_dir else href
                try:
                    html_data = zf.read(full_path).decode("utf-8", errors="ignore")
                except KeyError:
                    continue
                # Strip tags, get text
                text = re.sub(r'<[^>]+>', ' ', html_data)
                text = re.sub(r'\s+', ' ', text).strip()
                # Try to find title from h1/h2/h3
                title_match = re.search(r'<h[1-3][^>]*>(.*?)</h[1-3]>', html_data, re.I | re.S)
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else f"Bölüm {len(chapters)+1}"
                if len(text) > 50:  # Skip near-empty chapters
                    chapters.append({"title": title, "text": text})
    except Exception:
        pass
    return chapters


def _extract_text_pdf(filepath: str) -> list:
    """PDF'den sayfa sayfa metin çıkar. [{title, text}, ...]"""
    pages = []
    try:
        import fitz
        doc = fitz.open(filepath)
        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text("text").strip()
            if len(text) > 20:
                pages.append({"title": f"Sayfa {i+1}", "text": text})
        doc.close()
    except Exception:
        pass
    return pages


def _extract_book_text(filepath: str, fmt: str) -> list:
    """Kitaptan bölüm/sayfa bazlı metin çıkar."""
    if fmt == "epub":
        return _extract_text_epub(filepath)
    elif fmt == "pdf":
        return _extract_text_pdf(filepath)
    return []


# ─────────────────── Edge-TTS + Timestamp ───────────────────

def _generate_tts_with_timestamps(text: str, lang: str = "tr") -> tuple:
    """Edge-TTS ile ses üret + kelime timestamp'leri döndür. Returns (audio_bytes, word_boundaries)."""
    import asyncio

    voice = "tr-TR-EmelNeural" if lang == "tr" else "en-US-JennyNeural"

    async def _gen():
        import edge_tts
        communicate = edge_tts.Communicate(text, voice, rate="-5%", pitch="+2Hz")
        audio_chunks = []
        word_boundaries = []

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                word_boundaries.append({
                    "offset": chunk["offset"] / 10_000_000,
                    "duration": chunk["duration"] / 10_000_000,
                    "text": chunk["text"],
                })

        return b"".join(audio_chunks), word_boundaries

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                result = pool.submit(lambda: asyncio.run(_gen())).result(timeout=180)
        else:
            result = loop.run_until_complete(_gen())
    except RuntimeError:
        result = asyncio.run(_gen())

    return result


def _build_sentence_timestamps(text: str, word_boundaries: list) -> list:
    """Kelime timestamp'lerinden cümle timestamp'leri oluştur."""
    import re
    sentences = re.split(r'(?<=[.!?…])\s+', text.strip())
    sentences = [s for s in sentences if s.strip()]

    if not word_boundaries:
        return [{"text": s, "start": i * 3.0, "end": (i + 1) * 3.0} for i, s in enumerate(sentences)]

    result = []
    wb_idx = 0
    for sent in sentences:
        word_count = len(sent.split())
        start = word_boundaries[wb_idx]["offset"] if wb_idx < len(word_boundaries) else 0
        end_idx = min(wb_idx + word_count - 1, len(word_boundaries) - 1)
        end = word_boundaries[end_idx]["offset"] + word_boundaries[end_idx]["duration"] if end_idx >= 0 else start + 2
        result.append({"text": sent, "start": round(start, 3), "end": round(end, 3)})
        wb_idx += word_count

    return result


# ─────────────────── Sesli Okuyucu HTML ───────────────────

def _audio_reader_html(sentences_data: list, audio_b64: str, title: str) -> str:
    """Premium sesli okuyucu — spotlight cümle takibi."""
    import json as _json
    sentences_js = _json.dumps(sentences_data, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<style>
/* font: sistem fontu kullaniliyor */
    * {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Inter',sans-serif; background:#faf8f5; min-height:100vh; }}

.ar-top {{ display:flex; align-items:center; justify-content:space-between;
  padding:12px 24px; background:linear-gradient(135deg,#94A3B8,#334155);
  color:#fff; border-bottom:3px solid #8b5cf6; position:sticky; top:0; z-index:100; }}
.ar-top h3 {{ font-size:.9rem; font-weight:700; max-width:40%; overflow:hidden;
  text-overflow:ellipsis; white-space:nowrap; }}
.ar-controls {{ display:flex; gap:8px; align-items:center; }}
.ar-btn {{ background:rgba(255,255,255,.1); border:1.5px solid rgba(255,255,255,.2);
  color:#fff; padding:8px 16px; border-radius:10px; cursor:pointer; font-size:.8rem;
  font-weight:700; transition:all .25s; font-family:inherit; }}
.ar-btn:hover {{ background:rgba(139,92,246,.5); border-color:rgba(139,92,246,.6);
  transform:translateY(-1px); }}
.ar-btn.active {{ background:linear-gradient(135deg,#8b5cf6,#6366f1);
  border-color:transparent; box-shadow:0 4px 15px rgba(139,92,246,.4); }}
.ar-speed {{ background:rgba(255,255,255,.08); color:#fff; border:1px solid rgba(255,255,255,.2);
  padding:6px 10px; border-radius:8px; font-size:.75rem; font-family:inherit; }}

.ar-progress {{ width:100%; height:6px; background:rgba(0,0,0,.08); cursor:pointer;
  position:relative; }}
.ar-progress-fill {{ height:100%; background:linear-gradient(90deg,#8b5cf6,#6366f1,#ec4899);
  border-radius:3px; transition:width .1s; width:0%; }}

.ar-body {{ max-width:780px; margin:0 auto; padding:32px 24px 80px; }}
.ar-sentence {{ font-family:'Merriweather',Georgia,serif; font-size:1.15rem; line-height:2.1;
  color:#64748b; padding:6px 12px; border-radius:8px; margin-bottom:2px;
  transition:all .4s cubic-bezier(.4,0,.2,1); display:inline; }}
.ar-sentence.active {{ color:#94A3B8; font-weight:600;
  background:linear-gradient(135deg,rgba(139,92,246,.08),rgba(99,102,241,.06));
  box-shadow:0 0 0 3px rgba(139,92,246,.1); border-radius:8px; }}
.ar-sentence.done {{ color:#94a3b8; }}

.ar-time {{ position:fixed; bottom:0; left:0; right:0; background:linear-gradient(135deg,#94A3B8,#334155);
  padding:10px 24px; display:flex; align-items:center; justify-content:space-between;
  color:#fff; font-size:.78rem; z-index:100; border-top:2px solid rgba(139,92,246,.3); }}
.ar-time .current {{ color:#a78bfa; font-weight:700; }}
.ar-time .total {{ color:#94a3b8; }}

body.dark {{ background:#0B0F19; }}
body.dark .ar-sentence {{ color:#475569; }}
body.dark .ar-sentence.active {{ color:#e2e8f0;
  background:linear-gradient(135deg,rgba(139,92,246,.15),rgba(99,102,241,.1)); }}
body.dark .ar-sentence.done {{ color:#334155; }}
</style>
</head>
<body>
<div class="ar-top">
  <h3>🔊 {title}</h3>
  <div class="ar-controls">
    <button class="ar-btn" id="btnPlay" onclick="togglePlay()">▶ Başlat</button>
    <button class="ar-btn" onclick="skipSentence(-1)">⏮</button>
    <button class="ar-btn" onclick="skipSentence(1)">⏭</button>
    <select class="ar-speed" onchange="setSpeed(this.value)">
      <option value="0.7">0.7x</option>
      <option value="0.85">0.85x</option>
      <option value="1" selected>1x</option>
      <option value="1.15">1.15x</option>
      <option value="1.3">1.3x</option>
    </select>
    <button class="ar-btn" onclick="toggleDark()">🌙</button>
  </div>
</div>
<div class="ar-progress" onclick="seekAudio(event)">
  <div class="ar-progress-fill" id="progFill"></div>
</div>
<audio id="aud" preload="auto">
  <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
</audio>
<div class="ar-body" id="textBody"></div>
<div class="ar-time">
  <span class="current" id="timeCur">0:00</span>
  <span id="sentInfo">Hazır</span>
  <span class="total" id="timeTotal">0:00</span>
</div>

<script>
var SENTS = {sentences_js};
var aud = document.getElementById("aud");
var curIdx = -1;
var isPlaying = false;

// Render sentences
(function() {{
  var body = document.getElementById("textBody");
  var html = "";
  SENTS.forEach(function(s, i) {{
    html += '<span class="ar-sentence" id="s'+i+'" data-idx="'+i+'" onclick="jumpTo('+i+')">'+s.text+' </span>';
  }});
  body.innerHTML = html;
}})();

function fmtTime(sec) {{
  var m = Math.floor(sec/60), s = Math.floor(sec%60);
  return m + ":" + (s<10?"0":"") + s;
}}

aud.addEventListener("loadedmetadata", function() {{
  document.getElementById("timeTotal").textContent = fmtTime(aud.duration);
}});

aud.addEventListener("timeupdate", function() {{
  var t = aud.currentTime;
  document.getElementById("timeCur").textContent = fmtTime(t);
  document.getElementById("progFill").style.width = (t/aud.duration*100)+"%";

  // Find active sentence
  var newIdx = -1;
  for (var i = 0; i < SENTS.length; i++) {{
    if (t >= SENTS[i].start && t < SENTS[i].end + 0.3) {{
      newIdx = i;
    }}
  }}

  if (newIdx !== curIdx) {{
    // Remove old highlights
    document.querySelectorAll(".ar-sentence").forEach(function(el, i) {{
      el.classList.remove("active");
      if (i < newIdx) el.classList.add("done");
      else el.classList.remove("done");
    }});
    // Highlight current
    if (newIdx >= 0) {{
      var el = document.getElementById("s" + newIdx);
      if (el) {{
        el.classList.add("active");
        el.scrollIntoView({{ behavior:"smooth", block:"center" }});
      }}
      document.getElementById("sentInfo").textContent = (newIdx+1) + " / " + SENTS.length + " cümle";
    }}
    curIdx = newIdx;
  }}
}});

aud.addEventListener("ended", function() {{
  isPlaying = false;
  document.getElementById("btnPlay").textContent = "▶ Başlat";
  document.getElementById("btnPlay").classList.remove("active");
  // Mark all done
  document.querySelectorAll(".ar-sentence").forEach(function(el) {{
    el.classList.remove("active");
    el.classList.add("done");
  }});
  document.getElementById("sentInfo").textContent = "✓ Tamamlandı";
}});

function togglePlay() {{
  if (isPlaying) {{
    aud.pause();
    isPlaying = false;
    document.getElementById("btnPlay").textContent = "▶ Devam";
    document.getElementById("btnPlay").classList.remove("active");
  }} else {{
    aud.play();
    isPlaying = true;
    document.getElementById("btnPlay").textContent = "⏸ Duraklat";
    document.getElementById("btnPlay").classList.add("active");
  }}
}}

function setSpeed(val) {{
  aud.playbackRate = parseFloat(val);
}}

function seekAudio(e) {{
  var rect = e.currentTarget.getBoundingClientRect();
  var pct = (e.clientX - rect.left) / rect.width;
  aud.currentTime = pct * aud.duration;
}}

function jumpTo(idx) {{
  if (idx >= 0 && idx < SENTS.length) {{
    aud.currentTime = SENTS[idx].start;
    if (!isPlaying) togglePlay();
  }}
}}

function skipSentence(dir) {{
  var next = Math.max(0, Math.min(SENTS.length - 1, curIdx + dir));
  jumpTo(next);
}}

function toggleDark() {{
  document.body.classList.toggle("dark", key="e_kitaplik_m1");
}}
</script>
</body></html>'''


def _load_katalog() -> list:
    try:
        with open(_KATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_katalog(books: list):
    os.makedirs(os.path.dirname(_KATALOG_PATH), exist_ok=True)
    with open(_KATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


# ─────────────────── EPUB Okuyucu ───────────────────

def _epub_reader_html(b64_data: str, title: str) -> str:
    """epub.js tabanlı premium EPUB okuyucu HTML'i."""
    return f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/epubjs@0.3.93/dist/epub.min.js"></script>
<style>
/* font: sistem fontu kullaniliyor */
    * {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Inter',sans-serif; background:#111827; overflow:hidden; height:100vh; }}
.reader-top {{ display:flex; align-items:center; justify-content:space-between;
  padding:10px 20px; background:linear-gradient(135deg,#94A3B8,#334155);
  color:#fff; border-bottom:3px solid #6366f1; }}
.reader-top h3 {{ font-size:.92rem; font-weight:700; white-space:nowrap;
  overflow:hidden; text-overflow:ellipsis; max-width:50%; }}
.reader-controls {{ display:flex; gap:6px; align-items:center; }}
.reader-controls button {{ background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.2);
  color:#fff; padding:6px 12px; border-radius:8px; cursor:pointer; font-size:.78rem;
  font-weight:600; transition:all .2s; }}
.reader-controls button:hover {{ background:rgba(99,102,241,.5); }}
.reader-controls select {{ background:#94A3B8; color:#fff; border:1px solid rgba(255,255,255,.2);
  padding:5px 8px; border-radius:6px; font-size:.75rem; }}
#viewer {{ width:100%; height:calc(100vh - 100px); overflow:hidden; position:relative; }}
.epub-view {{ height:100%; }}
.nav-bar {{ display:flex; justify-content:space-between; align-items:center;
  padding:6px 20px; background:#fff; border-top:1px solid #e2e8f0; }}
.nav-bar button {{ background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff;
  border:none; padding:8px 20px; border-radius:8px; cursor:pointer; font-weight:700;
  font-size:.82rem; transition:all .2s; }}
.nav-bar button:hover {{ transform:translateY(-1px); box-shadow:0 4px 12px rgba(99,102,241,.3); }}
.nav-bar .loc {{ font-size:.75rem; color:#64748b; }}
#toc-panel {{ position:absolute; top:0; left:0; width:280px; height:calc(100vh - 100px);
  background:#fff; box-shadow:4px 0 20px rgba(0,0,0,.15); z-index:100;
  transform:translateX(-300px); transition:transform .3s; overflow-y:auto;
  border-right:3px solid #6366f1; }}
#toc-panel.open {{ transform:translateX(0); }}
#toc-panel h4 {{ padding:16px 18px; font-size:.9rem; border-bottom:1px solid #e2e8f0;
  background:linear-gradient(135deg,#111827,#1A2035); color:#94A3B8; position:sticky;
  top:0; z-index:1; }}
#toc-panel ul {{ list-style:none; padding:8px 0; }}
#toc-panel li {{ padding:10px 18px; font-size:.8rem; color:#475569; cursor:pointer;
  border-bottom:1px solid #1A2035; transition:all .15s; }}
#toc-panel li:hover {{ background:rgba(99,102,241,.06); color:#6366f1; padding-left:22px; }}
body.dark {{ background:#0B0F19; }}
body.dark #viewer {{ background:#0B0F19; }}
body.dark .nav-bar {{ background:#94A3B8; border-color:#334155; }}
body.dark .nav-bar .loc {{ color:#94a3b8; }}
body.dark #toc-panel {{ background:#94A3B8; }}
body.dark #toc-panel h4 {{ background:#0B0F19; color:#e2e8f0; border-color:#334155; }}
body.dark #toc-panel li {{ color:#94a3b8; border-color:#334155; }}
body.dark #toc-panel li:hover {{ background:rgba(99,102,241,.15); color:#818cf8; }}
</style>
</head>
<body>
<div class="reader-top">
  <h3 id="bookTitle">{title}</h3>
  <div class="reader-controls">
    <button onclick="toggleToc()">☰ İçindekiler</button>
    <button onclick="changeFontSize(-1)">A-</button>
    <button onclick="changeFontSize(1)">A+</button>
    <select id="fontSelect" onchange="changeFont(this.value)">
      <option value="Merriweather">Serif</option>
      <option value="Inter">Sans-serif</option>
      <option value="Georgia">Georgia</option>
      <option value="monospace">Monospace</option>
    </select>
    <button onclick="toggleDark()">🌙</button>
  </div>
</div>
<div id="toc-panel"><h4>📑 İçindekiler</h4><ul id="toc-list"></ul></div>
<div id="viewer"></div>
<div class="nav-bar">
  <button onclick="rendition.prev()">◀ Önceki</button>
  <span class="loc" id="locInfo">Yükleniyor...</span>
  <button onclick="rendition.next()">Sonraki ▶</button>
</div>
<script>
var fontSize = 100;
var isDark = false;
var book, rendition;

(function() {{
  var raw = atob("{b64_data}");
  var arr = new Uint8Array(raw.length);
  for (var i = 0; i < raw.length; i++) arr[i] = raw.charCodeAt(i);

  book = ePub(arr.buffer);
  rendition = book.renderTo("viewer", {{
    width: "100%",
    height: "100%",
    spread: "none",
    flow: "paginated"
  }});

  rendition.themes.default({{
    body: {{ "font-family": "'Merriweather', Georgia, serif", "line-height": "1.8", "padding": "20px 40px !important" }},
    p: {{ "font-size": fontSize + "% !important", "margin-bottom": "0.8em !important" }},
    "h1,h2,h3": {{ "color": "#94A3B8 !important" }}
  }});

  rendition.display();

  book.loaded.navigation.then(function(nav) {{
    var ul = document.getElementById("toc-list");
    nav.toc.forEach(function(ch) {{
      var li = document.createElement("li");
      li.textContent = ch.label.trim();
      li.onclick = function() {{
        rendition.display(ch.href);
        document.getElementById("toc-panel").classList.remove("open");
      }};
      ul.appendChild(li);
    }});
  }});

  rendition.on("relocated", function(loc) {{
    var start = loc.start;
    var pct = Math.round((start.percentage || 0) * 100);
    document.getElementById("locInfo").textContent = "%" + pct + " okundu";
  }});

  // Keyboard nav
  document.addEventListener("keyup", function(e) {{
    if (e.key === "ArrowLeft") rendition.prev();
    if (e.key === "ArrowRight") rendition.next();
  }});
}})();

function toggleToc() {{
  document.getElementById("toc-panel").classList.toggle("open", key="e_kitaplik_m2");
}}

function changeFontSize(delta) {{
  fontSize = Math.max(60, Math.min(200, fontSize + delta * 10));
  rendition.themes.default({{
    p: {{ "font-size": fontSize + "% !important" }}
  }});
  rendition.views().forEach(function(v) {{ v.pane && v.pane.render(); }});
  if (rendition.manager) rendition.manager.clear();
  rendition.display(rendition.location ? rendition.location.start.cfi : undefined);
}}

function changeFont(font) {{
  rendition.themes.default({{
    body: {{ "font-family": "'" + font + "', serif" }}
  }});
  if (rendition.manager) rendition.manager.clear();
  rendition.display(rendition.location ? rendition.location.start.cfi : undefined);
}}

function toggleDark() {{
  isDark = !isDark;
  document.body.classList.toggle("dark", isDark, key="e_kitaplik_m3");
  rendition.themes.default({{
    body: {{ "background": isDark ? "#0B0F19 !important" : "#fff !important",
             "color": isDark ? "#e2e8f0 !important" : "#94A3B8 !important" }},
    "p,span,div": {{ "color": isDark ? "#cbd5e1 !important" : "#94A3B8 !important" }},
    "h1,h2,h3,h4": {{ "color": isDark ? "#1A2035 !important" : "#94A3B8 !important" }}
  }});
  if (rendition.manager) rendition.manager.clear();
  rendition.display(rendition.location ? rendition.location.start.cfi : undefined);
}}
</script>
</body></html>'''


# ─────────────────── PDF Okuyucu ───────────────────

def _pdf_reader_html(b64_data: str, title: str) -> str:
    """Flipbook tarzı premium PDF okuyucu – PDF.js + pure CSS 3D transforms ile sayfa çevirme."""
    return f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{
  background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
  display:flex;flex-direction:column;align-items:center;
  height:100vh;overflow:hidden;
  font-family:system-ui,-apple-system,sans-serif;
  margin:0;
}}

/* ── Toolbar ── */
.toolbar{{
  background:linear-gradient(135deg,#0a0e27,#1a1a2e);
  padding:8px 20px;display:flex;justify-content:space-between;
  align-items:center;border-bottom:2px solid #c9a84c;flex-shrink:0;
  z-index:100;
}}
.toolbar h3{{color:#c9a84c;font-size:14px;margin:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:30%;}}
.toolbar button{{
  background:rgba(201,168,76,0.15);border:1px solid rgba(201,168,76,0.4);
  color:#c9a84c;padding:6px 14px;border-radius:8px;
  cursor:pointer;font-size:12px;font-weight:600;transition:all 0.2s;
}}
.toolbar button:hover{{background:rgba(201,168,76,0.3);}}
.page-info{{color:#94a3b8;font-size:12px;min-width:100px;text-align:center;}}

/* ── Book container ── */
.book-container{{
  flex:1;display:flex;align-items:center;justify-content:center;
  perspective:2000px;padding:20px;position:relative;
}}

.book{{
  display:flex;position:relative;
  box-shadow:0 10px 60px rgba(0,0,0,0.5),0 0 100px rgba(0,0,0,0.2);
  border-radius:4px;
}}

/* Book spine shadow */
.book::after{{
  content:'';position:absolute;
  top:5%;bottom:5%;left:50%;
  width:6px;margin-left:-3px;
  background:linear-gradient(90deg,rgba(0,0,0,0.3),transparent,rgba(0,0,0,0.3));
  z-index:10;pointer-events:none;
}}

.page-slot{{
  background:#faf8f5;
  overflow:hidden;
  position:relative;
  transition:opacity 0.3s ease;
}}
.page-slot img{{
  width:100%;height:100%;object-fit:contain;
  display:block;
}}
.page-slot.left{{border-radius:4px 0 0 4px;}}
.page-slot.right{{border-radius:0 4px 4px 0;}}

/* Page transition animation */
.page-slot.flipping{{
  animation:pageFlip 0.4s ease;
}}
@keyframes pageFlip{{
  0%{{opacity:1;transform:rotateY(0);}}
  50%{{opacity:0.5;transform:rotateY(-15deg);}}
  100%{{opacity:1;transform:rotateY(0);}}
}}

/* ── Side navigation arrows ── */
.nav-arrow{{
  position:absolute;top:50%;transform:translateY(-50%);
  width:44px;height:44px;border-radius:50%;
  background:rgba(201,168,76,0.2);border:1px solid rgba(201,168,76,0.4);
  color:#c9a84c;font-size:20px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:all 0.2s;z-index:20;
}}
.nav-arrow:hover{{background:rgba(201,168,76,0.4);transform:translateY(-50%) scale(1.1);}}
.nav-arrow.left{{left:10px;}}
.nav-arrow.right{{right:10px;}}

/* ── Page number overlay ── */
.page-num{{
  position:absolute;bottom:8px;font-size:10px;
  color:#94a3b8;z-index:5;
}}
.page-num.l{{left:12px;}}
.page-num.r{{right:12px;}}

/* ── Loading ── */
.loading{{
  position:fixed;inset:0;background:rgba(10,14,39,0.97);
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;z-index:1000;color:#c9a84c;
}}
.spinner{{
  width:50px;height:50px;border:4px solid rgba(201,168,76,0.2);
  border-top-color:#c9a84c;border-radius:50%;
  animation:spin 1s linear infinite;
}}
@keyframes spin{{to{{transform:rotate(360deg);}}}}
.progress-bar{{
  width:200px;height:4px;background:rgba(201,168,76,0.2);
  border-radius:2px;margin-top:16px;overflow:hidden;
}}
.progress-fill{{
  height:100%;background:#c9a84c;border-radius:2px;
  transition:width 0.2s;
}}

/* ── Goto input ── */
.goto-input{{
  width:50px;padding:4px;border-radius:6px;
  border:1px solid rgba(201,168,76,0.4);
  background:rgba(201,168,76,0.1);color:#c9a84c;
  text-align:center;font-size:12px;
}}
.goto-input:focus{{outline:none;border-color:#c9a84c;}}
</style>
</head>
<body>

<!-- Loading overlay -->
<div class="loading" id="loadingOverlay">
  <div class="spinner"></div>
  <div style="margin-top:16px;font-size:14px;" id="loadText">Y&uuml;kleniyor...</div>
  <div class="progress-bar"><div class="progress-fill" id="progFill" style="width:0%"></div></div>
</div>

<!-- Toolbar -->
<div class="toolbar">
  <h3>{title}</h3>
  <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
    <button onclick="showSpread(0)">&#x23EE; &#x130;lk</button>
    <button onclick="prevSpread()">&#x25C0; &Ouml;nceki</button>
    <span class="page-info" id="pageInfo">Y&uuml;kleniyor...</span>
    <button onclick="nextSpread()">Sonraki &#x25B6;</button>
    <button onclick="showSpread(Math.ceil(totalPages/2)-1)">Son &#x23ED;</button>
    <input type="number" min="1" class="goto-input" id="gotoInput" placeholder="#"
           onkeydown="if(event.key==='Enter')goToPage(parseInt(this.value))">
    <span style="color:rgba(201,168,76,0.3);margin:0 2px;">|</span>
    <button onclick="zoomOut()" title="Kucult">&#x2796;</button>
    <span class="page-info" id="zoomInfo" style="min-width:40px;">100%</span>
    <button onclick="zoomIn()" title="Buyut">&#x2795;</button>
    <button onclick="zoomReset()" title="Sifirla">&#x1F50D;</button>
    <span style="color:rgba(201,168,76,0.3);margin:0 2px;">|</span>
    <button onclick="toggleFullscreen()" id="fsBtn" title="Tam Ekran">&#x26F6; Tam Ekran</button>
  </div>
</div>

<!-- Book area -->
<div class="book-container">
  <div class="nav-arrow left" onclick="prevSpread()">&#x25C0;</div>
  <div class="book" id="book">
    <div class="page-slot left" id="leftPage"
         onclick="if(event.offsetX < this.offsetWidth*0.3) prevSpread();"></div>
    <div class="page-slot right" id="rightPage"
         onclick="if(event.offsetX > this.offsetWidth*0.7) nextSpread();"></div>
  </div>
  <div class="nav-arrow right" onclick="nextSpread()">&#x25B6;</div>
</div>

<script>
pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

var pages = [];
var currentSpread = 0;
var totalPages = 0;

// Audio context for page flip sound
var audioCtx = null;
function playFlipSound() {{
  try {{
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    var dur = 0.2, sr = audioCtx.sampleRate;
    var buf = audioCtx.createBuffer(1, sr * dur, sr);
    var d = buf.getChannelData(0);
    for (var i = 0; i < d.length; i++) {{
      var t = i / sr;
      d[i] = (Math.random() * 2 - 1) * Math.sin(Math.PI * t / dur) * 0.12;
    }}
    for (var i = 1; i < d.length; i++) d[i] = d[i] * 0.6 + d[i - 1] * 0.4;
    var s = audioCtx.createBufferSource();
    s.buffer = buf;
    s.connect(audioCtx.destination);
    s.start();
  }} catch (e) {{}}
}}

async function loadPDF() {{
  try {{
    var raw = atob("{b64_data}");
    var arr = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) arr[i] = raw.charCodeAt(i);

    var pdf = await pdfjsLib.getDocument({{data: arr}}).promise;
    totalPages = pdf.numPages;
    pages = new Array(totalPages).fill(null);
    document.getElementById("gotoInput").max = totalPages;

    // Render all pages
    for (var i = 1; i <= totalPages; i++) {{
      var page = await pdf.getPage(i);
      var vp = page.getViewport({{scale: 1.2}});
      var canvas = document.createElement("canvas");
      canvas.width = vp.width;
      canvas.height = vp.height;
      var ctx = canvas.getContext("2d");
      await page.render({{canvasContext: ctx, viewport: vp}}).promise;
      pages[i - 1] = canvas.toDataURL("image/jpeg", 0.7);
      // Free memory
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      canvas.width = 1;
      canvas.height = 1;
      canvas = null;

      // Update progress
      document.getElementById("loadText").textContent = i + " / " + totalPages;
      document.getElementById("progFill").style.width = (i / totalPages * 100) + "%";

      // Let UI breathe
      if (i % 3 === 0) await new Promise(function(r) {{ setTimeout(r, 10); }});
    }}

    // Calculate book size and show
    resizeBook();
    showSpread(0);

    document.getElementById("loadingOverlay").style.display = "none";
  }} catch (err) {{
    document.getElementById("loadText").textContent = "Hata: " + err.message;
    console.error(err);
  }}
}}

var zoomLevel = 1.0;

function resizeBook() {{
  var maxW = window.innerWidth * 0.85;
  var maxH = window.innerHeight - 70;
  var pageH = maxH;
  var pageW = pageH / 1.414;
  if (pageW * 2 > maxW) {{
    pageW = maxW / 2;
    pageH = pageW * 1.414;
  }}
  // Apply zoom
  pageW *= zoomLevel;
  pageH *= zoomLevel;
  var book = document.getElementById("book");
  var left = document.getElementById("leftPage");
  var right = document.getElementById("rightPage");
  book.style.width = (pageW * 2) + "px";
  book.style.height = pageH + "px";
  left.style.width = pageW + "px";
  left.style.height = pageH + "px";
  right.style.width = pageW + "px";
  right.style.height = pageH + "px";
  // Scroll if zoomed
  var container = document.querySelector(".book-container");
  if (zoomLevel > 1.1) {{
    container.style.overflow = "auto";
  }} else {{
    container.style.overflow = "hidden";
  }}
  document.getElementById("zoomInfo").textContent = Math.round(zoomLevel * 100) + "%";
}}

function zoomIn() {{
  if (zoomLevel < 2.5) {{
    zoomLevel += 0.15;
    resizeBook();
  }}
}}

function zoomOut() {{
  if (zoomLevel > 0.4) {{
    zoomLevel -= 0.15;
    resizeBook();
  }}
}}

function zoomReset() {{
  zoomLevel = 1.0;
  resizeBook();
}}

function toggleFullscreen() {{
  var el = document.documentElement;
  if (!document.fullscreenElement && !document.webkitFullscreenElement) {{
    if (el.requestFullscreen) el.requestFullscreen();
    else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
    document.getElementById("fsBtn").innerHTML = "&#x2716; Cik";
  }} else {{
    if (document.exitFullscreen) document.exitFullscreen();
    else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
    document.getElementById("fsBtn").innerHTML = "&#x26F6; Tam Ekran";
  }}
}}
document.addEventListener("fullscreenchange", function() {{
  setTimeout(resizeBook, 100);
  var btn = document.getElementById("fsBtn");
  if (document.fullscreenElement) btn.innerHTML = "&#x2716; Cik";
  else btn.innerHTML = "&#x26F6; Tam Ekran";
}});

function showSpread(spreadIdx) {{
  var maxSpread = Math.ceil(totalPages / 2) - 1;
  if (spreadIdx < 0) spreadIdx = 0;
  if (spreadIdx > maxSpread) spreadIdx = maxSpread;

  var leftIdx = spreadIdx * 2;
  var rightIdx = spreadIdx * 2 + 1;

  var leftSlot = document.getElementById("leftPage");
  var rightSlot = document.getElementById("rightPage");

  // Left page
  if (leftIdx < pages.length && pages[leftIdx]) {{
    leftSlot.innerHTML = '<img src="' + pages[leftIdx] + '">' +
      '<div class="page-num l">' + (leftIdx + 1) + '</div>';
  }} else {{
    leftSlot.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;' +
      'width:100%;height:100%;color:#ccc;"></div>';
  }}

  // Right page
  if (rightIdx < pages.length && pages[rightIdx]) {{
    rightSlot.innerHTML = '<img src="' + pages[rightIdx] + '">' +
      '<div class="page-num r">' + (rightIdx + 1) + '</div>';
  }} else if (rightIdx >= pages.length) {{
    rightSlot.innerHTML = '<div style="width:100%;height:100%;background:#f0ede8;"></div>';
  }} else {{
    rightSlot.innerHTML = '';
  }}

  currentSpread = spreadIdx;
  document.getElementById("pageInfo").textContent =
    "Sayfa " + (leftIdx + 1) + (rightIdx < totalPages ? "-" + (rightIdx + 1) : "") + " / " + totalPages;
}}

function nextSpread() {{
  var maxSpread = Math.ceil(totalPages / 2) - 1;
  if (currentSpread < maxSpread) {{
    playFlipSound();
    document.getElementById("rightPage").classList.add("flipping");
    setTimeout(function() {{
      showSpread(currentSpread + 1);
      document.getElementById("rightPage").classList.remove("flipping");
    }}, 200);
  }}
}}

function prevSpread() {{
  if (currentSpread > 0) {{
    playFlipSound();
    document.getElementById("leftPage").classList.add("flipping");
    setTimeout(function() {{
      showSpread(currentSpread - 1);
      document.getElementById("leftPage").classList.remove("flipping");
    }}, 200);
  }}
}}

function goToPage(num) {{
  var pg = parseInt(num);
  if (!pg || pg < 1 || pg > totalPages) return;
  var spread = Math.floor((pg - 1) / 2);
  playFlipSound();
  showSpread(spread);
}}

// Keyboard navigation
document.addEventListener("keydown", function(e) {{
  if (e.target.tagName === "INPUT") return;
  if (e.key === "ArrowRight" || e.key === " ") {{ e.preventDefault(); nextSpread(); }}
  if (e.key === "ArrowLeft") {{ e.preventDefault(); prevSpread(); }}
  if (e.key === "Home") {{ e.preventDefault(); showSpread(0); }}
  if (e.key === "End") {{ e.preventDefault(); showSpread(Math.ceil(totalPages / 2) - 1); }}
  if (e.key === "+" || e.key === "=") {{ e.preventDefault(); zoomIn(); }}
  if (e.key === "-" || e.key === "_") {{ e.preventDefault(); zoomOut(); }}
  if (e.key === "0") {{ e.preventDefault(); zoomReset(); }}
  if (e.key === "f" || e.key === "F") {{ e.preventDefault(); toggleFullscreen(); }}
}});

// Resize handler
window.addEventListener("resize", function() {{
  clearTimeout(window._resizeTimer);
  window._resizeTimer = setTimeout(function() {{
    resizeBook();
    showSpread(currentSpread);
  }}, 200);
}});

// Start
loadPDF();
</script>
</body></html>'''


# ─────────────────── Ana Render ───────────────────

def render_e_kitaplik():
    """e-Kitaplık ana render fonksiyonu."""

    # ---- CSS ----
    st.markdown("""<style>
    .ek-hero{background:linear-gradient(135deg,#94A3B8,#334155,#475569);border-radius:20px;
      padding:32px 28px;color:#fff;margin-bottom:20px;position:relative;overflow:hidden}
    .ek-hero::before{content:'';position:absolute;top:-30%;right:-15%;width:50%;height:140%;
      background:radial-gradient(circle,rgba(99,102,241,.15),transparent 60%);pointer-events:none}
    .ek-hero h2{font-size:1.5rem;font-weight:900;margin:0 0 6px}
    .ek-hero p{font-size:.85rem;opacity:.75;margin:0}
    .ek-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px}
    .ek-stat{background:#fff;border:1.5px solid rgba(0,0,0,.06);border-radius:14px;
      padding:18px;text-align:center;transition:all .3s}
    .ek-stat:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.08)}
    .ek-stat .si{font-size:1.8rem;margin-bottom:6px}
    .ek-stat .sv{font-size:1.5rem;font-weight:900;color:#6366f1}
    .ek-stat .sl{font-size:.68rem;color:#94a3b8;text-transform:uppercase;letter-spacing:1.5px;font-weight:600}
    .ek-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px;margin:16px 0}
    .ek-book{background:#fff;border:1.5px solid rgba(0,0,0,.06);border-radius:14px;
      overflow:hidden;transition:all .3s;cursor:default}
    .ek-book:hover{transform:translateY(-3px);box-shadow:0 8px 25px rgba(99,102,241,.15);
      border-color:rgba(99,102,241,.2)}
    .ek-book .cover{width:100%;height:220px;background:linear-gradient(135deg,#6366f1,#8b5cf6);
      display:flex;align-items:center;justify-content:center;font-size:3rem;color:rgba(255,255,255,.7);
      position:relative;overflow:hidden}
    .ek-book .cover img{width:100%;height:100%;object-fit:cover}
    .ek-book .cover .fmt{position:absolute;top:8px;right:8px;background:rgba(0,0,0,.6);
      color:#fff;font-size:.6rem;font-weight:700;padding:3px 8px;border-radius:6px;
      text-transform:uppercase;letter-spacing:1px}
    .ek-book .info{padding:12px 14px}
    .ek-book .info .title{font-weight:700;font-size:.85rem;color:#94A3B8;margin-bottom:4px;
      overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .ek-book .info .author{font-size:.72rem;color:#64748b}
    .ek-book .info .size{font-size:.65rem;color:#94a3b8;margin-top:4px}
    .ek-empty{text-align:center;padding:60px 20px;color:#94a3b8}
    .ek-empty .icon{font-size:4rem;margin-bottom:16px}
    .ek-empty h3{color:#64748b;font-size:1.1rem;margin-bottom:8px}
    </style>""", unsafe_allow_html=True)

    # ---- Scan books ----
    books = _scan_books()
    epub_count = sum(1 for b in books if b["format"] == "epub")
    pdf_count = sum(1 for b in books if b["format"] == "pdf")

    # ---- Hero ----
    st.markdown(f"""<div class="ek-hero">
        <h2>📖 e-Kitaplık</h2>
        <p>EPUB ve PDF kitaplarınızı doğrudan tarayıcıda okuyun • Klasik eserler indirin • Premium okuma deneyimi</p>
    </div>""", unsafe_allow_html=True)

    # ---- Ana sekmeler: Kitaplığım / Klasik Eserler İndir ----
    ek_tabs = st.tabs(["📚 Kitaplığım", "📥 Türk Edebiyatı İndir (20 Klasik)"])

    with ek_tabs[1]:
        from views._e_kitap_indir import render_kitap_indir
        render_kitap_indir(_KITAPLAR_DIR, lang_filter="tr")

    with ek_tabs[0]:

        # Show reader if already loaded (top priority)
        if st.session_state.get("ek_reader_html"):
            st.markdown(f'<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;padding:12px 18px;'
                        f'border-radius:10px 10px 0 0;font-weight:700;font-size:.95rem">'
                        f'📖 {st.session_state.get("ek_reader_title", "Kitap")}</div>', unsafe_allow_html=True)
            st.components.v1.html(st.session_state["ek_reader_html"], height=750, scrolling=False)
            if st.button("✖ Okuyucuyu Kapat", key="ek_close", type="secondary", use_container_width=True):
                for k in ("ek_reader_html", "ek_reader_title"):
                    st.session_state.pop(k, None)
                st.rerun()
            return

        # ---- Stats ----
        c1, c2, c3 = st.columns(3)
        c1.metric("📚 Toplam Kitap", len(books))
        c2.metric("📗 EPUB", epub_count)
        c3.metric("📕 PDF", pdf_count)

        if not books:
            st.info("📚 Henüz kitap yok. **Klasik Eserler İndir** sekmesinden 85 klasik eseri tek tıkla indirebilirsiniz.")
            return

        # ---- Search ----
        search = st.text_input("🔍 Kitap veya yazar ara", key="ek_search", placeholder="Ara...")

        filtered = books[:]
        if search:
            q = search.lower()
            filtered = [b for b in filtered if q in b["baslik"].lower() or q in b.get("yazar", "").lower()]
        filtered.sort(key=lambda b: b["baslik"].lower())

        st.caption(f"📚 {len(filtered)} kitap")

        # ---- Book list with clickable buttons ----
        for idx, b in enumerate(filtered):
            icon = "📗" if b["format"] == "epub" else "📕"
            size_str = f'{b.get("boyut_mb", 0)} MB'
            yazar = b.get("yazar", "Bilinmiyor")

            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.markdown(
                    f'<div style="padding:8px 0;border-bottom:1px solid rgba(0,0,0,0.06);">'
                    f'<span style="font-size:1.3rem;vertical-align:middle;">{icon}</span> '
                    f'<b style="font-size:0.95rem;">{b["baslik"]}</b>'
                    f'<span style="color:#64748b;font-size:0.8rem;margin-left:8px;">{yazar}</span>'
                    f'<span style="color:#94a3b8;font-size:0.7rem;margin-left:8px;">{b["format"].upper()} • {size_str}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col_btn:
                if st.button("📖 Oku", key=f"ek_open_{idx}", use_container_width=True):
                    filepath = os.path.join(_KITAPLAR_DIR, b["dosya"])
                    if not os.path.isfile(filepath):
                        st.error(f"Dosya bulunamadı: {b['dosya']}")
                    else:
                        file_mb = os.path.getsize(filepath) / (1024 * 1024)
                        if file_mb > 20 and b["format"] == "pdf":
                            st.warning(f"⚠️ Bu kitap {file_mb:.0f} MB — tarayıcıda açılacak (flipbook bellek sınırı).")
                            import tempfile as _tf
                            _tp = os.path.join(_tf.gettempdir(), os.path.basename(filepath))
                            import shutil; shutil.copy2(filepath, _tp)
                            os.startfile(_tp)
                        else:
                            with st.spinner(f"📖 {b['baslik']} yükleniyor..."):
                                with open(filepath, "rb") as f:
                                    raw = f.read()
                                b64 = base64.b64encode(raw).decode()
                                if b["format"] == "epub":
                                    html = _epub_reader_html(b64, b["baslik"])
                                else:
                                    html = _pdf_reader_html(b64, b["baslik"])
                                st.session_state["ek_reader_html"] = html
                                st.session_state["ek_reader_title"] = b["baslik"]
                                # Extract text for audio reader availability
                                try:
                                    _book_text_pages = _extract_book_text(filepath, b["format"])
                                    if _book_text_pages:
                                        _full_text = " ".join(_book_text_pages[:3])[:2000]
                                        _audio_bytes, _word_bounds = _generate_tts_with_timestamps(_full_text)
                                        _sent_data = _build_sentence_timestamps(_full_text, _word_bounds)
                                        _audio_b64 = base64.b64encode(_audio_bytes).decode()
                                        st.session_state["ek_audio_html"] = _audio_reader_html(
                                            _sent_data, _audio_b64, b["baslik"])
                                except Exception:
                                    pass  # Audio reader is optional
                                st.rerun()
