# -*- coding: utf-8 -*-
"""MEB-aligned English curriculum data for High School (Grades 9-12).

Each grade has 36 weekly entries following the national curriculum themes.
Unit themes aligned with content banks in views/content_banks/gradeN.py.

Unit grouping: 36 weeks -> 10 units
  Units 1-6: 4 weeks each (positions 0-3, 4-7, 8-11, 12-15, 16-19, 20-23)
  Units 7-10: 3 weeks each (positions 24-26, 27-29, 30-32, 33-35)
"""

from __future__ import annotations


def _week(w, theme, theme_tr, vocab, structure, skills, categories=None):
    """Helper to build a consistent week entry."""
    return {
        "week": w,
        "theme": theme,
        "theme_tr": theme_tr,
        "vocab": vocab,
        "structure": structure,
        "skills": skills or {},
        "linked_content": {"categories": categories or []},
    }


# ══════════════════════════════════════════════════════════════════════════════
# GRADE 9 — B1+ (Intermediate Plus)
# Units: Student Life, Personality & Identity, Modern Communication,
#        Tenses Review, World Literature, Global Issues,
#        Science & Innovation, Art & Expression, Health & Well-being,
#        The Environment
# ══════════════════════════════════════════════════════════════════════════════

CURRICULUM_GRADE9 = [
    # ── Unit 1: Student Life (Weeks 1-4) ──
    _week(1, "Student Life", "Ogrenci Hayati",
          ["academic", "extracurricular", "schedule", "assignment", "deadline", "discipline", "GPA", "semester", "syllabus", "orientation"],
          "I have to balance my academic and social life. My schedule is quite full this semester.",
          {"listening": "Ogrenci hayati hakkinda monologlar dinler.", "speaking": "Okul deneyimlerini tartisir.", "reading": "Ogrenci blog yazisi okur.", "writing": "Okul gunlugu girdisi yazar."},
          ["Egitim"]),
    _week(2, "School Clubs & Activities", "Okul Kulupleri",
          ["club", "society", "debate", "photography", "volunteer", "leadership", "teamwork", "membership", "election", "candidate"],
          "I joined the debate club. We have elections for club president next week.",
          {"listening": "Kulup tanitim konusmasi dinler.", "speaking": "Kulup deneyimlerini paylasir.", "reading": "Kulup bulteni okur.", "writing": "Kulup basvuru mektubu yazar."},
          ["Egitim"]),
    _week(3, "Study Skills", "Calisma Becerileri",
          ["note-taking", "revision", "summary", "mind map", "highlight", "concentrate", "memorise", "strategy", "habit", "routine"],
          "Good study habits include regular revision. I use mind maps to organise my notes.",
          {"listening": "Calisma teknikleri sunumu dinler.", "speaking": "Calisma yontemlerini paylasir.", "reading": "Verimlilik rehberi okur.", "writing": "Calisma plani yazar."},
          ["Egitim"]),
    _week(4, "School Life Review", "Okul Hayati Tekrar",
          ["freshman", "mentor", "guidance", "counsellor", "timetable", "assembly", "locker", "canteen", "laboratory", "library"],
          "The guidance counsellor helped me choose my courses. The library opens at seven thirty.",
          {"listening": "Okul tanitim turu dinler.", "speaking": "Okul deneyimini ozetler.", "reading": "Okul rehberi okur.", "writing": "Okul tanitim yazisi yazar."},
          ["Egitim"]),

    # ── Unit 2: Personality & Identity (Weeks 5-8) ──
    _week(5, "Personality & Identity", "Kisilik ve Kimlik",
          ["introvert", "extrovert", "personality", "trait", "characteristic", "temperament", "identity", "self-esteem", "confidence", "authentic"],
          "What kind of personality do you have? I consider myself an introvert.",
          {"listening": "Kisilik testi aciklamasi dinler.", "speaking": "Kisilik ozelliklerini tartisir.", "reading": "Psikoloji metni okur.", "writing": "Kisisel profil yazar."},
          ["Psikoloji"]),
    _week(6, "Cultural Identity", "Kulturel Kimlik",
          ["multicultural", "diversity", "inclusion", "stereotype", "prejudice", "tolerance", "cross-cultural", "heritage", "custom", "assimilation"],
          "Cultural diversity enriches society. We should challenge stereotypes.",
          {"listening": "Kulturel deneyim hikayesi dinler.", "speaking": "Kulturel farkliliklari tartisir.", "reading": "Cok kulturlu toplum metni okur.", "writing": "Kultur karsilastirma yazisi yazar."},
          ["Kultur"]),
    _week(7, "Self-Expression", "Kendini Ifade",
          ["express", "emotion", "creative", "journal", "reflect", "perspective", "unique", "values", "beliefs", "growth"],
          "Art helps me express my emotions. Everyone has a unique perspective.",
          {"listening": "Kisisel hikaye dinler.", "speaking": "Degerlerini tartisir.", "reading": "Otobiyografi parcasi okur.", "writing": "Yansitici gunluk yazar."},
          ["Kisisel"]),
    _week(8, "Adolescent Psychology", "Ergen Psikolojisi",
          ["adolescence", "development", "peer pressure", "rebellion", "maturity", "independence", "responsibility", "role model", "influence", "decision"],
          "Adolescence is a time of change. Peer pressure can influence decisions.",
          {"listening": "Psikoloji ders dinler.", "speaking": "Ergenlik deneyimlerini tartisir.", "reading": "Gelisim psikolojisi metni okur.", "writing": "Ergenlik essay'i yazar."},
          ["Psikoloji"]),

    # ── Unit 3: Modern Communication (Weeks 9-12) ──
    _week(9, "Modern Communication", "Modern Iletisim",
          ["social media", "platform", "influence", "content", "algorithm", "trending", "viral", "follower", "engagement", "digital literacy"],
          "Social media has changed how we communicate. We should be digitally literate.",
          {"listening": "Medya tartismasi dinler.", "speaking": "Sosyal medya etkilerini tartisir.", "reading": "Arastirma makale okur.", "writing": "Tartismali paragraf yazar."},
          ["Teknoloji"]),
    _week(10, "Digital Ethics", "Dijital Etik",
          ["privacy", "cyberbullying", "netiquette", "data", "security", "phishing", "copyright", "screenshot", "block", "report"],
          "Protect your privacy online. Cyberbullying is a serious issue.",
          {"listening": "Siber guvenlik uyarisi dinler.", "speaking": "Dijital etik kurallarini tartisir.", "reading": "Siber guvenlik rehberi okur.", "writing": "Dijital vatandaslik essay'i yazar."},
          ["Teknoloji"]),
    _week(11, "Media Literacy", "Medya Okuryazarligi",
          ["bias", "credibility", "fact-check", "propaganda", "source", "clickbait", "misinformation", "critical thinking", "editorial", "objectivity"],
          "Always check your sources. Not everything online is true.",
          {"listening": "Medya analiz tartismasi dinler.", "speaking": "Haberleri elestirel degerlendirir.", "reading": "Medya okuryazarligi makale okur.", "writing": "Medya analiz raporu yazar."},
          ["Medya"]),
    _week(12, "Communication Review", "Iletisim Tekrar",
          ["debate", "persuade", "rhetorical", "rebuttal", "stance", "logic", "eloquence", "body language", "eye contact", "intonation"],
          "I believe that... On the other hand... In conclusion...",
          {"listening": "Resmi tartisma dinler.", "speaking": "Muns tarzi tartisir.", "reading": "Persuasive essay okur.", "writing": "Persuasive essay yazar."},
          ["Iletisim"]),

    # ── Unit 4: Tenses Review (Weeks 13-16) ──
    _week(13, "Tenses Review", "Zamanlar Tekrari",
          ["present perfect", "past continuous", "future perfect", "conditional", "passive", "reported speech", "clause", "conjunction", "transition", "coherence"],
          "I have been studying English for 5 years. If I had more time, I would read more.",
          {"listening": "Gramer aciklamalari dinler.", "speaking": "Zaman cumlelerini kullanir.", "reading": "Gramer referans metni okur.", "writing": "Zaman uyumlu paragraf yazar."},
          ["Gramer"]),
    _week(14, "Academic Writing Basics", "Akademik Yazim Temelleri",
          ["thesis", "argument", "evidence", "conclusion", "bibliography", "citation", "paragraph", "introduction", "body", "counter-argument"],
          "A good essay has a clear thesis statement. Support your argument with evidence.",
          {"listening": "Akademik sunum dinler.", "speaking": "Tez cumlesi tartisir.", "reading": "Akademik makale okur.", "writing": "5-paragraf essay yazar."},
          ["Akademik"]),
    _week(15, "History & Civilisations", "Tarih ve Medeniyetler",
          ["civilisation", "ancient", "medieval", "renaissance", "revolution", "empire", "dynasty", "archaeology", "artifact", "legacy"],
          "The Ancient Greeks contributed greatly to democracy. The Renaissance changed art and science.",
          {"listening": "Tarih belgeseli dinler.", "speaking": "Tarihi donem tartisir.", "reading": "Tarih metni okur.", "writing": "Tarih essay'i yazar."},
          ["Tarih"]),
    _week(16, "Ethics & Philosophy", "Etik ve Felsefe",
          ["ethics", "moral", "dilemma", "principle", "value", "justice", "fairness", "virtue", "consequence", "responsibility"],
          "What is the right thing to do? We face ethical dilemmas every day.",
          {"listening": "Felsefe tartismasi dinler.", "speaking": "Etik ikilem tartisir.", "reading": "Felsefe metni okur.", "writing": "Etik gorus yazisi yazar."},
          ["Felsefe"]),

    # ── Unit 5: World Literature (Weeks 17-20) ──
    _week(17, "World Literature", "Dunya Edebiyati",
          ["novel", "short story", "poem", "playwright", "genre", "fiction", "non-fiction", "protagonist", "antagonist", "theme"],
          "Shakespeare wrote Romeo and Juliet. The protagonist faces many challenges.",
          {"listening": "Edebi eser ozeti dinler.", "speaking": "Kitap tartismasi yapar.", "reading": "Kisa hikaye veya siir okur.", "writing": "Kitap incelemesi yazar."},
          ["Edebiyat"]),
    _week(18, "Literature Analysis", "Edebiyat Analizi",
          ["metaphor", "simile", "irony", "imagery", "tone", "mood", "narrator", "point of view", "allegory", "foreshadowing"],
          "The author uses metaphor to convey... The tone of this passage is...",
          {"listening": "Siir yorumu dinler.", "speaking": "Edebi eseri analiz eder.", "reading": "Edebi analiz metni okur.", "writing": "Edebi analiz essay'i yazar."},
          ["Edebiyat"]),
    _week(19, "Semester Project", "Donem Projesi",
          ["presentation", "research", "findings", "methodology", "analysis", "visual", "slide", "audience", "Q&A", "feedback"],
          "Our project explores... The findings suggest that...",
          {"listening": "Proje sunumlarini dinler.", "speaking": "Projeyi sunar.", "reading": "Proje rehberi okur.", "writing": "Proje raporu yazar."},
          ["Projeler"]),
    _week(20, "Career Planning", "Kariyer Planlama",
          ["career", "CV", "resume", "interview", "qualification", "internship", "mentor", "networking", "portfolio", "professional"],
          "I'm preparing my CV. What qualifications do I need for this job?",
          {"listening": "Is gorusmesi ornegi dinler.", "speaking": "Kariyer hedeflerini tartisir.", "reading": "CV orneklerini okur.", "writing": "CV yazar."},
          ["Kariyer"]),

    # ── Unit 6: Global Issues (Weeks 21-24) ──
    _week(21, "Global Issues", "Kuresel Sorunlar",
          ["poverty", "inequality", "migration", "refugee", "human rights", "UN", "sustainable", "development", "goal", "awareness"],
          "Poverty is a global issue. We should raise awareness about inequality.",
          {"listening": "Haber bulteni dinler.", "speaking": "Kuresel sorunlari tartisir.", "reading": "BM raporu okur.", "writing": "Problem-cozum essay yazar."},
          ["Sosyal"]),
    _week(22, "Human Rights", "Insan Haklari",
          ["right", "freedom", "equality", "discrimination", "justice", "democracy", "dignity", "declaration", "convention", "advocacy"],
          "All people have fundamental rights. Discrimination is unacceptable.",
          {"listening": "Insan haklari konusmasi dinler.", "speaking": "Insan haklarini tartisir.", "reading": "Insan Haklari Beyannamesi okur.", "writing": "Insan haklari essay'i yazar."},
          ["Hukuk"]),
    _week(23, "Volunteering", "Gonulluluk",
          ["volunteer", "community service", "NGO", "charity", "outreach", "impact", "empowerment", "contribution", "activism", "philanthropy"],
          "Volunteering makes a difference. I joined a community service project.",
          {"listening": "Gonullu deneyimi dinler.", "speaking": "Gonulluluk deneyimlerini paylasir.", "reading": "STK raporu okur.", "writing": "Gonulluluk basvuru mektubu yazar."},
          ["Sosyal"]),
    _week(24, "Turkish Identity", "Turk Kimligi",
          ["republic", "secular", "democratic", "constitution", "citizen", "heritage", "Ataturk", "reform", "modernisation", "sovereignty"],
          "Ataturk founded the Turkish Republic. Our constitution guarantees equal rights.",
          {"listening": "Cumhuriyet tarihini dinler.", "speaking": "Cumhuriyet degerleri tartisir.", "reading": "Ataturk biyografisi okur.", "writing": "Cumhuriyet essay'i yazar."},
          ["Tarih", "Kultur"]),

    # ── Unit 7: Science & Innovation (Weeks 25-27) ──
    _week(25, "Science & Innovation", "Bilim ve Inovasyon",
          ["research", "hypothesis", "data", "peer review", "breakthrough", "innovation", "patent", "prototype", "AI", "biotechnology"],
          "Scientists are developing new treatments. AI is transforming many industries.",
          {"listening": "Bilim podcast'i dinler.", "speaking": "Bilimsel gelismeleri tartisir.", "reading": "Bilim makalesi okur.", "writing": "Bilim raporu yazar."},
          ["Bilim"]),
    _week(26, "Space Exploration", "Uzay Arastirmasi",
          ["astronaut", "space station", "Mars", "satellite", "orbit", "launch", "mission", "telescope", "NASA", "discovery"],
          "Humans may colonise Mars in the future. The ISS orbits the Earth.",
          {"listening": "Uzay belgeseli dinler.", "speaking": "Uzay kesfini tartisir.", "reading": "Uzay makale okur.", "writing": "Gelecek tahmin yazisi yazar."},
          ["Bilim"]),
    _week(27, "Entrepreneurship", "Girisimcilik",
          ["startup", "innovation", "pitch", "investor", "business model", "venture", "disruption", "scalable", "funding", "incubator"],
          "She pitched her startup idea. Innovation drives economic growth.",
          {"listening": "Girisimci hikayesi dinler.", "speaking": "Is fikri sunar.", "reading": "Girisimcilik metni okur.", "writing": "Is plani ozeti yazar."},
          ["Ekonomi"]),

    # ── Unit 8: Art & Expression (Weeks 28-30) ──
    _week(28, "Art & Expression", "Sanat ve Ifade",
          ["abstract", "contemporary", "sculpture", "exhibition", "curator", "masterpiece", "aesthetic", "symbolism", "critique", "perspective"],
          "Art is a form of expression. This abstract painting symbolises freedom.",
          {"listening": "Sanat galerisi rehber anlatimini dinler.", "speaking": "Sanat eserleri hakkinda fikrini belirtir.", "reading": "Sanat elestirisi okur.", "writing": "Sanat incelemesi yazar."},
          ["Sanat"]),
    _week(29, "Film & Cinema", "Film ve Sinema",
          ["director", "screenplay", "cinematography", "genre", "plot", "setting", "soundtrack", "award", "review", "sequel"],
          "The film was directed by... The plot explores the theme of...",
          {"listening": "Film incelemesi dinler.", "speaking": "Film tartismasi yapar.", "reading": "Film elestirisi okur.", "writing": "Film incelemesi yazar."},
          ["Sanat"]),
    _week(30, "Psychology & Behaviour", "Psikoloji ve Davranis",
          ["behaviour", "motivation", "perception", "cognition", "emotion", "habit", "stimulus", "response", "conditioning", "subconscious"],
          "Our behaviour is influenced by many factors. Habits are formed through repetition.",
          {"listening": "Psikoloji ders dinler.", "speaking": "Insan davranisini tartisir.", "reading": "Psikoloji metni okur.", "writing": "Davranis analizi yazar."},
          ["Psikoloji"]),

    # ── Unit 9: Health & Well-being (Weeks 31-33) ──
    _week(31, "Health & Well-being", "Saglik ve Refah",
          ["mental health", "well-being", "stress", "anxiety", "meditation", "mindfulness", "therapy", "counselling", "resilience", "self-care"],
          "Mental health is as important as physical health. Mindfulness can reduce stress.",
          {"listening": "Saglik uzmani konusmasi dinler.", "speaking": "Stres yonetimini tartisir.", "reading": "Saglik rehberi okur.", "writing": "Saglik tavsiye yazisi yazar."},
          ["Saglik"]),
    _week(32, "Public Speaking", "Hitabet",
          ["speech", "audience", "rhetoric", "body language", "eye contact", "intonation", "pause", "emphasis", "confidence", "charisma"],
          "Good speakers use eye contact and pauses effectively.",
          {"listening": "TED Talk dinler.", "speaking": "Kisa konusma yapar.", "reading": "Konusma teknikleri okur.", "writing": "Konusma metni yazar."},
          ["Iletisim"]),
    _week(33, "Economics & Business", "Ekonomi ve Is Dunyasi",
          ["economy", "market", "supply", "demand", "inflation", "investment", "entrepreneur", "startup", "profit", "revenue"],
          "Supply and demand affect prices. She started her own business.",
          {"listening": "Ekonomi haberi dinler.", "speaking": "Is fikirleri tartisir.", "reading": "Is plani okur.", "writing": "Is fikri ozeti yazar."},
          ["Ekonomi"]),

    # ── Unit 10: The Environment (Weeks 34-36) ──
    _week(34, "The Environment", "Cevre",
          ["ecosystem", "biodiversity", "deforestation", "carbon emissions", "greenhouse", "ozone", "conservation", "habitat", "endangered", "extinction"],
          "Deforestation threatens biodiversity. We must conserve natural habitats.",
          {"listening": "Cevre belgeseli dinler.", "speaking": "Cevre cozumleri tartisir.", "reading": "Cevre raporu okur.", "writing": "Cevre mektubu yazar."},
          ["Cevre"]),
    _week(35, "Exam Preparation", "Sinav Hazirligi",
          ["exam", "revision", "strategy", "practice", "past paper", "time management", "mock test", "performance", "score", "preparation"],
          "Start revising early. Use past papers for practice.",
          {"listening": "Sinav stratejileri dinler.", "speaking": "Calisma yontemlerini paylasir.", "reading": "Sinav stratejileri okur.", "writing": "Calisma plani yazar."},
          ["Egitim"]),
    _week(36, "Year-End Reflection", "Yil Sonu Degerlendirmesi",
          ["reflection", "achievement", "growth", "challenge", "overcome", "grateful", "milestone", "progress", "aspiration", "next steps"],
          "I have grown a lot this year. My biggest achievement was...",
          {"listening": "Degerlendirme konusmasi dinler.", "speaking": "Yili degerlendirir.", "reading": "Yansima metni okur.", "writing": "Yil sonu yansima essay'i yazar."},
          ["Kisisel"]),
]


# ══════════════════════════════════════════════════════════════════════════════
# GRADES 10-12 — B1-B2 to B2-C1
# Each grade has 36 weekly entries with themes aligned to content banks.
# Unit start positions: 0, 4, 8, 12, 16, 20, 24, 27, 30, 33
# ══════════════════════════════════════════════════════════════════════════════

def _generate_upper_grade_curriculum(grade):
    """Generate curriculum for grades 10-12 with themes aligned to content banks."""
    # 36 themes per grade, ordered so unit-start positions match content banks
    # Positions 0,4,8,12,16,20 = units 1-6 start (4 weeks each)
    # Positions 24,27,30,33 = units 7-10 start (3 weeks each)
    THEMES = {
        10: [
            # Unit 1: Identity & Society (w1-4)
            ("Identity & Society", "Kimlik ve Toplum"),
            ("Social Stratification", "Sosyal Tabakalaşma"),
            ("Youth Identity in Turkey", "Turkiye'de Genclik Kimligi"),
            ("Identity Formation", "Kimlik Olusumu"),
            # Unit 2: The Power of Language (w5-8)
            ("The Power of Language", "Dilin Gucu"),
            ("Linguistic Relativity", "Dilsel Gorelilik"),
            ("Multilingualism", "Cok Dillilik"),
            ("Language & Culture", "Dil ve Kultur"),
            # Unit 3: Media & Information (w9-12)
            ("Media & Information", "Medya ve Bilgi"),
            ("Fake News & Fact-checking", "Sahte Haberler"),
            ("Digital Literacy", "Dijital Okuryazarlik"),
            ("Echo Chambers", "Yanki Odalari"),
            # Unit 4: Advanced Grammar (w13-16)
            ("Advanced Grammar", "Ileri Gramer"),
            ("Participle Clauses & Inversions", "Ortac Tumceleri ve Devrikler"),
            ("Cleft Sentences & Emphasis", "Vurgulu Tumceler"),
            ("Discourse Markers", "Soylem Belirleyicileri"),
            # Unit 5: World Novels (w17-20)
            ("World Novels", "Dunya Romanlari"),
            ("Comparative Literature", "Karsilastirmali Edebiyat"),
            ("Narrative Techniques", "Anlatim Teknikleri"),
            ("Literary Criticism", "Edebi Elestiri"),
            # Unit 6: Globalisation (w21-24)
            ("Globalisation", "Kuresellesme"),
            ("International Trade", "Uluslararasi Ticaret"),
            ("Cultural Homogenisation", "Kulturel Turdelestirme"),
            ("Fair Trade & Ethics", "Adil Ticaret ve Etik"),
            # Unit 7: Biotechnology (w25-27)
            ("Biotechnology", "Biyoteknoloji"),
            ("Gene Editing & CRISPR", "Gen Duzenleme"),
            ("Bioethics", "Biyoetik"),
            # Unit 8: Music & Culture (w28-30)
            ("Music & Culture", "Muzik ve Kultur"),
            ("Cross-Cultural Music", "Kulturlerarasi Muzik"),
            ("Music & Identity", "Muzik ve Kimlik"),
            # Unit 9: Public Health (w31-33)
            ("Public Health", "Halk Sagligi"),
            ("Mental Health Awareness", "Ruh Sagligi Farkindaligi"),
            ("Epidemiology Basics", "Epidemiyoloji Temelleri"),
            # Unit 10: Sustainable Living (w34-36)
            ("Sustainable Living", "Surdurulebilir Yasam"),
            ("Renewable Energy", "Yenilenebilir Enerji"),
            ("Year-End Portfolio", "Yil Sonu Portfolyo"),
        ],
        11: [
            # Unit 1: Academic English (w1-4)
            ("Academic English", "Akademik Ingilizce"),
            ("Research Methodology", "Arastirma Metodolojisi"),
            ("Academic Vocabulary", "Akademik Kelime Bilgisi"),
            ("Citation & Referencing", "Atif ve Kaynak Gosterme"),
            # Unit 2: Critical Thinking (w5-8)
            ("Critical Thinking", "Elestirel Dusunce"),
            ("Logical Fallacies", "Mantik Hatalari"),
            ("Argumentation", "Argumanasyon"),
            ("Evidence Evaluation", "Kanit Degerlendirme"),
            # Unit 3: Digital Transformation (w9-12)
            ("Digital Transformation", "Dijital Donusum"),
            ("AI & Machine Learning", "YZ ve Makine Ogrenmesi"),
            ("Information Ethics", "Bilgi Etigi"),
            ("Future of Work", "Isin Gelecegi"),
            # Unit 4: Complex Structures (w13-16)
            ("Complex Structures", "Karmasik Yapilar"),
            ("Advanced Modals & Conditionals", "Ileri Kiplikler"),
            ("Academic Register", "Akademik Kayit"),
            ("Cohesion & Coherence", "Baglasiklik ve Tutarlilik"),
            # Unit 5: Comparative Literature (w17-20)
            ("Comparative Literature", "Karsilastirmali Edebiyat"),
            ("Postcolonial Literature", "Somurgecilik Sonrasi Edebiyat"),
            ("Turkish Literature in Translation", "Ceviride Turk Edebiyati"),
            ("Literary Theory", "Edebiyat Kurami"),
            # Unit 6: Geopolitics (w21-24)
            ("Geopolitics", "Jeopolitik"),
            ("International Organisations", "Uluslararasi Orgutler"),
            ("Turkey's Strategic Position", "Turkiye'nin Stratejik Konumu"),
            ("Diplomacy & Conflict Resolution", "Diplomasi ve Cozum"),
            # Unit 7: Medical Advances (w25-27)
            ("Medical Advances", "Tip Gelismeleri"),
            ("Personalised Medicine", "Kisisellestirilmis Tip"),
            ("Medical Ethics", "Tip Etigi"),
            # Unit 8: Performing Arts (w28-30)
            ("Performing Arts", "Sahne Sanatlari"),
            ("Theatre & Drama", "Tiyatro ve Drama"),
            ("Cultural Performance", "Kulturel Performans"),
            # Unit 9: Epidemiology (w31-33)
            ("Epidemiology", "Epidemiyoloji"),
            ("Pandemic Preparedness", "Pandemi Hazirlik"),
            ("Global Health Systems", "Kuresel Saglik Sistemleri"),
            # Unit 10: Cultural Exchange (w34-36)
            ("Cultural Exchange", "Kulturel Degisim"),
            ("Study Abroad", "Yurt Disi Egitim"),
            ("Year-End Showcase", "Yil Sonu Sergi"),
        ],
        12: [
            # Unit 1: University-Level English (w1-4)
            ("University-Level English", "Universite Duzeyinde Ingilizce"),
            ("Academic Discourse", "Akademik Soylem"),
            ("Seminar Skills", "Seminer Becerileri"),
            ("Research Proposal Writing", "Arastirma Onerisi Yazimi"),
            # Unit 2: Analytical Writing (w5-8)
            ("Analytical Writing", "Analitik Yazim"),
            ("Rhetorical Analysis", "Retorik Analiz"),
            ("Data Interpretation", "Veri Yorumlama"),
            ("Persuasive Techniques", "Ikna Teknikleri"),
            # Unit 3: Cybersecurity & Privacy (w9-12)
            ("Cybersecurity & Privacy", "Siber Guvenlik ve Gizlilik"),
            ("Data Protection", "Veri Koruma"),
            ("Digital Rights", "Dijital Haklar"),
            ("Surveillance Ethics", "Gozetim Etigi"),
            # Unit 4: Advanced Syntax (w13-16)
            ("Advanced Syntax", "Ileri Sozdizimi"),
            ("Nominalisation", "Adlastirma"),
            ("Academic Hedging", "Akademik Ihtiyat"),
            ("Stylistic Analysis", "Uslup Analizi"),
            # Unit 5: Nobel Literature (w17-20)
            ("Nobel Literature", "Nobel Edebiyati"),
            ("Literary Masterpieces", "Edebi Basesekler"),
            ("Author Studies", "Yazar Incelemeleri"),
            ("Literature & Society", "Edebiyat ve Toplum"),
            # Unit 6: International Relations (w21-24)
            ("International Relations", "Uluslararasi Iliskiler"),
            ("Multilateral Diplomacy", "Cok Tarafli Diplomasi"),
            ("Turkish Foreign Policy", "Turk Dis Politikasi"),
            ("Global Governance", "Kuresel Yonetisim"),
            # Unit 7: Quantum Computing (w25-27)
            ("Quantum Computing", "Kuantum Bilisim"),
            ("Future Technologies", "Gelecek Teknolojileri"),
            ("Science Communication", "Bilim Iletisimi"),
            # Unit 8: Visual Arts (w28-30)
            ("Visual Arts", "Gorsel Sanatlar"),
            ("Art as Critical Discourse", "Elestirel Soylem Olarak Sanat"),
            ("Contemporary Art Movements", "Cagdas Sanat Akimlari"),
            # Unit 9: Global Health (w31-33)
            ("Global Health", "Kuresel Saglik"),
            ("Health Governance", "Saglik Yonetisimi"),
            ("Pandemic Lessons", "Pandemi Dersleri"),
            # Unit 10: Green Technology (w34-36)
            ("Green Technology", "Yesil Teknoloji"),
            ("YDS/YDT Final Prep", "YDS/YDT Son Hazirlik"),
            ("Graduation & Beyond", "Mezuniyet ve Otesi"),
        ],
    }

    # Tema bazlı gerçek kelimeler (her tema için 10 kelime)
    VOCAB = {
        10: {
            # Unit 1: Identity & Society
            "Identity & Society": ["identity", "individualism", "conformity", "stereotype", "social norm", "marginalised", "mainstream", "subculture", "self-perception", "societal"],
            "Social Stratification": ["class", "privilege", "inequality", "mobility", "bourgeoisie", "proletariat", "hierarchy", "discrimination", "disparity", "meritocracy"],
            "Youth Identity in Turkey": ["secular", "traditional", "urbanisation", "generational", "diaspora", "pluralism", "patriotism", "civic", "demographic", "assimilation"],
            "Identity Formation": ["self-concept", "role model", "peer group", "socialisation", "autonomy", "conformist", "rebellious", "cultural capital", "social identity", "self-expression"],
            # Unit 2: The Power of Language
            "The Power of Language": ["rhetoric", "persuasion", "discourse", "eloquence", "semantics", "pragmatics", "connotation", "denotation", "euphemism", "propaganda"],
            "Linguistic Relativity": ["hypothesis", "cognition", "perception", "linguistic", "relativity", "conceptual", "categorical", "morphology", "syntax", "phonetics"],
            "Multilingualism": ["bilingual", "code-switching", "mother tongue", "lingua franca", "proficiency", "immersion", "heritage language", "acquisition", "fluency", "interference"],
            "Language & Culture": ["idiom", "proverb", "colloquialism", "slang", "register", "dialect", "jargon", "taboo", "politeness", "cross-cultural"],
            # Unit 3: Media & Information
            "Media & Information": ["credibility", "objectivity", "editorial", "headline", "bias", "sensationalism", "tabloid", "broadsheet", "press freedom", "accountability"],
            "Fake News & Fact-checking": ["misinformation", "disinformation", "verification", "source", "hoax", "clickbait", "algorithm", "filter bubble", "propaganda", "critical thinking"],
            "Digital Literacy": ["netiquette", "phishing", "encryption", "firewall", "malware", "two-factor", "privacy settings", "digital footprint", "screenshot", "metadata"],
            "Echo Chambers": ["confirmation bias", "polarisation", "filter bubble", "partisan", "tribalism", "groupthink", "cognitive bias", "selective exposure", "radicalisation", "moderation"],
            # Unit 4: Advanced Grammar
            "Advanced Grammar": ["subjunctive", "conditional", "passive voice", "reported speech", "relative clause", "gerund", "infinitive", "modal verb", "auxiliary", "tense"],
            "Participle Clauses & Inversions": ["participle", "inversion", "emphasis", "fronting", "cleft sentence", "reduced clause", "dangling modifier", "ellipsis", "nominal clause", "adverbial"],
            "Cleft Sentences & Emphasis": ["focal point", "information structure", "cleft", "pseudo-cleft", "extraposition", "topicalisation", "theme", "rheme", "given information", "new information"],
            "Discourse Markers": ["furthermore", "nevertheless", "consequently", "moreover", "whereas", "albeit", "notwithstanding", "henceforth", "thereby", "thus"],
            # Unit 5: World Novels
            "World Novels": ["narrative", "protagonist", "antagonist", "setting", "plot twist", "climax", "resolution", "motif", "symbolism", "allegory"],
            "Comparative Literature": ["intertextuality", "adaptation", "translation", "archetype", "genre", "canon", "postmodernism", "realism", "naturalism", "romanticism"],
            "Narrative Techniques": ["stream of consciousness", "unreliable narrator", "flashback", "foreshadowing", "omniscient", "first-person", "third-person", "frame narrative", "epistolary", "monologue"],
            "Literary Criticism": ["formalism", "structuralism", "feminist criticism", "postcolonial", "psychoanalytic", "Marxist", "deconstruction", "reader-response", "historicism", "semiotics"],
            # Unit 6: Globalisation
            "Globalisation": ["interdependence", "outsourcing", "multinational", "free trade", "tariff", "quota", "deregulation", "liberalisation", "protectionism", "supply chain"],
            "International Trade": ["export", "import", "surplus", "deficit", "exchange rate", "commodity", "embargo", "sanction", "bilateral", "multilateral"],
            "Cultural Homogenisation": ["Americanisation", "local culture", "cultural imperialism", "hybridisation", "glocal", "commodification", "authenticity", "erosion", "resistance", "preservation"],
            "Fair Trade & Ethics": ["exploitation", "sweatshop", "labour rights", "living wage", "certification", "transparency", "sustainable", "ethical consumption", "corporate responsibility", "supply chain ethics"],
            # Unit 7: Biotechnology
            "Biotechnology": ["genome", "genetic engineering", "cloning", "stem cell", "transgenic", "biosensor", "bioinformatics", "synthetic biology", "gene therapy", "molecular"],
            "Gene Editing & CRISPR": ["CRISPR", "Cas9", "mutation", "gene drive", "off-target", "knockout", "precision medicine", "hereditary", "chromosome", "nucleotide"],
            "Bioethics": ["consent", "autonomy", "beneficence", "non-maleficence", "eugenics", "designer baby", "clinical trial", "organ donation", "euthanasia", "bioethical dilemma"],
            # Unit 8: Music & Culture
            "Music & Culture": ["genre", "rhythm", "melody", "harmony", "composition", "improvisation", "acoustic", "amplify", "resonance", "timbre"],
            "Cross-Cultural Music": ["fusion", "indigenous", "folk music", "world music", "ethnomusicology", "percussion", "pentatonic", "scale", "syncopation", "polyrhythm"],
            "Music & Identity": ["anthem", "protest song", "subgenre", "counterculture", "mainstream", "underground", "lyric", "verse", "chorus", "bridge"],
            # Unit 9: Public Health
            "Public Health": ["epidemic", "pandemic", "vaccination", "quarantine", "surveillance", "prevalence", "incidence", "mortality", "morbidity", "screening"],
            "Mental Health Awareness": ["stigma", "anxiety", "depression", "therapy", "counselling", "resilience", "coping mechanism", "trauma", "mindfulness", "well-being"],
            "Epidemiology Basics": ["outbreak", "transmission", "vector", "pathogen", "host", "incubation", "contact tracing", "herd immunity", "R-number", "clinical trial"],
            # Unit 10: Sustainable Living
            "Sustainable Living": ["carbon footprint", "renewable", "biodegradable", "composting", "zero waste", "circular economy", "upcycling", "sustainable development", "ecological footprint", "green energy"],
            "Renewable Energy": ["solar panel", "wind turbine", "hydroelectric", "geothermal", "biomass", "grid", "energy storage", "emission", "decarbonise", "fossil fuel"],
            "Year-End Portfolio": [],
        },
        11: {
            # Unit 1: Academic English
            "Academic English": ["thesis statement", "peer review", "abstract", "methodology", "literature review", "hypothesis", "qualitative", "quantitative", "empirical", "longitudinal"],
            "Research Methodology": ["variable", "sample size", "control group", "correlation", "causation", "validity", "reliability", "replication", "statistical", "data collection"],
            "Academic Vocabulary": ["paradigm", "discourse", "framework", "criterion", "synthesis", "juxtaposition", "implication", "correlation", "phenomenon", "rationale"],
            "Citation & Referencing": ["plagiarism", "paraphrase", "quotation", "bibliography", "footnote", "endnote", "in-text citation", "reference list", "APA style", "primary source"],
            # Unit 2: Critical Thinking
            "Critical Thinking": ["premise", "inference", "deduction", "induction", "syllogism", "validity", "soundness", "assumption", "bias", "objectivity"],
            "Logical Fallacies": ["ad hominem", "straw man", "red herring", "false dichotomy", "slippery slope", "circular reasoning", "hasty generalisation", "appeal to authority", "bandwagon", "tu quoque"],
            "Argumentation": ["claim", "warrant", "rebuttal", "concession", "counterargument", "qualification", "grounds", "backing", "refutation", "dialectic"],
            "Evidence Evaluation": ["credibility", "relevance", "sufficiency", "anecdotal", "empirical", "statistical", "testimonial", "corroboration", "triangulation", "peer-reviewed"],
            # Unit 3: Digital Transformation
            "Digital Transformation": ["disruption", "automation", "digitisation", "cloud computing", "big data", "Internet of Things", "scalability", "integration", "legacy system", "digital strategy"],
            "AI & Machine Learning": ["neural network", "deep learning", "natural language processing", "algorithm", "supervised learning", "unsupervised", "reinforcement", "training data", "bias in AI", "generative AI"],
            "Information Ethics": ["surveillance", "data mining", "consent", "anonymity", "transparency", "accountability", "algorithmic bias", "digital divide", "open source", "intellectual property"],
            "Future of Work": ["remote work", "gig economy", "freelance", "upskilling", "reskilling", "automation", "hybrid work", "digital nomad", "work-life balance", "entrepreneurship"],
            # Unit 4: Complex Structures
            "Complex Structures": ["subordinate clause", "embedded clause", "complement", "adjunct", "coordination", "subordination", "apposition", "ellipsis", "anaphora", "cataphora"],
            "Advanced Modals & Conditionals": ["might have", "could have", "should have", "mixed conditional", "third conditional", "modal perfective", "epistemic", "deontic", "hypothetical", "counterfactual"],
            "Academic Register": ["hedging", "tentative", "assertive", "impersonal", "nominalisation", "passive construction", "formal register", "objectivity", "precision", "conciseness"],
            "Cohesion & Coherence": ["lexical cohesion", "referencing", "substitution", "conjunction", "thematic progression", "topic sentence", "paragraph unity", "transitional phrase", "logical connector", "discourse structure"],
            # Unit 5: Comparative Literature
            "Comparative Literature": ["intertextuality", "adaptation", "translation theory", "cultural context", "narrative voice", "thematic analysis", "close reading", "comparative analysis", "literary tradition", "reception theory"],
            "Postcolonial Literature": ["colonialism", "imperialism", "subaltern", "othering", "hybridity", "diaspora", "postcolonial identity", "resistance literature", "decolonisation", "cultural hegemony"],
            "Turkish Literature in Translation": ["Orhan Pamuk", "Elif Safak", "Nazim Hikmet", "Yasar Kemal", "translation studies", "cultural nuance", "literary prize", "Nobel laureate", "modernist", "social realism"],
            "Literary Theory": ["structuralism", "post-structuralism", "deconstruction", "semiotics", "narratology", "formalism", "new criticism", "reader-response", "cultural studies", "ecocriticism"],
            # Unit 6: Geopolitics
            "Geopolitics": ["sovereignty", "territorial", "geostrategy", "sphere of influence", "balance of power", "hegemony", "deterrence", "containment", "proxy war", "superpower"],
            "International Organisations": ["United Nations", "NATO", "European Union", "World Bank", "IMF", "WHO", "WTO", "Security Council", "General Assembly", "peacekeeping"],
            "Turkey's Strategic Position": ["Bosphorus", "NATO ally", "EU candidacy", "Middle East", "Caucasus", "energy corridor", "refugee policy", "bilateral", "soft power", "regional power"],
            "Diplomacy & Conflict Resolution": ["negotiation", "mediation", "arbitration", "ceasefire", "peace treaty", "sanction", "embargo", "humanitarian intervention", "reconciliation", "transitional justice"],
            # Unit 7: Medical Advances
            "Medical Advances": ["genomics", "telemedicine", "robotic surgery", "immunotherapy", "gene therapy", "nanotechnology", "biomarker", "clinical trial", "drug development", "regenerative medicine"],
            "Personalised Medicine": ["pharmacogenomics", "biomarker", "targeted therapy", "precision medicine", "genetic testing", "personalised treatment", "molecular profiling", "companion diagnostic", "patient stratification", "therapeutic response"],
            "Medical Ethics": ["informed consent", "confidentiality", "autonomy", "beneficence", "non-maleficence", "justice", "resource allocation", "end-of-life care", "organ transplant", "clinical ethics"],
            # Unit 8: Performing Arts
            "Performing Arts": ["choreography", "improvisation", "ensemble", "rehearsal", "director", "producer", "libretto", "overture", "act", "scene"],
            "Theatre & Drama": ["monologue", "dialogue", "soliloquy", "aside", "dramatic irony", "catharsis", "tragedy", "comedy", "farce", "absurdist"],
            "Cultural Performance": ["ritual", "ceremony", "folklore", "oral tradition", "puppet theatre", "shadow play", "Karagoz", "whirling dervish", "traditional dance", "cultural preservation"],
            # Unit 9: Epidemiology
            "Epidemiology": ["cohort study", "case-control", "cross-sectional", "randomised trial", "meta-analysis", "systematic review", "odds ratio", "relative risk", "confidence interval", "p-value"],
            "Pandemic Preparedness": ["stockpile", "ventilator", "PPE", "contact tracing", "lockdown", "social distancing", "flattening the curve", "surge capacity", "supply chain", "early warning"],
            "Global Health Systems": ["universal healthcare", "primary care", "WHO", "health equity", "access to medicine", "health infrastructure", "disease burden", "life expectancy", "health policy", "public-private partnership"],
            # Unit 10: Cultural Exchange
            "Cultural Exchange": ["exchange programme", "host family", "cultural immersion", "study abroad", "Erasmus", "cultural ambassador", "intercultural competence", "culture shock", "adaptation", "repatriation"],
            "Study Abroad": ["scholarship", "application", "transcript", "recommendation letter", "personal statement", "IELTS", "TOEFL", "admission", "tuition", "campus life"],
            "Year-End Showcase": [],
        },
        12: {
            # Unit 1: University-Level English
            "University-Level English": ["seminar", "tutorial", "lecture", "symposium", "colloquium", "academic integrity", "plagiarism detection", "peer feedback", "critical reading", "scholarly"],
            "Academic Discourse": ["hedging language", "stance", "epistemic modality", "assertive", "tentative", "impersonal construction", "nominalisation", "academic tone", "formality", "precision"],
            "Seminar Skills": ["facilitate", "moderate", "synthesise", "elaborate", "clarify", "paraphrase", "summarise", "challenge", "respond", "consensus"],
            "Research Proposal Writing": ["rationale", "research question", "literature gap", "theoretical framework", "methodology", "timeline", "budget", "significance", "limitation", "ethical approval"],
            # Unit 2: Analytical Writing
            "Analytical Writing": ["thesis", "antithesis", "synthesis", "analytical framework", "critical evaluation", "comparative analysis", "evidence-based", "nuanced", "objective", "subjective"],
            "Rhetorical Analysis": ["ethos", "pathos", "logos", "rhetorical device", "anaphora", "antithesis", "parallelism", "juxtaposition", "hyperbole", "understatement"],
            "Data Interpretation": ["graph", "chart", "trend", "correlation", "outlier", "distribution", "sample", "variable", "statistical significance", "margin of error"],
            "Persuasive Techniques": ["call to action", "emotional appeal", "logical reasoning", "credibility", "counterargument", "concession", "rhetorical question", "repetition", "analogy", "testimonial"],
            # Unit 3: Cybersecurity & Privacy
            "Cybersecurity & Privacy": ["encryption", "firewall", "vulnerability", "cyber attack", "ransomware", "breach", "authentication", "zero-day", "penetration test", "incident response"],
            "Data Protection": ["GDPR", "KVKK", "data controller", "data processor", "consent", "right to be forgotten", "data minimisation", "pseudonymisation", "breach notification", "compliance"],
            "Digital Rights": ["net neutrality", "freedom of expression", "censorship", "access to information", "digital divide", "open internet", "platform regulation", "content moderation", "algorithmic transparency", "digital sovereignty"],
            "Surveillance Ethics": ["mass surveillance", "facial recognition", "biometric", "CCTV", "whistleblower", "oversight", "proportionality", "civil liberties", "privacy by design", "surveillance capitalism"],
            # Unit 4: Advanced Syntax
            "Advanced Syntax": ["syntactic tree", "constituency", "dependency", "phrase structure", "transformation", "deep structure", "surface structure", "movement", "binding", "government"],
            "Nominalisation": ["nominalise", "abstract noun", "process noun", "agent noun", "result noun", "deverbal", "deadjectival", "suffix", "derivation", "lexical density"],
            "Academic Hedging": ["arguably", "presumably", "tentatively", "apparently", "conceivably", "potentially", "plausibly", "allegedly", "seemingly", "reportedly"],
            "Stylistic Analysis": ["register", "tone", "diction", "syntax", "imagery", "figurative language", "connotation", "denotation", "authorial voice", "stylistic device"],
            # Unit 5: Nobel Literature
            "Nobel Literature": ["laureate", "magnum opus", "oeuvre", "literary canon", "avant-garde", "existentialism", "absurdism", "magical realism", "dystopia", "bildungsroman"],
            "Literary Masterpieces": ["epic", "saga", "novella", "chronicle", "memoir", "autobiography", "anthology", "compendium", "classic", "masterwork"],
            "Author Studies": ["biographical criticism", "authorial intent", "literary influence", "thematic concern", "stylistic evolution", "narrative technique", "social commentary", "philosophical inquiry", "cultural context", "legacy"],
            "Literature & Society": ["censorship", "propaganda", "social critique", "political allegory", "satire", "protest literature", "feminist literature", "minority voices", "diaspora literature", "engaged literature"],
            # Unit 6: International Relations
            "International Relations": ["realism", "liberalism", "constructivism", "anarchy", "state sovereignty", "non-state actor", "international law", "diplomacy", "foreign policy", "global order"],
            "Multilateral Diplomacy": ["summit", "resolution", "veto", "consensus", "ratification", "treaty", "protocol", "convention", "declaration", "communique"],
            "Turkish Foreign Policy": ["neo-Ottomanism", "zero problems", "strategic depth", "regional influence", "NATO membership", "EU accession", "Eastern Mediterranean", "Syrian conflict", "defence industry", "humanitarian diplomacy"],
            "Global Governance": ["multilateralism", "supranational", "intergovernmental", "civil society", "stakeholder", "accountability", "legitimacy", "reform", "representation", "subsidiarity"],
            # Unit 7: Quantum Computing
            "Quantum Computing": ["qubit", "superposition", "entanglement", "quantum gate", "decoherence", "quantum supremacy", "quantum algorithm", "error correction", "quantum cryptography", "Shor's algorithm"],
            "Future Technologies": ["nanotechnology", "brain-computer interface", "augmented reality", "blockchain", "6G", "space tourism", "fusion energy", "autonomous vehicle", "digital twin", "synthetic biology"],
            "Science Communication": ["peer review", "scientific literacy", "public engagement", "science journalism", "infographic", "data visualisation", "popularisation", "outreach", "science policy", "ethical communication"],
            # Unit 8: Visual Arts
            "Visual Arts": ["composition", "perspective", "chiaroscuro", "palette", "medium", "installation", "conceptual art", "mixed media", "abstract expressionism", "minimalism"],
            "Art as Critical Discourse": ["art criticism", "cultural commentary", "political art", "performance art", "provocative", "subversive", "institutional critique", "public art", "site-specific", "socially engaged"],
            "Contemporary Art Movements": ["postmodernism", "neo-expressionism", "digital art", "NFT", "street art", "bioart", "relational aesthetics", "fluxus", "pop art", "surrealism"],
            # Unit 9: Global Health
            "Global Health": ["health equity", "universal coverage", "disease burden", "social determinants", "health literacy", "maternal health", "infectious disease", "non-communicable", "health system", "preventive medicine"],
            "Health Governance": ["WHO", "health policy", "regulation", "funding mechanism", "stakeholder engagement", "public-private partnership", "health diplomacy", "accountability", "transparency", "evidence-based policy"],
            "Pandemic Lessons": ["preparedness", "resilience", "misinformation", "vaccine hesitancy", "supply chain disruption", "telemedicine", "mental health impact", "socioeconomic impact", "global cooperation", "lessons learned"],
            # Unit 10: Green Technology
            "Green Technology": ["clean energy", "carbon capture", "smart grid", "energy efficiency", "green building", "sustainable transport", "circular economy", "green bond", "environmental technology", "eco-innovation"],
            "YDS/YDT Final Prep": ["reading comprehension", "vocabulary in context", "paragraph completion", "translation", "cloze test", "sentence completion", "restatement", "inference", "main idea", "supporting detail"],
            "Graduation & Beyond": [],
        },
    }

    themes = THEMES.get(grade, THEMES[10])
    grade_vocab = VOCAB.get(grade, {})
    curriculum = []
    for i, (theme_en, theme_tr) in enumerate(themes):
        w = i + 1
        is_review = "review" in theme_en.lower() or "tekrar" in theme_tr.lower()
        vocab = [] if is_review else grade_vocab.get(theme_en, [])
        skills = {
            "listening": f"{'Tekrar dinleme.' if is_review else f'{theme_en} konulu akademik dinleme yapar.'}",
            "speaking": f"{'Tekrar konusma.' if is_review else f'{theme_en} hakkinda tartisir.'}",
            "reading": f"{'Tekrar okuma.' if is_review else f'{theme_en} makale/metin okur.'}",
            "writing": f"{'Tekrar yazma.' if is_review else f'{theme_en} konulu essay/rapor yazar.'}",
        }
        curriculum.append(_week(
            w, theme_en, theme_tr, vocab,
            f"Review of recent weeks." if is_review else f"Advanced discussion and analysis of {theme_en}.",
            skills,
            ["Tekrar"] if is_review else [theme_en.split("&")[0].strip()],
        ))
    return curriculum


CURRICULUM_GRADE10 = _generate_upper_grade_curriculum(10)
CURRICULUM_GRADE11 = _generate_upper_grade_curriculum(11)
CURRICULUM_GRADE12 = _generate_upper_grade_curriculum(12)
