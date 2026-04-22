"""Builder script: Run this once to generate grade11.py, then delete this file."""
import os

TARGET = os.path.join(os.path.dirname(__file__), "grade11.py")

content = '''"""
Grade 11 Content Banks - High School (Ages 16-17, B2 CEFR)
Complete content for 10 units with 16 bank sections.
Units: Future Jobs & Career, Hobbies & Skills, Hard Times, What a Life!,
       Back to the Past, Open Your Heart, Facts About Turkey, Sports & Fair Play,
       My Friends, Values & Norms
"""

# =============================================================================
# 1. STORY CHARACTERS
# =============================================================================
STORY_CHARACTERS = {
    11: {
        "main": [
            {"name": "Deniz", "age": 17, "trait": "ambitious aspiring engineer who dreams of designing sustainable cities"},
            {"name": "Elif", "age": 16, "trait": "compassionate debate champion with a passion for social justice"},
            {"name": "Can", "age": 17, "trait": "introspective history enthusiast who writes poetry in his spare time"},
            {"name": "Zeynep", "age": 16, "trait": "athletic and philosophical, questions everything around her"}
        ],
        "teacher": {
            "name": "Mr. Kenan",
            "role": "Literature and Philosophy teacher who inspires critical thinking"
        }
    }
}

# =============================================================================
# 2. STORY BANK
# =============================================================================
STORY_BANK = {
    11: {
        1: {
            "title": "The Crossroads of Tomorrow",
            "previously": "Deniz, Elif, Can, and Zeynep have just started their final preparatory year, each harbouring distinct ambitions for the future.",
            "episode": (
                "The autumn wind swept through the corridors of Anatolian High School as Deniz stared at the career aptitude results on his screen. "
                "He had always envisioned himself designing bridges that connected communities, yet the test suggested a future in data science. "
                "Elif noticed his furrowed brow from across the library and walked over with quiet determination. "
                "You look as though someone has rewritten your entire blueprint, she remarked, settling into the chair beside him. "
                "Deniz sighed and turned the screen toward her. According to this algorithm, I will have become a data analyst by 2035, not an engineer. "
                "Elif studied the results carefully, her analytical mind already dissecting the methodology. These tests measure tendencies, not destinies, she said firmly. "
                "Meanwhile, Can was in Mr. Kenan s office, discussing his own dilemma: whether to pursue literature or history at university. "
                "Mr. Kenan leaned back in his chair and offered a perspective that would alter Can s thinking permanently. "
                "By the time you graduate, you will have read thousands of texts. The question is not what you study but how deeply you engage with ideas. "
                "Can felt the weight of those words settle into his consciousness like stones dropped into still water. "
                "Zeynep, on the other hand, was on the track field, running laps as though she could outpace her own uncertainty. "
                "She had been offered a sports scholarship, yet her heart yearned for philosophy, a field her family considered impractical. "
                "That evening, the four friends gathered at their usual cafe near the school, each carrying invisible burdens. "
                "Deniz shared his frustration first, and to his surprise, the others responded not with solutions but with their own confessions of doubt. "
                "Elif admitted that her parents expected her to study law, though she dreamed of becoming a diplomat. "
                "Can confessed that he had secretly applied to a creative writing programme abroad without telling anyone. "
                "Zeynep revealed the scholarship offer, her voice cracking under the pressure of the decision. "
                "The cafe owner, an elderly woman who had overheard their conversation, placed four cups of Turkish tea on the table without being asked. "
                "I will have been running this cafe for forty years next spring, she said with a knowing smile. I never planned it. I followed what felt honest. "
                "Her words hung in the air like the steam rising from their glasses. "
                "Deniz looked at his friends and realised that the future was not a destination but a conversation they would keep having. "
                "They made a pact that night: by the end of the year, each would have explored at least one path they had never considered. "
                "As they stepped into the cool night air, the city lights reflected in their eyes like constellations waiting to be mapped. "
                "None of them noticed the envelope Mr. Kenan had slipped under the cafe door, an invitation to a national youth leadership summit."
            ),
            "cliffhanger": "What does Mr. Kenan s mysterious invitation contain, and will it change the trajectory of their carefully laid plans?",
            "vocab_tie": ["career aptitude", "blueprint", "trajectory", "scholarship", "summit"]
        },
        2: {
            "title": "The Hidden Talent",
            "previously": "The four friends received Mr. Kenan s invitation to a national youth leadership summit and began preparing.",
            "episode": (
                "The summit application required each participant to demonstrate a unique skill beyond their academic profile. "
                "Deniz, who had spent years with equations and technical drawings, found himself staring at a blank section labelled Creative Expression. "
                "It was Elif who suggested he try building a miniature bridge from reclaimed materials, engineering as art. "
                "Reluctantly, Deniz began collecting discarded wood and wire from the school workshop, his hands learning a new language. "
                "Elif herself had taken up calligraphy the previous summer, a hobby she had kept hidden from her debate colleagues. "
                "She feared they would consider it frivolous, yet the disciplined strokes brought her a peace that argumentation never could. "
                "Can had been secretly composing music, translating his poems into melodies on a second-hand keyboard in his bedroom. "
                "He remembered giving up piano lessons at twelve because his father insisted sports were more important for a young man. "
                "Now, at seventeen, his fingers moved across the keys with the confidence of someone reclaiming a stolen inheritance. "
                "Zeynep s hidden talent surprised everyone the most: she had been painting portraits of people she observed in public spaces. "
                "Her sketchbook was filled with faces of the bus driver, the simit seller, the old man feeding pigeons in the park. "
                "Mr. Kenan visited each of them individually during the preparation week, not to instruct but to observe. "
                "He watched Deniz struggle with a joint that refused to hold and said nothing, knowing the struggle itself was the lesson. "
                "He listened to Can play a hesitant melody and simply nodded, as though the music confirmed something he already knew. "
                "When he saw Zeynep s portraits, his eyes widened slightly, the only visible emotion he permitted himself. "
                "Elif showed him her calligraphy portfolio during lunch break, her hands trembling with rare vulnerability. "
                "Hobbies are not distractions from our purpose, Mr. Kenan told the group. They are windows into who we truly are. "
                "The deadline was three days away, and each friend had begun to see themselves through a different lens. "
                "Deniz s bridge model, imperfect and asymmetric, somehow looked more beautiful than any of his precise technical drawings. "
                "Can recorded his composition on his phone, listening to it on the bus, hearing both its flaws and its honesty. "
                "Zeynep added one final portrait to her collection: a self-portrait, the hardest one she had ever attempted. "
                "On the night they submitted applications, Elif raised her tea glass. To becoming more than our transcripts. "
                "They clinked glasses in the amber light, unaware that organisers had already flagged their applications as exceptional. "
                "The next morning, Mr. Kenan received a phone call that would complicate everything."
            ),
            "cliffhanger": "Who called Mr. Kenan, and why might the summit be in jeopardy just as they discovered their hidden talents?",
            "vocab_tie": ["calligraphy", "portfolio", "reclaimed", "composition", "transcript"]
        },
        3: {
            "title": "Through the Storm",
            "previously": "The friends submitted summit applications showcasing hidden talents, but Mr. Kenan received a troubling phone call.",
            "episode": (
                "The phone call brought devastating news: the summit venue had been severely damaged by an earthquake in the southeast. "
                "Mr. Kenan gathered the four students in his classroom before the announcement spread through official channels. "
                "Elif was the first to speak, her voice steady despite the shock. People have lost their homes. The summit is the least of our concerns. "
                "Deniz nodded, but his engineering mind was already racing through structural damage assessments. "
                "Can sat quietly, his notebook open, writing fragments of what he was feeling, a habit that had become his anchor during hard times. "
                "Zeynep asked what they could do, her body leaning forward as though ready to sprint toward the problem. "
                "Mr. Kenan had anticipated their reactions. The organisers have proposed relocating, but they need volunteer coordinators. "
                "He paused. They have asked whether our school would host it and whether you four would lead the effort. "
                "The challenge was enormous: three weeks to prepare a venue, coordinate with forty schools, and manage unfamiliar logistics. "
                "Deniz had not slept properly since hearing the news; aftershock reports reminded him of fragility he usually ignored. "
                "Elif threw herself into coordination, making calls during lunch and staying after school to draft schedules. "
                "By the end of the first week, she had dark circles under her eyes and a voice hoarse from endless conversations. "
                "Can volunteered at the counselling centre, where younger students came to talk about their fears and anxieties. "
                "He discovered that listening, truly listening, was harder and more important than any poem he had ever written. "
                "Zeynep organised a fundraising sports event, training while simultaneously managing registrations and sponsorships. "
                "On the twelfth day, Elif broke down in the library, overwhelmed by a logistics spreadsheet multiplying its problems. "
                "Deniz found her there, tears falling onto her keyboard, and for the first time he did not try to solve the problem. "
                "He simply sat beside her. You have already done more than anyone could have expected. It is enough. "
                "Those words, imperfect and unrehearsed, proved more effective than any strategic plan. "
                "Elif wiped her eyes, took a breath, and reorganised the spreadsheet with renewed clarity. "
                "By the third week, the gymnasium was transformed, decorated with Zeynep s portraits and Can s welcome poems. "
                "Mr. Kenan stood at the entrance on summit morning, watching his students greet delegates from across the country. "
                "He had never told them that the organisers first choice had been a prestigious private school in Istanbul. "
                "As the opening ceremony began, a message arrived on Elif s phone from an unknown number."
            ),
            "cliffhanger": "Who sent the mysterious message to Elif, and what revelation will it bring on the most important day of their lives?",
            "vocab_tie": ["resilience", "logistics", "aftershock", "coordinate", "fundraising"]
        },
        4: {
            "title": "Lives Intertwined",
            "previously": "The friends successfully hosted the summit after the original venue was damaged. Elif received a mysterious message.",
            "episode": (
                "The message read: Your grandmother was one of the first female engineers in Turkey. I have her blueprints. Panel Room 3. "
                "Elif had never known her maternal grandmother, who had passed away before she was born, spoken of only in whispers. "
                "Never had she imagined that her grandmother s story would intersect with her own at a summit in her own school. "
                "She slipped away from the opening ceremony, her heart hammering against her ribs like a trapped bird. "
                "In Panel Room 3 sat an elderly woman with silver hair: Professor Aysel Karaca, a retired civil engineer. "
                "Seldom had Elif felt so disarmed; the professor s gaze seemed to penetrate decades of family silence. "
                "Your grandmother, Neriman, and I graduated from the same programme in 1968, Professor Aysel began quietly. "
                "She opened a leather folder and revealed yellowed blueprints of a pedestrian bridge in Ankara. "
                "Not only had Neriman designed the bridge, but she had also fought to have it built when female engineers were discouraged. "
                "Elif traced the lines with her fingertip, feeling a connection that transcended time and silence. "
                "Meanwhile, Can was moderating a panel when a delegate from Diyarbakir shared a biography that left him speechless. "
                "The delegate s great-uncle had been a poet during the early Republic, writing in Turkish and Kurdish, bridging cultures. "
                "Rarely had Can encountered someone who understood the power of words the way this stranger did. "
                "Deniz attended a workshop on sustainable architecture and met a young woman from Trabzon who had designed a rainwater system. "
                "Her ingenuity challenged his assumption that innovation required expensive laboratories and prestigious degrees. "
                "Zeynep, during the sports ethics discussion, encountered a paralympic athlete whose story redefined her understanding of strength. "
                "Under no circumstances had she expected to cry during a panel discussion, yet tears streamed freely down her face. "
                "That evening, the four friends sat on the school rooftop and shared what they had experienced. "
                "Elif showed photographs of the blueprints, her voice thick. My family never told me. They erased her. "
                "Can read aloud a poem the delegate had given him, the words floating into the night sky like sparks. "
                "Deniz spoke about the Trabzon girl and questioned whether his ambitions were driven by ego or purpose. "
                "Zeynep was last. I met someone who lost both legs and still competes internationally. What is my excuse for hesitating? "
                "The city below them hummed with ordinary life, indifferent to the extraordinary transformations on that rooftop. "
                "Mr. Kenan found them there an hour later, not to reprimand them but to deliver a second piece of news."
            ),
            "cliffhanger": "What is Mr. Kenan s second announcement, and how will these discovered biographies change their own life stories?",
            "vocab_tie": ["biography", "blueprint", "perseverance", "intersect", "inversion"]
        },
        5: {
            "title": "Echoes of Yesterday",
            "previously": "At the summit, each friend discovered a powerful biography mirroring their aspirations. Mr. Kenan arrived with more news.",
            "episode": (
                "Mr. Kenan s news was both thrilling and daunting: the Ministry had selected their school for a pilot heritage project. "
                "Each student would research a historical period and present how its lessons applied to contemporary challenges. "
                "Deniz wished he had paid more attention in history class; his knowledge of the past was embarrassingly shallow. "
                "If only he had listened when Can tried to share Ottoman engineering marvels during study sessions, he would not feel so lost. "
                "Elif chose the early Republic era, drawn by her grandmother s story and the broader struggle for women s rights. "
                "She wished she could have met Neriman, sat across from her, and asked the questions that now burned unanswered. "
                "Can selected the Seljuk period, fascinated by the caravanserais, structures built to shelter travellers of every origin. "
                "He saw in them a metaphor for the world he wanted to write into existence: open, generous, unafraid of difference. "
                "Zeynep chose ancient Olympia and its connection to modern sports ethics, bridging her two passions perfectly. "
                "If only the ancient Greeks had included women in the original games, how different athletics history might have been. "
                "The research took them to unexpected places: Deniz visited an Ottoman aqueduct with Professor Aysel. "
                "Standing beneath stone arches, he understood that engineering was not about conquering nature but conversing with it. "
                "Elif spent weekends in the national archives, uncovering documents about women excluded from historical narratives. "
                "She wished the archivists had been more helpful; their indifference felt like a continuation of the erasure she studied. "
                "Can travelled to Konya with Mr. Kenan to visit a restored caravanserai, where acoustics made whispers feel monumental. "
                "He recorded ambient sounds and wove them into a new composition inspired by centuries of hospitality. "
                "Zeynep interviewed elderly athletes at a retirement home, collecting oral histories never officially recorded. "
                "One former wrestler told her: We did not compete to defeat our opponents. We competed to honour the tradition. "
                "Presentation day arrived with the weight of months of research and the lightness of genuine discovery. "
                "Deniz projected aqueduct images alongside his sustainable bridge designs, showing continuity across centuries. "
                "Elif s presentation on erased women engineers received a standing ovation, including from Professor Aysel. "
                "Can performed his composition live, Seljuk-inspired melodies filling the auditorium with ancient and urgent sounds. "
                "Zeynep screened a short documentary from athlete interviews, trembling voices carrying more authority than any textbook. "
                "As applause filled the hall, none of them noticed a journalist from a national newspaper had been recording everything."
            ),
            "cliffhanger": "What will the journalist publish, and will national attention bring opportunity or unwanted scrutiny?",
            "vocab_tie": ["heritage", "caravanserai", "archive", "continuity", "erasure"]
        },
        6: {
            "title": "The Giving Thread",
            "previously": "The friends completed a heritage project connecting past and present. A journalist recorded their presentations.",
            "episode": (
                "The newspaper article appeared on Monday under the headline: Four Students Prove That History Is Not Dead. "
                "By Tuesday, it had been shared over fifty thousand times on social media, and the school phones were overwhelmed. "
                "Deniz had his mother read the article aloud at breakfast, his engineering sketches displayed prominently in the photograph. "
                "Elif received messages from women engineers across the country, thanking her for uncovering stories they had given up hearing. "
                "Can s composition was requested by a radio station, and Zeynep s documentary was invited to a youth film festival. "
                "The attention was flattering, but Mr. Kenan reminded them that visibility without purpose was merely vanity. "
                "The earthquake region still needs help, he said. What will you do with this platform you have been given? "
                "The question struck like a bell in a quiet room. They had been so consumed that the earthquake had faded from consciousness. "
                "Elif proposed a charity initiative, a structured long-term project rather than a one-time donation drive. "
                "She had the organisers contact her; she had them send detailed needs assessments; she had logistics mapped in forty-eight hours. "
                "Deniz designed a modular classroom using sustainable materials, something assemblable by volunteers without specialised tools. "
                "He had the blueprints reviewed by Professor Aysel, who made him redesign the foundation twice before approving. "
                "Can organised a benefit concert, curating student performances and inviting the Diyarbakir delegate to read poetry. "
                "He got the administration to waive the auditorium fee; he had local businesses donate refreshments and printing. "
                "Zeynep launched a sports equipment drive, collecting used but functional gear from athletic clubs across the city. "
                "She had coaches and athletes sign donated items with encouragement messages, a small gesture with enormous emotional weight. "
                "The initiative was named Kopru, Bridge, an homage to Deniz s engineering passion and their metaphorical connections. "
                "Within two weeks, Kopru raised enough funds for three modular classrooms and a small sports facility. "
                "The four friends travelled to the earthquake zone during winter break, accompanied by Mr. Kenan and volunteer builders. "
                "Deniz supervised construction, his hands blistered but his spirit soaring as the first classroom took shape. "
                "Elif coordinated with local officials, navigating bureaucratic obstacles with diplomatic skill that surprised even herself. "
                "Can taught a creative writing workshop to children in a temporary shelter, their stories raw and full of stubborn hope. "
                "Zeynep organised a mini sports day for displaced children, watching them laugh for what some parents said was the first time in months. "
                "On their last evening, an elderly woman pressed a hand-knitted scarf into Elif s hands. "
                "You have given us walls, the woman said, but more importantly, you have given us the feeling that we have not been forgotten."
            ),
            "cliffhanger": "As they return from the earthquake zone, each carries a transformed sense of purpose, but will ordinary school life feel impossibly small?",
            "vocab_tie": ["charity", "modular", "bureaucratic", "causative", "initiative"]
        },
        7: {
            "title": "The Land Speaks",
            "previously": "The friends launched Kopru, a charity initiative building modular classrooms in the earthquake zone. They returned transformed.",
            "episode": (
                "Returning to classes after the earthquake zone felt like stepping from colour into monochrome. "
                "Deniz found himself unable to concentrate on physics, his mind drifting to children studying in the classrooms he had helped build. "
                "Mr. Kenan announced a new assignment: a comprehensive project on the geography, culture, and hidden stories of Turkey. "
                "The project required fieldwork and primary research, precisely the antidote to their post-service restlessness. "
                "Elif chose to investigate women who contributed to Turkey s cultural heritage but whose names appeared in no official textbook. "
                "The women whose achievements had been documented only in family photographs and village memories were the stories she wanted to amplify. "
                "Can focused on the literary traditions of Anatolia, the oral storytelling that had survived empires and modernisation. "
                "The stories which he collected from elderly villagers in the Black Sea region carried a rhythm no written text could replicate. "
                "Deniz studied the ancient water management systems of Cappadocia, underground cities whose engineering still baffled modern experts. "
                "The tunnels through which air circulated had been designed with fluid dynamics understanding that preceded formal theory by centuries. "
                "Zeynep explored oil wrestling in Kirkpinar, where sportsmanship and ritual intertwined in ways modern athletics had abandoned. "
                "The wrestlers whom she interviewed spoke of sport not as competition but as a form of moving meditation. "
                "Each friend s research drew them deeper into aspects of Turkey they had taken for granted or never known. "
                "Deniz stood in an underground city in Kaymakli, running his hands along walls carved by people whose names history had not preserved. "
                "He felt kinship with those anonymous engineers, builders who solved problems not for fame but for survival and community. "
                "Elif visited a Hatay village where women maintained a centuries-old mosaic-making tradition, each piece a universe of colour and patience. "
                "Can recorded a meddah, a traditional storyteller, in a Bursa teahouse, the man s voice rising and falling like a river through a canyon. "
                "Zeynep attended the Kirkpinar festival, where the opening ceremony moved her to tears with its blend of ancient ritual and celebration. "
                "Back at school, they assembled findings into a multimedia exhibition transforming the gymnasium into a journey across Turkey. "
                "Visitors walked through recreated environments: a Cappadocian tunnel, a Black Sea storytelling circle, a mosaic workshop, a wrestling arena. "
                "The exhibition attracted not only the school community but also local media and cultural organisations. "
                "A representative from UNESCO s cultural heritage programme attended and expressed interest in supporting similar youth projects. "
                "Mr. Kenan watched from the back of the gymnasium, his expression unreadable but his eyes bright with something like pride. "
                "That evening, the UNESCO representative asked to meet with the four students privately."
            ),
            "cliffhanger": "What does the UNESCO representative want, and could this meeting open a door to an international stage none had dared imagine?",
            "vocab_tie": ["heritage", "Cappadocia", "mosaic", "documentation", "Kirkpinar"]
        },
        8: {
            "title": "The Fair Play Accord",
            "previously": "The friends created a cultural exhibition about Turkey that attracted UNESCO attention. A private meeting was requested.",
            "episode": (
                "The UNESCO representative, Dr. Miriam Okafor, was a Nigerian-born cultural anthropologist whose warmth immediately put them at ease. "
                "She explained that UNESCO was launching a global youth programme on sports ethics and wanted their school as Turkey s pilot site. "
                "Zeynep s eyes widened: this was the intersection of her two passions, delivered by forces she could not have orchestrated. "
                "The programme would culminate in an international conference in Geneva, where student delegates would present findings on ethics. "
                "Deniz, ever practical, asked about funding. Dr. Okafor said UNESCO would cover travel, impressed by their Kopru initiative. "
                "Can, whose shyness made international stages terrifying, felt his stomach contract. School assemblies were one thing; Geneva was another. "
                "Elif immediately began structuring a research plan, her organisational instincts activated like a well-calibrated machine. "
                "Mr. Kenan served as faculty advisor but made clear the students would drive every decision. This is your project. I am the safety net. "
                "Research revealed uncomfortable truths: doping scandals, match-fixing allegations, and the commodification of young athletes in Turkey. "
                "Zeynep interviewed a former national team athlete who had been pressured to use performance-enhancing substances at seventeen. "
                "Shaken, she sat alone in the changing room for an hour, reconsidering every supplement and regimen she had accepted without question. "
                "Deniz analysed sports infrastructure economics, discovering publicly funded facilities that served private interests over community needs. "
                "Elif examined legal frameworks governing youth sports, finding gaps in protection that left young athletes vulnerable to exploitation. "
                "Can collected personal narratives from retired athletes, stories painting a complex picture of glory, sacrifice, and abandonment. "
                "They structured their presentation around a Fair Play Accord, a student-drafted charter of ethical principles for youth sports. "
                "They consulted coaches, parents, psychologists, and fellow students via an online survey receiving over three thousand responses. "
                "The accord addressed six pillars: bodily autonomy, mental health, equitable access, anti-corruption education, cultural respect, and athlete aftercare. "
                "Drafting took weeks of debate, revision, and compromise, teaching them more about diplomacy than any textbook. "
                "Zeynep presented the athletic perspective, speaking about pressure to win at any cost and how it corroded the values sports claimed to uphold. "
                "Can wrote the preamble with the precision of a poet and the gravity of a legislator. "
                "Elif structured legal recommendations, drawing on international sports law and child protection frameworks. "
                "Deniz designed visual presentations, translating complex data into compelling infographics telling human stories through numbers. "
                "The day before departure, the school held a send-off assembly, and applause carried them out the door into the unknown. "
                "At the airport, Elif checked her email and found a message from the Turkish Olympic Committee requesting a formal copy of the Accord."
            ),
            "cliffhanger": "How will Geneva receive their bold charter, and what will the Olympic Committee s interest mean for four students who started the year uncertain?",
            "vocab_tie": ["ethics", "accord", "commodification", "autonomy", "charter"]
        },
        9: {
            "title": "The Bonds That Hold",
            "previously": "The friends drafted a Fair Play Accord and were invited to present it at UNESCO in Geneva. The Olympic Committee expressed interest.",
            "episode": (
                "Geneva was everything and nothing like they had imagined: pristine, international, and quietly intimidating in its institutional grandeur. "
                "The conference centre overlooked Lake Geneva, glass walls reflecting mountains that seemed to belong to a different planet from their school. "
                "Deniz, the most composed during preparations, became unexpectedly anxious upon seeing the delegate list: forty-seven countries. "
                "Elif seemed to grow taller in the presence of challenge, her confidence expanding to fill the enormous rooms. "
                "Can clutched his notebook like a talisman, having rewritten his preamble speech seven times on the flight. "
                "Zeynep dealt with nerves the only way she knew: a five-a.m. run along the lake, cold air sharpening her focus. "
                "Their presentation was scheduled for the second afternoon, meaning a full day of watching other delegations and comparing. "
                "The Brazilian team presented on favela sports programmes; Japan addressed the psychological toll of perfectionism in youth athletics. "
                "Each presentation was polished and powerful, and with every passing hour, the Turkish team felt both inspired and increasingly small. "
                "That evening, tension surfaced. Deniz criticised Elif s slide transitions; Elif snapped at Can for mumbling during rehearsal. "
                "Can withdrew into silence, which made Zeynep angry because she interpreted quietness as disengagement rather than anxiety. "
                "Mr. Kenan sensed the fracture at breakfast. You are not here to be perfect. You are here to be honest. Moreover, you are here as friends. "
                "His words functioned as both reminder and repair. Besides, they all knew he was right: their strength was collective trust, not individual brilliance. "
                "They spent the morning reconciling: Deniz apologised for being controlling; Elif acknowledged her sharpness under pressure. "
                "Can explained his silence was paralysis, not indifference, and Zeynep admitted she had been projecting her own fear. "
                "By lunchtime they were a team again, imperfect, honest, and ready. Furthermore, the argument had revealed their investment in each other. "
                "Can s preamble shook for three sentences before steadying into quiet authority. "
                "Elif delivered the legal framework with clarity that commanded the room; even senior delegates leaned forward. "
                "Deniz s infographics drew audible reactions, particularly a visualisation correlating youth dropout rates with ethical violations. "
                "Zeynep closed with personal testimony about the scholarship that forced her to choose between body and mind. "
                "In addition to fair rules, we need fair conversations, she concluded. Young athletes deserve to be heard, not just measured. "
                "The applause was not the loudest but, as Dr. Okafor later told them, the most sincere. "
                "Three delegations requested copies before the session ended; consequently, the document began circulating internationally that evening."
            ),
            "cliffhanger": "As the Accord gains international traction, how will the friends navigate attention and strain when they return home?",
            "vocab_tie": ["delegation", "reconcile", "moreover", "consequently", "testimony"]
        },
        10: {
            "title": "The Compass Within",
            "previously": "The friends presented the Fair Play Accord at Geneva to international acclaim. Their friendship was tested and strengthened.",
            "episode": (
                "They returned to Turkey as minor celebrities, an uncomfortable status for students who defined themselves by work, not image. "
                "The principal organised a press conference, during which Deniz gave measured answers while Elif deflected personal questions toward substance. "
                "Can refused to attend, claiming a headache, though everyone knew he could not bear the performative nature of media attention. "
                "Zeynep attended but spent the event staring out the window, calculating how many training sessions she had missed. "
                "The weeks that followed forced each to confront a philosophical question they had been circling all year: What do we truly value? "
                "Deniz received an internship offer from a prestigious engineering firm, a remarkable opportunity for a high school student. "
                "He should have been elated, yet the offer felt hollow compared to the satisfaction of building classrooms in the earthquake zone. "
                "He spent three evenings with his father, who finally said: Prestige is what others give you. Purpose is what you give yourself. "
                "Elif was invited to join a political youth council, a path aligning perfectly with her diplomatic aspirations and family expectations. "
                "She accepted, then withdrew two days later, realising she had said yes to please her parents rather than herself. "
                "The conversation with her mother was the hardest she had ever had, harder than any debate or international presentation. "
                "Can submitted his portfolio to the creative writing programme abroad and received an acceptance letter. "
                "He must have read the letter fifty times before telling anyone, joy tempered by knowing that leaving meant leaving his friends. "
                "Zeynep finally decided about the sports scholarship: she accepted it but negotiated permission to minor in philosophy. "
                "The university had never received such a request from an athletic recruit; they granted it, impressed by her conviction. "
                "Mr. Kenan called them to his office one last time, the same office where Can had sat twelve months earlier, uncertain and afraid. "
                "He did not give a speech. Instead, he placed four envelopes on his desk, each containing a letter he had written individually. "
                "Deniz s letter spoke of the courage required to choose meaning over prestige. "
                "Elif s addressed the strength it takes to disappoint those we love in order to be true to ourselves. "
                "Can s acknowledged the loneliness of the creative path and assured him that distance does not diminish true friendship. "
                "Zeynep s praised her refusal to be defined by a single talent and her insistence on wholeness. "
                "They read their letters in silence, late afternoon sun casting long shadows across Mr. Kenan s cluttered desk. "
                "Elif was the first to cry, which surprised no one. Can was the second, which surprised everyone. "
                "They left the office together, walking through school corridors one final time, footsteps echoing off walls that had witnessed their transformation. "
                "Deniz looked at his friends: Whatever happens next, I want you to know that this year taught me what matters."
            ),
            "cliffhanger": "As they step into separate futures, the bonds forged this year become the invisible architecture of the adults they are becoming.",
            "vocab_tie": ["values", "conviction", "threshold", "prestige", "philosophy"]
        }
    }
}
'''

with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Part 1 written to {TARGET}")
