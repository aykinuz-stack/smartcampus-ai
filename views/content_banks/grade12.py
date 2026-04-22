# -*- coding: utf-8 -*-
"""Content banks for Grade 12 (High School Senior / Ages 17-18 / B2+/C1 CEFR).

High tier sections (15): story, reading, grammar, listening, writing,
pronunciation, culture, turkey, project, steam, review, workbook,
mission, fun_facts, gamification.

Units:
  1  University-Level English
  2  Analytical Writing
  3  Cybersecurity & Privacy
  4  Advanced Syntax
  5  Nobel Literature
  6  International Relations
  7  Quantum Computing
  8  Visual Arts
  9  Global Health
  10 Green Technology
"""

# ---------------------------------------------------------------------------
# 1. STORY CHARACTERS
# ---------------------------------------------------------------------------
STORY_CHARACTERS = {
    12: {
        1: [
            {"name": "Elif", "role": "aspiring neuroscientist and valedictorian candidate", "traits": "driven, poetic, questions everything with scientific rigour"},
            {"name": "Prof. Aydin", "role": "Applied Linguistics professor and mentor", "traits": "Socratic, diplomatic, inspires through real-world projects"},
            {"name": "Nobel Laureate (guest)", "role": "visiting neuroscience lecturer", "traits": "eloquent, thought-provoking, challenges assumptions"}
        ],
        2: [
            {"name": "Elif", "role": "analytical essay writer", "traits": "meticulous with language, pursues clarity over cleverness"},
            {"name": "Kerem", "role": "self-taught ethical hacker and contrarian thinker", "traits": "witty, challenges prescriptivism, codes and writes in parallel"},
            {"name": "Sofia", "role": "exchange student and mediator", "traits": "multilingual, diplomatic, marshals evidence from multiple perspectives"}
        ],
        3: [
            {"name": "Kerem", "role": "cybersecurity specialist and ethical hacker", "traits": "vigilant, open-source advocate, translates technical risk into plain language"},
            {"name": "Elif", "role": "neuroscience student linking cognition to security", "traits": "connects brain wiring to digital vulnerability"},
            {"name": "Deniz", "role": "visual communicator and campaign designer", "traits": "turns complex data into compelling infographics and short films"}
        ],
        4: [
            {"name": "Prof. Aydin", "role": "syntax and register instructor", "traits": "precise, uses Proustian sentences as teaching tools"},
            {"name": "Sofia", "role": "diplomat-in-training and register expert", "traits": "compresses complexity into clarity, masters modal verbs"},
            {"name": "Kerem", "role": "coder who refactors language like code", "traits": "fast, pragmatic, blogs in informal register"}
        ],
        5: [
            {"name": "Elif", "role": "literature devotee and comparative analyst", "traits": "widely read, emotionally intelligent, dog-ears favourite books"},
            {"name": "Kerem", "role": "reluctant reader turned algorithmic analyst", "traits": "maps sentence length against emotional intensity with code"},
            {"name": "Deniz", "role": "visual essayist and illustrator", "traits": "translates literary themes into watercolour and mixed-media art"}
        ],
        6: [
            {"name": "Sofia", "role": "Model UN delegate representing Turkey", "traits": "persuasive, masters hedging language, emotionally committed"},
            {"name": "Elif", "role": "epidemiological data researcher", "traits": "translates statistics into persuasive talking points"},
            {"name": "Kerem", "role": "real-time fact-checking dashboard builder", "traits": "supports team with live data during debates"}
        ],
        7: [
            {"name": "Kerem", "role": "quantum computing workshop attendee", "traits": "fascinated by qubits, builds circuit simulators"},
            {"name": "Elif", "role": "neuroscience-to-quantum bridge thinker", "traits": "connects superposition to parallel neural processing"},
            {"name": "Deniz", "role": "abstract pattern artist", "traits": "sees quantum interference patterns as art, visualises the invisible"}
        ],
        8: [
            {"name": "Deniz", "role": "solo exhibition artist and curator", "traits": "rigorous, provocative, merges surveillance critique with gold-leaf beauty"},
            {"name": "Kerem", "role": "generative art coder", "traits": "writes Python art that responds to viewer movement"},
            {"name": "Sofia", "role": "international section curator", "traits": "pairs Turkish miniatures with European installations"}
        ],
        9: [
            {"name": "Elif", "role": "epidemiological curve tracker", "traits": "explains R-naught values, bridges science and communication"},
            {"name": "Kerem", "role": "misinformation analyst and bot detector", "traits": "flags fake accounts, demonstrates viral headline mechanics"},
            {"name": "Deniz", "role": "public health poster designer", "traits": "uses colour psychology across three languages"}
        ],
        10: [
            {"name": "Elif", "role": "valedictorian and commencement speaker", "traits": "handwrites speeches on index cards, rejects teleprompters"},
            {"name": "Kerem", "role": "farewell animation coder", "traits": "live-codes gratitude in algorithms, closes laptop for once"},
            {"name": "Deniz", "role": "portrait painter and bookmark artist", "traits": "gifts oil portrait to Prof. Aydin, creates watercolour keepsakes"}
        ]
    },
}

# ---------------------------------------------------------------------------
# 2. STORY BANK (10 episodes, 14-16 sentences each)
# ---------------------------------------------------------------------------
STORY_BANK = {
    12: {
        1: {
            "title": "The Lecture That Changed Everything",
            "previously": None,
            "episode": (
                "Elif sat in the front row of the university auditorium, notebook open. "
                "The guest lecturer, a Nobel laureate in neuroscience, adjusted his microphone. "
                "'The brain is not merely an organ; it is the universe folded inward,' he began. "
                "Elif felt a shiver and scribbled the phrase verbatim. "
                "Kerem was livestreaming the talk, whispering annotations into his earpiece. "
                "Sofia cross-referenced the claims with a journal article on her phone. "
                "Deniz sketched the lecturer's profile in charcoal, capturing deep lines of thought. "
                "When Q&A opened, Elif raised her hand first. "
                "'If consciousness emerges from neural complexity, can artificial systems ever truly be conscious?' "
                "The auditorium fell silent; even the professor paused. "
                "'That is perhaps the defining question of your generation,' he replied slowly. "
                "Afterwards, the four friends gathered in the courtyard, minds ablaze. "
                "Prof. Aydin joined them with Turkish tea. 'I see the spark in your eyes,' he said. "
                "'This year, pursue a question that keeps you awake at night.' "
                "Elif looked at her friends and knew this final year would be unlike any other."
            ),
            "cliffhanger": "What questions will each of them choose — and where will those questions lead?",
            "vocab_tie": ["consciousness", "complexity", "emergence", "neural", "auditorium", "verbatim"],
        },
        2: {
            "title": "The Argument on Paper",
            "previously": "A Nobel laureate's lecture ignited the four friends' intellectual ambitions.",
            "episode": (
                "Prof. Aydin distributed Orwell's 'Politics and the English Language.' "
                "'Every sloppy sentence is a small act of intellectual dishonesty,' he declared. "
                "Elif underlined the phrase twice; Kerem composed a rebuttal in his head. "
                "'Orwell was a product of his era — prescriptivism is futile,' Kerem argued aloud. "
                "Sofia mediated: 'Both have a point, but the real skill is marshalling evidence.' "
                "Deniz pinned propaganda posters on the board: 'Words and images manipulate together.' "
                "Prof. Aydin assigned a 1,500-word analytical essay: dissect any public discourse's rhetoric. "
                "Elif chose a TED talk on neuroplasticity; Kerem picked a cybersecurity press release. "
                "Sofia selected a UN resolution on refugee rights; Deniz analysed a controversial exhibit. "
                "Late that evening, Elif stared at her blank document, cursor blinking like a metronome. "
                "She typed: 'The most dangerous lies are dressed in the language of truth.' "
                "Kerem texted the group: 'Anyone else finding it terrifyingly hard to write honestly?' "
                "Sofia replied: 'Always.' "
                "Deniz sent a sketch of a pen battling a sword, captioned: 'The oldest war.' "
                "They worked through the night, discovering that clarity required more courage than cleverness."
            ),
            "cliffhanger": "Whose essay will Prof. Aydin single out — for praise or for critique?",
            "vocab_tie": ["rhetoric", "prescriptivism", "discourse", "analytical", "propaganda", "dissect"],
        },
        3: {
            "title": "The Breach",
            "previously": "The friends grappled with their first analytical writing assignment on rhetoric and honesty.",
            "episode": (
                "Kerem's phone buzzed at 3 a.m.: unauthorised access detected on his home server. "
                "He traced the intrusion — a zero-day vulnerability in an open-source library he had contributed to. "
                "By morning he had contained the breach, but the implications haunted him. "
                "At school, Prof. Aydin said gravely: 'This is exactly what Unit 3 is about.' "
                "Sofia raised an eyebrow: 'If even Kerem can be compromised, what hope has the average user?' "
                "Elif connected it to neuroscience: 'Our brains are wired for convenience, not caution — that is the real vulnerability.' "
                "Deniz proposed a school-wide awareness campaign using infographics and short films. "
                "Kerem built a penetration-testing workshop for classmates. "
                "During the workshop, students discovered their passwords had been leaked in previous breaches. "
                "Gasps and nervous laughter filled the room. 'Knowledge is the first firewall,' Kerem told them. "
                "Prof. Aydin watched from the back, nodding: 'More effective than any textbook.' "
                "Elif journaled that night: 'Privacy is not a luxury; it is the scaffolding of autonomy.' "
                "Kerem patched the vulnerability and submitted a report to the open-source community. "
                "Sofia murmured: 'One breach, and suddenly cybersecurity is personal.' "
                "The principal, impressed, asked them to present the workshop district-wide."
            ),
            "cliffhanger": "Will the school administration support or shut down Kerem's ethical hacking programme?",
            "vocab_tie": ["vulnerability", "breach", "intrusion", "penetration", "autonomy", "scaffolding"],
        },
        4: {
            "title": "The Architecture of Sentences",
            "previously": "A real cyberattack made cybersecurity deeply personal for the group.",
            "episode": (
                "Prof. Aydin wrote a single Proustian sentence stretching across the entire board. "
                "'One hundred and twelve words, perfectly grammatical,' he said. 'Now reduce it to twelve.' "
                "The class groaned, but Sofia's eyes lit up: 'Diplomats do this daily — compress complexity into clarity.' "
                "Kerem typed three versions in a minute: 'Coding taught me to refactor,' he grinned. "
                "Deniz sketched the sentence as a tree diagram with branches and leaves. "
                "'Syntax is architecture,' she announced, stepping back to admire her drawing. "
                "Prof. Aydin introduced nominalization: 'The government decided' becomes 'The governmental decision.' "
                "'Notice the shift in agency,' he said. "
                "Elif frowned: 'Nominalization can obscure responsibility. That is dangerous in scientific writing.' "
                "'Precisely — every syntactic choice is an ethical choice,' the professor replied. "
                "The homework: rewrite a newspaper article in three registers — tabloid, broadsheet, and academic journal. "
                "Kerem finished first and posted his versions on the class forum for peer review. "
                "Sofia commented: 'Your academic version still sounds like a blog post.' "
                "Kerem shot back: 'And your tabloid reads like a treaty.' They both laughed. "
                "That evening, each of them saw language differently — as a tool that shapes thought itself."
            ),
            "cliffhanger": "Can they master register-shifting before the mid-term examination?",
            "vocab_tie": ["nominalization", "syntax", "register", "clause", "refactor", "agency"],
        },
        5: {
            "title": "The Laureate's Shadow",
            "previously": "The class explored how syntactic choices carry ethical weight in writing.",
            "episode": (
                "A literature festival brought a Nobel Prize-winning novelist to their city. "
                "Elif had devoured every book in the author's catalogue and carried a dog-eared copy. "
                "The reading was held in an old stone library that smelled of cedarwood and history. "
                "The novelist read about exile, and Sofia felt tears — her grandmother had fled a civil war. "
                "Deniz recorded the cadence, planning to translate it into watercolour paintings. "
                "During the signing, Elif asked: 'How do you decide what a character conceals versus reveals?' "
                "The novelist smiled: 'The same way you decide in life — through courage to be selective.' "
                "Kerem, initially reluctant, was captivated by the prose's mathematical precision. "
                "'There is an algorithm to her paragraphs — repetition, variation, resolution,' he whispered. "
                "Prof. Aydin assigned a comparative essay: two Nobel laureates, analyse their narrative techniques. "
                "Sofia paired Pamuk with Morrison, exploring how both weave collective memory into fiction. "
                "Elif chose Cajal's scientific memoirs alongside Ishiguro's novels. "
                "Deniz created a visual essay — part illustration, part analysis — that left Prof. Aydin speechless. "
                "Kerem wrote a code-generated textual analysis mapping sentence length against emotional intensity. "
                "The class debated: does literature change the world, or merely reflect it?"
            ),
            "cliffhanger": "Will the novelist's words inspire a project that transcends the classroom?",
            "vocab_tie": ["laureate", "cadence", "exile", "narrative", "catalogue", "collective"],
        },
        6: {
            "title": "The Delegation",
            "previously": "A Nobel novelist's reading deepened their understanding of literature's power.",
            "episode": (
                "Sofia was selected to represent Turkey at a Model United Nations conference in Geneva. "
                "She would argue for equitable vaccine distribution in the General Assembly simulation. "
                "Elif helped research epidemiological data, translating statistics into persuasive talking points. "
                "Kerem built a real-time fact-checking dashboard Sofia could consult during debates. "
                "Deniz designed the delegation's visual identity: a crescent merged with a globe. "
                "On the flight, Sofia rehearsed until cabin crew asked her to keep her voice down. "
                "The conference hall was vast — students from forty-seven countries in measured diplomatic tones. "
                "Sofia's opening silenced the room: 'A virus does not recognise a passport; neither should a vaccine.' "
                "Brazil's delegate challenged her, citing intellectual property concerns. "
                "Sofia countered with a TRIPS Agreement precedent, earning murmurs of approval. "
                "During the caucus, Japan's delegate complimented her hedging language. "
                "'You said might and could with such conviction they sounded like will and shall,' he observed. "
                "Sofia laughed: 'Prof. Aydin would call that the diplomacy of modal verbs.' "
                "The resolution passed; Sofia's clause on technology transfer was adopted verbatim. "
                "She video-called the group: 'We did it.' Her voice cracked with emotion."
            ),
            "cliffhanger": "How will Sofia's international experience reshape the group's final projects?",
            "vocab_tie": ["delegation", "equitable", "precedent", "amendment", "caucus", "diplomacy"],
        },
        7: {
            "title": "Entangled",
            "previously": "Sofia's MUN triumph in Geneva brought international diplomacy to life.",
            "episode": (
                "Kerem attended a weekend workshop at a quantum computing lab in Istanbul. "
                "Dr. Yilmaz demonstrated a five-qubit processor cooled to near absolute zero. "
                "'Qubits exist in superposition — both states simultaneously,' she explained. "
                "Kerem stared at the cryogenic chamber, frost forming fractal patterns on the glass. "
                "Back at school, he told the class: 'Imagine reading every book in a library at once.' "
                "Elif connected superposition to neural processing: 'The brain evaluates multiple hypotheses in parallel.' "
                "Sofia raised the geopolitical angle: 'Quantum supremacy could render encryption obsolete — a security crisis.' "
                "Deniz projected quantum interference patterns: 'These look like abstract art,' she marvelled. "
                "Prof. Aydin steered the discussion: 'How do we communicate concepts that defy everyday logic?' "
                "'Metaphor,' Elif said. 'Science has always relied on it.' "
                "'And mathematics,' Kerem added. 'Equations are a universal language.' "
                "The class debated whether quantum computing would democratise or concentrate power. "
                "Kerem proposed building a quantum circuit simulator as a school project. "
                "Dr. Yilmaz agreed to mentor them remotely with weekly problem sets. "
                "Deniz texted that night: 'If particles can be entangled across space, maybe ideas can too.'"
            ),
            "cliffhanger": "Can the team build a functioning quantum simulator before the science fair?",
            "vocab_tie": ["superposition", "qubit", "entangled", "cryogenic", "supremacy", "obsolete"],
        },
        8: {
            "title": "The Exhibition",
            "previously": "A visit to a quantum lab sparked an ambitious interdisciplinary project.",
            "episode": (
                "Deniz's solo exhibition opened on a rainy Friday at the school's renovated gallery. "
                "The theme: 'Invisible Architectures' — artworks exploring hidden structures that shape society. "
                "One installation featured surveillance cameras projecting live feeds onto canvas overlaid with gold leaf. "
                "'I want viewers to feel watched and beautiful simultaneously,' Deniz's artist statement read. "
                "Elif stood before a neural-network sculpture of copper wire and blown glass: 'It looks like a synapse firing.' "
                "Kerem contributed a generative art piece coded in Python, responding to viewers' movements. "
                "Sofia curated the international section, pairing Turkish miniatures with European installations. "
                "Prof. Aydin invited a national newspaper's art critic, who spent two hours examining every piece. "
                "The critic told Deniz: 'Your work has the rigour of research and the soul of protest. Rare at any age.' "
                "Deniz's hands trembled; praise from a stranger cut deeper than from friends. "
                "The highlight was a collaborative mural painted over six weekends. "
                "It depicted a tree: roots of equations, trunk of a double helix, leaves of words. "
                "Visitors lingered, some photographing details, others standing in silence. "
                "'Art is the language that speaks when all other languages fail,' Deniz said in closing. "
                "The applause was the loudest the school gallery had ever heard."
            ),
            "cliffhanger": "Will the critic's review open doors to a university art scholarship for Deniz?",
            "vocab_tie": ["installation", "generative", "curate", "rigour", "collaborative", "miniature"],
        },
        9: {
            "title": "The Outbreak",
            "previously": "Deniz's art exhibition revealed the power of interdisciplinary collaboration.",
            "episode": (
                "News broke of a novel respiratory virus emerging in Southeast Asia. "
                "Prof. Aydin paused the curriculum: 'This is happening now. Let us understand it in real time.' "
                "Elif tracked the epidemiological curve, explaining R-naught values to classmates. "
                "Kerem analysed misinformation on social media, flagging bot accounts with his detection algorithm. "
                "Sofia examined the WHO's multilingual communication strategy, noting clarity disparities. "
                "Deniz designed public health posters in three languages using colour psychology. "
                "The principal asked them to present a briefing to the student body. "
                "Elif opened: 'Fear is natural, but informed action is more powerful than fear.' "
                "Kerem demonstrated how one misleading headline generates ten thousand shares in an hour. "
                "Sofia outlined the vaccine supply chain and ethical dilemmas of triage. "
                "Deniz displayed posters distilling complex guidelines into single compelling images. "
                "Students asked sharp questions about mutation rates, travel restrictions, freedom versus safety. "
                "Prof. Aydin intervened: 'Every good question here requires knowledge from multiple disciplines.' "
                "The briefing was covered by local news; the school became a model for student-led health literacy. "
                "Elif reflected: 'Science without communication is a locked library.'"
            ),
            "cliffhanger": "As the virus evolves, will their initiative scale beyond the school walls?",
            "vocab_tie": ["epidemiological", "misinformation", "triage", "mutation", "literacy", "disparity"],
        },
        10: {
            "title": "Commencement",
            "previously": "A real-world health crisis tested their ability to apply knowledge across disciplines.",
            "episode": (
                "Graduation day arrived under a cloudless June sky, campus draped in blue and white banners. "
                "Elif was chosen as valedictorian after a unanimous faculty vote. "
                "She stood at the podium, speech handwritten on index cards — a deliberate rejection of teleprompters. "
                "'We entered as students,' she began. 'We leave as questions in search of better answers.' "
                "Sofia wiped her eyes, thinking of Geneva, of distances that shrank over the year. "
                "Kerem live-coded a farewell animation, algorithms painting 'gratitude' in real time on the screen behind Elif. "
                "Deniz unveiled a gift for Prof. Aydin: a portrait in oils capturing his habit of pacing while quoting Rumi. "
                "The professor accepted it with trembling hands: 'Teaching is the art of being changed by your students.' "
                "Diplomas were handed out, each feeling heavier than its paper weight. "
                "Elif's mother, a nurse who had worked double shifts, sobbed quietly in the third row. "
                "After the ceremony, the four sat on their favourite bench beneath the ancient plane tree. "
                "'Whatever happens next,' Sofia said, 'this year proved learning is not solitary.' "
                "Kerem closed his laptop — for once — and looked at the sky: 'The best code is co-authored.' "
                "Deniz pressed a small envelope into each hand: a watercolour bookmark of their shared tree mural. "
                "Elif held hers up to the sunlight and smiled: 'To be continued.'"
            ),
            "cliffhanger": "The story ends, but their journeys are just beginning.",
            "vocab_tie": ["valedictorian", "commencement", "unanimous", "solitary", "gratitude", "algorithm"],
        },
    },
}

# ---------------------------------------------------------------------------
# 3. READING BANK (~400 words each, formal academic prose)
# ---------------------------------------------------------------------------
READING_BANK = {
    12: {
        1: {
            "title": "The Transformation of Higher Education",
            "text": (
                "The landscape of higher education has undergone a profound transformation over the past two decades, "
                "driven by technological innovation, shifting labour market demands, and evolving pedagogical philosophies. "
                "Massive Open Online Courses, commonly known as MOOCs, were once heralded as the great equaliser — platforms "
                "that would democratise access to world-class instruction regardless of geography or socioeconomic status. "
                "Yet enrolment data reveals a more nuanced picture: completion rates hover around five to fifteen per cent, "
                "suggesting that access alone does not guarantee engagement. Critics argue that the absence of mentorship, "
                "peer collaboration, and structured accountability undermines purely digital models. Conversely, proponents "
                "contend that hybrid approaches — blending online modules with in-person seminars — offer the best of both "
                "worlds. Universities in Scandinavia have pioneered flipped classroom models where students watch lectures "
                "at home and devote classroom time to Socratic dialogue and problem-solving. A 2024 meta-analysis of "
                "forty-seven studies found that flipped classrooms improved critical thinking scores by fourteen per cent "
                "compared to traditional formats. Meanwhile, micro-credentials and stackable certificates are challenging "
                "the primacy of the four-year degree. Employers in technology, healthcare, and green energy increasingly "
                "value demonstrable skills over institutional prestige. This shift has prompted universities to unbundle "
                "curricula, offering modular pathways that allow learners to accumulate credits over a lifetime. The "
                "implications for equity are significant: working adults, caregivers, and individuals in developing nations "
                "stand to benefit most from flexible, competency-based models. However, accreditation bodies must adapt to "
                "ensure quality assurance keeps pace with innovation. As Martha Nussbaum has argued, education is not merely "
                "vocational preparation but a cultivation of capabilities essential for democratic citizenship. The challenge "
                "for the twenty-first century university is to honour that ideal while embracing structural changes that "
                "technology makes possible. Institutions must resist reducing learning to transactional modules and instead "
                "preserve the transformative, humanistic core that has defined the university since its medieval origins."
            ),
            "pre_reading": [
                "What are the main advantages and disadvantages of online learning?",
                "How might university education look different in twenty years?",
                "Should employers value skills or degrees more?",
            ],
            "post_reading": [
                "What is the author's main argument about MOOCs?",
                "Explain the 'flipped classroom' concept as described in the text.",
                "What evidence supports hybrid learning models?",
                "How do micro-credentials challenge traditional degrees?",
                "What does Nussbaum's philosophy contribute to the argument?",
                "Do you agree that education should be more than vocational preparation? Why?",
            ],
            "vocabulary": [
                {"word": "pedagogical", "meaning": "relating to teaching methods and theory", "example": "The university adopted a new pedagogical approach emphasising active learning."},
                {"word": "democratise", "meaning": "to make accessible to all people", "example": "Open-source software aims to democratise access to technology."},
                {"word": "efficacy", "meaning": "the ability to produce a desired result", "example": "The efficacy of the treatment was confirmed by clinical trials."},
                {"word": "hybrid", "meaning": "combining two different elements", "example": "Hybrid vehicles use both petrol and electric power."},
                {"word": "meta-analysis", "meaning": "statistical analysis combining results from multiple studies", "example": "The meta-analysis reviewed data from over fifty papers."},
                {"word": "micro-credential", "meaning": "a short qualification certifying specific skills", "example": "She earned a micro-credential in data analytics."},
                {"word": "unbundle", "meaning": "to separate a package into individual components", "example": "Streaming services unbundled music from traditional albums."},
                {"word": "competency-based", "meaning": "focused on demonstrated ability rather than time spent", "example": "Competency-based assessment ensures mastery before advancement."},
                {"word": "accreditation", "meaning": "official recognition that an institution meets quality standards", "example": "The programme lost accreditation due to low graduation rates."},
                {"word": "vocational", "meaning": "relating to a specific occupation or trade", "example": "Vocational training prepares students for skilled trades."},
                {"word": "transactional", "meaning": "relating to an exchange, implying lack of deeper engagement", "example": "A purely transactional view of education ignores its social value."},
                {"word": "humanistic", "meaning": "emphasising human values, potential, and dignity", "example": "The humanistic tradition values critical thinking and empathy."},
                {"word": "modular", "meaning": "composed of separate units combinable flexibly", "example": "The modular curriculum let students personalise their paths."},
                {"word": "socioeconomic", "meaning": "relating to social and economic factors combined", "example": "Socioeconomic background should not determine access to quality education."},
            ],
            "reading_strategy": "Identify the thesis in opening sentences, then track how each paragraph provides evidence, counter-arguments, or qualifications. Note signal phrases like 'critics argue' and 'conversely' to map argumentative structure.",
        },
        2: {
            "title": "The Rhetoric of Persuasion in the Digital Age",
            "text": (
                "Aristotle identified three pillars of persuasion — ethos, pathos, and logos — over two millennia ago, yet "
                "their relevance has never been greater than in the era of social media and algorithmic curation. Persuasive "
                "messages now reach billions within hours, amplified by platforms designed to maximise engagement rather than "
                "accuracy. Ethos, or credibility, has been complicated by influencer culture, where perceived authenticity "
                "substitutes for verifiable expertise. A beauty influencer endorsing a health supplement may command more "
                "trust among younger audiences than a peer-reviewed study in The Lancet. Pathos, the appeal to emotion, "
                "has been weaponised through micro-targeted advertising exploiting psychological vulnerabilities identified "
                "via data harvesting. Cambridge Analytica's use of Facebook data to influence elections remains a cautionary "
                "tale about the scalability of emotional manipulation. Logos, the appeal to reason, faces its own crisis: "
                "deepfakes, fabricated statistics, and AI-generated text have eroded the distinction between legitimate "
                "evidence and convincing fabrication. Media literacy programmes have emerged as a partial remedy, equipping "
                "citizens to interrogate sources, recognise fallacies, and evaluate provenance. Finland's national curriculum "
                "integrates critical media literacy from primary school, and studies show Finnish students outperform peers "
                "in identifying misleading headlines. However, education alone is insufficient without systemic reform: "
                "platforms must be accountable for algorithmic amplification, and regulatory frameworks must balance free "
                "expression with the right to reliable information. The ancient art of rhetoric is not obsolete; it is "
                "indispensable. Understanding how persuasion operates — and how it can be distorted — is a civic competency "
                "as essential as numeracy. In a world saturated with competing narratives, distinguishing reasoned argument "
                "from sophisticated propaganda may determine the health of democratic institutions for generations."
            ),
            "pre_reading": [
                "How do you decide whether to trust information online?",
                "Can you recall an advertisement that targeted your emotions rather than logic?",
                "What responsibility do social media platforms have for content they amplify?",
            ],
            "post_reading": [
                "Define ethos, pathos, and logos with a modern example of each.",
                "Why does the author describe pathos as 'weaponised'?",
                "What role did Cambridge Analytica play in demonstrating data-driven persuasion dangers?",
                "How does Finland's media literacy approach differ from most countries?",
                "What does the author mean by calling rhetoric 'indispensable'?",
                "Propose one reform that could reduce misinformation online.",
            ],
            "vocabulary": [
                {"word": "rhetoric", "meaning": "the art of effective or persuasive communication", "example": "Political rhetoric shapes public opinion on critical issues."},
                {"word": "algorithmic", "meaning": "relating to rules or processes followed by a computer", "example": "Algorithmic bias can perpetuate discrimination in hiring."},
                {"word": "curation", "meaning": "the selection and organisation of content", "example": "Social media curation determines which posts appear in your feed."},
                {"word": "authenticity", "meaning": "the quality of being genuine or real", "example": "Consumers value brand authenticity over polished advertising."},
                {"word": "micro-targeted", "meaning": "directed at a very specific, narrow audience", "example": "Micro-targeted ads use personal data to reach individual users."},
                {"word": "proliferation", "meaning": "rapid increase in number or amount", "example": "The proliferation of fake news alarmed media watchdogs."},
                {"word": "deepfake", "meaning": "AI-generated synthetic media designed to look authentic", "example": "Deepfake technology can make anyone appear to say anything."},
                {"word": "provenance", "meaning": "the origin or source of something", "example": "Verifying provenance is key in journalism."},
                {"word": "fallacy", "meaning": "a mistaken belief or flawed reasoning", "example": "The ad hominem fallacy attacks the person, not the argument."},
                {"word": "indispensable", "meaning": "absolutely necessary; essential", "example": "Critical thinking is indispensable in a knowledge economy."},
                {"word": "saturated", "meaning": "filled to excess", "example": "The market is saturated with streaming services."},
                {"word": "propaganda", "meaning": "biased information promoting a particular cause", "example": "Wartime propaganda dehumanises the opposing side."},
                {"word": "civic", "meaning": "relating to duties and activities of citizens", "example": "Civic education encourages democratic participation."},
                {"word": "fabrication", "meaning": "the act of inventing something false", "example": "The journalist was dismissed for fabrication of quotes."},
            ],
            "reading_strategy": "Categorise each paragraph under ethos, pathos, or logos. Then evaluate whether the author practises what they preach — does this text use all three effectively?",
        },
        3: {
            "title": "Digital Privacy in the Age of Surveillance Capitalism",
            "text": (
                "Shoshana Zuboff coined 'surveillance capitalism' to describe an economic system in which human experience "
                "is claimed as raw material for translation into behavioural data. This data is fabricated into prediction "
                "products that anticipate what individuals will do now, soon, and later. The implications for privacy are "
                "staggering. Every search query, GPS coordinate, and biometric scan contributes to a digital dossier most "
                "users neither see nor meaningfully consent to. The EU's General Data Protection Regulation, enacted in 2018, "
                "represented a landmark attempt to rebalance power between data subjects and controllers. Its provisions — "
                "the right to erasure, data portability, and explicit consent — have inspired legislation in Brazil, Japan, "
                "and South Korea. Yet enforcement remains uneven, and multinational corporations exploit jurisdictional gaps. "
                "State surveillance adds a parallel concern. The Snowden revelations exposed the scope of governmental data "
                "collection, prompting debate about national security versus civil liberties. Encryption has emerged as both "
                "shield and flashpoint: privacy advocates champion end-to-end encryption as a right, while law enforcement "
                "argues it creates 'dark spaces' for criminal activity. The philosophical dimensions are complex. Autonomy, "
                "a cornerstone of liberal democratic theory, presupposes a private sphere where individuals form beliefs free "
                "from external manipulation. When that sphere is colonised by commercial and governmental actors, self-"
                "determination erodes. Reclaiming digital privacy requires stronger legislation, robust technical safeguards, "
                "and a cultural shift in how societies value the boundary between public and intimate. As Julie Cohen wrote, "
                "'Privacy is not merely an individual preference; it is an infrastructural condition for a flourishing "
                "democratic society.' The question is whether societies will treat privacy as a right worth defending or a "
                "relic of a pre-digital era."
            ),
            "pre_reading": [
                "How much personal data do companies collect about you daily?",
                "Do you read terms and conditions before accepting? Why or why not?",
                "Is privacy a right or a privilege in the digital age?",
            ],
            "post_reading": [
                "Explain 'surveillance capitalism' in your own words.",
                "What are three key GDPR provisions mentioned in the text?",
                "Why is enforcement of data protection laws described as 'uneven'?",
                "Summarise the encryption debate between privacy advocates and law enforcement.",
                "How does privacy erosion threaten democratic autonomy?",
                "Do you agree with Julie Cohen's statement? Support your view with evidence.",
            ],
            "vocabulary": [
                {"word": "surveillance", "meaning": "close observation, especially of a suspected person or group", "example": "Surveillance technology expansion raises ethical concerns."},
                {"word": "seminal", "meaning": "strongly influencing later developments; groundbreaking", "example": "Darwin's seminal work transformed biology."},
                {"word": "behavioural data", "meaning": "information about a person's actions and habits", "example": "Behavioural data personalises online advertising."},
                {"word": "biometric", "meaning": "relating to unique physical characteristics for identification", "example": "Biometric scanners use fingerprints for access control."},
                {"word": "dossier", "meaning": "a collection of documents about a person or subject", "example": "Intelligence agencies compile dossiers on persons of interest."},
                {"word": "portability", "meaning": "the ability to transfer data between systems", "example": "Data portability lets users move information to new services."},
                {"word": "jurisdictional", "meaning": "relating to a legal body's authority within a defined area", "example": "Jurisdictional conflicts complicate cybercrime prosecution."},
                {"word": "encryption", "meaning": "converting information into a secure code", "example": "End-to-end encryption ensures only sender and recipient can read messages."},
                {"word": "autonomy", "meaning": "the right of self-governance", "example": "Patient autonomy is a core principle of medical ethics."},
                {"word": "presuppose", "meaning": "to require as a precondition", "example": "Democracy presupposes an informed citizenry."},
                {"word": "safeguard", "meaning": "a protective measure", "example": "Firewalls are essential safeguards against cyberattacks."},
                {"word": "infrastructural", "meaning": "relating to basic systems and structures of a society", "example": "Reliable internet is an infrastructural necessity for education."},
                {"word": "colonise", "meaning": "to take control of a domain (metaphorical)", "example": "Advertising has colonised nearly every digital space."},
                {"word": "flourishing", "meaning": "developing successfully; thriving", "example": "A flourishing democracy depends on a free press."},
            ],
            "reading_strategy": "Identify the multiple layers — economic, legal, technical, philosophical — and note how the author integrates them into a coherent thesis about the systemic nature of the privacy challenge.",
        },
        4: {
            "title": "The Evolution of English Syntax",
            "text": (
                "The syntactic history of English is a narrative of radical simplification and dynamic expansion. Old English, "
                "spoken from the fifth to twelfth century, was heavily inflected with four cases, three genders, and free "
                "word order. The Norman Conquest of 1066 initiated contact-induced change: French vocabulary flooded the "
                "language while inflectional endings eroded, forcing English toward subject-verb-object order. By the Early "
                "Modern period, most case distinctions had vanished, replaced by prepositions and fixed word order. Shakespeare "
                "exploited remaining flexibility brilliantly, inverting subject and verb, nesting clauses, and coining "
                "compounds that compressed metaphors into single words. The eighteenth-century standardisation movement, "
                "driven by grammarians like Lowth and Murray, imposed prescriptive rules — many borrowed from Latin — that "
                "persist in style guides today. The split infinitive prohibition, for instance, reflects Latin norms rather "
                "than natural English usage. In the twentieth and twenty-first centuries, globalisation introduced new "
                "syntactic patterns from contact with other languages. Indian English frequently uses progressive aspect "
                "with stative verbs: 'I am knowing the answer,' influenced by Hindi. Nigerian English employs serial verb "
                "constructions absent from British or American varieties. These World Englishes challenge the notion of a "
                "single 'correct' syntax and invite a pluricentric understanding of the language. Descriptive linguists "
                "argue that all varieties are equally systematic, governed by internal rules as rigorous as those of any "
                "prestige dialect. For advanced learners, syntactic awareness is not merely academic: it is the key to "
                "register flexibility, enabling writers and speakers to adapt language to context with precision. Understanding "
                "why English syntax evolved as it did illuminates the forces — conquest, trade, technology, migration — that "
                "continue to shape language today."
            ),
            "pre_reading": [
                "How has English changed since you first started learning it?",
                "Why did English become a global lingua franca?",
                "Should there be one 'correct' English, or are all varieties valid?",
            ],
            "post_reading": [
                "Describe two syntactic features of Old English mentioned in the text.",
                "How did the Norman Conquest influence English word order?",
                "Which prescriptive rules does the author identify as Latin-influenced?",
                "Give one example of a World English syntactic pattern from the text.",
                "What does 'pluricentric understanding' of English mean?",
                "How can syntactic awareness improve your writing and speaking?",
            ],
            "vocabulary": [
                {"word": "inflected", "meaning": "having word forms that change for grammatical relations", "example": "Latin is a highly inflected language with six cases."},
                {"word": "lingua franca", "meaning": "a language used between groups with different native tongues", "example": "English is the lingua franca of international business."},
                {"word": "lexical", "meaning": "relating to words or vocabulary", "example": "Lexical richness reflects the writer's vocabulary range."},
                {"word": "prescriptive", "meaning": "establishing rules about correct usage", "example": "Prescriptive grammar insists on 'whom' as an object."},
                {"word": "pluricentric", "meaning": "having multiple standard varieties", "example": "German is pluricentric with Austrian, Swiss, and German standards."},
                {"word": "subordinate clause", "meaning": "a clause dependent on the main clause", "example": "In 'Although it rained, we went out,' the first clause is subordinate."},
                {"word": "contact-induced", "meaning": "caused by interaction between speakers of different languages", "example": "Contact-induced change explains many English loanwords."},
                {"word": "standardisation", "meaning": "establishing uniform norms", "example": "Spelling standardisation accelerated after the printing press."},
                {"word": "progressive aspect", "meaning": "a verb form indicating ongoing action", "example": "'She is reading' uses progressive aspect."},
                {"word": "stative verb", "meaning": "a verb describing a state, not an action", "example": "'Know,' 'believe,' and 'own' are stative verbs."},
                {"word": "compound", "meaning": "a word formed by combining existing words", "example": "Shakespeare coined compounds like 'eyeball.'"},
                {"word": "register", "meaning": "a language variety appropriate to a context", "example": "Academic register requires formal vocabulary."},
                {"word": "coining", "meaning": "inventing a new word or phrase", "example": "The coining of 'selfie' reflected a cultural shift."},
                {"word": "serial verb", "meaning": "a sequence of verbs acting as a single predicate", "example": "'Take the book go home' uses serial verbs."},
            ],
            "reading_strategy": "Create a timeline as you read, noting each period and its syntactic changes. Chronological mapping reveals causation rather than mere sequence.",
        },
        5: {
            "title": "Nobel Literature and the Burden of Witness",
            "text": (
                "The Nobel Prize in Literature occupies a unique position: at once the most prestigious literary honour and "
                "the most controversial. Critics question the Swedish Academy's historical bias toward European and male "
                "authors — fewer than twenty of over one hundred and twenty prizes have gone to women. Yet its power to "
                "amplify marginalised voices is undeniable. When Toni Morrison won in 1993, her acceptance speech — a "
                "meditation on the violence and beauty of language — became a canonical text. Morrison called language 'an "
                "act of will and a political act,' insisting writers bear responsibility for the worlds their words create. "
                "Orhan Pamuk's 2006 prize brought attention to Turkish literary traditions and the fraught relationship "
                "between memory and national identity. His novels navigate Istanbul's layered history with melancholy "
                "precision that resists both nostalgia and polemic. Abdulrazak Gurnah's 2021 award for exploring colonialism "
                "and the refugee experience highlighted literature's capacity to humanise abstract political categories. "
                "The concept of witness — bearing testimony to suffering, injustice, and resilience — recurs across laureates. "
                "Svetlana Alexievich described her method as 'a novel of voices,' assembling oral testimonies of ordinary "
                "people who lived through catastrophes. This polyphonic approach challenges singular authorial perspectives "
                "and democratises narrative authority. For students, engaging with Nobel works is not merely aesthetic "
                "appreciation; it is an encounter with moral complexities. The Swedish Academy's charter honours those who "
                "'conferred the greatest benefit on humankind' — a reminder that literature, at its finest, is service. "
                "In a world fractured by conflict, Nobel literature offers not solutions but something equally vital: the "
                "capacity to see through another's eyes."
            ),
            "pre_reading": [
                "Name a Nobel-winning author you have read. What impressed you?",
                "Should literary prizes prioritise artistic quality or social impact?",
                "What does it mean for a writer to 'bear witness'?",
            ],
            "post_reading": [
                "What criticisms of the Nobel Prize in Literature are mentioned?",
                "How did Toni Morrison define writers' responsibility?",
                "What aspect of Pamuk's work does the text highlight?",
                "Explain Alexievich's 'polyphonic' approach.",
                "What does 'humanise abstract political categories' mean?",
                "Is literature a form of service? Support your argument.",
            ],
            "vocabulary": [
                {"word": "canonical", "meaning": "accepted as the most important works in a field", "example": "Shakespeare's plays are part of the Western canon."},
                {"word": "marginalised", "meaning": "treated as insignificant or peripheral", "example": "The initiative amplifies marginalised voices."},
                {"word": "polemic", "meaning": "a strong attack on a belief or opinion", "example": "The essay was more polemic than analysis."},
                {"word": "unflinching", "meaning": "not showing fear in facing difficulty", "example": "The documentary gave an unflinching portrayal of war."},
                {"word": "polyphonic", "meaning": "having multiple voices or perspectives", "example": "Dostoevsky's novels are celebrated for polyphonic narrative."},
                {"word": "testimony", "meaning": "a formal statement based on personal experience", "example": "Survivor testimony is central to Holocaust education."},
                {"word": "resilience", "meaning": "capacity to recover from difficulties", "example": "Community resilience after the earthquake inspired the nation."},
                {"word": "melancholy", "meaning": "a deep, reflective sadness", "example": "The film's melancholy tone captured urban loneliness."},
                {"word": "aesthetic", "meaning": "concerned with beauty or artistic appreciation", "example": "The building's aesthetic appeal masks structural flaws."},
                {"word": "laureate", "meaning": "a person honoured for outstanding achievement", "example": "The poet laureate composed a verse for the ceremony."},
                {"word": "fraught", "meaning": "filled with anxiety and difficulty", "example": "Negotiations were fraught with tension."},
                {"word": "charter", "meaning": "a formal document defining rights and principles", "example": "The UN Charter establishes foundational goals."},
                {"word": "nostalgia", "meaning": "sentimental longing for the past", "example": "Nostalgia for simpler times pervades the novel."},
                {"word": "conferred", "meaning": "granted or bestowed", "example": "The university conferred an honorary degree."},
            ],
            "reading_strategy": "Identify each laureate and the literary quality attributed to them. Consider how individual examples build toward the broader argument about literature and witness.",
        },
        6: {
            "title": "Multilateral Diplomacy in an Era of Fragmentation",
            "text": (
                "The post-WWII international order, anchored by the UN, World Bank, and IMF, was predicated on the assumption "
                "that multilateral cooperation would replace unilateral action. For decades this held: EU expansion, WTO trade "
                "agreements, and environmental accords like Kyoto confirmed steady progress toward a rules-based order. "
                "However, the twenty-first century has seen a resurgence of nationalism, protectionism, and bilateral deal-"
                "making. Brexit, NAFTA renegotiation, and WTO Appellate Body paralysis are symptoms of broader disillusionment "
                "with supranational governance. Climate diplomacy is instructive: the Paris Agreement relies on nationally "
                "determined contributions — voluntary pledges whose ambition varies dramatically. A 2024 emissions gap report "
                "concluded current pledges would yield 2.5 degrees warming, well beyond the stated target. The gap between "
                "aspiration and implementation exposes a fundamental tension: consensus-building involves compromise, and "
                "compromise dilutes ambition. Yet alternatives — unilateralism, isolationism, great-power bilateralism — "
                "offer no systemic solution to transnational challenges. Pandemics, climate change, nuclear proliferation, "
                "and cybersecurity threats respect no borders. The task for the next generation is not to abandon "
                "multilateralism but to reform it: build institutions that are more agile, inclusive, and capable of holding "
                "signatories accountable. Regional arrangements like ASEAN and the African Union demonstrate that "
                "multilateralism can be adapted to local contexts. Digital diplomacy and AI-assisted translation are lowering "
                "barriers to participation, enabling smaller states to engage more effectively. As Kofi Annan observed, "
                "'We may have different religions, different languages, different coloured skin, but we all belong to one "
                "human race.' That belonging is the premise of multilateralism — and its best argument."
            ),
            "pre_reading": [
                "What international organisations can you name, and what do they do?",
                "Is international cooperation more important now than fifty years ago?",
                "What are the risks of countries acting alone on global issues?",
            ],
            "post_reading": [
                "What assumption underpinned the post-WWII international order?",
                "List three examples of multilateral cooperation in the late twentieth century.",
                "What challenges to multilateralism does the author identify?",
                "Why does the Paris Agreement illustrate a tension in multilateral diplomacy?",
                "What reforms does the author suggest for multilateral institutions?",
                "Can multilateralism survive nationalist trends? Argue your position.",
            ],
            "vocabulary": [
                {"word": "multilateral", "meaning": "involving three or more parties, especially governments", "example": "Multilateral trade agreements benefit all participants."},
                {"word": "predicated", "meaning": "based or established upon", "example": "The policy was predicated on continued growth."},
                {"word": "unilateral", "meaning": "performed by only one side", "example": "The unilateral withdrawal surprised allies."},
                {"word": "protectionism", "meaning": "restricting imports to protect domestic industries", "example": "Rising protectionism threatens global supply chains."},
                {"word": "supranational", "meaning": "having authority transcending national boundaries", "example": "The EU is a supranational body with legislative powers."},
                {"word": "signatory", "meaning": "a party that has signed an agreement", "example": "All signatories pledged to reduce emissions."},
                {"word": "consensus", "meaning": "general agreement among a group", "example": "Building consensus requires patience and skill."},
                {"word": "dilute", "meaning": "to weaken or reduce strength", "example": "Excessive compromise can dilute policy effectiveness."},
                {"word": "transnational", "meaning": "extending across national boundaries", "example": "Organised crime is a transnational challenge."},
                {"word": "agile", "meaning": "able to adapt quickly", "example": "Agile institutions respond faster to crises."},
                {"word": "bilateral", "meaning": "involving two parties", "example": "Bilateral negotiations resumed after a year."},
                {"word": "resurgence", "meaning": "a revival or renewed occurrence", "example": "The resurgence of populism reshaped politics."},
                {"word": "isolationism", "meaning": "avoiding involvement in international affairs", "example": "Isolationism is impractical in a connected economy."},
                {"word": "accountable", "meaning": "required to justify actions", "example": "Officials must be held accountable by the public."},
            ],
            "reading_strategy": "Map the argument chronologically: multilateral optimism, period of challenge, proposed way forward. Note concessive structures ('Yet,' 'However') signalling the author's balanced stance.",
        },
        7: {
            "title": "Quantum Computing: Promise, Peril, and Limits",
            "text": (
                "Quantum computing represents a fundamental paradigm shift in how information is encoded and interpreted. "
                "Classical computers use bits — binary units in state zero or one. Quantum computers utilise qubits, which "
                "exist in superposition of both states simultaneously. When qubits become entangled — what Einstein called "
                "'spooky action at a distance' — measuring one instantaneously determines its partner's state regardless "
                "of distance. These properties enable parallel exploration of vast solution spaces. Drug discovery could be "
                "revolutionised by quantum simulations modelling molecular interactions at the atomic level — a task taking "
                "classical supercomputers millennia. Cryptography faces profound impact: Shor's algorithm, on a powerful "
                "quantum computer, could factor large primes exponentially faster than classical methods, breaking RSA "
                "encryption. This has spurred development of quantum-resistant standards; NIST published its first post-"
                "quantum algorithms in 2024. Yet quantum computing remains nascent. Current machines suffer from decoherence "
                "— loss of quantum information due to environmental interference — and high error rates requiring extensive "
                "correction. Scaling from noisy intermediate-scale devices to fault-tolerant machines solving real problems "
                "is enormously complex. The philosophical implications are compelling: quantum computing forces us to confront "
                "limits of deterministic thinking and embrace probabilistic models challenging intuitive causality. Richard "
                "Feynman, who first proposed quantum simulation in 1982, noted that 'Nature isn't classical, and if you want "
                "to make a simulation of nature, you'd better make it quantum mechanical.' The revolution is not only "
                "technological but epistemological — a redefinition of what it means to compute, know, and predict. Whether "
                "quantum supremacy becomes a democratising force or a tool of concentrated power depends on governance "
                "decisions being made today."
            ),
            "pre_reading": [
                "What is the difference between classical and quantum computers?",
                "Why might breaking encryption be both useful and dangerous?",
                "Can you think of a problem that requires more computing power than currently available?",
            ],
            "post_reading": [
                "Explain superposition as described in the text.",
                "What did Einstein mean by 'spooky action at a distance'?",
                "How could quantum computing revolutionise drug discovery?",
                "What is Shor's algorithm and why is it significant?",
                "What is decoherence and why is it a challenge?",
                "In what sense is the quantum revolution 'epistemological'?",
            ],
            "vocabulary": [
                {"word": "paradigm", "meaning": "a fundamental framework of thought", "example": "Quantum physics was a paradigm shift in science."},
                {"word": "superposition", "meaning": "existing in multiple states simultaneously", "example": "Superposition allows qubits to be zero and one at once."},
                {"word": "entangled", "meaning": "quantum-mechanically linked particles", "example": "Entangled photons enable quantum key distribution."},
                {"word": "decoherence", "meaning": "loss of quantum behaviour from environmental interaction", "example": "Decoherence is the primary obstacle to stable quantum computers."},
                {"word": "cryptography", "meaning": "secure communication through encoding", "example": "Modern cryptography relies on hard mathematical problems."},
                {"word": "exponentially", "meaning": "at an increasingly rapid rate", "example": "Computing power has grown exponentially."},
                {"word": "nascent", "meaning": "just beginning to develop", "example": "The nascent quantum industry attracts billions."},
                {"word": "fault-tolerant", "meaning": "operating correctly despite component failures", "example": "Fault-tolerant systems are essential for infrastructure."},
                {"word": "probabilistic", "meaning": "based on probability rather than certainty", "example": "Quantum mechanics is inherently probabilistic."},
                {"word": "epistemological", "meaning": "relating to the theory of knowledge", "example": "The discovery raised epistemological questions."},
                {"word": "deterministic", "meaning": "following fixed cause and effect", "example": "Classical physics is largely deterministic."},
                {"word": "protocol", "meaning": "a set of rules governing a procedure", "example": "Internet communication follows TCP/IP protocol."},
                {"word": "intermediate-scale", "meaning": "between experimental and production size", "example": "Current quantum devices are noisy intermediate-scale."},
                {"word": "causality", "meaning": "the relationship between cause and effect", "example": "Establishing causality requires more than correlation."},
            ],
            "reading_strategy": "Distinguish between theoretical potential and current capability. The gap between promise and reality is central to the author's balanced assessment.",
        },
        8: {
            "title": "The Visual Arts as Critical Discourse",
            "text": (
                "Throughout history, visual arts have functioned as instruments of social commentary, political resistance, "
                "and philosophical inquiry. The cave paintings of Lascaux, seventeen thousand years old, may be humanity's "
                "earliest attempts to impose narrative order on chaos. Renaissance artists like Leonardo and Michelangelo "
                "were public intellectuals whose commissions carried political messages. The Sistine Chapel ceiling is "
                "simultaneously a theological statement, a display of papal power, and a perspectival tour de force. The "
                "twentieth century radicalised art's political role. Picasso's Guernica, responding to the Spanish Civil "
                "War bombing, became the definitive anti-war image — a monochrome howl of anguish refusing the consolation "
                "of colour. The Dada movement rejected rational aesthetics, using absurdity to protest industrialised "
                "slaughter. Contemporary artists continue pushing boundaries. Ai Weiwei confronts authoritarianism with "
                "wit and scale; Kara Walker's silhouettes excavate slavery's legacy. Street art, once dismissed as vandalism, "
                "has been legitimised by Banksy, whose anonymous interventions raise questions about ownership and the "
                "commodification of dissent. Digital art and NFTs introduce debates about authenticity, originality, and the "
                "definition of art itself. What unites these practices is a commitment to making the invisible visible — "
                "rendering power structures and suppressed histories legible through visual form. For the engaged viewer, "
                "art demands interpretation, challenges assumptions, and invites renegotiation of the boundary between "
                "observer and participant. The philosopher Jacques Ranciere argued that aesthetics and politics are "
                "inseparable because both involve the distribution of the sensible — determining what can be seen, heard, "
                "and thought. To look at art critically is, in essence, to practise critical citizenship."
            ),
            "pre_reading": [
                "Can art change society, or does it only reflect it?",
                "What is the most powerful artwork you have seen, and why?",
                "Should art always carry a social or political message?",
            ],
            "post_reading": [
                "How do Lascaux cave paintings establish the author's historical argument?",
                "What multiple meanings does the Sistine Chapel ceiling carry?",
                "Why is Guernica described as 'a monochrome howl of anguish'?",
                "What was the Dada movement protesting, and how?",
                "How do Ai Weiwei and Banksy continue art as social commentary?",
                "Explain 'critical viewing as critical citizenship.'",
            ],
            "vocabulary": [
                {"word": "discourse", "meaning": "formal discussion or debate on a topic", "example": "Academic discourse requires evidence-based argumentation."},
                {"word": "perspectival", "meaning": "relating to representing 3D space on a flat surface", "example": "Renaissance artists mastered perspectival drawing."},
                {"word": "monochrome", "meaning": "using only one colour or its shades", "example": "The monochrome photograph conveyed stark timelessness."},
                {"word": "absurdity", "meaning": "the quality of being wildly unreasonable", "example": "The play used absurdity to critique societal norms."},
                {"word": "commodification", "meaning": "treating something as a product to buy and sell", "example": "Commodification reduces art to market transactions."},
                {"word": "dissent", "meaning": "expression of opinions contrary to official views", "example": "Artistic dissent is the first casualty of authoritarianism."},
                {"word": "excavate", "meaning": "to uncover by careful investigation (figurative)", "example": "The historian excavated forgotten colonial stories."},
                {"word": "silhouette", "meaning": "a dark outline against a lighter background", "example": "Walker's silhouettes depict racial violence with stark simplicity."},
                {"word": "legitimise", "meaning": "to make acceptable or lawful", "example": "Gallery exhibitions legitimised street art."},
                {"word": "intervention", "meaning": "action taken to alter a situation", "example": "Banksy's interventions appear unannounced on public walls."},
                {"word": "legible", "meaning": "clear enough to understand", "example": "Good infographics make complex data legible."},
                {"word": "renegotiation", "meaning": "discussing terms again for new agreement", "example": "Social media forced a renegotiation of privacy norms."},
                {"word": "tour de force", "meaning": "an impressive feat of skill", "example": "The recital was a tour de force of mastery."},
                {"word": "implicit", "meaning": "suggested though not directly expressed", "example": "The painting carried an implicit critique of power."},
            ],
            "reading_strategy": "Trace the chronological progression from ancient to contemporary art. For each period, identify both the artistic movement and the social context linked to it.",
        },
        9: {
            "title": "Global Health Governance: Lessons From Pandemics",
            "text": (
                "The history of global health governance is a history of crises that exposed institutional inadequacy and "
                "catalysed reform. The International Sanitary Conferences of the mid-nineteenth century, responding to cholera "
                "pandemics, established that disease control required international cooperation — radical in an era of fierce "
                "sovereignty. The WHO's founding in 1948 institutionalised this principle, and its crowning achievement, "
                "smallpox eradication in 1980, demonstrated what concerted action could accomplish. Yet structural weaknesses "
                "persisted. The WHO's dependence on voluntary contributions — over eighty per cent of its budget by 2020 — "
                "left it vulnerable to donor influence. The 2014 Ebola outbreak exposed catastrophic failures in surveillance "
                "and rapid response, prompting recommended reforms. COVID-19 subjected global health architecture to its "
                "most severe stress test, laying bare vaccine access inequities and the dangers of politicised health "
                "messaging. The concept of 'health security' gained traction, though critics warned that securitising health "
                "could marginalise social determinants: poverty, education, housing, nutrition. Pandemic Treaty negotiations, "
                "launched in 2022, sought to codify lessons: equitable access, transparent data sharing, strengthened "
                "preparedness. Whether these yield binding commitments or aspirational declarations remains uncertain. "
                "Meanwhile, antimicrobial resistance — dubbed the 'silent pandemic' — kills over a million people annually "
                "and receives a fraction of the attention given to acute outbreaks. The One Health approach, recognising "
                "interconnections between human, animal, and environmental health, offers a more holistic framework. Global "
                "health governance is only as effective as the political will sustaining it. The next pandemic is not a "
                "question of if but when, and preparedness is a measure of civilisational maturity."
            ),
            "pre_reading": [
                "What lessons did the world learn from COVID-19?",
                "Why is international cooperation essential for disease outbreaks?",
                "Should health be treated as a security issue? What are the pros and cons?",
            ],
            "post_reading": [
                "What event first established the principle of international health cooperation?",
                "Why is smallpox eradication the WHO's greatest achievement?",
                "What structural weakness of the WHO is highlighted?",
                "How did Ebola and COVID-19 expose governance failures?",
                "What risks come from 'securitising' health?",
                "Will the Pandemic Treaty succeed? Justify your view.",
            ],
            "vocabulary": [
                {"word": "governance", "meaning": "the system by which a society is managed", "example": "Good governance requires transparency."},
                {"word": "catalyse", "meaning": "to cause or accelerate change", "example": "The crisis catalysed banking reforms."},
                {"word": "eradication", "meaning": "complete elimination of something", "example": "Polio eradication remains a global priority."},
                {"word": "concerted", "meaning": "jointly arranged; coordinated", "example": "A concerted effort is needed for climate change."},
                {"word": "surveillance", "meaning": "systematic monitoring for disease detection", "example": "Disease surveillance enables early outbreak detection."},
                {"word": "inequity", "meaning": "unfairness in resource distribution", "example": "Vaccine inequity prolonged the pandemic."},
                {"word": "securitise", "meaning": "to frame a non-military issue as a security threat", "example": "Securitising migration can violate human rights."},
                {"word": "determinant", "meaning": "a factor decisively affecting outcome", "example": "Education is a key social determinant of health."},
                {"word": "codify", "meaning": "to arrange into a systematic code", "example": "International law codifies prisoner-of-war rights."},
                {"word": "countermeasure", "meaning": "an action to counteract a threat", "example": "Vaccines are primary medical countermeasures."},
                {"word": "auspices", "meaning": "sponsorship or guidance of an authority", "example": "Negotiations were under UN auspices."},
                {"word": "aspirational", "meaning": "expressing hope rather than obligation", "example": "The declaration was aspirational, lacking enforcement."},
                {"word": "preparedness", "meaning": "readiness for a future event", "example": "Pandemic preparedness requires stockpiling supplies."},
                {"word": "binding", "meaning": "imposing a legal obligation", "example": "A binding treaty is enforceable under international law."},
            ],
            "reading_strategy": "Identify the crisis-reform-limitation pattern recurring throughout. This cyclical structure is the author's central framework for analysing global health governance.",
        },
        10: {
            "title": "Green Technology and the Sustainable Energy Transition",
            "text": (
                "The transition from fossil fuels to renewables is one of the twenty-first century's defining challenges. "
                "The scientific consensus, articulated by the IPCC, is unequivocal: human combustion of coal, oil, and gas "
                "drives warming at an unprecedented rate. The economic case has strengthened dramatically. Solar photovoltaic "
                "costs fell ninety per cent between 2010 and 2024, making solar cheaper than new coal in most markets. "
                "Onshore wind followed a similar trajectory, and battery storage costs declined over eighty per cent, "
                "addressing intermittency. Electric vehicles, powered by increasingly efficient batteries, should reach "
                "price parity with combustion engines by 2027. Yet the transition is complex. Extraction of critical "
                "minerals — lithium, cobalt, rare earths — raises environmental and ethical concerns, particularly in the "
                "Democratic Republic of Congo, where artisanal cobalt mining involves child labour. The concept of a 'just "
                "transition' recognises that decarbonisation must not exacerbate inequality. Workers in fossil fuel industries "
                "deserve retraining and safety nets; developing nations deserve support to leapfrog carbon-intensive "
                "industrialisation. Green hydrogen, produced by electrolysis powered by renewables, addresses hard-to-"
                "decarbonise sectors: heavy industry, shipping, aviation. Turkey, with abundant solar and wind resources "
                "and strategic geography, could become a regional green hydrogen hub. Circular economy principles — "
                "designing products for reuse, repair, and recycling — complement the energy transition by reducing resource "
                "extraction. The sustainable energy transition is ultimately a test of collective imagination and political "
                "courage. The technology exists; economics increasingly favour it. What remains is the will to deploy it "
                "at the speed and scale the climate crisis demands."
            ),
            "pre_reading": [
                "What renewable energy sources are used in your community?",
                "Why has the green energy transition been slower than hoped?",
                "What trade-offs might a rapid shift to renewables involve?",
            ],
            "post_reading": [
                "What evidence shows improved economics of green technology?",
                "Why does mineral extraction complicate the green narrative?",
                "Explain the 'just transition' concept.",
                "What role could green hydrogen play?",
                "Why does the author single out Turkey as a potential hub?",
                "Is the main barrier political will or technology? Argue your position.",
            ],
            "vocabulary": [
                {"word": "levelised cost", "meaning": "average cost of energy over a generating asset's lifetime", "example": "Solar's levelised cost has fallen below coal's."},
                {"word": "intermittency", "meaning": "occurring at irregular intervals", "example": "Battery storage addresses solar intermittency."},
                {"word": "photovoltaic", "meaning": "converting light into electricity", "example": "Photovoltaic panels generate household electricity."},
                {"word": "parity", "meaning": "the state of being equal", "example": "EVs are approaching cost parity with petrol cars."},
                {"word": "decarbonisation", "meaning": "reducing carbon dioxide emissions", "example": "Steel decarbonisation requires innovative technology."},
                {"word": "artisanal", "meaning": "traditional, small-scale production", "example": "Artisanal mining often lacks safety regulations."},
                {"word": "leapfrog", "meaning": "to bypass intermediate development stages", "example": "Developing nations can leapfrog landlines with mobile phones."},
                {"word": "electrolysis", "meaning": "chemical decomposition via electric current", "example": "Green hydrogen comes from electrolysis using renewables."},
                {"word": "exacerbate", "meaning": "to make worse", "example": "Poor policies can exacerbate inequality."},
                {"word": "trajectory", "meaning": "path or progression over time", "example": "Renewable cost trajectories trend consistently downward."},
                {"word": "consensus", "meaning": "general expert agreement", "example": "The scientific consensus on climate change is overwhelming."},
                {"word": "unequivocal", "meaning": "clear and unambiguous", "example": "Evidence for human-caused warming is unequivocal."},
                {"word": "combustion", "meaning": "the process of burning fuel", "example": "Internal combustion engines convert fuel to motion."},
                {"word": "hub", "meaning": "a centre of activity", "example": "Istanbul is a major trade and logistics hub."},
            ],
            "reading_strategy": "Track the balance between optimism and caution. The author presents encouraging data alongside significant obstacles — mapping this duality is key to understanding the argument.",
        },
    },
}

# ---------------------------------------------------------------------------
# 4. GRAMMAR BANK (advanced syntax, academic register)
# ---------------------------------------------------------------------------
GRAMMAR_BANK = {
    12: {
        1: {
            "topic": "Advanced Syntax Review: Cleft Sentences and Inversion",
            "explanation": (
                "Cleft sentences restructure a simple sentence to emphasise one element using 'It is/was ... that/who' or 'What ... is/was.' "
                "Inversion reverses normal subject-verb order for emphasis or after negative/restrictive adverbials. "
                "Both structures are hallmarks of formal, academic, and literary English. "
                "Cleft sentences allow writers to control information focus without adding new content. "
                "Inversion after negative adverbials such as 'Never,' 'Rarely,' and 'Not only' creates a dramatic, elevated register. "
                "Mastering these patterns is essential for C1-level writing and comprehension."
            ),
            "examples": [
                "It was the GDPR that fundamentally changed data protection in Europe.",
                "What concerns researchers most is the lack of longitudinal data.",
                "Not only did the study challenge existing assumptions, but it also proposed a new framework.",
                "Rarely have scientists encountered such a rapid mutation rate.",
                "It is through education that societies cultivate democratic values.",
                "Under no circumstances should confidential data be shared without consent.",
            ],
            "exercises": [
                {"instruction": "Rewrite each sentence as a cleft sentence beginning with 'It is/was ... that/who.'", "items": [
                    "The pandemic accelerated digital transformation globally.",
                    "Marie Curie discovered radium in 1898.",
                    "Lack of funding prevents many researchers from publishing.",
                    "The students organised the entire conference independently.",
                    "Climate change threatens biodiversity most severely in tropical regions.",
                    "Critical thinking distinguishes excellent students from average ones.",
                ]},
                {"instruction": "Rewrite using inversion after the given negative adverbial.", "items": [
                    "She had never seen such a compelling argument. (Never ...)",
                    "They not only finished early but also exceeded expectations. (Not only ...)",
                    "We rarely encounter this level of sophistication in undergraduate work. (Rarely ...)",
                    "He little realised the impact his research would have. (Little ...)",
                    "The committee had hardly announced the decision when protests erupted. (Hardly ...)",
                    "You should under no circumstances plagiarise another scholar's work. (Under no circumstances ...)",
                ]},
                {"instruction": "Rewrite as 'What' cleft sentences.", "items": [
                    "The students need more practice with academic writing.",
                    "Her meticulous methodology impressed the examiners.",
                    "The rapid spread of misinformation alarmed public health officials.",
                    "His ability to synthesise complex data sets him apart.",
                    "The committee recommended a complete restructuring of the programme.",
                    "Persistent inequality undermines democratic institutions.",
                ]},
                {"instruction": "Choose the correct form (cleft or inversion) to complete each gap.", "items": [
                    "___ (It was / What was) in 2015 ___ the Paris Agreement was signed.",
                    "___ (Never / What) before had the world faced such a coordinated lockdown.",
                    "___ (It is / Seldom) creativity that drives genuine innovation.",
                    "___ (Rarely / It was) does a single study transform an entire field.",
                    "___ (What / Not until) the researchers found surprised everyone.",
                    "___ (Not until / What) 2024 did quantum-resistant standards emerge.",
                ]},
            ],
            "tip": "In academic essays, use cleft sentences to foreground your thesis and inversion to create rhetorical impact in conclusions. Overuse diminishes the effect — reserve these structures for key arguments.",
        },
        2: {
            "topic": "Nominalization and Academic Register",
            "explanation": (
                "Nominalization converts verbs and adjectives into noun phrases, a defining feature of academic prose. "
                "'The government decided' becomes 'The governmental decision'; 'people communicate effectively' becomes 'effective communication.' "
                "This process increases information density and creates an impersonal, objective tone. "
                "However, excessive nominalization can obscure agency and reduce readability. "
                "Skilled academic writers balance nominalized constructions with active, agent-foregrounding sentences. "
                "Understanding nominalization is crucial for both producing and critically reading scholarly texts."
            ),
            "examples": [
                "'Researchers discovered the gene' -> 'The discovery of the gene by researchers...'",
                "'Students participate actively' -> 'Active student participation...'",
                "'The policy failed completely' -> 'The complete failure of the policy...'",
                "'Technology develops rapidly' -> 'The rapid development of technology...'",
                "'The committee recommended changes' -> 'The committee's recommendation for changes...'",
                "'Emissions have declined significantly' -> 'The significant decline in emissions...'",
            ],
            "exercises": [
                {"instruction": "Convert each verbal sentence into a nominalized form.", "items": [
                    "The population grew rapidly in urban areas.",
                    "Scientists analysed the data meticulously.",
                    "The government implemented new regulations swiftly.",
                    "Deforestation has accelerated alarmingly in the Amazon.",
                    "Researchers investigated the correlation between diet and disease.",
                    "The university expanded its online programmes significantly.",
                ]},
                {"instruction": "Convert each nominalized phrase back into an active sentence with a clear agent.", "items": [
                    "The implementation of stricter data protection measures...",
                    "The significant reduction in carbon emissions...",
                    "The systematic exclusion of minority voices from public discourse...",
                    "The rapid deterioration of diplomatic relations...",
                    "The establishment of an independent review panel...",
                    "The widespread adoption of remote working practices...",
                ]},
                {"instruction": "Rewrite each paragraph in a more academic register using nominalization.", "items": [
                    "People are migrating to cities because jobs are scarce in rural areas.",
                    "Students perform better when teachers give them regular feedback.",
                    "The ocean is warming, and this threatens marine ecosystems.",
                    "Countries compete fiercely, and this makes cooperation harder.",
                    "AI is transforming healthcare, and experts debate whether this is ethical.",
                    "Voters distrust politicians because they break their promises.",
                ]},
                {"instruction": "Identify the nominalization in each sentence and evaluate whether it obscures agency.", "items": [
                    "The displacement of indigenous communities was regrettable.",
                    "Implementation of the new policy led to widespread confusion.",
                    "The deterioration of air quality poses a significant health risk.",
                    "An investigation into the allegations is currently underway.",
                    "The exploitation of natural resources continues unchecked.",
                    "Considerable investment in renewable energy has been undertaken.",
                ]},
            ],
            "tip": "Use nominalization to sound academic, but always ask: 'Who did what?' If your sentence hides the agent, consider whether that concealment serves clarity or evades responsibility.",
        },
        3: {
            "topic": "Hedging and Boosting in Academic Writing",
            "explanation": (
                "Hedging involves using cautious language to qualify claims: 'may,' 'might,' 'appears to,' 'suggests that,' 'it is possible that.' "
                "Boosting involves strengthening claims with assertive language: 'clearly,' 'undoubtedly,' 'it is evident that.' "
                "Academic writing requires precise calibration of certainty — overclaiming invites critique, while excessive hedging weakens arguments. "
                "Hedging is especially important when discussing findings, predictions, and generalisations. "
                "Boosting is appropriate when evidence is overwhelming or when summarising well-established facts. "
                "The balance between hedging and boosting reflects a writer's understanding of epistemic responsibility."
            ),
            "examples": [
                "The results suggest that screen time may be associated with reduced attention spans.",
                "It appears that multilingual education could enhance cognitive flexibility.",
                "The evidence clearly demonstrates that vaccination reduces mortality.",
                "There is a strong possibility that quantum computing will disrupt cryptography.",
                "It is widely acknowledged that climate change poses an existential threat.",
                "The data tend to indicate a correlation, though causality remains unestablished.",
            ],
            "exercises": [
                {"instruction": "Add appropriate hedging language to make each claim more academically cautious.", "items": [
                    "Social media causes depression in teenagers.",
                    "Online learning is inferior to face-to-face instruction.",
                    "Artificial intelligence will replace most human jobs within a decade.",
                    "Bilingual children are more creative than monolingual children.",
                    "The new drug cures the disease in all patients.",
                    "Economic growth always leads to improved quality of life.",
                ]},
                {"instruction": "Identify whether each sentence uses hedging or boosting, and explain the effect.", "items": [
                    "The findings unequivocally support the hypothesis.",
                    "It is conceivable that alternative explanations exist.",
                    "The correlation appears to be statistically significant.",
                    "There can be no doubt that the policy has failed.",
                    "The data seem to suggest a modest improvement.",
                    "It is abundantly clear that reform is overdue.",
                ]},
                {"instruction": "Rewrite each boosted claim with hedging, and each hedged claim with boosting.", "items": [
                    "This study proves conclusively that exercise improves mental health.",
                    "There may be some evidence to suggest a link between poverty and crime.",
                    "It is indisputable that technology has transformed education.",
                    "The results might possibly indicate a slight trend.",
                    "Renewable energy is without question the future of power generation.",
                    "It could perhaps be argued that globalisation has had some benefits.",
                ]},
                {"instruction": "Write one hedged and one boosted version of each statement.", "items": [
                    "Climate change affects agricultural productivity.",
                    "Social media influences political opinions.",
                    "Early childhood education improves long-term outcomes.",
                    "Antibiotics are losing effectiveness due to overuse.",
                    "International cooperation is essential for addressing pandemics.",
                    "Digital literacy should be a core component of education.",
                ]},
            ],
            "tip": "In exam essays, hedge when you lack evidence and boost when you have strong support. A single well-placed hedge ('The evidence largely supports...') is more persuasive than absolute certainty.",
        },
        4: {
            "topic": "Complex Sentence Patterns: Conditionals and Subjunctive",
            "explanation": (
                "Advanced conditional structures go beyond the four basic types to include mixed conditionals, inverted conditionals, and implied conditions. "
                "Mixed conditionals combine time references: 'If she had studied medicine (past), she would be a doctor now (present).' "
                "Inverted conditionals omit 'if' and use inversion: 'Had I known, I would have acted differently.' "
                "The subjunctive mood, though declining in everyday English, persists in formal and academic contexts. "
                "It appears after verbs of recommendation ('insist,' 'suggest,' 'demand') and in formulaic expressions ('If I were you,' 'be that as it may'). "
                "Mastering these patterns enables nuanced expression of hypothetical, counterfactual, and formal reasoning."
            ),
            "examples": [
                "Had the committee been informed earlier, the crisis might have been averted.",
                "If she were to accept the position, she would need to relocate immediately.",
                "Were it not for international aid, the humanitarian situation would be catastrophic.",
                "Should you require further information, please do not hesitate to contact us.",
                "The board recommended that the CEO resign immediately. (subjunctive)",
                "If the experiment had been replicated, the results would now be more credible. (mixed)",
            ],
            "exercises": [
                {"instruction": "Rewrite each conditional using inversion (omitting 'if').", "items": [
                    "If I had known about the scholarship, I would have applied.",
                    "If she were the director, she would reform the entire department.",
                    "If the data should prove unreliable, the study will be retracted.",
                    "If we had invested in renewables earlier, emissions would be lower now.",
                    "If the treaty were to collapse, regional stability would be threatened.",
                    "If he had not intervened, the situation would have escalated.",
                ]},
                {"instruction": "Complete each sentence with the correct conditional or subjunctive form.", "items": [
                    "The professor insisted that each student ___ (submit) the assignment by Friday.",
                    "Were the government to ___ (increase) funding, research output would improve.",
                    "Had the warning ___ (be) issued sooner, lives could have been saved.",
                    "It is essential that the report ___ (be) completed before the deadline.",
                    "Should the experiment ___ (fail), the team will revise the methodology.",
                    "If she ___ (not study) linguistics, she would never have understood code-switching.",
                ]},
                {"instruction": "Write mixed conditionals for each situation.", "items": [
                    "He did not learn to code as a teenager. He is not a software engineer now.",
                    "They did not sign the treaty in 2015. They are still negotiating today.",
                    "She is not fluent in Mandarin. She did not get the diplomatic posting last year.",
                    "The country did not invest in education. The workforce is unskilled now.",
                    "He is naturally cautious. He did not invest in the risky venture.",
                    "The climate talks failed last year. Emissions are still rising now.",
                ]},
                {"instruction": "Identify errors in conditional/subjunctive usage and correct them.", "items": [
                    "If I would have known, I would have helped.",
                    "The committee suggested that the policy is revised.",
                    "Had he would study harder, he would have passed.",
                    "It is vital that every citizen votes in the election.",
                    "If she was the president, she would change the law.",
                    "Were the results would be significant, the paper will be published.",
                ]},
            ],
            "tip": "Inverted conditionals ('Had I known...', 'Were she to...', 'Should you need...') are powerful in formal writing. Use them in essay introductions and conclusions for a sophisticated, authoritative tone.",
        },
        5: {
            "topic": "Error Analysis and Self-Editing",
            "explanation": (
                "Error analysis is the systematic identification and classification of language errors in written or spoken production. "
                "Common error categories include: subject-verb agreement, tense consistency, article usage, preposition choice, word order, and collocational mismatch. "
                "At C1 level, errors tend to be subtle — misuse of academic collocations, register slips, or logical connectors used imprecisely. "
                "Self-editing requires reading one's own text as a critical outsider, checking for coherence, cohesion, and accuracy. "
                "Peer review adds another layer: explaining why something is wrong deepens grammatical understanding. "
                "Developing a personal error log helps learners track recurring mistakes and measure progress over time."
            ),
            "examples": [
                "Error: 'According to me...' -> Correct: 'In my opinion / I believe that...'",
                "Error: 'The research aims to proof...' -> Correct: '...aims to prove...' (verb/noun confusion)",
                "Error: 'Despite of the challenges...' -> Correct: 'Despite the challenges...'",
                "Error: 'This is an important contribute...' -> Correct: '...an important contribution...'",
                "Error: 'It can be seen that there is an increase of crime.' -> Correct: '...increase in crime.'",
                "Error: 'The results are consisted with...' -> Correct: 'The results are consistent with...'",
            ],
            "exercises": [
                {"instruction": "Find and correct the error in each sentence.", "items": [
                    "The research was conducted in order to investigate about the effects of pollution.",
                    "According to me, education is the most important factor for success.",
                    "The number of students have increased significantly over the past decade.",
                    "Despite of the government's efforts, poverty remains widespread.",
                    "This study aims to proof that bilingualism enhances cognitive ability.",
                    "The datas show a clear trend toward urbanisation.",
                ]},
                {"instruction": "Identify the error type (agreement, collocation, register, article, preposition, tense).", "items": [
                    "Each of the participants were given a questionnaire.",
                    "The results are consisted with previous findings.",
                    "We done the experiment three times to ensure accuracy.",
                    "She made a research on climate change impacts.",
                    "The report discusses about the implications of AI.",
                    "There is lots of evidences supporting this theory.",
                ]},
                {"instruction": "Edit the following paragraph for errors (there are 6 errors).", "items": [
                    "According to me, the most important contribute of this study is it's methodology.",
                    "The researches were conducted in three different countrys over a period of two years.",
                    "Despite of the limitations, the findings suggests that renewable energy is the future.",
                    "The datas collected from the survey indicates a significant increase of awareness.",
                    "Each participants were asked to complete a questionnaire about their experiences.",
                    "The committee have recommended that the policy is revised immediately.",
                ]},
                {"instruction": "Rewrite each sentence to eliminate register inconsistencies.", "items": [
                    "The results were pretty cool and showed that the drug kinda works.",
                    "This paper is gonna look at the impact of social media on politics.",
                    "A bunch of studies have found that exercise helps with depression.",
                    "The experiment totally proved our hypothesis right.",
                    "Scientists figured out that the gene is super important for brain development.",
                    "The findings are legit and backed up by tons of data.",
                ]},
            ],
            "tip": "Build a personal error log: each time you receive corrected work, record the error, the correction, and the rule. Review it before writing assignments. Patterns will emerge, and awareness is the first step to accuracy.",
        },
        6: {
            "topic": "Stylistic Variation and Rhetorical Devices",
            "explanation": (
                "Effective writers vary sentence length, structure, and rhythm to maintain reader engagement and create rhetorical effects. "
                "Short sentences create impact and urgency. Long, complex sentences develop nuance and qualification. "
                "Parallelism — repeating grammatical structures — creates rhythm, emphasis, and memorability. "
                "Antithesis juxtaposes contrasting ideas in balanced structures: 'Ask not what your country can do for you...' "
                "Tricolon groups ideas in threes for rhetorical force: 'government of the people, by the people, for the people.' "
                "Understanding these devices enables both analytical reading and powerful writing."
            ),
            "examples": [
                "Parallelism: 'She came, she saw, she conquered the committee's objections.'",
                "Antithesis: 'It was the best of times; it was the worst of times.'",
                "Tricolon: 'Life, liberty, and the pursuit of happiness.'",
                "Anaphora: 'We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields.'",
                "Asyndeton: 'He was brave, resourceful, determined.' (no conjunctions)",
                "Polysyndeton: 'He was brave and resourceful and determined and tireless.' (extra conjunctions)",
            ],
            "exercises": [
                {"instruction": "Identify the rhetorical device used in each sentence.", "items": [
                    "To err is human; to forgive, divine.",
                    "I came, I saw, I conquered.",
                    "We will not tire, we will not falter, we will not fail.",
                    "The policy was ambitious, comprehensive, transformative.",
                    "Not for glory, not for wealth, but for justice — that is why we fight.",
                    "They studied and they practised and they rehearsed and they performed.",
                ]},
                {"instruction": "Rewrite each sentence using the specified rhetorical device.", "items": [
                    "Education is important. (Use tricolon to explain why.)",
                    "The old system was slow. The new one is fast. (Use antithesis.)",
                    "She worked hard every day. (Use anaphora with three clauses.)",
                    "Climate change affects oceans and forests and cities. (Rewrite with asyndeton.)",
                    "The speech was powerful. (Use parallelism to describe its effects.)",
                    "He believed in democracy. (Use tricolon to elaborate.)",
                ]},
                {"instruction": "Vary the sentence lengths in each passage for better rhythm.", "items": [
                    "The experiment was conducted over six months. The sample included 200 participants. The results were analysed using SPSS. The findings were significant.",
                    "AI is transforming every sector of the economy and it is doing so at a pace that regulators cannot match which raises serious ethical concerns.",
                    "Privacy matters. Data protection matters. Individual rights matter. These things are not negotiable.",
                    "The novel was published in 1925. It became a classic. It is still read today. It explores the American Dream.",
                    "Multilateralism is the only viable approach to transnational challenges because no single nation can address climate change or pandemics alone.",
                    "She spoke clearly. She argued persuasively. She won the debate. Nobody was surprised.",
                ]},
                {"instruction": "Write a short paragraph (4-5 sentences) using at least three different rhetorical devices.", "items": [
                    "Topic: The importance of free speech in a democracy.",
                    "Topic: Why scientific literacy matters in the twenty-first century.",
                    "Topic: The beauty and danger of artificial intelligence.",
                    "Topic: Lessons from the COVID-19 pandemic.",
                    "Topic: The value of learning a foreign language.",
                    "Topic: Why art education should not be cut from school budgets.",
                ]},
            ],
            "tip": "Read your essays aloud. If every sentence has the same length and rhythm, the writing will sound monotonous. Alternate between short, punchy statements and longer, elaborated ones to create a dynamic reading experience.",
        },
        7: {
            "topic": "Register Shifting: Formal, Semi-Formal, and Informal",
            "explanation": (
                "Register refers to the level of formality and the vocabulary, grammar, and tone appropriate to a given context. "
                "Academic register uses nominalization, passive voice, hedging, and specialised terminology. "
                "Journalistic register employs shorter sentences, active voice, and vivid vocabulary. "
                "Informal register features contractions, phrasal verbs, colloquialisms, and first/second person. "
                "Skilled communicators shift between registers fluently, adapting their language to audience and purpose. "
                "Register awareness is tested in C1 examinations through tasks requiring transformation of texts across formality levels."
            ),
            "examples": [
                "Formal: 'The committee resolved to defer the decision pending further consultation.'",
                "Semi-formal: 'The committee decided to wait for more input before making a decision.'",
                "Informal: 'They put off deciding until they'd talked to more people.'",
                "Formal: 'It is incumbent upon all signatories to comply with the provisions herein.'",
                "Semi-formal: 'All parties who signed the agreement must follow its terms.'",
                "Informal: 'Everyone who signed up has to stick to the rules.'",
            ],
            "exercises": [
                {"instruction": "Rewrite each formal sentence in informal register.", "items": [
                    "The acquisition of language proficiency necessitates sustained engagement with authentic materials.",
                    "It is imperative that all stakeholders be consulted prior to the implementation of the revised policy.",
                    "The deterioration of bilateral relations may be attributed to a fundamental divergence of interests.",
                    "Notwithstanding the aforementioned limitations, the findings merit further investigation.",
                    "The proliferation of disinformation constitutes a grave threat to democratic governance.",
                    "One cannot overstate the significance of equitable access to healthcare.",
                ]},
                {"instruction": "Rewrite each informal sentence in academic register.", "items": [
                    "Kids who grow up poor usually don't do as well in school.",
                    "Loads of people think social media is messing up democracy.",
                    "The government messed up big time with the vaccine rollout.",
                    "You can't really trust a study with only twenty people in it.",
                    "AI is going to totally change how doctors do their jobs.",
                    "Basically, the whole system needs a complete overhaul.",
                ]},
                {"instruction": "Identify the register of each text and justify your answer.", "items": [
                    "Pursuant to Section 14(b) of the aforementioned regulation, compliance is mandatory.",
                    "The study found that regular exercise may help reduce anxiety symptoms.",
                    "Honestly, the whole thing was a bit of a disaster from start to finish.",
                    "Sources close to the minister confirmed that negotiations had stalled.",
                    "It could be argued that the current framework is no longer fit for purpose.",
                    "Like, nobody even reads the terms and conditions, do they?",
                ]},
                {"instruction": "Transform this academic paragraph into a journalistic news report and a social media post.", "items": [
                    "The longitudinal study demonstrated a statistically significant correlation between early childhood nutrition and subsequent academic attainment.",
                    "The implementation of renewable energy infrastructure has been demonstrated to yield substantial economic benefits in rural communities.",
                    "A comprehensive meta-analysis of forty-seven studies found that mindfulness-based interventions significantly reduced symptoms of anxiety and depression.",
                    "The proliferation of autonomous vehicles is anticipated to fundamentally alter urban planning paradigms within the next two decades.",
                    "Researchers at the University of Oxford have identified a novel biomarker that may facilitate early detection of neurodegenerative disorders.",
                    "The systematic review concluded that remote working arrangements had a negligible impact on overall organisational productivity.",
                ]},
            ],
            "tip": "When shifting register, change at least four elements: vocabulary (formal/informal words), grammar (passive/active), sentence length (long/short), and pronouns (third person/first-second person). Changing only one element creates an inconsistent tone.",
        },
        8: {
            "topic": "Advanced Cohesion: Substitution, Ellipsis, and Reference",
            "explanation": (
                "Cohesion refers to the linguistic devices that connect sentences and paragraphs into a unified text. "
                "Reference uses pronouns, demonstratives, and comparatives to point back (anaphoric) or forward (cataphoric) in a text. "
                "Substitution replaces a word or phrase with a pro-form: 'I prefer this theory to the one proposed earlier.' "
                "Ellipsis omits recoverable information: 'She completed the assignment on time; he didn't [complete the assignment on time].' "
                "Lexical cohesion uses repetition, synonyms, and collocations to maintain thematic continuity. "
                "Strong cohesion makes academic writing flow logically without redundancy."
            ),
            "examples": [
                "Reference: 'Zuboff coined the term. She defined it as...' (anaphoric pronoun)",
                "Cataphoric reference: 'This is what matters: evidence, not opinion.'",
                "Substitution: 'The first experiment failed; the second one succeeded.'",
                "Ellipsis: 'She can speak French and he can [speak French] too.'",
                "Lexical cohesion: 'The policy... this initiative... the programme...' (synonym chain)",
                "Comparative reference: 'The 2024 results were better than those of the previous year.'",
            ],
            "exercises": [
                {"instruction": "Identify the cohesive device (reference, substitution, ellipsis, or lexical cohesion) in each pair.", "items": [
                    "The study was conducted in 2023. It revealed significant findings.",
                    "She completed the first task; he, the second.",
                    "The policy was ambitious. This initiative, however, lacked funding.",
                    "Some students preferred online learning; others did not.",
                    "The climate crisis... this existential threat... the environmental emergency...",
                    "The early results were promising, but the later ones were not.",
                ]},
                {"instruction": "Improve cohesion in each passage using appropriate devices.", "items": [
                    "The researcher published a paper. The paper discussed climate change. Climate change is a global issue.",
                    "Students learn grammar rules. Students also learn vocabulary. Students need both grammar rules and vocabulary.",
                    "The first experiment tested hypothesis A. The second experiment tested hypothesis B. Both experiments were successful.",
                    "The government introduced a policy. The policy aimed to reduce inequality. Inequality remains a significant problem.",
                    "She studied medicine. He studied medicine. They both graduated from the same university.",
                    "The report highlighted three issues. The first issue was funding. The second issue was staffing. The third issue was infrastructure.",
                ]},
                {"instruction": "Use ellipsis to make each sentence more concise.", "items": [
                    "She can speak English fluently and he can speak English fluently too.",
                    "The first group completed the survey on time, but the second group did not complete the survey on time.",
                    "Some countries have ratified the treaty, while other countries have not ratified the treaty.",
                    "He wanted to study abroad, but his parents did not want him to study abroad.",
                    "The teacher asked the students to revise Chapter 5, but the students had already revised Chapter 5.",
                    "We could invest in solar energy or we could invest in wind energy.",
                ]},
                {"instruction": "Add cataphoric reference to create anticipation in each opening sentence.", "items": [
                    "Evidence supports climate action. (Rewrite to begin with 'This is what the evidence shows: ...')",
                    "Three factors explain the decline. (Rewrite to begin with 'What explains the decline is this: ...')",
                    "Education transforms lives. (Use cataphoric 'The following truth...')",
                    "Democracy depends on participation. (Use 'Here is the paradox: ...')",
                    "Technology creates inequality. (Use 'Consider this: ...')",
                    "Language shapes thought. (Use 'The central claim is this: ...')",
                ]},
            ],
            "tip": "After drafting an essay, highlight every pronoun and check its referent. Ambiguous reference ('This is important' — what is 'this'?) is one of the most common weaknesses in academic writing. Use 'This finding / This trend / This policy' instead.",
        },
        9: {
            "topic": "Ellipsis, Fronting, and Marked Word Order",
            "explanation": (
                "Fronting moves an element to the beginning of a sentence for emphasis or contrast: 'This theory I find unconvincing.' "
                "It is a form of marked word order — deviating from the default SVO pattern to achieve a communicative effect. "
                "Complement fronting ('Excellent she considered the proposal') is rare and highly literary. "
                "Adverbial fronting ('In no way does this undermine the argument') combines with inversion for formality. "
                "Ellipsis in conversation differs from ellipsis in academic writing; the latter must ensure recoverability. "
                "These advanced structures appear frequently in C1/C2 examinations and in sophisticated academic and literary prose."
            ),
            "examples": [
                "Fronting: 'This argument we shall examine in detail in Chapter 3.'",
                "Fronting: 'More significant than the data itself is the methodology used to collect it.'",
                "Adverbial fronting + inversion: 'Only after the intervention did the situation improve.'",
                "Ellipsis: 'The first cohort improved significantly; the second, only marginally.'",
                "Fronting: 'Gone are the days when a university degree guaranteed employment.'",
                "Marked order: 'What the researchers failed to consider was the cultural context.'",
            ],
            "exercises": [
                {"instruction": "Rewrite each sentence using fronting for emphasis.", "items": [
                    "I find this argument entirely unconvincing.",
                    "We will address the ethical implications in the final chapter.",
                    "The potential consequences of inaction are far more concerning than the costs of intervention.",
                    "The committee considered the proposal unacceptable.",
                    "We should never underestimate the power of grassroots movements.",
                    "The real challenge lies not in the technology but in its governance.",
                ]},
                {"instruction": "Complete each sentence using appropriate ellipsis.", "items": [
                    "Group A showed significant improvement; Group B ___.",
                    "She has published extensively on climate policy; he ___ on cybersecurity.",
                    "The first study was quantitative; the second, ___.",
                    "Some delegates supported the amendment; others ___.",
                    "The urban population grew by 15%; the rural, ___.",
                    "The theory explains some phenomena; however, not ___.",
                ]},
                {"instruction": "Combine fronting and inversion to create formal academic sentences.", "items": [
                    "The implications of this finding are significant. We will discuss them later.",
                    "The evidence does not support this conclusion under any circumstances.",
                    "The policy has rarely been implemented with such rigour.",
                    "We can achieve meaningful reform only through international cooperation.",
                    "Students seldom encounter such demanding material at undergraduate level.",
                    "The author acknowledges these limitations nowhere in the paper.",
                ]},
                {"instruction": "Identify whether each sentence uses fronting, ellipsis, or marked word order.", "items": [
                    "This approach the author rejects entirely.",
                    "The first experiment succeeded; the second did not.",
                    "More problematic still is the lack of a control group.",
                    "She speaks French; he, German.",
                    "Gone is the assumption that economic growth guarantees well-being.",
                    "Only through sustained effort can lasting change be achieved.",
                ]},
            ],
            "tip": "Fronting is a powerful tool for essay coherence: by moving the topic to sentence-initial position, you signal to the reader what the sentence is about before delivering the comment. Use it to create smooth paragraph transitions.",
        },
        10: {
            "topic": "Exam Preparation: Integrated Grammar Strategies",
            "explanation": (
                "C1-level grammar examinations test not isolated rules but the ability to deploy grammar flexibly in context. "
                "Key word transformation tasks require combining multiple structures: passives with modals, conditionals with clefts, reported speech with inversion. "
                "Open cloze exercises test awareness of fixed phrases, dependent prepositions, and discourse markers. "
                "Essay-level grammar assessment evaluates coherence, register consistency, and the strategic use of advanced structures. "
                "The most effective preparation combines targeted practice with extensive reading of authentic academic and journalistic texts. "
                "Review all structures covered this year — clefts, inversion, nominalization, hedging, conditionals, cohesion, register — as an integrated toolkit."
            ),
            "examples": [
                "Transformation: 'People believe he is innocent.' -> 'He is believed to be innocent.' (passive + infinitive)",
                "Transformation: 'I regret not studying harder.' -> 'If only I had studied harder.' (conditional wish)",
                "Transformation: 'The announcement surprised everyone.' -> 'What surprised everyone was the announcement.' (cleft)",
                "Transformation: 'She is too young to vote.' -> 'She is not old enough to vote.' (degree + negation)",
                "Cloze: 'The study was carried ___ over a period of three years.' (out)",
                "Cloze: '___ it not been for the quick response, the damage would have been catastrophic.' (Had)",
            ],
            "exercises": [
                {"instruction": "Complete each key word transformation using the word given (3-6 words).", "items": [
                    "'Nobody expected the results to be so dramatic.' CAME -> The results _____ a surprise to everyone.",
                    "'I wish I had attended the conference.' ONLY -> If _____ the conference.",
                    "'They say the new policy will reduce emissions.' SAID -> The new policy _____ emissions.",
                    "'She speaks so eloquently that everyone listens.' SUCH -> She is _____ everyone listens.",
                    "'Without your help, I would not have succeeded.' HAD -> _____ your help, I would not have succeeded.",
                    "'The moment she finished, the audience applauded.' SOONER -> No _____ the audience applauded.",
                ]},
                {"instruction": "Fill each gap with one appropriate word.", "items": [
                    "The study was carried ___ in three phases over a two-year period.",
                    "___ it not been for the early warning system, casualties would have been higher.",
                    "She takes ___ her mother in both appearance and temperament.",
                    "The findings are ___ line with previous research on the topic.",
                    "It remains to ___ seen whether the policy will achieve its stated objectives.",
                    "The results, ___ and large, confirmed the original hypothesis.",
                ]},
                {"instruction": "Rewrite each sentence using the structure indicated in brackets.", "items": [
                    "People think the minister will resign. (passive reporting: The minister...)",
                    "I did not realise how important the meeting was. (fronting + inversion: Little...)",
                    "The evidence convinced the jury. (cleft: It was...)",
                    "She had barely finished speaking when the fire alarm rang. (inversion: Barely...)",
                    "The research proves the theory conclusively. (hedged academic: The research appears to...)",
                    "He is very talented. Everyone admires him. (such...that: He is such...)",
                ]},
                {"instruction": "Choose the best option (A, B, C, or D) for each gap — exam-style.", "items": [
                    "_____ the evidence to suggest otherwise, the committee upheld its decision. (A) Despite (B) Although (C) Notwithstanding (D) However",
                    "Not until the final results were published _____ the full extent of the problem become clear. (A) has (B) did (C) had (D) was",
                    "The proposal, _____ merits were widely acknowledged, was nevertheless rejected. (A) which (B) that (C) whose (D) whom",
                    "_____ she to be elected, she would be the youngest prime minister in history. (A) Would (B) Were (C) Should (D) Had",
                    "The findings are _____ with those of earlier studies. (A) consistent (B) consisted (C) consisting (D) consists",
                    "It is essential that every participant _____ informed consent. (A) gives (B) give (C) gave (D) has given",
                ]},
            ],
            "tip": "In transformation tasks, identify which TWO grammar points are being tested. Most items combine structures — e.g., passive + reporting verb, conditional + inversion. Practise combining rather than isolating structures.",
        },
    },
}

# ---------------------------------------------------------------------------
# 5. CULTURE CORNER BANK
# ---------------------------------------------------------------------------
CULTURE_CORNER_BANK = {
    12: {
        1: {
            "title": "The Oxford Tutorial System",
            "country": "United Kingdom",
            "text": (
                "The University of Oxford has employed the tutorial system for over seven hundred years, making it one of the "
                "oldest and most distinctive pedagogical models in higher education. In a typical tutorial, one or two students "
                "meet weekly with a tutor — a leading academic in their field — to discuss an essay the student has written. "
                "The tutor challenges arguments, probes assumptions, and pushes the student to defend or revise their position. "
                "This Socratic method develops critical thinking, intellectual independence, and the ability to construct and "
                "deconstruct arguments under pressure. Critics note the system's resource intensity and its historical association "
                "with privilege, but proponents argue that it remains the gold standard for deep learning. Many Oxford graduates "
                "credit the tutorial system with shaping their ability to think rigorously and communicate persuasively."
            ),
            "did_you_know": "Each Oxford student writes an average of one essay per week during term — approximately sixty essays across a three-year degree.",
            "compare_question": "How does the tutorial system compare with the lecture-based model used in most Turkish universities? Which do you think produces more independent thinkers?",
        },
        2: {
            "title": "The French Dissertation Tradition",
            "country": "France",
            "text": (
                "In France, the dissertation is not merely an academic exercise but a cultural institution. From secondary school "
                "through the grandes ecoles, students are trained in the rigorous three-part structure: these, antithese, synthese "
                "(thesis, antithesis, synthesis). This dialectical approach requires writers to present an argument, systematically "
                "dismantle it with counter-arguments, and then arrive at a nuanced synthesis that transcends both positions. "
                "The baccalaureat philosophy exam, taken by all final-year lycee students, epitomises this tradition: candidates "
                "must compose a four-hour essay on abstract questions such as 'Is freedom possible without law?' The emphasis on "
                "structured argumentation permeates French intellectual life, from political debate to literary criticism. Critics "
                "argue the format can be formulaic, but defenders maintain it instils disciplined thinking and a respect for "
                "intellectual complexity that serves graduates throughout their careers."
            ),
            "did_you_know": "The baccalaureat philosophy exam has been a requirement for all French students since 1808, regardless of their intended field of study.",
            "compare_question": "How does the French dissertation structure compare with the five-paragraph essay commonly taught in English-speaking countries? Which approach better prepares students for complex argumentation?",
        },
        3: {
            "title": "Estonia's Digital Society",
            "country": "Estonia",
            "text": (
                "Estonia has earned the nickname 'e-Estonia' for its pioneering approach to digital governance. Since declaring "
                "internet access a human right in 2000, the country has built a comprehensive digital infrastructure that allows "
                "citizens to vote, file taxes, access medical records, and sign contracts online using a secure digital identity. "
                "The X-Road platform connects all government databases while maintaining strict data privacy through blockchain-"
                "verified access logs. Citizens can see exactly who has accessed their data and challenge any unauthorised access. "
                "Estonia's approach to cybersecurity education begins in primary school, where coding and digital literacy are "
                "mandatory subjects. The country's experience offers a model for balancing digital convenience with robust privacy "
                "protections — a challenge that larger nations continue to struggle with."
            ),
            "did_you_know": "Estonia's e-Residency programme allows anyone in the world to establish and manage an EU-based company entirely online, without ever visiting the country.",
            "compare_question": "What lessons could Turkey learn from Estonia's digital governance model? What challenges might arise in scaling such a system to a country with a much larger population?",
        },
        4: {
            "title": "Iceland's Linguistic Purism",
            "country": "Iceland",
            "text": (
                "Iceland takes a unique approach to language preservation. Rather than borrowing foreign terms for new concepts, "
                "the Icelandic Language Committee coins native equivalents using Old Norse roots. 'Computer' became 'tolva' "
                "(a blend of 'tala,' meaning number, and 'volva,' meaning prophetess), and 'telephone' became 'simi' (from the "
                "Old Norse word for thread). This linguistic purism ensures that modern Icelanders can still read the medieval "
                "sagas with relative ease — a connection to their literary heritage that few other nations can claim. The policy "
                "reflects a broader cultural commitment to linguistic identity in the face of English-language globalisation. "
                "Critics argue that purism can impede international communication, but supporters contend that it enriches the "
                "language by forcing creative word formation rather than passive borrowing."
            ),
            "did_you_know": "Icelandic has changed so little over the centuries that schoolchildren can read manuscripts from the thirteenth century without specialised training.",
            "compare_question": "Turkey underwent a major language reform in the 1930s, replacing many Arabic and Persian loanwords with Turkish equivalents. How does this compare with Iceland's approach? What are the cultural implications of such reforms?",
        },
        5: {
            "title": "Colombia's Literary Legacy",
            "country": "Colombia",
            "text": (
                "Colombia's literary tradition, though often overshadowed by its troubled political history, is one of Latin "
                "America's richest. Gabriel Garcia Marquez, who won the Nobel Prize in 1982, put Colombian literature on the "
                "world map with his masterpiece 'One Hundred Years of Solitude,' a novel that blends magical realism with the "
                "historical traumas of a fictional town. Marquez's influence extends beyond literature: his narrative techniques "
                "have shaped journalism, film, and political discourse across the Spanish-speaking world. Today, Colombia's "
                "literary scene is vibrant, with authors like Juan Gabriel Vasquez and Piedad Bonnett exploring violence, memory, "
                "and reconciliation. The annual Hay Festival in Cartagena attracts writers from around the globe, cementing "
                "Colombia's reputation as a country where storytelling is not merely entertainment but a means of processing "
                "collective trauma and imagining alternative futures."
            ),
            "did_you_know": "Garcia Marquez originally trained as a journalist and considered journalism and fiction to be complementary forms of truth-telling.",
            "compare_question": "How does magical realism as a literary style compare with the realist tradition in Turkish literature represented by writers like Yasar Kemal? Can fiction convey truths that journalism cannot?",
        },
        6: {
            "title": "Switzerland's Multilingual Governance",
            "country": "Switzerland",
            "text": (
                "Switzerland operates with four official languages — German, French, Italian, and Romansh — a multilingual "
                "arrangement that shapes its political institutions, education system, and national identity. The principle of "
                "territoriality means that each canton determines its official language, but the federal government communicates "
                "in all four. Parliamentary debates are conducted in whichever language a speaker chooses, with simultaneous "
                "interpretation available. This linguistic pluralism is enshrined in the constitution and reflects a deep "
                "commitment to cultural coexistence. Schools in German-speaking regions teach French from an early age, and "
                "vice versa. Critics note that English is increasingly displacing the smaller official languages in business "
                "and academia, but Switzerland's model demonstrates that multilingualism can be a source of national cohesion "
                "rather than division."
            ),
            "did_you_know": "Romansh, spoken by fewer than 40,000 people, was recognised as a national language in 1938 partly as a symbolic rejection of Italian fascism's linguistic imperialism.",
            "compare_question": "How does Switzerland's approach to multilingualism compare with Turkey's language policies? What advantages and challenges does official multilingualism bring?",
        },
        7: {
            "title": "China's Quantum Ambitions",
            "country": "China",
            "text": (
                "China has invested heavily in quantum technology, viewing it as a strategic priority for the twenty-first century. "
                "In 2016, China launched Micius, the world's first quantum communications satellite, enabling quantum key "
                "distribution over distances exceeding one thousand kilometres. The Hefei National Laboratory for Physical Sciences "
                "at the Microscale houses one of the world's most advanced quantum computing research centres, where scientists "
                "achieved quantum supremacy in 2020 using a photonic system. China's national strategy integrates quantum research "
                "into its broader technological ambitions, including artificial intelligence, advanced manufacturing, and secure "
                "communications. The geopolitical implications are significant: whoever masters quantum computing first may gain "
                "decisive advantages in intelligence, cryptography, and economic competitiveness. International collaboration "
                "remains limited due to security concerns, raising questions about whether quantum technology will unite or further "
                "divide the global scientific community."
            ),
            "did_you_know": "China's quantum communication network, spanning over 4,600 kilometres from Beijing to Shanghai, is the longest in the world and is used for secure government and financial communications.",
            "compare_question": "How should smaller nations like Turkey position themselves in the quantum technology race? Is collaboration or independent development the better strategy?",
        },
        8: {
            "title": "Japan's Living National Treasures",
            "country": "Japan",
            "text": (
                "Since 1950, Japan has designated exceptional practitioners of traditional arts as 'Living National Treasures' — "
                "individuals whose mastery of crafts such as pottery, metalwork, textile dyeing, and performing arts like Noh "
                "and Kabuki is deemed irreplaceable. The programme, formally known as Holders of Important Intangible Cultural "
                "Properties, provides financial support to enable these masters to continue practising and, crucially, to train "
                "apprentices. This policy reflects a philosophy that cultural heritage resides not only in objects and monuments "
                "but in living human skills and knowledge. The designation carries enormous prestige and has inspired similar "
                "programmes in South Korea, France, and the Philippines. Critics argue that it can freeze traditions rather than "
                "allowing them to evolve, but proponents insist that preservation and innovation are not mutually exclusive."
            ),
            "did_you_know": "As of 2024, only about 100 individuals hold the Living National Treasure designation at any given time, across all artistic disciplines.",
            "compare_question": "Turkey has its own tradition of master craftspeople, particularly in calligraphy, tile-making, and marbling (ebru). Should Turkey adopt a formal 'Living National Treasure' programme? What benefits and risks might it bring?",
        },
        9: {
            "title": "Rwanda's Community Health Worker Model",
            "country": "Rwanda",
            "text": (
                "Rwanda has achieved remarkable health outcomes despite limited resources, largely through its innovative community "
                "health worker programme. Over 45,000 trained volunteers — three per village — serve as the first point of contact "
                "for basic healthcare, providing treatment for malaria, pneumonia, and diarrhoea, and referring complex cases to "
                "clinics. The programme has been credited with reducing child mortality by over sixty per cent since 2000. "
                "Community health workers also play a vital role in health education, family planning, and disease surveillance. "
                "Rwanda's model has attracted international attention because it demonstrates that health system strengthening "
                "need not wait for expensive infrastructure; it can begin with trained, trusted community members. The WHO has "
                "cited Rwanda's approach as a model for other low-income countries seeking to achieve universal health coverage."
            ),
            "did_you_know": "Rwanda mandates community-based health insurance (Mutuelles de Sante), covering over 90% of the population — one of the highest rates in Africa.",
            "compare_question": "How could elements of Rwanda's community health model be adapted for rural areas in Turkey? What cultural and structural differences would need to be considered?",
        },
        10: {
            "title": "Denmark's Wind Energy Revolution",
            "country": "Denmark",
            "text": (
                "Denmark is a global leader in wind energy, generating over fifty per cent of its electricity from wind turbines "
                "as of 2024. The country's commitment to renewable energy began in the 1970s, spurred by the oil crisis and a "
                "strong grassroots movement that demanded energy independence. Danish company Vestas is the world's largest wind "
                "turbine manufacturer, and the country's expertise in offshore wind technology has been exported globally. "
                "Denmark's success is built on a combination of political will, public investment, and community ownership — many "
                "wind farms are partly owned by local cooperatives, ensuring that communities benefit directly from the energy "
                "transition. The government aims to reach net-zero emissions by 2045, with plans for energy islands that will "
                "serve as hubs for offshore wind production. Denmark's experience demonstrates that a small nation can lead a "
                "global energy transformation when policy, technology, and public engagement align."
            ),
            "did_you_know": "Denmark's largest energy island, planned for the North Sea, will initially produce 3 GW of offshore wind power — enough to supply three million European households.",
            "compare_question": "Turkey has significant wind energy potential, particularly in the Aegean and Marmara regions. What lessons from Denmark's experience could accelerate Turkey's wind energy development?",
        },
    },
}

# ---------------------------------------------------------------------------
# 6. FUN FACTS BANK
# ---------------------------------------------------------------------------
FUN_FACTS_BANK = {
    12: {
        1: {
            "facts": [
                "The oldest known university, the University of al-Qarawiyyin in Fez, Morocco, was founded in 859 CE by a woman, Fatima al-Fihri.",
                "A study by MIT found that false news stories spread six times faster on Twitter than true ones.",
                "The average university student in Finland reads approximately 40 academic articles per semester.",
            ],
            "source_hint": "UNESCO, MIT Media Lab, Finnish Ministry of Education",
        },
        2: {
            "facts": [
                "George Orwell's '1984' sees a spike in sales every time a government surveillance scandal breaks in the news.",
                "The word 'rhetoric' comes from the Greek 'rhetor,' meaning public speaker — in ancient Athens, rhetoric was considered as important as mathematics.",
                "A 2023 study found that people spend an average of only 15 seconds evaluating the credibility of a news article before sharing it.",
            ],
            "source_hint": "Publisher sales data, Classical studies, Reuters Institute",
        },
        3: {
            "facts": [
                "The first computer virus, 'Creeper,' was created in 1971 and simply displayed the message: 'I'm the creeper, catch me if you can!'",
                "Cybercrime costs the global economy over $8 trillion annually — more than the GDP of Japan.",
                "The average person has over 100 online accounts but uses only 5-7 unique passwords across all of them.",
            ],
            "source_hint": "Computer History Museum, Cybersecurity Ventures, NordPass",
        },
        4: {
            "facts": [
                "Shakespeare invented over 1,700 words that are still used in English today, including 'assassination,' 'lonely,' and 'generous.'",
                "The longest sentence in English literature appears in Jonathan Coe's novel 'The Rotters' Club' — it contains 13,955 words.",
                "The English language has approximately 170,000 words in current use, but the average adult uses only about 20,000-35,000.",
            ],
            "source_hint": "Oxford English Dictionary, Guinness World Records, Cambridge Language Research",
        },
        5: {
            "facts": [
                "Bob Dylan is the only musician to have won the Nobel Prize in Literature (2016), sparking heated debate about the definition of 'literature.'",
                "Orhan Pamuk's 'Museum of Innocence' in Istanbul is both a novel and an actual museum — visitors can see the objects described in the book.",
                "The Nobel Prize medal for Literature weighs approximately 175 grams and is made of 18-carat green gold plated with 24-carat gold.",
            ],
            "source_hint": "Nobel Foundation, Museum of Innocence Istanbul, Swedish Mint",
        },
        6: {
            "facts": [
                "The United Nations has six official languages: Arabic, Chinese, English, French, Russian, and Spanish — but most informal negotiations happen in English and French.",
                "The Treaty of Versailles (1919) was the first major international treaty to be written in English as well as French, breaking France's diplomatic language monopoly.",
                "There are currently 193 UN member states, but over 200 entities have applied for membership that was not granted.",
            ],
            "source_hint": "United Nations, Diplomatic history archives, UN General Assembly records",
        },
        7: {
            "facts": [
                "A quantum computer's qubit can process exponentially more information than a classical bit — a 300-qubit machine could theoretically represent more states than there are atoms in the observable universe.",
                "Google's quantum processor 'Sycamore' completed a calculation in 200 seconds that would take the fastest classical supercomputer 10,000 years.",
                "The operating temperature of most quantum computers is about 15 millikelvin — colder than outer space.",
            ],
            "source_hint": "Nature journal, Google AI blog, IBM Research",
        },
        8: {
            "facts": [
                "Picasso's 'Guernica' is 3.49 metres tall and 7.76 metres wide — roughly the size of a small apartment wall.",
                "The art market generated over $65 billion in global sales in 2023, with digital art and NFTs accounting for approximately 5%.",
                "The Mona Lisa has its own mailbox at the Louvre because of the volume of love letters it receives from admirers.",
            ],
            "source_hint": "Museo Reina Sofia, Art Basel report, Louvre Museum archives",
        },
        9: {
            "facts": [
                "The 1918 influenza pandemic infected approximately one-third of the world's population and killed an estimated 50-100 million people.",
                "Smallpox is the only human disease to have been completely eradicated — the last natural case occurred in Somalia in 1977.",
                "Antimicrobial resistance already causes over 1.2 million deaths annually and is projected to cause 10 million by 2050 if unaddressed.",
            ],
            "source_hint": "CDC, WHO, The Lancet",
        },
        10: {
            "facts": [
                "If all the solar energy hitting Earth's surface for one hour could be captured, it would meet global energy demand for an entire year.",
                "Denmark produced 55.9% of its electricity from wind power in 2023 — the highest proportion of any country.",
                "Turkey's solar energy potential is among the highest in Europe, with an average of 2,640 hours of sunshine per year.",
            ],
            "source_hint": "US Department of Energy, Danish Energy Agency, Turkish Ministry of Energy",
        },
    },
}

# ---------------------------------------------------------------------------
# 7. PROJECT BANK
# ---------------------------------------------------------------------------
PROJECT_BANK = {
    12: {
        1: {
            "title": "University Readiness Portfolio",
            "goal": "Create a comprehensive portfolio demonstrating university-level academic skills.",
            "steps": [
                "Write a statement of purpose (500 words) for a university application in your field of interest.",
                "Compile an annotated bibliography of ten academic sources on a topic of your choice.",
                "Draft a research proposal (300 words) outlining a question, methodology, and expected outcomes.",
                "Record a three-minute academic presentation summarising your proposal.",
                "Peer-review two classmates' portfolios using a structured rubric.",
            ],
            "materials": ["Word processor", "Academic databases (Google Scholar, JSTOR)", "Presentation software", "Peer review rubric"],
            "outcome": "A polished portfolio showcasing academic writing, research, and presentation skills suitable for university applications.",
        },
        2: {
            "title": "Rhetoric in Action: Media Analysis Report",
            "goal": "Analyse the rhetorical strategies used in a current media campaign.",
            "steps": [
                "Select a media campaign (political, commercial, or social) and collect at least five primary sources.",
                "Identify examples of ethos, pathos, and logos in each source.",
                "Analyse the target audience and the campaign's intended versus actual effects.",
                "Write a 1,000-word analytical report with evidence and academic references.",
                "Present your findings in a class seminar with visual aids.",
            ],
            "materials": ["Media sources (print, digital, video)", "Rhetorical analysis framework", "Presentation software", "Academic citation guide"],
            "outcome": "A researched, well-argued media analysis report demonstrating critical literacy and rhetorical awareness.",
        },
        3: {
            "title": "Cybersecurity Awareness Campaign",
            "goal": "Design and implement a school-wide cybersecurity awareness initiative.",
            "steps": [
                "Research the top five cybersecurity threats facing young people today.",
                "Design infographics, short videos, or interactive quizzes for each threat.",
                "Organise a workshop or assembly presentation for younger students.",
                "Create a 'Digital Safety Pledge' for students to sign.",
                "Evaluate the campaign's impact through a pre- and post-survey.",
            ],
            "materials": ["Graphic design tools (Canva, Adobe)", "Survey platform", "Presentation equipment", "Cybersecurity resources (NCSC, CISA)"],
            "outcome": "A measurable awareness campaign that educates peers about cybersecurity risks and protective behaviours.",
        },
        4: {
            "title": "Language Evolution Documentary",
            "goal": "Produce a short documentary exploring how English syntax has changed over time.",
            "steps": [
                "Research three major periods of English syntactic change (Old, Middle, Modern).",
                "Interview an English teacher or linguist about current language change.",
                "Script a ten-minute documentary with narration, visuals, and examples.",
                "Film and edit the documentary using available technology.",
                "Screen the documentary for the class and lead a discussion on language change.",
            ],
            "materials": ["Camera or smartphone", "Video editing software", "Historical language resources", "Interview recording equipment"],
            "outcome": "A polished short documentary that makes linguistic history accessible and engaging for a general audience.",
        },
        5: {
            "title": "Nobel Literature Reading Circle",
            "goal": "Organise a structured reading circle focusing on works by Nobel laureates.",
            "steps": [
                "Select three Nobel Prize-winning novels or short story collections from different regions.",
                "Create a reading schedule with weekly discussion questions for each text.",
                "Lead weekly discussions using Socratic seminar techniques.",
                "Write a comparative essay (800 words) connecting themes across the three works.",
                "Present a 'Reader's Guide' poster for the school library recommending Nobel literature.",
            ],
            "materials": ["Selected novels", "Discussion question templates", "Essay writing guide", "Poster materials"],
            "outcome": "Deeper engagement with world literature and improved skills in comparative literary analysis and discussion facilitation.",
        },
        6: {
            "title": "Model United Nations Position Paper",
            "goal": "Research, write, and defend a position paper on a current international issue.",
            "steps": [
                "Choose a country and an international issue (e.g., climate migration, digital governance).",
                "Research your assigned country's official position using government and UN sources.",
                "Write a formal position paper (800 words) following MUN format and conventions.",
                "Prepare a three-minute opening speech for a simulated committee session.",
                "Participate in a class-level MUN debate, practising negotiation and amendment drafting.",
            ],
            "materials": ["UN documentation databases", "MUN position paper template", "Country profile resources", "Formal debate timer"],
            "outcome": "A polished position paper and demonstrated ability to engage in formal diplomatic discourse and negotiation.",
        },
        7: {
            "title": "Quantum Computing Explainer Series",
            "goal": "Create an accessible explainer series that demystifies quantum computing for non-specialists.",
            "steps": [
                "Research five key quantum computing concepts (qubit, superposition, entanglement, decoherence, quantum supremacy).",
                "Design an infographic or animated video for each concept using analogies and visuals.",
                "Test your explainers on non-specialist classmates and gather feedback.",
                "Revise based on feedback to improve clarity and accuracy.",
                "Publish the series on the school website or social media channels.",
            ],
            "materials": ["Animation software (Powtoon, Canva)", "Physics textbooks and online resources", "Feedback survey", "School website access"],
            "outcome": "A five-part explainer series that makes quantum computing concepts understandable to a general audience.",
        },
        8: {
            "title": "Art as Activism Exhibition",
            "goal": "Curate a class exhibition exploring how visual art addresses social and political issues.",
            "steps": [
                "Research five artists (historical and contemporary) who use art for social commentary.",
                "Create an original artwork responding to a current social issue.",
                "Write a 200-word artist statement explaining your work's message and methods.",
                "Design the exhibition layout, including labels, lighting plan, and visitor guide.",
                "Host an opening event with guided tours and a Q&A session.",
            ],
            "materials": ["Art supplies (varied media)", "Exhibition space", "Printing for labels and guide", "Lighting equipment"],
            "outcome": "A curated exhibition demonstrating understanding of art's social function and the ability to communicate ideas through visual media.",
        },
        9: {
            "title": "Global Health Policy Brief",
            "goal": "Write a professional-quality policy brief recommending action on a global health challenge.",
            "steps": [
                "Select a global health issue (antimicrobial resistance, vaccine equity, mental health, NCD prevention).",
                "Conduct a literature review using WHO reports, journal articles, and news sources.",
                "Write a two-page policy brief with executive summary, background, analysis, and recommendations.",
                "Design a one-page infographic summarising your key findings.",
                "Present the brief to classmates acting as a health ministry advisory panel.",
            ],
            "materials": ["Academic databases", "Policy brief template", "Infographic design tool", "Presentation equipment"],
            "outcome": "A concise, evidence-based policy brief demonstrating analytical writing and the ability to translate research into actionable recommendations.",
        },
        10: {
            "title": "Green Technology Innovation Pitch",
            "goal": "Develop and pitch a green technology solution to a real environmental problem.",
            "steps": [
                "Identify an environmental problem in your community (waste, energy, water, transport).",
                "Research existing green technology solutions and identify gaps or improvement opportunities.",
                "Design a feasible solution, including technical description, cost estimate, and environmental impact.",
                "Create a pitch deck (10 slides) following startup presentation conventions.",
                "Deliver a five-minute pitch to a panel of teachers and classmates acting as investors.",
            ],
            "materials": ["Research databases", "Pitch deck template", "Cost estimation tools", "Presentation software"],
            "outcome": "A compelling innovation pitch demonstrating understanding of green technology, entrepreneurial thinking, and persuasive communication.",
        },
    },
}

# ---------------------------------------------------------------------------
# 8. PROGRESS CHECK BANK
# ---------------------------------------------------------------------------
PROGRESS_CHECK_BANK = {
    12: {
        1: {
            "can_do": [
                "I can understand and discuss university-level academic texts.",
                "I can write a well-structured statement of purpose.",
                "I can identify and evaluate pedagogical approaches in higher education.",
                "I can use cleft sentences and inversion for emphasis in writing.",
                "I can discuss the advantages and limitations of online learning models.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "Which academic skill do you most need to develop before university? What steps will you take this term?",
        },
        2: {
            "can_do": [
                "I can analyse rhetorical strategies (ethos, pathos, logos) in media texts.",
                "I can write a 1,000-word analytical essay with evidence and references.",
                "I can use nominalization to shift register toward academic prose.",
                "I can identify propaganda techniques in advertising and political communication.",
                "I can evaluate the credibility and bias of digital information sources.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "How has your ability to analyse persuasive language changed this unit? Give a specific example.",
        },
        3: {
            "can_do": [
                "I can explain key cybersecurity concepts (encryption, phishing, zero-day vulnerabilities).",
                "I can discuss the ethical dimensions of digital privacy and surveillance.",
                "I can use hedging and boosting appropriately in academic writing.",
                "I can evaluate data protection policies and their effectiveness.",
                "I can design a cybersecurity awareness resource for a general audience.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "Has this unit changed how you manage your own digital privacy? What specific actions have you taken?",
        },
        4: {
            "can_do": [
                "I can identify and use advanced conditional structures, including mixed and inverted forms.",
                "I can shift register fluently between formal, semi-formal, and informal English.",
                "I can analyse the syntactic evolution of English across historical periods.",
                "I can use the subjunctive mood correctly in formal contexts.",
                "I can rewrite texts in different registers while maintaining meaning.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "Which advanced grammatical structure do you find most challenging? What strategy will you use to master it?",
        },
        5: {
            "can_do": [
                "I can analyse narrative techniques in Nobel Prize-winning literature.",
                "I can write a comparative literary essay with textual evidence.",
                "I can use stylistic variation and rhetorical devices in my own writing.",
                "I can discuss the social and political functions of literature.",
                "I can evaluate the Nobel Prize's role in shaping the literary canon.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "Which Nobel laureate's work resonated with you most? How did it change your understanding of literature's purpose?",
        },
        6: {
            "can_do": [
                "I can discuss current issues in international relations using appropriate terminology.",
                "I can write a formal position paper following diplomatic conventions.",
                "I can use modal verbs strategically for hedging in diplomatic discourse.",
                "I can analyse the strengths and weaknesses of multilateral institutions.",
                "I can participate effectively in a structured debate or Model UN simulation.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "How has studying international relations changed your perspective on global events? Give a specific example.",
        },
        7: {
            "can_do": [
                "I can explain basic quantum computing concepts using appropriate analogies.",
                "I can discuss the potential applications and risks of quantum technology.",
                "I can use advanced cohesion devices (substitution, ellipsis, reference) effectively.",
                "I can evaluate scientific claims for accuracy and appropriate hedging.",
                "I can create an accessible explanation of a complex scientific concept.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "What was the most challenging concept to understand in this unit? How did you overcome that challenge?",
        },
        8: {
            "can_do": [
                "I can analyse visual artworks as forms of social and political commentary.",
                "I can write an artist statement and exhibition catalogue entry.",
                "I can use fronting and marked word order for emphasis in academic writing.",
                "I can discuss the relationship between aesthetics and politics.",
                "I can curate and present a themed exhibition with supporting text.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "How has this unit changed the way you look at visual art? Can you now 'read' an artwork critically?",
        },
        9: {
            "can_do": [
                "I can discuss global health challenges using epidemiological terminology.",
                "I can write a policy brief with evidence-based recommendations.",
                "I can use integrated grammar strategies for exam-level writing tasks.",
                "I can evaluate the effectiveness of international health governance.",
                "I can design a public health communication resource.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "If you could advise the WHO on one priority, what would it be and why?",
        },
        10: {
            "can_do": [
                "I can discuss the sustainable energy transition using technical and economic vocabulary.",
                "I can write and deliver a persuasive pitch for a green technology solution.",
                "I can deploy all advanced grammar structures learned this year in integrated tasks.",
                "I can evaluate environmental claims for scientific accuracy and rhetorical strategy.",
                "I can reflect on my overall language development and set goals for future learning.",
            ],
            "self_rate_labels": ["Not yet", "With support", "Independently", "Confidently", "I can teach this"],
            "reflection_prompt": "Looking back at the entire year, which skill has grown the most? What will you continue to develop after graduation?",
        },
    },
}

# ---------------------------------------------------------------------------
# 9. LISTENING SCRIPT BANK (14-16 sentences each)
# ---------------------------------------------------------------------------
LISTENING_SCRIPT_BANK = {
    12: {
        1: {
            "title": "A University Open Day",
            "script": (
                "Welcome, everyone, to the Faculty of Social Sciences Open Day. "
                "My name is Dr. Kaya, and I coordinate admissions for this faculty. "
                "Today you will have the opportunity to attend taster lectures, tour our research centres, and speak with current students. "
                "Our faculty offers twelve undergraduate programmes, ranging from Political Science to Data Analytics. "
                "What distinguishes us from other universities is our commitment to interdisciplinary learning. "
                "Every student completes a capstone project in their final year that integrates at least two disciplines. "
                "Last year, one student combined neuroscience and economics to study decision-making under uncertainty. "
                "We also have partnerships with over forty universities worldwide for exchange programmes. "
                "Scholarships are available for students who demonstrate both academic excellence and community engagement. "
                "The application deadline is the fifteenth of June, and interviews take place in July. "
                "I strongly recommend that you attend at least two taster lectures today to get a feel for our teaching style. "
                "Professor Aksoy's lecture on the psychology of persuasion begins in twenty minutes in Room 204. "
                "After that, our student ambassadors will be available in the main hall for informal Q&A sessions. "
                "Please pick up an information pack from the table by the entrance before you leave. "
                "We look forward to welcoming some of you as students next year."
            ),
            "tasks": [
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": [
                    "How many undergraduate programmes does the faculty offer? (A) 10 (B) 12 (C) 14 (D) 16",
                    "What must every final-year student complete? (A) An internship (B) A capstone project (C) A language exam (D) A thesis defence",
                    "When is the application deadline? (A) May 15 (B) June 15 (C) July 15 (D) August 15",
                    "Where is Professor Aksoy's lecture? (A) Main hall (B) Room 104 (C) Room 204 (D) Auditorium",
                    "What kind of scholarships are available? (A) Athletic (B) Need-based only (C) Academic and community (D) Research only",
                    "How many international partnerships does the faculty have? (A) 20 (B) 30 (C) 40+ (D) 50+",
                ]},
                {"type": "gap_fill", "instruction": "Complete each sentence with a word or phrase from the listening.", "items": [
                    "The faculty is distinguished by its commitment to ___ learning.",
                    "Last year, a student combined ___ and economics for their project.",
                    "Scholarships require both academic excellence and ___ engagement.",
                    "Student ___ will be available in the main hall.",
                    "Visitors should pick up an ___ pack from the entrance table.",
                    "Interviews for admitted candidates take place in ___.",
                ]},
            ],
        },
        2: {
            "title": "A Podcast on Media Literacy",
            "script": (
                "Hello and welcome to 'Think Twice,' the podcast about navigating information in the digital age. "
                "I'm your host, Maya Chen, and today we're discussing why media literacy should be considered a fundamental civic skill. "
                "My guest is Professor Lars Eriksson from the University of Helsinki, where media literacy has been part of the national curriculum since 2016. "
                "Professor Eriksson, what exactly do you mean by media literacy? "
                "Well, Maya, media literacy is the ability to access, analyse, evaluate, and create media in various forms. "
                "It goes beyond simply checking facts — it involves understanding how media messages are constructed and for what purpose. "
                "In Finland, we start teaching these skills in primary school, using age-appropriate methods. "
                "By the time students reach secondary school, they can identify logical fallacies, recognise emotional manipulation, and trace the ownership structures behind media outlets. "
                "That sounds impressive, but critics argue that media literacy education can be politicised. "
                "That is a valid concern. Our approach is strictly methodological — we teach the tools of analysis, not what conclusions to draw. "
                "The goal is to produce critical thinkers, not to push any particular ideology. "
                "Studies show that Finnish students outperform their European peers by a significant margin in identifying misleading headlines. "
                "For countries looking to implement similar programmes, what would your top recommendation be? "
                "Start with teacher training. You cannot teach critical thinking if teachers themselves have not been trained in it. "
                "Thank you, Professor. Listeners, you can find resources and links in our show notes."
            ),
            "tasks": [
                {"type": "true_false", "instruction": "Write True or False for each statement.", "items": [
                    "Media literacy has been in the Finnish curriculum since 2006.",
                    "Professor Eriksson defines media literacy as only fact-checking.",
                    "Finnish students start learning media literacy in primary school.",
                    "The Finnish approach focuses on teaching methodology, not ideology.",
                    "Finnish students are average compared to European peers in spotting misleading headlines.",
                    "Professor Eriksson's top recommendation for other countries is to invest in teacher training.",
                ]},
                {"type": "short_answer", "instruction": "Answer each question in one or two sentences.", "items": [
                    "According to Professor Eriksson, what four abilities does media literacy involve?",
                    "What can Finnish secondary school students do as a result of media literacy education?",
                    "How does the Finnish approach respond to concerns about politicisation?",
                    "Why does the professor emphasise teacher training as a priority?",
                    "What type of programme is 'Think Twice'?",
                    "Name one skill beyond fact-checking that media literacy involves.",
                ]},
            ],
        },
        3: {
            "title": "A Panel Discussion on Digital Privacy",
            "script": (
                "Good evening, everyone. Welcome to tonight's panel: 'Who Owns Your Data?' "
                "I'm Dr. Aslan, and joining me are three experts. "
                "First, let me introduce Ms. Bergman, a data protection lawyer from Brussels. "
                "Next, we have Mr. Tanaka, a cybersecurity engineer from Tokyo. "
                "And finally, Dr. Okafor, a digital rights researcher from Lagos. "
                "Ms. Bergman, the GDPR has been in effect since 2018. Has it been effective? "
                "The GDPR established important principles, but enforcement has been uneven. "
                "Large tech companies still find ways to circumvent the spirit of the law through complex consent interfaces. "
                "Mr. Tanaka, from a technical perspective, is true data privacy even possible? "
                "It is technically achievable through strong encryption and decentralised architectures, but it requires trade-offs in convenience. "
                "Most users are unwilling to sacrifice usability for privacy, which companies exploit. "
                "Dr. Okafor, what about the developing world? "
                "In many African countries, data protection legislation is either absent or poorly enforced. "
                "Yet digital adoption is accelerating faster than regulatory frameworks can keep up. "
                "The risk is a new form of digital colonialism, where data from the Global South enriches corporations in the Global North. "
                "Thank you all. The key takeaway seems to be that privacy is not merely a technical problem but a political and economic one."
            ),
            "tasks": [
                {"type": "matching", "instruction": "Match each panellist with their field and key argument.", "items": [
                    "Ms. Bergman — Field: ___ — Key point: ___",
                    "Mr. Tanaka — Field: ___ — Key point: ___",
                    "Dr. Okafor — Field: ___ — Key point: ___",
                    "The moderator summarises privacy as a ___, ___, and ___ problem.",
                    "According to Mr. Tanaka, users are unwilling to sacrifice ___ for privacy.",
                    "Dr. Okafor warns of a new form of digital ___.",
                ]},
                {"type": "note_completion", "instruction": "Complete the notes from the panel discussion.", "items": [
                    "GDPR established since: ___",
                    "Main GDPR enforcement issue: ___",
                    "Technical solutions for privacy: ___ and ___",
                    "Challenge in developing world: legislation is ___ or ___",
                    "Risk identified by Dr. Okafor: digital ___",
                    "Panel's key takeaway: privacy is not merely ___ but also ___ and ___",
                ]},
            ],
        },
        4: {
            "title": "A Lecture on the History of English",
            "script": (
                "Good morning, class. Today we continue our exploration of how English evolved into a global language. "
                "Let us begin with the Norman Conquest of 1066, which was perhaps the single most transformative event in English linguistic history. "
                "When William the Conqueror took the throne, French became the language of the court, law, and administration. "
                "English survived among the common people but absorbed thousands of French words in the process. "
                "This is why English often has two words for the same concept: one Germanic, one French. "
                "Think of 'begin' and 'commence,' or 'ask' and 'inquire.' "
                "The French words tend to carry a more formal register — a sociolinguistic fossil from the class divide of medieval England. "
                "By the fourteenth century, English was reasserting itself, culminating in Chaucer's Canterbury Tales. "
                "The Great Vowel Shift, occurring between roughly 1400 and 1700, dramatically changed pronunciation without altering spelling. "
                "This explains why English spelling is so irregular — our spelling system largely reflects medieval pronunciation. "
                "The printing press, introduced by Caxton in 1476, accelerated standardisation but also froze many inconsistencies. "
                "In the Early Modern period, Shakespeare expanded the vocabulary by coining over seventeen hundred words. "
                "The eighteenth century brought prescriptive grammarians who tried to impose Latin rules on English — many of which persist today. "
                "For your assignment, I want you to trace one English word from its Old English or French origin to its current usage. "
                "Include examples of how its meaning, spelling, or register has changed over time."
            ),
            "tasks": [
                {"type": "timeline", "instruction": "Place each event on the timeline by writing the correct date or period.", "items": [
                    "Norman Conquest: ___",
                    "Chaucer's Canterbury Tales: ___ century",
                    "Great Vowel Shift: ___ to ___",
                    "Caxton's printing press: ___",
                    "Shakespeare's era: ___ Modern period",
                    "Prescriptive grammarians: ___ century",
                ]},
                {"type": "short_answer", "instruction": "Answer in one or two sentences.", "items": [
                    "Why does English often have two words for the same concept?",
                    "What is the Great Vowel Shift and why does it matter for spelling?",
                    "How did the printing press both help and hinder English standardisation?",
                    "Give one example of a Germanic-French word pair mentioned in the lecture.",
                    "What is the homework assignment?",
                    "Why does the lecturer call French-origin formality a 'sociolinguistic fossil'?",
                ]},
            ],
        },
        5: {
            "title": "An Interview with a Nobel Prize Researcher",
            "script": (
                "Thank you for joining us, Dr. Mendez. You have spent twenty years studying Nobel Prize-winning literature. "
                "What first drew you to this field? "
                "I was fascinated by how the Nobel Prize shapes literary reputations. "
                "A writer can be relatively unknown one day and a global figure the next simply because Stockholm made a phone call. "
                "That asymmetry of influence is both remarkable and troubling. "
                "You mention it is troubling. Can you elaborate? "
                "The prize has historically favoured European writers, particularly Scandinavian and Western European ones. "
                "African, Asian, and Latin American literatures have been systematically underrepresented. "
                "However, recent decades have shown improvement, with laureates from Tanzania, South Korea, and Poland. "
                "Which laureate's work do you think had the greatest social impact? "
                "That is a difficult question, but I would argue Toni Morrison. "
                "Her Nobel lecture in 1993 is itself a masterpiece — a meditation on how language can liberate or oppress. "
                "It is studied in universities worldwide as both literature and philosophy. "
                "What about Turkish literature? Where does Orhan Pamuk fit? "
                "Pamuk is significant because he brought the rich tradition of Turkish storytelling to a global audience. "
                "His novels challenge Western readers to engage with a non-Western intellectual tradition on its own terms."
            ),
            "tasks": [
                {"type": "multiple_choice", "instruction": "Choose the correct answer based on the interview.", "items": [
                    "How long has Dr. Mendez studied Nobel literature? (A) 10 years (B) 15 years (C) 20 years (D) 25 years",
                    "What does Dr. Mendez find 'troubling' about the Nobel Prize? (A) The prize money (B) The influence asymmetry and geographic bias (C) The ceremony format (D) The selection timeline",
                    "Which laureate does Mendez consider most socially impactful? (A) Pamuk (B) Morrison (C) Marquez (D) Ishiguro",
                    "What is Morrison's Nobel lecture described as? (A) A political speech (B) A meditation on language (C) A historical account (D) An autobiography",
                    "What did Pamuk achieve according to Dr. Mendez? (A) Won the first Nobel for Asia (B) Brought Turkish storytelling to a global audience (C) Inspired the Swedish Academy's reforms (D) Founded a literary festival",
                    "Which recent laureate countries are mentioned as signs of improvement? (A) India, China, Mexico (B) Tanzania, South Korea, Poland (C) Nigeria, Japan, Brazil (D) Egypt, Thailand, Argentina",
                ]},
                {"type": "gap_fill", "instruction": "Complete each statement.", "items": [
                    "The Nobel Prize creates an ___ of influence between known and unknown writers.",
                    "The prize has historically favoured ___ writers.",
                    "Morrison's Nobel lecture is studied as both ___ and ___.",
                    "Pamuk challenges Western readers to engage with a ___ intellectual tradition.",
                    "Dr. Mendez has spent ___ years studying Nobel literature.",
                    "Recent decades have shown ___ in geographic representation.",
                ]},
            ],
        },
        6: {
            "title": "A Diplomatic Briefing on Climate Negotiations",
            "script": (
                "Good afternoon, delegates. I am Ambassador Petrov, and I will brief you on the current state of climate negotiations. "
                "As you know, the Paris Agreement set a target of limiting warming to 1.5 degrees above pre-industrial levels. "
                "However, the latest IPCC assessment indicates that current nationally determined contributions are insufficient. "
                "Even if all pledges are fully implemented, we are on track for approximately 2.5 degrees of warming by 2100. "
                "The emissions gap remains the central challenge of these negotiations. "
                "Developing nations argue, with justification, that they should not bear the same burden as industrialised countries. "
                "The principle of common but differentiated responsibilities must guide our approach. "
                "Financial commitments remain contentious. The promised 100 billion dollars per year in climate finance has not been consistently delivered. "
                "Loss and damage funding, agreed in principle at COP27, still lacks a clear implementation mechanism. "
                "Technology transfer is equally critical — developing nations need access to clean energy technology without prohibitive licensing costs. "
                "I want to be candid: without stronger commitments from major emitters, the 1.5-degree target will become unattainable. "
                "The window for meaningful action is narrowing rapidly. "
                "I urge all delegations to approach tomorrow's sessions with ambition, flexibility, and a genuine commitment to compromise. "
                "The credibility of this process — and of multilateralism itself — depends on what we achieve this week."
            ),
            "tasks": [
                {"type": "note_completion", "instruction": "Complete the briefing notes.", "items": [
                    "Paris Agreement target: ___ degrees above pre-industrial levels.",
                    "Projected warming with current pledges: approximately ___ degrees by ___.",
                    "Key principle for burden-sharing: common but ___ responsibilities.",
                    "Undelivered financial commitment: ___ billion dollars per year.",
                    "COP27 agreement lacking implementation: ___ and ___ funding.",
                    "Ambassador's assessment of the 1.5-degree target without stronger commitments: ___.",
                ]},
                {"type": "short_answer", "instruction": "Answer in complete sentences.", "items": [
                    "What is the 'emissions gap' the ambassador refers to?",
                    "Why do developing nations argue they should not bear the same burden?",
                    "What does the ambassador mean by 'technology transfer'?",
                    "What three qualities does the ambassador urge delegates to show?",
                    "According to the ambassador, what is at stake beyond climate targets?",
                    "What is the tone of the briefing: optimistic, cautiously urgent, or pessimistic? Justify your answer.",
                ]},
            ],
        },
        7: {
            "title": "A Science Podcast on Quantum Computing",
            "script": (
                "Welcome back to 'Quantum Leaps,' the podcast that makes cutting-edge physics accessible. "
                "I am Dr. Patel, and today I am joined by Professor Li Wei from the Beijing Institute of Quantum Science. "
                "Professor Li, can you explain quantum superposition in a way that a non-physicist might understand? "
                "Imagine flipping a coin. In classical physics, the coin is either heads or tails. "
                "In quantum mechanics, it is as if the coin is spinning in the air — both heads and tails at the same time until you catch it. "
                "That spinning state is superposition, and it is what gives quantum computers their extraordinary power. "
                "Now, what about entanglement? "
                "Entanglement is even stranger. Imagine two coins that are mysteriously linked. "
                "No matter how far apart they are, when you catch one and it shows heads, the other instantly shows tails. "
                "Einstein called this 'spooky action at a distance' because it seemed to violate the speed of light. "
                "And the practical applications? "
                "Drug discovery is perhaps the most exciting. Simulating molecular interactions is incredibly difficult for classical computers. "
                "A quantum computer could model these interactions at the atomic level, potentially accelerating the development of new medicines by decades. "
                "But there are risks too — quantum computers could break the encryption that protects our digital infrastructure. "
                "That is why the race for quantum-resistant encryption is just as important as the race for quantum computing itself."
            ),
            "tasks": [
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": [
                    "What analogy does Professor Li use for superposition? (A) A light switch (B) A spinning coin (C) A pair of dice (D) A mirror",
                    "What did Einstein call entanglement? (A) Quantum mystery (B) Spooky action at a distance (C) The uncertainty principle (D) Cosmic linkage",
                    "Which application does Professor Li consider most exciting? (A) Cryptography (B) Artificial intelligence (C) Drug discovery (D) Space exploration",
                    "Why could quantum computers be dangerous? (A) They use too much energy (B) They could break current encryption (C) They are too expensive (D) They replace human workers",
                    "What is as important as quantum computing development? (A) Classical computing upgrades (B) Quantum-resistant encryption (C) Space technology (D) AI regulation",
                    "Where is Professor Li from? (A) Shanghai (B) Tokyo (C) Beijing (D) Seoul",
                ]},
                {"type": "summary_completion", "instruction": "Complete the summary of the podcast.", "items": [
                    "Quantum superposition means a qubit can be in ___ states simultaneously.",
                    "Entanglement links two particles so that measuring one instantly affects the ___.",
                    "Classical computers struggle to simulate ___ interactions at the atomic level.",
                    "Quantum computing could accelerate drug development by ___.",
                    "The main security risk is that quantum computers could break ___.",
                    "The race for quantum-___ encryption is equally important.",
                ]},
            ],
        },
        8: {
            "title": "A Gallery Talk on Contemporary Art",
            "script": (
                "Good afternoon, and welcome to the Istanbul Modern's exhibition, 'Borders and Belonging.' "
                "I am curator Ayse Demir, and I will guide you through the main installations today. "
                "The exhibition explores how contemporary artists respond to migration, identity, and displacement. "
                "Our first piece is by Ai Weiwei — a life jacket installation representing the thousands who have crossed the Mediterranean. "
                "Each jacket was actually worn by a refugee, which gives the work its emotional and ethical weight. "
                "Moving to the next room, you will see Shirin Neshat's photographic series on women's voices in Iran. "
                "Neshat writes Farsi poetry directly onto the photographs, blurring the boundary between image and text. "
                "The third installation, by Turkish artist Hale Tenger, uses mirrors and sound to create a disorienting space. "
                "It simulates the psychological experience of being interrogated, forcing visitors to confront their own vulnerability. "
                "Tenger's work has been exhibited at the Venice Biennale and is considered a landmark of Turkish contemporary art. "
                "In the final gallery, we have a collaborative mural by refugee artists from Syria, Afghanistan, and Somalia. "
                "Each section of the mural tells a personal story of journey and resilience through colour and symbol. "
                "What unites all these works is their insistence that art can bear witness to experiences that statistics alone cannot capture. "
                "Please take your time with each piece. The exhibition closes on the thirty-first of March."
            ),
            "tasks": [
                {"type": "matching", "instruction": "Match each artist with their artwork and medium.", "items": [
                    "Ai Weiwei: medium — ___; subject — ___",
                    "Shirin Neshat: medium — ___; subject — ___",
                    "Hale Tenger: medium — ___; subject — ___",
                    "Refugee collaborative: medium — ___; subject — ___",
                    "The exhibition theme combines migration, ___, and ___.",
                    "The curator says art bears witness to experiences that ___ cannot capture.",
                ]},
                {"type": "short_answer", "instruction": "Answer in complete sentences.", "items": [
                    "What gives Ai Weiwei's life jacket installation its emotional weight?",
                    "How does Shirin Neshat blur the boundary between image and text?",
                    "What psychological experience does Hale Tenger's installation simulate?",
                    "Where has Tenger's work been previously exhibited?",
                    "What is the collaborative mural's subject matter?",
                    "What is the unifying theme the curator identifies across all works?",
                ]},
            ],
        },
        9: {
            "title": "A WHO Press Conference on Pandemic Preparedness",
            "script": (
                "Good morning, ladies and gentlemen. I am Dr. Rahman, WHO Director for Health Emergencies. "
                "Today I will update you on the progress of the Pandemic Treaty negotiations. "
                "Since the launch of negotiations in 2022, member states have held twelve rounds of formal discussions. "
                "There has been significant progress on three fronts: early warning systems, data sharing, and equitable access to medical countermeasures. "
                "However, two major sticking points remain. "
                "First, the question of intellectual property waivers during health emergencies. "
                "Pharmaceutical companies argue that waivers undermine the incentive to innovate. "
                "Developing nations counter that profit should not determine who lives and who dies during a pandemic. "
                "Second, the issue of financial contributions. "
                "Wealthy nations have been reluctant to commit binding financial obligations to a pandemic preparedness fund. "
                "Without predictable funding, any preparedness framework will remain aspirational rather than operational. "
                "I want to emphasise that the next pandemic is not hypothetical — it is a statistical certainty. "
                "The only uncertainty is when it will occur and how prepared we will be. "
                "We owe it to the millions who lost their lives during COVID-19 to ensure we are better prepared next time. "
                "I will now take your questions."
            ),
            "tasks": [
                {"type": "true_false", "instruction": "Write True or False.", "items": [
                    "The Pandemic Treaty negotiations began in 2020.",
                    "Twelve rounds of formal discussions have been held.",
                    "There has been progress on early warning systems.",
                    "Pharmaceutical companies support intellectual property waivers.",
                    "Wealthy nations have committed binding financial obligations.",
                    "Dr. Rahman describes the next pandemic as a statistical certainty.",
                ]},
                {"type": "note_completion", "instruction": "Complete the press conference notes.", "items": [
                    "Three areas of progress: ___, ___, and ___.",
                    "Sticking point 1: intellectual property ___ during emergencies.",
                    "Pharmaceutical companies' argument: waivers undermine ___.",
                    "Sticking point 2: wealthy nations reluctant to commit ___ financial obligations.",
                    "Without predictable funding, the framework will be ___ rather than ___.",
                    "Dr. Rahman says the next pandemic is not ___ but a ___.",
                ]},
            ],
        },
        10: {
            "title": "A TED Talk on Green Hydrogen",
            "script": (
                "What if I told you that the most abundant element in the universe could solve our energy crisis? "
                "I am Dr. Aylin Celik, and I research green hydrogen at Istanbul Technical University. "
                "Hydrogen is everywhere — in water, in organic matter, in the sun. "
                "But producing it cleanly has been the challenge. Traditional hydrogen production uses natural gas, releasing carbon dioxide. "
                "Green hydrogen is different. It is produced through electrolysis — splitting water into hydrogen and oxygen using renewable electricity. "
                "The only by-product is oxygen. No carbon. No pollution. "
                "So why is not the whole world using it? Cost. "
                "Until recently, green hydrogen was three to four times more expensive than its fossil-fuel-derived counterpart. "
                "But that gap is closing rapidly. As solar and wind costs plummet, so does the cost of electrolysis. "
                "By 2030, green hydrogen could reach price parity with grey hydrogen in many markets. "
                "The applications are transformative: steel production without coal, shipping without bunker fuel, aviation without kerosene. "
                "Turkey has extraordinary potential here. With 2,640 hours of sunshine per year and strong wind corridors, Turkey could become a green hydrogen superpower. "
                "Imagine exporting clean energy to Europe through existing pipeline infrastructure. "
                "The technology is ready. The economics are improving. What we need now is political will and investment. "
                "Thank you."
            ),
            "tasks": [
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": [
                    "What is the main barrier to green hydrogen adoption? (A) Technology (B) Cost (C) Public opinion (D) Safety",
                    "How is green hydrogen produced? (A) Burning natural gas (B) Nuclear fission (C) Electrolysis using renewables (D) Chemical synthesis",
                    "What is the only by-product of green hydrogen production? (A) Carbon dioxide (B) Methane (C) Nitrogen (D) Oxygen",
                    "When could green hydrogen reach price parity? (A) 2025 (B) 2028 (C) 2030 (D) 2035",
                    "How many hours of sunshine does Turkey receive annually? (A) 2,000 (B) 2,400 (C) 2,640 (D) 3,000",
                    "Which sectors does the speaker mention as applications? (A) Agriculture, mining, tourism (B) Steel, shipping, aviation (C) Healthcare, education, finance (D) Construction, retail, logistics",
                ]},
                {"type": "summary_completion", "instruction": "Complete the summary.", "items": [
                    "Green hydrogen is produced by splitting ___ into hydrogen and ___.",
                    "Traditional hydrogen production uses ___, which releases CO2.",
                    "The cost gap is closing because ___ and wind costs are falling.",
                    "Three hard-to-decarbonise sectors mentioned: ___, ___, and ___.",
                    "Turkey's advantages include abundant ___ and strong ___ corridors.",
                    "The speaker concludes that the technology is ready but ___ and ___ are needed.",
                ]},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 10. MODEL WRITING BANK (160-200 words each)
# ---------------------------------------------------------------------------
MODEL_WRITING_BANK = {
    12: {
        1: {
            "genre": "Statement of Purpose",
            "title": "Application to BSc Cognitive Science",
            "model_text": (
                "My fascination with the human mind began at fifteen, when I read Oliver Sacks's 'The Man Who Mistook His Wife "
                "for a Hat.' The case studies revealed that cognition is not a monolithic faculty but a fragile, beautiful assembly "
                "of interdependent processes. Since then, I have pursued this interest rigorously: completing advanced coursework "
                "in biology and psychology, conducting a school-based research project on memory encoding strategies, and attending "
                "a neuroscience summer school at Koc University. What draws me to your programme specifically is its interdisciplinary "
                "structure, integrating philosophy, linguistics, and computer science alongside neuroscience. I believe that "
                "understanding the mind requires precisely this kind of convergent approach. My long-term ambition is to research "
                "neuroplasticity in multilingual individuals — a topic that sits at the intersection of linguistics and cognitive "
                "neuroscience. I bring not only academic preparation but also the curiosity, resilience, and collaborative spirit "
                "that your programme values. I am confident that studying at your university will equip me with the skills and "
                "perspectives to contribute meaningfully to this field."
            ),
            "structure_notes": [
                "Opening hook: a specific, personal moment that sparked interest.",
                "Evidence of sustained engagement: coursework, research, extracurriculars.",
                "Why this programme: specific features that align with the applicant's goals.",
                "Long-term ambition: a clear, focused research interest.",
                "Closing: personal qualities and confident forward-looking statement.",
            ],
            "writing_prompt": "Write a statement of purpose (180-200 words) for a university programme in your field of interest. Include a personal hook, evidence of preparation, and a specific reason for choosing the programme.",
        },
        2: {
            "genre": "Analytical Essay (Introduction)",
            "title": "The Rhetoric of Climate Change Denial",
            "model_text": (
                "Despite overwhelming scientific consensus that human activity is driving global warming, a well-funded and "
                "strategically sophisticated denial industry continues to cast doubt on climate science. This essay analyses the "
                "rhetorical strategies employed by climate change denial organisations, focusing on three primary techniques: the "
                "manufacture of false balance in media coverage, the strategic deployment of credentialed contrarians, and the "
                "exploitation of scientific uncertainty as a rhetorical weapon. Drawing on Oreskes and Conway's seminal work "
                "'Merchants of Doubt,' I argue that these strategies are not spontaneous expressions of scepticism but deliberate, "
                "coordinated campaigns modelled on the tobacco industry's earlier efforts to obscure the link between smoking and "
                "cancer. The analysis proceeds in three sections: first, an examination of how false balance operates in broadcast "
                "media; second, a case study of the Heartland Institute's communication strategy; and third, an evaluation of "
                "counter-strategies employed by climate scientists and communicators. By understanding the mechanics of denial, "
                "citizens and policymakers can develop more effective defences against misinformation."
            ),
            "structure_notes": [
                "Context: establish the scientific consensus as background.",
                "Thesis: clearly state the argument — denial is strategic, not spontaneous.",
                "Scope: identify three specific techniques to be analysed.",
                "Academic grounding: reference a key scholarly source.",
                "Road map: outline the essay's structure for the reader.",
            ],
            "writing_prompt": "Write an analytical essay introduction (180-200 words) on a topic of your choice. Include context, a clear thesis, defined scope, and a structural road map.",
        },
        3: {
            "genre": "Opinion Essay",
            "title": "Privacy in the Digital Age: A Right, Not a Luxury",
            "model_text": (
                "In an era where every click, search, and GPS coordinate is harvested for commercial gain, privacy has ceased to "
                "be a personal preference and become a fundamental human right requiring robust legal protection. Proponents of "
                "data-driven business models argue that users consent to data collection by accepting terms of service — but this "
                "argument collapses under scrutiny. Studies consistently show that fewer than ten per cent of users read privacy "
                "policies, and those who do often lack the technical literacy to understand them. Consent, in this context, is a "
                "legal fiction. Furthermore, the asymmetry of power between multinational technology corporations and individual "
                "users renders meaningful choice illusory. The European Union's General Data Protection Regulation represents "
                "a significant step forward, establishing principles such as data minimisation, purpose limitation, and the right "
                "to erasure. However, enforcement remains inconsistent, and jurisdictional fragmentation allows global corporations "
                "to exploit regulatory gaps. What is needed is an international framework — a digital Geneva Convention — that "
                "enshrines data privacy as a universal right, not a market commodity. Without such a framework, democratic "
                "autonomy itself is at risk."
            ),
            "structure_notes": [
                "Opening assertion: privacy as a right, not preference.",
                "Counter-argument acknowledged and refuted: consent is a fiction.",
                "Evidence: statistics on user behaviour.",
                "Existing solution evaluated: GDPR praised but critiqued.",
                "Proposed solution: international framework with a memorable label.",
            ],
            "writing_prompt": "Write an opinion essay (180-200 words) arguing for or against a specific digital rights policy. Acknowledge the opposing view and support your argument with evidence.",
        },
        4: {
            "genre": "Comparative Essay (Body Paragraph)",
            "title": "Syntactic Complexity in Pamuk and Morrison",
            "model_text": (
                "Both Orhan Pamuk and Toni Morrison employ syntactic complexity as a narrative strategy, yet their approaches "
                "serve fundamentally different purposes. Pamuk's sentences in 'Istanbul: Memories and the City' are characterised "
                "by long, subordinate-clause-heavy constructions that mirror the layered, palimpsestic quality of the city itself. "
                "The reader, like the narrator, must navigate multiple temporal and spatial frames within a single sentence, "
                "creating a sense of melancholy disorientation that is central to the book's emotional register. Morrison, by "
                "contrast, uses syntactic disruption — fragmented sentences, abrupt shifts in tense and person, and stream-of-"
                "consciousness passages — to enact the psychological trauma of her characters. In 'Beloved,' the title character's "
                "monologue abandons conventional syntax altogether, reflecting the impossibility of articulating an experience "
                "that exceeds language's capacity. Where Pamuk's complexity invites contemplation, Morrison's demands participation: "
                "the reader must actively reconstruct meaning from syntactic fragments. Both writers demonstrate that syntax is not "
                "merely a vehicle for content but a form of content itself — a structural argument about how memory, identity, "
                "and history are experienced."
            ),
            "structure_notes": [
                "Topic sentence: both use syntactic complexity but differently.",
                "Analysis of Writer A: technique, example, effect.",
                "Analysis of Writer B: technique, example, effect.",
                "Comparison: explicit contrast using linking language.",
                "Concluding insight: syntax as content, not just container.",
            ],
            "writing_prompt": "Write a comparative body paragraph (180-200 words) analysing a specific literary or linguistic technique in two authors you have studied.",
        },
        5: {
            "genre": "Literary Analysis Essay",
            "title": "The Politics of Memory in Pamuk's 'Snow'",
            "model_text": (
                "Orhan Pamuk's 'Snow' interrogates the relationship between political ideology and personal memory through the "
                "figure of Ka, a poet in self-imposed exile who returns to the remote Turkish city of Kars. The novel's structure "
                "— narrated retrospectively by a friend who reconstructs Ka's experiences from notebooks and interviews — enacts "
                "the unreliability of memory at a formal level. Every event is mediated, interpreted, and potentially distorted. "
                "Pamuk uses this narrative instability to explore how competing political ideologies — secularism, Islamism, "
                "nationalism — each construct their own version of Turkish history and identity. Ka's poems, which arrive unbidden "
                "during moments of emotional intensity, represent an alternative form of knowing: intuitive, personal, and "
                "resistant to ideological appropriation. Yet even poetry, Pamuk suggests, is not innocent; Ka arranges his poems "
                "in a structure modelled on a snowflake, imposing geometric order on what is inherently chaotic. The novel thus "
                "argues that all acts of remembering are also acts of constructing — and that this construction is always, "
                "inescapably, political."
            ),
            "structure_notes": [
                "Opening: identify the central thematic concern.",
                "Structural analysis: connect narrative form to thematic content.",
                "Political dimension: link to competing ideologies.",
                "Symbolic reading: interpret a key motif (poetry/snowflake).",
                "Closing argument: synthesis of form, theme, and politics.",
            ],
            "writing_prompt": "Write a literary analysis paragraph (180-200 words) on a novel you have studied, connecting a formal element (structure, narration, symbolism) to a thematic concern.",
        },
        6: {
            "genre": "Position Paper (MUN Format)",
            "title": "Republic of Turkey: Digital Governance and Cybersecurity",
            "model_text": (
                "The Republic of Turkey recognises that digital governance and cybersecurity are inseparable pillars of twenty-"
                "first-century sovereignty. As a nation undergoing rapid digital transformation, Turkey has invested significantly "
                "in e-government infrastructure, with over 5,700 public services now accessible through the e-Devlet platform. "
                "However, this digital expansion necessitates proportional investment in cybersecurity. Turkey established the "
                "National Cyber Incident Response Centre in 2013 and enacted the Personal Data Protection Law in 2016, aligning "
                "domestic legislation with international standards. Turkey supports the development of a comprehensive UN "
                "framework for responsible state behaviour in cyberspace, building on the 2015 GGE norms. We call upon member "
                "states to commit to three priorities: first, the establishment of national computer emergency response teams; "
                "second, mandatory cybersecurity education in secondary school curricula; and third, the creation of a multilateral "
                "fund to support capacity building in developing nations. Turkey stands ready to share its experience in digital "
                "governance and to collaborate with all willing partners in building a secure, inclusive digital future."
            ),
            "structure_notes": [
                "Opening: state the country's position clearly.",
                "National context: what the country has done domestically.",
                "International alignment: reference to existing frameworks.",
                "Three specific proposals: numbered for clarity.",
                "Closing: offer of collaboration and forward-looking tone.",
            ],
            "writing_prompt": "Write a MUN position paper (180-200 words) representing Turkey (or another country) on an international issue of your choice. Include national context, international references, and specific proposals.",
        },
        7: {
            "genre": "Expository Essay",
            "title": "Quantum Computing Explained for Non-Specialists",
            "model_text": (
                "Quantum computing harnesses the principles of quantum mechanics to process information in ways that are "
                "fundamentally impossible for classical computers. Where a classical bit exists as either zero or one, a quantum "
                "bit — or qubit — can exist in both states simultaneously through a phenomenon called superposition. When multiple "
                "qubits are entangled, measuring one instantaneously determines the state of its partner, regardless of distance. "
                "These properties allow quantum computers to explore vast numbers of possibilities in parallel, making them "
                "extraordinarily powerful for specific tasks: simulating molecular structures for drug discovery, optimising "
                "complex logistics networks, and factoring the large prime numbers that underpin modern encryption. However, "
                "quantum computing is not a simple upgrade to existing technology; it is an entirely different paradigm that "
                "requires new algorithms, new error-correction techniques, and operating temperatures colder than outer space. "
                "Current machines are still in the 'noisy intermediate-scale' phase, meaning they are powerful enough to "
                "demonstrate quantum advantage for certain problems but not yet reliable enough for widespread practical use. "
                "The transition from experimental curiosity to transformative technology will likely take another decade of "
                "sustained research and investment."
            ),
            "structure_notes": [
                "Opening definition: what quantum computing is at a fundamental level.",
                "Key concepts explained: superposition, entanglement, parallelism.",
                "Applications: three concrete examples.",
                "Limitations: honest assessment of current constraints.",
                "Future outlook: realistic timeline for practical impact.",
            ],
            "writing_prompt": "Write an expository paragraph (180-200 words) explaining a complex scientific or technological concept to a non-specialist audience. Use analogies and avoid unnecessary jargon.",
        },
        8: {
            "genre": "Art Critique",
            "title": "Ai Weiwei's 'Sunflower Seeds': Beauty and Mass Production",
            "model_text": (
                "Ai Weiwei's 'Sunflower Seeds' (2010), installed in the Turbine Hall of Tate Modern, consisted of one hundred "
                "million hand-painted porcelain seeds spread across the vast floor. Each seed was individually crafted by artisans "
                "in Jingdezhen, China's porcelain capital, over a period of two and a half years. The installation operates on "
                "multiple levels simultaneously. On one level, it is a meditation on mass production and individuality: from a "
                "distance, the seeds appear identical; up close, each bears the unique marks of its maker's hand. On another, it "
                "evokes the relationship between the individual and the collective in Chinese political culture, where the sunflower "
                "was a symbol of the people's devotion to Chairman Mao. The sheer scale — one hundred million — is itself a "
                "statement about the overwhelming weight of population, labour, and history. Visitors were initially invited to walk "
                "on the seeds, but dust concerns led to the closure of this interactive element, inadvertently reinforcing the work's "
                "theme: that even in art, individual agency is constrained by institutional decisions."
            ),
            "structure_notes": [
                "Context: artist, title, date, location, medium.",
                "Description: what the work looks like and how it was made.",
                "Interpretation layer 1: mass production vs. individuality.",
                "Interpretation layer 2: political symbolism.",
                "Ironic coda: the closure as unintentional thematic reinforcement.",
            ],
            "writing_prompt": "Write an art critique (180-200 words) of an artwork you have seen or studied. Describe the work, then offer at least two levels of interpretation.",
        },
        9: {
            "genre": "Policy Brief (Executive Summary)",
            "title": "Addressing Antimicrobial Resistance: A Policy Brief",
            "model_text": (
                "Antimicrobial resistance (AMR) constitutes one of the most urgent yet underappreciated threats to global public "
                "health. The World Health Organisation estimates that drug-resistant infections already cause over 1.2 million "
                "deaths annually — more than HIV/AIDS or malaria — and projects that this figure could rise to ten million by 2050 "
                "without decisive intervention. The primary drivers of AMR include the overuse of antibiotics in human medicine, "
                "the routine use of antimicrobials in livestock farming, and inadequate infection prevention and control in "
                "healthcare settings. This policy brief recommends four evidence-based interventions: first, implementing national "
                "antimicrobial stewardship programmes that regulate prescribing practices; second, phasing out the use of "
                "medically important antibiotics as growth promoters in agriculture; third, investing in rapid diagnostic "
                "technologies that enable targeted rather than empirical antibiotic use; and fourth, establishing a globally "
                "coordinated surveillance network modelled on the WHO's Global Antimicrobial Resistance Surveillance System. "
                "Without coordinated multilateral action, AMR threatens to reverse a century of medical progress and render "
                "routine surgical procedures, chemotherapy, and organ transplants prohibitively dangerous."
            ),
            "structure_notes": [
                "Problem statement: scale and urgency of the threat.",
                "Data: key statistics from authoritative sources.",
                "Drivers: identify root causes clearly.",
                "Recommendations: four numbered, evidence-based actions.",
                "Warning: consequences of inaction to motivate urgency.",
            ],
            "writing_prompt": "Write a policy brief executive summary (180-200 words) on a global health challenge. Include the problem, key data, drivers, and at least three specific recommendations.",
        },
        10: {
            "genre": "Persuasive Speech",
            "title": "Investing in Green Technology Is Investing in Our Future",
            "model_text": (
                "Distinguished panel, fellow students — the question before us is not whether we can afford to invest in green "
                "technology, but whether we can afford not to. The economics are clear: solar energy costs have fallen ninety per "
                "cent in fourteen years; electric vehicles will reach price parity with petrol cars by 2027; and green hydrogen "
                "is poised to decarbonise the industries that renewables alone cannot reach. Turkey, with 2,640 hours of annual "
                "sunshine and powerful wind corridors along its coasts, possesses natural advantages that many nations would envy. "
                "Yet we are deploying these resources at a fraction of our potential. Every year of delay means more carbon locked "
                "into infrastructure, more health costs from air pollution, and more economic opportunity lost to competitors who "
                "are moving faster. The just transition framework ensures that this shift need not leave anyone behind: retraining "
                "programmes, community energy cooperatives, and targeted investment in underserved regions can distribute the "
                "benefits equitably. I urge this panel to recommend an accelerated national green technology strategy — not as an "
                "idealistic aspiration, but as a hard-headed economic imperative. Our planet's future, and our nation's prosperity, "
                "depend on the decisions we make today."
            ),
            "structure_notes": [
                "Opening: reframe the question to shift the burden of proof.",
                "Evidence: three compelling economic data points.",
                "National relevance: Turkey's specific advantages.",
                "Urgency: consequences of delay.",
                "Call to action: specific recommendation with confident closing.",
            ],
            "writing_prompt": "Write a persuasive speech (180-200 words) advocating for a specific green technology policy or investment. Use economic data, national relevance, and a clear call to action.",
        },
    },
}

# ---------------------------------------------------------------------------
# 11. PRONUNCIATION BANK
# ---------------------------------------------------------------------------
PRONUNCIATION_BANK = {
    12: {
        1: {
            "focus": "Academic Word Stress Patterns",
            "explanation": "In academic English, word stress often shifts when suffixes are added. Understanding these patterns helps both comprehension and production of formal vocabulary.",
            "examples": [
                "eDUcate -> eduCAtion -> educaTIONal",
                "aNAlyse -> aNAlysis -> analyTIcal",
                "deMOcracy -> demoCAtic -> democraTIsation",
                "eCOnomy -> ecoNOMic -> ecoNOMical",
                "PHOtograph -> phoTOgraphy -> photoGRAPHic",
                "psyCHOlogy -> psychoLOGical -> psycholoGIcally",
            ],
            "tongue_twister": "The philosophical psychologist photographically analysed the economical educational establishment.",
            "practice_words": ["pedagogy", "pedagogical", "university", "curriculum", "interdisciplinary", "methodology", "accreditation", "vocational"],
        },
        2: {
            "focus": "Contrastive Stress for Emphasis",
            "explanation": "In English, shifting stress to a different word in a sentence changes its meaning. This is crucial for argumentation, where emphasis signals the writer or speaker's key point.",
            "examples": [
                "I did not say he STOLE the data. (Someone else said it.)",
                "I did NOT say he stole the data. (I deny saying it.)",
                "I did not say HE stole the data. (Someone else stole it.)",
                "I did not say he stole the DATA. (He stole something else.)",
                "THIS argument is flawed, not THAT one.",
                "She did not ANALYSE the text; she merely SUMMARISED it.",
            ],
            "tongue_twister": "She said she should show Sean the short sharp shock of a shift in stress.",
            "practice_words": ["rhetoric", "persuasion", "analytical", "propaganda", "discourse", "credibility", "manipulation", "fabrication"],
        },
        3: {
            "focus": "Connected Speech: Elision and Assimilation",
            "explanation": "In natural speech, sounds are often dropped (elision) or modified to match neighbouring sounds (assimilation). Recognising these patterns improves listening comprehension at C1 level.",
            "examples": [
                "next day -> /neks deI/ (t elided before d)",
                "handbag -> /haembag/ (d elided, n assimilates to m before b)",
                "used to -> /juːstə/ (d elided)",
                "want to -> /wɒnə/ (informal: 'wanna')",
                "government -> /gʌvəmənt/ (n elided in fast speech)",
                "probably -> /prɒbli/ (ab reduced in casual speech)",
            ],
            "tongue_twister": "The government granted greater privacy protection, but the public probably could not comprehend the complicated conditions.",
            "practice_words": ["surveillance", "encryption", "vulnerability", "cybersecurity", "authentication", "infrastructure", "jurisdiction", "algorithm"],
        },
        4: {
            "focus": "Intonation in Academic Presentations",
            "explanation": "Falling intonation signals statements and completed thoughts. Rising intonation signals questions and lists. A fall-rise pattern signals contrast, reservation, or incompleteness. Mastering these patterns makes presentations more engaging and clear.",
            "examples": [
                "Falling: 'The results are conclusive.' (statement, certainty)",
                "Rising: 'Have the results been verified?' (yes/no question)",
                "Fall-rise: 'The results are promising... but not conclusive.' (reservation)",
                "List intonation: 'We analysed syntax, ↑ morphology, ↑ and semantics. ↓' (rise on items, fall on last)",
                "Rhetorical question: 'Is this really what we want? ↓' (falling = the answer is obvious)",
                "Emphatic: 'THIS is the key finding. ↓' (strong fall on stressed word)",
            ],
            "tongue_twister": "Can the cunning linguist distinguish a rising rhetorical question from a falling factual assertion?",
            "practice_words": ["nominalization", "subordinate", "prescriptive", "inflection", "syntax", "register", "morphology", "etymology"],
        },
        5: {
            "focus": "Literary Pronunciation: Reading Aloud",
            "explanation": "Reading literature aloud requires attention to rhythm, pacing, and the sound patterns authors embed in prose. Prose rhythm — the alternation of stressed and unstressed syllables — creates musicality and emotional effect.",
            "examples": [
                "Iambic rhythm: 'The BRAIN is NOT merELY an ORgan' (da-DUM pattern)",
                "Pausing at semicolons creates dramatic separation.",
                "Alliteration: 'the BEAUTY and BURDEN of BEARING witness'",
                "Long vowels slow pace: 'the old stone library that smelled of cedarwood'",
                "Short, punchy words accelerate: 'She came. She saw. She spoke.'",
                "Enjambment in prose: reading past the line break maintains flow.",
            ],
            "tongue_twister": "The laureate's lyrical legacy lingers long in literary landscapes of lasting luminosity.",
            "practice_words": ["melancholy", "polyphonic", "canonical", "resilience", "testimony", "narrative", "protagonist", "allegory"],
        },
        6: {
            "focus": "Diplomatic Register Pronunciation",
            "explanation": "Diplomatic English uses measured pacing, precise articulation, and careful intonation to convey authority and respect. Hedging phrases receive particular attention to intonation to signal appropriate caution.",
            "examples": [
                "'With respect, we believe...' (measured pace, slight fall-rise on 'respect')",
                "'The delegation WOULD like to PROPOSE...' (stress on modal and verb)",
                "'This is, if I may say so, a MATTER of some URGENCY.' (parenthetical lowered)",
                "'We find ourselves in BROAD agreement.' (stress on 'broad' to signal qualification)",
                "'The CHAIR recognises the delegate from Turkey.' (formal falling tone)",
                "'Might we SUGGEST an alternative FORMULATION?' (rising on 'formulation' for politeness)",
            ],
            "tongue_twister": "The distinguished delegate deliberately delivered a diplomatically delicate declaration on disarmament.",
            "practice_words": ["multilateral", "amendment", "ratification", "sovereignty", "humanitarian", "arbitration", "precedent", "resolution"],
        },
        7: {
            "focus": "Scientific Terminology Stress",
            "explanation": "Scientific terms often follow Greek or Latin stress patterns. Words ending in -tion, -sion, -ic, and -ical have predictable stress on the syllable before the suffix. Terms ending in -ment, -ness, and -ly retain the base word's stress.",
            "examples": [
                "SUperposition (stress on SU-, not on -po-)",
                "decoHErence (stress on -HE-)",
                "crypTOGraphy -> cryptoGRAPHic",
                "determiNIStic vs. probabiLIStic (stress before -istic)",
                "epiSTEMological (stress on -STE-)",
                "quanTUM (stress on first syllable in noun; QUANTUM)",
            ],
            "tongue_twister": "The probabilistic epistemological implications of quantum superposition perplex even the most perspicacious physicists.",
            "practice_words": ["superposition", "entanglement", "decoherence", "cryptographic", "deterministic", "probabilistic", "epistemological", "algorithm"],
        },
        8: {
            "focus": "Expressive Reading of Art Criticism",
            "explanation": "Art criticism uses evocative, descriptive language that benefits from expressive reading. Adjective clusters require careful pacing, and evaluative terms need appropriate emphasis to convey the critic's stance.",
            "examples": [
                "'a monochrome HOWL of ANguish' (strong stress on emotive words)",
                "'simultaneously a THEological statement AND a TOUR de force' (dual stress for balance)",
                "'stark, TIMEless, UNcompromising' (pause between adjectives for weight)",
                "French borrowings: 'tour de force' /tʊər də fɔːrs/, 'avant-garde' /ævɒ̃ gɑːrd/",
                "'the commodiFICation of disSENT' (stress on key syllables of nominalizations)",
                "'exCAVate the PAINful LEGacy' (rhythmic stress pattern for dramatic effect)",
            ],
            "tongue_twister": "The avant-garde artist's austere aesthetic alienated audiences accustomed to accessible, agreeable art.",
            "practice_words": ["aesthetic", "perspectival", "monochrome", "commodification", "installation", "avant-garde", "silhouette", "contemporary"],
        },
        9: {
            "focus": "Medical and Health Terminology",
            "explanation": "Health-related terminology follows specific stress patterns. Words from Greek roots often stress the antepenultimate syllable. Familiarity with these patterns aids comprehension of health news and academic texts.",
            "examples": [
                "epiDEMiological (stress on -DE-)",
                "antimiCRObial (stress on -CRO-)",
                "immuNIsation vs. vacciNAtion (different stress positions)",
                "panDEMic vs. epiDEMic (same stress pattern)",
                "pharMACeutical (stress on -CEU-)",
                "asymptoMATic (stress on -MAT-)",
            ],
            "tongue_twister": "The epidemiological investigation identified asymptomatic antimicrobial-resistant pathogens in pharmaceutical facilities.",
            "practice_words": ["epidemiological", "antimicrobial", "pharmaceutical", "asymptomatic", "immunisation", "pathogen", "surveillance", "quarantine"],
        },
        10: {
            "focus": "Persuasive Speech Delivery",
            "explanation": "Effective persuasive speaking combines stress, pacing, pausing, and pitch variation. Key techniques include the 'power pause' before important points, tricolon rhythm, and pitch drops for authority.",
            "examples": [
                "PAUSE before the key word: 'What we need now is... [pause] ...COURAGE.'",
                "Tricolon rhythm: 'The technology EXISTS. ↓ The economics FAVOUR it. ↓ The time is NOW. ↓↓'",
                "Building volume: 'Not tomorrow. Not next year. TODAY.'",
                "Pitch drop for authority: 'This is not optional. ↓↓'",
                "Rhetorical question + pause: 'Can we afford to wait? [long pause] No.'",
                "Emphatic contrast: 'The question is not WHETHER but HOW FAST.'",
            ],
            "tongue_twister": "The passionate presenter persuasively promoted practical, progressive, planet-preserving policies with powerful precision.",
            "practice_words": ["sustainable", "decarbonisation", "photovoltaic", "electrolysis", "intermittency", "infrastructure", "renewable", "trajectory"],
        },
    },
}

# ---------------------------------------------------------------------------
# 12. WORKBOOK BANK
# ---------------------------------------------------------------------------
WORKBOOK_BANK = {
    12: {
        1: {
            "exercises": [
                {"type": "transformation", "instruction": "Rewrite each sentence using a cleft structure.", "items": [
                    "The digital revolution transformed higher education most dramatically.",
                    "Dr. Aydin inspired the students to pursue interdisciplinary research.",
                    "The flipped classroom model improved critical thinking scores.",
                    "A lack of mentorship undermines online learning.",
                    "Micro-credentials are challenging the traditional degree.",
                    "Martha Nussbaum argued for education as democratic cultivation.",
                ]},
                {"type": "vocabulary", "instruction": "Complete each sentence with a word from the unit vocabulary.", "items": [
                    "The university adopted a new ___ approach emphasising project-based learning.",
                    "MOOCs aimed to ___ access to higher education globally.",
                    "The ___ of online-only programmes remains debated among educators.",
                    "A ___ model combining online and in-person learning shows the best results.",
                    "___ bodies must adapt to ensure quality keeps pace with innovation.",
                    "Education should not be reduced to ___ preparation alone.",
                ]},
                {"type": "reading_comprehension", "instruction": "Read the passage and answer the questions.", "items": [
                    "According to the passage, why do MOOC completion rates remain low?",
                    "What does 'unbundling curricula' mean in the context of higher education?",
                    "How do micro-credentials differ from traditional degrees?",
                    "What is Martha Nussbaum's view on the purpose of education?",
                    "Why does the author mention Scandinavian universities specifically?",
                    "Do you agree that technology can preserve the humanistic core of education? Explain.",
                ]},
                {"type": "writing", "instruction": "Write a paragraph (100-120 words) on the given topic.", "items": [
                    "Compare the advantages of traditional and online university education.",
                    "Argue for or against making micro-credentials equivalent to university degrees.",
                    "Describe how technology has changed your own learning experience.",
                    "Evaluate the flipped classroom model based on your experience.",
                    "Discuss whether university prestige matters more than demonstrated skills.",
                    "Propose one change to improve higher education in Turkey.",
                ]},
                {"type": "error_correction", "instruction": "Find and correct the error in each sentence.", "items": [
                    "The number of online students have increased dramatically since 2020.",
                    "Education is important for to develop critical thinking skills.",
                    "Despite of the challenges, hybrid learning shows promising results.",
                    "The university which I studied at it is ranked in the top 100.",
                    "Each of the programmes are designed for working professionals.",
                    "She has been studying in this university since three years.",
                ]},
            ],
        },
        2: {
            "exercises": [
                {"type": "transformation", "instruction": "Nominalise the underlined verb or adjective.", "items": [
                    "The company decided to restructure. -> The company's ___ to restructure...",
                    "The government failed to respond quickly. -> The government's ___ to respond...",
                    "Technology has developed rapidly. -> The rapid ___ of technology...",
                    "Populations are growing in urban areas. -> Urban population ___...",
                    "Researchers investigated the phenomenon. -> The ___ of the phenomenon...",
                    "Inequality persists in developing nations. -> The ___ of inequality...",
                ]},
                {"type": "vocabulary", "instruction": "Match each word with its correct definition.", "items": [
                    "rhetoric — (a) the art of persuasion (b) the study of grammar (c) formal writing",
                    "provenance — (a) a type of government (b) the origin of something (c) a legal right",
                    "fabrication — (a) manufacturing (b) inventing something false (c) building materials",
                    "fallacy — (a) a proven theory (b) flawed reasoning (c) a type of evidence",
                    "propaganda — (a) neutral reporting (b) biased information for a cause (c) academic writing",
                    "indispensable — (a) unnecessary (b) absolutely essential (c) easily replaced",
                ]},
                {"type": "gap_fill", "instruction": "Complete each sentence with an appropriate hedging or boosting expression.", "items": [
                    "The results ___ that social media influences political opinions. (hedge)",
                    "It is ___ that climate change poses a serious threat. (boost)",
                    "There ___ be a correlation between diet and academic performance. (hedge)",
                    "The evidence ___ demonstrates the effectiveness of the intervention. (boost)",
                    "The findings ___ indicate a modest improvement. (hedge)",
                    "It is ___ acknowledged that education reduces poverty. (boost)",
                ]},
                {"type": "analysis", "instruction": "Identify the rhetorical strategy (ethos, pathos, or logos) in each example.", "items": [
                    "'As a doctor with thirty years of experience, I can assure you...'",
                    "'Imagine a child going to bed hungry every night in a country that wastes 40% of its food.'",
                    "'Studies show a 23% reduction in emissions when carbon taxes are implemented.'",
                    "'Nine out of ten dentists recommend this toothpaste.'",
                    "'Our soldiers did not die for this. They died for freedom.'",
                    "'The data from three independent laboratories confirms the hypothesis.'",
                ]},
                {"type": "writing", "instruction": "Write a short analytical paragraph (100-120 words).", "items": [
                    "Analyse the rhetorical strategies used in a political speech you have heard recently.",
                    "Evaluate the effectiveness of a social media campaign's use of pathos.",
                    "Discuss whether influencer endorsements constitute a form of ethos.",
                    "Argue that media literacy should be a compulsory school subject.",
                    "Compare the rhetorical strategies of two advertisements for similar products.",
                    "Analyse how a news headline uses language to influence reader interpretation.",
                ]},
            ],
        },
        3: {
            "exercises": [
                {"type": "vocabulary", "instruction": "Complete each sentence with the correct cybersecurity term.", "items": [
                    "A ___ vulnerability is one that has not yet been discovered by the software developer.",
                    "End-to-end ___ ensures that only the sender and receiver can read messages.",
                    "___ testing involves simulating attacks to find security weaknesses.",
                    "A data ___ occurs when unauthorised parties access confidential information.",
                    "___ scanning identifies individuals using unique physical characteristics.",
                    "The GDPR grants citizens the right to data ___: transferring their data to another service.",
                ]},
                {"type": "transformation", "instruction": "Add appropriate hedging to each claim.", "items": [
                    "Social media companies sell user data to third parties.",
                    "Artificial intelligence will make human programmers obsolete.",
                    "Government surveillance prevents terrorism.",
                    "Teenagers are addicted to their smartphones.",
                    "Encryption should be banned because criminals use it.",
                    "All personal data should be publicly accessible.",
                ]},
                {"type": "reading_comprehension", "instruction": "Answer based on the unit reading text.", "items": [
                    "What does Zuboff mean by 'prediction products'?",
                    "How do tech companies exploit jurisdictional gaps?",
                    "What is the 'right to erasure' under the GDPR?",
                    "Why do privacy advocates support end-to-end encryption?",
                    "How does surveillance capitalism threaten autonomy?",
                    "What cultural shift does the author argue is necessary?",
                ]},
                {"type": "debate_preparation", "instruction": "Prepare arguments for and against each statement.", "items": [
                    "Governments should have the right to access encrypted communications.",
                    "Social media companies should be liable for data breaches.",
                    "Biometric data collection should be banned in schools.",
                    "The right to privacy is absolute and cannot be overridden.",
                    "Companies that violate data protection laws should face criminal prosecution.",
                    "Users who agree to terms of service have consented to data collection.",
                ]},
                {"type": "writing", "instruction": "Write a paragraph (100-120 words).", "items": [
                    "Argue for or against mandatory data protection education in schools.",
                    "Evaluate the effectiveness of the GDPR in protecting user privacy.",
                    "Discuss whether convenience or privacy should take priority in app design.",
                    "Propose a policy to protect children's data online.",
                    "Compare government surveillance in democratic and authoritarian states.",
                    "Explain why the concept of 'informed consent' is problematic in digital contexts.",
                ]},
            ],
        },
        4: {
            "exercises": [
                {"type": "transformation", "instruction": "Rewrite using inverted conditionals (remove 'if').", "items": [
                    "If I had known about the deadline, I would have applied.",
                    "If she were offered the scholarship, she would accept immediately.",
                    "If they should encounter difficulties, they must contact the supervisor.",
                    "If we had invested earlier, the results would be different now.",
                    "If the evidence were stronger, the conclusion would be more convincing.",
                    "If he had not been so persistent, the discovery would not have been made.",
                ]},
                {"type": "register_shift", "instruction": "Rewrite in the specified register.", "items": [
                    "Kids who don't read do worse at school. (Academic register)",
                    "The implementation of pedagogical reform necessitates stakeholder consultation. (Informal)",
                    "The guy basically proved his theory was right. (Academic register)",
                    "Notwithstanding the aforementioned limitations, the methodology remains robust. (Informal)",
                    "Lots of people think grammar doesn't matter anymore. (Academic register)",
                    "The empirical evidence substantiates the hypothesis conclusively. (Journalistic register)",
                ]},
                {"type": "gap_fill", "instruction": "Complete with the correct subjunctive or conditional form.", "items": [
                    "The committee recommended that the proposal ___ (accept) without amendment.",
                    "Were the data ___ (be) more reliable, the conclusions would carry greater weight.",
                    "It is essential that every student ___ (complete) the ethics training.",
                    "Had the researchers ___ (anticipate) the variable, the results might have differed.",
                    "The chair insisted that all delegates ___ (remain) seated during the vote.",
                    "Should the experiment ___ (yield) unexpected results, the protocol must be revised.",
                ]},
                {"type": "analysis", "instruction": "Identify the register of each passage and justify your answer.", "items": [
                    "The longitudinal analysis yielded statistically significant results across all cohorts.",
                    "So basically, they found that the thing works, which is pretty cool.",
                    "Sources familiar with the negotiations said talks had reached an impasse.",
                    "Pursuant to Regulation 7(b), all parties shall comply with the revised schedule.",
                    "It seems like the experiment kinda worked, but there were some issues.",
                    "The findings, while preliminary, suggest a promising avenue for further investigation.",
                ]},
                {"type": "writing", "instruction": "Write the same content in three different registers (2-3 sentences each).", "items": [
                    "Topic: The impact of social media on mental health. (Academic, Journalistic, Informal)",
                    "Topic: A new study on bilingualism and brain function. (Academic, Journalistic, Informal)",
                    "Topic: Government plans to increase renewable energy. (Academic, Journalistic, Informal)",
                    "Topic: The discovery of a new species in the Amazon. (Academic, Journalistic, Informal)",
                    "Topic: University tuition fees should be abolished. (Academic, Journalistic, Informal)",
                    "Topic: AI is changing the way we work. (Academic, Journalistic, Informal)",
                ]},
            ],
        },
        5: {
            "exercises": [
                {"type": "literary_analysis", "instruction": "Identify the narrative technique and explain its effect.", "items": [
                    "Pamuk's use of a retrospective narrator reconstructing events from notebooks.",
                    "Morrison's stream-of-consciousness passages in 'Beloved.'",
                    "Marquez's use of circular time in 'One Hundred Years of Solitude.'",
                    "Ishiguro's unreliable narrator in 'The Remains of the Day.'",
                    "Alexievich's polyphonic assembly of oral testimonies.",
                    "Gurnah's shifting between past and present tense to signal displacement.",
                ]},
                {"type": "vocabulary", "instruction": "Use each word in a sentence about literature.", "items": [
                    "canonical", "polyphonic", "melancholy", "testimony", "resilience", "nostalgia",
                ]},
                {"type": "rhetorical_devices", "instruction": "Write a sentence using the specified device.", "items": [
                    "Parallelism about the power of reading.",
                    "Antithesis contrasting fiction and reality.",
                    "Tricolon describing what literature teaches us.",
                    "Anaphora about why we read.",
                    "Asyndeton listing qualities of great prose.",
                    "Rhetorical question about the purpose of the Nobel Prize.",
                ]},
                {"type": "comparative", "instruction": "Write two sentences comparing the given pair.", "items": [
                    "Pamuk's use of place vs. Morrison's use of memory.",
                    "Marquez's magical realism vs. Ishiguro's quiet realism.",
                    "Alexievich's non-fiction vs. Gurnah's fiction approach to historical trauma.",
                    "Morrison's fragmented syntax vs. Pamuk's elaborate syntax.",
                    "The Nobel Prize's European bias vs. its power to amplify marginalised voices.",
                    "Literature as entertainment vs. literature as witness.",
                ]},
                {"type": "writing", "instruction": "Write a literary analysis paragraph (100-120 words).", "items": [
                    "Analyse how one Nobel laureate uses language to convey the experience of exile.",
                    "Compare how two authors use syntax to create different emotional effects.",
                    "Discuss whether the Nobel Prize helps or hinders literary diversity.",
                    "Evaluate Morrison's claim that language is 'a political act.'",
                    "Analyse the role of memory in a novel you have studied.",
                    "Argue whether great literature must address social or political themes.",
                ]},
            ],
        },
        6: {
            "exercises": [
                {"type": "vocabulary", "instruction": "Complete with the correct diplomatic/IR term.", "items": [
                    "A ___ agreement involves only two countries, while a ___ one involves three or more.",
                    "The principle of ___ means that countries govern themselves without external interference.",
                    "A country that has signed a treaty is called a ___.",
                    "___ is the policy of avoiding involvement in international affairs.",
                    "The Paris Agreement relies on nationally ___ contributions from each country.",
                    "Building ___ among diverse nations requires patience and compromise.",
                ]},
                {"type": "modal_verbs", "instruction": "Complete with appropriate modal verbs for diplomatic hedging.", "items": [
                    "The delegation ___ propose an amendment to Article 7.",
                    "It ___ be advisable to reconsider the timeline for implementation.",
                    "Member states ___ to comply with the agreed-upon framework.",
                    "The committee ___ wish to note that further consultation is necessary.",
                    "This resolution ___ not be interpreted as a precedent for future action.",
                    "We ___ recommend that the working group reconvene in September.",
                ]},
                {"type": "gap_fill", "instruction": "Complete the diplomatic phrases.", "items": [
                    "With ___ to the delegate from France, we must respectfully disagree.",
                    "The motion is ___ of order and cannot be debated at this time.",
                    "The chair ___ the floor to the representative of Turkey.",
                    "We call ___ all parties to exercise restraint and return to negotiations.",
                    "The draft resolution has been ___ to include the proposed amendments.",
                    "This delegation reserves the ___ to revisit this matter at a later date.",
                ]},
                {"type": "analysis", "instruction": "Analyse the diplomatic language in each statement.", "items": [
                    "'We would welcome a constructive dialogue on this matter.'",
                    "'The delegation expresses its grave concern regarding recent developments.'",
                    "'We note with interest the proposal put forward by the distinguished delegate.'",
                    "'It is the view of this delegation that further delay would be inadvisable.'",
                    "'We reiterate our commitment to the principles enshrined in the charter.'",
                    "'The resolution, while commendable in its ambition, may lack practical enforceability.'",
                ]},
                {"type": "writing", "instruction": "Write in diplomatic register (100-120 words).", "items": [
                    "Draft an opening statement for a MUN committee on climate change.",
                    "Write a formal objection to a proposed amendment.",
                    "Compose a closing statement summarising your delegation's position.",
                    "Write a press release announcing a bilateral agreement.",
                    "Draft a letter from one head of state to another proposing cooperation.",
                    "Write a position statement on the role of youth in international diplomacy.",
                ]},
            ],
        },
        7: {
            "exercises": [
                {"type": "vocabulary", "instruction": "Match each quantum computing term with its definition.", "items": [
                    "superposition — (a) loss of quantum state (b) existing in multiple states (c) linking particles",
                    "entanglement — (a) quantum connection between particles (b) error correction (c) classical computing",
                    "decoherence — (a) quantum advantage (b) loss of quantum information (c) particle acceleration",
                    "qubit — (a) classical bit (b) quantum bit (c) encryption key",
                    "fault-tolerant — (a) operating despite errors (b) faster processing (c) lower temperature",
                    "nascent — (a) fully developed (b) just emerging (c) declining",
                ]},
                {"type": "cohesion", "instruction": "Improve cohesion using substitution, ellipsis, or reference.", "items": [
                    "Quantum computers use qubits. Qubits can exist in superposition. Superposition allows parallel processing.",
                    "The first experiment tested Algorithm A. The second experiment tested Algorithm B.",
                    "She explained superposition. He explained entanglement. They both explained decoherence.",
                    "Classical computers cannot solve the problem. Quantum computers can solve the problem.",
                    "The processor operates at 15 millikelvin. The temperature of 15 millikelvin is colder than space.",
                    "Google achieved quantum supremacy. IBM disputed that Google achieved quantum supremacy.",
                ]},
                {"type": "analogy_creation", "instruction": "Create an analogy to explain each concept to a non-specialist.", "items": [
                    "Superposition", "Entanglement", "Decoherence",
                    "Quantum supremacy", "Error correction", "Qubit vs. classical bit",
                ]},
                {"type": "reading_comprehension", "instruction": "Answer based on the unit reading.", "items": [
                    "Why does the author call quantum computing a 'paradigm shift'?",
                    "What is Shor's algorithm and why does it matter?",
                    "Explain the 'noisy intermediate-scale' phase.",
                    "How is quantum computing epistemological as well as technological?",
                    "What practical applications are mentioned?",
                    "Why is the race for quantum-resistant encryption urgent?",
                ]},
                {"type": "writing", "instruction": "Write a paragraph (100-120 words).", "items": [
                    "Explain quantum superposition to a ten-year-old.",
                    "Argue whether quantum computing will democratise or concentrate power.",
                    "Discuss the ethical implications of breaking current encryption.",
                    "Compare classical and quantum computing using an extended analogy.",
                    "Evaluate Turkey's potential role in the quantum technology landscape.",
                    "Propose a school-level project related to quantum computing concepts.",
                ]},
            ],
        },
        8: {
            "exercises": [
                {"type": "vocabulary", "instruction": "Use each term in a sentence about visual art.", "items": [
                    "installation", "commodification", "avant-garde", "monochrome", "perspectival", "curate",
                ]},
                {"type": "fronting", "instruction": "Rewrite using fronting for emphasis.", "items": [
                    "I find this interpretation entirely convincing.",
                    "We will address the political dimensions in the next section.",
                    "The emotional impact of the work is more significant than its technical skill.",
                    "The committee considered the exhibition proposal inadequate.",
                    "Artists have never had greater access to global audiences.",
                    "The boundary between art and activism has become increasingly blurred.",
                ]},
                {"type": "art_analysis", "instruction": "Write two sentences analysing each artwork's message and technique.", "items": [
                    "Picasso's Guernica", "Banksy's 'Girl with Balloon'", "Ai Weiwei's 'Sunflower Seeds'",
                    "Kara Walker's silhouettes", "Shirin Neshat's photography", "A Turkish miniature painting",
                ]},
                {"type": "gap_fill", "instruction": "Complete with appropriate art criticism vocabulary.", "items": [
                    "The ___ of the work lies in its ability to provoke discomfort without resorting to shock.",
                    "The artist's use of ___ creates a sense of depth and spatial complexity.",
                    "The exhibition was ___ by a team of international specialists.",
                    "Street art challenges the ___ of public space and artistic ownership.",
                    "The ___ between beauty and violence is central to the artist's practice.",
                    "Digital art raises questions about ___ and the definition of an original work.",
                ]},
                {"type": "writing", "instruction": "Write a paragraph (100-120 words).", "items": [
                    "Write an artist statement for an imaginary artwork you would create.",
                    "Compare two artworks that address the same social issue differently.",
                    "Argue for or against the claim that 'all art is political.'",
                    "Describe how a specific artwork changed your perspective on an issue.",
                    "Evaluate whether NFTs represent a positive development for artists.",
                    "Discuss the role of art in Turkish cultural identity.",
                ]},
            ],
        },
        9: {
            "exercises": [
                {"type": "vocabulary", "instruction": "Complete with the correct health governance term.", "items": [
                    "Disease ___ systems enable early detection of outbreaks.",
                    "The WHO's greatest achievement was the ___ of smallpox.",
                    "Vaccine ___ between rich and poor nations prolonged the pandemic.",
                    "___ resistance is sometimes called the 'silent pandemic.'",
                    "The Pandemic Treaty aims to ___ lessons from COVID-19 into binding commitments.",
                    "Social ___ of health include poverty, education, and housing.",
                ]},
                {"type": "transformation", "instruction": "Complete each key word transformation.", "items": [
                    "'People believe the treaty will succeed.' BELIEVED -> The treaty ___ succeed.",
                    "'The moment the results arrived, the team celebrated.' SOONER -> No ___ the team celebrated.",
                    "'The WHO established the programme.' IT -> ___ the programme.",
                    "'She had barely finished speaking when the alarm sounded.' BARELY -> ___ when the alarm sounded.",
                    "'Without funding, the project will fail.' WERE -> ___ the project would fail.",
                    "'Everyone acknowledges the severity of AMR.' WIDELY -> The severity of AMR ___.",
                ]},
                {"type": "reading_comprehension", "instruction": "Answer based on the unit reading.", "items": [
                    "What principle did the International Sanitary Conferences establish?",
                    "Why is the WHO vulnerable to donor influence?",
                    "What failures did the Ebola outbreak expose?",
                    "What is the 'One Health' approach?",
                    "Why do critics warn against 'securitising' health?",
                    "What does the author mean by 'civilisational maturity'?",
                ]},
                {"type": "policy_analysis", "instruction": "Evaluate each policy proposal.", "items": [
                    "Mandatory vaccination for all school-age children.",
                    "A global tax on pharmaceutical companies to fund pandemic preparedness.",
                    "Open-source sharing of all pandemic-related research data.",
                    "Community health worker programmes in every country.",
                    "Intellectual property waivers for vaccines during pandemics.",
                    "A standing UN pandemic response force.",
                ]},
                {"type": "writing", "instruction": "Write a paragraph (100-120 words).", "items": [
                    "Argue for or against intellectual property waivers during health emergencies.",
                    "Evaluate the WHO's response to a pandemic of your choice.",
                    "Discuss how misinformation threatens public health outcomes.",
                    "Propose a policy to address antimicrobial resistance.",
                    "Compare the health systems of two countries you have studied.",
                    "Discuss whether health is a human right or a commodity.",
                ]},
            ],
        },
        10: {
            "exercises": [
                {"type": "vocabulary", "instruction": "Complete with the correct green technology term.", "items": [
                    "The ___ cost of solar energy has fallen by 90% since 2010.",
                    "Battery storage addresses the ___ of wind and solar power.",
                    "___ involves splitting water into hydrogen and oxygen using electricity.",
                    "The concept of a 'just ___' ensures workers are not left behind.",
                    "Turkey has the potential to become a green hydrogen ___.",
                    "___ economy principles promote reuse, repair, and recycling.",
                ]},
                {"type": "integrated_grammar", "instruction": "Rewrite using the structure indicated.", "items": [
                    "Solar costs have fallen dramatically. (Cleft: It is...)",
                    "If countries had invested earlier, emissions would be lower. (Inversion: Had...)",
                    "The transition requires political courage. (Fronting: What the transition requires...)",
                    "Experts believe green hydrogen will transform heavy industry. (Passive reporting: Green hydrogen...)",
                    "Despite challenges, the economics favour renewables. (Concessive nominalization: Notwithstanding...)",
                    "Countries must act now or face catastrophic consequences. (Inverted conditional: Should countries fail to act...)",
                ]},
                {"type": "data_interpretation", "instruction": "Write a sentence describing each trend.", "items": [
                    "Solar PV cost: $0.36/kWh (2010) -> $0.04/kWh (2024)",
                    "Global wind capacity: 200 GW (2010) -> 900 GW (2024)",
                    "Battery costs: $1,100/kWh (2010) -> $140/kWh (2024)",
                    "EV market share: 1% (2015) -> 18% (2024)",
                    "Turkey solar capacity: 40 MW (2013) -> 11,000 MW (2024)",
                    "Green hydrogen cost projection: $5/kg (2020) -> $1.50/kg (2030)",
                ]},
                {"type": "debate_preparation", "instruction": "Prepare arguments for and against.", "items": [
                    "Nuclear energy should be part of the green transition.",
                    "Carbon taxes are the most effective tool for reducing emissions.",
                    "Developing nations should not be expected to decarbonise at the same rate.",
                    "Individual consumer choices matter more than government policy.",
                    "Fossil fuel companies should pay reparations for climate damage.",
                    "Green hydrogen will replace natural gas within twenty years.",
                ]},
                {"type": "writing", "instruction": "Write a paragraph (100-120 words).", "items": [
                    "Evaluate Turkey's potential as a green hydrogen exporter.",
                    "Argue for or against nuclear energy as part of the energy transition.",
                    "Discuss whether individual action or government policy is more effective for climate change.",
                    "Propose a green technology solution for your community.",
                    "Reflect on what you have learned this year and how it has changed your thinking.",
                    "Write a letter to a future student recommending one thing they should learn from this course.",
                ]},
            ],
        },
    },
}

# ===========================================================================
# TURKEY_CORNER_BANK
# ===========================================================================
TURKEY_CORNER_BANK = {
    12: {
        1: {"title": "Turkish Universities on the World Stage", "text": "Turkey's higher education system has grown rapidly, with over 200 universities. Institutions such as Bogazici, METU, Koc and Sabanci regularly appear in global rankings. Turkish universities offer programmes in English, attracting international students. Research output has increased significantly, particularly in engineering, medicine and social sciences. The YOK (Council of Higher Education) oversees quality assurance. Turkey's Bologna Process alignment means degrees are recognised across Europe. Many graduates pursue postgraduate studies at leading institutions worldwide.", "image_desc": "Bogazici University campus overlooking the Bosphorus", "discussion_q": "What factors should students consider when choosing a university?"},
        2: {"title": "Turkish Literary Tradition", "text": "Turkey has a rich literary heritage spanning centuries. From Yunus Emre's mystical poetry in the 13th century to Orhan Pamuk's Nobel Prize in 2006, Turkish literature reflects the nation's cultural evolution. The transition from Ottoman script to Latin alphabet in 1928 transformed written expression. Modern Turkish authors like Elif Safak write in both Turkish and English, reaching global audiences. The Istanbul International Book Fair is one of Europe's largest. Poetry remains deeply embedded in Turkish culture, with poems recited at gatherings and celebrations.", "image_desc": "Portrait of Orhan Pamuk with his Nobel Prize medal", "discussion_q": "How does a country's literature reflect its cultural identity?"},
        3: {"title": "Turkey's Cybersecurity Infrastructure", "text": "Turkey has invested heavily in cybersecurity, establishing the National Cyber Incidents Response Centre (USOM) and BTK as regulatory bodies. Turkish universities offer specialised programmes in information security. The country hosts annual cybersecurity exercises and hackathons. Turkey's National Cyber Security Strategy aims to protect critical infrastructure including energy, finance and telecommunications. Turkish tech companies like Havelsan and ASELSAN develop indigenous cybersecurity solutions. The growing digital economy has made cybersecurity a national priority.", "image_desc": "Turkey's national cybersecurity operations centre", "discussion_q": "Why is cybersecurity increasingly important for national security?"},
        4: {"title": "The Evolution of Turkish Language", "text": "The Turkish language has undergone remarkable transformations. The 1928 alphabet reform replaced Arabic script with Latin letters, dramatically increasing literacy. The Turkish Language Association (TDK) was established to standardise and modernise the language. Turkish belongs to the Turkic language family, with mutual intelligibility with Azerbaijani and Turkmen. The language has absorbed loanwords from Arabic, Persian, French and English throughout history. Today, Turkish is spoken by approximately 80 million people and is gaining learners worldwide through cultural exports like television dramas.", "image_desc": "Historical comparison of Ottoman and modern Turkish scripts", "discussion_q": "How do language reforms shape a nation's cultural development?"},
        5: {"title": "Turkish Nobel Laureates and Literary Icons", "text": "Orhan Pamuk became the first Turkish Nobel laureate in Literature in 2006. His novels, including 'My Name is Red' and 'Snow', explore the tension between East and West, tradition and modernity. Aziz Sancar, a Turkish-American biochemist, won the Nobel Prize in Chemistry in 2015 for his work on DNA repair mechanisms. These achievements demonstrate Turkey's intellectual contributions to global culture and science. Other influential Turkish thinkers include sociologist Zygmunt Bauman and philosopher Hilmi Ziya Ulken.", "image_desc": "Orhan Pamuk and Aziz Sancar at their Nobel ceremonies", "discussion_q": "How do Nobel Prize winners inspire future generations?"},
        6: {"title": "Turkey's Role in International Diplomacy", "text": "Turkey occupies a unique geopolitical position bridging Europe and Asia. As a NATO member since 1952 and EU candidate, Turkey plays a significant role in international diplomacy. The country has mediated conflicts in the Middle East, hosted millions of refugees, and contributed to UN peacekeeping missions. Turkey's G20 presidency in 2015 addressed global economic challenges. The country's foreign policy balances Western alliances with regional partnerships. Istanbul and Antalya regularly host international summits and diplomatic conferences.", "image_desc": "Aerial view of the G20 summit venue in Antalya", "discussion_q": "How does geography influence a country's diplomatic role?"},
        7: {"title": "Turkey's Technology Sector", "text": "Turkey's technology sector has experienced rapid growth, with Istanbul becoming a significant startup hub. Turkish engineers have contributed to projects ranging from satellite development to autonomous vehicles. TUBITAK, the Scientific and Technological Research Council, funds innovation across sectors. Turkey's first domestically developed car, TOGG, represents the country's ambitions in electric vehicle technology. The Teknofest festival showcases young Turkish innovators. Universities like ITU and Bilkent produce graduates who work at major global technology companies.", "image_desc": "TOGG electric vehicle at its unveiling ceremony", "discussion_q": "How can developing countries build competitive technology sectors?"},
        8: {"title": "Turkish Arts: From Miniatures to Contemporary", "text": "Turkish visual arts span from Ottoman miniature painting to cutting-edge contemporary installations. The Istanbul Biennial, established in 1987, is one of the world's most prestigious contemporary art events. Turkish artists like Fahrelnissa Zeid and Burhan Dogancay have achieved international recognition. Traditional arts including ebru (marbling), calligraphy and ceramic work are UNESCO-listed. The Istanbul Modern museum, opened in 2004, bridges traditional and contemporary aesthetics. Art galleries in Istanbul, Ankara and Izmir showcase emerging talent alongside established masters.", "image_desc": "Istanbul Modern museum exterior on the Bosphorus waterfront", "discussion_q": "How do traditional arts influence contemporary artistic expression?"},
        9: {"title": "Turkey's Healthcare System", "text": "Turkey transformed its healthcare system through reforms beginning in 2003. Universal health coverage now reaches over 99% of the population. The country has become a leading destination for medical tourism, particularly in ophthalmology, dentistry and cosmetic surgery. Turkish hospitals use advanced technology and many doctors train abroad. The COVID-19 pandemic accelerated telemedicine adoption. Turkey developed its own vaccine, TURKOVAC. City hospitals built in major cities provide comprehensive care. Turkey's pharmaceutical industry exports to over 150 countries.", "image_desc": "Modern city hospital complex in Istanbul", "discussion_q": "What are the key features of an effective healthcare system?"},
        10: {"title": "Turkey's Green Energy Transition", "text": "Turkey is investing significantly in renewable energy. The country's installed wind capacity has grown from 20 MW in 2002 to over 11,000 MW. Turkey has the world's fourth-largest geothermal energy capacity. The Karapinar Solar Power Plant is one of Europe's largest. Turkey aims to achieve net-zero emissions by 2053. Hydroelectric power has long been a major energy source, with dams across Anatolia. The country's diverse geography provides excellent potential for solar, wind and geothermal energy. Green hydrogen projects are under development.", "image_desc": "Karapinar Solar Power Plant aerial view", "discussion_q": "What role should developing countries play in the global green energy transition?"}
    }
}

# ===========================================================================
# GAMIFICATION_BANK
# ===========================================================================
GAMIFICATION_BANK = {
    12: {
        "levels": [
            {"level": 1, "title": "Academic Apprentice", "xp_needed": 0},
            {"level": 2, "title": "Critical Analyst", "xp_needed": 800},
            {"level": 3, "title": "Research Scholar", "xp_needed": 2000},
            {"level": 4, "title": "Academic Author", "xp_needed": 4000},
            {"level": 5, "title": "Language Master", "xp_needed": 7000},
        ],
        "unit_badges": {
            1: {"name": "University Ready", "desc": "Demonstrated academic English proficiency."},
            2: {"name": "Critical Writer", "desc": "Produced analytical writing with evidence."},
            3: {"name": "Digital Guardian", "desc": "Analysed cybersecurity and privacy issues."},
            4: {"name": "Syntax Expert", "desc": "Mastered advanced grammatical structures."},
            5: {"name": "Literary Critic", "desc": "Analysed Nobel Prize-winning literature."},
            6: {"name": "Global Diplomat", "desc": "Debated international relations topics."},
            7: {"name": "Tech Visionary", "desc": "Explored quantum computing concepts."},
            8: {"name": "Art Connoisseur", "desc": "Analysed and critiqued visual arts."},
            9: {"name": "Health Advocate", "desc": "Researched global health challenges."},
            10: {"name": "Green Innovator", "desc": "Proposed sustainable technology solutions."},
        },
        "bonus_xp": [
            {"task": "Write a 500-word academic essay with proper citations", "xp": 300},
            {"task": "Deliver a 5-minute presentation on a research topic", "xp": 250},
            {"task": "Lead a class debate on a controversial issue", "xp": 200},
            {"task": "Create an annotated bibliography of 10 sources", "xp": 150},
            {"task": "Peer-review a classmate's essay with detailed feedback", "xp": 100},
        ],
    }
}

# ===========================================================================
# MISSION_BANK
# ===========================================================================
MISSION_BANK = {
    12: {
        1: {"title": "University Application Portfolio", "objective": "Create a mock university application portfolio in English.", "tasks": ["Write a personal statement of 300-400 words.", "Prepare a CV highlighting academic achievements.", "Draft a motivation letter for your chosen programme.", "Conduct a mock interview with a partner."], "reward": "University Ready Badge + 300 XP"},
        2: {"title": "Op-Ed Publication", "objective": "Write a persuasive opinion piece on a current issue.", "tasks": ["Choose a controversial topic and research multiple perspectives.", "Write a 400-word op-ed with evidence and counter-arguments.", "Peer-review a classmate's op-ed and provide feedback.", "Revise based on feedback and present to class."], "reward": "Published Writer Badge + 300 XP"},
        3: {"title": "Digital Security Audit", "objective": "Conduct a personal digital security assessment.", "tasks": ["Audit your online accounts for security vulnerabilities.", "Research best practices for password management and 2FA.", "Create a personal cybersecurity action plan.", "Present your findings and recommendations to the class."], "reward": "Cyber Guardian Badge + 300 XP"},
        4: {"title": "Grammar Masterclass", "objective": "Create a grammar reference guide for younger students.", "tasks": ["Select 10 advanced grammar topics covered this year.", "Write clear explanations with examples for each topic.", "Design practice exercises with answer keys.", "Test your guide with younger students and revise."], "reward": "Grammar Guru Badge + 300 XP"},
        5: {"title": "Literary Analysis Symposium", "objective": "Present a critical analysis of a Nobel Prize-winning work.", "tasks": ["Read a short work by a Nobel laureate.", "Analyse themes, style and cultural context.", "Write a 500-word critical essay.", "Present your analysis in a class symposium."], "reward": "Literary Scholar Badge + 300 XP"},
        6: {"title": "Model United Nations", "objective": "Participate in a class Model UN simulation.", "tasks": ["Research your assigned country's foreign policy positions.", "Prepare a position paper on a global issue.", "Deliver a speech representing your country.", "Negotiate a resolution with other delegates."], "reward": "Diplomat Badge + 300 XP"},
        7: {"title": "Future Tech Presentation", "objective": "Research and present an emerging technology.", "tasks": ["Choose a cutting-edge technology topic.", "Research current developments and future potential.", "Create a multimedia presentation.", "Answer audience questions and lead discussion."], "reward": "Tech Pioneer Badge + 300 XP"},
        8: {"title": "Art Exhibition Curator", "objective": "Curate a virtual art exhibition with critical commentary.", "tasks": ["Select 8-10 artworks from different periods and cultures.", "Write gallery notes for each piece (100 words each).", "Design the exhibition layout and theme.", "Present your curation choices and rationale."], "reward": "Curator Badge + 300 XP"},
        9: {"title": "Health Policy Brief", "objective": "Write a policy brief on a global health issue.", "tasks": ["Research a current global health challenge.", "Analyse existing policies and their effectiveness.", "Propose evidence-based recommendations.", "Present your policy brief in a stakeholder simulation."], "reward": "Policy Analyst Badge + 300 XP"},
        10: {"title": "Green Innovation Pitch", "objective": "Develop and pitch a green technology solution.", "tasks": ["Identify an environmental problem in your community.", "Research existing green technology solutions.", "Design an innovative solution with feasibility analysis.", "Pitch your solution to a panel of judges."], "reward": "Green Innovator Badge + 300 XP"}
    }
}

# ===========================================================================
# STEAM_BANK
# ===========================================================================
STEAM_BANK = {
    12: {
        1: {"title": "Academic Writing Workshop", "subject_link": "English + Research Methods", "activity": "Practise academic writing conventions through a mini research project.", "materials": ["academic journals", "citation guide", "word processor", "peer review rubric"], "steps": ["Choose a research question related to education.", "Find and evaluate 5 academic sources.", "Write a 400-word literature review section.", "Apply proper APA citation format.", "Peer-review a classmate's work using the rubric."], "learning_outcome": "Apply academic writing and research skills to produce scholarly text."},
        2: {"title": "Data-Driven Argumentation", "subject_link": "Mathematics + English + Statistics", "activity": "Use statistical data to support written arguments.", "materials": ["data sets", "spreadsheet software", "graph paper", "calculator"], "steps": ["Choose a social issue and find relevant statistics.", "Create charts and graphs to visualise the data.", "Write an analytical essay incorporating data evidence.", "Evaluate the reliability of your sources.", "Present findings with visual aids."], "learning_outcome": "Integrate quantitative evidence into analytical writing."},
        3: {"title": "Encryption and Cryptography", "subject_link": "Mathematics + Computer Science", "activity": "Explore the mathematics behind encryption.", "materials": ["paper", "calculator", "computer", "cipher wheel template"], "steps": ["Learn about Caesar cipher and frequency analysis.", "Encrypt and decrypt messages using substitution ciphers.", "Research how RSA encryption uses prime numbers.", "Create a presentation on modern encryption methods.", "Discuss the balance between security and privacy."], "learning_outcome": "Understand mathematical principles underlying digital security."},
        4: {"title": "Linguistic Analysis Project", "subject_link": "Linguistics + English + Data Analysis", "activity": "Analyse language patterns using corpus linguistics methods.", "materials": ["text corpus", "word frequency tools", "spreadsheet", "academic articles"], "steps": ["Select a corpus of English texts.", "Analyse word frequency, collocations and patterns.", "Compare formal and informal registers.", "Create visualisations of linguistic data.", "Write a report on your findings."], "learning_outcome": "Apply analytical methods to study language structure and use."},
        5: {"title": "Comparative Literature Map", "subject_link": "Literature + Geography + History", "activity": "Create an interactive map linking Nobel laureates to their cultural contexts.", "materials": ["world map", "research materials", "coloured pins", "summary cards"], "steps": ["Research 10 Nobel Prize winners in Literature.", "Map their countries and cultural backgrounds.", "Identify common themes across cultures.", "Create summary cards with key works and themes.", "Present patterns and connections discovered."], "learning_outcome": "Connect literary works to geographical and historical contexts."},
        6: {"title": "Geopolitical Simulation", "subject_link": "Political Science + Geography + Economics", "activity": "Simulate international negotiations on a global issue.", "materials": ["country profiles", "negotiation framework", "position papers", "voting cards"], "steps": ["Assign countries and research their positions.", "Prepare position papers with evidence.", "Conduct multi-round negotiations.", "Draft a resolution incorporating compromises.", "Reflect on the diplomacy process."], "learning_outcome": "Apply knowledge of international relations to simulated diplomacy."},
        7: {"title": "Quantum Concepts Visualisation", "subject_link": "Physics + Art + Computer Science", "activity": "Create visual representations of quantum computing concepts.", "materials": ["art supplies", "digital design tools", "physics references", "presentation software"], "steps": ["Research quantum superposition and entanglement.", "Create visual metaphors for quantum concepts.", "Design an infographic explaining quantum vs classical computing.", "Build a simple logic gate demonstration.", "Present your visualisations with explanations."], "learning_outcome": "Translate complex scientific concepts into accessible visual formats."},
        8: {"title": "Art and Mathematics: The Golden Ratio", "subject_link": "Art + Mathematics", "activity": "Investigate the golden ratio in art and nature.", "materials": ["compass", "ruler", "art prints", "calculator", "camera"], "steps": ["Calculate the golden ratio and Fibonacci sequence.", "Find examples in famous artworks and architecture.", "Photograph examples of the golden ratio in nature.", "Create an original artwork using golden ratio proportions.", "Present your findings on mathematics in aesthetics."], "learning_outcome": "Explore the intersection of mathematical principles and artistic beauty."},
        9: {"title": "Epidemiological Modelling", "subject_link": "Mathematics + Biology + Public Health", "activity": "Create simple disease spread models using mathematical concepts.", "materials": ["spreadsheet software", "graph paper", "calculator", "epidemiology data"], "steps": ["Learn basic SIR model concepts.", "Input parameters and calculate disease spread scenarios.", "Graph different intervention outcomes.", "Compare your models with real-world pandemic data.", "Write a report on the role of modelling in public health."], "learning_outcome": "Apply mathematical modelling to understand disease dynamics."},
        10: {"title": "Sustainable Design Challenge", "subject_link": "Engineering + Environmental Science + Economics", "activity": "Design a sustainable product or system for your school.", "materials": ["design software or paper", "recycled materials", "cost calculator", "sustainability metrics"], "steps": ["Audit your school's environmental impact.", "Identify one area for improvement.", "Design a sustainable solution with cost analysis.", "Build a prototype or detailed plan.", "Present to school administration with ROI analysis."], "learning_outcome": "Apply engineering design principles to create sustainable solutions."}
    }
}

# ===========================================================================
# SONG_BANK
# ===========================================================================
SONG_BANK = {
    12: {
        1: {
            "title": "The Spark (University Readiness Ode)",
            "lyrics": (
                "'The brain is not merely an organ,' the lecturer began,\n"
                "'It is the universe folded into the span of a man.'\n"
                "Elif scribbled the phrase, Kerem streamed the hall,\n"
                "Sofia cross-referenced, Deniz sketched it all.\n"
                "This final year is not a finish line,\n"
                "It is the launchpad where our questions shine.\n"
                "Pursue the thing that keeps you up at night,\n"
                "And let that spark become your guiding light."
            ),
            "activity": "Students write a personal 'spark' verse about the academic question that drives them most. Share in a Commencement Poetry Circle and discuss common themes."
        },
        2: {
            "title": "The Pen and the Sword (Analytical Writing Rap)",
            "lyrics": (
                "Every sloppy sentence is a small dishonesty,\n"
                "Orwell warned us: language bends reality.\n"
                "Rhetoric can heal or rhetoric can harm,\n"
                "The most dangerous lies wear truth's own charm.\n"
                "Dissect the discourse, marshal the evidence tight,\n"
                "Clarity demands more courage than being right.\n"
                "So sharpen your pen and choose your words with care,\n"
                "Because honest writing is the rarest form of prayer."
            ),
            "activity": "Students find a piece of public discourse and write an eight-line analytical response verse, identifying at least two rhetorical strategies. Present as a spoken-word rebuttal."
        },
        3: {
            "title": "Firewall (Cybersecurity Spoken Word)",
            "lyrics": (
                "Zero-day vulnerability at three a.m.,\n"
                "A breach that turns convenience into mayhem.\n"
                "Privacy is not a luxury, it's the scaffolding of self,\n"
                "Without autonomy, freedom sits upon a shelf.\n"
                "Knowledge is the first firewall we raise,\n"
                "Awareness is the armour for digital days.\n"
                "Patch the code, report the flaw, speak loud and clear,\n"
                "Cybersecurity is personal — and the threat is here."
            ),
            "activity": "Students audit one of their own online accounts for security weaknesses and write a verse about what they found. Anonymise and share in a Digital Awareness Gallery."
        },
        4: {
            "title": "Syntax Architect (Grammar Verse)",
            "lyrics": (
                "One hundred words, perfectly grammatical and long,\n"
                "'Now reduce to twelve' — the professor's challenge song.\n"
                "Nominalization shifts the agent out of view,\n"
                "'The government decided' becomes a noun in lieu.\n"
                "Every syntactic choice carries ethical weight,\n"
                "Register and clause can liberate or legislate.\n"
                "Tabloid, broadsheet, journal — pick your frame,\n"
                "Language shapes the thought; the words are not the same."
            ),
            "activity": "Students take a single news event and write it in three registers: tabloid headline, broadsheet paragraph, and academic abstract. Present all three and discuss how syntax changes meaning."
        },
        5: {
            "title": "The Laureate's Echo (Nobel Literature Poem)",
            "lyrics": (
                "Cedarwood and history perfume the reading hall,\n"
                "A Nobel voice recounts the exile's call.\n"
                "How do you decide what a character conceals?\n"
                "'The same way you decide in life,' she reveals.\n"
                "Pamuk weaves the melancholy of a vanished throne,\n"
                "Morrison sings collective memory's undertone.\n"
                "Literature does not merely mirror what we see,\n"
                "It shows us who we are and who we could still be."
            ),
            "activity": "Students choose a Nobel laureate and write a six-line tribute poem that captures the author's central theme. Compile into a class Nobel Anthology."
        },
        6: {
            "title": "The Diplomacy of Modal Verbs (International Relations Verse)",
            "lyrics": (
                "'A virus does not recognise a passport,' Sofia said,\n"
                "'Neither should a vaccine' — and the chamber bowed its head.\n"
                "Might and could with such conviction softly spoken,\n"
                "The diplomacy of modal verbs left no promise broken.\n"
                "TRIPS Agreement precedent, technology transfer clause,\n"
                "Language is the weapon in the diplomat's just cause.\n"
                "Negotiate with nuance, hedge with honest care,\n"
                "The resolution passes — equity is there."
            ),
            "activity": "Students write a short diplomatic speech on a global issue using at least five modal verbs for hedging. Perform in a class Model UN simulation."
        },
        7: {
            "title": "Entangled (Quantum Computing Verse)",
            "lyrics": (
                "Qubits dance in superposition's dream,\n"
                "Both states at once — not quite what they seem.\n"
                "Cryogenic chambers cooled to absolute zero's brink,\n"
                "Faster than a library, yet smaller than you think.\n"
                "Quantum supremacy could shatter every code,\n"
                "Encryption obsolete along the digital road.\n"
                "If particles can be entangled across infinite space,\n"
                "Then maybe ideas can too — time will make the case."
            ),
            "activity": "Students create a metaphor poem explaining one quantum concept (superposition, entanglement, or interference) to a non-scientist. Vote on the clearest and most creative metaphor."
        },
        8: {
            "title": "Invisible Architectures (Visual Arts Ode)",
            "lyrics": (
                "Surveillance cameras draped in gold-leaf light,\n"
                "Watched and beautiful — a paradox of sight.\n"
                "Copper synapses and blown-glass thought,\n"
                "Generative code that moves as viewers are caught.\n"
                "Turkish miniatures beside installations vast,\n"
                "Art connects the future to the ancient past.\n"
                "'Art is the language that speaks when all others fail,'\n"
                "Deniz said softly — and the gallery held its tale."
            ),
            "activity": "Students create a mixed-media response to one artwork described in the lyrics. Write an artist statement of 100 words explaining their creative choices."
        },
        9: {
            "title": "R-Naught (Global Health Rap)",
            "lyrics": (
                "R-naught rising, the curve begins to climb,\n"
                "Misinformation spreads faster every time.\n"
                "One misleading headline, ten thousand shares an hour,\n"
                "Fear without knowledge is a dangerous power.\n"
                "Triage the data, vaccinate with truth,\n"
                "Science without communication sits in an ivory booth.\n"
                "Distil the complex into one compelling frame,\n"
                "Public health literacy is everybody's game."
            ),
            "activity": "Students design a public health infographic based on one line from the rap. Present to the class and evaluate each other's designs for clarity and accuracy."
        },
        10: {
            "title": "To Be Continued (Commencement Anthem)",
            "lyrics": (
                "We entered as students, we leave as questions in flight,\n"
                "Index cards in hand, no teleprompter in sight.\n"
                "Algorithms painting gratitude on the screen,\n"
                "Oil portraits of a teacher and the years between.\n"
                "Learning is not solitary, the best code is co-authored,\n"
                "Every bridge we built this year was mutually sponsored.\n"
                "Watercolour bookmarks of our shared tree mural's grace,\n"
                "Hold them to the sunlight — to be continued, in every place."
            ),
            "activity": "Students write a farewell verse to their class, incorporating at least three vocabulary words from the year. Read aloud at a class Commencement Poetry Evening."
        }
    }
}

# ---------------------------------------------------------------------------
# 17. DIALOGUE BANK
# ---------------------------------------------------------------------------
DIALOGUE_BANK = {
    12: {
        1: {
            "setting": "University Admissions Interview",
            "characters": ["Applicant", "Interviewer"],
            "lines": [
                ("Interviewer", "Thank you for applying. Could you elaborate on your academic motivation and long-term aspirations?"),
                ("Applicant", "Absolutely. I have always been fascinated by the intersection of neuroscience and linguistics, which is why I chose to pursue this programme."),
                ("Interviewer", "Interesting. How have you demonstrated that passion outside the classroom?"),
                ("Applicant", "I co-founded a peer-tutoring club at my Anatolian high school where we explored cognitive science articles in English every week."),
                ("Interviewer", "That shows initiative. What would you say is the most significant challenge you have overcome?"),
                ("Applicant", "Presenting my TÜBİTAK research in English at an international symposium was daunting, but it taught me resilience and the power of clear communication."),
                ("Interviewer", "Impressive. Where do you see yourself contributing after graduation?"),
                ("Applicant", "I envision conducting bilingual literacy research that bridges Turkish educational policy with global best practices.")
            ],
            "focus_language": "Formal register, complex sentences, persuasion, hedging language",
            "task": "Role-play the interview with a partner. Then swap roles and improvise follow-up questions using formal hedging (I would argue that…, It could be said that…)."
        },
        2: {
            "setting": "Academic Peer-Review Workshop",
            "characters": ["Author", "Reviewer"],
            "lines": [
                ("Reviewer", "I appreciate the depth of your thesis statement, but I think the second paragraph could benefit from more nuanced argumentation."),
                ("Author", "Could you be more specific? I tried to balance evidence from both qualitative and quantitative sources."),
                ("Reviewer", "Yes, your quantitative data is solid. However, the qualitative analysis feels somewhat superficial — perhaps integrating direct quotations would strengthen it."),
                ("Author", "That is a fair point. Would you also recommend restructuring the counter-argument section?"),
                ("Reviewer", "Definitely. Placing the rebuttal before the conclusion would create a more compelling rhetorical arc."),
                ("Author", "Thank you for the constructive feedback. I will revise and resubmit by Friday."),
                ("Reviewer", "I look forward to reading the revised draft. Your writing style is already remarkably polished.")
            ],
            "focus_language": "Constructive criticism, hedging, academic vocabulary, diplomatic tone",
            "task": "Exchange essays with a partner and conduct a live peer-review dialogue. Use at least five hedging expressions (perhaps, it might be argued, one could consider…)."
        },
        3: {
            "setting": "Cybersecurity Awareness Panel Discussion",
            "characters": ["Moderator", "Expert", "Student Panellist"],
            "lines": [
                ("Moderator", "Welcome to today's panel on digital privacy. Let us start with a fundamental question: how vulnerable are our daily online interactions?"),
                ("Expert", "More than most people realise. Every time you accept cookies without reading the policy, you are essentially handing over behavioural data."),
                ("Student Panellist", "But isn't that the trade-off for free services? We get convenience in exchange for some personal information."),
                ("Expert", "That is a common misconception. The issue is not the exchange itself but the lack of informed consent and transparency."),
                ("Moderator", "How can young users in Turkey protect themselves more effectively?"),
                ("Student Panellist", "I think digital literacy should be integrated into the national curriculum from middle school onwards."),
                ("Expert", "Agreed. Turkey's KVKK legislation is a step forward, but enforcement and public awareness still lag behind."),
                ("Moderator", "Thank you both. Let us open the floor to audience questions.")
            ],
            "focus_language": "Formal debate register, concession and rebuttal, technical vocabulary, rhetorical questions",
            "task": "Organise a mini panel in groups of three. Each student takes a role and debates a digital privacy scenario. Record key arguments and present a summary to the class."
        },
        4: {
            "setting": "Grammar Masterclass Tutorial",
            "characters": ["Tutor", "Tutee"],
            "lines": [
                ("Tutor", "Let us examine why the subjunctive mood is disappearing from everyday English. Can you identify the subjunctive in this sentence?"),
                ("Tutee", "Is it 'I suggest that he attend the meeting'? The base form 'attend' instead of 'attends' signals the subjunctive."),
                ("Tutor", "Exactly. Now, how would this differ in informal register?"),
                ("Tutee", "Most speakers would say 'I suggest that he should attend' or simply 'I suggest he attends,' dropping the subjunctive entirely."),
                ("Tutor", "Precisely. This shift mirrors a broader trend toward analytical rather than synthetic structures. How does Turkish handle similar nuances?"),
                ("Tutee", "Turkish uses the optative suffix -sIn or conditional -sA to express wishes and hypotheticals, which is quite different structurally."),
                ("Tutor", "Excellent cross-linguistic awareness. For your assignment, compare subjunctive usage in five academic papers from different decades.")
            ],
            "focus_language": "Metalinguistic discussion, subjunctive mood, comparative syntax, academic register",
            "task": "With a partner, create a dialogue explaining a complex grammar concept to a younger student. Practise simplifying without losing accuracy."
        },
        5: {
            "setting": "Literary Salon — Nobel Prize Discussion",
            "characters": ["Host", "Literature Enthusiast"],
            "lines": [
                ("Host", "Tonight we discuss Orhan Pamuk's Nobel lecture, 'My Father's Suitcase.' What struck you most about his exploration of identity?"),
                ("Literature Enthusiast", "His meditation on the writer's solitude resonated deeply — the idea that literature emerges from a tension between isolation and engagement."),
                ("Host", "How does Pamuk navigate the East-West dichotomy without falling into reductive stereotypes?"),
                ("Literature Enthusiast", "He reframes the binary by centring Istanbul as a liminal space — neither fully Eastern nor Western, but a palimpsest of both."),
                ("Host", "Beautifully put. Do you think his Nobel recognition changed perceptions of Turkish literature globally?"),
                ("Literature Enthusiast", "Undoubtedly. It opened doors for writers like Elif Şafak and brought attention to Turkey's rich narrative tradition beyond Orientalist clichés."),
                ("Host", "Let us close with your favourite passage. Would you read it aloud for our audience?"),
                ("Literature Enthusiast", "With pleasure. 'A writer is someone who spends years patiently trying to discover the second being inside him…'")
            ],
            "focus_language": "Literary analysis vocabulary, evaluative adjectives, quotation integration, subjective interpretation",
            "task": "Host a literary salon in groups. Each student presents a favourite passage from a Nobel laureate and defends its significance using evaluative language."
        },
        6: {
            "setting": "Model United Nations Committee Session",
            "characters": ["Chairperson", "Delegate A", "Delegate B"],
            "lines": [
                ("Chairperson", "The committee will now hear opening statements on the resolution concerning refugee education. Delegate of Turkey, you have the floor."),
                ("Delegate A", "Thank you, Chair. Turkey hosts the largest refugee population in the world. We have enrolled over 700,000 Syrian children in our schools, yet funding remains critically insufficient."),
                ("Delegate B", "The delegate raises a valid point. However, our delegation believes that international burden-sharing must be codified, not merely aspirational."),
                ("Delegate A", "We concur with the spirit of that proposal. Nevertheless, codification without enforcement mechanisms risks becoming yet another unfulfilled declaration."),
                ("Chairperson", "Are there any amendments to the operative clauses?"),
                ("Delegate B", "Yes, Chair. We move to amend clause three to include a mandatory review mechanism every two years."),
                ("Delegate A", "We second the amendment, provided that the review includes input from host-country educators and refugee communities themselves."),
                ("Chairperson", "The amendment is noted. We shall proceed to a vote after a five-minute consultation period.")
            ],
            "focus_language": "Diplomatic register, parliamentary procedure, conditional clauses, formal concession",
            "task": "Simulate a UN committee session. Draft a one-page resolution on an international issue and debate amendments using formal parliamentary language."
        },
        7: {
            "setting": "Quantum Computing Research Lab Briefing",
            "characters": ["Lead Researcher", "Graduate Student"],
            "lines": [
                ("Lead Researcher", "Before we begin the experiment, let me verify your understanding. What distinguishes a qubit from a classical bit?"),
                ("Graduate Student", "A classical bit exists in a definite state of zero or one, whereas a qubit can exist in a superposition of both states simultaneously."),
                ("Lead Researcher", "Correct. And why does this matter for computational complexity?"),
                ("Graduate Student", "Because superposition, combined with entanglement, allows quantum computers to explore multiple solution paths in parallel — exponentially reducing processing time for certain problems."),
                ("Lead Researcher", "Good. Now, what are the primary obstacles to achieving fault-tolerant quantum computing?"),
                ("Graduate Student", "Decoherence and error rates. Current systems require extensive error correction, which consumes a large proportion of available qubits."),
                ("Lead Researcher", "Precisely. Turkey's quantum research initiative at TÜBİTAK aims to develop novel error-correction protocols. Your thesis could contribute directly to that effort."),
                ("Graduate Student", "That is incredibly motivating. I will finalise my literature review by next week and propose a methodology.")
            ],
            "focus_language": "Scientific register, technical definitions, cause-and-effect structures, hypothesis formulation",
            "task": "Role-play a lab briefing where one student explains a complex scientific concept and the other asks clarifying questions. Use at least three cause-and-effect connectors."
        },
        8: {
            "setting": "Art Gallery Curator Meeting",
            "characters": ["Curator", "Artist"],
            "lines": [
                ("Curator", "Your portfolio is striking. The juxtaposition of Ottoman miniature techniques with digital manipulation creates a fascinating tension."),
                ("Artist", "Thank you. I wanted to challenge the notion that traditional and contemporary art are mutually exclusive. Istanbul's visual heritage is my primary palette."),
                ("Curator", "How do you respond to critics who argue that digital intervention diminishes the authenticity of traditional forms?"),
                ("Artist", "I would argue that authenticity is not static. Every generation reinterprets its heritage — the miniaturists themselves were innovators in their time."),
                ("Curator", "A compelling perspective. For the exhibition, would you be willing to include an interactive installation?"),
                ("Artist", "Absolutely. I envision a projection-mapped calligraphy piece where viewers' movements alter the composition in real time."),
                ("Curator", "That would be a remarkable centrepiece. Let us discuss the spatial requirements and technical specifications.")
            ],
            "focus_language": "Aesthetic vocabulary, opinion justification, conditional proposals, evaluative language",
            "task": "Pair up as curator and artist. Present a fictional exhibition concept and negotiate the artistic vision using evaluative and descriptive language."
        },
        9: {
            "setting": "World Health Organisation Strategy Meeting",
            "characters": ["Regional Director", "Epidemiologist"],
            "lines": [
                ("Regional Director", "The latest data from the Eastern Mediterranean region shows a concerning uptick in antimicrobial resistance. What is your assessment?"),
                ("Epidemiologist", "The trend is alarming but not unexpected. Over-prescription and inadequate sanitation infrastructure are the primary drivers."),
                ("Regional Director", "What interventions have proven most effective in comparable contexts?"),
                ("Epidemiologist", "Integrated surveillance systems combined with community health education have shown measurable impact in Southeast Asia. Turkey's family medicine model could serve as an adaptation framework."),
                ("Regional Director", "How quickly could we pilot such a programme?"),
                ("Epidemiologist", "With adequate funding and ministerial cooperation, a pilot in three provinces could launch within six months."),
                ("Regional Director", "Draft a proposal by the end of the month. Include cost projections and a monitoring framework."),
                ("Epidemiologist", "Understood. I will also incorporate lessons learned from Turkey's successful vaccination campaigns as a precedent.")
            ],
            "focus_language": "Public health terminology, data-driven argumentation, conditional timelines, formal directives",
            "task": "In pairs, simulate a health policy meeting. Present epidemiological data and propose an intervention plan using evidence-based argumentation."
        },
        10: {
            "setting": "Green Technology Startup Pitch",
            "characters": ["Founder", "Investor"],
            "lines": [
                ("Founder", "Thank you for meeting with us. Our startup has developed a solar-powered desalination unit specifically designed for Turkey's arid southeastern regions."),
                ("Investor", "Intriguing. What differentiates your technology from existing desalination solutions?"),
                ("Founder", "Our unit operates at sixty per cent lower energy cost by utilising a novel membrane technology developed in collaboration with İTÜ's materials science department."),
                ("Investor", "What is your go-to-market strategy?"),
                ("Founder", "We plan to partner with municipal water authorities in Şanlıurfa and Mardin for initial deployment, then scale to export markets in North Africa and Central Asia."),
                ("Investor", "And the return on investment timeline?"),
                ("Founder", "We project break-even within three years, with a twenty-two per cent annual return by year five, assuming current government subsidies for renewable energy remain in place."),
                ("Investor", "Impressive projections. Send me the full business plan and we will schedule a follow-up with our technical advisory board.")
            ],
            "focus_language": "Business pitch register, persuasive data presentation, conditional projections, formal negotiation",
            "task": "Create a startup pitch for a green technology innovation. Present to classmates acting as investors. Use data, projections, and persuasive language."
        }
    }
}

# ---------------------------------------------------------------------------
# 18. COMIC STRIP BANK
# ---------------------------------------------------------------------------
COMIC_STRIP_BANK = {
    12: {
        1: {
            "title": "The Acceptance Letter",
            "panels": [
                {"scene": "Elif checks her email on a rainy Istanbul morning, laptop on a café table.", "speech": "This is it… the email from Oxford.", "thought": "Four years of preparation come down to this single notification."},
                {"scene": "She opens the email; her eyes widen.", "speech": "Dear Ms. Yılmaz, we are pleased to offer you…", "thought": "I cannot believe this is real."},
                {"scene": "She video-calls her parents in Ankara.", "speech": "Anne, Baba — I got in!", "thought": "Their sacrifices made this possible."},
                {"scene": "Her father wipes a tear; her mother clasps her hands.", "speech": "We always knew you would, kızım.", "thought": "Our daughter, studying where Atatürk dreamed Turkish youth would reach."},
                {"scene": "Back at the café, Elif stares out the window at the Bosphorus.", "speech": "Istanbul will always be home, no matter where I go.", "thought": "But the world is waiting, and so am I."}
            ],
            "drawing_task": "Illustrate Elif's emotional journey from anxiety to joy. Use colour symbolism — grey tones for uncertainty shifting to warm gold for triumph.",
            "language_focus": "Present perfect for life achievements, emotional vocabulary, formal vs. informal register contrast"
        },
        2: {
            "title": "The Thesis Deadline",
            "panels": [
                {"scene": "A cluttered desk with books, coffee cups, and sticky notes. Clock shows 2 AM.", "speech": "Only six hours until the submission deadline.", "thought": "Why did I leave the conclusion until the last minute?"},
                {"scene": "The student types frantically, referencing multiple sources.", "speech": "According to Chomsky… no, wait — Halliday's framework fits better here.", "thought": "Coherence, cohesion, coherence, cohesion…"},
                {"scene": "A notification pops up: 'Plagiarism check complete — 3% similarity.'", "speech": "Thank goodness. All original work.", "thought": "Those months of paraphrasing practice actually paid off."},
                {"scene": "The student hits 'Submit' at 7:58 AM. Sunlight streams through the window.", "speech": "Submitted with two minutes to spare!", "thought": "I swear I will start earlier next time. (I will not.)"},
                {"scene": "The student collapses on the desk, smiling.", "speech": "Now I sleep for approximately seventy-two hours.", "thought": "Actually, I am already thinking about my next paper topic."}
            ],
            "drawing_task": "Depict the passage of time through changing light — from lamplight at 2 AM to sunrise at 8 AM. Show the emotional arc from panic to relief.",
            "language_focus": "Academic writing vocabulary, time expressions, hyperbole for humour, self-referential irony"
        },
        3: {
            "title": "The Phishing Trap",
            "panels": [
                {"scene": "A student receives an official-looking email: 'Your university account will be suspended.'", "speech": "This looks legitimate — it has the university logo and everything.", "thought": "But wait… the sender address looks slightly off."},
                {"scene": "Close-up of the email address: 'admin@un1versity-portal.com' — the 'i' is replaced with '1'.", "speech": "Classic typosquatting! This is a phishing attempt.", "thought": "My cybersecurity course is already paying dividends."},
                {"scene": "The student reports the email to the IT security team.", "speech": "I have forwarded the suspicious email with full headers attached.", "thought": "If I had clicked that link, my credentials would have been compromised."},
                {"scene": "The IT team sends a campus-wide alert.", "speech": "ALERT: Phishing campaign targeting students. Do NOT click unverified links.", "thought": "One vigilant student can protect an entire community."},
                {"scene": "The student teaches classmates how to verify email authenticity.", "speech": "Always check the sender domain, hover over links before clicking, and enable two-factor authentication.", "thought": "Digital literacy is not optional — it is survival."}
            ],
            "drawing_task": "Use a detective/noir visual style with magnifying glass motifs. Highlight suspicious elements in red, safe elements in green.",
            "language_focus": "Technical cybersecurity vocabulary, imperative mood for instructions, conditional sentences (If you had clicked…)"
        },
        4: {
            "title": "The Grammar Time Machine",
            "panels": [
                {"scene": "A student accidentally activates a 'Grammar Time Machine' in the school library.", "speech": "Where am I? Everyone is speaking in Old English!", "thought": "Hwæt! This sounds nothing like modern English."},
                {"scene": "A medieval scribe explains verb conjugations on parchment.", "speech": "In our tongue, verbs carry person and number — 'ic singe, þū singest, hē singeþ.'", "thought": "So English used to be as inflected as Turkish!"},
                {"scene": "The machine jumps to the 18th century. A gentleman adjusts his wig.", "speech": "Pray tell, young scholar, whence hast thou come?", "thought": "The subjunctive is still alive here — 'whence hast thou come.'"},
                {"scene": "Back in 2026. The student reflects at a modern desk.", "speech": "English shed its inflections over centuries. Turkish kept them. Both systems work.", "thought": "Language evolution is not about progress — it is about adaptation."},
                {"scene": "The student presents a timeline poster to the class.", "speech": "From synthetic to analytic: the story of English morphology in five centuries.", "thought": "Understanding history makes me a better writer today."}
            ],
            "drawing_task": "Create distinct visual styles for each era — illuminated manuscript borders for Old English, Enlightenment portraiture for the 18th century, and modern minimalism for 2026.",
            "language_focus": "Historical linguistics vocabulary, comparative syntax, metalinguistic awareness, morphological terminology"
        },
        5: {
            "title": "The Nobel Acceptance Speech",
            "panels": [
                {"scene": "A young Turkish author stands backstage at the Stockholm Concert Hall, adjusting her notes.", "speech": "In five minutes, I address the Swedish Academy.", "thought": "Orhan Pamuk stood here in 2006. Nazım Hikmet never got the chance."},
                {"scene": "She walks to the podium. The audience is a sea of formal attire.", "speech": "Your Majesties, distinguished members of the Academy, fellow dreamers…", "thought": "Every word must honour the tradition I inherited and the future I represent."},
                {"scene": "She reads a passage from her award-winning novel.", "speech": "In Anatolia, stories do not end — they migrate, like the storks that cross the Bosphorus each spring.", "thought": "This metaphor carries the weight of my grandmother's oral tradition."},
                {"scene": "The audience applauds. Tears glisten in the front row.", "speech": "Literature is the last democracy — every reader holds equal citizenship.", "thought": "If one student in Diyarbakır reads this and feels seen, I have succeeded."},
                {"scene": "She holds the Nobel medal, looking toward the camera.", "speech": "This belongs to every child who ever wrote a story in the margins of a textbook.", "thought": "And the journey is only beginning."}
            ],
            "drawing_task": "Use a cinematic widescreen format. Alternate between close-up emotional portraits and wide establishing shots of the grand ceremony hall.",
            "language_focus": "Rhetorical devices (metaphor, anaphora, inclusive 'we'), formal ceremonial register, literary allusion"
        },
        6: {
            "title": "The Diplomatic Incident",
            "panels": [
                {"scene": "Two MUN delegates argue in a corridor during a break.", "speech": "Your amendment undermines the entire resolution!", "thought": "I need to stay diplomatic, even when I disagree fundamentally."},
                {"scene": "A mediator steps in with a calm demeanour.", "speech": "Perhaps we could find common ground if we separate the operative clauses from the preamble.", "thought": "Conflict resolution is about reframing, not winning."},
                {"scene": "The three sit at a small table, drafting a compromise.", "speech": "What if we include a sunset clause — the provision expires unless renewed by consensus?", "thought": "A sunset clause gives both sides an exit strategy without losing face."},
                {"scene": "They return to the committee room with a unified proposal.", "speech": "Chair, we present a jointly amended resolution.", "thought": "Diplomacy is the art of letting someone else have your way."},
                {"scene": "The resolution passes unanimously. All delegates shake hands.", "speech": "This is how international cooperation should work.", "thought": "If only real diplomacy were this efficient."}
            ],
            "drawing_task": "Use a split-panel technique showing internal thoughts versus external diplomatic composure. Contrast body language with thought bubbles.",
            "language_focus": "Diplomatic language, conditional proposals, compromise vocabulary, formal negotiation register"
        },
        7: {
            "title": "Schrödinger's Exam",
            "panels": [
                {"scene": "A physics student stares at a sealed envelope containing exam results.", "speech": "Until I open this, I have both passed and failed simultaneously.", "thought": "Schrödinger would appreciate the irony."},
                {"scene": "A friend arrives with a whiteboard showing the wave function equation.", "speech": "That is not how quantum superposition works, and you know it!", "thought": "But the metaphor is too perfect to resist."},
                {"scene": "The student opens the envelope. The result: 94/100.", "speech": "The wave function has collapsed — and it collapsed favourably!", "thought": "All those late nights studying quantum mechanics were worth it."},
                {"scene": "They celebrate with Turkish tea in the campus canteen.", "speech": "To Schrödinger's cat — may it always land on its feet.", "thought": "That mixed metaphor would horrify my English teacher."},
                {"scene": "The student places the result on a wall next to a poster of Feynman.", "speech": "Nobody understands quantum mechanics — but at least I passed the exam about it.", "thought": "Next challenge: explaining entanglement to my grandmother."}
            ],
            "drawing_task": "Incorporate quantum physics visual motifs — wave functions, probability clouds, and the famous cat. Use a playful, infographic-inspired style.",
            "language_focus": "Scientific humour, mixed registers (formal physics + informal banter), metaphor and analogy, quotation attribution"
        },
        8: {
            "title": "The Restoration Project",
            "panels": [
                {"scene": "An art restoration workshop in Topkapı Palace. A student examines a damaged İznik tile.", "speech": "This tile dates to the 16th century. The cobalt blue pigment is remarkably preserved.", "thought": "Centuries of history in a single ceramic piece."},
                {"scene": "The restoration mentor demonstrates kintsugi-inspired repair.", "speech": "We do not hide the damage — we highlight it with gold. The repair becomes part of the artwork's story.", "thought": "Wabi-sabi meets Ottoman craftsmanship."},
                {"scene": "The student carefully applies the gold lacquer.", "speech": "Every crack tells a story of survival — earthquakes, wars, the passage of time.", "thought": "Art conservation is archaeology with a paintbrush."},
                {"scene": "The restored tile is placed in a museum display.", "speech": "Visitors will see both the original artistry and the journey of preservation.", "thought": "Past and present in dialogue, joined by gold."},
                {"scene": "The student sketches a modern İznik-inspired design in a notebook.", "speech": "Tradition is not a museum — it is a living conversation.", "thought": "My generation's contribution to this conversation is just beginning."}
            ],
            "drawing_task": "Blend Ottoman decorative motifs with contemporary graphic novel aesthetics. Use actual İznik colour palette — cobalt blue, turquoise, and coral red.",
            "language_focus": "Art history vocabulary, philosophical reflection, present simple for timeless truths, metaphorical language"
        },
        9: {
            "title": "The Outbreak Detective",
            "panels": [
                {"scene": "A public health student in Ankara receives an alert on her tablet: 'Unusual cluster of respiratory cases in Southeastern province.'", "speech": "Three villages, same symptoms, same timeline. This is not a coincidence.", "thought": "Epidemiological alarm bells are ringing."},
                {"scene": "She maps the cases on a geographic information system.", "speech": "The index case traces back to a livestock market. Possible zoonotic transmission.", "thought": "Contact tracing is like detective work with microscopes."},
                {"scene": "Video call with the WHO regional office.", "speech": "We recommend immediate sample collection and genomic sequencing. Turkey's Hıfzıssıhha Institute can process within 48 hours.", "thought": "Speed saves lives in outbreak response."},
                {"scene": "Lab results arrive: a known pathogen with a novel mutation.", "speech": "The mutation affects transmissibility but not virulence. Existing antivirals should remain effective.", "thought": "Evidence-based communication prevents panic."},
                {"scene": "She drafts a public health advisory in clear, accessible language.", "speech": "Transparent communication is not just ethical — it is the most effective public health intervention.", "thought": "Science without communication is incomplete."}
            ],
            "drawing_task": "Use a procedural/detective visual style with evidence boards, maps, and data visualisations. Colour-code risk levels from green to red.",
            "language_focus": "Epidemiological terminology, passive voice for scientific reporting, hedging language for uncertainty, formal advisory register"
        },
        10: {
            "title": "The Solar Farm Debate",
            "panels": [
                {"scene": "A town hall meeting in Konya. A solar energy company presents plans for a large-scale farm.", "speech": "This project will provide clean energy for 50,000 households and create 200 local jobs.", "thought": "The numbers are compelling, but the community has concerns."},
                {"scene": "A local farmer raises her hand.", "speech": "What about the agricultural land this will displace? We have farmed this soil for generations.", "thought": "Progress should not come at the cost of heritage."},
                {"scene": "An environmental engineer proposes a compromise.", "speech": "Agrivoltaics — solar panels elevated above crops — allows farming and energy generation on the same land.", "thought": "Innovation means finding solutions that honour multiple values."},
                {"scene": "Community members examine a scale model of the agrivoltaic system.", "speech": "So we keep our wheat fields AND generate solar power? This changes everything.", "thought": "Technology should serve communities, not displace them."},
                {"scene": "A handshake between the company CEO and the village muhtar.", "speech": "Partnership, not imposition. That is how sustainable development works.", "thought": "Konya — from breadbasket to powerhouse, without losing its roots."}
            ],
            "drawing_task": "Contrast rural agricultural landscapes with futuristic solar technology. Use warm earth tones for farming scenes and clean blues for technology panels.",
            "language_focus": "Debate and persuasion vocabulary, conditional structures, stakeholder perspectives, compromise language"
        }
    }
}

# ---------------------------------------------------------------------------
# 19. ESCAPE ROOM BANK
# ---------------------------------------------------------------------------
ESCAPE_ROOM_BANK = {
    12: {
        1: {
            "title": "The University Application Vault",
            "story": "You have been locked in the admissions office the night before application deadlines. To escape, you must complete five university-level English challenges. Each correct answer reveals a digit of the exit code.",
            "puzzles": [
                {"type": "vocabulary", "question": "Rearrange the letters 'TSIIUENDQIR' to form a word meaning 'a systematic investigation' — essential for any university applicant.", "answer": "DISQUISITION", "hint": "Think of a formal academic essay or investigation."},
                {"type": "grammar", "question": "Correct the error: 'Had the applicant would have submitted her essay on time, she might have been accepted.'", "answer": "Had the applicant submitted her essay on time, she might have been accepted.", "hint": "Third conditional — remove the auxiliary that does not belong after 'Had.'"},
                {"type": "reading", "question": "Read the abstract: 'This longitudinal study examines the correlation between bilingual education and cognitive flexibility in Turkish adolescents.' What type of research design is described?", "answer": "Longitudinal study", "hint": "The key term appears at the very beginning of the abstract."},
                {"type": "writing", "question": "Write a one-sentence thesis statement for an essay arguing that gap years should be normalised in Turkish higher education culture.", "answer": "Gap years should be normalised in Turkish higher education because they foster personal maturity, global awareness, and clearer academic motivation.", "hint": "A strong thesis includes a claim and at least two supporting reasons."},
                {"type": "listening", "question": "The professor says: 'The sine qua non of academic integrity is proper attribution.' What does 'sine qua non' mean?", "answer": "An essential condition / something absolutely necessary", "hint": "It is a Latin phrase meaning 'without which, not.'"}
            ],
            "final_code": "APPLY2026",
            "reward": "You have unlocked the Admissions Vault! Your reward: a personalised university preparation checklist and a mock interview opportunity."
        },
        2: {
            "title": "The Editor's Labyrinth",
            "story": "You are trapped in the archives of a prestigious literary journal. To escape, you must demonstrate mastery of analytical writing by solving five editorial challenges.",
            "puzzles": [
                {"type": "coherence", "question": "Reorder these sentences to form a coherent paragraph: A) 'Furthermore, the evidence suggests a causal link.' B) 'This hypothesis has been widely debated.' C) 'In conclusion, further research is warranted.' D) 'Several studies have examined this phenomenon.' E) 'However, methodological limitations persist.'", "answer": "D, B, A, E, C", "hint": "Follow the academic paragraph structure: context → debate → evidence → limitation → conclusion."},
                {"type": "vocabulary", "question": "Replace the informal word in: 'The study basically shows that screen time messes up adolescent sleep patterns.'", "answer": "The study fundamentally demonstrates that screen time disrupts adolescent sleep patterns.", "hint": "Replace 'basically' and 'messes up' with academic equivalents."},
                {"type": "citation", "question": "Convert to APA format: John Smith wrote a book called 'Digital Minds' published in 2024 by Cambridge University Press.", "answer": "Smith, J. (2024). Digital minds. Cambridge University Press.", "hint": "APA: Surname, Initial. (Year). Title in italics. Publisher."},
                {"type": "argumentation", "question": "Identify the logical fallacy: 'We should not teach critical thinking because my grandfather never studied it and he was perfectly successful.'", "answer": "Anecdotal evidence / Appeal to tradition", "hint": "One person's experience does not constitute universal evidence."},
                {"type": "synthesis", "question": "Combine these two claims into one complex sentence using a concessive clause: 'AI writing tools improve productivity.' 'They may diminish original thinking.'", "answer": "Although AI writing tools improve productivity, they may diminish original thinking.", "hint": "Use 'although,' 'while,' or 'even though' to create a concessive relationship."}
            ],
            "final_code": "WRITE2026",
            "reward": "You have escaped the Editor's Labyrinth! Your reward: a masterclass certificate in analytical writing and a peer-reviewed publication simulation."
        },
        3: {
            "title": "The Firewall Breach",
            "story": "A rogue AI has locked you inside a virtual server room. To regain access and escape, you must solve five cybersecurity and digital literacy puzzles.",
            "puzzles": [
                {"type": "encryption", "question": "Decode this Caesar cipher (shift of 3): 'FUBSWRJUDSKB LV WKH DUWRI VHFXUH FRPPXQLFDWLRQ'", "answer": "CRYPTOGRAPHY IS THE ART OF SECURE COMMUNICATION", "hint": "Shift each letter three positions back in the alphabet."},
                {"type": "vocabulary", "question": "Define 'zero-day vulnerability' in one sentence using your own words.", "answer": "A zero-day vulnerability is a previously unknown software flaw that attackers can exploit before developers have created a patch.", "hint": "Think about what 'zero days' refers to — how many days the developer has had to fix it."},
                {"type": "ethics", "question": "A company discovers a data breach affecting 10 million users but delays disclosure for three months. Which ethical principle is violated and why?", "answer": "Transparency / duty of disclosure — users have a right to know their data is compromised so they can take protective action.", "hint": "Consider the stakeholders' right to informed decision-making."},
                {"type": "password", "question": "Rank these passwords from weakest to strongest: A) 'password123' B) 'Tr!buN4l#2026xQ' C) 'merhaba' D) 'MyDogMax2020'", "answer": "C, A, D, B", "hint": "Strength depends on length, character variety, and unpredictability."},
                {"type": "critical_thinking", "question": "You receive a text: 'Your bank account has been locked. Click here to verify: bit.ly/x7kQ2.' List three red flags.", "answer": "1) Unsolicited urgency, 2) Shortened/suspicious URL, 3) No personalisation (no name or account details).", "hint": "Legitimate institutions rarely use URL shorteners or create artificial urgency."}
            ],
            "final_code": "SECURE26",
            "reward": "You have breached the firewall and escaped! Your reward: a Digital Citizenship Certificate and a cybersecurity awareness badge."
        },
        4: {
            "title": "The Syntax Dungeon",
            "story": "You have fallen into a dungeon constructed entirely of complex sentences. Each puzzle requires you to parse, transform, or construct advanced syntactic structures to progress.",
            "puzzles": [
                {"type": "parsing", "question": "Identify the type of subordinate clause: 'The theory that language shapes thought, which was proposed by Sapir and Whorf, remains controversial.'", "answer": "Appositive/noun clause ('that language shapes thought') + non-restrictive relative clause ('which was proposed by Sapir and Whorf').", "hint": "Look for two different types of dependent clauses modifying 'theory.'"},
                {"type": "transformation", "question": "Transform this active sentence into a cleft sentence: 'Chomsky revolutionised linguistics in 1957.'", "answer": "It was Chomsky who revolutionised linguistics in 1957. / It was in 1957 that Chomsky revolutionised linguistics.", "hint": "Use 'It was… who/that…' to emphasise one element."},
                {"type": "error_correction", "question": "Fix the dangling modifier: 'Having studied all night, the exam was easier than expected.'", "answer": "Having studied all night, I/she found the exam easier than expected.", "hint": "The participial phrase must refer to the grammatical subject of the main clause."},
                {"type": "creation", "question": "Write a single sentence containing a relative clause, a conditional clause, and a participial phrase.", "answer": "The student who had been preparing for months would have succeeded if she had not fallen ill, having exhausted herself with excessive revision.", "hint": "Layer three clause types: 'who…', 'if…', and a '-ing/-ed' participial phrase."},
                {"type": "comparison", "question": "Explain how Turkish and English handle relative clauses differently, using one example from each language.", "answer": "English uses relative pronouns (who/which/that) post-nominally: 'the book that I read.' Turkish uses participial suffixes pre-nominally: 'okuduğum kitap' (the book I-read).", "hint": "Consider word order and the position of the modifying clause relative to the noun."}
            ],
            "final_code": "SYNTAX26",
            "reward": "You have escaped the Syntax Dungeon! Your reward: the title of 'Master Syntactician' and a grammar reference poster for your study wall."
        },
        5: {
            "title": "The Nobel Archives",
            "story": "You have been locked in the Nobel Prize Museum archives in Stockholm. To escape, you must demonstrate deep knowledge of Nobel Literature laureates and their works.",
            "puzzles": [
                {"type": "matching", "question": "Match the opening line to the novel: 'Many years later, as he faced the firing squad, Colonel Aureliano Buendía was to remember that distant afternoon when his father took him to discover ice.'", "answer": "One Hundred Years of Solitude by Gabriel García Márquez (Nobel 1982)", "hint": "A Colombian author famous for magical realism."},
                {"type": "analysis", "question": "Orhan Pamuk's Nobel lecture is titled 'My Father's Suitcase.' What does the suitcase symbolise?", "answer": "The suitcase symbolises literary inheritance, the anxiety of creative ambition, and the tension between a private inner world and public expression.", "hint": "Think about what a father passes to a son — and the weight of unexpressed creativity."},
                {"type": "comparison", "question": "Compare the narrative technique of stream of consciousness in Virginia Woolf and Orhan Pamuk. Name one similarity and one difference.", "answer": "Similarity: Both use interior monologue to explore subjective time. Difference: Woolf fragments syntax to mirror thought; Pamuk layers cultural memory and urban geography.", "hint": "Consider how each author represents the flow of thought differently."},
                {"type": "creative", "question": "Write the opening sentence of a novel that you believe could win the Nobel Prize. Explain your stylistic choices in one sentence.", "answer": "(Student's original sentence) — e.g., 'The city remembered her before she remembered herself.' Choice: Personification of setting to blur individual and collective memory.", "hint": "Nobel-worthy openings often subvert expectations and establish a distinctive voice immediately."},
                {"type": "vocabulary", "question": "Define 'intertextuality' and provide an example from any Nobel laureate's work.", "answer": "Intertextuality is the relationship between texts where one references or echoes another. Example: Pamuk's 'The New Life' echoes Dante's 'La Vita Nuova' in title and structure.", "hint": "Think about how texts 'talk' to each other across time and cultures."}
            ],
            "final_code": "NOBEL026",
            "reward": "You have unlocked the Nobel Archives! Your reward: a curated reading list of Nobel Literature laureates and a creative writing masterclass invitation."
        },
        6: {
            "title": "The Diplomatic Cipher Room",
            "story": "You are trapped in a decommissioned NATO communications room beneath Ankara. To escape, you must solve five international relations and diplomacy puzzles.",
            "puzzles": [
                {"type": "terminology", "question": "What is the difference between 'multilateral' and 'bilateral' diplomacy? Provide one example of each involving Turkey.", "answer": "Multilateral involves multiple nations (Turkey in NATO). Bilateral involves two nations (Turkey-Azerbaijan relations).", "hint": "Count the number of parties involved."},
                {"type": "drafting", "question": "Write a single operative clause for a UN resolution on climate refugees that would be acceptable to both developed and developing nations.", "answer": "Urges member states to establish, in accordance with their respective capacities, a voluntary fund for climate-displaced populations with transparent reporting mechanisms.", "hint": "Use inclusive language and voluntary rather than mandatory commitments."},
                {"type": "negotiation", "question": "You represent Turkey in a trade negotiation. Your counterpart offers tariff reduction on automotive imports in exchange for agricultural concessions. What is your counter-offer?", "answer": "Accept phased tariff reduction over five years, conditional on reciprocal agricultural technology transfer and protection of Turkish small-scale farmers.", "hint": "A good counter-offer protects domestic interests while showing willingness to engage."},
                {"type": "analysis", "question": "Explain the concept of 'soft power' and give two examples of Turkey exercising soft power internationally.", "answer": "Soft power is influence through culture, values, and institutions rather than coercion. Examples: Turkish television dramas' global popularity, TİKA development aid programmes.", "hint": "Think beyond military and economic pressure — what attracts other nations to Turkey?"},
                {"type": "language", "question": "Translate this diplomatic euphemism into plain English: 'The parties agreed to disagree and will continue consultations at a mutually convenient time.'", "answer": "The negotiations failed, and neither side is willing to compromise at this time, but neither wants to formally end talks.", "hint": "Diplomatic language often disguises failure as process."}
            ],
            "final_code": "DIPLO026",
            "reward": "You have escaped the Cipher Room! Your reward: a Model United Nations preparation kit and a diplomatic communication skills certificate."
        },
        7: {
            "title": "The Quantum Laboratory Lockdown",
            "story": "A quantum computer malfunction has sealed the laboratory. To override the lockdown, you must solve five puzzles that combine quantum computing concepts with advanced English.",
            "puzzles": [
                {"type": "definition", "question": "Explain 'quantum entanglement' in exactly two sentences, using language accessible to a non-specialist.", "answer": "Quantum entanglement occurs when two particles become linked so that measuring one instantly determines the state of the other, regardless of distance. Einstein famously called this 'spooky action at a distance.'", "hint": "Simplify without sacrificing accuracy — imagine explaining to an intelligent 15-year-old."},
                {"type": "analogy", "question": "Create an original analogy to explain superposition using a real-world Turkish context.", "answer": "Superposition is like a Turkish election ballot before it is unfolded — it simultaneously represents every candidate until the moment of observation.", "hint": "Find a situation where something is undetermined until observed or measured."},
                {"type": "reading", "question": "In quantum computing, what does 'decoherence' mean and why is it a problem?", "answer": "Decoherence is the loss of quantum properties when a qubit interacts with its environment, causing it to behave classically. It limits computation time and accuracy.", "hint": "Think of it as the quantum state 'leaking' into the surrounding environment."},
                {"type": "ethics", "question": "Quantum computers could break current encryption standards. Write a one-sentence argument for why governments should invest in post-quantum cryptography NOW.", "answer": "Governments must invest in post-quantum cryptography immediately because adversaries may already be storing encrypted data to decrypt once quantum computers become sufficiently powerful — a strategy known as 'harvest now, decrypt later.'", "hint": "Consider the time gap between data collection and future decryption capability."},
                {"type": "communication", "question": "Rewrite this jargon-heavy sentence for a general audience: 'The implementation of Shor's algorithm on a fault-tolerant quantum processor would render RSA-2048 cryptographically obsolete.'", "answer": "Once a powerful enough quantum computer runs a specific algorithm, the encryption protecting most of the world's online communications could be broken.", "hint": "Remove technical terms and focus on the real-world impact."}
            ],
            "final_code": "QUBIT026",
            "reward": "You have overridden the lockdown! Your reward: a quantum computing glossary poster and access to an online quantum simulation platform."
        },
        8: {
            "title": "The Gallery After Dark",
            "story": "You are locked in Istanbul Modern after closing time. The security system requires you to solve five art and visual culture puzzles to unlock the exit.",
            "puzzles": [
                {"type": "analysis", "question": "Describe the artistic technique of chiaroscuro in one sentence and name one Ottoman-era artist or tradition that used dramatic light contrast.", "answer": "Chiaroscuro uses strong contrasts between light and dark to create depth and drama; Ottoman shadow puppet theatre (Karagöz) employs similar light-contrast principles.", "hint": "Think beyond painting — consider performing arts that use light and shadow."},
                {"type": "vocabulary", "question": "What is the difference between 'aesthetic' and 'ascetic'? Use each in a sentence related to art.", "answer": "Aesthetic relates to beauty and taste: 'The exhibition's aesthetic was minimalist.' Ascetic means austere/self-denying: 'The artist's ascetic lifestyle influenced her sparse compositions.'", "hint": "They sound similar but have opposite connotations — beauty versus self-denial."},
                {"type": "interpretation", "question": "A painting shows a woman holding a pomegranate in front of the Maiden's Tower. Propose two symbolic interpretations.", "answer": "1) The pomegranate symbolises fertility and abundance — the woman embodies Istanbul's creative potential. 2) The pomegranate's many seeds represent the city's diverse cultures united within a single form.", "hint": "Pomegranates carry rich symbolism across Turkish, Greek, and Persian traditions."},
                {"type": "comparison", "question": "Compare İznik tile art with Delft Blue pottery in terms of colour palette, motifs, and cultural function.", "answer": "Both use blue-and-white palettes, but İznik features tulips, carnations, and arabesques reflecting Islamic art, while Delft depicts pastoral scenes reflecting Dutch mercantile culture. Both served decorative and status functions.", "hint": "Look at what each tradition depicts and why — cultural values shape artistic motifs."},
                {"type": "creation", "question": "Write an ekphrastic poem (3-4 lines) describing an imaginary painting titled 'Dawn Over the Golden Horn.'", "answer": "(Student's original poem) — e.g., 'Minarets pierce the amber veil of morning, / fishermen's nets catch light before they catch the sea, / and the Golden Horn remembers every civilisation / that ever mistook its beauty for possession.'", "hint": "Ekphrasis means writing that vividly describes a visual artwork — make the reader 'see' the painting."}
            ],
            "final_code": "ARTIS026",
            "reward": "You have escaped the gallery! Your reward: a virtual tour of world-class museums and a personalised art vocabulary journal."
        },
        9: {
            "title": "The Pandemic Preparedness Simulation",
            "story": "You are in a WHO emergency operations centre during a simulated pandemic. To complete the simulation and exit, solve five global health communication challenges.",
            "puzzles": [
                {"type": "communication", "question": "Rewrite this WHO advisory for a social media audience (max 280 characters): 'The Organisation recommends enhanced surveillance and contact tracing measures in light of emerging evidence of sustained human-to-human transmission.'", "answer": "NEW: Evidence of person-to-person spread confirmed. Health authorities stepping up testing & contact tracing. Stay informed, stay safe. #PublicHealth", "hint": "Keep the core message, remove jargon, add urgency without panic."},
                {"type": "data_literacy", "question": "A graph shows that Country A has more total cases than Country B, but Country B has a higher per capita rate. Explain why per capita data is more meaningful for comparison.", "answer": "Per capita rates account for population size differences, allowing fair comparison. A country of 80 million with 10,000 cases (125 per million) is less affected than a country of 1 million with 5,000 cases (5,000 per million).", "hint": "Think about proportions — raw numbers can be misleading without context."},
                {"type": "ethics", "question": "During a vaccine shortage, should healthcare workers or elderly citizens be prioritised? Argue both sides in one sentence each.", "answer": "Healthcare workers first: protecting frontline capacity ensures the system can treat all patients. Elderly first: the most vulnerable deserve protection based on the ethical principle of reducing mortality.", "hint": "Both positions have valid ethical foundations — utilitarianism vs. vulnerability-based ethics."},
                {"type": "vocabulary", "question": "Define 'epidemiological triad' and explain its three components.", "answer": "The epidemiological triad is a model for disease causation comprising: 1) Agent (the pathogen), 2) Host (the organism affected), 3) Environment (external factors enabling transmission).", "hint": "Three interconnected elements that must align for disease to occur."},
                {"type": "writing", "question": "Draft a one-paragraph public health advisory for Turkish schools during a respiratory illness outbreak.", "answer": "Dear school community, in response to the current respiratory illness outbreak, we advise the following precautions: ensure adequate ventilation in all classrooms, encourage regular handwashing, and ask symptomatic students to stay home and consult a healthcare provider. Temperature screening will be conducted at school entrances. These measures protect our students, staff, and their families. For questions, contact your school health coordinator.", "hint": "Balance authority with empathy, be specific about actions, and provide a contact point."}
            ],
            "final_code": "HEALTH26",
            "reward": "Simulation complete! Your reward: a Global Health Literacy Certificate and a first-aid communication handbook."
        },
        10: {
            "title": "The Carbon Neutral Challenge",
            "story": "You are locked in a green technology innovation hub. To power the exit, you must solve five sustainability and environmental English puzzles, each activating a solar panel.",
            "puzzles": [
                {"type": "vocabulary", "question": "Explain the difference between 'carbon neutral,' 'carbon negative,' and 'net zero.' Which is the most ambitious target?", "answer": "Carbon neutral: offsetting emissions to zero net output. Net zero: reducing emissions as much as possible, offsetting the remainder. Carbon negative: removing more carbon than emitted. Carbon negative is most ambitious.", "hint": "Think of a spectrum from balance (neutral) to surplus removal (negative)."},
                {"type": "persuasion", "question": "Write a one-sentence elevator pitch for a Turkish green technology startup that converts olive oil waste into biofuel.", "answer": "We transform Turkey's 400,000 tonnes of annual olive oil waste into clean biofuel, turning an environmental liability into a renewable energy source that powers rural communities.", "hint": "Include a specific statistic, the problem, and the solution in one compelling sentence."},
                {"type": "analysis", "question": "Why is the term 'greenwashing' problematic, and how can consumers identify it? Give one Turkish example.", "answer": "Greenwashing is when companies falsely market products as environmentally friendly. Consumers should look for third-party certifications. Example: a Turkish textile company claiming 'eco-friendly' dyes without independent verification.", "hint": "Look for vague claims without evidence or certification."},
                {"type": "debate", "question": "Nuclear energy produces no direct carbon emissions but generates radioactive waste. In one sentence, argue FOR nuclear energy in Turkey's energy mix.", "answer": "Given Turkey's growing energy demand and seismic considerations notwithstanding, nuclear power at Akkuyu provides a reliable, low-carbon baseload that complements intermittent renewables like solar and wind.", "hint": "Focus on the carbon-reduction benefit and energy security."},
                {"type": "writing", "question": "Complete this sentence with a strong conclusion: 'The transition to green technology is not merely an environmental imperative; it is…'", "answer": "…an economic opportunity, a moral obligation to future generations, and the defining challenge of our era — one that Turkey, with its renewable energy potential and young, innovative population, is uniquely positioned to lead.", "hint": "End with a statement that connects the global issue to Turkey's specific strengths."}
            ],
            "final_code": "GREEN026",
            "reward": "All five solar panels activated — exit unlocked! Your reward: a Sustainability Champion badge and a tree planted in your name through TEMA Foundation."
        }
    }
}

# ---------------------------------------------------------------------------
# 20. FAMILY CORNER BANK
# ---------------------------------------------------------------------------
FAMILY_CORNER_BANK = {
    12: {
        1: {
            "title": "University Preparation: A Family Journey",
            "activity": "Research three universities together (one Turkish, one European, one international). Create a comparison chart covering programmes, campus life, and career outcomes. Discuss what matters most to your family.",
            "together": "Watch a TED Talk on 'How to Choose a University' together and discuss: What values should guide this decision? How can we balance ambition with well-being?",
            "parent_question": "Dear parent, university selection is a pivotal family moment. How did your own educational journey shape the person you became, and what wisdom would you share with your child at this crossroads?",
            "signature": True
        },
        2: {
            "title": "The Art of Argumentation at Home",
            "activity": "Choose a family-relevant topic (e.g., screen time limits, household responsibilities). Each family member writes a one-paragraph argument, then exchange and provide constructive written feedback.",
            "together": "Host a 'family debate night' — choose a lighthearted motion ('Cats make better pets than dogs') and practise structured argumentation with opening statements, rebuttals, and closing arguments.",
            "parent_question": "Dear parent, analytical thinking is a lifelong skill. Can you share a time when the ability to construct a clear argument helped you in your professional or personal life?",
            "signature": True
        },
        3: {
            "title": "Our Family's Digital Safety Audit",
            "activity": "Conduct a family digital security audit: review passwords, enable two-factor authentication on all accounts, and check privacy settings on social media together.",
            "together": "Create a 'Family Cybersecurity Protocol' — agreed rules for sharing personal information online, responding to suspicious messages, and protecting family devices.",
            "parent_question": "Dear parent, digital threats evolve constantly. What online safety concerns are most relevant to your family, and how comfortable do you feel navigating them?",
            "signature": True
        },
        4: {
            "title": "Language Heritage in Our Family",
            "activity": "Create a family language tree — map the languages, dialects, and regional expressions used across three generations. Discuss how language has evolved in your family.",
            "together": "Play 'Translation Challenge' — each family member translates the same Turkish proverb into English, then compare interpretations. Discuss what gets lost (and found) in translation.",
            "parent_question": "Dear parent, language carries identity. Are there family expressions, proverbs, or regional phrases you would like your child to remember and pass on?",
            "signature": True
        },
        5: {
            "title": "A Literary Evening at Home",
            "activity": "Each family member selects a short poem or literary passage (in any language) that holds personal significance. Read aloud and explain why the words resonate.",
            "together": "Visit a local bookshop or library together. Each person chooses a book for another family member based on what they think that person would enjoy. Exchange with a personal note explaining the choice.",
            "parent_question": "Dear parent, literature shapes how we see the world. Is there a book or author that profoundly influenced your thinking? We would love to hear why.",
            "signature": True
        },
        6: {
            "title": "Understanding Global Perspectives Together",
            "activity": "Follow an international news story together for one week. Each day, read coverage from a different country's English-language media. At week's end, discuss how perspectives varied.",
            "together": "Cook a dish from a country currently in the news. While cooking, discuss that country's culture, challenges, and Turkey's relationship with it. Combine culinary and geopolitical exploration.",
            "parent_question": "Dear parent, global awareness begins at home. How has Turkey's relationship with the world changed since your own school years, and what does international understanding mean to your family?",
            "signature": True
        },
        7: {
            "title": "Technology and Ethics: A Family Discussion",
            "activity": "Read a short article about AI or quantum computing together. Each family member writes three questions it raises about society, employment, or ethics. Share and discuss.",
            "together": "Play 'Future Forecast' — each family member predicts three ways technology will change daily life in Turkey by 2040. Compare predictions and discuss which excite or concern you.",
            "parent_question": "Dear parent, technology is transforming every profession. What technological change has most affected your work, and how do you think your child should prepare for an AI-influenced future?",
            "signature": True
        },
        8: {
            "title": "Art Appreciation as a Family",
            "activity": "Visit a museum, gallery, or virtual exhibition together (Istanbul Modern, Pera Museum, or an online collection). Each person selects one artwork and writes a brief English reflection on why it moved them.",
            "together": "Create a collaborative family artwork — each person contributes one element (drawing, collage, calligraphy). Frame it together and discuss the creative process.",
            "parent_question": "Dear parent, art opens windows to empathy and imagination. What role does art or creativity play in your life, and is there an artwork or artist you would like to share with your child?",
            "signature": True
        },
        9: {
            "title": "Health and Wellbeing: Our Family Plan",
            "activity": "Create a 'Family Wellbeing Charter' — agreed commitments for physical health, mental health, and nutrition. Write it in English and display it at home.",
            "together": "Cook a healthy meal together using a recipe written in English. Practise measurement vocabulary (tablespoon, pinch, simmer) and discuss the connection between nutrition and academic performance.",
            "parent_question": "Dear parent, health is the foundation of achievement. What family health traditions or habits would you like to strengthen, and how can the whole family support each other's wellbeing?",
            "signature": True
        },
        10: {
            "title": "Our Family's Green Commitment",
            "activity": "Calculate your family's approximate carbon footprint using an online calculator (in English). Identify three actionable steps to reduce it and track progress for one month.",
            "together": "Plant something together — a tree, herbs, or a window garden. Research the plant's environmental benefits in English. Create a care schedule that the whole family follows.",
            "parent_question": "Dear parent, environmental responsibility is inherited. What environmental changes have you witnessed in your lifetime, and what legacy do you hope to leave for the next generation?",
            "signature": True
        }
    }
}

# ---------------------------------------------------------------------------
# 21. SEL (Social-Emotional Learning) BANK
# ---------------------------------------------------------------------------
SEL_BANK = {
    12: {
        1: {
            "emotion": "Anticipatory anxiety and excitement",
            "prompt": "You are about to begin the university application process. You feel both excitement about new possibilities and anxiety about uncertainty. How do you hold both emotions simultaneously without letting either dominate?",
            "activity": "Write a letter to your future self (to be opened on your first day of university). Include your current hopes, fears, and three promises you make to yourself about maintaining well-being during the transition.",
            "mindfulness": "The Threshold Meditation: Stand in a doorway. Feel the frame with both hands. Breathe in — you are in the familiar. Step forward and breathe out — you enter the unknown. Repeat three times. Notice that you chose to step forward each time.",
            "discussion": "How can we distinguish between healthy anticipation that motivates us and unhealthy anxiety that paralyses us? What strategies help you personally stay in the productive zone?"
        },
        2: {
            "emotion": "Intellectual humility",
            "prompt": "You receive critical feedback on an essay you were proud of. Your first instinct is defensiveness. How do you move from defensiveness to genuine openness to learning?",
            "activity": "The Revision Ritual: Take a piece of your own writing that received criticism. Read the feedback without responding for five minutes. Then rewrite the weakest section, genuinely trying to improve. Reflect: how did the quality change?",
            "mindfulness": "Beginner's Mind Breathing: For three minutes, breathe as if you have never breathed before. Notice the sensation with fresh curiosity. Apply this same 'beginner's mind' to receiving feedback — every critique is information, not judgement.",
            "discussion": "Why is intellectual humility considered a strength, not a weakness, in academic and professional contexts? Can you think of a time when admitting you were wrong led to growth?"
        },
        3: {
            "emotion": "Digital overwhelm and boundary-setting",
            "prompt": "You realise you have spent four hours scrolling social media and feel drained, anxious, and unproductive. You know you need boundaries but fear missing out. How do you navigate this tension?",
            "activity": "Digital Detox Experiment: Choose one day this week to limit social media to 30 minutes total. Journal about the experience — what did you notice about your attention, mood, and productivity?",
            "mindfulness": "The Notification Pause: Each time your phone buzzes, wait ten seconds before looking. During those ten seconds, take one conscious breath. After one week, reflect: did the pause change your relationship with your device?",
            "discussion": "Is FOMO (fear of missing out) a genuine social need or a manufactured anxiety? How do digital platforms exploit our emotional vulnerabilities, and what does healthy digital citizenship look like?"
        },
        4: {
            "emotion": "Precision and perfectionism",
            "prompt": "You are revising an essay and cannot stop editing. Every sentence feels imperfect. You have rewritten the introduction seven times. How do you distinguish between productive refinement and paralysing perfectionism?",
            "activity": "The 'Good Enough' Exercise: Set a timer for 20 minutes. Write a one-page response to a prompt. When the timer stops, submit it AS IS. Reflect on the discomfort of imperfection and what you learned about your own standards.",
            "mindfulness": "Wabi-Sabi Contemplation: Find an object with a visible flaw — a cracked mug, a bent leaf, a chipped tile. Spend two minutes appreciating its beauty precisely because of its imperfection. How does this perspective apply to your own work?",
            "discussion": "Research shows that perfectionism is rising among young people globally. Why might this be, and what is the difference between high standards and self-destructive perfectionism?"
        },
        5: {
            "emotion": "Empathy through literature",
            "prompt": "You read a novel about a character whose life, culture, and values are entirely different from yours. You find yourself deeply moved. How does literature create empathy across boundaries that physical distance cannot bridge?",
            "activity": "Empathy Mapping: Choose a character from a novel you have read this year. Create an empathy map: What do they think? Feel? Say? Do? What are their fears and hopes? Present your map to the class and explain how understanding this character changed your own perspective.",
            "mindfulness": "The Other's Shoes: Close your eyes and imagine waking up as someone in a very different life situation — a refugee, an elderly person, someone with a disability. Spend three minutes truly inhabiting their morning routine. What did you feel?",
            "discussion": "Orhan Pamuk says, 'The writer's secret is not inspiration but stubbornness.' How does patient attention to others' stories build the empathy that society needs?"
        },
        6: {
            "emotion": "Moral courage in complex situations",
            "prompt": "You witness a classmate being excluded from a group project because of their political views. You agree with neither the exclusion nor the classmate's views. What do you do, and why?",
            "activity": "The Moral Dilemma Protocol: In small groups, discuss a real-world ethical dilemma (e.g., whistleblowing, intervening in injustice). Each person writes their position, then reads and genuinely considers an opposing view. Did anyone change their mind?",
            "mindfulness": "Courage Anchoring: Place your hand on your chest. Feel your heartbeat. Tell yourself: 'I can feel afraid and still act with integrity.' Repeat three times. This is not about eliminating fear but about acting despite it.",
            "discussion": "What is the difference between moral courage and recklessness? How do we develop the judgement to know when to speak up and when to listen?"
        },
        7: {
            "emotion": "Wonder and intellectual curiosity",
            "prompt": "You learn that quantum physics suggests reality at the smallest scale behaves nothing like our everyday experience. Instead of feeling confused, you feel wonder. How do you cultivate and protect this sense of wonder in an age of information overload?",
            "activity": "The Wonder Journal: For one week, write down one thing each day that genuinely surprised or amazed you — from a physics concept to a sunset to a stranger's kindness. At week's end, reflect on patterns in what triggers your sense of wonder.",
            "mindfulness": "Stargazing Meditation: If weather permits, spend five minutes looking at the night sky. If indoors, watch a time-lapse of the cosmos. Let the scale of the universe dissolve your daily worries. Notice how smallness can feel liberating rather than diminishing.",
            "discussion": "Einstein said, 'The most beautiful thing we can experience is the mysterious.' In a world that demands certainty and productivity, how do we make space for wonder and not-knowing?"
        },
        8: {
            "emotion": "Creative vulnerability",
            "prompt": "You have created an artwork — a painting, a poem, a song — that expresses something deeply personal. Your teacher asks you to share it with the class. You feel exposed. How do you navigate the vulnerability of creative expression?",
            "activity": "The Vulnerability Gallery: Each student creates a small artwork (any medium) that expresses a genuine emotion. Display anonymously. Walk through the gallery in silence. Then, voluntarily, creators reveal themselves and share their process.",
            "mindfulness": "Creative Breathing: Inhale and imagine gathering raw emotion. Hold briefly — let it take shape. Exhale and release it as creative expression. Repeat five times. Notice that creation requires both gathering and releasing.",
            "discussion": "Brené Brown argues that vulnerability is the birthplace of creativity and belonging. Why does sharing our authentic creative work feel risky, and what makes it worth the risk?"
        },
        9: {
            "emotion": "Compassion fatigue and sustainable caring",
            "prompt": "You care deeply about global health crises, climate change, refugee rights, and social justice. But the constant stream of suffering in the news leaves you feeling helpless and exhausted. How do you sustain compassion without burning out?",
            "activity": "The Circle of Influence: Draw two concentric circles. In the inner circle, write actions you can actually take (volunteering locally, donating, educating peers). In the outer circle, write systemic issues beyond your direct control. Focus your energy on the inner circle.",
            "mindfulness": "Compassion Meditation (Tonglen): Breathe in — imagine absorbing the suffering of one person you know. Breathe out — send them relief and kindness. Practise for three minutes. Notice that compassion is an active practice, not passive absorption.",
            "discussion": "How do healthcare workers, aid workers, and activists sustain their compassion over decades? What can we learn from their strategies about sustainable caring?"
        },
        10: {
            "emotion": "Gratitude and legacy",
            "prompt": "This is your final year of secondary school. You are about to leave behind teachers, friends, routines, and a version of yourself. What are you grateful for, and what legacy do you want to leave?",
            "activity": "The Gratitude Letter: Write a genuine letter of thanks to one person who shaped your school experience — a teacher, a friend, a parent, a librarian. Deliver it in person if possible. Observe their reaction and your own feelings.",
            "mindfulness": "The Closing Meditation: Sit quietly for five minutes. With each exhale, mentally thank one person, one experience, one lesson from your school years. With each inhale, welcome one hope for the future. End by placing your hand on your heart and saying silently: 'I am ready.'",
            "discussion": "What does it mean to leave a legacy at 18? How can gratitude — genuinely practised, not performatively expressed — transform our relationship with endings and beginnings?"
        }
    }
}

# ---------------------------------------------------------------------------
# 22. PODCAST BANK
# ---------------------------------------------------------------------------
PODCAST_BANK = {
    12: {
        1: {
            "title": "Episode 1: The University-Level English Challenge",
            "host": "Elif & Prof. Aydin",
            "summary": "An exploration of what it truly means to communicate at university level — from academic register to the unwritten rules of intellectual discourse.",
            "segments": [
                "Intro (0:00): Welcome to 'Beyond the Classroom' — the podcast for ambitious Turkish students preparing for global academia.",
                "Topic (0:30): What changes when English stops being a 'subject' and becomes your medium of instruction? Academic shock and how to survive it.",
                "Interview (2:00): A Turkish exchange student at UCL shares her first-week experience — 'I could speak English, but I could not think in it yet.'",
                "Fun Fact (3:30): The average university textbook contains approximately 3,000 unique academic vocabulary items. Most B2 speakers know only 1,200.",
                "Challenge (4:00): Record a two-minute academic presentation on any topic from this unit. Use at least five academic transition phrases. Share with a peer for feedback."
            ],
            "student_task": "Produce your own five-minute podcast episode discussing 'The biggest misconception about studying in English at university.' Include an interview segment with a classmate."
        },
        2: {
            "title": "Episode 2: Writing That Changes Minds",
            "host": "Elif & Dr. Kaya",
            "summary": "A deep dive into the art and science of analytical writing — from Aristotle's rhetoric to modern op-ed columns in The Guardian and Hürriyet Daily News.",
            "segments": [
                "Intro (0:00): Why does some writing persuade while other writing merely informs? Today we dissect the anatomy of argumentation.",
                "Topic (0:30): The three pillars of persuasion — ethos, pathos, logos — and how they operate in Turkish and English academic traditions.",
                "Interview (2:00): A columnist from Hürriyet Daily News explains how she structures an argument in 800 words or fewer.",
                "Fun Fact (3:30): The most-cited academic paper ever — with over 330,000 citations — is a methods paper. Structure and clarity win over style.",
                "Challenge (4:00): Write a 500-word op-ed on a topic you care about. Apply the ethos-pathos-logos framework. Submit to your school newspaper or blog."
            ],
            "student_task": "Create a podcast episode reviewing a published op-ed. Analyse its rhetorical strategies and rate its persuasiveness on a scale of 1-10 with justification."
        },
        3: {
            "title": "Episode 3: Your Digital Shadow",
            "host": "Elif & Cyber-Expert Mert",
            "summary": "An investigation into the data trail we leave online — from cookies to metadata — and how Turkish and EU regulations attempt to protect our privacy.",
            "segments": [
                "Intro (0:00): You have probably accepted 200 cookie policies this month without reading a single one. Today, we read them for you.",
                "Topic (0:30): What data do apps actually collect? A live audit of five popular apps' privacy policies, with surprising revelations.",
                "Interview (2:00): A KVKK (Turkish Data Protection Authority) representative explains your legal rights — and how few people exercise them.",
                "Fun Fact (3:30): Your smartphone generates approximately 40 megabytes of metadata per day — location, usage patterns, biometric data — even when you are not actively using it.",
                "Challenge (4:00): Conduct a personal data audit. Check the privacy settings on three of your most-used apps. Write a one-page report on what you found and what you changed."
            ],
            "student_task": "Produce a podcast episode titled 'I Read the Terms and Conditions So You Don't Have To.' Analyse one app's privacy policy and translate the legal jargon into plain English."
        },
        4: {
            "title": "Episode 4: The Grammar Detectives",
            "host": "Elif & Linguist Zeynep",
            "summary": "A linguistic investigation into how English syntax has evolved, why some rules are breaking down, and what this tells us about language change.",
            "segments": [
                "Intro (0:00): Is it wrong to split an infinitive? Is 'they' singular? Today, the Grammar Detectives investigate the cold cases of English syntax.",
                "Topic (0:30): Prescriptivism versus descriptivism — the eternal debate. We examine three 'rules' that never were rules at all.",
                "Interview (2:00): A computational linguist at Boğaziçi University explains how corpus data reveals the grammar people actually use versus what textbooks prescribe.",
                "Fun Fact (3:30): Shakespeare invented over 1,700 words and freely violated the grammar rules we now treat as sacred. If he were alive today, autocorrect would drive him mad.",
                "Challenge (4:00): Find three examples of 'incorrect' grammar in published English (newspapers, novels, speeches). Argue whether each is an error or an evolution."
            ],
            "student_task": "Create a podcast episode called 'Grammar Myth Busters.' Debunk three common grammar myths using evidence from linguistics research."
        },
        5: {
            "title": "Episode 5: Reading the Nobel Laureates",
            "host": "Elif & Literature Professor Selin",
            "summary": "A guided tour through the Nobel Prize in Literature — its history, controversies, and what it reveals about which stories the world chooses to celebrate.",
            "segments": [
                "Intro (0:00): The Nobel Prize in Literature is the world's most prestigious literary award — but is it also the most controversial? Let us investigate.",
                "Topic (0:30): From Pamuk to Morrison to Müller — how Nobel selections reflect geopolitical shifts and literary politics.",
                "Interview (2:00): A comparative literature doctoral student discusses her thesis on 'peripheral literatures' and why some traditions remain underrepresented.",
                "Fun Fact (3:30): Tolstoy, Borges, Nabokov, and Chinua Achebe never won the Nobel Prize in Literature. The committee has admitted to some historical oversights.",
                "Challenge (4:00): Read one short work by a Nobel laureate you have never encountered. Write a 300-word critical response exploring why this author deserved (or did not deserve) the prize."
            ],
            "student_task": "Produce a podcast episode titled 'The Nobel Prize Should Have Gone To…' Argue the case for an author who was never awarded the prize."
        },
        6: {
            "title": "Episode 6: Diplomacy in Plain English",
            "host": "Elif & Ambassador (Ret.) Hakan Bey",
            "summary": "A behind-the-scenes look at international diplomacy — the language, the protocols, and the unspoken rules that govern how nations negotiate.",
            "segments": [
                "Intro (0:00): When diplomats say 'interesting,' they mean 'terrible.' Welcome to the world of diplomatic double-speak.",
                "Topic (0:30): Decoding diplomatic language — a glossary of what diplomats actually mean versus what they literally say.",
                "Interview (2:00): A retired Turkish ambassador shares stories from multilateral negotiations — what happens when translation fails and how humour saves treaties.",
                "Fun Fact (3:30): The United Nations has six official languages, but approximately 85% of informal negotiations happen in English — even between non-native speakers.",
                "Challenge (4:00): Write a diplomatic communiqué (one paragraph) announcing a fictional agreement between two countries. Then 'translate' it into plain English beneath."
            ],
            "student_task": "Create a podcast episode analysing a recent international agreement or summit. Decode the diplomatic language used in the official statement."
        },
        7: {
            "title": "Episode 7: Quantum Computing for the Curious",
            "host": "Elif & Physicist Dr. Barış",
            "summary": "A beginner-friendly exploration of quantum computing — what it is, why it matters, and how Turkey is positioning itself in the quantum race.",
            "segments": [
                "Intro (0:00): If classical computers are typewriters, quantum computers are entire printing presses — and they are about to change everything.",
                "Topic (0:30): Qubits, superposition, and entanglement explained with zero equations and maximum clarity. Yes, it is possible.",
                "Interview (2:00): A researcher at TÜBİTAK's quantum computing initiative explains Turkey's five-year quantum strategy and what skills future graduates will need.",
                "Fun Fact (3:30): Google's quantum computer Sycamore performed a calculation in 200 seconds that would take the world's fastest supercomputer 10,000 years.",
                "Challenge (4:00): Explain quantum superposition to a family member using only everyday analogies. Record their reaction and your explanation."
            ],
            "student_task": "Produce a podcast episode titled 'Quantum Computing and Me.' Explore how quantum computing might affect your chosen career field in the next 20 years."
        },
        8: {
            "title": "Episode 8: Seeing the World Through Art",
            "host": "Elif & Curator Aslı",
            "summary": "How visual art communicates across language barriers — from Ottoman miniatures to Instagram aesthetics — and why visual literacy matters as much as verbal literacy.",
            "segments": [
                "Intro (0:00): A painting has no grammar, no syntax, no vocabulary — and yet it speaks. Today, we learn to listen to visual art.",
                "Topic (0:30): Visual literacy in the age of Instagram — how understanding composition, colour theory, and symbolism makes you a more critical consumer of images.",
                "Interview (2:00): A curator at Istanbul Modern discusses how Turkish contemporary artists are reinterpreting Ottoman visual traditions for global audiences.",
                "Fun Fact (3:30): The human brain processes images 60,000 times faster than text. This is why propaganda, advertising, and social media all prioritise visuals.",
                "Challenge (4:00): Visit a museum (physically or virtually) and select one artwork. Record a three-minute audio guide for that artwork as if you were a museum docent."
            ],
            "student_task": "Create a podcast episode called 'Art Speaks.' Choose three artworks from different cultures and discuss what each communicates without words."
        },
        9: {
            "title": "Episode 9: The Health of Nations",
            "host": "Elif & Epidemiologist Dr. Deniz",
            "summary": "A global health deep dive — from pandemic preparedness to antimicrobial resistance — and Turkey's role in international health governance.",
            "segments": [
                "Intro (0:00): The next pandemic is not a question of 'if' but 'when.' Are we ready? More importantly — are we communicating readiness effectively?",
                "Topic (0:30): Health communication — why clear, honest, multilingual public health messaging saves more lives than any single medicine.",
                "Interview (2:00): A WHO communications officer explains how misinformation during health crises is itself a public health emergency — an 'infodemic.'",
                "Fun Fact (3:30): Turkey's family medicine reform of 2005 reduced infant mortality by 70% in a decade — one of the most successful primary healthcare transformations globally.",
                "Challenge (4:00): Create a one-minute public health announcement in English for a fictional health campaign in Turkey. Focus on clarity, empathy, and actionable advice."
            ],
            "student_task": "Produce a podcast episode titled 'Infodemic.' Investigate how health misinformation spreads on social media and propose three evidence-based counter-strategies."
        },
        10: {
            "title": "Episode 10: Building a Greener Tomorrow",
            "host": "Elif & Environmental Engineer Canan",
            "summary": "The final episode explores green technology innovations — from solar desalination to urban farming — and challenges listeners to become agents of environmental change.",
            "segments": [
                "Intro (0:00): The final episode of Season 1 — and the most important one. Because there is no Season 2 on a planet we have not protected.",
                "Topic (0:30): Green technology success stories from Turkey — the Karapınar solar plant, geothermal energy in Denizli, and wind farms along the Aegean coast.",
                "Interview (2:00): A young Turkish entrepreneur who won the UN Young Champions of the Earth award discusses her biodegradable packaging startup.",
                "Fun Fact (3:30): Turkey has enough geothermal energy potential to power the entire country for 200 years. Currently, less than 15% of this potential is utilised.",
                "Challenge (4:00): Design a green technology solution for your school or neighbourhood. Create a one-page English proposal including the problem, solution, cost estimate, and expected impact."
            ],
            "student_task": "Produce the season finale of your own podcast series. Reflect on everything you have learned this year and issue a personal call to action for your generation."
        }
    }
}
