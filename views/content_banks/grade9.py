"""
Grade 9 Content Banks - High Tier (Ages 14-15, B1+ CEFR)
10 Units, 16 Banks per unit
Themes: Student Life, Personality & Identity, Modern Communication,
        Tenses Review, World Literature, Global Issues, Science & Innovation,
        Art & Expression, Health & Well-being, The Environment
"""

STORY_CHARACTERS = {
    9: {
        1: [
            {"name": "Emre", "role": "ambitious high school freshman", "traits": "organised, curious, slightly anxious about new school"},
            {"name": "Selin", "role": "senior student mentor", "traits": "supportive, experienced, natural leader"},
            {"name": "Mr. Demir", "role": "guidance counsellor", "traits": "approachable, wise, encouraging"}
        ],
        2: [
            {"name": "Defne", "role": "introspective teenager", "traits": "thoughtful, creative, struggles with self-expression"},
            {"name": "Can", "role": "outgoing classmate", "traits": "confident, empathetic, socially aware"},
            {"name": "Ms. Yilmaz", "role": "psychology teacher", "traits": "insightful, warm, analytical"}
        ],
        3: [
            {"name": "Berk", "role": "tech-savvy student", "traits": "innovative, digitally fluent, entrepreneurial"},
            {"name": "Zeynep", "role": "journalism club president", "traits": "articulate, critical thinker, ethical"},
            {"name": "Mr. Aksoy", "role": "IT teacher", "traits": "forward-thinking, practical, patient"}
        ],
        4: [
            {"name": "Arda", "role": "exchange student from Germany", "traits": "multilingual, observant, adaptable"},
            {"name": "Elif", "role": "grammar enthusiast", "traits": "detail-oriented, helpful, systematic"},
            {"name": "Ms. Kaya", "role": "English teacher", "traits": "methodical, passionate about languages, encouraging"}
        ],
        5: [
            {"name": "Yasemin", "role": "avid reader and book club leader", "traits": "imaginative, eloquent, passionate about stories"},
            {"name": "Kerem", "role": "reluctant reader turned enthusiast", "traits": "initially sceptical, gradually inspired, analytical"},
            {"name": "Mr. Polat", "role": "literature teacher", "traits": "scholarly, dramatic, deeply knowledgeable"}
        ],
        6: [
            {"name": "Deniz", "role": "student activist", "traits": "passionate, informed, determined to make a difference"},
            {"name": "Mert", "role": "debate team captain", "traits": "logical, persuasive, open-minded"},
            {"name": "Ms. Celik", "role": "social studies teacher", "traits": "globally aware, inspiring, fair-minded"}
        ],
        7: [
            {"name": "Tugce", "role": "aspiring scientist", "traits": "methodical, curious, inventive"},
            {"name": "Onur", "role": "robotics club member", "traits": "technical, collaborative, persistent"},
            {"name": "Dr. Ozkan", "role": "science teacher", "traits": "experimental, encouraging, knowledgeable"}
        ],
        8: [
            {"name": "Hazal", "role": "talented visual artist", "traits": "expressive, sensitive, unconventional thinker"},
            {"name": "Burak", "role": "musician and songwriter", "traits": "creative, emotionally intelligent, reflective"},
            {"name": "Ms. Erdem", "role": "art teacher", "traits": "inspiring, open-minded, culturally aware"}
        ],
        9: [
            {"name": "Ceren", "role": "school health ambassador", "traits": "health-conscious, responsible, caring"},
            {"name": "Kaan", "role": "student athlete", "traits": "disciplined, competitive, learning about balance"},
            {"name": "Dr. Acar", "role": "school nurse and health educator", "traits": "knowledgeable, approachable, preventive-minded"}
        ],
        10: [
            {"name": "Ipek", "role": "environmental club founder", "traits": "eco-conscious, proactive, scientifically minded"},
            {"name": "Cem", "role": "urban planning enthusiast", "traits": "analytical, solution-oriented, community-focused"},
            {"name": "Mr. Toprak", "role": "geography and ecology teacher", "traits": "nature-loving, data-driven, activist"}
        ]
    }
}

STORY_BANK = {
    9: {
        1: [
            "Emre stood at the entrance of his new high school, clutching his timetable with slightly trembling hands.",
            "The corridors seemed endless compared to his middle school, and hundreds of unfamiliar faces rushed past him in every direction.",
            "Selin, wearing a mentor badge, noticed Emre's confused expression and approached him with a reassuring smile.",
            "She explained that every freshman felt overwhelmed during the first week but that the feeling would pass quickly.",
            "Emre confessed that he was worried about managing five major subjects alongside extracurricular activities.",
            "Selin laughed gently and shared that she had felt exactly the same way three years ago when she first arrived.",
            "She took him on a tour of the key facilities: the library, the science laboratories, the sports hall, and the student lounge.",
            "At each stop, Selin introduced Emre to a club representative who briefly described their activities and meeting times.",
            "By lunchtime, Emre had already signed up for the debate club and the photography society.",
            "Mr. Demir, the guidance counsellor, gave a welcoming speech in the assembly hall about setting realistic academic goals.",
            "He emphasised that high school was not just about grades but also about discovering one's strengths and passions.",
            "After the assembly, Emre felt a wave of relief wash over him as he realised he was not alone in this journey.",
            "He exchanged phone numbers with three other freshmen who shared his classes, and they agreed to form a study group.",
            "Walking home that afternoon, Emre reflected that what had seemed terrifying in the morning now felt like the beginning of an exciting chapter."
        ],
        2: [
            "Defne sat in the school courtyard during break, sketching abstract patterns in her notebook while her classmates chatted loudly around her.",
            "She often felt like an observer rather than a participant, watching social interactions as though studying them from behind glass.",
            "In psychology class, Ms. Yilmaz introduced the concept of personality types and asked students to take a self-assessment quiz.",
            "Defne discovered that she was an introverted-intuitive type, which explained her preference for deep thinking over small talk.",
            "Can, who sat next to her, scored as an extroverted-feeling type and was fascinated by how different their results were.",
            "He told Defne that he admired her ability to concentrate deeply on creative tasks, something he found genuinely difficult.",
            "Defne was surprised by the compliment because she had always considered her quietness to be a social disadvantage.",
            "Ms. Yilmaz explained that every personality type brought unique strengths to a group, and that diversity of thought was essential.",
            "For their project, Can and Defne were paired together to create a presentation on the value of different perspectives.",
            "Initially, Defne was nervous about presenting in front of the class, but Can encouraged her to share her insights confidently.",
            "During the presentation, Defne spoke about how introverts process information differently, using thoughtful examples from her own experience.",
            "The class responded with genuine interest and several students admitted they had never considered these differences before.",
            "After the presentation, three classmates approached Defne to tell her that her perspective had changed how they viewed quiet people.",
            "That evening, Defne wrote in her journal that understanding herself better had actually helped her connect more authentically with others."
        ],
        3: [
            "Berk was working on a new feature for the school's mobile application when Zeynep walked into the computer lab looking frustrated.",
            "She explained that the school newspaper's website had crashed during peak traffic and she needed urgent technical help.",
            "Berk quickly diagnosed the problem as a server overload issue and suggested migrating to a cloud-based hosting service.",
            "While he worked on the technical fix, Zeynep told him about the ethical dilemma she was facing with a recent article.",
            "A student had shared sensitive information on social media, and Zeynep was debating whether the newspaper should report on it.",
            "Berk pointed out that modern communication platforms had blurred the line between public and private information.",
            "Mr. Aksoy, who overheard their conversation, joined in and discussed the concept of digital citizenship and online responsibility.",
            "He challenged both students to think about how technology could be used to inform without causing unnecessary harm.",
            "Zeynep decided to write an editorial about responsible social media use instead of reporting on the individual incident.",
            "Berk offered to create an interactive infographic about digital literacy to accompany the article on the website.",
            "Together, they launched a school-wide digital awareness campaign that included workshops on privacy settings and online etiquette.",
            "The campaign received enthusiastic support from both students and teachers, and other schools expressed interest in adopting similar programmes.",
            "Mr. Aksoy praised their initiative and suggested they present their project at the regional education technology conference.",
            "Berk and Zeynep realised that the most powerful use of modern communication was not just sharing information but shaping responsible digital communities."
        ],
        4: [
            "Arda had arrived in Turkey from Germany just two weeks ago, and he was still adjusting to the rhythm of his new school.",
            "Although he spoke English fluently, he noticed that certain grammatical structures were used differently in academic contexts here.",
            "Elif, who was known as the class grammar expert, offered to help Arda review English tenses during their study period.",
            "She created a comprehensive timeline chart that mapped all twelve English tenses from simple present to future perfect continuous.",
            "Arda was impressed by Elif's systematic approach and admitted that even native-level speakers sometimes confused tense usage.",
            "Ms. Kaya assigned a challenging essay that required students to use at least eight different tenses accurately and meaningfully.",
            "Arda struggled with the past perfect continuous, finding it difficult to express duration before a specific past event naturally.",
            "Elif showed him a technique where she visualised each tense as a different colour on a timeline, making the relationships clearer.",
            "Together, they wrote practice paragraphs about historical events, using multiple tenses to describe causes, events, and consequences.",
            "Ms. Kaya reviewed their work and highlighted how mastering tenses allowed writers to control the flow of time in their narratives.",
            "She explained that understanding tense relationships was essential for academic writing, storytelling, and even scientific reporting.",
            "Arda began to see grammar not as a set of rigid rules but as a flexible tool for precise and nuanced expression.",
            "By the end of the unit, he had written an essay about his cross-cultural experiences that his teacher described as remarkably sophisticated.",
            "Elif and Arda agreed that their collaboration had deepened both their understanding, proving that teaching others was the best way to learn."
        ],
        5: [
            "Yasemin had organised the school's first international book club, and today they were discussing a classic novel from Latin American literature.",
            "She had chosen the book because it combined magical realism with powerful social commentary, themes she found deeply compelling.",
            "Kerem, who had reluctantly joined the club at his mother's insistence, admitted that he had never finished a novel for pleasure before.",
            "However, something about this particular story had captivated him, and he had read the entire book in just three days.",
            "Mr. Polat, who served as the club's faculty adviser, began the discussion by asking what the author's use of magical elements revealed about reality.",
            "Yasemin argued that the magical elements represented the emotional truths that conventional narrative could not adequately express.",
            "Kerem surprised everyone by offering a different interpretation, suggesting that the magic symbolised the resilience of ordinary people.",
            "Mr. Polat smiled and noted that great literature always generated multiple valid interpretations, which was precisely what made it great.",
            "The discussion then moved to comparing the novel with a Turkish literary work that used similar techniques of blending reality and imagination.",
            "Several students pointed out thematic parallels between the two works despite their vastly different cultural contexts.",
            "Yasemin proposed that they create a world literature map on the classroom wall, connecting books from different countries through shared themes.",
            "The project grew into an interactive display that included student reviews, author biographies, and thematic connections across continents.",
            "By the semester's end, the book club had doubled in membership, and even students who had never enjoyed reading were participating actively.",
            "Kerem told Yasemin that the club had taught him that stories were not just entertainment but windows into the human experience across cultures."
        ],
        6: [
            "Deniz arrived at school early on Monday carrying a stack of printouts about global poverty statistics she had researched over the weekend.",
            "She was preparing for the inter-school debate tournament, and her team's topic was whether wealthy nations had a moral obligation to reduce global inequality.",
            "Mert, the debate team captain, helped her organise the arguments into a logical framework that addressed economic, social, and ethical dimensions.",
            "Ms. Celik reminded them that a strong debater must understand both sides of an argument equally well before taking a position.",
            "Deniz found it challenging to construct counterarguments against her own beliefs, but she recognised the intellectual value of the exercise.",
            "During their research, they discovered that climate change disproportionately affected the poorest communities, adding another layer to their argument.",
            "Mert suggested they include real case studies from different regions to make their arguments more concrete and emotionally compelling.",
            "The team practised their speeches after school, timing each segment carefully and refining their transitions between points.",
            "On the day of the debate, Deniz delivered the opening statement with a combination of statistical evidence and personal conviction that impressed the judges.",
            "The opposing team presented strong economic arguments about national sovereignty and the limitations of international aid programmes.",
            "Mert's rebuttal was sharp and well-structured, acknowledging the valid concerns while redirecting focus to long-term global cooperation.",
            "Their team won the debate, but more importantly, both teams agreed afterwards that the discussion had broadened their understanding of global issues.",
            "Ms. Celik praised Deniz and Mert for demonstrating that informed debate was one of the most powerful tools for addressing complex global challenges.",
            "Deniz wrote a reflection essay arguing that understanding global issues was not optional for their generation but an essential responsibility."
        ],
        7: [
            "Tugce had been working on her science fair project for three months, developing a water filtration system using locally available materials.",
            "Her goal was to create an affordable solution that could provide clean drinking water to rural communities without access to modern infrastructure.",
            "Onur, from the robotics club, offered to help her design an automated monitoring system that could track the filter's performance in real time.",
            "Dr. Ozkan supervised their collaboration and encouraged them to apply the scientific method rigorously at every stage of development.",
            "They began by researching existing filtration technologies, analysing the strengths and limitations of each approach in peer-reviewed journals.",
            "Tugce hypothesised that a combination of activated charcoal, sand, and a bio-membrane could remove ninety-five percent of common contaminants.",
            "Onur designed a sensor array using Arduino microcontrollers that measured water clarity, pH levels, and bacterial contamination rates.",
            "Their initial tests showed promising results, but the flow rate was too slow for practical household use, requiring significant design modifications.",
            "After several iterations, they discovered that adjusting the layer thickness and adding a gravity-fed pressure system dramatically improved performance.",
            "Dr. Ozkan helped them document their methodology carefully, emphasising that reproducibility was a cornerstone of credible scientific research.",
            "At the regional science fair, their project received the innovation award for its practical application of scientific principles to real-world problems.",
            "A local engineering firm expressed interest in developing a prototype based on their design, offering mentorship and laboratory access.",
            "Tugce and Onur presented their findings at a school assembly, inspiring other students to pursue science projects with social impact.",
            "They concluded that true scientific innovation was not about complexity but about applying knowledge creatively to solve problems that mattered."
        ],
        8: [
            "Hazal had been experimenting with mixed-media art for months, combining traditional painting techniques with digital elements and found materials.",
            "Her latest piece explored the theme of cultural identity in a globalised world, using layers of Turkish calligraphy beneath modern urban imagery.",
            "Burak, who was composing music for the school's end-of-year exhibition, suggested they collaborate on a multimedia installation.",
            "He had been writing instrumental pieces inspired by the contrast between traditional Turkish music and contemporary electronic sounds.",
            "Ms. Erdem encouraged their collaboration, explaining that the boundaries between artistic disciplines were becoming increasingly fluid in the modern art world.",
            "Hazal and Burak spent weeks discussing how visual and auditory elements could work together to create a unified emotional experience.",
            "They decided that each of Hazal's paintings would be accompanied by a specific musical composition that reflected the same emotional themes.",
            "The installation space was designed so that visitors would walk through a corridor where the art and music changed progressively from traditional to modern.",
            "During the creation process, Hazal discovered that listening to Burak's compositions while painting influenced her colour choices and brushwork significantly.",
            "Similarly, Burak found that studying Hazal's paintings helped him find melodic structures he would never have discovered through music alone.",
            "On the opening night, the installation attracted more visitors than any previous school exhibition, and the response was overwhelmingly positive.",
            "Several visitors commented that the combination of visual art and music had affected them more deeply than either medium could have achieved independently.",
            "Ms. Erdem invited a local gallery curator to view the installation, and she expressed interest in featuring their work in a youth arts showcase.",
            "Hazal and Burak reflected that art was most powerful when it crossed boundaries and invited audiences to experience the world through multiple senses simultaneously."
        ],
        9: [
            "Ceren had noticed that many of her classmates were skipping meals, sleeping poorly, and relying heavily on caffeine to keep up with their studies.",
            "As the school's newly appointed health ambassador, she decided to address these issues by organising a comprehensive wellness awareness week.",
            "Kaan, a varsity basketball player, admitted that even athletes sometimes neglected proper nutrition and mental health in pursuit of performance goals.",
            "Dr. Acar provided Ceren with research data showing that sleep deprivation among teenagers directly correlated with reduced academic performance.",
            "Together, they designed a series of interactive workshops covering nutrition, sleep hygiene, stress management, and the importance of physical activity.",
            "Ceren created informative posters using evidence-based guidelines from the World Health Organisation, which she displayed throughout the school corridors.",
            "Kaan shared his personal experience of burnout after training excessively without adequate rest, explaining how it had affected both his health and his grades.",
            "The first workshop on nutrition attracted sixty students, far exceeding their expectations, and the discussions were remarkably honest and open.",
            "Several students revealed that they had developed unhealthy eating habits due to exam stress and unrealistic body image expectations from social media.",
            "Dr. Acar explained the science behind stress responses and taught practical relaxation techniques including deep breathing and progressive muscle relaxation.",
            "The school administration was so impressed with the initiative that they agreed to introduce a weekly mindfulness session during morning assembly.",
            "Ceren also established a peer support network where trained student volunteers could provide basic wellness guidance to their classmates.",
            "By the end of the term, a school survey showed that students' self-reported well-being scores had improved by twenty-three percent compared to the previous year.",
            "Ceren and Kaan agreed that investing in health was not a distraction from academic success but rather its most essential foundation."
        ],
        10: [
            "Ipek had spent the summer collecting data on air quality, water pollution, and biodiversity levels in her neighbourhood using portable monitoring equipment.",
            "The results were alarming: particulate matter levels regularly exceeded safe limits, and the local stream contained elevated concentrations of industrial chemicals.",
            "She presented her findings to Cem, who was researching urban planning solutions for his geography coursework, and together they formulated an action plan.",
            "Mr. Toprak helped them understand the complex relationships between urbanisation, industrial activity, and environmental degradation in rapidly developing cities.",
            "Ipek proposed a school-wide environmental audit that would measure energy consumption, waste generation, and water usage across all facilities.",
            "Cem designed a data visualisation dashboard that displayed the audit results in real time on screens installed in the main entrance hall.",
            "The initial audit revealed that the school was generating over two hundred kilograms of recyclable waste per week, most of which was going to landfill.",
            "They launched a comprehensive recycling programme with clearly labelled bins, student monitors, and weekly progress reports shared in assemblies.",
            "Mr. Toprak connected them with a local environmental organisation that provided expertise on composting, rainwater harvesting, and energy-efficient lighting.",
            "Within two months, the school had reduced its landfill waste by forty percent and its energy consumption by fifteen percent through simple behavioural changes.",
            "Ipek wrote a detailed proposal for a school garden that would serve both as an educational resource and a carbon offset initiative.",
            "The garden project received funding from the municipality, and students from all grade levels participated in the planning and planting phases.",
            "Cem presented their combined results at a youth environmental summit, where their school was recognised as a model for sustainable education practices.",
            "Ipek reflected that environmental protection was not about grand gestures but about systematic, data-driven action at every level of community life."
        ]
    }
}

READING_BANK = {
    9: {
        1: [
            {
                "title": "Navigating the Transition to High School",
                "text": "The transition from middle school to high school represents one of the most significant academic and social shifts in a young person's educational journey. Research conducted by educational psychologists consistently demonstrates that the first semester of ninth grade is a critical period that can determine a student's long-term academic trajectory. Students who establish effective study habits, build supportive peer networks, and develop positive relationships with their teachers during this initial phase are statistically more likely to maintain higher grade point averages throughout their entire secondary education. One of the primary challenges facing new high school students is the dramatic increase in academic expectations. Unlike middle school, where teachers often provide considerable scaffolding and repeated reminders about assignments, high school educators generally expect students to manage their own learning independently. This shift requires the development of sophisticated organisational skills, including effective time management, strategic note-taking, and the ability to prioritise competing demands. Furthermore, the social landscape of high school is considerably more complex than that of earlier educational stages. Students must navigate new social hierarchies, develop their individual identities, and learn to balance academic responsibilities with extracurricular involvement and personal interests. Schools that implement structured orientation programmes, peer mentoring systems, and regular academic counselling sessions report significantly higher rates of student satisfaction and retention during this transitional period.",
                "questions": [
                    {"question": "According to the passage, what factor most influences long-term academic performance in high school?", "options": ["Natural intelligence levels", "The habits and connections formed in the first semester", "The quality of middle school preparation", "Parental involvement in schoolwork"], "answer": 1},
                    {"question": "What does the passage identify as a key difference between middle and high school teaching approaches?", "options": ["High school has fewer subjects", "Middle school teachers are less qualified", "High school expects greater student independence", "High school has more homework"], "answer": 2},
                    {"question": "The word 'scaffolding' in the context of this passage most likely means:", "options": ["Physical structures in classrooms", "Structured support to aid learning", "Construction of new buildings", "Examination preparation materials"], "answer": 1}
                ]
            }
        ],
        2: [
            {
                "title": "The Psychology of Personality Development in Adolescence",
                "text": "Adolescence is widely recognised by developmental psychologists as the most dynamic period of personality formation in the human lifespan. During this phase, which typically spans from ages twelve to eighteen, individuals undergo profound cognitive, emotional, and social changes that fundamentally shape who they will become as adults. Erik Erikson's influential theory of psychosocial development identifies the central task of adolescence as the resolution of the identity versus role confusion crisis. According to Erikson, teenagers must actively explore different values, beliefs, and social roles before they can establish a coherent and stable sense of self. This exploration process, though sometimes turbulent, is essential for healthy psychological development. Contemporary research has expanded upon Erikson's framework by examining how cultural context, socioeconomic factors, and digital environments influence identity formation. Studies show that adolescents who are encouraged to explore their interests, question assumptions, and express their individuality within a supportive environment tend to develop stronger self-esteem and more resilient psychological profiles. Conversely, those who experience excessive pressure to conform to rigid expectations may struggle with identity development and exhibit higher rates of anxiety and depression. The concept of multiple intelligences, proposed by Howard Gardner, has further enriched our understanding of personality by demonstrating that individuals possess distinct cognitive strengths that shape their interactions with the world. Recognising and nurturing these diverse intelligences during adolescence can significantly enhance both academic engagement and personal well-being, creating a foundation for lifelong fulfilment and meaningful contribution to society.",
                "questions": [
                    {"question": "According to Erikson's theory, what is the primary psychological task of adolescence?", "options": ["Achieving academic excellence", "Resolving the identity versus role confusion crisis", "Developing physical strength", "Establishing financial independence"], "answer": 1},
                    {"question": "What does contemporary research suggest about adolescents who face excessive pressure to conform?", "options": ["They develop stronger identities", "They perform better academically", "They may experience higher anxiety and depression", "They become more socially skilled"], "answer": 2},
                    {"question": "Howard Gardner's concept of multiple intelligences is mentioned to illustrate that:", "options": ["Some people are naturally smarter than others", "Intelligence cannot be measured accurately", "People have different cognitive strengths that affect their personalities", "Academic grades are the only measure of intelligence"], "answer": 2}
                ]
            }
        ],
        3: [
            {
                "title": "The Evolution of Digital Communication and Its Impact on Society",
                "text": "The landscape of human communication has undergone a revolutionary transformation over the past two decades, fundamentally altering how individuals interact, access information, and participate in public discourse. The proliferation of smartphones, social media platforms, and instant messaging applications has created an interconnected global community where information travels at unprecedented speed and scale. This digital revolution has democratised access to knowledge and given voice to communities that were previously marginalised in traditional media structures. However, these advances have also introduced significant challenges that society is still learning to navigate effectively. The phenomenon of information overload, where individuals are exposed to more data than they can meaningfully process, has been linked to increased cognitive fatigue, reduced attention spans, and difficulty distinguishing between reliable and unreliable sources. The rise of algorithmic content curation, where platforms use artificial intelligence to determine what users see, has created so-called filter bubbles that can reinforce existing biases and limit exposure to diverse perspectives. Furthermore, the boundaries between personal and public life have become increasingly blurred, raising complex questions about privacy, consent, and digital identity. Cybersecurity experts warn that the average teenager's digital footprint contains sufficient personal information to pose significant risks if accessed by malicious actors. Educational institutions have responded by incorporating digital literacy into their curricula, teaching students to evaluate sources critically, protect their personal data, and engage in online discourse responsibly. The challenge for the current generation is to harness the extraordinary potential of digital communication while developing the critical thinking skills necessary to mitigate its risks.",
                "questions": [
                    {"question": "What does the passage identify as a positive outcome of the digital revolution?", "options": ["Reduced need for education", "Democratised access to knowledge for marginalised communities", "Elimination of all communication barriers", "Guaranteed accuracy of online information"], "answer": 1},
                    {"question": "According to the passage, what are 'filter bubbles'?", "options": ["Physical barriers to internet access", "Environments where algorithms limit exposure to diverse views", "Special email filtering systems", "Government censorship programmes"], "answer": 1},
                    {"question": "The passage suggests that educational institutions are addressing digital challenges by:", "options": ["Banning technology in schools", "Ignoring the issue entirely", "Teaching digital literacy and critical evaluation skills", "Replacing teachers with artificial intelligence"], "answer": 2}
                ]
            }
        ],
        4: [
            {
                "title": "Understanding English Tenses: A Systematic Approach",
                "text": "The English tense system, comprising twelve distinct forms organised across past, present, and future time frames, represents one of the most sophisticated temporal expression systems among world languages. Unlike many languages that rely primarily on verb inflection to indicate time, English employs a combination of auxiliary verbs, participle forms, and contextual markers to convey precise temporal relationships. This complexity, while initially challenging for learners, ultimately provides writers and speakers with remarkable precision in expressing when events occur, how long they last, and how they relate to other events in time. The distinction between simple, continuous, perfect, and perfect continuous aspects allows English users to communicate subtle differences in meaning that would require lengthy explanations in less aspectually rich languages. For example, the difference between 'I have lived here for five years' and 'I have been living here for five years' conveys distinct information about the speaker's perspective on the permanence and ongoing nature of the situation. Similarly, the contrast between 'When she arrived, he left' and 'When she arrived, he had left' communicates fundamentally different temporal sequences using minimal linguistic resources. Academic writing places particular demands on tense usage, requiring writers to navigate between reporting past research findings, stating present facts, and making future predictions within a single paragraph. Mastering these transitions is essential for producing coherent, sophisticated academic prose. Research in applied linguistics has demonstrated that explicit instruction in tense semantics, combined with extensive contextualised practice, produces significantly better outcomes than traditional rule-memorisation approaches. Students who understand the conceptual logic underlying each tense form are better equipped to make appropriate choices in novel communicative situations.",
                "questions": [
                    {"question": "According to the passage, what makes the English tense system distinctive?", "options": ["It has fewer tenses than other languages", "It uses auxiliary verbs, participles, and context markers together", "It relies solely on verb inflection", "It cannot express future events"], "answer": 1},
                    {"question": "The examples comparing 'I have lived' and 'I have been living' illustrate:", "options": ["That the two forms are interchangeable", "Subtle differences in perspective on permanence and continuity", "Common grammatical errors", "Regional dialect variations"], "answer": 1},
                    {"question": "What approach to learning tenses does the passage recommend?", "options": ["Memorising rules without context", "Avoiding complex tenses entirely", "Understanding conceptual logic with contextualised practice", "Learning only the most common three tenses"], "answer": 2}
                ]
            }
        ],
        5: [
            {
                "title": "The Universal Power of World Literature",
                "text": "World literature, a concept first articulated by Johann Wolfgang von Goethe in the early nineteenth century, refers to the circulation and reception of literary works beyond their national boundaries, creating a shared reservoir of human experience and artistic expression. Goethe envisioned a future in which readers would engage with texts from diverse cultures, recognising both the universal themes that connect all human beings and the particular cultural perspectives that distinguish different societies. This vision has become increasingly relevant in our globalised era, where translated works from every continent are readily accessible to readers worldwide. The study of world literature encourages readers to develop cultural empathy by experiencing the world through perspectives radically different from their own. When a Turkish reader engages with a Japanese novel, an African poem, or a South American short story, they encounter different ways of understanding love, justice, suffering, and hope that challenge and enrich their own worldview. Literary scholars argue that this capacity for empathetic imagination is not merely an aesthetic pleasure but a cognitive skill with significant social implications. Research in psychology has demonstrated that regular readers of literary fiction score higher on measures of empathy, social perception, and emotional intelligence compared to non-readers. Furthermore, world literature provides invaluable insights into historical and contemporary social conditions, offering perspectives that are often absent from official historical narratives. Novels, poems, and plays frequently give voice to the experiences of ordinary individuals and marginalised communities, preserving stories that might otherwise be lost. In an era of increasing cultural polarisation, the study of world literature serves as a powerful antidote, reminding us of our shared humanity while celebrating the rich diversity of human expression.",
                "questions": [
                    {"question": "Who first articulated the concept of world literature?", "options": ["William Shakespeare", "Johann Wolfgang von Goethe", "Leo Tolstoy", "Orhan Pamuk"], "answer": 1},
                    {"question": "According to the passage, what cognitive benefit does reading literary fiction provide?", "options": ["Improved mathematical ability", "Higher empathy and social perception scores", "Better physical health", "Increased technological skills"], "answer": 1},
                    {"question": "The passage argues that world literature serves as an 'antidote' to:", "options": ["Poor writing skills", "Low literacy rates", "Cultural polarisation", "Economic inequality"], "answer": 2}
                ]
            }
        ],
        6: [
            {
                "title": "Understanding Global Inequality: Causes, Consequences, and Solutions",
                "text": "Global inequality, defined as the unequal distribution of resources, opportunities, and power among the world's nations and populations, remains one of the most pressing challenges of the twenty-first century. Despite remarkable progress in reducing extreme poverty over the past three decades, with the proportion of people living on less than two dollars per day falling from thirty-six percent to approximately ten percent, the gap between the world's richest and poorest communities continues to widen in many dimensions. The causes of global inequality are complex and interconnected, rooted in historical patterns of colonialism, unequal trade relationships, inadequate governance, and structural barriers to economic development. Climate change has emerged as a powerful amplifier of existing inequalities, as the communities least responsible for greenhouse gas emissions often suffer the most severe consequences of environmental degradation. Small island nations face existential threats from rising sea levels, while agricultural communities in sub-Saharan Africa experience increasingly unpredictable weather patterns that devastate crop yields and food security. International organisations such as the United Nations have established ambitious frameworks for addressing these challenges, most notably the Sustainable Development Goals, which set specific targets for reducing poverty, improving health and education, and promoting environmental sustainability by 2030. However, critics argue that achieving these goals requires fundamental reforms to international economic systems, including fairer trade agreements, debt relief for developing nations, and increased investment in renewable energy infrastructure. Young people around the world are increasingly engaged with these issues, recognising that the decisions made today about resource distribution, climate policy, and economic justice will determine the quality of life for generations to come.",
                "questions": [
                    {"question": "According to the passage, what has happened to extreme poverty rates over the past three decades?", "options": ["They have remained unchanged", "They have increased dramatically", "They have fallen from approximately 36% to 10%", "They have been completely eliminated"], "answer": 2},
                    {"question": "How does the passage describe the relationship between climate change and inequality?", "options": ["Climate change affects all countries equally", "Climate change reduces inequality", "Those least responsible for emissions suffer the most", "Climate change only affects wealthy nations"], "answer": 2},
                    {"question": "What do critics say is needed to achieve the Sustainable Development Goals?", "options": ["More charitable donations", "Fundamental reforms to international economic systems", "Less international cooperation", "Increased military spending"], "answer": 1}
                ]
            }
        ],
        7: [
            {
                "title": "The Intersection of Science and Innovation in the Modern World",
                "text": "The relationship between scientific discovery and technological innovation has never been more dynamic or consequential than it is in the current era. Breakthroughs in fields such as artificial intelligence, biotechnology, quantum computing, and materials science are transforming virtually every aspect of human life, from healthcare and agriculture to transportation and communication. The pace of innovation has accelerated dramatically, with the time between a scientific discovery and its practical application shrinking from decades to years, and in some cases, months. Artificial intelligence, perhaps the most transformative technology of our era, has evolved from a theoretical concept to a practical tool that influences daily decisions in medicine, finance, education, and governance. Machine learning algorithms can now diagnose certain medical conditions with accuracy comparable to experienced physicians, while natural language processing systems enable real-time translation across hundreds of languages. However, these advances raise profound ethical questions about algorithmic bias, employment displacement, and the appropriate boundaries of machine decision-making in contexts that affect human lives. Biotechnology represents another frontier of innovation with enormous potential and significant ethical complexity. Gene editing technologies such as CRISPR-Cas9 offer the possibility of eliminating hereditary diseases, enhancing crop resilience, and developing novel therapeutic approaches. Yet the ability to modify the fundamental building blocks of life demands rigorous ethical oversight and public deliberation about acceptable applications. Scientists and policymakers increasingly recognise that technological innovation without ethical reflection and inclusive governance can exacerbate existing inequalities rather than reduce them. The challenge for the current generation of scientists, engineers, and citizens is to ensure that innovation serves the common good while respecting fundamental human values and environmental sustainability.",
                "questions": [
                    {"question": "What trend does the passage identify regarding the pace of innovation?", "options": ["Innovation has slowed considerably", "The gap between discovery and application is widening", "The time from discovery to application is shrinking rapidly", "Innovation is limited to wealthy countries"], "answer": 2},
                    {"question": "What ethical concern about AI does the passage mention?", "options": ["AI is too expensive to develop", "AI cannot perform useful tasks", "Algorithmic bias and employment displacement", "AI will never match human intelligence"], "answer": 2},
                    {"question": "The passage argues that technological innovation without ethical reflection can:", "options": ["Solve all global problems", "Exacerbate existing inequalities", "Eliminate the need for governance", "Replace scientific research entirely"], "answer": 1}
                ]
            }
        ],
        8: [
            {
                "title": "Art as a Mirror and Window: Understanding Creative Expression",
                "text": "Throughout human history, artistic expression has served dual functions that the literary scholar Rudine Sims Bishop eloquently described as mirrors and windows. As mirrors, works of art reflect the experiences, values, and identities of their creators and audiences, affirming cultural heritage and personal identity. As windows, they provide glimpses into unfamiliar worlds, fostering understanding and empathy across cultural, temporal, and geographical boundaries. This dual capacity makes art an indispensable element of human civilisation, serving purposes that extend far beyond mere aesthetic pleasure or entertainment. Contemporary art criticism increasingly recognises the interconnectedness of different artistic disciplines, challenging traditional boundaries between visual arts, music, literature, dance, and digital media. Interdisciplinary artists who work across multiple media forms often discover that each discipline offers unique expressive possibilities that can enhance and transform the others. A painter who incorporates sound elements into an installation, for example, creates an immersive experience that engages multiple sensory channels simultaneously, producing emotional responses that neither visual nor auditory art could achieve independently. The democratisation of artistic tools through digital technology has expanded creative participation to an unprecedented degree. Software applications for music production, graphic design, video editing, and three-dimensional modelling have made sophisticated artistic tools accessible to anyone with a computer or smartphone. This democratisation has generated vibrant online communities where artists from diverse backgrounds share work, exchange techniques, and collaborate across geographical boundaries. However, this abundance also presents challenges, as the sheer volume of creative content can make it difficult for individual artists to find audiences and sustain professional careers. Despite these challenges, the fundamental human need for creative expression remains as powerful as ever, and the arts continue to play an essential role in helping individuals and communities make sense of their experiences.",
                "questions": [
                    {"question": "What does the 'mirrors and windows' metaphor describe in relation to art?", "options": ["Architectural design principles", "Art's ability to reflect familiar experiences and reveal unfamiliar ones", "Techniques for painting glass surfaces", "The difference between indoor and outdoor art"], "answer": 1},
                    {"question": "According to the passage, what advantage do interdisciplinary artists gain?", "options": ["Higher income from multiple sources", "Expressive possibilities that transform and enhance each discipline", "Easier access to art galleries", "Shorter production times for artworks"], "answer": 1},
                    {"question": "What challenge has the democratisation of artistic tools created?", "options": ["Lower quality artwork overall", "Difficulty for individual artists to find audiences", "Reduced interest in traditional art forms", "Excessive government regulation of art"], "answer": 1}
                ]
            }
        ],
        9: [
            {
                "title": "Adolescent Health and Well-being: A Comprehensive Perspective",
                "text": "The health and well-being of adolescents has emerged as a priority concern for public health professionals, educators, and policymakers worldwide. The World Health Organisation defines adolescent health broadly, encompassing not only the absence of disease but also physical fitness, mental resilience, emotional stability, and positive social functioning. This holistic perspective recognises that the health behaviours established during adolescence frequently persist into adulthood, making this developmental period a critical window for preventive intervention. Research consistently identifies several interconnected factors that significantly influence adolescent well-being. Adequate sleep, defined as eight to ten hours per night for teenagers, is essential for cognitive function, emotional regulation, and physical growth. However, studies reveal that fewer than thirty percent of high school students consistently achieve the recommended amount of sleep, with electronic device usage and early school start times identified as primary contributing factors. Nutrition represents another critical dimension, with evidence suggesting that dietary patterns during adolescence directly affect academic performance, mood stability, and long-term health outcomes. The prevalence of processed food consumption and irregular meal patterns among teenagers has been associated with increased rates of obesity, type two diabetes, and cardiovascular risk factors. Physical activity, recommended at sixty minutes of moderate-to-vigorous exercise daily, provides benefits that extend beyond physical fitness to include improved concentration, reduced anxiety, and enhanced self-esteem. Perhaps most significantly, mental health awareness among adolescents has increased dramatically in recent years, reducing stigma and encouraging help-seeking behaviour. Schools that implement comprehensive wellness programmes addressing nutrition, sleep, exercise, and mental health report measurable improvements in both student well-being and academic achievement.",
                "questions": [
                    {"question": "How does the WHO define adolescent health according to the passage?", "options": ["Simply as the absence of disease", "As physical fitness only", "Holistically, including physical, mental, emotional, and social dimensions", "As academic performance"], "answer": 2},
                    {"question": "What percentage of high school students consistently get enough sleep?", "options": ["Over seventy percent", "Approximately fifty percent", "Fewer than thirty percent", "Nearly all students"], "answer": 2},
                    {"question": "What outcome do schools with comprehensive wellness programmes report?", "options": ["Lower attendance rates", "Improvements in both well-being and academic achievement", "Increased student complaints", "No measurable differences"], "answer": 1}
                ]
            }
        ],
        10: [
            {
                "title": "Environmental Sustainability: Science, Policy, and Individual Action",
                "text": "Environmental sustainability, broadly defined as meeting present needs without compromising the ability of future generations to meet their own needs, has become the defining challenge of the twenty-first century. The scientific consensus, supported by extensive data from climate monitoring stations, satellite observations, and computational models, confirms that human activities are driving unprecedented changes in Earth's climate, biodiversity, and ecosystem functioning. Global average temperatures have risen by approximately 1.1 degrees Celsius above pre-industrial levels, with the rate of warming accelerating measurably over the past four decades. The consequences of environmental degradation are already visible across the globe. Rising sea levels threaten coastal communities, extreme weather events are increasing in both frequency and intensity, and biodiversity loss is occurring at rates estimated to be one hundred to one thousand times higher than natural background extinction levels. These environmental changes disproportionately affect vulnerable populations, including low-income communities, indigenous peoples, and small island developing states, creating what environmental justice scholars describe as climate inequality. International efforts to address these challenges have produced significant policy frameworks, including the Paris Agreement, which established the goal of limiting global warming to 1.5 degrees Celsius above pre-industrial levels. However, current national commitments remain insufficient to achieve this target, requiring substantially more ambitious action across all sectors of the economy. Individual behaviour change, while insufficient on its own, plays an important role within broader systemic transformation. Research demonstrates that sustainable consumption choices, energy conservation practices, and civic engagement in environmental advocacy collectively contribute to the cultural and political conditions necessary for large-scale policy change. Education is increasingly recognised as a critical enabler of sustainability transitions, equipping young people with the knowledge, skills, and values needed to address environmental challenges effectively.",
                "questions": [
                    {"question": "By how much have global average temperatures risen above pre-industrial levels?", "options": ["Approximately 0.5 degrees Celsius", "Approximately 1.1 degrees Celsius", "Approximately 2.0 degrees Celsius", "Approximately 3.5 degrees Celsius"], "answer": 1},
                    {"question": "What does the passage say about current biodiversity loss rates?", "options": ["They are within normal historical ranges", "They are decreasing due to conservation efforts", "They are 100 to 1,000 times higher than natural rates", "They only affect marine ecosystems"], "answer": 2},
                    {"question": "According to the passage, what role does individual behaviour change play?", "options": ["It is completely irrelevant", "It is sufficient to solve all environmental problems", "It contributes to conditions for large-scale policy change", "It is more important than government action"], "answer": 2}
                ]
            }
        ]
    }
}

GRAMMAR_BANK = {
    9: {
        1: [
            {
                "topic": "Present Simple vs Present Continuous",
                "explanation": "The present simple describes habits, routines, general truths, and permanent states (e.g., 'School starts at 8:30 every day'). The present continuous describes actions happening right now or temporary situations (e.g., 'I am studying for my first exam this week'). Stative verbs like 'know', 'believe', 'belong' are typically not used in the continuous form.",
                "examples": [
                    "Emre attends five classes every day. (routine)",
                    "He is adjusting to his new timetable this month. (temporary situation)",
                    "The library opens at 8 a.m. and closes at 6 p.m. (general fact)",
                    "Selin is mentoring three freshmen this semester. (current ongoing activity)"
                ],
                "exercises": [
                    {"question": "Every morning, Emre ___ (wake) up at 6:30 to prepare for school.", "answer": "wakes"},
                    {"question": "This week, the students ___ (take) placement tests in all subjects.", "answer": "are taking"},
                    {"question": "The school ___ (have) over 1,200 students enrolled this year.", "answer": "has"},
                    {"question": "Right now, Mr. Demir ___ (give) a speech in the assembly hall.", "answer": "is giving"}
                ]
            },
            {
                "topic": "Past Simple vs Past Continuous",
                "explanation": "The past simple describes completed actions at a specific time in the past (e.g., 'Emre arrived at school at 7:45'). The past continuous describes actions that were in progress at a specific moment or when another action interrupted them (e.g., 'While he was walking through the corridor, he met Selin').",
                "examples": [
                    "Emre registered for two clubs on his first day. (completed action)",
                    "While students were queuing for lunch, the fire alarm rang. (interrupted action)",
                    "Selin was explaining the school rules when Emre asked a question. (background + interruption)",
                    "It was raining heavily when the school bus arrived. (simultaneous background)"
                ],
                "exercises": [
                    {"question": "While Emre ___ (explore) the campus, he discovered the art studio.", "answer": "was exploring"},
                    {"question": "The bell ___ (ring) just as the teacher finished the lesson.", "answer": "rang"},
                    {"question": "Students ___ (chat) in the corridor when the principal appeared.", "answer": "were chatting"},
                    {"question": "Selin ___ (introduce) Emre to five different club leaders yesterday.", "answer": "introduced"}
                ]
            }
        ],
        2: [
            {
                "topic": "Modals of Deduction (must, might, could, can't)",
                "explanation": "Modal verbs are used to express how certain we are about something. 'Must' indicates strong logical deduction (near certainty). 'Might/could' express possibility (less certain). 'Can't' expresses strong negative deduction (near impossibility). For past deductions, we use modal + have + past participle.",
                "examples": [
                    "Defne must be very creative - her artwork is exceptional. (strong deduction)",
                    "Can might be nervous about the presentation. (possibility)",
                    "That can't be the correct answer - it contradicts the data. (strong negative deduction)",
                    "She must have spent hours preparing that portfolio. (past deduction)"
                ],
                "exercises": [
                    {"question": "Defne always scores highly on creative tasks. She ___ (must/be) very talented.", "answer": "must be"},
                    {"question": "I'm not sure where Can is. He ___ (might/study) in the library.", "answer": "might be studying"},
                    {"question": "That ___ (can't/be) Ms. Yilmaz - she's on leave today.", "answer": "can't be"},
                    {"question": "The project is outstanding. They ___ (must/work) on it for weeks.", "answer": "must have worked"}
                ]
            },
            {
                "topic": "Noun Clauses (that, what, whether/if)",
                "explanation": "Noun clauses function as subjects, objects, or complements in sentences. They begin with 'that', 'what', 'where', 'how', 'whether/if', or other question words. The word order within the noun clause is subject + verb (not inverted as in questions).",
                "examples": [
                    "What surprised Defne was how positive the feedback was. (subject)",
                    "Ms. Yilmaz believes that every personality type has unique strengths. (object)",
                    "The question is whether introverts can be effective leaders. (complement)",
                    "Nobody knows how many students took the personality quiz. (object)"
                ],
                "exercises": [
                    {"question": "___ she said during the presentation impressed everyone. (What/That)", "answer": "What"},
                    {"question": "It is widely accepted ___ personality develops throughout adolescence. (what/that)", "answer": "that"},
                    {"question": "Can asked ___ Defne would be comfortable presenting first. (that/whether)", "answer": "whether"},
                    {"question": "The research shows ___ diverse teams perform better than homogeneous ones. (what/that)", "answer": "that"}
                ]
            }
        ],
        3: [
            {
                "topic": "Passive Voice (all tenses)",
                "explanation": "The passive voice is formed with 'be' + past participle. It is used when the action is more important than the doer, the doer is unknown, or in formal/academic writing. The passive can be formed in all tenses: 'is written' (present simple), 'is being written' (present continuous), 'was written' (past simple), 'has been written' (present perfect), etc.",
                "examples": [
                    "The school newspaper is published every Friday. (present simple passive)",
                    "A new website is being developed by the IT team. (present continuous passive)",
                    "The article was written by Zeynep last weekend. (past simple passive)",
                    "The campaign has been launched successfully. (present perfect passive)",
                    "The server will be upgraded next month. (future simple passive)"
                ],
                "exercises": [
                    {"question": "The school's mobile app ___ (develop) by Berk last semester.", "answer": "was developed"},
                    {"question": "Currently, the website ___ (redesign) to improve user experience.", "answer": "is being redesigned"},
                    {"question": "Over 500 articles ___ (publish) on the school newspaper's website since 2023.", "answer": "have been published"},
                    {"question": "The new privacy policy ___ (announce) at next week's assembly.", "answer": "will be announced"}
                ]
            },
            {
                "topic": "Causatives (have/get something done)",
                "explanation": "Causative structures are used when we arrange for someone else to do something for us. 'Have something done' (have + object + past participle) is the standard form. 'Get something done' is slightly more informal. 'Have someone do something' and 'get someone to do something' specify who performs the action.",
                "examples": [
                    "Zeynep had the website redesigned by a professional developer. (have + object + pp)",
                    "She got the articles proofread before publication. (get + object + pp)",
                    "Mr. Aksoy had Berk fix the server issue. (have + person + base form)",
                    "Zeynep got her classmates to contribute articles. (get + person + to + base form)"
                ],
                "exercises": [
                    {"question": "The school ___ (have/the server/upgrade) during the summer break.", "answer": "had the server upgraded"},
                    {"question": "Berk ___ (get/the app/test) by fifty students before the official launch.", "answer": "got the app tested"},
                    {"question": "Ms. Celik ___ (have/the students/research) digital citizenship guidelines.", "answer": "had the students research"},
                    {"question": "They ___ (get/a designer/create) the infographic for the campaign.", "answer": "got a designer to create"}
                ]
            }
        ],
        4: [
            {
                "topic": "All Twelve Tenses - Comprehensive Review",
                "explanation": "English has twelve tenses formed by combining four aspects (simple, continuous, perfect, perfect continuous) across three time frames (past, present, future). Each tense conveys specific temporal information. Mastering all twelve allows precise expression of when events happen and how they relate to each other.",
                "examples": [
                    "Present Simple: Water boils at 100 degrees Celsius.",
                    "Present Continuous: Arda is learning Turkish this year.",
                    "Present Perfect: Elif has studied English grammar for six years.",
                    "Present Perfect Continuous: They have been practising tenses all morning.",
                    "Past Simple: Arda arrived in Turkey two weeks ago.",
                    "Past Continuous: While he was reading, the phone rang.",
                    "Past Perfect: By the time Elif arrived, Arda had already finished the exercise.",
                    "Past Perfect Continuous: He had been struggling with tenses before Elif helped him.",
                    "Future Simple: Ms. Kaya will assign a new essay next week.",
                    "Future Continuous: This time tomorrow, they will be taking the grammar test.",
                    "Future Perfect: By June, Arda will have completed the entire course.",
                    "Future Perfect Continuous: By the end of term, he will have been studying here for six months."
                ],
                "exercises": [
                    {"question": "Arda ___ (study) English since he was seven years old.", "answer": "has been studying"},
                    {"question": "By the time Elif arrived, Arda ___ (complete) three exercises already.", "answer": "had completed"},
                    {"question": "This time next week, we ___ (sit) our final grammar examination.", "answer": "will be sitting"},
                    {"question": "By December, Arda ___ (live) in Turkey for exactly one year.", "answer": "will have been living"}
                ]
            },
            {
                "topic": "Conditionals (Zero, First, Second, Third)",
                "explanation": "Zero conditional: If + present simple, present simple (general truths). First conditional: If + present simple, will + base form (real/likely future). Second conditional: If + past simple, would + base form (unreal/hypothetical present). Third conditional: If + past perfect, would have + past participle (unreal past). Mixed conditionals combine second and third for present results of past actions or vice versa.",
                "examples": [
                    "Zero: If you heat ice, it melts.",
                    "First: If Arda practises every day, he will master all twelve tenses.",
                    "Second: If I spoke five languages, I would work as a translator.",
                    "Third: If Elif hadn't helped him, Arda wouldn't have passed the test.",
                    "Mixed: If Arda had studied Turkish earlier, he would speak it fluently now."
                ],
                "exercises": [
                    {"question": "If you ___ (mix) blue and yellow, you get green. (zero)", "answer": "mix"},
                    {"question": "If Arda ___ (finish) his homework early, he will join us for dinner. (first)", "answer": "finishes"},
                    {"question": "If I ___ (be) fluent in Japanese, I would read manga in the original language. (second)", "answer": "were"},
                    {"question": "If they ___ (start) the project earlier, they would have finished on time. (third)", "answer": "had started"}
                ]
            }
        ],
        5: [
            {
                "topic": "Wish / If Only (present, past, future)",
                "explanation": "We use 'wish/if only + past simple' for present wishes (things we want to be different now). 'Wish/if only + past perfect' for past regrets (things we wish had been different). 'Wish/if only + would + base form' for future wishes or complaints about habits. 'Were' is used instead of 'was' in formal usage after wish.",
                "examples": [
                    "I wish I had more time to read. (present wish - I don't have enough time)",
                    "If only Kerem had discovered literature earlier. (past regret)",
                    "Yasemin wishes more students would join the book club. (future wish/complaint)",
                    "If only the library were open on weekends. (present wish, formal)"
                ],
                "exercises": [
                    {"question": "Kerem wishes he ___ (start) reading for pleasure years ago.", "answer": "had started"},
                    {"question": "If only the school library ___ (have) a larger collection of world literature.", "answer": "had"},
                    {"question": "Yasemin wishes her classmates ___ (read) more diverse authors.", "answer": "would read"},
                    {"question": "I wish I ___ (can) read novels in their original languages.", "answer": "could"}
                ]
            },
            {
                "topic": "Cleft Sentences (It is/was... that/who)",
                "explanation": "Cleft sentences are used for emphasis, splitting a simple sentence into two clauses. 'It is/was + focused element + that/who + rest of sentence' highlights specific information. 'What' clefts use 'What + subject + verb + is/was + focused element'. These structures are common in academic writing and formal discourse.",
                "examples": [
                    "It was Goethe who first proposed the concept of world literature.",
                    "It is through reading that we develop cultural empathy.",
                    "What Kerem enjoyed most was the discussion about symbolism.",
                    "What makes great literature timeless is its exploration of universal themes."
                ],
                "exercises": [
                    {"question": "It ___ Yasemin who organised the international book club.", "answer": "was"},
                    {"question": "What ___ (impress) Mr. Polat most was Kerem's insightful interpretation.", "answer": "impressed"},
                    {"question": "It is through literature ___ we gain insight into different cultures.", "answer": "that"},
                    {"question": "What the students ___ (find) most valuable was comparing texts from different countries.", "answer": "found"}
                ]
            }
        ],
        6: [
            {
                "topic": "Adverbial Clauses (concession, reason, result, purpose)",
                "explanation": "Adverbial clauses modify verbs, adjectives, or adverbs and show relationships such as concession (although, even though, despite the fact that), reason (because, since, as), result (so...that, such...that), and purpose (so that, in order that). They add complexity and precision to academic writing.",
                "examples": [
                    "Although wealthy nations have resources, they often fail to act on global issues. (concession)",
                    "Since climate change affects everyone, international cooperation is essential. (reason)",
                    "The evidence was so compelling that the judges changed their position. (result)",
                    "Deniz researched extensively so that her arguments would be well-supported. (purpose)"
                ],
                "exercises": [
                    {"question": "___ the opposing team presented strong arguments, Deniz's team won the debate.", "answer": "Although"},
                    {"question": "The inequality is ___ severe that immediate action is required.", "answer": "so"},
                    {"question": "Mert prepared counterarguments ___ he could respond to any challenge.", "answer": "so that"},
                    {"question": "___ global poverty rates have fallen, inequality continues to widen.", "answer": "Even though"}
                ]
            },
            {
                "topic": "Inversion for Emphasis",
                "explanation": "Inversion (placing the auxiliary or verb before the subject) is used for emphasis in formal English. Common patterns include: 'Never have I...', 'Not only...but also...', 'Hardly had...when...', 'Only by...can we...', 'No sooner...than...', 'Under no circumstances should...'. This structure is frequent in academic essays and formal speeches.",
                "examples": [
                    "Never before has the gap between rich and poor been so wide.",
                    "Not only did Deniz win the debate, but she also inspired her peers.",
                    "Hardly had the debate ended when the audience began applauding.",
                    "Only through international cooperation can we address global inequality."
                ],
                "exercises": [
                    {"question": "Never ___ I seen such a well-prepared debate team.", "answer": "have"},
                    {"question": "Not only ___ the team win the tournament, but they also received a special commendation.", "answer": "did"},
                    {"question": "Only by working together ___ nations solve the climate crisis.", "answer": "can"},
                    {"question": "Hardly ___ the speaker finished when questions began pouring in.", "answer": "had"}
                ]
            }
        ],
        7: [
            {
                "topic": "Reported Speech (advanced - modals, questions, commands)",
                "explanation": "When reporting speech, tenses typically shift back (backshift). Modals change: 'can' becomes 'could', 'will' becomes 'would', 'may' becomes 'might'. 'Must' can become 'had to'. Reported questions use statement word order (no inversion). Reported commands use 'told/asked/ordered + object + to + base form'.",
                "examples": [
                    "Dr. Ozkan said that scientific research must be reproducible. (modal report)",
                    "Tugce asked whether the filtration system could remove heavy metals. (reported question)",
                    "The teacher told the students to document every step of their experiment. (reported command)",
                    "Onur explained that he had been working on the sensor array for three weeks. (backshift)"
                ],
                "exercises": [
                    {"question": "Tugce said, 'I will present our findings next week.' -> Tugce said that she ___ present their findings the following week.", "answer": "would"},
                    {"question": "Dr. Ozkan asked, 'Have you tested the water samples?' -> Dr. Ozkan asked whether they ___ the water samples.", "answer": "had tested"},
                    {"question": "The judge said, 'You must submit your project by Friday.' -> The judge said that they ___ submit their project by Friday.", "answer": "had to"},
                    {"question": "Onur asked, 'How does the sensor measure pH levels?' -> Onur asked how the sensor ___ pH levels.", "answer": "measured"}
                ]
            },
            {
                "topic": "Relative Clauses (defining, non-defining, reduced)",
                "explanation": "Defining relative clauses identify which person/thing we mean (no commas). Non-defining add extra information (with commas). Relative pronouns: who/that (people), which/that (things), whose (possession), where (place), when (time). Reduced relative clauses omit the pronoun and use participles: 'The student studying...' (active) or 'The project designed by...' (passive).",
                "examples": [
                    "The filtration system that Tugce designed removed 95% of contaminants. (defining)",
                    "Dr. Ozkan, who supervises the science club, encouraged their research. (non-defining)",
                    "The laboratory where they conducted experiments had modern equipment. (defining, place)",
                    "The sensors measuring water quality were built by Onur. (reduced active)"
                ],
                "exercises": [
                    {"question": "The scientist ___ research inspired Tugce received the Nobel Prize.", "answer": "whose"},
                    {"question": "CRISPR-Cas9, ___ was discovered in 2012, has revolutionised genetics.", "answer": "which"},
                    {"question": "Students ___ (participate) in the science fair must register by March. (reduced)", "answer": "participating"},
                    {"question": "The award ___ (give) to the best project was announced at the ceremony. (reduced passive)", "answer": "given"}
                ]
            }
        ],
        8: [
            {
                "topic": "Participle Clauses (present, past, perfect)",
                "explanation": "Participle clauses replace full adverbial or relative clauses for more concise, sophisticated sentences. Present participle (-ing) for active/simultaneous actions: 'Painting the canvas, Hazal felt calm.' Past participle (-ed/irregular) for passive meaning: 'Inspired by Turkish calligraphy, she created a new series.' Perfect participle (having + pp) for completed earlier actions: 'Having finished the composition, Burak reviewed it.'",
                "examples": [
                    "Working with mixed media, Hazal discovered new textures and combinations. (simultaneous)",
                    "Fascinated by the exhibition, visitors stayed for hours. (reason, passive)",
                    "Having studied both traditional and digital art, she understood their differences. (completed action)",
                    "Not knowing what to expect, the audience was pleasantly surprised. (negative participle)"
                ],
                "exercises": [
                    {"question": "___ (complete) the installation, Hazal and Burak invited visitors to the opening.", "answer": "Having completed"},
                    {"question": "___ (inspire) by Turkish motifs, the artwork blended cultural heritage with modern design.", "answer": "Inspired"},
                    {"question": "___ (listen) to Burak's music, Hazal found new colour palettes for her paintings.", "answer": "Listening"},
                    {"question": "___ (not/experience) multimedia art before, many visitors were deeply moved.", "answer": "Not having experienced"}
                ]
            },
            {
                "topic": "Advanced Passive Structures (impersonal passive, passive with two objects)",
                "explanation": "Impersonal passive uses 'It is said/believed/known/reported + that clause' or 'Subject + is said/believed + to + infinitive'. These are common in academic writing. With verbs that take two objects (give, tell, show, offer), either object can become the subject of the passive sentence.",
                "examples": [
                    "It is widely believed that art enhances cognitive development.",
                    "Art is said to improve emotional intelligence and empathy.",
                    "It has been reported that the exhibition attracted over 500 visitors.",
                    "Hazal was given a scholarship. / A scholarship was given to Hazal. (two-object passive)"
                ],
                "exercises": [
                    {"question": "It ___ (believe) that exposure to art reduces stress levels significantly.", "answer": "is believed"},
                    {"question": "Creativity ___ (say) to be one of the most valuable skills in the 21st century.", "answer": "is said"},
                    {"question": "Burak ___ (offer) a place at the music academy last month.", "answer": "was offered"},
                    {"question": "It ___ (report) that interdisciplinary projects improve student engagement.", "answer": "has been reported"}
                ]
            }
        ],
        9: [
            {
                "topic": "Gerunds and Infinitives (advanced patterns)",
                "explanation": "Some verbs take gerund (-ing), some take infinitive (to + base form), and some take both with different meanings. 'Stop doing' (cease the action) vs 'stop to do' (pause in order to). 'Remember doing' (recall past action) vs 'remember to do' (not forget future action). Complex patterns include: 'too + adjective + to', 'adjective + enough + to', 'verb + object + infinitive'.",
                "examples": [
                    "Ceren suggested organising a wellness week. (verb + gerund)",
                    "Kaan decided to reduce his training intensity. (verb + infinitive)",
                    "She stopped eating junk food. (ceased the action) vs She stopped to eat lunch. (paused to eat)",
                    "Dr. Acar encouraged the students to practise relaxation techniques. (verb + object + infinitive)"
                ],
                "exercises": [
                    {"question": "Many students avoid ___ (discuss) their mental health concerns openly.", "answer": "discussing"},
                    {"question": "Dr. Acar recommended ___ (get) at least eight hours of sleep.", "answer": "getting"},
                    {"question": "Kaan will never forget ___ (collapse) during training last year. (past memory)", "answer": "collapsing"},
                    {"question": "The school agreed ___ (implement) weekly mindfulness sessions.", "answer": "to implement"}
                ]
            },
            {
                "topic": "Mixed Conditionals and Wish Structures (advanced)",
                "explanation": "Mixed conditionals combine elements from second and third conditionals. Type 1 mixed: If + past perfect, would + base form (past condition, present result). Type 2 mixed: If + past simple, would have + past participle (present condition, past result). Advanced wish patterns: 'wish + past perfect' for past regrets, 'wish + would' for future changes or complaints about present habits.",
                "examples": [
                    "If Kaan had rested properly last season, he would be healthier now. (past condition -> present result)",
                    "If Ceren weren't so dedicated, she wouldn't have organised the wellness week. (present condition -> past result)",
                    "I wish students would take their health more seriously. (complaint/future wish)",
                    "If only we had known about these techniques earlier, we would be less stressed now. (mixed)"
                ],
                "exercises": [
                    {"question": "If Kaan ___ (not/overtrain) last year, he would feel better now.", "answer": "hadn't overtrained"},
                    {"question": "If Ceren ___ (not/be) so passionate about health, she wouldn't have started the campaign.", "answer": "weren't"},
                    {"question": "I wish the school ___ (introduce) wellness programmes years ago.", "answer": "had introduced"},
                    {"question": "If we ___ (sleep) enough every night, we would have performed better on the exams.", "answer": "slept"}
                ]
            }
        ],
        10: [
            {
                "topic": "Hypothetical Structures (suppose, as if, it's time, would rather)",
                "explanation": "'Suppose/Supposing' + past simple for hypothetical situations. 'As if/as though' + past simple for unreal comparisons (present), or + past perfect (past). 'It's (high) time' + past simple for something that should happen now. 'Would rather' + past simple when the subject differs from the person we wish to act.",
                "examples": [
                    "Suppose we ran out of clean water tomorrow, what would we do?",
                    "Some people act as if climate change weren't real.",
                    "It's high time governments took stronger action on emissions.",
                    "I'd rather you didn't use single-use plastics."
                ],
                "exercises": [
                    {"question": "It's high time the school ___ (adopt) a zero-waste policy.", "answer": "adopted"},
                    {"question": "Suppose every household ___ (reduce) its energy use by 20%, the impact would be enormous.", "answer": "reduced"},
                    {"question": "Some corporations behave as if environmental regulations ___ (not/apply) to them.", "answer": "didn't apply"},
                    {"question": "I'd rather the government ___ (invest) more in renewable energy.", "answer": "invested"}
                ]
            },
            {
                "topic": "Cohesive Devices and Discourse Markers (academic writing)",
                "explanation": "Cohesive devices connect ideas within and between paragraphs. Addition: furthermore, moreover, in addition. Contrast: however, nevertheless, on the other hand. Cause/effect: consequently, therefore, as a result. Example: for instance, such as, namely. Sequence: firstly, subsequently, finally. Concession: admittedly, granted, albeit. These markers are essential for sophisticated academic writing.",
                "examples": [
                    "The data clearly shows rising temperatures. Furthermore, sea levels have increased significantly.",
                    "Recycling rates have improved. Nevertheless, landfill waste remains a serious problem.",
                    "Carbon emissions continued to rise. Consequently, the government introduced stricter regulations.",
                    "Several species are at risk, namely the polar bear, the coral reef ecosystem, and the monarch butterfly."
                ],
                "exercises": [
                    {"question": "The school reduced waste by 40%. ___, energy consumption dropped by 15%. (addition)", "answer": "Furthermore"},
                    {"question": "Individual action is important. ___, systemic change is equally necessary. (contrast/addition)", "answer": "However"},
                    {"question": "Temperatures have risen by 1.1 degrees. ___, extreme weather events have become more frequent. (result)", "answer": "Consequently"},
                    {"question": "___ the challenges are significant, there are reasons for optimism. (concession)", "answer": "Although"}
                ]
            }
        ]
    }
}

CULTURE_CORNER_BANK = {
    9: {
        1: [
            {
                "title": "Education Systems Around the World",
                "content": "Education systems vary dramatically across cultures, reflecting different values and priorities. In Finland, students begin formal education at age seven and have minimal homework, yet consistently rank among the world's top performers. Japanese schools emphasise group responsibility, with students cleaning their own classrooms daily. In Germany, students are tracked into different educational pathways at age ten. The British system uses a house system in many schools, fostering inter-group competition and community. South Korean students often attend 'hagwons' (private academies) after regular school hours. Despite these differences, all systems share the common goal of preparing young people for productive and fulfilling lives.",
                "discussion_questions": [
                    "Which education system's approach appeals to you most and why?",
                    "What aspects of the Turkish education system would you share with students from other countries?",
                    "Do you think there is one 'best' education system, or should systems be adapted to cultural contexts?"
                ]
            }
        ],
        2: [
            {
                "title": "Cultural Perspectives on Personality and Identity",
                "content": "Different cultures view personality and individual identity in remarkably different ways. Western societies tend to emphasise individualism, encouraging people to discover and express their unique qualities. In contrast, many East Asian cultures prioritise collective identity, where harmony with the group is valued above personal distinction. Indigenous Australian cultures understand identity through deep connection to land, ancestors, and community. In many African philosophical traditions, the concept of 'Ubuntu' ('I am because we are') defines identity through relationships with others. The Myers-Briggs personality framework, developed in America, reflects Western assumptions about individual differences. Understanding these varying perspectives enriches our appreciation of the complex relationship between culture and selfhood.",
                "discussion_questions": [
                    "How does Turkish culture balance individual identity with community belonging?",
                    "Do you think personality is more influenced by nature or culture?",
                    "How might the concept of Ubuntu change how we think about personal identity?"
                ]
            }
        ],
        3: [
            {
                "title": "Digital Communication Across Cultures",
                "content": "The way people communicate digitally varies significantly across cultures. In Japan, LINE is the dominant messaging platform, featuring elaborate stickers that convey nuanced emotional expressions. Brazilian WhatsApp culture is characterised by extensive voice messaging rather than text. Chinese WeChat functions as a complete digital ecosystem, integrating messaging, payments, shopping, and government services into a single application. In many Scandinavian countries, digital government services are so advanced that most citizens interact with bureaucracy entirely online. American social media culture tends to favour visual platforms like Instagram and TikTok, while Russian-speaking communities often prefer VKontakte. These differences reflect not only technological preferences but deeper cultural values around communication, privacy, and social interaction.",
                "discussion_questions": [
                    "What messaging platforms and social media are most popular in Turkey?",
                    "How do cultural values influence the way people communicate online?",
                    "Should governments regulate social media platforms? Why or why not?"
                ]
            }
        ],
        4: [
            {
                "title": "The Diversity of World Languages",
                "content": "The approximately seven thousand languages spoken worldwide represent an extraordinary diversity of human expression. Mandarin Chinese, with over a billion speakers, uses tonal distinctions that can change a word's meaning entirely. Arabic is written from right to left and has a rich tradition of calligraphy that blends language with visual art. Finnish has fifteen grammatical cases compared to English's essentially zero, allowing incredibly precise expression of spatial relationships. Turkish belongs to the Turkic language family, which stretches from Turkey to Central Asia and Siberia, and uses agglutination to build complex words from smaller morphemes. Pirahã, spoken by a small community in the Brazilian Amazon, has been controversially claimed to lack recursion, a feature once considered universal to all languages. Each language represents a unique way of perceiving and categorising reality.",
                "discussion_questions": [
                    "What features of the Turkish language do you think are unique or interesting?",
                    "Why is it important to preserve endangered languages?",
                    "How does learning a foreign language change the way you think?"
                ]
            }
        ],
        5: [
            {
                "title": "Literary Traditions Across Civilisations",
                "content": "Every civilisation has developed rich literary traditions that reflect its values, struggles, and aspirations. The Epic of Gilgamesh, from ancient Mesopotamia, is considered the world's oldest literary work, exploring themes of friendship, mortality, and the search for meaning that remain relevant today. Ancient Greek drama established conventions of tragedy and comedy that continue to influence theatre worldwide. Classical Arabic literature produced masterworks like One Thousand and One Nights, which introduced narrative framing techniques still used by modern authors. Japanese haiku distils profound observations into just seventeen syllables, demonstrating that brevity can achieve remarkable depth. Latin American magical realism, pioneered by authors like Gabriel Garcia Marquez, challenged Western assumptions about the boundaries between reality and imagination. Turkish literature, from the court poetry of the Ottoman divan tradition to the novels of Nobel laureate Orhan Pamuk, bridges Eastern and Western literary worlds.",
                "discussion_questions": [
                    "What Turkish literary works would you recommend to an international reader?",
                    "Why do stories about universal themes resonate across different cultures?",
                    "How has literature helped you understand a culture different from your own?"
                ]
            }
        ],
        6: [
            {
                "title": "Approaches to Social Justice Around the World",
                "content": "Different societies have developed diverse approaches to addressing inequality and promoting social justice. The Scandinavian welfare state model emphasises universal public services funded through progressive taxation, resulting in some of the world's lowest inequality rates. Rwanda, after the devastating genocide of 1994, implemented remarkable reconciliation processes including community-based 'gacaca' courts that prioritised restorative rather than purely punitive justice. India's constitutional reservation system allocates educational and government positions to historically marginalised castes. New Zealand's Treaty of Waitangi settlements aim to address historical injustices against the Maori people through negotiated agreements. South Korea's rapid economic transformation from poverty to prosperity within a single generation offers lessons about industrial policy and education investment. Turkey's position bridging Europe and Asia provides unique perspectives on balancing economic development, cultural preservation, and social equity.",
                "discussion_questions": [
                    "Which approach to social justice do you find most effective and why?",
                    "Can economic growth alone solve inequality, or are additional measures needed?",
                    "What role should young people play in addressing social justice issues?"
                ]
            }
        ],
        7: [
            {
                "title": "Scientific Innovation Across Cultures and Centuries",
                "content": "Scientific innovation has emerged from diverse civilisations throughout history, challenging the common misconception that modern science is exclusively a Western achievement. Islamic Golden Age scholars like Ibn al-Haytham pioneered the scientific method and made foundational contributions to optics centuries before European scientists adopted similar approaches. Chinese civilisation independently developed printing, gunpowder, the compass, and paper, technologies that transformed the entire world. Indian mathematicians invented the concept of zero and the decimal system that forms the basis of modern mathematics. The ancient Maya developed sophisticated astronomical calendars with remarkable accuracy. In the modern era, scientific collaboration has become increasingly international, with major projects like the Large Hadron Collider and the International Space Station bringing together researchers from dozens of countries. Turkey has contributed to global science through institutions like TUBITAK and the growing presence of Turkish researchers in international scientific communities.",
                "discussion_questions": [
                    "Why is it important to recognise scientific contributions from all civilisations?",
                    "How does international collaboration advance scientific progress?",
                    "What scientific challenges require global cooperation to solve?"
                ]
            }
        ],
        8: [
            {
                "title": "Artistic Expression in Different Societies",
                "content": "Artistic expression takes remarkably different forms across world cultures, reflecting diverse aesthetic values and social functions. Aboriginal Australian art, one of the world's oldest continuous art traditions spanning over 65,000 years, serves as a visual language encoding spiritual knowledge, geographical information, and cultural law. Japanese wabi-sabi aesthetics find beauty in imperfection, transience, and incompleteness, a philosophical perspective that contrasts sharply with Western ideals of symmetry and permanence. West African griot tradition combines oral storytelling, music, and historical preservation into a single artistic practice. Brazilian carnival demonstrates how visual art, music, dance, and costume design can merge into a massive communal creative expression. Islamic geometric art developed extraordinary mathematical precision as a form of spiritual expression, avoiding figurative representation to create mesmerising patterns of infinite complexity. Turkish arts encompass ebru (paper marbling), miniature painting, ceramic tilework, and shadow puppet theatre, each reflecting different aspects of the country's rich cultural heritage.",
                "discussion_questions": [
                    "Which art form from another culture would you most like to learn about?",
                    "How does Turkish artistic heritage compare with other traditions mentioned?",
                    "Do you think art should have a social purpose or exist for its own sake?"
                ]
            }
        ],
        9: [
            {
                "title": "Health Practices and Beliefs Around the World",
                "content": "Approaches to health and healing vary enormously across cultures, reflecting different understandings of the relationship between body, mind, and environment. Traditional Chinese Medicine, practised for over two thousand years, views health as a balance of opposing forces (yin and yang) and uses acupuncture, herbal remedies, and tai chi to restore equilibrium. Ayurvedic medicine from India classifies individuals into body types (doshas) and prescribes personalised diet, exercise, and lifestyle recommendations. Many Indigenous American healing traditions incorporate spiritual ceremonies, herbal knowledge, and community involvement in the healing process. Nordic countries have long traditions of sauna use, cold-water swimming, and 'friluftsliv' (outdoor living) as foundations of physical and mental well-being. The Mediterranean diet, traditional to countries including Turkey, Greece, and Italy, has been extensively validated by modern research as one of the healthiest dietary patterns in the world. Modern integrative medicine increasingly seeks to combine evidence-based conventional treatments with beneficial practices from traditional healing systems.",
                "discussion_questions": [
                    "What traditional health practices are common in Turkish culture?",
                    "Should traditional medicine be integrated with modern healthcare?",
                    "How do cultural attitudes influence people's approach to mental health?"
                ]
            }
        ],
        10: [
            {
                "title": "Environmental Stewardship Across Cultures",
                "content": "Different cultures have developed profoundly different relationships with the natural environment, offering valuable lessons for contemporary sustainability challenges. Many Indigenous communities worldwide practise environmental stewardship based on the principle that humans are part of nature rather than separate from or superior to it. The Maori concept of 'kaitiakitanga' in New Zealand emphasises guardianship of the natural world for future generations. Bhutan measures national success through Gross National Happiness rather than GDP, incorporating environmental conservation as a constitutional requirement. Japanese 'satoyama' landscapes demonstrate how centuries of careful human management can create biodiverse ecosystems that serve both ecological and agricultural functions. Costa Rica has reversed deforestation and now generates over 98% of its electricity from renewable sources. In Turkey, the concept of 'vakif' (charitable endowment) historically included the protection and maintenance of water sources, green spaces, and natural resources. These diverse perspectives suggest that effective environmental protection requires combining scientific knowledge with cultural wisdom and community engagement.",
                "discussion_questions": [
                    "What can modern societies learn from Indigenous environmental practices?",
                    "Should countries measure success through environmental indicators rather than GDP?",
                    "How does Turkish cultural heritage relate to environmental stewardship?"
                ]
            }
        ]
    }
}

FUN_FACTS_BANK = {
    9: {
        1: [
            "The longest school year in the world is in Japan, where students attend approximately 243 days per year compared to about 180 in the United States.",
            "Finland's education system, consistently ranked among the best globally, does not give standardised tests to students until they are sixteen years old.",
            "The oldest continuously operating school in the world is The King's School in Canterbury, England, founded in 597 AD - over 1,400 years ago.",
            "In Denmark, students and teachers address each other by first names, reflecting the culture's emphasis on equality and informality.",
            "South Korea spends more per student on education than almost any other OECD country, and the literacy rate is virtually 100 percent."
        ],
        2: [
            "Psychologist Carl Jung, who influenced the Myers-Briggs personality test, believed that personality type was innate but that life experiences shaped how it manifested.",
            "Research shows that identical twins raised apart still share remarkable personality similarities, suggesting a strong genetic component to personality.",
            "The Big Five personality traits (openness, conscientiousness, extraversion, agreeableness, neuroticism) have been found to be consistent across more than fifty cultures worldwide.",
            "Studies indicate that personality can continue to change well into a person's sixties and seventies, challenging the idea that personality is fixed by early adulthood.",
            "The concept of the 'self' varies so much across cultures that some languages do not have a direct equivalent of the English word 'I' as a standalone concept."
        ],
        3: [
            "The first email was sent by Ray Tomlinson in 1971, and he chose the @ symbol simply because it was rarely used and would not appear in anyone's name.",
            "Approximately 500 million tweets are sent every day, which is equivalent to roughly 6,000 tweets per second across the globe.",
            "The first text message ever sent, on 3 December 1992, simply read 'Merry Christmas' and was sent by engineer Neil Papworth.",
            "Over 65 billion messages are sent through WhatsApp every day, making it the most widely used messaging application in the world.",
            "The average person checks their smartphone approximately 96 times per day, or once every ten minutes during waking hours."
        ],
        4: [
            "English has borrowed words from over 350 languages, making it one of the most linguistically diverse vocabularies in the world.",
            "The word 'set' has the most definitions of any English word, with the Oxford English Dictionary listing over 430 distinct senses.",
            "There are approximately 170,000 words currently in use in the English language, though the average adult uses only about 20,000 to 35,000 in daily life.",
            "The most common letter in English is 'e', appearing in approximately 11 percent of all words, which is why it is worth only one point in Scrabble.",
            "English is the only major language that does not have an official regulatory body governing its grammar and vocabulary, unlike French (Academie Francaise) or Turkish (TDK)."
        ],
        5: [
            "The Library of Alexandria, established around 283 BC in Egypt, aimed to collect every book in the world and may have held up to 400,000 scrolls at its peak.",
            "Miguel de Cervantes' Don Quixote, published in 1605, is considered the first modern novel and has been translated into more languages than any other book except the Bible.",
            "Nigerian author Chinua Achebe's Things Fall Apart has sold over 20 million copies and been translated into 57 languages since its publication in 1958.",
            "The shortest published poem in English is attributed to Muhammad Ali: 'Me, We.' - just four letters exploring the relationship between individual and community.",
            "Turkish Nobel laureate Orhan Pamuk's novels have been translated into over 60 languages, making him one of the most widely read authors in the world."
        ],
        6: [
            "If the world's wealth were distributed equally, every adult on Earth would have approximately $87,000, yet currently the richest 1% own more than the bottom 50% combined.",
            "Norway's sovereign wealth fund, built from oil revenues, is worth over $1.4 trillion and owns approximately 1.5% of all listed companies worldwide.",
            "The Sustainable Development Goals adopted in 2015 have 169 specific targets across 17 goals, creating the most comprehensive framework for global development ever agreed upon.",
            "Bangladesh has reduced its poverty rate from 44% to under 15% in just two decades, representing one of the fastest poverty reduction rates in human history.",
            "The concept of GDP was invented in 1934 by Simon Kuznets, who himself warned that it should not be used as a measure of welfare or well-being."
        ],
        7: [
            "The human brain contains approximately 86 billion neurons, each connected to up to 10,000 other neurons, creating roughly 100 trillion neural connections.",
            "CRISPR gene editing technology costs approximately $75 per experiment today, compared to over $5,000 for earlier gene editing methods, democratising access to genetic research.",
            "Quantum computers can theoretically perform certain calculations millions of times faster than classical computers by exploiting quantum mechanical phenomena like superposition.",
            "The International Space Station travels at approximately 28,000 kilometres per hour, orbiting Earth once every 90 minutes and crossing 16 sunrises per day.",
            "More computing power exists in a modern smartphone than was used by NASA for the entire Apollo 11 moon landing mission in 1969."
        ],
        8: [
            "The Lascaux cave paintings in France, estimated to be 17,000 years old, demonstrate that artistic expression is one of the most ancient and fundamental human activities.",
            "Leonardo da Vinci's Mona Lisa, painted between 1503 and 1519, is viewed by approximately 10 million visitors per year at the Louvre Museum in Paris.",
            "The Turkish art of ebru (paper marbling) was inscribed on UNESCO's Representative List of Intangible Cultural Heritage of Humanity in 2014.",
            "Beethoven composed many of his greatest works, including his Ninth Symphony, after becoming almost completely deaf, demonstrating the power of inner artistic vision.",
            "The Sistine Chapel ceiling, painted by Michelangelo, contains over 300 figures and took approximately four years to complete (1508-1512)."
        ],
        9: [
            "The human body contains approximately 37.2 trillion cells, and roughly 3.8 million cells are replaced every second through natural processes.",
            "Teenagers need between 8 and 10 hours of sleep per night, but their circadian rhythms naturally shift later, making early school start times biologically challenging.",
            "Regular physical exercise has been shown to be as effective as medication for treating mild to moderate depression in numerous clinical studies.",
            "The Mediterranean diet, traditional in Turkey, has been associated with a 25% reduction in cardiovascular disease risk in large-scale research studies.",
            "Chronic stress can physically shrink the hippocampus, the brain region responsible for memory and learning, but this effect is reversible with stress management techniques."
        ],
        10: [
            "Earth's atmosphere contains approximately 420 parts per million of carbon dioxide, the highest concentration in at least 800,000 years based on ice core data.",
            "A single mature tree can absorb approximately 22 kilograms of carbon dioxide per year and produce enough oxygen for two people to breathe.",
            "The Great Pacific Garbage Patch, a collection of marine debris in the North Pacific Ocean, covers an area roughly three times the size of France.",
            "Renewable energy sources now provide approximately 30% of global electricity generation, with solar and wind power costs falling by over 85% in the past decade.",
            "Turkey is home to three of the world's 36 biodiversity hotspots, making it one of the most ecologically significant countries in the Mediterranean basin."
        ]
    }
}

PROJECT_BANK = {
    9: {
        1: [
            {
                "title": "High School Survival Guide",
                "description": "Create a comprehensive, visually appealing digital guide for incoming freshmen that includes practical advice on time management, study strategies, navigating social situations, and getting involved in extracurricular activities. Include interviews with current students and teachers.",
                "steps": [
                    "Research common challenges faced by new high school students through surveys and interviews",
                    "Organise information into clear categories: academics, social life, extracurriculars, and well-being",
                    "Design the guide using digital tools (Canva, Google Slides, or similar) with engaging visuals",
                    "Include practical templates such as weekly planners, goal-setting worksheets, and club comparison charts",
                    "Present the guide to the class and distribute it to incoming freshmen at orientation"
                ],
                "outcomes": ["Research and interview skills", "Digital design competence", "Organisational thinking", "Empathetic communication"]
            }
        ],
        2: [
            {
                "title": "Personality Profile Exhibition",
                "description": "Design an interactive classroom exhibition exploring different personality frameworks (Myers-Briggs, Big Five, multiple intelligences). Create visual displays, interactive quizzes, and reflective activities that help visitors understand their own personality traits and appreciate diversity.",
                "steps": [
                    "Research at least three personality frameworks and their scientific basis",
                    "Create visual displays explaining each framework with clear, accessible language",
                    "Design interactive activities that visitors can participate in during the exhibition",
                    "Prepare a reflection journal template that visitors can take away and complete",
                    "Host the exhibition for other classes and collect feedback on the experience"
                ],
                "outcomes": ["Research methodology", "Visual communication", "Understanding of psychological frameworks", "Event planning"]
            }
        ],
        3: [
            {
                "title": "Digital Citizenship Campaign",
                "description": "Develop a school-wide awareness campaign about responsible digital communication. Create multimedia materials including infographics, short videos, and interactive workshops that address topics such as online privacy, cyberbullying, misinformation, and digital well-being.",
                "steps": [
                    "Conduct a school survey to identify the most pressing digital communication concerns",
                    "Research best practices for digital citizenship from reputable educational sources",
                    "Create a series of infographics and short videos addressing key issues",
                    "Design and deliver an interactive workshop for younger students",
                    "Measure the campaign's impact through a follow-up survey and present results"
                ],
                "outcomes": ["Survey design and analysis", "Multimedia content creation", "Public speaking", "Digital literacy education"]
            }
        ],
        4: [
            {
                "title": "Tenses in Real Life Documentary",
                "description": "Produce a short documentary or video essay that demonstrates how different English tenses are used in authentic contexts such as news reporting, scientific writing, storytelling, and everyday conversation. Include examples, expert commentary, and viewer exercises.",
                "steps": [
                    "Collect authentic examples of tense usage from newspapers, academic articles, novels, and conversations",
                    "Categorise examples by tense type and analyse why each tense was chosen in context",
                    "Write a script that explains each tense with engaging real-world examples",
                    "Film and edit the documentary using available technology (phones, tablets, laptops)",
                    "Screen the documentary for the class and facilitate a discussion about tense awareness"
                ],
                "outcomes": ["Linguistic analysis skills", "Video production", "Academic writing awareness", "Critical thinking about language"]
            }
        ],
        5: [
            {
                "title": "World Literature Festival",
                "description": "Organise a class or school literature festival celebrating stories from at least five different continents. Create book displays, author profiles, themed readings, creative writing responses, and a world literature map showing thematic connections across cultures.",
                "steps": [
                    "Select representative works from at least five different literary traditions",
                    "Research the cultural and historical context of each selected work",
                    "Create visually engaging book displays with author biographies and cultural context",
                    "Write creative responses (poems, short stories, or essays) inspired by the selected works",
                    "Design an interactive world literature map and present the festival to the school community"
                ],
                "outcomes": ["Cross-cultural literary analysis", "Creative writing", "Visual display design", "Event coordination"]
            }
        ],
        6: [
            {
                "title": "Global Issues Awareness Conference",
                "description": "Plan and host a mini-conference on global issues where student teams present research on topics such as poverty, climate change, education inequality, and public health. Include panel discussions, poster presentations, and an action plan workshop.",
                "steps": [
                    "Form teams and assign specific global issues for in-depth research",
                    "Gather data from reliable international sources (UN, WHO, World Bank)",
                    "Prepare professional presentations with statistical evidence and case studies",
                    "Organise panel discussions where teams debate potential solutions",
                    "Develop concrete action plans that students can implement at school or community level"
                ],
                "outcomes": ["Research and data analysis", "Public speaking and debate", "Critical evaluation of global challenges", "Action planning"]
            }
        ],
        7: [
            {
                "title": "Innovation Challenge: Solve a Local Problem",
                "description": "Apply the scientific method and design thinking to identify and address a real problem in your school or community. Develop a prototype solution, test it, gather feedback, and present your findings as a professional research poster.",
                "steps": [
                    "Identify a specific problem through observation, surveys, and data collection",
                    "Research existing solutions and evaluate their strengths and limitations",
                    "Design and build a prototype solution using available materials and technologies",
                    "Test the prototype systematically, collect data, and iterate based on results",
                    "Create a professional research poster and present findings at a school science showcase"
                ],
                "outcomes": ["Scientific method application", "Design thinking", "Prototyping and testing", "Professional presentation skills"]
            }
        ],
        8: [
            {
                "title": "Cross-Disciplinary Art Installation",
                "description": "Collaborate with classmates to create an art installation that combines at least two artistic disciplines (visual art, music, creative writing, digital media, performance) around a common theme. Document the creative process and present the installation to the school community.",
                "steps": [
                    "Select a theme that resonates with the group and brainstorm how different art forms can express it",
                    "Assign roles based on individual strengths and interests across different disciplines",
                    "Create individual artistic components that contribute to the unified installation",
                    "Design the installation space and coordinate how the different elements interact",
                    "Document the creative process through photos, videos, and reflective writing, then host an opening event"
                ],
                "outcomes": ["Interdisciplinary collaboration", "Creative problem-solving", "Artistic technique development", "Exhibition curation"]
            }
        ],
        9: [
            {
                "title": "School Wellness Programme Design",
                "description": "Design a comprehensive wellness programme for your school that addresses nutrition, physical activity, sleep, and mental health. Include evidence-based recommendations, practical resources, and a plan for implementation and evaluation.",
                "steps": [
                    "Conduct a school-wide health needs assessment through surveys and focus groups",
                    "Research evidence-based wellness strategies from public health organisations",
                    "Design programme components addressing the four pillars: nutrition, exercise, sleep, and mental health",
                    "Create practical resources including meal planning guides, exercise routines, and stress management toolkits",
                    "Present the programme proposal to school administration and pilot one component"
                ],
                "outcomes": ["Health research literacy", "Programme design", "Survey methodology", "Advocacy and persuasion skills"]
            }
        ],
        10: [
            {
                "title": "School Environmental Sustainability Audit and Action Plan",
                "description": "Conduct a comprehensive environmental audit of your school, measuring energy use, water consumption, waste generation, and biodiversity. Analyse the data, identify areas for improvement, and develop a detailed action plan with measurable targets.",
                "steps": [
                    "Develop audit methodology and data collection tools for energy, water, waste, and biodiversity",
                    "Collect baseline data over a two-week period using systematic measurement techniques",
                    "Analyse data and create visualisations showing current environmental performance",
                    "Research best practices from eco-schools and sustainability programmes worldwide",
                    "Develop a prioritised action plan with specific targets, timelines, and responsible parties, then present to the school board"
                ],
                "outcomes": ["Data collection and analysis", "Environmental science application", "Strategic planning", "Stakeholder communication"]
            }
        ]
    }
}

PROGRESS_CHECK_BANK = {
    9: {
        1: [
            {"skill": "Reading", "task": "Read a text about high school orientation programmes and answer comprehension questions about main ideas, supporting details, and vocabulary in context.", "criteria": "Correctly identify main argument, locate specific details, and infer meaning from context with at least 70% accuracy."},
            {"skill": "Writing", "task": "Write a formal email to a school counsellor describing your academic goals and requesting advice on course selection (120-150 words).", "criteria": "Appropriate formal register, clear organisation, correct grammar, and specific goal statements."},
            {"skill": "Grammar", "task": "Complete a cloze passage using present simple, present continuous, past simple, and past continuous accurately in context.", "criteria": "Minimum 80% accuracy in tense selection with correct verb forms."},
            {"skill": "Vocabulary", "task": "Define and use ten key terms related to academic life (curriculum, extracurricular, orientation, semester, elective, etc.) in original sentences.", "criteria": "Accurate definitions and contextually appropriate usage in well-formed sentences."},
            {"skill": "Speaking", "task": "Give a two-minute presentation introducing yourself to new classmates, including your academic interests, goals, and extracurricular plans.", "criteria": "Clear pronunciation, logical organisation, appropriate register, and confident delivery."}
        ],
        2: [
            {"skill": "Reading", "task": "Analyse an article about personality development theories and evaluate the arguments presented.", "criteria": "Demonstrate understanding of key theories, compare perspectives, and form a supported personal opinion."},
            {"skill": "Writing", "task": "Write a reflective essay about your own personality traits and how they influence your learning style (130-150 words).", "criteria": "Thoughtful self-reflection, clear structure, use of personality-related vocabulary, and grammatical accuracy."},
            {"skill": "Grammar", "task": "Use modals of deduction (must, might, could, can't) and noun clauses correctly in a series of contextualised exercises.", "criteria": "Minimum 80% accuracy with appropriate modal selection and correct noun clause word order."},
            {"skill": "Vocabulary", "task": "Match personality adjectives with their definitions and use them in descriptive paragraphs about real or fictional people.", "criteria": "Accurate matching and natural usage demonstrating understanding of nuance."},
            {"skill": "Speaking", "task": "Participate in a group discussion about the advantages and challenges of different personality types in a school setting.", "criteria": "Active contribution, use of target vocabulary, respectful engagement with differing opinions."}
        ],
        3: [
            {"skill": "Reading", "task": "Read an article about digital communication trends and distinguish between facts, opinions, and biased claims.", "criteria": "Correctly categorise at least 80% of identified statements and explain reasoning."},
            {"skill": "Writing", "task": "Write an opinion essay on the impact of social media on teenage communication (130-150 words).", "criteria": "Clear thesis, balanced arguments, appropriate linking words, and well-supported conclusion."},
            {"skill": "Grammar", "task": "Transform active sentences to passive voice across different tenses and construct causative sentences.", "criteria": "Minimum 80% accuracy with correct passive forms and appropriate causative structures."},
            {"skill": "Vocabulary", "task": "Use fifteen technology and communication terms accurately in context (algorithm, encryption, bandwidth, platform, etc.).", "criteria": "Contextually appropriate usage demonstrating genuine understanding of each term."},
            {"skill": "Speaking", "task": "Deliver a persuasive speech proposing three specific measures to promote responsible digital communication in your school.", "criteria": "Logical argumentation, effective use of persuasive techniques, and clear call to action."}
        ],
        4: [
            {"skill": "Reading", "task": "Read a text that uses all twelve English tenses and identify each tense, explaining why the author chose it.", "criteria": "Correctly identify at least 10 of 12 tenses and provide logical explanations for their usage."},
            {"skill": "Writing", "task": "Write a biographical narrative about a historical figure using at least eight different tenses accurately (130-150 words).", "criteria": "Accurate tense usage, clear timeline, engaging narrative, and minimum eight distinct tenses."},
            {"skill": "Grammar", "task": "Complete mixed conditional exercises (zero through third) and identify the conditional type used in authentic texts.", "criteria": "Minimum 80% accuracy in both production and identification tasks."},
            {"skill": "Vocabulary", "task": "Explain the meaning of common time expressions and match them with appropriate tenses.", "criteria": "Accurate matching and ability to explain the logical connection between time markers and tenses."},
            {"skill": "Speaking", "task": "Tell a three-minute story about a memorable experience, consciously using a variety of tenses to manage the timeline.", "criteria": "Natural tense transitions, engaging delivery, and accurate usage of at least six different tenses."}
        ],
        5: [
            {"skill": "Reading", "task": "Read an extract from a work of world literature and analyse its themes, literary devices, and cultural context.", "criteria": "Identify at least three themes and two literary devices, connecting them to the work's cultural background."},
            {"skill": "Writing", "task": "Write a comparative essay analysing a common theme in two literary works from different cultures (140-160 words).", "criteria": "Clear thesis, effective comparison structure, textual evidence, and insightful cultural analysis."},
            {"skill": "Grammar", "task": "Use wish/if only structures and cleft sentences accurately in exercises based on literary contexts.", "criteria": "Minimum 80% accuracy with correct tense usage after wish and proper cleft sentence construction."},
            {"skill": "Vocabulary", "task": "Define and use fifteen literary analysis terms (metaphor, symbolism, allegory, irony, narrative voice, etc.).", "criteria": "Accurate definitions and appropriate application to specific literary examples."},
            {"skill": "Speaking", "task": "Participate in a book club discussion, presenting your interpretation of a text and responding to others' viewpoints.", "criteria": "Evidence-based arguments, respectful engagement, use of literary vocabulary, and willingness to consider alternative interpretations."}
        ],
        6: [
            {"skill": "Reading", "task": "Analyse a report on a global issue using data, charts, and statistics to evaluate the severity and proposed solutions.", "criteria": "Accurate data interpretation, critical evaluation of proposed solutions, and evidence-based conclusions."},
            {"skill": "Writing", "task": "Write a problem-solution essay on a specific global issue, including evidence and a realistic action plan (140-160 words).", "criteria": "Clear problem definition, evidence-based analysis, feasible solutions, and appropriate academic register."},
            {"skill": "Grammar", "task": "Use adverbial clauses and inversion structures accurately in formal academic sentences.", "criteria": "Minimum 80% accuracy with correct clause structure and appropriate use of inverted forms."},
            {"skill": "Vocabulary", "task": "Use twenty key terms related to global issues (sustainability, inequality, governance, humanitarian, infrastructure, etc.).", "criteria": "Accurate contextual usage demonstrating understanding of political, economic, and social terminology."},
            {"skill": "Speaking", "task": "Participate in a formal debate on a global issue, presenting arguments for or against a specific position.", "criteria": "Well-structured arguments, effective use of evidence, appropriate formal register, and respectful rebuttal of opposing views."}
        ],
        7: [
            {"skill": "Reading", "task": "Read a scientific article and evaluate the methodology, findings, and conclusions using critical analysis skills.", "criteria": "Identify research question, evaluate methodology, assess evidence quality, and determine conclusion validity."},
            {"skill": "Writing", "task": "Write a research summary describing a scientific experiment's hypothesis, method, results, and implications (140-160 words).", "criteria": "Clear scientific structure, accurate use of passive voice, precise vocabulary, and logical presentation."},
            {"skill": "Grammar", "task": "Use reported speech with modals, questions, and commands, and construct defining and non-defining relative clauses.", "criteria": "Minimum 80% accuracy in backshifting, correct word order, and appropriate relative pronoun selection."},
            {"skill": "Vocabulary", "task": "Define and use fifteen scientific and technological terms (hypothesis, variable, prototype, algorithm, sustainable, etc.).", "criteria": "Accurate definitions and appropriate contextual usage in scientific and general contexts."},
            {"skill": "Speaking", "task": "Present a scientific innovation to the class, explaining how it works, its benefits, and potential ethical concerns.", "criteria": "Clear explanation, logical structure, appropriate technical vocabulary, and thoughtful ethical reflection."}
        ],
        8: [
            {"skill": "Reading", "task": "Read a critical review of an artwork or performance and evaluate the reviewer's arguments and criteria.", "criteria": "Identify the reviewer's thesis, evaluate supporting evidence, and assess the fairness of the critique."},
            {"skill": "Writing", "task": "Write a critical review of a piece of art, music, or literature, supporting your evaluation with specific evidence (130-150 words).", "criteria": "Clear evaluative thesis, specific evidence, appropriate arts vocabulary, and balanced assessment."},
            {"skill": "Grammar", "task": "Use participle clauses and advanced passive structures (impersonal passive, passive with two objects) in academic contexts.", "criteria": "Minimum 80% accuracy with natural-sounding participle clauses and correct impersonal passive formation."},
            {"skill": "Vocabulary", "task": "Use fifteen terms related to art and creative expression (aesthetic, composition, genre, medium, interpretation, etc.).", "criteria": "Accurate and natural usage demonstrating genuine understanding of artistic terminology."},
            {"skill": "Speaking", "task": "Present a comparative analysis of two artworks from different cultures, discussing similarities, differences, and cultural significance.", "criteria": "Structured comparison, relevant cultural context, appropriate vocabulary, and personal critical response."}
        ],
        9: [
            {"skill": "Reading", "task": "Read a public health report on adolescent well-being and extract key findings, trends, and recommendations.", "criteria": "Accurately identify statistical trends, distinguish between correlation and causation, and summarise recommendations."},
            {"skill": "Writing", "task": "Write a proposal for a school health initiative, including rationale, objectives, activities, and expected outcomes (140-160 words).", "criteria": "Clear rationale with evidence, specific measurable objectives, feasible activities, and realistic outcomes."},
            {"skill": "Grammar", "task": "Use advanced gerund and infinitive patterns and mixed conditional structures in health-related contexts.", "criteria": "Minimum 80% accuracy with correct verb patterns and appropriate conditional type selection."},
            {"skill": "Vocabulary", "task": "Define and use fifteen health and well-being terms (cardiovascular, metabolism, resilience, cognitive, preventive, etc.).", "criteria": "Accurate definitions and contextually appropriate usage in both scientific and everyday contexts."},
            {"skill": "Speaking", "task": "Lead a group discussion on how schools can better support student well-being, proposing and defending specific strategies.", "criteria": "Effective facilitation, evidence-based proposals, inclusive discussion management, and clear summary of conclusions."}
        ],
        10: [
            {"skill": "Reading", "task": "Analyse an environmental report using data, graphs, and expert opinions to evaluate proposed sustainability measures.", "criteria": "Accurate data interpretation, critical evaluation of evidence quality, and well-reasoned conclusions."},
            {"skill": "Writing", "task": "Write an argumentative essay on the most effective approach to environmental protection, comparing individual action with systemic change (140-160 words).", "criteria": "Clear thesis, balanced argument with evidence, effective counterargument, and strong conclusion."},
            {"skill": "Grammar", "task": "Use hypothetical structures (suppose, as if, it's time, would rather) and cohesive devices in academic paragraphs.", "criteria": "Minimum 80% accuracy with natural usage and effective paragraph cohesion."},
            {"skill": "Vocabulary", "task": "Use twenty environmental and sustainability terms (biodiversity, carbon footprint, ecosystem, renewable, deforestation, etc.).", "criteria": "Accurate and contextually appropriate usage demonstrating understanding of ecological concepts."},
            {"skill": "Speaking", "task": "Deliver a formal presentation proposing a sustainability plan for your school, using data to support each recommendation.", "criteria": "Data-driven arguments, professional delivery, effective visual aids, and persuasive call to action."}
        ]
    }
}

LISTENING_SCRIPT_BANK = {
    9: {
        1: [
            {
                "title": "Welcome to Anatolian High School",
                "type": "announcement",
                "script": "Good morning, everyone, and welcome to the new academic year at Anatolian High School. My name is Mr. Demir, and I am the head of student guidance. I would like to take a few minutes to share some important information with our new ninth-grade students. First, your timetables are available on the school's mobile application. Please download the app if you haven't already. Second, orientation sessions will run throughout this first week. Each session covers a different aspect of school life, from academic expectations to extracurricular opportunities. I strongly encourage all freshmen to attend every session. Third, each of you has been assigned a senior student mentor. Your mentor's name is listed in the app, and they will contact you by the end of today. Do not hesitate to ask your mentor any questions, no matter how small they may seem. Finally, our library is open from seven-thirty in the morning until six in the evening, and the student lounge is available during all break periods. We want you to feel at home here, and we are committed to supporting your transition. Thank you, and have an excellent first day.",
                "questions": [
                    {"question": "Where can students find their timetables?", "answer": "On the school's mobile application"},
                    {"question": "How long do the orientation sessions last?", "answer": "Throughout the first week"},
                    {"question": "Who will contact each freshman by the end of the first day?", "answer": "Their assigned senior student mentor"}
                ]
            }
        ],
        2: [
            {
                "title": "Understanding Yourself: A Psychology Lecture",
                "type": "lecture",
                "script": "Today we are going to explore a fascinating area of psychology: personality types. Now, many of you may have heard of the Myers-Briggs Type Indicator, which classifies people into sixteen personality types based on four dimensions. However, I want to introduce you to a more scientifically validated framework called the Big Five. This model identifies five core personality traits: openness to experience, conscientiousness, extraversion, agreeableness, and neuroticism. You can remember these with the acronym OCEAN. Research conducted across more than fifty cultures has consistently found these five traits in every population studied. What is particularly interesting for you as teenagers is that your personality is not fixed. Studies show that personality continues to develop well into your twenties and even beyond. Most people become more conscientious and agreeable as they mature, while neuroticism tends to decrease with age. So if you feel uncertain about who you are right now, that is completely normal. Adolescence is precisely the time when you are meant to explore different aspects of your identity. The key is to approach this exploration with curiosity rather than anxiety.",
                "questions": [
                    {"question": "What does the acronym OCEAN stand for?", "answer": "Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism"},
                    {"question": "How many cultures has the Big Five been validated across?", "answer": "More than fifty cultures"},
                    {"question": "According to the lecture, what happens to conscientiousness as people mature?", "answer": "It increases / people become more conscientious"}
                ]
            }
        ],
        3: [
            {
                "title": "Digital Literacy Workshop Introduction",
                "type": "workshop",
                "script": "Welcome to our digital literacy workshop. Over the next hour, we will cover three essential topics that every modern communicator needs to understand. First, we will discuss how to evaluate online information sources. Not everything you read online is accurate, and learning to distinguish reliable sources from unreliable ones is a critical skill. We will practise using a simple checklist: check the author's credentials, look for citations, examine the publication date, consider whether the source has a potential bias, and cross-reference with at least two other reputable sources. Second, we will explore privacy settings on the most popular social media platforms. Many students share far more personal information than they realise, and adjusting your privacy settings takes only a few minutes but can significantly reduce your digital vulnerability. Third, we will discuss the concept of a digital footprint. Every time you post, comment, like, or share something online, you are creating a permanent record that can be accessed by future employers, universities, and other institutions. The average teenager has a digital footprint that contains over ten thousand data points. Understanding and managing this footprint is essential for your future.",
                "questions": [
                    {"question": "How many topics will the workshop cover?", "answer": "Three essential topics"},
                    {"question": "What is the first step in evaluating online sources mentioned in the talk?", "answer": "Check the author's credentials"},
                    {"question": "How many data points does the average teenager's digital footprint contain?", "answer": "Over ten thousand data points"}
                ]
            }
        ],
        4: [
            {
                "title": "The History of English Tenses",
                "type": "lecture",
                "script": "Let me tell you something that might surprise you about English grammar. Old English, spoken over a thousand years ago, only had two tenses: past and present. There was no future tense at all. People expressed future meaning through context or by using the present tense with time markers. The auxiliary verb 'will' originally meant 'want' or 'desire', and 'shall' meant 'owe' or 'must'. Over centuries, these verbs gradually lost their original meanings and evolved into future tense markers. The perfect tenses developed during the Middle English period, between roughly 1100 and 1500, influenced partly by contact with French after the Norman Conquest. The continuous or progressive forms, which we create with 'be' plus the present participle, became common only in the seventeenth and eighteenth centuries. So the twelve-tense system that you are learning today is actually a relatively recent development in the history of English. What this means for you as learners is that tenses are not arbitrary rules imposed by grammarians. They evolved because speakers needed increasingly precise ways to express temporal relationships. Understanding this history can help you appreciate why each tense exists and when to use it most effectively.",
                "questions": [
                    {"question": "How many tenses did Old English have?", "answer": "Two tenses (past and present)"},
                    {"question": "What did the verb 'will' originally mean?", "answer": "Want or desire"},
                    {"question": "When did the continuous forms become common?", "answer": "In the seventeenth and eighteenth centuries"}
                ]
            }
        ],
        5: [
            {
                "title": "A Conversation About World Literature",
                "type": "discussion",
                "script": "Mr. Polat: Welcome back to our book club meeting. Today I would like to hear your thoughts on the novel we finished this week. Yasemin, would you like to start? Yasemin: Certainly. What struck me most was how the author used magical elements not as fantasy but as a way to express emotional truths that realistic fiction could not capture. When the character's sadness literally causes flowers to wilt, we understand the depth of her grief more powerfully than any description could convey. Kerem: I actually had a different reaction. I thought the magical elements represented the resilience of ordinary people. Despite impossible circumstances, the characters found ways to survive and even create beauty. It reminded me of stories my grandmother tells about her childhood. Mr. Polat: Both interpretations are valid, and that is precisely what makes great literature great. It generates multiple layers of meaning. Yasemin, you mentioned emotional truth. Kerem, you connected it to personal experience. These are exactly the kinds of deep reading we want to develop. Now, let me ask you both: how does this novel compare to the Turkish work we read last month?",
                "questions": [
                    {"question": "According to Yasemin, what purpose do the magical elements serve?", "answer": "To express emotional truths that realistic fiction cannot capture"},
                    {"question": "What did the magical elements remind Kerem of?", "answer": "Stories his grandmother tells about her childhood"},
                    {"question": "What does Mr. Polat say makes great literature great?", "answer": "It generates multiple layers of meaning"}
                ]
            }
        ],
        6: [
            {
                "title": "Global Inequality: A Panel Discussion",
                "type": "panel discussion",
                "script": "Moderator: Welcome to our panel on global inequality. Professor Aydin, could you start by giving us an overview of the current situation? Professor Aydin: Certainly. Despite significant progress in reducing extreme poverty, global inequality remains deeply troubling. The richest one percent of the world's population currently owns more wealth than the bottom fifty percent combined. And while average incomes have risen in many developing countries, the gap between the wealthiest and poorest nations continues to grow. Moderator: Dr. Sahin, what do you see as the primary causes? Dr. Sahin: The causes are complex and interconnected. Historical factors like colonialism created structural disadvantages that persist today. Unequal trade relationships mean that developing countries often export raw materials cheaply and import expensive manufactured goods. Additionally, climate change is amplifying existing inequalities because the poorest communities, which contributed least to the problem, suffer the most severe consequences. Moderator: What solutions would you both recommend? Professor Aydin: I believe we need fundamental reforms to international trade agreements and significant increases in educational investment. Dr. Sahin: I agree, and I would add that debt relief for developing nations and massive investment in renewable energy infrastructure are equally essential.",
                "questions": [
                    {"question": "How much wealth does the richest one percent own compared to the bottom fifty percent?", "answer": "More than the bottom fifty percent combined"},
                    {"question": "What historical factor does Dr. Sahin mention as creating lasting disadvantages?", "answer": "Colonialism"},
                    {"question": "What two solutions does Dr. Sahin recommend?", "answer": "Debt relief for developing nations and investment in renewable energy infrastructure"}
                ]
            }
        ],
        7: [
            {
                "title": "A Science Fair Presentation",
                "type": "presentation",
                "script": "Good afternoon, judges and fellow students. My name is Tugce, and together with my partner Onur, I am presenting our project: an affordable water filtration system designed for rural communities. The problem we identified is straightforward: approximately two billion people worldwide lack access to safely managed drinking water. Existing filtration technologies are often too expensive or too complex for communities without modern infrastructure. Our solution uses three locally available materials: activated charcoal, graded sand, and a bio-membrane made from plant cellulose. We hypothesised that this combination could remove at least ninety-five percent of common water contaminants while maintaining a practical flow rate. Onur designed an Arduino-based sensor array that monitors water clarity, pH levels, and bacterial contamination in real time. After seventeen iterations of our design, our final prototype achieves ninety-seven percent contaminant removal at a flow rate of two litres per minute, which is sufficient for household use. The total material cost per unit is approximately fifteen dollars. We believe this project demonstrates that meaningful scientific innovation does not require expensive equipment. It requires creative application of fundamental scientific principles to real problems.",
                "questions": [
                    {"question": "How many people worldwide lack access to safely managed drinking water?", "answer": "Approximately two billion people"},
                    {"question": "What three materials does the filtration system use?", "answer": "Activated charcoal, graded sand, and a bio-membrane made from plant cellulose"},
                    {"question": "What contaminant removal rate did the final prototype achieve?", "answer": "Ninety-seven percent"}
                ]
            }
        ],
        8: [
            {
                "title": "Gallery Talk: The Art of Crossing Boundaries",
                "type": "gallery tour",
                "script": "Thank you all for coming to the opening of our student exhibition, 'Crossing Boundaries.' I am Ms. Erdem, the art department chair, and I would like to guide you through this remarkable installation created by two of our most talented students, Hazal and Burak. What you see before you is a corridor designed to take you on a journey from tradition to modernity. On your left, Hazal's paintings begin with Turkish calligraphy rendered in deep indigo and gold, referencing centuries of Islamic artistic tradition. As you walk forward, the images gradually incorporate elements of urban life: street signs, digital interfaces, satellite photographs. The transformation is subtle but powerful. Accompanying the visual journey is Burak's original music. Notice how the soundscape begins with instruments reminiscent of traditional Turkish music, then progressively introduces electronic elements, synthesisers, and sampled urban sounds. What makes this installation exceptional is how the visual and auditory elements enhance each other. Hazal has told me that listening to Burak's compositions literally changed the colours she chose. And Burak says that studying Hazal's paintings helped him discover melodic structures he never would have found through music alone. This is the power of interdisciplinary art.",
                "questions": [
                    {"question": "What is the name of the exhibition?", "answer": "Crossing Boundaries"},
                    {"question": "What artistic tradition do Hazal's paintings reference at the beginning?", "answer": "Turkish calligraphy and Islamic artistic tradition"},
                    {"question": "How did the collaboration affect Hazal's work, according to Ms. Erdem?", "answer": "Listening to Burak's compositions changed the colours she chose"}
                ]
            }
        ],
        9: [
            {
                "title": "Student Health Forum",
                "type": "forum",
                "script": "Dr. Acar: Good morning, students. Today's health forum focuses on a topic that affects every single one of you: sleep. I know many of you think you can function perfectly well on five or six hours of sleep, but the scientific evidence tells a very different story. Research consistently shows that teenagers need between eight and ten hours of sleep per night for optimal cognitive function. When you sleep fewer than seven hours, your ability to concentrate decreases by approximately thirty percent, your emotional regulation becomes impaired, and your immune system weakens significantly. Ceren: Dr. Acar, I conducted a survey of two hundred students in our school, and the results were alarming. Only twenty-two percent reported getting eight or more hours of sleep on school nights. The most common reasons were homework overload, social media use before bed, and early school start times. Kaan: As an athlete, I can personally confirm the impact of poor sleep. Last year I was training six days a week but only sleeping about five hours. My performance dropped, I started getting injured more frequently, and my grades suffered too. It was not until I prioritised sleep that everything improved. Dr. Acar: Thank you both. The key message is this: sleep is not a luxury that you sacrifice for productivity. Sleep is the foundation upon which all productivity is built.",
                "questions": [
                    {"question": "By what percentage does concentration decrease with fewer than seven hours of sleep?", "answer": "Approximately thirty percent"},
                    {"question": "What percentage of surveyed students reported getting eight or more hours of sleep?", "answer": "Twenty-two percent"},
                    {"question": "What three consequences did Kaan experience from poor sleep?", "answer": "Performance dropped, more frequent injuries, and grades suffered"}
                ]
            }
        ],
        10: [
            {
                "title": "Environmental Summit Student Address",
                "type": "speech",
                "script": "Distinguished guests, fellow students, and educators, my name is Cem, and I am here to present the results of our school's environmental sustainability initiative. Six months ago, my partner Ipek and I began by asking a simple question: what is our school's actual environmental impact? The answer, frankly, was sobering. Our initial audit revealed that the school was generating over two hundred kilograms of recyclable waste per week, almost all of which was going to landfill. Our energy consumption was thirty percent higher than comparable institutions, and our water usage was similarly excessive. We implemented a three-phase response. Phase one focused on waste reduction through a comprehensive recycling programme with clearly labelled bins and student monitors. Phase two addressed energy consumption through behavioural changes such as turning off lights and equipment when not in use. Phase three involved structural improvements including LED lighting and a rainwater harvesting system. The results after just five months are significant. Landfill waste has decreased by forty-two percent. Energy consumption has dropped by seventeen percent. And we have established a school garden that serves as both an educational resource and a carbon offset initiative. But perhaps the most important outcome is cultural. Students and staff across the school now think about environmental impact as a daily consideration, not an abstract concern. This is the kind of systemic change that, when replicated across thousands of schools, can genuinely contribute to environmental sustainability.",
                "questions": [
                    {"question": "How much recyclable waste was the school generating per week before the initiative?", "answer": "Over two hundred kilograms"},
                    {"question": "What were the three phases of the response?", "answer": "Phase one: waste reduction/recycling, Phase two: energy consumption behavioural changes, Phase three: structural improvements"},
                    {"question": "By what percentage did landfill waste decrease?", "answer": "Forty-two percent"}
                ]
            }
        ]
    }
}

MODEL_WRITING_BANK = {
    9: {
        1: [
            {
                "type": "Formal Email",
                "topic": "Writing to a school counsellor about academic goals",
                "model": "Dear Mr. Demir,\n\nI am writing to request a meeting to discuss my academic goals for this year. As a new ninth-grade student, I am eager to make the most of my high school experience, but I recognise that I need guidance in planning my course selections and extracurricular commitments.\n\nSpecifically, I would like to discuss three areas. First, I am interested in pursuing advanced science courses but am unsure whether my current preparation is sufficient. Second, I would appreciate advice on balancing academic workload with extracurricular activities, particularly the debate club and photography society. Third, I would like to explore potential career pathways that align with my interests in science and communication.\n\nI am available during study periods on Tuesday and Thursday afternoons. Would either of these times be convenient for a thirty-minute meeting?\n\nThank you for your time and support.\n\nYours sincerely,\nEmre Yildirim",
                "word_count": 138,
                "key_features": ["Formal register", "Clear purpose statement", "Specific discussion points", "Polite request", "Appropriate closing"]
            }
        ],
        2: [
            {
                "type": "Reflective Essay",
                "topic": "Understanding my personality type and its influence on learning",
                "model": "Discovering that I am an introverted-intuitive personality type has fundamentally changed how I approach my education. For years, I assumed that my preference for quiet reflection over group discussion was a weakness, something I needed to overcome in order to succeed academically. However, studying personality psychology has taught me that introversion is not a limitation but a different mode of processing information.\n\nI now understand that I learn most effectively when I have time to think independently before engaging in discussion. Rather than forcing myself to contribute immediately in class, I prepare my thoughts in advance, which actually leads to more meaningful contributions. I have also recognised that my tendency towards deep focus, while sometimes making social situations challenging, gives me an advantage in subjects that require sustained concentration, such as literature and mathematics.\n\nThis self-awareness has not only improved my academic performance but has also helped me build more authentic relationships with classmates who appreciate my thoughtful approach.",
                "word_count": 152,
                "key_features": ["Personal reflection", "Self-awareness", "Specific examples", "Growth narrative", "Connection to learning"]
            }
        ],
        3: [
            {
                "type": "Opinion Essay",
                "topic": "The impact of social media on teenage communication",
                "model": "Social media has fundamentally transformed how teenagers communicate, bringing both significant benefits and serious concerns that our generation must address thoughtfully. On the positive side, platforms like Instagram and Twitter have given young people unprecedented access to diverse perspectives, enabling connections across geographical and cultural boundaries that would have been impossible just two decades ago.\n\nHowever, the negative consequences cannot be ignored. Research consistently links excessive social media use with increased anxiety, reduced attention spans, and difficulty maintaining deep, meaningful relationships. The algorithmic curation of content creates filter bubbles that reinforce existing beliefs rather than encouraging critical thinking. Furthermore, the pressure to maintain a curated online identity often leads to unhealthy comparisons and diminished self-esteem.\n\nIn my view, the solution is not to abandon social media entirely but to develop stronger digital literacy skills. Schools should teach students to evaluate information critically, manage their screen time consciously, and use these powerful tools responsibly rather than being used by them.",
                "word_count": 150,
                "key_features": ["Clear thesis", "Balanced argument", "Evidence references", "Personal stance", "Practical conclusion"]
            }
        ],
        4: [
            {
                "type": "Biographical Narrative",
                "topic": "A historical figure using multiple tenses",
                "model": "Marie Curie remains one of the most influential scientists in history. Born in Warsaw in 1867, she grew up in a Poland that was under Russian occupation and had limited educational opportunities for women. Despite these obstacles, she had been studying secretly at an underground university before she moved to Paris in 1891 to pursue her education at the Sorbonne.\n\nBy the time she completed her doctoral thesis in 1903, Curie had already discovered two new elements: polonium and radium. She was awarded the Nobel Prize in Physics that same year, which she shared with her husband Pierre and Henri Becquerel. She would go on to win a second Nobel Prize in 1911, this time in Chemistry, making her the first person ever to have received Nobel Prizes in two different scientific fields.\n\nToday, researchers are still building upon the foundations that Curie established, and her legacy will continue to inspire future generations of scientists who are working to expand the boundaries of human knowledge.",
                "word_count": 163,
                "key_features": ["Multiple tenses (8+)", "Chronological flow", "Time markers", "Natural tense transitions", "Historical accuracy"]
            }
        ],
        5: [
            {
                "type": "Comparative Literary Essay",
                "topic": "Universal themes across cultures",
                "model": "The theme of the individual's struggle against societal expectations appears with remarkable consistency across world literature, yet each cultural tradition approaches it from a distinctive perspective. In Charlotte Bronte's Jane Eyre, the protagonist's resistance to Victorian social constraints is framed as a deeply personal quest for moral and emotional independence. Jane's famous declaration that she is 'a free human being with an independent will' reflects Western Enlightenment ideals of individual autonomy.\n\nBy contrast, Chinua Achebe's Things Fall Apart explores a similar tension through the lens of communal African society. Okonkwo's struggle is not simply personal but represents the collision between traditional Igbo values and colonial modernity. His tragedy lies not in asserting individual will but in the destruction of the collective identity that gave his life meaning.\n\nWhat these works share is the conviction that authentic selfhood requires courage, whether that courage is directed towards personal liberation or communal preservation. Together, they remind us that the human desire for dignity and meaning transcends all cultural boundaries.",
                "word_count": 160,
                "key_features": ["Clear comparative structure", "Textual evidence", "Cultural context", "Analytical depth", "Unified conclusion"]
            }
        ],
        6: [
            {
                "type": "Problem-Solution Essay",
                "topic": "Addressing educational inequality globally",
                "model": "Educational inequality remains one of the most significant barriers to global development, with approximately 260 million children worldwide currently out of school. This crisis perpetuates cycles of poverty, limits economic growth, and undermines social cohesion in communities across every continent. The causes are complex, ranging from inadequate government funding and teacher shortages to cultural barriers and the devastating impact of conflict on educational infrastructure.\n\nAddressing this challenge requires a multi-layered approach. Firstly, international organisations and wealthy nations must increase funding for education in developing countries, prioritising teacher training and infrastructure development. Secondly, technology can play a transformative role through digital learning platforms that provide quality educational content to remote communities. Thirdly, local solutions must be developed in consultation with the communities they serve, respecting cultural contexts while ensuring that all children, regardless of gender, ethnicity, or socioeconomic status, have access to quality education.\n\nUltimately, investing in global education is not merely a moral obligation but an economic imperative that benefits every nation.",
                "word_count": 155,
                "key_features": ["Statistical evidence", "Clear problem definition", "Multi-layered solutions", "Academic register", "Strong concluding argument"]
            }
        ],
        7: [
            {
                "type": "Research Summary",
                "topic": "A scientific experiment on water filtration",
                "model": "This study investigated the effectiveness of a low-cost water filtration system using locally available materials for potential deployment in rural communities lacking modern water treatment infrastructure. It was hypothesised that a three-layer system combining activated charcoal, graded sand, and a plant-cellulose bio-membrane could remove at least ninety-five percent of common water contaminants while maintaining a practical flow rate.\n\nThe filtration prototype was tested over a four-week period using water samples collected from three different sources with varying contamination levels. Water quality was measured using an Arduino-based sensor array that monitored clarity, pH levels, and bacterial contamination rates at fifteen-minute intervals. After seventeen design iterations, the final prototype achieved a contaminant removal rate of ninety-seven percent at a flow rate of two litres per minute.\n\nThese findings suggest that effective water filtration can be achieved using affordable, accessible materials. The implications are significant for public health in communities where commercial filtration systems are prohibitively expensive. Further research should examine the system's long-term durability and maintenance requirements.",
                "word_count": 162,
                "key_features": ["Scientific structure (aim, method, results, implications)", "Passive voice", "Precise data", "Objective tone", "Suggestions for further research"]
            }
        ],
        8: [
            {
                "type": "Critical Review",
                "topic": "Reviewing a multimedia art installation",
                "model": "The student exhibition 'Crossing Boundaries,' created by Hazal Korkmaz and Burak Arslan, represents a remarkably mature exploration of cultural identity in a globalised world. The installation guides visitors through a corridor where visual art and original music interact to create an immersive journey from tradition to modernity.\n\nHazal's paintings demonstrate sophisticated technique, beginning with Ottoman-inspired calligraphy in deep indigo and gold before gradually incorporating urban and digital imagery. The transitions between traditional and contemporary elements are handled with subtlety, avoiding the jarring contrasts that often weaken similar attempts. Burak's accompanying compositions mirror this progression convincingly, though certain electronic sections in the middle passage could benefit from greater dynamic variation.\n\nThe installation's greatest strength is its insistence that tradition and modernity are not opposing forces but points on a continuous spectrum of cultural evolution. By engaging both visual and auditory senses simultaneously, the work achieves an emotional depth that neither medium could accomplish independently. This is collaborative art at its most effective.",
                "word_count": 155,
                "key_features": ["Evaluative thesis", "Specific evidence", "Balanced critique", "Arts vocabulary", "Justified conclusion"]
            }
        ],
        9: [
            {
                "type": "Proposal",
                "topic": "School wellness programme initiative",
                "model": "I propose the establishment of a comprehensive Student Wellness Programme at our school, addressing the four interconnected pillars of adolescent health: nutrition, physical activity, sleep, and mental well-being. A recent survey of two hundred students revealed that only twenty-two percent achieve recommended sleep levels, forty percent skip breakfast regularly, and sixty-five percent report experiencing significant academic stress.\n\nThe programme would include four core components. First, weekly nutrition workshops conducted in partnership with the school canteen to promote healthier meal options. Second, a daily fifteen-minute guided movement session incorporated into the morning routine. Third, a sleep hygiene awareness campaign providing evidence-based strategies for improving sleep quality. Fourth, a peer support network of trained student wellness ambassadors available for confidential conversations.\n\nImplementation would begin with a pilot phase during the spring semester, with effectiveness measured through pre- and post-programme surveys assessing self-reported well-being, sleep duration, and stress levels. Based on preliminary research from similar programmes, we anticipate a fifteen to twenty percent improvement in reported well-being scores.",
                "word_count": 158,
                "key_features": ["Clear rationale with data", "Specific components", "Measurable objectives", "Implementation timeline", "Evidence-based predictions"]
            }
        ],
        10: [
            {
                "type": "Argumentative Essay",
                "topic": "Individual action versus systemic change for environmental protection",
                "model": "The debate over whether individual behaviour change or systemic policy reform is more effective in addressing environmental challenges presents a false dichotomy. Both approaches are essential, and neither can succeed without the other. Individual actions such as reducing energy consumption, minimising waste, and making sustainable purchasing decisions are valuable not only for their direct environmental impact but also for their role in shifting cultural norms and creating political demand for systemic change.\n\nHowever, individual action alone is clearly insufficient to address challenges of the scale and complexity we currently face. The hundred largest corporations are responsible for approximately seventy-one percent of global greenhouse gas emissions, a statistic that demonstrates the limitations of placing environmental responsibility primarily on individual consumers. Meaningful progress requires government regulation, international agreements, corporate accountability, and massive investment in renewable energy infrastructure.\n\nThe most effective approach combines both levels of action. Informed, environmentally conscious citizens who make sustainable choices in their daily lives are also more likely to vote for environmental policies, support sustainable businesses, and hold corporations accountable. Individual and systemic change are not alternatives but mutually reinforcing elements of a comprehensive environmental strategy.",
                "word_count": 175,
                "key_features": ["Nuanced thesis rejecting false dichotomy", "Statistical evidence", "Balanced analysis", "Logical argumentation", "Synthesised conclusion"]
            }
        ]
    }
}

# ===========================================================================
# PRONUNCIATION_BANK
# ===========================================================================
PRONUNCIATION_BANK = {
    9: {
        1: {"focus": "Sentence stress and rhythm", "explanation": "English is a stress-timed language. Content words (nouns, verbs, adjectives) are stressed, while function words (articles, prepositions) are reduced. This creates a natural rhythm in speech.", "examples": ["I WENT to the SHOP to BUY some BREAD.", "She's STUDYing for her FINAL exAMS.", "The TEACHER gave us a LOT of HOMEwork.", "We NEED to FINISH the proJECT by FRIday.", "MOST stuDENTS preFER group WORK.", "They've been WAITing for the reSULTS all WEEK."], "tongue_twister": "She sells sea shells by the sea shore, and the shells she sells are sea shells, I'm sure.", "practice_words": ["education", "examination", "university", "curriculum", "certificate", "academic", "scholarship", "registration"]},
        2: {"focus": "Word stress in multi-syllable words", "explanation": "In words with three or more syllables, identifying the stressed syllable is crucial for intelligibility. Suffixes like -tion, -sion, -ity shift stress to the preceding syllable.", "examples": ["perSONality (stress on 3rd syllable)", "iDENtity (stress on 2nd syllable)", "charACteristic (stress on 3rd syllable)", "indiVIDual (stress on 3rd syllable)", "deTERmination (stress on 4th syllable)", "reSPONsibility (stress on 4th syllable)"], "tongue_twister": "Peter's personality is particularly pleasant, presenting persistent positivity.", "practice_words": ["personality", "identity", "characteristic", "determination", "responsibility", "independence", "confidence", "introvert"]},
        3: {"focus": "Connected speech: linking and elision", "explanation": "In natural speech, words link together. Consonant-to-vowel linking (turn_it_off), consonant elision (las' night), and vowel-to-vowel linking with /w/ or /j/ are common features.", "examples": ["turn it off -> tur-ni-toff", "last night -> las' night", "go away -> go/w/away", "the end -> thee/y/end", "want to -> wanna (informal)", "going to -> gonna (informal)"], "tongue_twister": "Can you can a can as a canner can can a can?", "practice_words": ["connected", "natural", "informal", "reduction", "linking", "elision", "contraction", "fluency"]},
        4: {"focus": "Intonation patterns in questions", "explanation": "Yes/no questions typically rise at the end, while wh-questions fall. Tag questions rise when seeking confirmation but fall when expecting agreement. These patterns convey different meanings.", "examples": ["Have you finished? (rising)", "What time is it? (falling)", "She's coming, isn't she? (falling = expecting yes)", "You like coffee, don't you? (rising = genuinely asking)", "Could you help me? (rising = polite request)", "Where did you go? (falling = wh-question)"], "tongue_twister": "Would you, could you, should you? Who would, who could, who should?", "practice_words": ["intonation", "emphasis", "confirmation", "interrogative", "rhetorical", "clarification", "assertion", "uncertainty"]},
        5: {"focus": "Vowel sounds: /ae/ vs /e/ vs /i:/", "explanation": "Distinguishing between short and long vowels is essential. The vowel in 'man' /ae/ differs from 'men' /e/ and 'mean' /i:/. Minimal pairs help train the ear.", "examples": ["man /ae/ vs men /e/ vs mean /i:/", "bad /ae/ vs bed /e/ vs bead /i:/", "sat /ae/ vs set /e/ vs seat /i:/", "pan /ae/ vs pen /e/ vs peen /i:/", "had /ae/ vs head /e/ vs heed /i:/", "bat /ae/ vs bet /e/ vs beat /i:/"], "tongue_twister": "A big black bear sat on a big black rug and read a really interesting book.", "practice_words": ["literature", "character", "metaphor", "narrative", "allegory", "genre", "aesthetic", "heritage"]},
        6: {"focus": "Consonant clusters", "explanation": "English has complex consonant clusters at the beginning and end of words. Clusters like /str/, /spl/, /sks/ require careful articulation. Many learners insert vowels between consonants.", "examples": ["strengths /streNkTs/ - 3 consonants at start, 4 at end", "scripts /skrIpts/ - 3+3 cluster", "splashed /splaeSt/ - 3+2 cluster", "twelfths /twelfTs/ - complex ending", "glimpsed /glImpst/ - complex ending", "texts /teksts/ - 4 final consonants"], "tongue_twister": "Strange strategic strikes struck strongly across the sprawling streets.", "practice_words": ["globalisation", "infrastructure", "exploitation", "sustainability", "industrialisation", "entrepreneurship", "discrimination", "unprecedented"]},
        7: {"focus": "Weak forms and schwa /e/", "explanation": "The schwa /e/ is the most common vowel sound in English. Function words like 'to', 'for', 'can', 'of' often reduce to schwa in connected speech. Using weak forms makes speech more natural.", "examples": ["I can /ken/ do it vs I CAN /kaen/ do it (emphasis)", "to /te/ the shop vs TO /tu:/ be or not TO /tu:/ be", "for /fe/ you vs What FOR /fo:/?", "of /ev/ course", "from /frem/ London", "was /wez/ happy"], "tongue_twister": "A cup of coffee for the professor from the office across the corridor.", "practice_words": ["innovation", "scientific", "technology", "experiment", "hypothesis", "laboratory", "discovery", "petroleum"]},
        8: {"focus": "Expressive intonation", "explanation": "Intonation conveys emotion and attitude. A wider pitch range expresses enthusiasm or surprise. A narrow range can sound bored or serious. Practising different emotions with the same sentence develops expressive speaking.", "examples": ["That's amazing! (wide rise = genuine excitement)", "That's amazing. (flat = sarcastic)", "Really? (high rise = surprised)", "Really. (fall = unimpressed)", "I love this painting! (enthusiastic)", "I love this painting. (contemplative)"], "tongue_twister": "How much wood would a woodchuck chuck if a woodchuck could chuck wood with wonderful artistic expression?", "practice_words": ["expression", "aesthetic", "interpretation", "contemporary", "masterpiece", "composition", "perspective", "abstract"]},
        9: {"focus": "Medical and scientific terminology pronunciation", "explanation": "Medical and scientific terms often derive from Greek or Latin. Understanding common roots helps with pronunciation: -ology (study of), -itis (inflammation), -emia (blood condition). Stress usually falls before the suffix.", "examples": ["epiDEMiology (stress before -ology)", "imMUnity (stress on 2nd syllable)", "pharMAceutical (stress on 3rd syllable)", "diAGnosis (stress on 2nd syllable)", "theraPEUtic (stress on 3rd syllable)", "epIDEMic vs panDEMic"], "tongue_twister": "The physician's pharmaceutical prescription was particularly precise and therapeutically thorough.", "practice_words": ["epidemiology", "pharmaceutical", "therapeutic", "diagnosis", "vaccination", "antibiotic", "cardiovascular", "neurological"]},
        10: {"focus": "Formal presentation delivery", "explanation": "Academic presentations require clear articulation, appropriate pacing, strategic pausing, and varied intonation. Signpost language should be stressed to guide listeners through the argument.", "examples": ["FIRSTly, I'd like to DRAW your atTENtion to... (stress signpost)", "MOREover, the eVIdence sugGESTS... (pause after moreover)", "In conCLUsion, ... (slow, deliberate pace)", "Let me TURN now to my SECOND point. (stress transitions)", "As you can SEE from this GRAPH... (stress visual reference)", "To SUM up, THERE are THREE key FINDings. (stress numbers)"], "tongue_twister": "The thoughtful thesis thoroughly examined three theoretical frameworks through thematic analysis.", "practice_words": ["sustainability", "infrastructure", "renewable", "biodegradable", "deforestation", "conservation", "photovoltaic", "ecosystem"]}
    }
}

# ===========================================================================
# WORKBOOK_BANK
# ===========================================================================
WORKBOOK_BANK = {
    9: {
        1: {"exercises": [
            {"type": "fill", "instruction": "Complete with the correct tense.", "items": ["I ___ (study) at this school for three years now. (have been studying)", "She ___ (finish) her homework before dinner yesterday. (had finished)", "By next June, we ___ (complete) the course. (will have completed)", "He ___ (read) when the phone rang. (was reading)", "They ___ (live) in Ankara since 2018. (have lived)", "If I ___ (know), I would have told you. (had known)"]},
            {"type": "transform", "instruction": "Rewrite using the word in brackets.", "items": ["I started learning English five years ago. (FOR) -> I have been learning English for five years.", "She finished her work, then she went out. (AFTER) -> After she had finished her work, she went out.", "They will arrive before we leave. (BY THE TIME) -> By the time we leave, they will have arrived.", "He didn't study, so he failed. (IF) -> If he had studied, he wouldn't have failed.", "We moved here in 2020. (SINCE) -> We have lived here since 2020."]},
            {"type": "error", "instruction": "Find and correct the error in each sentence.", "items": ["She has been working here since five years. -> for five years", "I wish I can speak French fluently. -> could speak", "The report was wrote by the committee. -> was written", "He must has forgotten about the meeting. -> must have forgotten", "If I would have known, I would have come. -> If I had known"]},
            {"type": "choose", "instruction": "Choose the correct option.", "items": ["By next year, she will finish / will have finished her degree.", "I wish I was / were taller.", "The building has been / was built in 1990.", "He might have / might has left early.", "If she had studied, she would pass / would have passed."]},
            {"type": "write", "instruction": "Write sentences using the prompts.", "items": ["school life / present perfect continuous", "a past regret / wish + past perfect", "a prediction / will + have + past participle", "a rule at school / must / mustn't", "something uncertain / might + have + past participle"]}
        ]},
        2: {"exercises": [
            {"type": "fill", "instruction": "Complete with a suitable adjective or adverb.", "items": ["She is extremely ___ and always helps others. (kind/generous)", "He speaks ___ and clearly in presentations. (confidently)", "The ___ student won the debate competition. (determined)", "She is ___ shy but very talented. (somewhat)", "He approached the problem ___. (analytically)", "The results were ___ impressive. (remarkably)"]},
            {"type": "match", "instruction": "Match personality adjectives with definitions.", "items": ["resilient - able to recover from difficulties", "empathetic - understanding others' feelings", "assertive - confident in expressing opinions", "conscientious - careful and thorough", "versatile - able to adapt to many functions", "pragmatic - dealing with things practically"]},
            {"type": "transform", "instruction": "Change the word form as indicated.", "items": ["confident (noun) -> confidence", "creative (noun) -> creativity", "determine (adjective) -> determined", "analyse (noun) -> analysis", "independent (noun) -> independence", "responsible (noun) -> responsibility"]},
            {"type": "choose", "instruction": "Choose the correct word.", "items": ["She's very sensible / sensitive about criticism.", "He's an economic / economical shopper.", "The test was quite hard / hardly.", "I could hard / hardly believe the news.", "She's a very respectable / respectful student."]},
            {"type": "write", "instruction": "Describe personality traits.", "items": ["Describe yourself using 5 personality adjectives with examples.", "Write about someone you admire and their qualities.", "Compare two people's personalities using contrast linkers.", "Describe your ideal leader's personality.", "Write about how your personality has changed over the years."]}
        ]},
        3: {"exercises": [
            {"type": "fill", "instruction": "Complete with appropriate communication vocabulary.", "items": ["Social media has ___ the way we communicate. (transformed)", "Many people prefer ___ communication over face-to-face. (digital)", "Effective communication requires active ___. (listening)", "Body language is a form of ___ communication. (non-verbal)", "Miscommunication can lead to ___. (misunderstandings)", "Email remains a ___ tool in professional settings. (vital)"]},
            {"type": "match", "instruction": "Match communication terms with examples.", "items": ["formal register - Dear Sir/Madam", "informal register - Hey, what's up?", "passive voice - The email was sent yesterday", "hedging - It might be worth considering", "discourse marker - Furthermore, the evidence suggests", "euphemism - He passed away (instead of died)"]},
            {"type": "rewrite", "instruction": "Change from informal to formal register.", "items": ["Hey, can you send me that stuff? -> Dear colleague, could you kindly forward the relevant documents?", "That idea's rubbish. -> I'm afraid I have reservations about that proposal.", "We gotta finish this ASAP. -> It is imperative that we complete this at the earliest opportunity.", "Thanks a bunch! -> I greatly appreciate your assistance.", "I reckon we should try something else. -> I would suggest we consider an alternative approach."]},
            {"type": "error", "instruction": "Identify the communication barrier.", "items": ["Texting during a face-to-face conversation -> not listening / distraction", "Using jargon with a non-specialist audience -> language barrier", "Sending an angry email immediately -> emotional barrier", "Assuming everyone uses the same social media -> digital divide", "Speaking too fast in a presentation -> pace/clarity barrier"]},
            {"type": "write", "instruction": "Write about communication.", "items": ["Compare face-to-face and digital communication advantages.", "Write formal and informal versions of the same message.", "Describe how communication has changed in the last 20 years.", "Write about a time when miscommunication caused a problem.", "Propose rules for effective online communication."]}
        ]},
        4: {"exercises": [
            {"type": "fill", "instruction": "Complete with the correct tense form.", "items": ["She ___ (work) here since 2015. (has been working)", "By the time I arrived, they ___ (leave). (had left)", "This time next year, I ___ (study) at university. (will be studying)", "I wish I ___ (pay) attention in class. (had paid)", "If only she ___ (tell) me earlier. (had told)", "He ___ (must/forget) about the deadline. (must have forgotten)"]},
            {"type": "transform", "instruction": "Rewrite using the structure in brackets.", "items": ["People believe he is innocent. (PASSIVE) -> He is believed to be innocent.", "They say the company is bankrupt. (IT) -> It is said that the company is bankrupt.", "I regret not studying harder. (WISH) -> I wish I had studied harder.", "It's possible that she missed the train. (MIGHT) -> She might have missed the train.", "The fact that he lied shocked everyone. (WHAT) -> What shocked everyone was the fact that he lied."]},
            {"type": "error", "instruction": "Correct the grammatical error.", "items": ["I used to living in a small town. -> used to live", "She suggested me to take a break. -> suggested that I take / suggested taking", "Despite of the rain, we went out. -> Despite the rain", "He denied to steal the money. -> denied stealing", "The more harder you work, the better. -> The harder"]},
            {"type": "choose", "instruction": "Select the correct option.", "items": ["I'd rather you didn't / don't tell anyone.", "It's high time we left / leave.", "Hardly had I arrived when / than the meeting started.", "Not only did she win / she won the prize, but she also set a record.", "Were I to know / If I would know the answer, I would tell you."]},
            {"type": "write", "instruction": "Write complex sentences.", "items": ["Use an inverted conditional about a past regret.", "Write a sentence using a cleft structure for emphasis.", "Use 'hardly...when' to describe a surprising event.", "Write a mixed conditional about a past decision affecting the present.", "Use a reduced relative clause in a formal sentence."]}
        ]},
        5: {"exercises": [
            {"type": "fill", "instruction": "Complete with literary terms.", "items": ["A ___ is a comparison using 'like' or 'as'. (simile)", "The use of symbols to represent ideas is called ___. (symbolism)", "A story within a story is a ___ narrative. (frame/embedded)", "The ___ is the central message of a literary work. (theme)", "Writing from a character's perspective uses ___ person narration. (first)", "___ is the use of hints about future events. (Foreshadowing)"]},
            {"type": "match", "instruction": "Match literary devices with examples.", "items": ["metaphor - Life is a journey.", "personification - The wind whispered through the trees.", "irony - A fire station burns down.", "alliteration - Peter Piper picked a peck of pickled peppers.", "hyperbole - I've told you a million times.", "oxymoron - deafening silence"]},
            {"type": "analyse", "instruction": "Identify the literary device used.", "items": ["The old man's eyes were deep oceans of wisdom. -> metaphor", "It was the best of times, it was the worst of times. -> antithesis/parallel structure", "The leaves danced in the autumn breeze. -> personification", "She carried the weight of the world on her shoulders. -> hyperbole/metaphor", "The calm before the storm. -> foreshadowing/idiom"]},
            {"type": "choose", "instruction": "Choose the correct literary term.", "items": ["An unexpected twist is an example of irony / symbolism.", "Comparing two unlike things without 'like' or 'as' is a metaphor / simile.", "A recurring image or idea is a motif / plot.", "The narrator who knows everything is omniscient / limited.", "The emotional atmosphere of a text is its mood / theme."]},
            {"type": "write", "instruction": "Write about literature.", "items": ["Analyse a short poem using three literary devices.", "Compare two authors' writing styles.", "Write a paragraph using at least 3 literary devices.", "Discuss how setting contributes to mood in a novel you've read.", "Write a book review of 150 words for a novel you've read."]}
        ]},
        6: {"exercises": [
            {"type": "fill", "instruction": "Complete with global issues vocabulary.", "items": ["Climate change is one of the biggest ___ facing humanity. (challenges)", "Poverty ___ affects millions of children worldwide. (disproportionately)", "Sustainable ___ aims to meet present needs without compromising the future. (development)", "Access to clean water is a basic human ___. (right)", "International ___ is essential for solving global problems. (cooperation)", "Income ___ has increased in many countries. (inequality)"]},
            {"type": "match", "instruction": "Match organisations with their missions.", "items": ["WHO - global public health", "UNICEF - children's welfare", "UNESCO - education and culture", "UNHCR - refugee protection", "WTO - international trade regulation", "IMF - global financial stability"]},
            {"type": "rewrite", "instruction": "Express the same idea more formally.", "items": ["Lots of people don't have enough food. -> A significant proportion of the global population lacks adequate nutrition.", "Rich countries should help poor ones. -> Developed nations have an obligation to support developing countries.", "Things are getting worse. -> The situation is deteriorating.", "We need to do something fast. -> Urgent action is imperative.", "Nobody cares about this problem. -> This issue receives insufficient attention."]},
            {"type": "choose", "instruction": "Choose the correct word.", "items": ["The crisis has had a devastating / devastated effect.", "There has been a significant rise / raise in temperatures.", "The policy aims to reduce / deduce poverty.", "Many countries are economic / economically disadvantaged.", "Global warming affects / effects the entire planet."]},
            {"type": "write", "instruction": "Write about global issues.", "items": ["Argue for or against: 'Individual actions can solve climate change.'", "Write a formal letter to a world leader about a global issue.", "Compare two approaches to reducing poverty.", "Propose three solutions for improving global education access.", "Write a persuasive paragraph on why international cooperation matters."]}
        ]},
        7: {"exercises": [
            {"type": "fill", "instruction": "Complete with science and innovation vocabulary.", "items": ["The scientist conducted an ___ to test the hypothesis. (experiment)", "Artificial ___ is transforming many industries. (intelligence)", "The ___ of penicillin saved millions of lives. (discovery)", "Renewable ___ sources include solar and wind power. (energy)", "Gene ___ raises ethical questions about modifying DNA. (editing)", "The research was published in a peer-___ journal. (reviewed)"]},
            {"type": "match", "instruction": "Match inventions with their impact.", "items": ["printing press - spread of knowledge", "antibiotics - treatment of infections", "internet - global communication", "telescope - understanding of space", "vaccine - disease prevention", "transistor - modern electronics"]},
            {"type": "transform", "instruction": "Nominalise the verbs.", "items": ["They discovered a new element. -> The discovery of a new element was significant.", "Scientists innovated rapidly. -> Rapid innovation characterised the period.", "The company developed new software. -> The development of new software was announced.", "Researchers investigated the cause. -> The investigation into the cause began.", "They implemented the new system. -> The implementation of the new system started."]},
            {"type": "choose", "instruction": "Choose the correct scientific term.", "items": ["A prediction that can be tested is a hypothesis / theory.", "The results section presents / analyses the data.", "A variable that is changed is the independent / dependent variable.", "Repeating an experiment tests its reliability / validity.", "Drawing conclusions from data is inductive / deductive reasoning."]},
            {"type": "write", "instruction": "Write about science.", "items": ["Describe the most important invention of the last century.", "Argue whether AI will create more jobs or destroy them.", "Write about an ethical dilemma in modern science.", "Compare two renewable energy technologies.", "Propose a scientific solution to a local problem."]}
        ]},
        8: {"exercises": [
            {"type": "fill", "instruction": "Complete with art vocabulary.", "items": ["The artist used warm ___ to create a sense of comfort. (colours/tones)", "This ___ was painted during the Renaissance period. (masterpiece)", "The sculpture was made from recycled ___. (materials)", "Her work is displayed in a modern art ___. (gallery)", "The ___ of the painting draws the viewer's eye to the centre. (composition)", "Abstract art does not attempt to ___ reality. (represent)"]},
            {"type": "match", "instruction": "Match art movements with descriptions.", "items": ["Impressionism - capturing light and atmosphere", "Cubism - multiple perspectives simultaneously", "Surrealism - dream-like imagery", "Minimalism - simplicity and essential forms", "Pop Art - popular culture imagery", "Expressionism - emotional experience over reality"]},
            {"type": "transform", "instruction": "Change to passive voice.", "items": ["Picasso painted Guernica in 1937. -> Guernica was painted by Picasso in 1937.", "The gallery displays contemporary art. -> Contemporary art is displayed by the gallery.", "Critics praised the exhibition. -> The exhibition was praised by critics.", "They will restore the fresco next year. -> The fresco will be restored next year.", "Artists have used this technique for centuries. -> This technique has been used by artists for centuries."]},
            {"type": "choose", "instruction": "Choose the correct word.", "items": ["The painting evokes / invokes a feeling of sadness.", "Her artistic / artful use of colour is remarkable.", "The exhibition features / feats works from the 19th century.", "The portrait is very life-like / living.", "He is a very imaginary / imaginative artist."]},
            {"type": "write", "instruction": "Write about art.", "items": ["Describe a painting or artwork that moved you.", "Compare two different art movements.", "Argue whether photography is an art form.", "Write a gallery review of an exhibition.", "Discuss how art reflects society."]}
        ]},
        9: {"exercises": [
            {"type": "fill", "instruction": "Complete with health vocabulary.", "items": ["Regular exercise improves both physical and ___ health. (mental)", "A balanced ___ includes proteins, carbohydrates and vitamins. (diet)", "Stress can weaken the ___ system. (immune)", "___ is as important as physical health. (Mental wellbeing)", "Getting enough ___ is essential for cognitive function. (sleep)", "Preventive medicine focuses on ___ rather than cure. (prevention)"]},
            {"type": "match", "instruction": "Match health terms.", "items": ["sedentary - involving little physical activity", "holistic - treating the whole person", "chronic - lasting a long time", "acute - severe but short-lasting", "rehabilitate - restore to health", "prognosis - likely course of a disease"]},
            {"type": "rewrite", "instruction": "Make recommendations using different structures.", "items": ["Eat more vegetables. -> It is advisable to increase vegetable consumption.", "Exercise regularly. -> Regular exercise is strongly recommended.", "Don't skip meals. -> Skipping meals should be avoided.", "Get 8 hours of sleep. -> It is essential to obtain adequate sleep.", "Reduce screen time. -> A reduction in screen time is recommended."]},
            {"type": "choose", "instruction": "Choose the correct word.", "items": ["A healthy / healthful lifestyle includes regular exercise.", "The disease is highly contagious / contiguous.", "She made a full recover / recovery.", "Stress can effect / affect your immune system.", "The doctor prescribed / proscribed medication."]},
            {"type": "write", "instruction": "Write about health.", "items": ["Compare traditional and modern approaches to healthcare.", "Write advice for managing exam stress.", "Discuss the relationship between mental and physical health.", "Propose a school wellness programme.", "Argue for or against mandatory physical education."]}
        ]},
        10: {"exercises": [
            {"type": "fill", "instruction": "Complete with environmental vocabulary.", "items": ["Carbon ___ from vehicles contribute to air pollution. (emissions)", "Deforestation leads to loss of ___. (biodiversity)", "Renewable energy sources are more ___ than fossil fuels. (sustainable)", "The ___ footprint measures environmental impact. (carbon/ecological)", "___ energy includes solar, wind and hydroelectric power. (Renewable)", "Ocean ___ threatens marine ecosystems. (acidification/pollution)"]},
            {"type": "match", "instruction": "Match environmental terms.", "items": ["biodegradable - breaks down naturally", "renewable - can be replenished", "ecosystem - community of living organisms", "carbon neutral - zero net CO2 emissions", "conservation - protection of natural resources", "sustainability - meeting needs without depleting resources"]},
            {"type": "transform", "instruction": "Change to more academic register.", "items": ["Trees clean the air. -> Arboreal vegetation purifies atmospheric conditions.", "Pollution kills fish. -> Aquatic fauna mortality results from environmental contamination.", "People waste too much water. -> Excessive water consumption represents a significant concern.", "Cars produce harmful gases. -> Vehicular emissions generate detrimental atmospheric pollutants.", "We need to recycle more. -> An increase in recycling rates is imperative."]},
            {"type": "choose", "instruction": "Choose the correct term.", "items": ["Global warming / heating is caused by greenhouse gases.", "We should reduce / reuse / recycle where possible. (all three)", "Fossil fuels are non-renewable / unrenewable resources.", "The ozone layer / level protects us from UV radiation.", "Organic farming avoids synthetic / sympathetic chemicals."]},
            {"type": "write", "instruction": "Write about the environment.", "items": ["Propose three actions your school can take to be greener.", "Write a formal letter to local government about an environmental issue.", "Compare solar and wind energy advantages and disadvantages.", "Discuss whether economic growth and environmental protection can coexist.", "Write a persuasive essay on the importance of biodiversity conservation."]}
        ]}
    }
}

# ===========================================================================
# TURKEY_CORNER_BANK
# ===========================================================================
TURKEY_CORNER_BANK = {
    9: {
        1: {"title": "Turkish Education System", "text": "Turkey's education system serves over 18 million students across primary, secondary and higher education levels. The system underwent significant reform in 2012 with the 4+4+4 structure. Turkish universities have gained international recognition, with several ranking among the world's top institutions. The country invests heavily in STEM education and has established science high schools across all provinces. Student exchange programmes like Erasmus connect Turkish students with European peers, fostering academic and cultural growth.", "image_desc": "Students at a modern Turkish science high school laboratory", "discussion_q": "How can education systems better prepare students for the challenges of the 21st century?"},
        2: {"title": "Turkish Youth Identity", "text": "Turkey's youth population represents a dynamic blend of traditional values and modern aspirations. Young Turks navigate between cultural heritage and global influences, creating a unique contemporary identity. Social media has given Turkish youth a powerful voice in cultural discourse. Young entrepreneurs, artists and activists are shaping Turkey's future while honouring its past. The concept of identity in Turkey is enriched by the country's position as a bridge between Eastern and Western cultures, making Turkish youth particularly adept at cross-cultural communication.", "image_desc": "Young Turkish professionals at a technology startup in Istanbul", "discussion_q": "How does cultural heritage influence personal identity formation?"},
        3: {"title": "Turkey's Digital Transformation", "text": "Turkey has embraced digital transformation across government, education and business. The e-Government portal provides citizens with access to hundreds of online services. Turkish startups like Trendyol, Peak Games and Getir have achieved global recognition. Istanbul's tech ecosystem is one of the fastest-growing in Europe. The government's Digital Turkey initiative aims to create a fully connected society by 2025. Turkish software developers and engineers work at major international technology companies, contributing to global innovation.", "image_desc": "Istanbul's technology hub with modern startup offices", "discussion_q": "What are the benefits and risks of rapid digital transformation?"},
        4: {"title": "Language and Literature in Turkey", "text": "Turkish is spoken by approximately 80 million people and belongs to the Turkic language family. The 1928 alphabet reform was one of the most revolutionary changes in the Republic's history, transitioning from Arabic script to Latin letters. Turkish literature spans from Divan poetry to contemporary fiction. Authors like Nazim Hikmet, Yasar Kemal and Orhan Pamuk have gained international acclaim. Turkey's rich oral tradition, including shadow puppet theatre (Karagoz) and storytelling (meddah), is preserved as UNESCO intangible cultural heritage.", "image_desc": "A collection of Turkish literary works from different periods", "discussion_q": "How does language shape the way we think and express ourselves?"},
        5: {"title": "Turkish Storytelling Traditions", "text": "Turkey has a rich tradition of storytelling that spans millennia. The epic of Dede Korkut, dating back to the 15th century, contains twelve tales of Oghuz Turks. Nasreddin Hodja's humorous stories teach wisdom through laughter and have spread across the Middle East and Central Asia. The meddah tradition of public storytelling combined entertainment with social commentary. Modern Turkish literature continues this narrative tradition, with contemporary authors weaving ancient themes into modern settings. Turkish television dramas have become a new form of storytelling, exported to over 150 countries.", "image_desc": "An illustration from the Dede Korkut epic manuscript", "discussion_q": "How do traditional stories remain relevant in the modern world?"},
        6: {"title": "Turkey's Humanitarian Role", "text": "Turkey hosts the world's largest refugee population, demonstrating its commitment to humanitarian values. The country has provided shelter, education and healthcare to millions of displaced people. Turkish humanitarian organisations like the Red Crescent and AFAD respond to natural disasters globally. Turkey's development aid agency TIKA operates in over 150 countries. The country's geographical position makes it a crucial partner in addressing migration, conflict resolution and regional stability. Turkey's humanitarian efforts reflect both its cultural tradition of hospitality and its role as a responsible global actor.", "image_desc": "Turkish Red Crescent workers providing aid", "discussion_q": "What responsibilities do countries have towards refugees and displaced people?"},
        7: {"title": "Turkish Innovation and R&D", "text": "Turkey has significantly increased its investment in research and development. Technology development zones across the country host thousands of companies and researchers. TUBITAK, the national research council, funds projects in science, technology and innovation. Turkish engineers have contributed to major international projects, including CERN's Large Hadron Collider. The country's first domestically built satellite, Turksat, and the TOGG electric vehicle project demonstrate growing technological capabilities. Turkey aims to become one of the world's top ten economies partly through science and innovation leadership.", "image_desc": "TUBITAK research centre with scientists at work", "discussion_q": "How important is investment in R&D for a country's economic development?"},
        8: {"title": "Contemporary Turkish Art Scene", "text": "Turkey's contemporary art scene is vibrant and internationally recognised. The Istanbul Biennial, established in 1987, attracts artists and collectors from around the world. Istanbul Modern, Turkey's first museum of modern and contemporary art, showcases both Turkish and international works. Young Turkish artists explore themes of identity, urbanisation and cultural hybridity through various media including installation, video and performance art. The art market in Turkey has grown substantially, with galleries in Istanbul, Ankara and Izmir gaining international reputations.", "image_desc": "Interior of Istanbul Modern art museum", "discussion_q": "How does contemporary art reflect social and political issues?"},
        9: {"title": "Health Tourism in Turkey", "text": "Turkey has emerged as a leading destination for health tourism, attracting over 700,000 international patients annually. World-class hospitals in Istanbul, Ankara and Antalya offer treatments in cardiology, oncology, ophthalmology and dental care at competitive prices. The country's thermal springs, particularly in Afyon and Bursa, have been used for therapeutic purposes for centuries. Turkey combines modern medical technology with traditional wellness practices like hammam culture. The government's Healthcare Tourism Development Programme has positioned Turkey among the top five health tourism destinations globally.", "image_desc": "Modern hospital facility in Istanbul with international patient wing", "discussion_q": "What are the advantages and challenges of health tourism?"},
        10: {"title": "Turkey's Green Future", "text": "Turkey has committed to achieving net-zero carbon emissions by 2053. The country's renewable energy capacity has grown rapidly, with wind farms along the Aegean coast and solar installations in southeastern Anatolia. Turkey has the world's fourth-largest geothermal energy reserves. The government has introduced incentives for electric vehicles and green building standards. Environmental awareness is growing, with youth-led initiatives promoting recycling, urban farming and sustainable consumption. Turkey's diverse geography provides exceptional potential for renewable energy development, positioning the country for a sustainable economic future.", "image_desc": "Wind turbines along the Turkish Aegean coast", "discussion_q": "How can Turkey balance economic growth with environmental sustainability?"}
    }
}

# ===========================================================================
# GAMIFICATION_BANK
# ===========================================================================
GAMIFICATION_BANK = {
    9: {
        "levels": [
            {"level": 1, "title": "Language Learner", "xp_needed": 0},
            {"level": 2, "title": "Critical Thinker", "xp_needed": 600},
            {"level": 3, "title": "Academic Writer", "xp_needed": 1500},
            {"level": 4, "title": "Research Scholar", "xp_needed": 3500},
            {"level": 5, "title": "English Master", "xp_needed": 6000},
        ],
        "unit_badges": {
            1: {"name": "Campus Navigator", "desc": "Discussed student life using a range of tenses."},
            2: {"name": "Identity Explorer", "desc": "Analysed personality and identity concepts."},
            3: {"name": "Digital Communicator", "desc": "Compared modern communication methods critically."},
            4: {"name": "Grammar Architect", "desc": "Mastered all twelve English tenses."},
            5: {"name": "Literary Analyst", "desc": "Analysed world literature using literary devices."},
            6: {"name": "Global Citizen", "desc": "Debated global issues with evidence-based arguments."},
            7: {"name": "Innovation Advocate", "desc": "Explored science and innovation topics in English."},
            8: {"name": "Art Critic", "desc": "Expressed opinions about art using expressive language."},
            9: {"name": "Wellness Champion", "desc": "Discussed health with appropriate medical vocabulary."},
            10: {"name": "Eco Warrior", "desc": "Proposed environmental solutions using academic English."},
        },
        "bonus_xp": [
            {"task": "Write a 300-word analytical essay", "xp": 200},
            {"task": "Give a 3-minute presentation on a research topic", "xp": 200},
            {"task": "Read an English novel and write a review", "xp": 250},
            {"task": "Lead a class discussion on a global issue", "xp": 150},
            {"task": "Create a vocabulary notebook with 100+ academic words", "xp": 100},
        ],
    }
}

# ===========================================================================
# MISSION_BANK
# ===========================================================================
MISSION_BANK = {
    9: {
        1: {"title": "Student Life Documentary", "objective": "Create a short documentary about student life.", "tasks": ["Interview 5 students about their daily routines.", "Write a script using a range of tenses.", "Record or present your documentary.", "Include statistics about student life."], "reward": "Filmmaker Badge + 200 XP"},
        2: {"title": "Personality Profile Portfolio", "objective": "Create detailed personality profiles.", "tasks": ["Complete a personality questionnaire.", "Research personality psychology theories.", "Write a 200-word self-analysis essay.", "Present your findings comparing profiles."], "reward": "Psychologist Badge + 200 XP"},
        3: {"title": "Communication Audit", "objective": "Analyse communication habits in your community.", "tasks": ["Survey 20 people about their communication methods.", "Create charts showing communication preferences by age.", "Write a report comparing findings.", "Propose guidelines for effective digital communication."], "reward": "Communication Expert Badge + 200 XP"},
        4: {"title": "Grammar Teaching Video", "objective": "Create an instructional video on a grammar topic.", "tasks": ["Choose a complex grammar topic.", "Write a clear explanation with examples.", "Create a 3-minute teaching video.", "Include practice exercises for viewers."], "reward": "Grammar Guru Badge + 200 XP"},
        5: {"title": "Literary Magazine", "objective": "Produce a class literary magazine.", "tasks": ["Write an original short story or poem.", "Write a review of a book you have read.", "Design a page layout for the magazine.", "Compile contributions into a class publication."], "reward": "Literary Editor Badge + 200 XP"},
        6: {"title": "Global Issues Conference", "objective": "Organise a mini-conference on global issues.", "tasks": ["Research a specific global issue in depth.", "Prepare a 5-minute conference presentation.", "Create an informative poster or handout.", "Participate in a Q&A session after presentations."], "reward": "Global Ambassador Badge + 200 XP"},
        7: {"title": "Innovation Showcase", "objective": "Present a scientific innovation that changed the world.", "tasks": ["Research the history and impact of your chosen innovation.", "Create a timeline of its development.", "Write a 250-word essay on its societal impact.", "Present with visual aids to the class."], "reward": "Innovation Scout Badge + 200 XP"},
        8: {"title": "Art Exhibition Guide", "objective": "Create an audio guide for an art exhibition.", "tasks": ["Select 8 artworks from different periods.", "Write descriptive commentary for each piece.", "Record your audio guide narration.", "Present your exhibition concept."], "reward": "Art Curator Badge + 200 XP"},
        9: {"title": "School Wellness Campaign", "objective": "Design a health and wellness campaign for your school.", "tasks": ["Research common health issues among teenagers.", "Design informational posters and leaflets.", "Write a persuasive article for the school magazine.", "Present your campaign plan to the class."], "reward": "Health Ambassador Badge + 200 XP"},
        10: {"title": "Environmental Action Plan", "objective": "Develop an actionable environmental plan for your school.", "tasks": ["Audit your school's environmental impact.", "Research best practices from eco-schools.", "Write a detailed action plan with timelines.", "Present your proposal to school administration."], "reward": "Eco Leader Badge + 200 XP"}
    }
}

# ===========================================================================
# STEAM_BANK
# ===========================================================================
STEAM_BANK = {
    9: {
        1: {"title": "Student Life Data Analysis", "subject_link": "Mathematics + Social Sciences", "activity": "Collect and analyse data about student daily routines.", "materials": ["survey forms", "spreadsheet software", "graph paper", "calculator"], "steps": ["Design a survey about daily time allocation.", "Collect data from at least 20 students.", "Calculate mean, median and mode for each activity.", "Create pie charts and bar graphs.", "Write an analytical report with conclusions."], "learning_outcome": "Apply statistical analysis to real-world social data."},
        2: {"title": "Psychology of Personality", "subject_link": "Psychology + English + Biology", "activity": "Explore the science behind personality traits.", "materials": ["personality questionnaires", "research articles", "presentation tools", "poster paper"], "steps": ["Research the Big Five personality model.", "Complete a personality assessment.", "Research the biological basis of personality.", "Create a visual presentation of your findings.", "Discuss nature vs nurture in personality development."], "learning_outcome": "Connect psychological theory with biological science."},
        3: {"title": "Communication Technology Timeline", "subject_link": "History + Technology + English", "activity": "Create a comprehensive timeline of communication technology.", "materials": ["research materials", "timeline template", "images", "presentation software"], "steps": ["Research communication from ancient to modern times.", "Identify 20 key milestones in communication technology.", "Create a visual timeline with descriptions.", "Analyse the rate of technological change.", "Present your timeline with commentary."], "learning_outcome": "Trace the historical development of communication technology."},
        4: {"title": "Linguistic Data Mining", "subject_link": "English + Mathematics + ICT", "activity": "Analyse language patterns using frequency data.", "materials": ["text samples", "word counter tool", "spreadsheet", "graph paper"], "steps": ["Collect text samples from different genres.", "Count word frequencies and sentence lengths.", "Calculate averages and create distributions.", "Compare patterns across genres.", "Write a report on your linguistic findings."], "learning_outcome": "Apply mathematical analysis to language study."},
        5: {"title": "Literature and Geography", "subject_link": "Literature + Geography + Art", "activity": "Map the geographical settings of literary works.", "materials": ["world map", "literary texts", "coloured pins", "summary cards"], "steps": ["Select 10 literary works from different countries.", "Map their settings on a world map.", "Research how geography influenced each work.", "Create visual cards connecting place and literature.", "Present geographical patterns in world literature."], "learning_outcome": "Explore the relationship between geography and literary creation."},
        6: {"title": "Global Issues Infographic", "subject_link": "Geography + Mathematics + Design", "activity": "Create data-driven infographics about global challenges.", "materials": ["global statistics", "design software or paper", "coloured markers", "ruler"], "steps": ["Choose a global issue and gather data.", "Design an infographic with clear visual hierarchy.", "Include accurate statistics and source citations.", "Use colour coding and icons effectively.", "Present and explain your infographic."], "learning_outcome": "Combine data literacy with visual design skills."},
        7: {"title": "Renewable Energy Experiment", "subject_link": "Physics + Environmental Science", "activity": "Build and test a simple solar or wind energy device.", "materials": ["small solar panel or motor", "LED lights", "wires", "cardboard"], "steps": ["Research how solar/wind energy is converted to electricity.", "Design a simple energy harvesting device.", "Build your prototype.", "Test and measure its output.", "Write a lab report with results and improvements."], "learning_outcome": "Apply physics principles to renewable energy technology."},
        8: {"title": "Art Analysis Through Mathematics", "subject_link": "Art + Mathematics", "activity": "Analyse mathematical principles in famous artworks.", "materials": ["art prints", "ruler", "protractor", "calculator"], "steps": ["Study the golden ratio and Fibonacci sequence.", "Identify these proportions in famous paintings.", "Measure and calculate ratios in artworks.", "Create an original composition using mathematical proportions.", "Present your analysis of maths in art."], "learning_outcome": "Discover mathematical structures underlying artistic beauty."},
        9: {"title": "Health Statistics Project", "subject_link": "Biology + Mathematics + Health", "activity": "Analyse health statistics and their implications.", "materials": ["health data sets", "spreadsheet software", "graph paper", "calculator"], "steps": ["Gather health statistics for Turkey and 3 other countries.", "Create comparative graphs and charts.", "Calculate rates and percentages.", "Analyse correlations between factors.", "Write a report with health recommendations."], "learning_outcome": "Apply statistical skills to public health data analysis."},
        10: {"title": "Carbon Footprint Calculator", "subject_link": "Environmental Science + Mathematics + ICT", "activity": "Calculate and compare carbon footprints.", "materials": ["carbon emission data", "calculator", "spreadsheet", "graph paper"], "steps": ["Research carbon emission factors for daily activities.", "Calculate your personal weekly carbon footprint.", "Compare with national and global averages.", "Identify the biggest contributors.", "Propose a reduction plan with measurable targets."], "learning_outcome": "Apply mathematical calculation to environmental impact assessment."}
    }
}

# ===========================================================================
# SONG_BANK
# ===========================================================================
SONG_BANK = {
    9: {
        1: {
            "title": "First Day Anthem",
            "lyrics": (
                "New halls, new faces, heart beating fast,\n"
                "Yesterday's comfort fading into the past.\n"
                "Timetables, lockers, a map in my hand,\n"
                "Trying to find where I'm supposed to stand.\n"
                "But every senior was a freshman once,\n"
                "Every expert started with a stumble and a stunt.\n"
                "So breathe in deep and take that step,\n"
                "This chapter's yours — no room for regret."
            ),
            "activity": "Students rewrite the second verse to reflect their own first-day experience. Perform as a spoken-word piece or rap in small groups."
        },
        2: {
            "title": "Mirror, Mirror (Identity Rap)",
            "lyrics": (
                "Mirror, mirror, who do you see?\n"
                "An introvert, extrovert, or something in between?\n"
                "Labels try to box me, put me on a shelf,\n"
                "But personality's a spectrum — I define myself.\n"
                "Quiet doesn't mean weak, loud doesn't mean strong,\n"
                "Every trait's a note in my personal song.\n"
                "So let the psychologists write their charts,\n"
                "I'll keep discovering all my parts."
            ),
            "activity": "Students write a personal identity verse using at least five personality adjectives from the unit vocabulary. Share in a class poetry slam."
        },
        3: {
            "title": "Connected (Digital Age Ballad)",
            "lyrics": (
                "We swipe, we scroll, we share, we post,\n"
                "Connected to the world from coast to coast.\n"
                "But are we really talking, face to face,\n"
                "Or hiding behind a screen in a digital space?\n"
                "A message sent is not a hand that's held,\n"
                "An emoji shared is not a story told.\n"
                "Let's bridge the gap between the click and care,\n"
                "True communication means we're truly there."
            ),
            "activity": "Students compose a response verse arguing for or against digital communication. Hold a class debate using their verses as opening statements."
        },
        4: {
            "title": "The Tense Traveller",
            "lyrics": (
                "I walked, I walk, I will walk on,\n"
                "Through past and present till the future's drawn.\n"
                "I had been dreaming when the clock struck three,\n"
                "I will have finished by the time you see.\n"
                "Twelve tenses spinning like a carousel,\n"
                "Each one a window, each one a spell.\n"
                "Simple, continuous, perfect, combined,\n"
                "The grammar of time lives inside my mind."
            ),
            "activity": "Students identify all twelve tenses in the lyrics and create their own verse using at least six different tenses correctly. Display as a Grammar Wall poster."
        },
        5: {
            "title": "Pages of the World",
            "lyrics": (
                "Open a book from a faraway land,\n"
                "Walk through its pages, take the author's hand.\n"
                "Magic and realism twist and turn,\n"
                "Every chapter holds a lesson to learn.\n"
                "From Lagos to Tokyo, Bogota to Rome,\n"
                "Every story is a doorway, every novel a home.\n"
                "So read beyond your borders, read beyond your street,\n"
                "The world is made of stories — let them make you complete."
            ),
            "activity": "Students choose a country from the lyrics and find a short story or poem from that culture. Present the piece and explain how it connects to the song's theme."
        },
        6: {
            "title": "One World (Global Issues Spoken Word)",
            "lyrics": (
                "One world, seven billion voices strong,\n"
                "But half are silenced — tell me, what went wrong?\n"
                "Poverty draws lines that maps don't show,\n"
                "Climate shifts the ground beneath our toes.\n"
                "We debate in classrooms, safe and warm,\n"
                "While somewhere else a child walks through a storm.\n"
                "Knowledge without action is a half-told tale,\n"
                "Our generation must not, will not, shall not fail."
            ),
            "activity": "Students research one global issue mentioned in the poem and write a four-line spoken-word extension. Perform as a class chain poem where each student adds their verse."
        },
        7: {
            "title": "Eureka Moment",
            "lyrics": (
                "A question asked, a theory born,\n"
                "Through trial and error, ideas are worn.\n"
                "Hypothesis, experiment, data, proof,\n"
                "Science lifts the world up through the roof.\n"
                "From filtered water to the stars above,\n"
                "Innovation starts with what we love.\n"
                "So tinker, test, and never stop,\n"
                "The next great breakthrough waits at every drop."
            ),
            "activity": "Students write a verse about a scientific innovation that changed daily life. Create a class Innovation Songbook with illustrations."
        },
        8: {
            "title": "Colours and Chords",
            "lyrics": (
                "A brushstroke sings what words cannot say,\n"
                "A melody paints the colours of the day.\n"
                "Canvas and keyboard, sculpture and sound,\n"
                "Art is the place where freedom is found.\n"
                "Traditional meets modern, East meets West,\n"
                "Expression is the thing that we do best.\n"
                "So pick up a pen or strum a string,\n"
                "Let your creative spirit take its wing."
            ),
            "activity": "Students pair a painting with a song that shares the same mood. Present the pairing and explain the emotional connection using descriptive adjectives from the unit."
        },
        9: {
            "title": "Mind and Body",
            "lyrics": (
                "Sleep eight hours, eat your greens,\n"
                "Health is more than what the mirror means.\n"
                "Stress is real, but so is rest,\n"
                "Take a breath — you're doing your best.\n"
                "Mental health deserves the same respect\n"
                "As any bone a doctor might inspect.\n"
                "Talk to someone, break the silent wall,\n"
                "Wellness means we're looking after all."
            ),
            "activity": "Students create a Wellness Playlist of five songs that promote well-being, writing a one-sentence justification for each choice. Share and discuss in groups."
        },
        10: {
            "title": "Green Footprint",
            "lyrics": (
                "Reduce, reuse, recycle — we know the phrase,\n"
                "But action speaks louder in a thousand ways.\n"
                "Plant a tree, conserve the stream,\n"
                "A greener future starts with a team.\n"
                "Data shows the damage, science shows the way,\n"
                "Every small decision shapes a better day.\n"
                "So audit, act, and advocate,\n"
                "Before it's too late — don't hesitate."
            ),
            "activity": "Students write a pledge verse committing to one environmental action. Compile into a class Green Pledge Poster displayed in the school entrance."
        }
    }
}

# ──────────────────────────────────────────────────────────────────────
# DIALOGUE BANK
# ──────────────────────────────────────────────────────────────────────
DIALOGUE_BANK = {
    9: {
        1: {
            "setting": "School Corridor",
            "characters": ["Emre (new student)", "Selin (senior mentor)"],
            "lines": [
                ("Emre", "Excuse me, is this the way to the science lab?"),
                ("Selin", "Yes! Go straight and turn right at the end. I'm Selin, by the way."),
                ("Emre", "Nice to meet you, Selin. I'm Emre. It's my first day here."),
                ("Selin", "Welcome! First days are always a bit stressful, but you'll love this school."),
                ("Emre", "Thanks! Do you know which teacher we have for biology?"),
                ("Selin", "Mr. Demir. He's great — really makes the subject come alive."),
                ("Emre", "That sounds promising. What about the canteen? Is it any good?"),
                ("Selin", "The lahmacun is legendary. Come on, I'll show you around at break time."),
            ],
            "focus_language": "Asking for directions, introductions, Present Simple",
            "task": "Role-play with a partner. Change the destination and add two more lines about after-school clubs.",
        },
        2: {
            "setting": "Guidance Counsellor's Office",
            "characters": ["Defne (student)", "Can (classmate)"],
            "lines": [
                ("Defne", "I took the personality quiz, and apparently I'm an introvert. What about you?"),
                ("Can", "I got extrovert, which makes sense — I love being around people."),
                ("Defne", "Do you think these labels really define us, though?"),
                ("Can", "Not completely. I think everyone has a bit of both."),
                ("Defne", "True. Sometimes I enjoy group work, but I need quiet time to recharge."),
                ("Can", "And I actually enjoy reading alone on weekends. So, we're both a mix!"),
                ("Defne", "That's a good point. Maybe personality is more like a spectrum."),
                ("Can", "Exactly. Let's tell Ms. Yılmaz our theory — she'll love it."),
            ],
            "focus_language": "Describing personality, expressing opinions, linking words (though, actually)",
            "task": "Role-play the dialogue, then continue the conversation with Ms. Yılmaz joining in.",
        },
        3: {
            "setting": "Computer Lab",
            "characters": ["Berk (tech student)", "Zeynep (journalism club president)"],
            "lines": [
                ("Zeynep", "Berk, have you seen the school's new social media policy?"),
                ("Berk", "Yes, they've banned phones during lessons. I think it's a bit extreme."),
                ("Zeynep", "I disagree. Students were scrolling instead of listening."),
                ("Berk", "But technology can support learning too — research, collaboration apps..."),
                ("Zeynep", "That's true. Maybe the rule should allow educational use only."),
                ("Berk", "Exactly! A balanced policy would be much better."),
                ("Zeynep", "Let's write an editorial for the school paper about it."),
                ("Berk", "Great idea. We could include a student survey as well."),
            ],
            "focus_language": "Agreeing and disagreeing, expressing opinions, modal verbs (should, could)",
            "task": "Role-play the dialogue. Then debate: Should phones be allowed in classrooms?",
        },
        4: {
            "setting": "English Classroom",
            "characters": ["Arda (exchange student)", "Elif (classmate)"],
            "lines": [
                ("Arda", "I always mix up the Present Perfect and Past Simple. Any tips?"),
                ("Elif", "Sure! Past Simple is for finished actions with a specific time."),
                ("Arda", "So, 'I visited Istanbul last summer' is Past Simple?"),
                ("Elif", "Exactly. And 'I have visited Istanbul three times' is Present Perfect."),
                ("Arda", "Because there's no specific time, and it connects to now?"),
                ("Elif", "Spot on! The experience is still relevant."),
                ("Arda", "What about 'I have been living here since September'?"),
                ("Elif", "That's Present Perfect Continuous — an action that started in the past and is still going on."),
                ("Arda", "Grammar suddenly makes more sense. Thanks, Elif!"),
                ("Elif", "Any time! Let's practise with some more examples."),
            ],
            "focus_language": "Present Perfect vs Past Simple, time expressions (since, for, last, ago)",
            "task": "Role-play, then create five original sentences — two Past Simple, two Present Perfect, one Present Perfect Continuous.",
        },
        5: {
            "setting": "School Library",
            "characters": ["Yasemin (book club leader)", "Kerem (reluctant reader)"],
            "lines": [
                ("Yasemin", "Kerem, have you started 'The Little Prince' yet?"),
                ("Kerem", "I tried, but it seems like a children's book. Why are we reading it?"),
                ("Yasemin", "It looks simple on the surface, but the themes are really deep."),
                ("Kerem", "Like what?"),
                ("Yasemin", "Loneliness, the meaning of friendship, how adults lose their imagination."),
                ("Kerem", "Hmm, that does sound more interesting than I expected."),
                ("Yasemin", "Read to chapter five and we'll discuss it at the book club on Friday."),
                ("Kerem", "All right, I'll give it a proper chance. But you owe me a coffee if I don't like it!"),
            ],
            "focus_language": "Persuading, expressing surprise, reported speech",
            "task": "Role-play the dialogue. Then one partner recommends a different book using similar persuasion techniques.",
        },
        6: {
            "setting": "Debate Club Room",
            "characters": ["Deniz (student activist)", "Mert (debate captain)"],
            "lines": [
                ("Deniz", "Did you see the news about the plastic waste in the Mediterranean?"),
                ("Mert", "Yes, it's alarming. Türkiye produces over 35 million tonnes of waste annually."),
                ("Deniz", "We should organise a school-wide awareness campaign."),
                ("Mert", "Good idea. But we need facts, not just emotions, to convince people."),
                ("Deniz", "You're right. Let's prepare an infographic with reliable data."),
                ("Mert", "We could also invite a speaker from an environmental NGO."),
                ("Deniz", "Perfect. And a petition to reduce single-use plastic in the canteen."),
                ("Mert", "Now that's a concrete action. Let's draft it tonight."),
            ],
            "focus_language": "Making suggestions, expressing necessity, passive voice (is produced, should be reduced)",
            "task": "Role-play the dialogue. Then plan your own school campaign on a global issue of your choice.",
        },
        7: {
            "setting": "Science Laboratory",
            "characters": ["Tuğçe (aspiring scientist)", "Onur (robotics club member)"],
            "lines": [
                ("Tugce", "Onur, our robot keeps turning left instead of going straight."),
                ("Onur", "Let me check the sensor. I think the calibration is off."),
                ("Tugce", "If we adjust the ultrasonic sensor by two degrees, it should fix it."),
                ("Onur", "Good thinking. Science is all about testing and adjusting."),
                ("Tugce", "Exactly — the scientific method in action!"),
                ("Onur", "What if we add a second sensor for redundancy?"),
                ("Tugce", "That would make it more reliable. Let's test both versions and compare."),
                ("Onur", "Brilliant. We might actually win the TÜBİTAK competition this year!"),
            ],
            "focus_language": "First and Second Conditionals, technical vocabulary, problem-solving language",
            "task": "Role-play the dialogue. Then describe a scientific problem and propose a solution using conditionals.",
        },
        8: {
            "setting": "Art Studio",
            "characters": ["Hazal (visual artist)", "Burak (musician)"],
            "lines": [
                ("Hazal", "I'm stuck on my painting. I want to show 'freedom' but nothing feels right."),
                ("Burak", "What does freedom mean to you? Start there."),
                ("Hazal", "It's like... open sky, no boundaries, the feeling of running."),
                ("Burak", "That's interesting. When I think of freedom, I hear a melody with no set rhythm."),
                ("Hazal", "So freedom is different for everyone. That gives me an idea!"),
                ("Burak", "What if we collaborate — your painting and my music together?"),
                ("Hazal", "A multimedia piece! We could present it at the school arts festival."),
                ("Burak", "Let's do it. Art is always more powerful when different forms come together."),
            ],
            "focus_language": "Abstract vocabulary, expressing feelings, relative clauses (that, which, where)",
            "task": "Role-play the dialogue. Then choose an abstract concept and describe it through two different art forms.",
        },
        9: {
            "setting": "School Garden",
            "characters": ["Selin (mentor)", "Emre (freshman)"],
            "lines": [
                ("Emre", "Selin, I've been feeling really tired lately, even though I sleep eight hours."),
                ("Selin", "Are you eating properly? Skipping meals is common during exam season."),
                ("Emre", "I usually skip breakfast because I wake up late."),
                ("Selin", "That's probably the problem. Breakfast fuels your brain for the whole morning."),
                ("Emre", "What do you usually have?"),
                ("Selin", "Eggs, cheese, tomatoes, and a glass of orange juice. Quick and healthy."),
                ("Emre", "I should try that. Do you exercise as well?"),
                ("Selin", "Yes, I jog three times a week. It helps with stress too."),
                ("Emre", "Maybe I'll join the morning running club. Thanks for the advice!"),
                ("Selin", "Any time. Health comes first — everything else follows."),
            ],
            "focus_language": "Giving advice (should, could, ought to), health vocabulary, frequency adverbs",
            "task": "Role-play the dialogue. Then create a 'Healthy Week' plan with at least five daily habits.",
        },
        10: {
            "setting": "Recycling Station in Schoolyard",
            "characters": ["Deniz (activist)", "Tuğçe (scientist)"],
            "lines": [
                ("Deniz", "Tuğçe, did you know our school produces about 200 kg of waste a week?"),
                ("Tugce", "That's a lot! How much of it is recyclable?"),
                ("Deniz", "According to my audit, nearly 60 percent — but most of it ends up in general waste."),
                ("Tugce", "We need a better sorting system. Colour-coded bins with clear labels."),
                ("Deniz", "And an awareness campaign so students actually use them."),
                ("Tugce", "What if we set up a composting area for the organic waste?"),
                ("Deniz", "Great idea! The biology class could use the compost for their garden project."),
                ("Tugce", "Science and sustainability working together. Let's present this to the principal."),
            ],
            "focus_language": "Quantifiers (much, many, most, nearly), suggesting solutions, passive voice",
            "task": "Role-play the dialogue. Then conduct a mini waste audit of your classroom and propose three improvements.",
        },
    }
}

# ──────────────────────────────────────────────────────────────────────
# COMIC STRIP BANK
# ──────────────────────────────────────────────────────────────────────
COMIC_STRIP_BANK = {
    9: {
        1: {
            "title": "First Day Jitters",
            "panels": [
                {"scene": "Emre stands outside the school gate looking nervous.",
                 "speech": "I can't believe it's my first day. What if nobody talks to me?",
                 "thought": "I should have practised my introduction last night..."},
                {"scene": "Emre walks into a crowded corridor; students rush past him.",
                 "speech": "",
                 "thought": "Everyone seems to know each other already."},
                {"scene": "Selin taps Emre on the shoulder with a friendly smile.",
                 "speech": "Hey! You look lost. I'm Selin — need a hand?",
                 "thought": ""},
                {"scene": "Emre and Selin walk together towards the classroom, both laughing.",
                 "speech": "Thanks! I'm Emre. This school is bigger than I expected!",
                 "thought": "Maybe today won't be so bad after all."},
                {"scene": "They sit together in class; the teacher writes 'Welcome!' on the board.",
                 "speech": "See? First days are scary, but they always get better.",
                 "thought": "I think I just made my first friend."},
            ],
            "drawing_task": "Draw your own first-day comic strip with 4 panels showing a problem and a happy ending.",
            "language_focus": "Present Simple, feelings vocabulary, introductions",
        },
        2: {
            "title": "The Personality Quiz",
            "panels": [
                {"scene": "Defne reads a personality quiz result on her phone, frowning.",
                 "speech": "It says I'm 100% introvert. That can't be right.",
                 "thought": "I do love being alone, but I also enjoy group projects..."},
                {"scene": "Can leans over, grinning.",
                 "speech": "Ha! Mine says extrovert. Apparently I 'thrive in social settings'.",
                 "thought": ""},
                {"scene": "Both look at each other confused as their results seem too extreme.",
                 "speech": "These categories are too black and white, aren't they?",
                 "thought": "People are more complicated than a quiz."},
                {"scene": "Ms. Yılmaz draws a spectrum on the board.",
                 "speech": "Nobody is 100% anything. Personality is a spectrum!",
                 "thought": ""},
                {"scene": "Defne and Can high-five, relieved.",
                 "speech": "So we're both 'ambiverts'? Cool!",
                 "thought": "Labels don't define me."},
            ],
            "drawing_task": "Create a 4-panel comic about discovering something surprising about your personality.",
            "language_focus": "Adjectives for personality, comparative structures, opinion expressions",
        },
        3: {
            "title": "The Phone Dilemma",
            "panels": [
                {"scene": "Berk is secretly checking his phone under the desk during class.",
                 "speech": "",
                 "thought": "Just one more notification... it might be important."},
                {"scene": "Mr. Aksoy notices and raises an eyebrow.",
                 "speech": "Berk, would you like to share what's so interesting?",
                 "thought": ""},
                {"scene": "Berk looks embarrassed; the screen shows a meme, not homework.",
                 "speech": "Sorry, sir. It was... research.",
                 "thought": "A meme about cats is NOT research."},
                {"scene": "After class, Zeynep talks to Berk seriously.",
                 "speech": "You know, our generation needs to prove we can use tech responsibly.",
                 "thought": ""},
                {"scene": "Berk puts his phone in his bag and opens his notebook.",
                 "speech": "You're right. Phone away, brain on.",
                 "thought": "Focus mode: activated."},
            ],
            "drawing_task": "Draw a 4-panel comic showing a student resisting a digital distraction and succeeding.",
            "language_focus": "Modal verbs (should, need to), digital vocabulary, imperative mood",
        },
        4: {
            "title": "Tense Trouble",
            "panels": [
                {"scene": "Arda stares at a grammar worksheet covered in red marks.",
                 "speech": "I wrote 'I have went' again! Why can't I remember?",
                 "thought": "German past tenses are so different..."},
                {"scene": "Elif draws a timeline on a piece of paper.",
                 "speech": "Look — Past Simple: specific time. Present Perfect: no specific time.",
                 "thought": ""},
                {"scene": "A lightbulb appears over Arda's head.",
                 "speech": "So 'I went yesterday' but 'I have been three times'?",
                 "thought": "It's clicking!"},
                {"scene": "Ms. Kaya hands back a new quiz; Arda got full marks.",
                 "speech": "Excellent work, Arda! What changed?",
                 "thought": ""},
                {"scene": "Arda winks at Elif across the room.",
                 "speech": "I had a great teacher — two, actually!",
                 "thought": "Timelines are magic."},
            ],
            "drawing_task": "Create a comic where a character learns a grammar rule through a funny mistake.",
            "language_focus": "Present Perfect vs Past Simple, irregular past participles",
        },
        5: {
            "title": "The Book That Changed Everything",
            "panels": [
                {"scene": "Kerem pushes 'The Little Prince' away on his desk.",
                 "speech": "A book about a kid on a tiny planet? No thanks.",
                 "thought": "This is definitely for primary school."},
                {"scene": "Yasemin slides a bookmark into the most powerful chapter.",
                 "speech": "Just read to page 40. Trust me.",
                 "thought": ""},
                {"scene": "Kerem reads under his blanket at night, clearly moved.",
                 "speech": "",
                 "thought": "'What is essential is invisible to the eye.' Wow."},
                {"scene": "Next day, Kerem arrives at book club first, holding the book tightly.",
                 "speech": "Okay, I was wrong. This book is incredible.",
                 "thought": "Never judge a book by its cover — literally."},
            ],
            "drawing_task": "Draw a 4-panel comic about a book or story that changed your perspective.",
            "language_focus": "Past Simple narrative, reporting speech, expressing opinions",
        },
        6: {
            "title": "The Plastic Problem",
            "panels": [
                {"scene": "Deniz picks up a plastic bottle from the school garden, disgusted.",
                 "speech": "This is the third bottle I've found today. Doesn't anyone care?",
                 "thought": ""},
                {"scene": "Mert shows Deniz a graph on his tablet — plastic waste statistics.",
                 "speech": "Look at these numbers. The ocean will have more plastic than fish by 2050.",
                 "thought": ""},
                {"scene": "They brainstorm at a whiteboard covered in ideas.",
                 "speech": "What if we replace all plastic bottles in school with reusable ones?",
                 "thought": "Small changes, big impact."},
                {"scene": "A month later: students proudly carry colourful reusable bottles.",
                 "speech": "We reduced plastic waste by 70 percent!",
                 "thought": ""},
                {"scene": "The principal shakes their hands at assembly.",
                 "speech": "Congratulations! You've shown that students can lead real change.",
                 "thought": "This is just the beginning."},
            ],
            "drawing_task": "Create a 4-panel comic about solving an environmental or social problem in your school.",
            "language_focus": "Future predictions (will), statistics language, persuasive expressions",
        },
        7: {
            "title": "Robot Gone Wrong",
            "panels": [
                {"scene": "Tuğçe and Onur present their robot at the science fair. It's supposed to walk straight.",
                 "speech": "Ladies and gentlemen, meet TechBot 3000!",
                 "thought": "Please work, please work..."},
                {"scene": "The robot spins in circles instead of walking forward.",
                 "speech": "",
                 "thought": "Oh no. Not again."},
                {"scene": "The audience laughs, but Dr. Özkan nods encouragingly.",
                 "speech": "Every great invention had failures first. What did you learn?",
                 "thought": ""},
                {"scene": "Tuğçe adjusts the sensor while Onur reprograms the code.",
                 "speech": "The left sensor was reading 3 degrees off. Fixed!",
                 "thought": "Failure is just data."},
                {"scene": "TechBot walks perfectly across the stage. The audience cheers.",
                 "speech": "TechBot 3000, version 2 — now with 100% more straight lines!",
                 "thought": "This is why I love science."},
            ],
            "drawing_task": "Draw a comic about an invention that fails first but succeeds after adjustments.",
            "language_focus": "Past Continuous, scientific vocabulary, cause and effect (because, so, therefore)",
        },
        8: {
            "title": "Art Is Everywhere",
            "panels": [
                {"scene": "Hazal stares at a blank canvas in the art studio, frustrated.",
                 "speech": "I have zero inspiration. Nothing looks right.",
                 "thought": "Maybe I'm not as creative as I thought."},
                {"scene": "Burak plays a melody on his guitar nearby.",
                 "speech": "Close your eyes and listen. What colours do you see?",
                 "thought": ""},
                {"scene": "Hazal closes her eyes; abstract colours swirl around her head.",
                 "speech": "",
                 "thought": "Blue... gold... like a sunset over the Bosphorus."},
                {"scene": "She paints passionately; the canvas comes alive with vibrant colours.",
                 "speech": "Music gave me the picture I couldn't find alone!",
                 "thought": ""},
                {"scene": "Ms. Erdem looks at the painting proudly.",
                 "speech": "This is what happens when art forms collaborate. Magnificent!",
                 "thought": "These two are going places."},
            ],
            "drawing_task": "Listen to a piece of music and draw what you 'see' in 4 panels.",
            "language_focus": "Sensory adjectives, when/while clauses, expressing inspiration",
        },
        9: {
            "title": "The Burnout Battle",
            "panels": [
                {"scene": "Emre is surrounded by textbooks, energy drinks, and alarm clocks at 2 AM.",
                 "speech": "If I study three more hours, I'll ace the exam.",
                 "thought": "I can't even remember what I just read."},
                {"scene": "Next morning, Emre falls asleep during the exam.",
                 "speech": "",
                 "thought": "Zzz..."},
                {"scene": "Selin finds Emre looking defeated after the exam.",
                 "speech": "You look terrible. When did you last sleep properly?",
                 "thought": ""},
                {"scene": "Selin shows Emre a study planner with regular breaks and sleep time.",
                 "speech": "Quality over quantity. Your brain needs rest to actually learn.",
                 "thought": ""},
                {"scene": "A week later, Emre studies calmly at a tidy desk with a water bottle.",
                 "speech": "Eight hours of sleep, focused study sessions, and I feel great!",
                 "thought": "Balance is the real secret to success."},
            ],
            "drawing_task": "Draw a 4-panel comic about finding balance between studying and self-care.",
            "language_focus": "Giving advice (should, ought to), health vocabulary, first conditional",
        },
        10: {
            "title": "One Tree at a Time",
            "panels": [
                {"scene": "Deniz shows satellite images of deforestation to the class.",
                 "speech": "Türkiye lost thousands of hectares of forest last year.",
                 "thought": ""},
                {"scene": "Tuğçe calculates CO2 absorption rates on the board.",
                 "speech": "One tree absorbs about 22 kg of CO2 per year. We need more trees, not fewer.",
                 "thought": "The maths is clear."},
                {"scene": "The whole class is planting saplings in the school garden.",
                 "speech": "If every school in Türkiye planted 50 trees, imagine the impact!",
                 "thought": ""},
                {"scene": "A time-lapse panel shows the saplings growing into tall trees over years.",
                 "speech": "",
                 "thought": ""},
                {"scene": "Students sit in the shade of the trees they planted years ago.",
                 "speech": "We planted these in Grade 9. Look at them now!",
                 "thought": "Small actions grow into big change."},
            ],
            "drawing_task": "Create a 4-panel comic showing an environmental project from start to finish.",
            "language_focus": "Conditional sentences, quantifiers, future time clauses (when, after, once)",
        },
    }
}

# ──────────────────────────────────────────────────────────────────────
# ESCAPE ROOM BANK
# ──────────────────────────────────────────────────────────────────────
ESCAPE_ROOM_BANK = {
    9: {
        1: {
            "title": "Escape from Orientation!",
            "story": "You're locked in the orientation hall! Solve 5 puzzles to find the exit code before the bell rings!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: L-U-C-I-R-R-U-C-M-U → A plan of study at school", "answer": "CURRICULUM", "hint": "It starts with 'C' and has 10 letters."},
                {"type": "grammar", "question": "Fill in: 'She ___ (go) to this school since 2023.' Choose the correct tense.", "answer": "has gone / has been going", "hint": "The action started in the past and continues now."},
                {"type": "reading", "question": "Read the school rules poster: 'Students must arrive by 08:30.' What time is the latest you can arrive?", "answer": "08:30", "hint": "Look for a specific time in the sentence."},
                {"type": "maths", "question": "The school has 4 floors. Each floor has 8 classrooms. Your class is in room (floors × classrooms ÷ 4). Which room?", "answer": "8", "hint": "4 × 8 = 32, then divide by 4."},
                {"type": "riddle", "question": "I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?", "answer": "A keyboard", "hint": "You use it every day in the computer lab."},
            ],
            "final_code": "WELCOME9",
            "reward": "Escaped! +40 XP! Badge: Orientation Survivor 🏫",
        },
        2: {
            "title": "The Identity Vault",
            "story": "A mysterious vault contains everyone's personality profiles! Crack the code to unlock it and discover who you really are.",
            "puzzles": [
                {"type": "vocabulary", "question": "Match the personality trait to its opposite: 'shy' → ???", "answer": "outgoing / confident", "hint": "Someone who loves meeting new people."},
                {"type": "grammar", "question": "Correct the sentence: 'He is more friendlier than his brother.'", "answer": "He is friendlier than his brother.", "hint": "You don't need 'more' with '-er' comparatives."},
                {"type": "reading", "question": "A character description says: 'Despite her quiet nature, she always speaks up for what is right.' Is she passive or assertive?", "answer": "assertive", "hint": "Focus on 'speaks up for what is right'."},
                {"type": "maths", "question": "In a class of 30, 40% are extroverts, 35% are introverts, the rest are ambiverts. How many ambiverts?", "answer": "7 (25% of 30 = 7.5, rounded to 7 or 8 accepted)", "hint": "100% - 40% - 35% = ?% then calculate."},
                {"type": "riddle", "question": "I can be cracked, made, told, and played. What am I?", "answer": "A joke", "hint": "Something that makes people laugh."},
            ],
            "final_code": "KNOWYOU",
            "reward": "Escaped! +40 XP! Badge: Identity Explorer 🔍",
        },
        3: {
            "title": "Hack the Network!",
            "story": "The school Wi-Fi is down! Navigate through five digital challenges to restore the connection before the online exam starts!",
            "puzzles": [
                {"type": "vocabulary", "question": "Define 'bandwidth' in simple English.", "answer": "The amount of data that can be sent over a network in a given time", "hint": "Think of it as the 'width' of a data pipe."},
                {"type": "grammar", "question": "Choose: 'If the server ___ (crash), we will lose our data.' (First Conditional)", "answer": "crashes", "hint": "First Conditional: If + Present Simple, will + base verb."},
                {"type": "reading", "question": "An email says: 'Dear user, click here to verify your account or it will be deleted.' Is this legitimate or a phishing attempt?", "answer": "phishing attempt", "hint": "Legitimate services rarely threaten to delete accounts."},
                {"type": "maths", "question": "A file is 2.4 GB. Download speed is 60 MB/s. How many seconds to download? (1 GB = 1000 MB)", "answer": "40 seconds", "hint": "2.4 GB = 2400 MB. Divide by 60."},
                {"type": "riddle", "question": "I connect millions but I'm not a road. I carry information but I'm not a book. What am I?", "answer": "The Internet", "hint": "You're using it right now."},
            ],
            "final_code": "ONLINE",
            "reward": "Escaped! +40 XP! Badge: Digital Hero 💻",
        },
        4: {
            "title": "The Tense Time Machine!",
            "story": "A time machine is stuck between past, present, and future! Fix the tenses in each era to return to the present!",
            "puzzles": [
                {"type": "vocabulary", "question": "What word means 'a word that shows when an action happens'? (Hint: past, present, future)", "answer": "tense", "hint": "It's also the name of this escape room theme."},
                {"type": "grammar", "question": "Fix: 'By the time we arrived, the concert already started.' Use the correct past form.", "answer": "By the time we arrived, the concert had already started.", "hint": "Use Past Perfect for the earlier action."},
                {"type": "reading", "question": "A diary from 1923 reads: 'Today we have celebrated the Republic.' Is the tense correct for a diary entry about that specific day?", "answer": "No — it should be 'Today we celebrated the Republic' (Past Simple for a specific day)", "hint": "Diary entries about specific days use Past Simple."},
                {"type": "maths", "question": "If the Past Simple started in the year 0 and the Present Perfect started 500 years later, what year did Present Perfect begin?", "answer": "500", "hint": "0 + 500 = ?"},
                {"type": "riddle", "question": "I'm always coming but never arrive. What am I?", "answer": "Tomorrow", "hint": "It's always one day away."},
            ],
            "final_code": "TENSES",
            "reward": "Escaped! +40 XP! Badge: Time Traveller ⏰",
        },
        5: {
            "title": "The Enchanted Library!",
            "story": "You're trapped in a magical library! The books have come alive and locked the doors. Answer their literary riddles to escape!",
            "puzzles": [
                {"type": "vocabulary", "question": "What literary device is used in 'The wind whispered through the trees'?", "answer": "personification", "hint": "Giving human qualities to non-human things."},
                {"type": "grammar", "question": "Rewrite in reported speech: The fox said, 'I don't want those grapes anyway.'", "answer": "The fox said (that) he didn't want those grapes anyway.", "hint": "Change present to past, 'I' to 'he'."},
                {"type": "reading", "question": "In 'The Little Prince', the fox says: 'You become responsible, forever, for what you have tamed.' What does 'tamed' mean here?", "answer": "formed a bond with / built a relationship with", "hint": "It's about connection, not control."},
                {"type": "maths", "question": "'The Little Prince' was published in 1943. How many years ago was that? (Current year: 2026)", "answer": "83", "hint": "2026 - 1943 = ?"},
                {"type": "riddle", "question": "I have a spine but no bones, pages but no age, a cover but no blanket. What am I?", "answer": "A book", "hint": "You'll find millions of me in this room."},
            ],
            "final_code": "READER",
            "reward": "Escaped! +40 XP! Badge: Literary Adventurer 📚",
        },
        6: {
            "title": "Mission: Save the Summit!",
            "story": "World leaders are trapped in a deadlocked climate summit! Solve the puzzles to unlock a compromise and save the planet!",
            "puzzles": [
                {"type": "vocabulary", "question": "What does 'carbon footprint' mean?", "answer": "The total amount of greenhouse gases produced by human activities, measured in CO2 equivalent", "hint": "It's about the impact your lifestyle has on the environment."},
                {"type": "grammar", "question": "Complete: 'If every country ___ (reduce) emissions by 50%, global warming ___ (slow) down.' (Second Conditional)", "answer": "If every country reduced emissions by 50%, global warming would slow down.", "hint": "Second Conditional: If + Past Simple, would + base verb."},
                {"type": "reading", "question": "A headline reads: 'Rising Sea Levels Threaten 300 Million People by 2050.' Is this a fact or an opinion?", "answer": "A prediction based on scientific data (informed estimate)", "hint": "It uses data but projects into the future."},
                {"type": "maths", "question": "A country emits 400 million tonnes of CO2. It pledges to cut 25%. How many tonnes will it emit after the cut?", "answer": "300 million tonnes", "hint": "400 × 0.75 = ?"},
                {"type": "riddle", "question": "I'm not alive, but I grow. I don't have lungs, but I need air. I don't have a mouth, but water kills me. What am I?", "answer": "Fire", "hint": "Think about wildfires and climate change."},
            ],
            "final_code": "PLANET",
            "reward": "Escaped! +40 XP! Badge: Climate Champion 🌍",
        },
        7: {
            "title": "Lab Lockdown!",
            "story": "A chemical spill has triggered an automatic lockdown in the science lab! Solve the puzzles to neutralise the spill and unlock the doors!",
            "puzzles": [
                {"type": "vocabulary", "question": "What is the scientific term for a substance that speeds up a chemical reaction without being consumed?", "answer": "catalyst", "hint": "It starts with 'C' and has 8 letters."},
                {"type": "grammar", "question": "Complete: 'If I ___ (mix) acid and base, the solution ___ (become) neutral.' (Zero Conditional)", "answer": "If I mix acid and base, the solution becomes neutral.", "hint": "Zero Conditional: If + Present Simple, Present Simple (scientific facts)."},
                {"type": "reading", "question": "Safety sign: 'Wear goggles at all times. Do NOT taste any chemicals.' Why is 'NOT' in capitals?", "answer": "To emphasise the danger and make the warning impossible to miss", "hint": "Capitalisation is used for emphasis in safety instructions."},
                {"type": "maths", "question": "You need 250 ml of solution. The beaker has 175 ml. How much more do you need?", "answer": "75 ml", "hint": "250 - 175 = ?"},
                {"type": "riddle", "question": "I am not alive, but I can die. I don't breathe, but I need oxygen. What am I?", "answer": "A battery", "hint": "It 'dies' when its energy runs out."},
            ],
            "final_code": "SAFETY",
            "reward": "Escaped! +40 XP! Badge: Lab Survivor 🔬",
        },
        8: {
            "title": "The Gallery Heist!",
            "story": "Someone has stolen the school's prize-winning painting! Follow the art clues through five rooms to catch the thief and recover the masterpiece!",
            "puzzles": [
                {"type": "vocabulary", "question": "What art technique uses dots of colour placed close together to form an image when viewed from a distance?", "answer": "pointillism", "hint": "Think of the painter Georges Seurat."},
                {"type": "grammar", "question": "Complete: 'The painting ___ (steal) sometime between 10 PM and 6 AM.' (Passive voice)", "answer": "was stolen", "hint": "Past Simple Passive: was/were + past participle."},
                {"type": "reading", "question": "A witness note says: 'I saw someone in a blue smock leaving the gallery at midnight.' What clue does this give?", "answer": "The thief may be an artist or someone disguised as one (blue smock = art clothing)", "hint": "Who typically wears a smock?"},
                {"type": "maths", "question": "The painting measures 80 cm × 60 cm. What is its area in square centimetres?", "answer": "4800 cm²", "hint": "Area = length × width."},
                {"type": "riddle", "question": "I can fill a room but take up no space. What am I?", "answer": "Light", "hint": "Essential in every art gallery."},
            ],
            "final_code": "ARTIST",
            "reward": "Escaped! +40 XP! Badge: Art Detective 🎨",
        },
        9: {
            "title": "The Wellness Maze!",
            "story": "You're trapped in a wellness centre that's gone haywire! The doors only open when you prove you know how to stay healthy!",
            "puzzles": [
                {"type": "vocabulary", "question": "What does 'sedentary' mean? (Hint: opposite of active)", "answer": "Involving much sitting and little physical activity", "hint": "Think of someone who sits at a desk all day."},
                {"type": "grammar", "question": "Give advice: 'You look exhausted.' Use 'should' and 'ought to'.", "answer": "You should get more sleep. / You ought to take a break.", "hint": "Both 'should' and 'ought to' express advice."},
                {"type": "reading", "question": "A nutrition label says: 'Sugar: 45g per serving.' The daily recommended limit is 25g. Is this product healthy?", "answer": "No — one serving contains nearly double the recommended daily sugar limit", "hint": "Compare 45g to the 25g limit."},
                {"type": "maths", "question": "You need 8 hours of sleep. You go to bed at 23:30. What time must you wake up?", "answer": "07:30", "hint": "23:30 + 8 hours = ?"},
                {"type": "riddle", "question": "The more you take, the more you leave behind. What am I?", "answer": "Footsteps", "hint": "Think about walking or running for exercise."},
            ],
            "final_code": "HEALTH",
            "reward": "Escaped! +40 XP! Badge: Wellness Warrior 💪",
        },
        10: {
            "title": "The Eco Bunker!",
            "story": "An underground eco-bunker has sealed shut during a recycling drill! Solve five environmental challenges to restore power and open the doors!",
            "puzzles": [
                {"type": "vocabulary", "question": "What is the term for the variety of plant and animal life in a habitat?", "answer": "biodiversity", "hint": "Bio = life, diversity = variety."},
                {"type": "grammar", "question": "Complete: 'By 2050, scientists predict that sea levels ___ (rise) by 30 cm.' Use Future Perfect.", "answer": "will have risen", "hint": "Future Perfect: will + have + past participle."},
                {"type": "reading", "question": "A sign reads: 'This forest is home to 3,000 species. Deforestation threatens 40% of them.' How many species are at risk?", "answer": "1,200", "hint": "3,000 × 0.40 = ?"},
                {"type": "maths", "question": "A solar panel produces 5 kWh/day. The bunker needs 35 kWh/day. How many panels are needed?", "answer": "7", "hint": "35 ÷ 5 = ?"},
                {"type": "riddle", "question": "I am taken from a mine and shut in a wooden case. I am used by almost everyone. What am I?", "answer": "Pencil lead (graphite)", "hint": "You write with me every day at school."},
            ],
            "final_code": "ECOWIN",
            "reward": "Escaped! +40 XP! Badge: Eco Guardian 🌱",
        },
    }
}

# ──────────────────────────────────────────────────────────────────────
# FAMILY CORNER BANK
# ──────────────────────────────────────────────────────────────────────
FAMILY_CORNER_BANK = {
    9: {
        1: {
            "title": "What Was School Like for You?",
            "activity": "Interview a parent or guardian about THEIR first day of high school. Write a comparison essay (150-200 words) highlighting similarities and differences.",
            "together": "Read your comparison essay aloud to your family. Discuss how school has changed over the years.",
            "parent_question": "Dear parent, please share a memorable moment from your first week of high school with your child. What advice would you give to a new high school student?",
            "signature": True,
        },
        2: {
            "title": "Family Personality Map",
            "activity": "Ask each family member to describe themselves in three adjectives. Create a 'Family Personality Map' poster showing everyone's traits.",
            "together": "Compare your maps. Which traits do you share? Which are unique? Discuss how different personalities make a family stronger.",
            "parent_question": "Dear parent, how has your personality changed since you were 15? Share one trait you hope your child will develop.",
            "signature": True,
        },
        3: {
            "title": "Our Family's Tech Timeline",
            "activity": "Create a timeline of technology in your family: What was the first phone/computer your parents used? Interview grandparents too if possible.",
            "together": "Present your timeline to the family. Discuss: Is technology making our lives better or more complicated?",
            "parent_question": "Dear parent, what technology did you grow up with? How do you feel about your child's screen time?",
            "signature": True,
        },
        4: {
            "title": "Languages in Our Home",
            "activity": "Document all the languages and dialects spoken in your family (including grandparents' generation). Create a 'Language Tree' poster.",
            "together": "Teach each other a word or phrase from a different language or dialect in your family. Discuss why language diversity matters.",
            "parent_question": "Dear parent, did you learn any foreign languages at school? How do you feel about your child learning English?",
            "signature": True,
        },
        5: {
            "title": "A Book That Shaped Us",
            "activity": "Ask each family member about a book, story, or film that deeply influenced them. Write a mini-review (100 words) of each recommendation.",
            "together": "Choose one recommendation to read or watch as a family. Discuss it over dinner.",
            "parent_question": "Dear parent, what story or book made the biggest impression on you as a teenager? Why?",
            "signature": True,
        },
        6: {
            "title": "Global Issues at the Dinner Table",
            "activity": "Choose a global issue (poverty, pollution, inequality) and discuss it with your family. Write a summary of everyone's opinions (200 words).",
            "together": "Watch a short documentary about the issue together. Can your family take one small action to help?",
            "parent_question": "Dear parent, which global issue concerns you most for your child's future? What gives you hope?",
            "signature": True,
        },
        7: {
            "title": "Inventions That Changed Our Lives",
            "activity": "Ask your parents: 'What invention has changed YOUR life the most?' Ask grandparents the same question. Write a comparison paragraph.",
            "together": "Discuss as a family: If you could invent one thing to solve a daily problem, what would it be?",
            "parent_question": "Dear parent, what scientific or technological development amazes you the most? Share why with your child.",
            "signature": True,
        },
        8: {
            "title": "Art in Our Family",
            "activity": "Find out if anyone in your family paints, plays music, writes poetry, or does handicrafts. Document their talent with photos or recordings.",
            "together": "Have a mini 'Family Arts Festival' at home — each person performs, shows, or shares something creative.",
            "parent_question": "Dear parent, did you have a creative hobby as a teenager? How did it shape who you are today?",
            "signature": True,
        },
        9: {
            "title": "Health Traditions in Our Family",
            "activity": "Interview your family about traditional health practices (herbal teas, home remedies, seasonal foods). Create an illustrated 'Family Health Guide'.",
            "together": "Cook a healthy traditional recipe together. Discuss which old practices are backed by modern science.",
            "parent_question": "Dear parent, what health advice did YOUR parents give you? Do you still follow it today?",
            "signature": True,
        },
        10: {
            "title": "Our Family's Green Habits",
            "activity": "Conduct a family 'eco-audit': How much water, electricity, and waste does your household produce in a week? Record and analyse the data.",
            "together": "Set three family goals to reduce your environmental footprint this month. Check progress weekly.",
            "parent_question": "Dear parent, how has the environment in your hometown changed since your childhood? What should we do differently?",
            "signature": True,
        },
    }
}

# ──────────────────────────────────────────────────────────────────────
# SEL (SOCIAL-EMOTIONAL LEARNING) BANK
# ──────────────────────────────────────────────────────────────────────
SEL_BANK = {
    9: {
        1: {
            "emotion": "Anxious / Hopeful",
            "prompt": "Starting high school brings mixed feelings. What are yours?",
            "activity": "Write a journal entry (150 words) about your first week of high school. Include at least three emotions you experienced and what triggered them.",
            "mindfulness": "Close your eyes. Visualise yourself succeeding this year — good grades, new friends, favourite lessons. What does it look like? Describe it in five sentences.",
            "discussion": "Discuss in pairs: What worries you most about high school? What excites you? Find one worry you share and one excitement you share.",
        },
        2: {
            "emotion": "Confused / Self-aware",
            "prompt": "Who are you really? Not your name or your grade — who are you on the inside?",
            "activity": "Create an 'Identity Iceberg': Above the waterline, write things people can see about you. Below, write hidden traits, dreams, and fears.",
            "mindfulness": "Sit quietly for two minutes. Focus on your breathing. With each exhale, silently say one positive trait about yourself.",
            "discussion": "In groups of four, share one 'below the waterline' trait. How does it feel to let others see the hidden parts of you?",
        },
        3: {
            "emotion": "Overwhelmed / Empowered",
            "prompt": "We live in a world of constant notifications. How does this make you feel?",
            "activity": "Track your screen time for one day. Write a reflection: How does technology affect your mood, sleep, and relationships?",
            "mindfulness": "Put all devices away for 10 minutes. Sit in silence or look out the window. Afterwards, write three observations about how you felt.",
            "discussion": "Debate: 'Social media does more harm than good for teenagers.' Take turns arguing both sides.",
        },
        4: {
            "emotion": "Frustrated / Determined",
            "prompt": "Learning grammar can feel like climbing a mountain. How do you handle frustration when something is difficult?",
            "activity": "Write about a time you struggled with something academic. What happened? How did you overcome it (or how are you still working on it)?",
            "mindfulness": "When you feel frustrated, try the 5-4-3-2-1 technique: Name 5 things you see, 4 you hear, 3 you can touch, 2 you smell, 1 you taste.",
            "discussion": "Share your strategies for dealing with academic frustration. Create a class 'Coping Toolkit' poster.",
        },
        5: {
            "emotion": "Moved / Reflective",
            "prompt": "Stories have the power to change how we see the world. Has a book, film, or story ever changed you?",
            "activity": "Write a letter to a fictional character who influenced you. Tell them what you learned from their story and how it changed your perspective.",
            "mindfulness": "Think of your favourite story character. What quality of theirs do you wish you had? Close your eyes and imagine having that quality for one day.",
            "discussion": "In pairs, share the character you wrote to. Why do we connect with fictional people? What does this say about empathy?",
        },
        6: {
            "emotion": "Angry / Compassionate",
            "prompt": "The world is full of injustice. When you see unfairness, what do you feel? What do you do?",
            "activity": "Write a 'Letter to the World' (200 words) about one issue that makes you angry. End with a constructive proposal.",
            "mindfulness": "Anger is natural but needs direction. When you feel angry about injustice, pause and ask: What is within my power to change? Focus your energy there.",
            "discussion": "Discuss: Is anger a useful emotion? When does it help us, and when does it harm us? How can we channel anger into positive action?",
        },
        7: {
            "emotion": "Curious / Persistent",
            "prompt": "Every great discovery started with failure. How do you react when an experiment or plan doesn't work?",
            "activity": "Write about your biggest 'failure' and what it taught you. Reframe it as a learning experience using the sentence: 'I didn't fail — I discovered that...'",
            "mindfulness": "Think of a problem you're currently facing. Instead of focusing on the problem, spend two minutes imagining three possible solutions. How does shifting focus feel?",
            "discussion": "Share famous failures that led to success (e.g., Thomas Edison, J.K. Rowling). What mindset do these people share?",
        },
        8: {
            "emotion": "Vulnerable / Inspired",
            "prompt": "Creating art means showing the world a piece of yourself. That takes courage.",
            "activity": "Create something — a drawing, poem, song, or short story — that expresses an emotion you find hard to talk about. Share it anonymously if you prefer.",
            "mindfulness": "Listen to a piece of music without doing anything else. Let yourself feel whatever comes up. Afterwards, write one sentence about the experience.",
            "discussion": "Why is it sometimes easier to express feelings through art than through words? How can creativity support mental health?",
        },
        9: {
            "emotion": "Stressed / Balanced",
            "prompt": "Exams, expectations, social pressure — teenage life can be intense. How do you take care of yourself?",
            "activity": "Create a personal 'Wellness Wheel' with six sections: sleep, nutrition, exercise, relationships, hobbies, and study. Rate each 1-10 and set one goal for the lowest area.",
            "mindfulness": "Body scan: Starting from your toes, slowly move your attention up through your body. Notice any tension. Breathe into those areas and consciously relax them.",
            "discussion": "In groups, share one healthy habit and one unhealthy habit. Make a class commitment to swap one bad habit for a good one this week.",
        },
        10: {
            "emotion": "Helpless / Empowered",
            "prompt": "Climate change can feel overwhelming. How do you deal with 'eco-anxiety'?",
            "activity": "Write two paragraphs: (1) What scares you about the environment's future? (2) What gives you hope? Focus on things within your control.",
            "mindfulness": "Go outside (or look through a window). Spend three minutes observing nature — a tree, the sky, a bird. Connect with what you're trying to protect.",
            "discussion": "Discuss: Is eco-anxiety a sign of weakness or awareness? How can we stay informed without feeling hopeless? Create a list of 'Empowering Actions'.",
        },
    }
}

# ──────────────────────────────────────────────────────────────────────
# PODCAST BANK
# ──────────────────────────────────────────────────────────────────────
PODCAST_BANK = {
    9: {
        1: {
            "title": "Episode 1: Welcome to High School!",
            "host": "Emre & Selin",
            "summary": "Emre and Selin discuss survival tips for the first year of high school — from finding classrooms to making friends.",
            "segments": [
                "Intro (0:00): Emre introduces himself as a nervous freshman; Selin laughs and promises it gets easier.",
                "Topic (0:30): Top 5 survival tips — be early, ask questions, join a club, find a mentor, stay organised.",
                "Interview (2:00): A senior student shares the most embarrassing first-day story and what they learned from it.",
                "Fun Fact (3:30): The average high school student walks 2 km per day just moving between classes!",
                "Challenge (4:00): Record a 30-second voice message introducing yourself to a new classmate.",
            ],
            "student_task": "Record a 2-minute podcast about your first impressions of high school. Include at least one tip for future freshmen.",
        },
        2: {
            "title": "Episode 2: Who Am I, Really?",
            "host": "Defne & Can",
            "summary": "Defne and Can explore personality types, identity, and why labels never tell the full story.",
            "segments": [
                "Intro (0:00): Defne shares her personality quiz result and questions its accuracy.",
                "Topic (0:30): Introvert vs extrovert vs ambivert — myths and realities.",
                "Interview (2:00): Ms. Yılmaz explains the Big Five personality traits in simple terms.",
                "Fun Fact (3:30): Your personality can change up to 20% between ages 14 and 25!",
                "Challenge (4:00): Ask three friends to describe you in one word each. Do the answers surprise you?",
            ],
            "student_task": "Record a 2-minute podcast where you describe your personality without using common labels. Focus on stories, not adjectives.",
        },
        3: {
            "title": "Episode 3: Digital Lives",
            "host": "Berk & Zeynep",
            "summary": "Berk and Zeynep debate the pros and cons of social media, screen time, and digital citizenship.",
            "segments": [
                "Intro (0:00): Berk admits he spends 5 hours a day on his phone; Zeynep is shocked.",
                "Topic (0:30): Social media — connecting or isolating? Both sides of the argument.",
                "Interview (2:00): Mr. Aksoy explains how algorithms keep us scrolling and how to fight back.",
                "Fun Fact (3:30): The average teenager checks their phone 96 times a day!",
                "Challenge (4:00): Go phone-free for 3 hours this weekend. Report back on how it felt.",
            ],
            "student_task": "Record a 2-minute podcast reviewing one app or platform. Give it a rating for usefulness, safety, and entertainment.",
        },
        4: {
            "title": "Episode 4: Tense Talk",
            "host": "Arda & Elif",
            "summary": "Arda and Elif make English tenses fun with real-life examples, common mistakes, and a quick quiz.",
            "segments": [
                "Intro (0:00): Arda confesses his biggest grammar mistake (saying 'I have went' in front of the whole class).",
                "Topic (0:30): A journey through tenses — when to use each one, with everyday examples.",
                "Interview (2:00): Ms. Kaya shares the three most common tense mistakes Turkish students make.",
                "Fun Fact (3:30): English has 12 tenses, but everyday speech mainly uses 5 or 6!",
                "Challenge (4:00): Tell a one-minute story using at least four different tenses correctly.",
            ],
            "student_task": "Record a 2-minute podcast explaining one English tense to a younger student using simple examples from daily life.",
        },
        5: {
            "title": "Episode 5: Books That Blow Your Mind",
            "host": "Yasemin & Kerem",
            "summary": "Yasemin and Kerem discuss world literature — why old books still matter and how stories connect cultures.",
            "segments": [
                "Intro (0:00): Kerem admits he used to hate reading; Yasemin pretends to faint.",
                "Topic (0:30): Why 'The Little Prince' is not a children's book — hidden themes for teenagers.",
                "Interview (2:00): Mr. Polat recommends five must-read books for every 15-year-old.",
                "Fun Fact (3:30): 'The Little Prince' has been translated into over 500 languages and dialects!",
                "Challenge (4:00): Read 10 pages of a book you'd normally never pick. Share your reaction.",
            ],
            "student_task": "Record a 2-minute book review podcast. Recommend a book and explain why your classmates should read it.",
        },
        6: {
            "title": "Episode 6: Change Makers",
            "host": "Deniz & Mert",
            "summary": "Deniz and Mert discuss what young people can do about global issues — from climate change to inequality.",
            "segments": [
                "Intro (0:00): Deniz shares a statistic that made her furious; Mert asks what she plans to do about it.",
                "Topic (0:30): Youth activism around the world — Greta Thunberg, Malala, and local heroes.",
                "Interview (2:00): Ms. Çelik explains how one school petition actually changed a local policy.",
                "Fun Fact (3:30): Over 50% of the world's population is under 30 — young people have enormous power.",
                "Challenge (4:00): Write a one-paragraph letter to your local council about an issue in your community.",
            ],
            "student_task": "Record a 2-minute podcast about one global issue you care about. Include facts, your opinion, and a call to action.",
        },
        7: {
            "title": "Episode 7: Future Tech",
            "host": "Tuğçe & Onur",
            "summary": "Tuğçe and Onur explore emerging technologies — AI, robotics, and renewable energy — and what they mean for the future.",
            "segments": [
                "Intro (0:00): Onur describes his dream invention; Tuğçe evaluates if it's scientifically possible.",
                "Topic (0:30): Three technologies that will change the world by 2040 — AI, gene editing, fusion energy.",
                "Interview (2:00): Dr. Özkan explains the difference between real science and science fiction.",
                "Fun Fact (3:30): The first robot was built in 1954, and it was used in a car factory!",
                "Challenge (4:00): Design an invention that solves a problem in your school. Explain how it works.",
            ],
            "student_task": "Record a 2-minute podcast explaining a recent scientific discovery in simple English. Make it exciting!",
        },
        8: {
            "title": "Episode 8: Art Matters",
            "host": "Hazal & Burak",
            "summary": "Hazal and Burak argue that art is not a luxury — it's essential for mental health, creativity, and understanding the world.",
            "segments": [
                "Intro (0:00): Hazal shares a painting that made her cry; Burak shares a song that changed his life.",
                "Topic (0:30): Why art education matters — studies show it improves empathy, critical thinking, and well-being.",
                "Interview (2:00): Ms. Erdem discusses famous Turkish artists and why their work matters globally.",
                "Fun Fact (3:30): Listening to music activates more areas of the brain simultaneously than any other activity!",
                "Challenge (4:00): Create a piece of art in 10 minutes — any medium. Share it with the class.",
            ],
            "student_task": "Record a 2-minute podcast about an artist, musician, or writer who inspires you. Play a sample of their work if possible.",
        },
        9: {
            "title": "Episode 9: Mind & Body",
            "host": "Selin & Emre",
            "summary": "Selin and Emre discuss teenage health — sleep, nutrition, exercise, and mental well-being.",
            "segments": [
                "Intro (0:00): Emre confesses he survived on energy drinks during exams; Selin is horrified.",
                "Topic (0:30): The science of sleep — why teenagers need 8-10 hours and what happens when they don't get it.",
                "Interview (2:00): A school nurse shares the top five health mistakes teenagers make.",
                "Fun Fact (3:30): Your brain is 73% water — even mild dehydration reduces concentration by 25%!",
                "Challenge (4:00): Try a 7-day sleep challenge: go to bed at the same time every night. Track your mood.",
            ],
            "student_task": "Record a 2-minute podcast with practical health tips for students during exam season.",
        },
        10: {
            "title": "Episode 10: Our Planet, Our Responsibility",
            "host": "Deniz & Tuğçe",
            "summary": "Deniz and Tuğçe combine activism and science to explore environmental challenges and solutions.",
            "segments": [
                "Intro (0:00): Deniz and Tuğçe share one thing they changed in their daily life to help the environment.",
                "Topic (0:30): The top three environmental threats facing Türkiye — wildfires, water scarcity, and air pollution.",
                "Interview (2:00): A local environmental organisation explains how students can volunteer.",
                "Fun Fact (3:30): If everyone on Earth lived like the average Turk, we'd need 3.3 planets!",
                "Challenge (4:00): Calculate your ecological footprint online and share your results with the class.",
            ],
            "student_task": "Record a 2-minute podcast about one environmental action your school could take. Include data, a plan, and a timeline.",
        },
    }
}
