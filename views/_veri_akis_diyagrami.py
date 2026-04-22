"""Veli/Öğrenci Veri Akış Diyagramı — Tıkla aç/kapat."""
import streamlit as st


def render_veri_akis_diyagrami():
    """Veri akış diyagramını gömülü olarak gösterir."""

    if st.button("📊 Veri Akış Diyagramı", key="veri_akis_toggle", use_container_width=True):
        st.session_state["_veri_akis_open"] = not st.session_state.get("_veri_akis_open", False)
        st.rerun()

    if not st.session_state.get("_veri_akis_open"):
        return

    st.components.v1.html(_build_diagram_html(), height=800, scrolling=True)


def _build_diagram_html():
    return '''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e27;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0;padding:20px}

.diagram{max-width:900px;margin:0 auto}

.section{margin-bottom:16px;border-radius:12px;overflow:hidden;border:1px solid rgba(201,168,76,0.2)}
.section-header{padding:14px 20px;cursor:pointer;display:flex;justify-content:space-between;
align-items:center;transition:all 0.2s;user-select:none}
.section-header:hover{filter:brightness(1.1)}
.section-header h3{font-size:15px;font-weight:700;display:flex;align-items:center;gap:8px}
.section-header .arrow{font-size:12px;transition:transform 0.3s}
.section.open .arrow{transform:rotate(90deg)}
.section-body{max-height:0;overflow:hidden;transition:max-height 0.4s ease;background:rgba(0,0,0,0.3)}
.section.open .section-body{max-height:2000px}
.section-content{padding:16px 20px}

/* Kaynak */
.s-kaynak .section-header{background:linear-gradient(135deg,#1e3a5f,#2563eb)}
/* Merkezi */
.s-merkez .section-header{background:linear-gradient(135deg,#7c2d12,#ea580c)}
/* Cikis */
.s-cikis .section-header{background:linear-gradient(135deg,#14532d,#16a34a)}

.data-item{display:flex;align-items:center;gap:10px;padding:8px 12px;margin:4px 0;
border-radius:8px;background:rgba(255,255,255,0.04);border-left:3px solid;font-size:13px}
.data-item.json{border-color:#3b82f6}
.data-item.func{border-color:#f59e0b}
.data-item.modul{border-color:#22c55e}
.data-item.warn{border-color:#ef4444}

.data-label{font-weight:700;min-width:180px;color:#c9a84c}
.data-value{color:#94a3b8;flex:1}
.data-badge{padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600}
.badge-ok{background:rgba(34,197,94,0.15);color:#22c55e}
.badge-wait{background:rgba(245,158,11,0.15);color:#f59e0b}

.flow-arrow{text-align:center;padding:8px 0;font-size:24px;color:rgba(201,168,76,0.5)}

.sub-title{font-size:13px;font-weight:700;color:#c9a84c;margin:12px 0 6px 0;
padding-bottom:4px;border-bottom:1px solid rgba(201,168,76,0.15)}

.tag{display:inline-block;padding:2px 8px;border-radius:6px;font-size:10px;
margin:2px;background:rgba(99,102,241,0.15);color:#818cf8}
</style>
</head><body>
<div class="diagram">

<div style="text-align:center;margin-bottom:20px;">
<div style="font-size:22px;font-weight:800;color:#c9a84c;">📊 Veli/Öğrenci Veri Akış Diyagramı</div>
<div style="font-size:12px;color:#64748b;margin-top:4px;">Bölümlere tıklayarak detayları açın</div>
</div>

<!-- KAYNAK 1: Sınıf Listeleri -->
<div class="section s-kaynak" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>🏢 Kurumsal Org. > Sınıf Listeleri <span class="tag">ANA KAYNAK</span></h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="sub-title">Öğrenci Verileri</div>
<div class="data-item json"><span class="data-label">📁 students.json</span><span class="data-value">ad, soyad, sınıf, şube, numara, TC, cinsiyet</span><span class="data-badge badge-ok">✓ Aktif</span></div>
<div class="data-item json"><span class="data-label">👪 Veli bilgileri</span><span class="data-value">veli_ad, veli_tel, veli_email, veli_tc</span><span class="data-badge badge-ok">✓ Gömülü</span></div>
<div class="sub-title">Veri Yolu</div>
<div class="data-item func"><span class="data-label">load_shared_students()</span><span class="data-value">Tüm modüller bu fonksiyonla öğrenci verisine erişir</span></div>
<div class="data-item func"><span class="data-label">get_veli_display_options()</span><span class="data-value">Veli seçim listesi oluşturur</span></div>
<div class="data-item func"><span class="data-label">get_sinif_sube_listesi()</span><span class="data-value">Sınıf/şube dropdown'ları için</span></div>
</div></div>
</div>

<!-- KAYNAK 2: Akademik Takip -->
<div class="section s-kaynak" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>📚 Akademik Takip <span class="tag">VERİ ÜRETİCİ</span></h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="data-item json"><span class="data-label">📊 grades.json</span><span class="data-value">Not kayıtları: ders, dönem, tür, puan, tarih</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">📅 attendance.json</span><span class="data-value">Devamsızlık: tarih, ders, saat, tür (izinli/izinsiz)</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">📋 schedule.json</span><span class="data-value">Ders programı: gün, saat, ders, öğretmen</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">🎯 kazanim_isleme.json</span><span class="data-value">Kazanım takibi: işlendi/işlenmedi/kısmen</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">📖 etut_kayitlari.json</span><span class="data-value">Etüt/destek dersi kayıtları</span><span class="data-badge badge-ok">✓</span></div>
</div></div>
</div>

<!-- KAYNAK 3: Ölçme Değerlendirme -->
<div class="section s-kaynak" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>📝 Ölçme ve Değerlendirme <span class="tag">VERİ ÜRETİCİ</span></h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="data-item json"><span class="data-label">📄 results.json</span><span class="data-value">Sınav sonuçları: puan, D/Y/B, analiz</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">📝 exams.json</span><span class="data-value">Sınavlar: blueprint, tarih, süre, ayarlar</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">❓ questions.json</span><span class="data-value">Soru bankası: 7 tip, Bloom, rubrik</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">📋 sessions.json</span><span class="data-value">Online sınav oturumları</span><span class="data-badge badge-ok">✓</span></div>
</div></div>
</div>

<!-- KAYNAK 4: Diğer Kaynaklar -->
<div class="section s-kaynak" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>🔗 Diğer Veri Kaynakları</h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="data-item json"><span class="data-label">📢 Halkla İlişkiler</span><span class="data-value">Aday → Kayıt → Sınıf Listesi aktarımı</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">🍽️ Kurum Hizmetleri</span><span class="data-value">Yemek menüsü → Günlük rapora yansır</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">📤 DK Ödev Gönder</span><span class="data-value">dk_odevler.json → Öğrenci/Veli paneline</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">🧠 Rehberlik</span><span class="data-value">Bültenler → Veli panelinde görünür</span><span class="data-badge badge-ok">✓</span></div>
<div class="data-item json"><span class="data-label">⚠️ Erken Uyarı</span><span class="data-value">AI risk analizi → Veli bildirimi</span><span class="data-badge badge-ok">✓</span></div>
</div></div>
</div>

<div class="flow-arrow">▼ ▼ ▼</div>

<!-- MERKEZİ KATMAN -->
<div class="section s-merkez" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>⚙️ Merkezi Veri Katmanı (shared_data.py) <span class="tag">HUB</span></h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="data-item func"><span class="data-label">load_shared_students()</span><span class="data-value">Tüm öğrencileri yükle</span></div>
<div class="data-item func"><span class="data-label">get_student_display_options()</span><span class="data-value">Filtrelenmiş öğrenci seçim listesi</span></div>
<div class="data-item func"><span class="data-label">get_veli_display_options()</span><span class="data-value">Veli seçim listesi</span></div>
<div class="data-item func"><span class="data-label">get_sinif_sube_listesi()</span><span class="data-value">Sınıf/şube dropdown verileri</span></div>
<div class="data-item func"><span class="data-label">load_kurum_profili()</span><span class="data-value">Kurum adı, logo, iletişim</span></div>
<div class="data-item func"><span class="data-label">get_ik_employee_names()</span><span class="data-value">İK personel listesi</span></div>
</div></div>
</div>

<div class="flow-arrow">▼ ▼ ▼</div>

<!-- ÇIKIŞ: Veli Paneli -->
<div class="section s-cikis" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>👨‍👩‍👧 Veli Paneli <span class="tag">TÜKETİCİ</span></h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="sub-title">Günlük Akademik Rapor</div>
<div class="data-item modul"><span class="data-label">🍽️ Yemek Menüsü</span><span class="data-value">Kurum Hizmetleri → Günlük menü</span></div>
<div class="data-item modul"><span class="data-label">📅 Devamsızlık</span><span class="data-value">Akademik Takip → attendance.json</span></div>
<div class="data-item modul"><span class="data-label">💻 Online Dersler</span><span class="data-value">Akademik Takip → schedule.json</span></div>
<div class="data-item modul"><span class="data-label">📋 Ödevler</span><span class="data-value">Ölçme Değ. → exams.json (son tarih filtresi)</span></div>
<div class="data-item modul"><span class="data-label">📊 Sınav Sonuçları</span><span class="data-value">Ölçme Değ. → results.json</span></div>
<div class="data-item modul"><span class="data-label">🎯 Kazanımlar</span><span class="data-value">Akademik Takip → kazanim_isleme.json</span></div>
<div class="data-item modul"><span class="data-label">📈 Not Özeti</span><span class="data-value">Akademik Takip → grades.json</span></div>
<div class="sub-title">Diğer Sekmeler</div>
<div class="data-item modul"><span class="data-label">📖 Kazanım Ödevleri</span><span class="data-value">AI + Soru bankası → Quiz</span></div>
<div class="data-item modul"><span class="data-label">🧠 Rehberlik</span><span class="data-value">Bültenler → 20 sayfa flipbook</span></div>
<div class="data-item modul"><span class="data-label">📱 Dijital Kütüphane</span><span class="data-value">Ödev takibi → dk_odevler.json</span></div>
</div></div>
</div>

<!-- ÇIKIŞ: Öğrenci Paneli -->
<div class="section s-cikis" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>🎒 Öğrenci Paneli <span class="tag">TÜKETİCİ</span></h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="data-item modul"><span class="data-label">📋 Günlük Rapor</span><span class="data-value">Veli paneli ile aynı veri kaynakları</span></div>
<div class="data-item modul"><span class="data-label">📝 Online Sınavlar</span><span class="data-value">Ölçme Değ. → sessions.json</span></div>
<div class="data-item modul"><span class="data-label">📤 Ödev Teslimi</span><span class="data-value">Ölçme Değ. → answers.json</span></div>
<div class="data-item modul"><span class="data-label">📱 Dijital Kütüphane</span><span class="data-value">36 oyun + dergi + e-kitap</span></div>
<div class="data-item modul"><span class="data-label">🎓 AI Bireysel Eğitim</span><span class="data-value">GPT-4o → Kişiselleştirilmiş</span></div>
<div class="data-item modul"><span class="data-label">🌐 Kişisel Dil Gelişimi</span><span class="data-value">5 dil × 104 ders</span></div>
</div></div>
</div>

<!-- ÇIKIŞ: Yönetim -->
<div class="section s-cikis" onclick="this.classList.toggle('open')">
<div class="section-header">
<h3>📊 Yönetim & Raporlama <span class="tag">TÜKETİCİ</span></h3>
<span class="arrow">▶</span>
</div>
<div class="section-body"><div class="section-content">
<div class="data-item modul"><span class="data-label">📊 Yönetim Tek Ekran</span><span class="data-value">Tüm verilerin özet dashboard'u</span></div>
<div class="data-item modul"><span class="data-label">⚠️ Erken Uyarı</span><span class="data-value">Devamsızlık + Not → AI risk analizi</span></div>
<div class="data-item modul"><span class="data-label">🏅 Eğitim Koçluğu</span><span class="data-value">Bireysel performans takibi</span></div>
<div class="data-item modul"><span class="data-label">📋 Karne/Transkript</span><span class="data-value">grades.json → PDF üretimi</span></div>
</div></div>
</div>

</div>
</body></html>'''
