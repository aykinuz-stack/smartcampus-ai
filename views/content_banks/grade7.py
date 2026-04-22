# -*- coding: utf-8 -*-
"""Content banks for Grade 7 (Middle / Ages 12-13 / A2+ CEFR)."""

# =============================================================================
# BANK 1: STORY CHARACTERS
# =============================================================================
STORY_CHARACTERS = {
    7: {
        "main": [
            {
                "name": "Elif",
                "age": 13,
                "desc": "A curious and tech-savvy girl from Istanbul who loves journalism and dreams of becoming a documentary filmmaker.",
                "emoji": "\ud83c\udfac"
            },
            {
                "name": "Kwame",
                "age": 12,
                "desc": "A thoughtful boy from Ghana now living in Ankara who is passionate about space science and plays the drums.",
                "emoji": "\ud83e\udd41"
            },
            {
                "name": "Mei",
                "age": 13,
                "desc": "A creative girl from Beijing who excels at coding and digital art and always carries a sketchpad.",
                "emoji": "\ud83c\udfa8"
            },
            {
                "name": "Carlos",
                "age": 12,
                "desc": "An energetic boy from Mexico City who is passionate about human rights and wants to be a lawyer.",
                "emoji": "\u2696\ufe0f"
            }
        ],
        "teacher": {
            "name": "Mr. Demir",
            "desc": "A well-travelled geography and social studies teacher who uses real-world projects to inspire critical thinking."
        }
    }
}

# =============================================================================
# BANK 2: STORY BANK (Serialized episodic stories, 10-12 sentences each)
# =============================================================================
STORY_BANK = {
    7: {
        1: {
            "title": "The Identity Project",
            "previously": "Mr. Demir announced a school-wide project about personal identity and heritage.",
            "episode": (
                "Elif stood in front of her bedroom mirror, staring at the collage she had made. "
                "It was covered with photos, ticket stubs, and little notes about who she was. "
                "At school, Mr. Demir asked everyone to create a personal identity map. "
                "'Include things that make you unique,' he explained. "
                "Kwame drew a map showing Ghana and Turkey, connected by a dotted line. "
                "Mei wrote code words that described her personality: creative, quiet, determined. "
                "Carlos listed the languages he spoke: Spanish, English, and now some Turkish. "
                "Elif decided to interview her grandmother about their family history. "
                "Her grandmother told stories about growing up in a small village near the Black Sea. "
                "Elif recorded everything on her phone, feeling proud of her roots. "
                "When the class shared their maps, they realised everyone had multiple layers to their identity. "
                "Mr. Demir smiled and said, 'Identity is not one thing. It is a mosaic.'"
            ),
            "cliffhanger": "Mr. Demir then revealed the next phase: they would interview someone from a completely different culture.",
            "vocab_tie": ["identity", "heritage", "unique", "mosaic", "roots"]
        },
        2: {
            "title": "The Festival Exchange",
            "previously": "The group discovered how many layers their identities had. Now Mr. Demir wanted them to explore traditions.",
            "episode": (
                "Mr. Demir announced a Traditions Fair where each student would present a custom from their culture. "
                "Kwame decided to present the Homowo harvest festival from Ghana. "
                "He brought in photos of people dancing and sharing food in the streets. "
                "Mei chose the Mid-Autumn Festival and explained the meaning behind mooncakes. "
                "Carlos talked about Dia de los Muertos and showed colourful sugar skull decorations. "
                "Elif presented Hidirellez, the spring festival, and how people write wishes on paper. "
                "During the fair, students tasted food, watched short videos, and asked questions. "
                "A younger student asked Carlos, 'Isn't it scary to celebrate the dead?' "
                "Carlos laughed gently and explained, 'No, it is about remembering people we love.' "
                "Mei noticed that many traditions involved food, family, and gratitude. "
                "Mr. Demir pointed out that traditions connect generations and keep history alive. "
                "The class voted to create a school Traditions Calendar with celebrations from every culture."
            ),
            "cliffhanger": "While researching, Elif found a tradition that had almost disappeared and wondered if they could help revive it.",
            "vocab_tie": ["tradition", "custom", "celebration", "gratitude", "generations"]
        },
        3: {
            "title": "Career Day Surprise",
            "previously": "The Traditions Fair was a success. Now the school was preparing for Career Week.",
            "episode": (
                "The school invited professionals to talk about their jobs during Career Week. "
                "Elif was excited because a documentary filmmaker was coming. "
                "Kwame wanted to meet the astrophysicist, but she cancelled at the last minute. "
                "Mr. Demir suggested Kwame video-call her instead, and she agreed. "
                "During the call, Dr. Asante explained how she studied black holes from a lab in Accra. "
                "Mei attended a workshop by a game developer who showed how coding creates virtual worlds. "
                "Carlos met a human rights lawyer who had worked with refugees in three countries. "
                "The lawyer said, 'You do not need to wait until you are an adult to make a difference.' "
                "After Career Day, the four friends sat together and discussed their dreams. "
                "Kwame said he had never seen a scientist who looked like him before Dr. Asante. "
                "Elif realised that careers could combine passions in unexpected ways. "
                "Mr. Demir challenged them to shadow a professional for one day the following month."
            ),
            "cliffhanger": "Kwame received an email from Dr. Asante offering him a virtual mentorship, but there was one condition.",
            "vocab_tie": ["career", "professional", "mentorship", "passion", "shadow"]
        },
        4: {
            "title": "The News Detective",
            "previously": "Career Week inspired the group. Kwame began his virtual mentorship with Dr. Asante.",
            "episode": (
                "Mr. Demir started a new unit on media literacy with a shocking headline on the board. "
                "'Is this real or fake?' he asked the class. Most students could not tell. "
                "Elif, who loved journalism, felt embarrassed that she had almost believed it. "
                "Mr. Demir taught them the SIFT method: Stop, Investigate, Find better coverage, Trace claims. "
                "He divided the class into teams and gave each a set of news articles to verify. "
                "Mei used reverse image search and discovered one photo was from a different event entirely. "
                "Carlos found that a so-called expert quoted in an article did not actually exist. "
                "Kwame checked the website's About page and realised it was a satire site. "
                "Elif cross-referenced a story with three reliable sources and confirmed parts were exaggerated. "
                "The class created a Media Literacy Guide for younger students in the school. "
                "Mr. Demir said, 'In the digital age, being a critical reader is as important as being a good writer.' "
                "Elif proposed starting a school fact-checking club, and twelve students signed up immediately."
            ),
            "cliffhanger": "The fact-checking club's first investigation uncovered something unexpected about a popular school social media account.",
            "vocab_tie": ["media literacy", "verify", "source", "critical thinking", "headline"]
        },
        5: {
            "title": "The Wellness Week",
            "previously": "The fact-checking club was running strong. But the group noticed something: everyone seemed stressed.",
            "episode": (
                "Exam season was approaching, and the school hallways felt tense. "
                "Mei had not been sleeping well and was drinking too much coffee. "
                "Carlos noticed that some students skipped lunch to study, which worried him. "
                "Mr. Demir proposed a Wellness Week with activities to promote health and balance. "
                "A school counsellor led a session on managing exam anxiety with breathing techniques. "
                "Kwame tried a guided meditation for the first time and said it felt strange but calming. "
                "Elif organised a walk-and-talk session where students discussed worries while walking outside. "
                "Mei learned about the connection between screen time and sleep quality. "
                "She decided to stop using her tablet one hour before bedtime. "
                "Carlos started a healthy snack station in the common room with fruit and nuts. "
                "By the end of the week, students reported feeling more relaxed and focused. "
                "Mr. Demir reminded them, 'Taking care of your body and mind is not a break from learning. It is part of it.'"
            ),
            "cliffhanger": "Mei's sleep tracker data revealed something surprising that she wanted to share with the whole school.",
            "vocab_tie": ["wellbeing", "anxiety", "meditation", "balance", "nutrition"]
        },
        6: {
            "title": "Message from the Stars",
            "previously": "Wellness Week helped everyone recharge. Now Kwame had exciting news from his mentorship.",
            "episode": (
                "Dr. Asante invited Kwame's class to participate in a citizen science project about exoplanets. "
                "Mr. Demir agreed, and the whole class got access to real telescope data online. "
                "Kwame explained that an exoplanet is a planet outside our solar system. "
                "Elif asked, 'How can we find something so far away?' Kwame showed them the transit method. "
                "When a planet passes in front of its star, the star's brightness dips slightly. "
                "Mei wrote a simple program to detect brightness dips in the data sets. "
                "Carlos was fascinated by the idea that some exoplanets might be in the habitable zone. "
                "'That means they could have liquid water,' Kwame explained enthusiastically. "
                "After two weeks of analysis, Mei's program flagged a pattern in one data set. "
                "They reported it to Dr. Asante, who said it looked promising but needed further verification. "
                "The class was thrilled at the possibility of contributing to real scientific discovery. "
                "Mr. Demir said, 'The universe does not care how old you are. Curiosity has no age limit.'"
            ),
            "cliffhanger": "Dr. Asante confirmed the pattern was real and asked if the class wanted to name their discovery.",
            "vocab_tie": ["exoplanet", "telescope", "habitable", "transit", "citizen science"]
        },
        7: {
            "title": "Kwame's Story",
            "previously": "The class was celebrating their space discovery. But Kwame had been unusually quiet.",
            "episode": (
                "One afternoon, Mr. Demir started a lesson on migration and immigration. "
                "He asked students to share what they knew about why people move to new countries. "
                "Some mentioned war, jobs, education, and natural disasters. "
                "Kwame raised his hand slowly and said, 'My family moved here because of economic hardship.' "
                "The room went silent as Kwame described leaving his friends and school in Accra. "
                "He talked about learning Turkish from scratch and feeling invisible at first. "
                "Elif felt a lump in her throat; she had never thought about how hard it must have been. "
                "Mei shared that her parents had also moved far from home and sometimes felt lonely. "
                "Carlos mentioned that his uncle had migrated to the United States and faced discrimination. "
                "Mr. Demir showed a documentary about refugee children rebuilding their lives in new countries. "
                "After the film, the class discussed empathy, inclusion, and how small actions matter. "
                "They decided to create a Welcome Kit for new students arriving at the school."
            ),
            "cliffhanger": "The Welcome Kit idea grew bigger than expected when the school principal asked them to present it to the entire district.",
            "vocab_tie": ["migration", "refugee", "empathy", "inclusion", "discrimination"]
        },
        8: {
            "title": "Lights, Camera, Action",
            "previously": "The Welcome Kit project was gaining attention. Meanwhile, the school film festival was announced.",
            "episode": (
                "The annual school film festival was open to all grades, and Elif could hardly contain her excitement. "
                "She proposed that the four friends make a short documentary about their year together. "
                "Kwame would handle the music, Mei the editing, Carlos the script, and Elif the directing. "
                "They spent a week brainstorming themes and decided on 'Bridges, Not Walls.' "
                "Carlos wrote a script about how different cultures connect rather than divide. "
                "They interviewed classmates, teachers, and even the school janitor about belonging. "
                "Mei learned to use video editing software and added subtitles in four languages. "
                "Kwame composed a short drum piece that played during the opening and closing credits. "
                "During filming, they disagreed about a scene, and Elif had to learn to compromise. "
                "The final cut was seven minutes long, and they watched it together nervously. "
                "At the festival, their documentary received a standing ovation from the audience. "
                "A local TV station asked permission to feature a clip on their evening news programme."
            ),
            "cliffhanger": "A film school in Istanbul contacted Elif and offered the team a weekend workshop, but they needed a parent's permission.",
            "vocab_tie": ["documentary", "editing", "script", "compromise", "audience"]
        },
        9: {
            "title": "The Algorithm Trap",
            "previously": "The documentary success opened new doors. But Mei noticed something troubling online.",
            "episode": (
                "Mei realised that her social media feed only showed her things she already agreed with. "
                "She mentioned it to Mr. Demir, who explained the concept of filter bubbles and algorithms. "
                "'Algorithms learn what you like and show you more of the same,' he said. "
                "Elif connected this to their media literacy unit and said, 'So we might miss important perspectives.' "
                "Mr. Demir introduced a project: design an app concept that promotes digital wellbeing. "
                "Kwame suggested an app that reminds users to take breaks from screens. "
                "Mei designed an interface that shows users how much time they spend on each app category. "
                "Carlos proposed a feature that introduces content from different viewpoints every day. "
                "Elif added a news feed that mixes verified sources from multiple countries. "
                "They presented their concept, called 'OpenLens,' to the school's computer science teacher. "
                "She was impressed and suggested they enter a national student innovation competition. "
                "Mr. Demir warned, 'Technology is a powerful tool. Make sure you control it, not the other way around.'"
            ),
            "cliffhanger": "The innovation competition accepted their application, but they had only three weeks to build a working prototype.",
            "vocab_tie": ["algorithm", "filter bubble", "digital wellbeing", "prototype", "artificial intelligence"]
        },
        10: {
            "title": "Voices That Matter",
            "previously": "The OpenLens app prototype was nearly ready. Now Mr. Demir had one final challenge for the year.",
            "episode": (
                "For the last unit, Mr. Demir asked the class to explore human rights through personal stories. "
                "He showed them the Universal Declaration of Human Rights and asked which articles they connected with. "
                "Carlos immediately pointed to Article 14: the right to seek asylum. "
                "Kwame chose Article 26: the right to education, which he said changed his life. "
                "Mei selected Article 19: the right to freedom of opinion and expression. "
                "Elif picked Article 27: the right to participate in cultural life. "
                "Mr. Demir invited a guest speaker from a human rights organisation to talk to the class. "
                "She told them about children around the world who fight for their rights every day. "
                "The class decided to write letters to world leaders about issues they cared about. "
                "They also created a Human Rights Wall in the school corridor with illustrations and quotes. "
                "At the year-end ceremony, the principal praised their work and said the school was proud. "
                "Elif, Kwame, Mei, and Carlos looked at each other, knowing this year had changed them forever."
            ),
            "cliffhanger": "As summer began, they received a mysterious letter from an international youth organisation inviting them to a global summit.",
            "vocab_tie": ["human rights", "declaration", "asylum", "equality", "advocacy"]
        }
    }
}

# =============================================================================
# BANK 3: READING BANK (~200 words each)
# =============================================================================
READING_BANK = {
    7: {
        1: {
            "title": "Who Am I? The Many Layers of Identity",
            "text": (
                "Have you ever thought about what makes you 'you'? Identity is not just your name "
                "or where you come from. It is made up of many layers: your family, your language, "
                "your hobbies, your beliefs, and even the music you listen to. Psychologists say that "
                "identity begins forming in childhood but keeps changing throughout life. As teenagers, "
                "we start asking deeper questions like 'What do I believe in?' and 'What kind of person "
                "do I want to be?' Some people feel strongly connected to their nationality or religion, "
                "while others define themselves through their friendships or talents. Social media has "
                "added a new layer: our online identity. The way we present ourselves online might be "
                "different from who we are in real life. Experts warn that comparing ourselves to others "
                "online can hurt our self-esteem. The truth is, identity is not fixed. It is like a living "
                "document that you update as you grow. The important thing is to be honest with yourself "
                "and respect others for who they are. After all, a world where everyone was the same "
                "would be a very boring place."
            ),
            "pre_reading": [
                "What are three words you would use to describe yourself?",
                "Do you think your identity has changed in the last two years? How?",
                "Is your online identity the same as your real-life identity?"
            ],
            "post_reading": [
                "According to the text, when does identity begin forming?",
                "Name three things that can be part of someone's identity.",
                "What warning do experts give about social media and identity?",
                "Why does the author compare identity to a 'living document'?",
                "Do you agree that a world where everyone was the same would be boring? Why or why not?"
            ],
            "vocabulary": [
                {"word": "identity", "meaning": "who a person is; the qualities that make someone unique", "example": "Language is an important part of cultural identity."},
                {"word": "layer", "meaning": "one of several levels or parts", "example": "Her personality has many layers that people discover over time."},
                {"word": "psychologist", "meaning": "a scientist who studies the mind and behaviour", "example": "The psychologist helped her understand her feelings."},
                {"word": "belief", "meaning": "something you think is true or right", "example": "His belief in equality guides his decisions."},
                {"word": "self-esteem", "meaning": "how much you value and respect yourself", "example": "Positive feedback can improve a student's self-esteem."},
                {"word": "nationality", "meaning": "the country where someone is a citizen", "example": "People of any nationality can apply for the programme."},
                {"word": "define", "meaning": "to describe or explain the meaning of something", "example": "How would you define happiness?"},
                {"word": "compare", "meaning": "to look at differences and similarities", "example": "Do not compare yourself to others on social media."},
                {"word": "respect", "meaning": "to show care and consideration for someone", "example": "We should respect people who are different from us."},
                {"word": "talent", "meaning": "a natural ability to do something well", "example": "She has a real talent for drawing."}
            ],
            "reading_strategy": "Activate prior knowledge: Before reading, think about your own identity and what shapes it. This helps you connect personally with the text."
        },
        2: {
            "title": "Wedding Traditions Around the World",
            "text": (
                "Weddings are celebrated in almost every culture, but the traditions can be very different. "
                "In Turkey, a bride's hands are decorated with beautiful henna patterns the night before "
                "the wedding. This ceremony, called Kina Gecesi, is full of music, dancing, and sometimes "
                "tears of joy. In India, weddings often last several days and include colourful clothing, "
                "flower garlands, and a sacred fire ceremony. Japanese weddings can follow Shinto traditions "
                "where the couple drinks sake three times to seal their bond. In Scotland, the bride and "
                "groom sometimes jump over a broomstick, symbolising a new beginning. Nigerian Yoruba "
                "weddings involve tasting four flavours: sour, bitter, spicy, and sweet, which represent "
                "the different experiences of married life. In some South American countries, the couple "
                "releases butterflies to symbolise a fresh start. While these customs look different on the "
                "outside, they all share common themes: love, family, commitment, and hope for the future. "
                "Understanding wedding traditions from other cultures helps us appreciate diversity and "
                "see how much we actually have in common."
            ),
            "pre_reading": [
                "Have you ever been to a wedding? What traditions did you see?",
                "Why do you think weddings have special customs?",
                "Can you name a wedding tradition from another country?"
            ],
            "post_reading": [
                "What is Kina Gecesi?",
                "How many times does a couple drink sake in a Japanese Shinto wedding?",
                "What do the four flavours represent in a Yoruba wedding?",
                "What common themes do all wedding traditions share?",
                "Which tradition from the text do you find most interesting? Why?"
            ],
            "vocabulary": [
                {"word": "tradition", "meaning": "a custom or belief passed down through generations", "example": "It is a tradition to eat special food during holidays."},
                {"word": "ceremony", "meaning": "a formal event with special actions or words", "example": "The opening ceremony of the Olympics is always spectacular."},
                {"word": "henna", "meaning": "a natural dye used to make patterns on skin", "example": "The bride had beautiful henna designs on her hands."},
                {"word": "garland", "meaning": "a ring or string of flowers or leaves", "example": "They decorated the hall with colourful garlands."},
                {"word": "sacred", "meaning": "holy; connected to religious belief", "example": "The river is considered sacred by the local people."},
                {"word": "symbolise", "meaning": "to represent or stand for something", "example": "A white dove symbolises peace."},
                {"word": "commitment", "meaning": "a promise or dedication to something", "example": "Marriage is a lifelong commitment."},
                {"word": "diversity", "meaning": "the state of having many different types", "example": "Cultural diversity makes our city interesting."},
                {"word": "appreciate", "meaning": "to understand and value something", "example": "Travelling helps you appreciate other cultures."},
                {"word": "custom", "meaning": "a traditional way of doing things in a society", "example": "It is a custom to remove your shoes before entering a home in Japan."}
            ],
            "reading_strategy": "Compare and contrast: As you read, note how wedding traditions differ and what they share in common using a simple chart."
        },
        3: {
            "title": "Jobs That Did Not Exist 10 Years Ago",
            "text": (
                "The world of work is changing faster than ever. Many of today's popular jobs did not "
                "exist ten years ago. Social media managers, for example, help companies communicate with "
                "customers through platforms like Instagram and Twitter. App developers create the programmes "
                "we use every day on our phones. Drone pilots are now hired for photography, agriculture, "
                "and even delivering packages. Data scientists analyse huge amounts of information to help "
                "businesses make better decisions. Sustainability consultants advise companies on how to be "
                "more environmentally friendly. E-sports coaches train professional video game players who "
                "compete for millions of dollars in prizes. Even the field of medicine has new roles: genetic "
                "counsellors help people understand their DNA and health risks. Experts predict that 65 percent "
                "of children starting school today will work in jobs that have not been invented yet. This means "
                "that learning how to learn is more important than memorising facts. Skills like critical thinking, "
                "creativity, communication, and adaptability will be essential for the careers of the future. "
                "So whatever you dream of becoming, stay curious and keep learning."
            ),
            "pre_reading": [
                "What job do you dream of having in the future?",
                "Can you think of a job that is new in the last few years?",
                "What skills do you think future workers will need?"
            ],
            "post_reading": [
                "Name three jobs mentioned in the text that did not exist ten years ago.",
                "What does a sustainability consultant do?",
                "What percentage of today's children may work in jobs not yet invented?",
                "Why does the text say 'learning how to learn' is important?",
                "Which new job from the text interests you most? Explain why."
            ],
            "vocabulary": [
                {"word": "career", "meaning": "a job or profession that someone does for a long time", "example": "She is planning a career in engineering."},
                {"word": "platform", "meaning": "a system or service used to share content", "example": "YouTube is a popular video platform."},
                {"word": "drone", "meaning": "an unmanned flying device controlled remotely", "example": "The drone took amazing photos of the coastline."},
                {"word": "analyse", "meaning": "to examine something in detail to understand it", "example": "Scientists analyse data to find patterns."},
                {"word": "sustainability", "meaning": "using resources in a way that protects the environment", "example": "Sustainability is important for the future of our planet."},
                {"word": "compete", "meaning": "to try to win against others", "example": "Teams from 20 countries will compete in the tournament."},
                {"word": "genetic", "meaning": "related to genes and DNA", "example": "Genetic research helps us understand diseases better."},
                {"word": "predict", "meaning": "to say what will happen in the future", "example": "Experts predict that AI will change many industries."},
                {"word": "adaptability", "meaning": "the ability to change and adjust to new situations", "example": "Adaptability is a key skill in today's job market."},
                {"word": "essential", "meaning": "absolutely necessary; very important", "example": "Good communication is essential for teamwork."}
            ],
            "reading_strategy": "Make predictions: Before reading each paragraph, guess what new jobs might be mentioned. Check your predictions as you read."
        },
        4: {
            "title": "Can You Spot Fake News?",
            "text": (
                "Every day, millions of news stories are shared online, but not all of them are true. "
                "Fake news is false information that is made to look like real news. It is designed to "
                "trick people, influence opinions, or get clicks for advertising money. Fake news is not "
                "new: propaganda has existed for centuries. However, social media has made it easier to "
                "spread false stories quickly. A study by MIT found that fake news travels six times faster "
                "than true stories on social media. So how can you protect yourself? First, check the source. "
                "Is the website well-known and trusted? Second, read beyond the headline. Many people share "
                "articles without reading them fully. Third, look for other sources reporting the same story. "
                "If only one website has the news, be suspicious. Fourth, check the date. Old stories are "
                "sometimes shared again to confuse people. Fifth, use fact-checking websites like Snopes or "
                "Teyit.org. Finally, think about your own biases. We tend to believe stories that match our "
                "existing opinions. Being a critical media consumer is one of the most important skills in "
                "the modern world."
            ),
            "pre_reading": [
                "Have you ever believed a story that turned out to be false?",
                "Where do you usually get your news?",
                "How do you decide if a news story is trustworthy?"
            ],
            "post_reading": [
                "What is fake news designed to do?",
                "According to MIT, how much faster does fake news travel than true stories?",
                "List three ways to check if a news story is real.",
                "Why might old stories be shared again?",
                "What role do personal biases play in believing fake news?"
            ],
            "vocabulary": [
                {"word": "fake", "meaning": "not real; false or imitation", "example": "The fake news story confused thousands of people."},
                {"word": "propaganda", "meaning": "information used to promote a particular point of view", "example": "During the war, propaganda posters were everywhere."},
                {"word": "influence", "meaning": "to have an effect on someone's thoughts or actions", "example": "Advertisements try to influence what we buy."},
                {"word": "headline", "meaning": "the title of a news article", "example": "The headline was shocking, but the story was exaggerated."},
                {"word": "suspicious", "meaning": "feeling that something is wrong or not trustworthy", "example": "I was suspicious because the offer seemed too good to be true."},
                {"word": "fact-checking", "meaning": "verifying whether information is true", "example": "Fact-checking websites help fight misinformation."},
                {"word": "bias", "meaning": "an unfair preference for or against something", "example": "Everyone has biases, but we should try to be aware of them."},
                {"word": "consumer", "meaning": "a person who buys or uses products/services/information", "example": "As media consumers, we need to be critical."},
                {"word": "source", "meaning": "where information comes from", "example": "Always check the source before sharing a story."},
                {"word": "verify", "meaning": "to check that something is true or correct", "example": "Journalists must verify facts before publishing."}
            ],
            "reading_strategy": "Question the text: As you read, write questions in the margins. Ask 'How do they know this?' and 'Is this fact or opinion?'"
        },
        5: {
            "title": "The Science of Sleep",
            "text": (
                "Most teenagers need between eight and ten hours of sleep each night, but studies show "
                "that many get less than seven. Why does sleep matter so much? During sleep, your brain "
                "does important work. It organises memories, processes emotions, and clears out waste products. "
                "Without enough sleep, you may have trouble concentrating, feel irritable, and even get sick "
                "more often. Researchers have found that sleep-deprived students score lower on tests, not "
                "because they are less intelligent but because their brains cannot function properly. The "
                "blue light from phones and tablets is a major sleep thief. It tricks your brain into thinking "
                "it is still daytime, which delays the production of melatonin, the sleep hormone. Experts "
                "recommend stopping screen use at least one hour before bed. Other sleep tips include keeping "
                "a regular schedule, making your room cool and dark, and avoiding caffeine after lunch. "
                "Physical exercise also improves sleep quality, but try to finish exercising at least three "
                "hours before bedtime. Think of sleep as charging your phone: you would not expect your "
                "phone to work well on 20 percent battery, so why expect your brain to?"
            ),
            "pre_reading": [
                "How many hours of sleep do you usually get?",
                "Do you use your phone before going to bed?",
                "How do you feel on days when you do not sleep well?"
            ],
            "post_reading": [
                "How many hours of sleep do teenagers need according to the text?",
                "What three things does the brain do during sleep?",
                "Why is blue light bad for sleep?",
                "Name two tips for better sleep from the text.",
                "Do you think the phone-battery comparison is a good one? Why?"
            ],
            "vocabulary": [
                {"word": "concentrate", "meaning": "to focus your attention on something", "example": "It is hard to concentrate when you are tired."},
                {"word": "irritable", "meaning": "easily annoyed or upset", "example": "Lack of sleep makes people irritable."},
                {"word": "sleep-deprived", "meaning": "not having enough sleep", "example": "Sleep-deprived students struggle in exams."},
                {"word": "function", "meaning": "to work or operate properly", "example": "Your brain cannot function well without rest."},
                {"word": "melatonin", "meaning": "a hormone that helps control sleep", "example": "Blue light reduces melatonin production."},
                {"word": "hormone", "meaning": "a chemical in the body that controls certain processes", "example": "Growth hormones are active during sleep."},
                {"word": "caffeine", "meaning": "a substance in coffee and tea that keeps you awake", "example": "Too much caffeine can disturb your sleep."},
                {"word": "schedule", "meaning": "a planned list of times for activities", "example": "A regular sleep schedule helps your body clock."},
                {"word": "quality", "meaning": "how good or bad something is", "example": "The quality of your sleep matters more than the quantity."},
                {"word": "recommend", "meaning": "to suggest as a good idea", "example": "Doctors recommend eight hours of sleep for teens."}
            ],
            "reading_strategy": "Summarise paragraphs: After each section, write a one-sentence summary. This helps you identify the main ideas."
        },
        6: {
            "title": "Life on Other Planets?",
            "text": (
                "Are we alone in the universe? This question has fascinated humans for thousands of years. "
                "Today, scientists are closer than ever to finding an answer. NASA's Kepler space telescope "
                "discovered over 2,600 exoplanets, some of which are in the habitable zone of their stars. "
                "The habitable zone, sometimes called the Goldilocks zone, is the area around a star where "
                "conditions might be right for liquid water to exist. Water is considered essential for life "
                "as we know it. Mars is another focus of research. NASA's Perseverance rover has been "
                "collecting rock samples on Mars since 2021, looking for signs of ancient microbial life. "
                "Scientists have also found interesting moons in our solar system. Europa, a moon of Jupiter, "
                "has a vast ocean beneath its icy surface. Enceladus, a moon of Saturn, shoots water geysers "
                "into space. Both could potentially harbour life. Meanwhile, the James Webb Space Telescope "
                "is analysing the atmospheres of distant exoplanets, searching for biosignatures like oxygen "
                "and methane. While we have not found alien life yet, the evidence suggests that the building "
                "blocks of life are common in the universe. The question may not be if we find life, but when."
            ),
            "pre_reading": [
                "Do you think there is life on other planets?",
                "What do you know about Mars exploration?",
                "What conditions does a planet need to support life?"
            ],
            "post_reading": [
                "What is the 'Goldilocks zone'?",
                "How many exoplanets did the Kepler telescope discover?",
                "Why are Europa and Enceladus interesting to scientists?",
                "What is the James Webb Space Telescope searching for?",
                "The text ends with 'The question may not be if, but when.' What does this mean?"
            ],
            "vocabulary": [
                {"word": "universe", "meaning": "everything that exists, including all space and matter", "example": "The universe contains billions of galaxies."},
                {"word": "exoplanet", "meaning": "a planet outside our solar system", "example": "Scientists have discovered thousands of exoplanets."},
                {"word": "habitable", "meaning": "suitable for living in", "example": "The habitable zone is where liquid water can exist."},
                {"word": "telescope", "meaning": "an instrument used to see distant objects", "example": "The new telescope can see galaxies billions of light-years away."},
                {"word": "microbial", "meaning": "relating to very tiny living organisms", "example": "Microbial life might exist under the surface of Mars."},
                {"word": "atmosphere", "meaning": "the layer of gases surrounding a planet", "example": "Earth's atmosphere protects us from harmful radiation."},
                {"word": "biosignature", "meaning": "a sign of life, past or present", "example": "Oxygen in a planet's atmosphere could be a biosignature."},
                {"word": "geyser", "meaning": "a natural spring that shoots hot water or steam", "example": "Enceladus has water geysers erupting from its surface."},
                {"word": "evidence", "meaning": "facts or information showing something is true", "example": "There is growing evidence that water once existed on Mars."},
                {"word": "potential", "meaning": "possible; capable of becoming real", "example": "Europa has the potential to harbour life."}
            ],
            "reading_strategy": "Visualise: As you read about planets and moons, create mental images or quick sketches. This helps you remember scientific concepts."
        },
        7: {
            "title": "A Journey Without a Map",
            "text": (
                "Every year, millions of people leave their homes and move to a new country. Some migrate "
                "by choice for better jobs or education. Others are forced to flee because of war, persecution, "
                "or natural disasters. According to the United Nations, there are over 100 million forcibly "
                "displaced people worldwide. Refugees face enormous challenges: learning a new language, "
                "finding work, and rebuilding their lives from scratch. Children are especially affected. "
                "Many miss months or years of school and struggle to make friends in unfamiliar places. "
                "However, history shows that immigrants have made tremendous contributions to their new "
                "countries. Albert Einstein was a refugee from Nazi Germany. Freddie Mercury's family fled "
                "violence in Zanzibar. The founder of Google, Sergey Brin, immigrated from Russia as a child. "
                "Countries that welcome immigrants often benefit from their skills, ideas, and cultural richness. "
                "Integration is a two-way process: newcomers adapt to their new home, and the host community "
                "opens its doors. When we see a refugee, we should not just see a statistic. We should see "
                "a person with dreams, talents, and a story worth hearing."
            ),
            "pre_reading": [
                "Why do people move to different countries?",
                "Do you know anyone who has moved to a new country?",
                "What challenges might a new student from another country face at your school?"
            ],
            "post_reading": [
                "What is the difference between choosing to migrate and being forced to flee?",
                "How many forcibly displaced people are there according to the UN?",
                "Name two famous people mentioned who were immigrants or refugees.",
                "What does the text mean by 'integration is a two-way process'?",
                "How can you help a new student from another country feel welcome?"
            ],
            "vocabulary": [
                {"word": "migrate", "meaning": "to move from one place to another to live", "example": "Many birds migrate south during winter."},
                {"word": "refugee", "meaning": "a person forced to leave their country due to danger", "example": "The camp provides shelter for thousands of refugees."},
                {"word": "persecution", "meaning": "cruel treatment because of race, religion, or beliefs", "example": "They fled their country because of religious persecution."},
                {"word": "displaced", "meaning": "forced to leave one's home", "example": "Millions of displaced families need humanitarian aid."},
                {"word": "contribution", "meaning": "something given or done to help", "example": "Immigrants make valuable contributions to society."},
                {"word": "integration", "meaning": "the process of becoming part of a group or society", "example": "Language classes support the integration of newcomers."},
                {"word": "adapt", "meaning": "to change to fit new conditions", "example": "It takes time to adapt to a new culture."},
                {"word": "tremendous", "meaning": "very great in amount or quality", "example": "She showed tremendous courage during difficult times."},
                {"word": "statistic", "meaning": "a number that represents a fact or measurement", "example": "Behind every statistic is a real person."},
                {"word": "humanitarian", "meaning": "concerned with improving people's lives and reducing suffering", "example": "The organisation provides humanitarian aid to refugees."}
            ],
            "reading_strategy": "Identify author's purpose: Ask yourself why the author chose certain examples and what message they want you to take away."
        },
        8: {
            "title": "How Movies Shape Our World",
            "text": (
                "Films are more than just entertainment. They shape how we see the world, influence our "
                "emotions, and even change society. Think about how many people learned about the Titanic "
                "disaster through James Cameron's 1997 film rather than a history book. Movies have the "
                "power to build empathy by letting us experience life through someone else's eyes. When "
                "we watch a character struggle with poverty, discrimination, or loss, we develop a deeper "
                "understanding of those issues. The film industry is also a mirror of culture. Bollywood "
                "reflects Indian values and dreams, Nollywood tells African stories, and Turkish diziler "
                "have become popular worldwide for their emotional depth. However, films can also spread "
                "stereotypes. For decades, Hollywood often portrayed certain groups in negative or one-dimensional "
                "ways. Today, there is a growing movement for better representation in cinema. Films like "
                "'Coco' celebrate Mexican culture, and 'Capernaum' brought attention to refugee children's "
                "struggles. The technology of filmmaking has also changed dramatically. Anyone with a smartphone "
                "can now make a short film and share it with the world. This democratisation of filmmaking means "
                "that more diverse voices can be heard than ever before."
            ),
            "pre_reading": [
                "What is your favourite film and why?",
                "Have you ever learned something new from watching a movie?",
                "Do you think films can change the way people think?"
            ],
            "post_reading": [
                "How do movies build empathy according to the text?",
                "What are Bollywood and Nollywood?",
                "What problem does the text mention about Hollywood's history?",
                "What does 'democratisation of filmmaking' mean?",
                "Can you think of a film that taught you something about another culture?"
            ],
            "vocabulary": [
                {"word": "entertainment", "meaning": "activities that give people enjoyment", "example": "Films are one of the most popular forms of entertainment."},
                {"word": "empathy", "meaning": "the ability to understand and share someone's feelings", "example": "Good films create empathy for the characters."},
                {"word": "stereotype", "meaning": "an oversimplified or unfair idea about a group", "example": "We should challenge stereotypes in the media."},
                {"word": "representation", "meaning": "showing different types of people fairly", "example": "Better representation in films helps everyone feel included."},
                {"word": "portray", "meaning": "to show or describe someone in a particular way", "example": "The film portrays village life beautifully."},
                {"word": "one-dimensional", "meaning": "lacking depth; showing only one side", "example": "The villain was a one-dimensional character with no backstory."},
                {"word": "dramatically", "meaning": "in a very noticeable or significant way", "example": "Technology has changed dramatically in the last decade."},
                {"word": "movement", "meaning": "a group of people working together for a cause", "example": "The movement for equality in cinema is growing."},
                {"word": "diverse", "meaning": "including many different types of people or things", "example": "A diverse cast makes films more interesting."},
                {"word": "cinema", "meaning": "the art or industry of making films", "example": "Turkish cinema has gained international recognition."}
            ],
            "reading_strategy": "Connect to personal experience: Think of films you have watched that relate to the points in the text. Personal connections make reading more meaningful."
        },
        9: {
            "title": "Living with Artificial Intelligence",
            "text": (
                "Artificial intelligence is no longer science fiction. It is part of our daily lives. "
                "When you ask a voice assistant a question, use a translation app, or get recommendations "
                "on a streaming service, you are using AI. But what exactly is AI? In simple terms, it is "
                "a computer system that can perform tasks that normally require human intelligence, such as "
                "recognising speech, making decisions, and translating languages. Machine learning, a branch "
                "of AI, allows computers to learn from data without being explicitly programmed. This is how "
                "your email filters spam and how social media knows which posts to show you. AI has enormous "
                "potential in fields like healthcare, where it can help detect diseases early, and education, "
                "where it can personalise learning for each student. However, AI also raises concerns. "
                "Some worry about job losses as machines replace human workers. Others are concerned about "
                "privacy, since AI systems collect vast amounts of personal data. There is also the question "
                "of bias: if AI learns from biased data, it can make unfair decisions. The key is to develop "
                "AI responsibly and ensure that humans remain in control. Technology should serve people, "
                "not the other way around."
            ),
            "pre_reading": [
                "What examples of AI do you use in your daily life?",
                "Do you think AI is helpful or dangerous? Why?",
                "Can a computer ever be as smart as a human?"
            ],
            "post_reading": [
                "How does the text define artificial intelligence?",
                "What is machine learning?",
                "Name two fields where AI has great potential.",
                "What are three concerns about AI mentioned in the text?",
                "Do you agree that 'technology should serve people'? Explain."
            ],
            "vocabulary": [
                {"word": "artificial intelligence", "meaning": "computer systems that can do tasks needing human-like thinking", "example": "Artificial intelligence is used in self-driving cars."},
                {"word": "algorithm", "meaning": "a set of rules a computer follows to solve problems", "example": "The algorithm decides which videos to recommend."},
                {"word": "machine learning", "meaning": "AI that improves itself by learning from data", "example": "Machine learning helps detect fraud in banking."},
                {"word": "data", "meaning": "information collected for analysis", "example": "The app collects data about your reading habits."},
                {"word": "privacy", "meaning": "the right to keep personal information secret", "example": "Online privacy is a major concern today."},
                {"word": "detect", "meaning": "to discover or notice something", "example": "The AI can detect diseases from medical images."},
                {"word": "personalise", "meaning": "to make something suitable for a specific person", "example": "AI can personalise learning materials for each student."},
                {"word": "responsible", "meaning": "acting with care and thinking about consequences", "example": "We must develop AI in a responsible way."},
                {"word": "replace", "meaning": "to take the place of something or someone", "example": "Some fear that robots will replace human workers."},
                {"word": "vast", "meaning": "extremely large in amount or size", "example": "AI systems process vast amounts of data every second."}
            ],
            "reading_strategy": "KWL chart: Before reading, write what you Know and Want to know about AI. After reading, fill in what you Learned."
        },
        10: {
            "title": "Children Who Changed the World",
            "text": (
                "You do not have to be an adult to fight for human rights. Throughout history, young people "
                "have stood up for justice and made a real difference. Malala Yousafzai was just 15 when "
                "she was attacked for defending girls' right to education in Pakistan. She survived and became "
                "the youngest Nobel Peace Prize winner at age 17. Iqbal Masih was a Pakistani boy who escaped "
                "child labour at age 10 and helped free over 3,000 children from bonded labour before his "
                "tragic death at 12. Greta Thunberg started her school strike for climate action alone outside "
                "the Swedish parliament at age 15, inspiring millions worldwide. In the United States, Ruby "
                "Bridges was only six years old when she became the first African American child to attend an "
                "all-white school in the South, facing angry crowds with quiet dignity. Thandiwe Chama from "
                "Zambia was eight when she led fellow students on a march after their school was closed, "
                "eventually winning an international children's peace prize. These young activists prove that "
                "age is not a barrier to courage. Every person, no matter how young, has the power to speak "
                "up against injustice and create positive change in the world."
            ),
            "pre_reading": [
                "Can you name a young person who has made a difference in the world?",
                "What human rights issue do you care about most?",
                "Do you think young people can change the world? Why or why not?"
            ],
            "post_reading": [
                "At what age did Malala Yousafzai win the Nobel Peace Prize?",
                "What did Iqbal Masih fight against?",
                "How did Greta Thunberg start her climate activism?",
                "Why was Ruby Bridges' action significant?",
                "Which young activist from the text inspires you most, and what would you fight for?"
            ],
            "vocabulary": [
                {"word": "human rights", "meaning": "basic rights that every person is entitled to", "example": "Education is a fundamental human right."},
                {"word": "justice", "meaning": "fairness and equal treatment for all", "example": "They marched for justice and equality."},
                {"word": "activist", "meaning": "a person who campaigns for social or political change", "example": "The young activist spoke at the United Nations."},
                {"word": "dignity", "meaning": "the quality of being worthy of respect", "example": "She faced the crowd with courage and dignity."},
                {"word": "bonded labour", "meaning": "a form of forced work to pay off debt", "example": "Millions of children worldwide are trapped in bonded labour."},
                {"word": "parliament", "meaning": "the group of people who make laws for a country", "example": "She protested outside parliament every Friday."},
                {"word": "courage", "meaning": "the ability to do something that is difficult or scary", "example": "It takes courage to stand up for what is right."},
                {"word": "injustice", "meaning": "unfair treatment or a situation that is not just", "example": "We should all speak up against injustice."},
                {"word": "barrier", "meaning": "something that prevents progress", "example": "Age should not be a barrier to making a difference."},
                {"word": "inspire", "meaning": "to fill someone with the desire to do something", "example": "Malala's story inspired millions of young girls."}
            ],
            "reading_strategy": "Emotional response journal: Write down how you feel as you read each activist's story. Emotions help deepen understanding and memory."
        }
    }
}

# =============================================================================
# BANK 4: GRAMMAR BANK
# =============================================================================
GRAMMAR_BANK = {
    7: {
        1: {
            "topic": "Present Perfect Continuous",
            "explanation": (
                "We use the Present Perfect Continuous to talk about actions that started in the past and "
                "are still continuing now, or have recently stopped. The structure is: subject + have/has + "
                "been + verb-ing. We often use 'for' (a period of time) and 'since' (a point in time) with "
                "this tense. It emphasises the duration or ongoing nature of an activity."
            ),
            "examples": [
                "I have been studying English for three years.",
                "She has been living in Istanbul since 2022.",
                "They have been waiting for the bus for twenty minutes.",
                "He has been playing the guitar since he was eight.",
                "We have been working on this project all morning."
            ],
            "exercises": [
                {
                    "instruction": "Complete the sentences with the Present Perfect Continuous form of the verb in brackets.",
                    "items": [
                        "I ___ (learn) Turkish since September.",
                        "She ___ (read) that book for two weeks.",
                        "They ___ (practise) for the concert all day.",
                        "He ___ (run) for an hour. He looks tired.",
                        "We ___ (plan) this trip since January."
                    ]
                },
                {
                    "instruction": "Choose 'for' or 'since' to complete each sentence.",
                    "items": [
                        "I have been studying ___ 9 o'clock.",
                        "She has been dancing ___ three hours.",
                        "They have been friends ___ primary school.",
                        "He has been cooking ___ lunchtime.",
                        "We have been living here ___ five years."
                    ]
                },
                {
                    "instruction": "Rewrite the sentences using the Present Perfect Continuous.",
                    "items": [
                        "I started learning the piano two years ago. (I still learn it.)",
                        "She began working here in March. (She still works here.)",
                        "They started playing at 3 PM. (They are still playing.)",
                        "He started writing his essay this morning. (He is still writing.)",
                        "We began waiting at noon. (We are still waiting.)"
                    ]
                },
                {
                    "instruction": "Correct the mistakes in these sentences.",
                    "items": [
                        "She have been studying all day.",
                        "I has been waiting since two hours.",
                        "They been working on the project.",
                        "He has been play football since 4 PM.",
                        "We have been know each other for years."
                    ]
                }
            ],
            "tip": "Use Present Perfect Continuous for actions that are ongoing. Use Present Perfect Simple for completed actions or results: 'I have written three emails' (finished) vs. 'I have been writing emails' (still going)."
        },
        2: {
            "topic": "Past Perfect (Introduction)",
            "explanation": (
                "The Past Perfect is used to show that one action happened before another action in the past. "
                "The structure is: subject + had + past participle. Think of it as 'the past of the past.' "
                "We often use it with 'before,' 'after,' 'when,' 'by the time,' and 'already.' It helps make "
                "the order of past events clear."
            ),
            "examples": [
                "When I arrived at the station, the train had already left.",
                "She had finished her homework before dinner.",
                "They had never seen snow before they moved to Erzurum.",
                "By the time the teacher came, the students had cleaned the classroom.",
                "He had lived in three countries before he turned twelve."
            ],
            "exercises": [
                {
                    "instruction": "Complete the sentences with the Past Perfect form of the verb in brackets.",
                    "items": [
                        "When I got home, my sister ___ (already/eat) dinner.",
                        "They ___ (not/visit) Turkey before last summer.",
                        "By the time the film started, we ___ (buy) popcorn.",
                        "She was sad because she ___ (lose) her favourite book.",
                        "The match ___ (already/begin) when we arrived."
                    ]
                },
                {
                    "instruction": "Put the events in the correct order and write sentences using the Past Perfect.",
                    "items": [
                        "The bus left. / I arrived at the stop. (When I arrived...)",
                        "She studied hard. / She passed the exam. (She passed because...)",
                        "They ate lunch. / They went to the park. (After they...)",
                        "He saved money. / He bought a bicycle. (He bought a bicycle after...)",
                        "The rain stopped. / We went outside. (We went outside after...)"
                    ]
                },
                {
                    "instruction": "Choose the correct tense: Past Simple or Past Perfect.",
                    "items": [
                        "By the time I woke up, my mum ___ (prepared / had prepared) breakfast.",
                        "She ___ (went / had gone) to bed after she finished studying.",
                        "We ___ (were / had been) tired because we walked for hours.",
                        "He ___ (didn't know / hadn't known) anyone when he started school.",
                        "They ___ (arrived / had arrived) before the ceremony began."
                    ]
                },
                {
                    "instruction": "Write sentences about your own life using the Past Perfect.",
                    "items": [
                        "By the time I was 10, I had...",
                        "Before I started secondary school, I had...",
                        "When I arrived at school today, my friend had already...",
                        "I was happy because I had...",
                        "By last summer, I had never..."
                    ]
                }
            ],
            "tip": "The Past Perfect is like a 'flashback' in a film. It takes you to an earlier point in a past story. If both actions are in sequence, you can often use Past Simple for both, but Past Perfect makes the order clearer."
        },
        3: {
            "topic": "Second Conditional",
            "explanation": (
                "We use the Second Conditional to talk about imaginary or unlikely situations in the present "
                "or future. The structure is: If + past simple, would + base verb. Even though we use past "
                "tense, we are talking about the present or future. We often use 'were' instead of 'was' in "
                "formal English: 'If I were you...' It is great for giving advice or imagining different scenarios."
            ),
            "examples": [
                "If I had a time machine, I would visit ancient Egypt.",
                "If she lived near the sea, she would swim every day.",
                "If we won the lottery, we would travel around the world.",
                "If I were you, I would study harder for the exam.",
                "If they spoke Turkish, they would understand the film."
            ],
            "exercises": [
                {
                    "instruction": "Complete the Second Conditional sentences with the correct form of the verb.",
                    "items": [
                        "If I ___ (be) the president, I ___ (build) more schools.",
                        "If she ___ (have) more time, she ___ (learn) to play the violin.",
                        "If we ___ (live) in Japan, we ___ (eat) sushi every day.",
                        "If he ___ (can) fly, he ___ (visit) every country.",
                        "If they ___ (not/have) homework, they ___ (play) outside."
                    ]
                },
                {
                    "instruction": "Match the beginnings with the endings.",
                    "items": [
                        "If I found a wallet on the street, ... (a) she would be a great singer.",
                        "If we didn't have school tomorrow, ... (b) I would take it to the police.",
                        "If she practised more, ... (c) they would save endangered animals.",
                        "If they had enough money, ... (d) we would stay up late.",
                        "If I were invisible, ... (e) I would sneak into a concert."
                    ]
                },
                {
                    "instruction": "Give advice using 'If I were you, I would...'",
                    "items": [
                        "Your friend is always tired. (go to bed earlier)",
                        "Your classmate failed the test. (study more regularly)",
                        "Your brother wants to get fit. (join a sports team)",
                        "Your friend is bored at weekends. (try a new hobby)",
                        "Your sister has an argument with her friend. (talk to her calmly)"
                    ]
                },
                {
                    "instruction": "Write your own Second Conditional sentences about these topics.",
                    "items": [
                        "Having a superpower",
                        "Living in another country",
                        "Meeting a famous person",
                        "Being a teacher for one day",
                        "Finding a treasure chest"
                    ]
                }
            ],
            "tip": "Remember: First Conditional = real/possible (If it rains, I will stay home). Second Conditional = imaginary/unlikely (If I were a bird, I would fly south). The difference is about probability, not time."
        },
        4: {
            "topic": "Passive Voice (Present and Past Simple)",
            "explanation": (
                "We use the passive voice when the action is more important than who does it, or when "
                "we do not know who did it. Present Simple Passive: am/is/are + past participle. Past "
                "Simple Passive: was/were + past participle. We use 'by' to mention who performs the action "
                "if needed. The passive is common in news reports, scientific writing, and formal texts."
            ),
            "examples": [
                "English is spoken in many countries. (Present Simple Passive)",
                "This school was built in 1985. (Past Simple Passive)",
                "The news is read by millions of people every day.",
                "The window was broken during the storm.",
                "Coffee is grown in Brazil and Colombia."
            ],
            "exercises": [
                {
                    "instruction": "Rewrite these sentences in the passive voice.",
                    "items": [
                        "They speak French in Canada.",
                        "Someone stole my bicycle yesterday.",
                        "People watch this programme every Friday.",
                        "Alexander Graham Bell invented the telephone.",
                        "They clean the classrooms every evening."
                    ]
                },
                {
                    "instruction": "Complete the sentences with the correct passive form.",
                    "items": [
                        "Turkish ___ (speak) by about 80 million people.",
                        "The Eiffel Tower ___ (build) in 1889.",
                        "Homework ___ (give) every day by our teacher.",
                        "The Olympic Games ___ (hold) every four years.",
                        "This song ___ (write) by a famous musician."
                    ]
                },
                {
                    "instruction": "Choose Active or Passive to complete each sentence correctly.",
                    "items": [
                        "The cake ___ (baked / was baked) by my grandmother.",
                        "Scientists ___ (discovered / were discovered) a new species.",
                        "Football ___ (plays / is played) in almost every country.",
                        "She ___ (awarded / was awarded) a prize for her project.",
                        "The students ___ (finished / were finished) the test on time."
                    ]
                },
                {
                    "instruction": "Write passive sentences about these facts.",
                    "items": [
                        "Paper / invent / China (Past)",
                        "The Mona Lisa / paint / Leonardo da Vinci (Past)",
                        "Rice / grow / many Asian countries (Present)",
                        "The news / broadcast / every evening (Present)",
                        "This bridge / design / a famous architect (Past)"
                    ]
                }
            ],
            "tip": "Not every sentence should be passive. Use the active voice when you want to emphasise who does the action. Use the passive when the action or result is more important than the doer."
        },
        5: {
            "topic": "Relative Clauses (who / which / that / where)",
            "explanation": (
                "Relative clauses give extra information about a noun. We use 'who' for people, 'which' "
                "for things and animals, 'that' for both people and things, and 'where' for places. "
                "Defining relative clauses are essential for understanding the sentence and do not use commas. "
                "They help us combine two short sentences into one, making our writing more sophisticated."
            ),
            "examples": [
                "The teacher who teaches us science is very funny.",
                "The book which I borrowed from the library is excellent.",
                "This is the school where my parents studied.",
                "The film that we watched last night was exciting.",
                "The girl who sits next to me speaks three languages."
            ],
            "exercises": [
                {
                    "instruction": "Join the sentences using who, which, that, or where.",
                    "items": [
                        "I have a friend. She lives in London.",
                        "This is the museum. We saw dinosaur skeletons there.",
                        "He bought a phone. It has an amazing camera.",
                        "The man is a doctor. He lives next door.",
                        "This is the restaurant. We had our birthday dinner there."
                    ]
                },
                {
                    "instruction": "Fill in the blanks with who, which, that, or where.",
                    "items": [
                        "The students ___ passed the exam are very happy.",
                        "Istanbul is a city ___ East meets West.",
                        "The laptop ___ I use for homework is quite old.",
                        "The woman ___ helped us was very kind.",
                        "This is the park ___ we play football every Saturday."
                    ]
                },
                {
                    "instruction": "Correct the errors in these relative clause sentences.",
                    "items": [
                        "The boy which won the race is my cousin.",
                        "This is the shop who sells the best ice cream.",
                        "The city who I was born in is very small.",
                        "She is the teacher which everyone loves.",
                        "The place which we met was a cafe."
                    ]
                },
                {
                    "instruction": "Write sentences about your life using relative clauses.",
                    "items": [
                        "Describe your best friend using 'who'.",
                        "Describe your favourite book or film using 'which/that'.",
                        "Describe a special place using 'where'.",
                        "Describe a family member using 'who'.",
                        "Describe something you own using 'that'."
                    ]
                }
            ],
            "tip": "In informal English, 'that' can often replace 'who' or 'which' in defining relative clauses. However, use 'who' for people and 'which' for things in formal writing for clarity."
        },
        6: {
            "topic": "Reported Speech (Statements)",
            "explanation": (
                "When we report what someone said, we usually change the tense one step back. Present Simple "
                "becomes Past Simple, Present Continuous becomes Past Continuous, and 'will' becomes 'would.' "
                "We also change pronouns and time expressions. The reporting verb is usually 'said' or 'told.' "
                "We use 'told' when we mention the listener: He told me... We use 'said' without a person after it."
            ),
            "examples": [
                "'I like science.' -> She said she liked science.",
                "'We are studying.' -> They said they were studying.",
                "'I will help you.' -> He told me he would help me.",
                "'I can swim.' -> She said she could swim.",
                "'I have finished.' -> He said he had finished."
            ],
            "exercises": [
                {
                    "instruction": "Change these direct speech sentences to reported speech.",
                    "items": [
                        "'I am tired,' said Elif.",
                        "'We live in Ankara,' they said.",
                        "'I will call you tomorrow,' he told me.",
                        "'She can play the piano,' said Kwame.",
                        "'I have read this book,' said Mei."
                    ]
                },
                {
                    "instruction": "Fill in the blanks to complete the reported speech.",
                    "items": [
                        "'I love football.' -> He said he ___ football.",
                        "'We are going home.' -> They said they ___ home.",
                        "'I will be there at 5.' -> She said she ___ there at 5.",
                        "'I don't understand.' -> He said he ___ .",
                        "'We have finished.' -> They said they ___ ."
                    ]
                },
                {
                    "instruction": "Change reported speech back to direct speech.",
                    "items": [
                        "She said she was happy.",
                        "He told me he would come to the party.",
                        "They said they had visited Istanbul.",
                        "She said she could speak French.",
                        "He said he didn't like spinach."
                    ]
                },
                {
                    "instruction": "Report what your classmates said. Use 'He/She said...' or 'He/She told me...'",
                    "items": [
                        "Your friend: 'I am going to the cinema tonight.'",
                        "Your teacher: 'You must study for the test.'",
                        "Your parent: 'I will pick you up at 4.'",
                        "Your classmate: 'I don't have a pencil.'",
                        "Your sibling: 'I have already done my homework.'"
                    ]
                }
            ],
            "tip": "Not every tense needs to change in reported speech. If the information is still true, you can keep the original tense: 'She said water boils at 100 degrees.' (still true)"
        },
        7: {
            "topic": "Too and Enough",
            "explanation": (
                "'Too' means more than necessary or wanted. It goes before adjectives and adverbs: too hot, "
                "too quickly. 'Enough' means as much as needed. It goes after adjectives and adverbs: old enough, "
                "fast enough. But 'enough' goes before nouns: enough money, enough time. We often use these with "
                "'to + infinitive' to explain the result or purpose."
            ),
            "examples": [
                "This coffee is too hot to drink.",
                "She is old enough to stay home alone.",
                "We don't have enough time to finish the project.",
                "The music is too loud. I can't concentrate.",
                "He runs fast enough to win the race."
            ],
            "exercises": [
                {
                    "instruction": "Complete the sentences with 'too' or 'enough'.",
                    "items": [
                        "The bag is ___ heavy for me to carry.",
                        "Is the room warm ___?",
                        "She is ___ young to drive a car.",
                        "We have ___ chairs for everyone.",
                        "This exercise is ___ difficult for beginners."
                    ]
                },
                {
                    "instruction": "Rewrite the sentences using 'too' or 'enough'.",
                    "items": [
                        "The water is very cold. I can't swim in it. (too)",
                        "He is very tall. He can reach the shelf. (enough)",
                        "The film was very scary. The children couldn't watch it. (too)",
                        "She doesn't have much money. She can't buy the book. (enough)",
                        "The soup is very salty. I can't eat it. (too)"
                    ]
                },
                {
                    "instruction": "Choose the correct option.",
                    "items": [
                        "We have (too / enough) food for the picnic.",
                        "It's (too / enough) late to go to the cinema.",
                        "She isn't (too / enough) strong enough to lift that box.",
                        "There aren't (too / enough) seats on the bus.",
                        "The test was (too / enough) easy. Everyone passed."
                    ]
                },
                {
                    "instruction": "Write your own sentences using 'too' and 'enough' about these topics.",
                    "items": [
                        "The weather today",
                        "Your English skills",
                        "A film you watched recently",
                        "Your school bag",
                        "A food you tried"
                    ]
                }
            ],
            "tip": "Remember the word order: TOO + adjective (too cold) but adjective + ENOUGH (warm enough). ENOUGH + noun (enough water). A common mistake is putting 'enough' before the adjective."
        },
        8: {
            "topic": "Gerunds and Infinitives",
            "explanation": (
                "A gerund is a verb + -ing used as a noun: 'Swimming is fun.' An infinitive is 'to + verb': "
                "'I want to swim.' Some verbs are followed by gerunds (enjoy, avoid, finish, suggest, mind), "
                "and some by infinitives (want, decide, hope, plan, agree). A few verbs can take both with "
                "little or no change in meaning (like, love, start, begin)."
            ),
            "examples": [
                "I enjoy watching documentaries. (gerund)",
                "She decided to study medicine. (infinitive)",
                "They avoid eating junk food. (gerund)",
                "We hope to visit Japan next year. (infinitive)",
                "He started learning / to learn the drums. (both)"
            ],
            "exercises": [
                {
                    "instruction": "Complete the sentences with the gerund or infinitive form of the verb.",
                    "items": [
                        "I enjoy ___ (read) books before bed.",
                        "She wants ___ (become) a doctor.",
                        "They decided ___ (join) the chess club.",
                        "He avoids ___ (eat) too much sugar.",
                        "We hope ___ (travel) to Europe this summer."
                    ]
                },
                {
                    "instruction": "Choose the correct form: gerund or infinitive.",
                    "items": [
                        "I don't mind (waiting / to wait) for you.",
                        "She agreed (helping / to help) with the project.",
                        "He suggested (going / to go) to the park.",
                        "We plan (visiting / to visit) the museum tomorrow.",
                        "They finished (doing / to do) their homework."
                    ]
                },
                {
                    "instruction": "Rewrite the sentences using a gerund as the subject.",
                    "items": [
                        "It is fun to play basketball. -> ___ is fun.",
                        "It is important to learn languages. -> ___ is important.",
                        "It is relaxing to listen to music. -> ___ is relaxing.",
                        "It is difficult to wake up early. -> ___ is difficult.",
                        "It is dangerous to text while walking. -> ___ is dangerous."
                    ]
                },
                {
                    "instruction": "Write sentences about yourself using these verbs + gerund or infinitive.",
                    "items": [
                        "enjoy + gerund",
                        "want + infinitive",
                        "avoid + gerund",
                        "hope + infinitive",
                        "suggest + gerund"
                    ]
                }
            ],
            "tip": "There is no perfect rule for which verbs take gerunds and which take infinitives. The best strategy is to learn them in groups. Make flashcards: 'enjoy + -ing', 'want + to'."
        },
        9: {
            "topic": "Phrasal Verbs (Common Digital & Daily Life)",
            "explanation": (
                "Phrasal verbs are verbs combined with a preposition or adverb that create a new meaning. "
                "'Look up' does not mean 'look' + 'up' literally; it means to search for information. "
                "Phrasal verbs are very common in everyday English, especially in informal speech. Some are "
                "separable (you can put an object between the verb and particle) and some are inseparable."
            ),
            "examples": [
                "I need to look up this word in the dictionary.",
                "Can you turn off your phone during class?",
                "She grew up in a small village.",
                "They set up a new website for their project.",
                "Please log in to your account."
            ],
            "exercises": [
                {
                    "instruction": "Match the phrasal verbs with their meanings.",
                    "items": [
                        "turn on (a) to search for information",
                        "look up (b) to start a device or machine",
                        "give up (c) to stop trying",
                        "find out (d) to reduce the volume",
                        "turn down (e) to discover or learn"
                    ]
                },
                {
                    "instruction": "Complete the sentences with the correct phrasal verb from the box: log in, sign up, turn off, look up, set up.",
                    "items": [
                        "Please ___ your computers before leaving.",
                        "You need to ___ to your email account.",
                        "I had to ___ the word in an online dictionary.",
                        "They ___ a charity to help homeless animals.",
                        "Would you like to ___ for the coding workshop?"
                    ]
                },
                {
                    "instruction": "Replace the underlined word with a phrasal verb.",
                    "items": [
                        "She discovered the truth about the story. (found out)",
                        "He stopped trying to solve the puzzle. (gave up)",
                        "They postponed the meeting until Friday. (put off)",
                        "I removed my jacket because it was hot. (took off)",
                        "She rejected the job offer. (turned down)"
                    ]
                },
                {
                    "instruction": "Write sentences using these phrasal verbs in a digital context.",
                    "items": [
                        "log out",
                        "back up (save a copy)",
                        "scroll down",
                        "pop up (appear suddenly on screen)",
                        "switch off"
                    ]
                }
            ],
            "tip": "Keep a phrasal verb notebook organised by topic (technology, school, daily life). When you learn a new one, write it in a sentence. Context helps you remember meaning better than a definition alone."
        },
        10: {
            "topic": "Tag Questions",
            "explanation": (
                "Tag questions are short questions added at the end of a sentence to check information or "
                "ask for agreement. The rule is: positive sentence + negative tag, and negative sentence + "
                "positive tag. The tag uses the same auxiliary verb as the main sentence. If there is no "
                "auxiliary, we use 'do/does/did.' Intonation matters: rising = real question, falling = expecting agreement."
            ),
            "examples": [
                "You like chocolate, don't you?",
                "She is a student, isn't she?",
                "They haven't finished, have they?",
                "He can swim, can't he?",
                "We should help them, shouldn't we?"
            ],
            "exercises": [
                {
                    "instruction": "Add the correct tag question.",
                    "items": [
                        "It's a beautiful day, ___?",
                        "You have been to London, ___?",
                        "They won't be late, ___?",
                        "She can play the piano, ___?",
                        "We should protect human rights, ___?"
                    ]
                },
                {
                    "instruction": "Complete the tag questions for these sentences.",
                    "items": [
                        "He speaks English, ___?",
                        "They didn't come yesterday, ___?",
                        "You are going to the party, ___?",
                        "She hasn't called yet, ___?",
                        "We were late, ___?"
                    ]
                },
                {
                    "instruction": "Correct the mistakes in these tag questions.",
                    "items": [
                        "She is kind, is she?",
                        "They live here, do they?",
                        "He can't drive, can't he?",
                        "You like pizza, do you?",
                        "We are friends, are we?"
                    ]
                },
                {
                    "instruction": "Write tag questions to check information about your classmates.",
                    "items": [
                        "You're from this city, ___?",
                        "You have a brother or sister, ___?",
                        "You enjoy English lessons, ___?",
                        "You didn't watch the film last night, ___?",
                        "You can ride a bicycle, ___?"
                    ]
                }
            ],
            "tip": "The most common mistake is using the same polarity (positive + positive or negative + negative). Always flip it: positive sentence = negative tag, negative sentence = positive tag."
        }
    }
}

# =============================================================================
# BANK 5: DIALOGUE BANK (8-10 lines each)
# =============================================================================
DIALOGUE_BANK = {
    7: {
        1: {
            "title": "Getting to Know Each Other",
            "context": "Elif meets a new student, Kwame, on the first day of school.",
            "lines": [
                {"speaker": "Elif", "line": "Hi! I'm Elif. Are you new here?"},
                {"speaker": "Kwame", "line": "Yes, I am. My name is Kwame. I just moved from Ghana."},
                {"speaker": "Elif", "line": "Welcome! How do you like Istanbul so far?"},
                {"speaker": "Kwame", "line": "It's amazing but very crowded. I'm still getting used to it."},
                {"speaker": "Elif", "line": "I can imagine. What do you enjoy doing in your free time?"},
                {"speaker": "Kwame", "line": "I love playing the drums and reading about space. What about you?"},
                {"speaker": "Elif", "line": "I'm really into filmmaking and journalism. I want to be a documentary filmmaker."},
                {"speaker": "Kwame", "line": "That's cool! Maybe you could make a film about space one day."},
                {"speaker": "Elif", "line": "That would be amazing! Would you like me to show you around the school?"},
                {"speaker": "Kwame", "line": "I'd love that. Thanks, Elif. I think I'm going to like it here."}
            ],
            "practice_prompts": [
                "Introduce yourself to a new classmate and ask about their hobbies.",
                "Tell someone three things that are important to your identity.",
                "Describe yourself in five sentences without saying your name."
            ]
        },
        2: {
            "title": "Comparing Traditions",
            "context": "Mei and Carlos discuss holiday traditions at lunch.",
            "lines": [
                {"speaker": "Mei", "line": "Carlos, do you celebrate any special holidays in Mexico?"},
                {"speaker": "Carlos", "line": "Yes! Dia de los Muertos is my favourite. We remember people who have died."},
                {"speaker": "Mei", "line": "That sounds meaningful. In China, we have the Qingming Festival for the same reason."},
                {"speaker": "Carlos", "line": "Really? What do you do during Qingming?"},
                {"speaker": "Mei", "line": "We visit family graves, clean them, and leave offerings like food and flowers."},
                {"speaker": "Carlos", "line": "We do something similar! We also make altars with photos and marigold flowers."},
                {"speaker": "Mei", "line": "It's interesting how different cultures have similar traditions, isn't it?"},
                {"speaker": "Carlos", "line": "Absolutely. I think remembering our loved ones is universal."},
                {"speaker": "Mei", "line": "We should present this comparison at the Traditions Fair!"},
                {"speaker": "Carlos", "line": "Great idea! Let's work on it together this weekend."}
            ],
            "practice_prompts": [
                "Compare a Turkish holiday tradition with one from another country.",
                "Describe your favourite family tradition to a partner.",
                "Ask your partner about three customs from their culture."
            ]
        },
        3: {
            "title": "What Do You Want to Be?",
            "context": "Kwame and Elif discuss their future career plans after Career Day.",
            "lines": [
                {"speaker": "Kwame", "line": "Career Day was incredible! I can't stop thinking about Dr. Asante's talk."},
                {"speaker": "Elif", "line": "The filmmaker's workshop was amazing too. Have you always wanted to be a scientist?"},
                {"speaker": "Kwame", "line": "Yes, ever since I was small. But I didn't know astrophysics was a real option."},
                {"speaker": "Elif", "line": "What do you mean?"},
                {"speaker": "Kwame", "line": "I had never seen an African astrophysicist before. Dr. Asante changed that for me."},
                {"speaker": "Elif", "line": "Representation really matters, doesn't it? What skills do you need for that career?"},
                {"speaker": "Kwame", "line": "Strong maths, physics, and problem-solving. Also patience and curiosity."},
                {"speaker": "Elif", "line": "For filmmaking, I need creativity, communication, and technical skills."},
                {"speaker": "Kwame", "line": "Maybe one day you'll make a documentary about my discoveries!"},
                {"speaker": "Elif", "line": "Deal! Let's make a pact to help each other reach our dreams."}
            ],
            "practice_prompts": [
                "Talk about what career you want and what skills you need for it.",
                "Interview your partner about their dream job using at least five questions.",
                "Describe a professional who has inspired you and explain why."
            ]
        },
        4: {
            "title": "Is This News Real?",
            "context": "Mei shows Elif a surprising article she found on social media.",
            "lines": [
                {"speaker": "Mei", "line": "Elif, look at this article! It says chocolate is healthier than fruit."},
                {"speaker": "Elif", "line": "Hmm, that sounds too good to be true. Where did you find it?"},
                {"speaker": "Mei", "line": "Someone shared it in my social media feed."},
                {"speaker": "Elif", "line": "Let's use the SIFT method Mr. Demir taught us. First, stop and don't share it yet."},
                {"speaker": "Mei", "line": "OK. Next, we should investigate the source, right?"},
                {"speaker": "Elif", "line": "Exactly. Look at the website name. Have you heard of 'DailyHealthBuzz.net'?"},
                {"speaker": "Mei", "line": "No, never. And there's no author name on the article either."},
                {"speaker": "Elif", "line": "That's a red flag. Let's search for the same claim on a trusted health website."},
                {"speaker": "Mei", "line": "I checked the WHO website. They say fruit is essential for a balanced diet. Nothing about chocolate being better."},
                {"speaker": "Elif", "line": "So it's fake news. See how easy it is to be tricked? Good thing we checked!"}
            ],
            "practice_prompts": [
                "Show your partner a headline and discuss whether it might be real or fake.",
                "Explain the SIFT method to someone who has never heard of it.",
                "Discuss why people create and share fake news."
            ]
        },
        5: {
            "title": "Let's Get Healthy",
            "context": "Carlos and Kwame plan wellness activities for the class.",
            "lines": [
                {"speaker": "Carlos", "line": "Have you noticed how stressed everyone is because of exams?"},
                {"speaker": "Kwame", "line": "Yes, Mei told me she hasn't been sleeping well at all."},
                {"speaker": "Carlos", "line": "I think we should organise some wellness activities for the class."},
                {"speaker": "Kwame", "line": "That's a great idea. What do you have in mind?"},
                {"speaker": "Carlos", "line": "How about a healthy snack station? I can bring fruit and nuts."},
                {"speaker": "Kwame", "line": "Perfect. I could lead a short meditation session during break time."},
                {"speaker": "Carlos", "line": "Do you know how to do that?"},
                {"speaker": "Kwame", "line": "I've been practising with an app. It's just five minutes of breathing exercises."},
                {"speaker": "Carlos", "line": "Sounds good. We should also remind everyone to take screen breaks."},
                {"speaker": "Kwame", "line": "Agreed. Let's talk to Mr. Demir and set it up for next week."}
            ],
            "practice_prompts": [
                "Give your partner three tips for better health and wellbeing.",
                "Plan a Wellness Day for your school. What activities would you include?",
                "Discuss the connection between sleep, exercise, and academic performance."
            ]
        },
        6: {
            "title": "Stargazing Plans",
            "context": "The friends plan a night of stargazing after their exoplanet project.",
            "lines": [
                {"speaker": "Kwame", "line": "Dr. Asante suggested we try stargazing to learn constellations. Anyone interested?"},
                {"speaker": "Elif", "line": "Definitely! But where can we go? There's too much light pollution in the city."},
                {"speaker": "Kwame", "line": "My uncle has a farm about an hour outside Istanbul. The sky is much darker there."},
                {"speaker": "Mei", "line": "I can bring my laptop and we can use a star map app to identify what we see."},
                {"speaker": "Carlos", "line": "Will we be able to see any planets with the naked eye?"},
                {"speaker": "Kwame", "line": "Yes! Jupiter and Saturn should be visible this month."},
                {"speaker": "Elif", "line": "I'll bring my camera and try to photograph the Milky Way."},
                {"speaker": "Carlos", "line": "What if it's cloudy?"},
                {"speaker": "Kwame", "line": "Then we'll watch a space documentary inside and try again another night."},
                {"speaker": "Mei", "line": "Either way, it's going to be an amazing evening. Let's ask our parents!"}
            ],
            "practice_prompts": [
                "Plan an outdoor science activity with your group. Discuss what you need and where to go.",
                "Describe the night sky to someone who has never seen stars clearly.",
                "Discuss why space exploration is important for humanity."
            ]
        },
        7: {
            "title": "A Warm Welcome",
            "context": "The group discusses how to welcome a new refugee student to their school.",
            "lines": [
                {"speaker": "Elif", "line": "Did you hear? A new student from Syria is joining our class next week."},
                {"speaker": "Carlos", "line": "That must be really hard, starting a new school in a new country."},
                {"speaker": "Kwame", "line": "I remember how difficult it was for me. I didn't speak any Turkish at first."},
                {"speaker": "Mei", "line": "What helped you the most when you first arrived?"},
                {"speaker": "Kwame", "line": "Having someone who was patient and showed me around. Small things made a big difference."},
                {"speaker": "Carlos", "line": "Let's make a Welcome Kit with a school map, useful phrases, and a list of clubs."},
                {"speaker": "Elif", "line": "Great idea! I can write some common phrases in Turkish and Arabic."},
                {"speaker": "Mei", "line": "I'll design a welcome card from the whole class."},
                {"speaker": "Kwame", "line": "And I'll volunteer to be his buddy for the first month."},
                {"speaker": "Carlos", "line": "Everyone deserves to feel like they belong. Let's make sure he does."}
            ],
            "practice_prompts": [
                "Role-play welcoming a new student from another country to your school.",
                "Discuss three things that make someone feel included in a new place.",
                "Share a time when someone made you feel welcome and how it affected you."
            ]
        },
        8: {
            "title": "Lights, Camera, Discussion",
            "context": "The friends discuss ideas for their documentary film.",
            "lines": [
                {"speaker": "Elif", "line": "OK team, we need to decide on a theme for our documentary. Any ideas?"},
                {"speaker": "Carlos", "line": "How about 'Bridges, Not Walls'? We could show how our different backgrounds connect us."},
                {"speaker": "Mei", "line": "I love that! We could interview students from different countries."},
                {"speaker": "Kwame", "line": "And we could ask teachers what they've learned from having diverse classrooms."},
                {"speaker": "Elif", "line": "Perfect. Who wants to handle which part? I'll direct and do the camera work."},
                {"speaker": "Carlos", "line": "I'll write the script and prepare the interview questions."},
                {"speaker": "Mei", "line": "I can do the editing. I've been learning video editing software."},
                {"speaker": "Kwame", "line": "I'll compose the background music. Something with drums and guitar."},
                {"speaker": "Elif", "line": "How long should it be? The festival limit is ten minutes."},
                {"speaker": "Carlos", "line": "Let's aim for seven minutes. Short enough to keep attention, long enough to tell a story."}
            ],
            "practice_prompts": [
                "Plan a short film with your group. Assign roles and discuss the theme.",
                "Recommend a film to your partner and explain why they should watch it.",
                "Discuss whether films or books are better for learning about other cultures."
            ]
        },
        9: {
            "title": "Digital Detox Challenge",
            "context": "Mei proposes a challenge to reduce screen time for one week.",
            "lines": [
                {"speaker": "Mei", "line": "I tracked my screen time last week, and I was on my phone for five hours a day!"},
                {"speaker": "Carlos", "line": "Five hours? That's like a part-time job!"},
                {"speaker": "Mei", "line": "I know, it's shocking. Most of it was social media and watching videos."},
                {"speaker": "Kwame", "line": "I think we should try a digital detox challenge for one week."},
                {"speaker": "Elif", "line": "What exactly would we do?"},
                {"speaker": "Kwame", "line": "Limit phone use to two hours a day and no screens one hour before bed."},
                {"speaker": "Carlos", "line": "That sounds really hard, but I'm willing to try."},
                {"speaker": "Mei", "line": "We could replace screen time with other activities, like reading or walking."},
                {"speaker": "Elif", "line": "Let's track our mood and sleep quality during the week and compare results."},
                {"speaker": "Kwame", "line": "It'll be like a real experiment. If it works, we can share the results with the school."}
            ],
            "practice_prompts": [
                "Discuss how much time you spend on your phone and whether you think it's too much.",
                "Debate: 'Social media does more harm than good for teenagers.'",
                "Create rules for healthy technology use and share them with a partner."
            ]
        },
        10: {
            "title": "Rights and Responsibilities",
            "context": "The class discusses human rights after a guest speaker's visit.",
            "lines": [
                {"speaker": "Carlos", "line": "The guest speaker really made me think. I didn't realise so many children can't go to school."},
                {"speaker": "Kwame", "line": "Education changed my life. When I think about kids who don't have that chance, it breaks my heart."},
                {"speaker": "Mei", "line": "She said that 258 million children worldwide are out of school. That number is huge."},
                {"speaker": "Elif", "line": "What can we actually do about it, though? We're just students."},
                {"speaker": "Carlos", "line": "Remember what the lawyer said on Career Day? You don't have to wait to be an adult."},
                {"speaker": "Mei", "line": "We could write letters to organisations or raise awareness at school."},
                {"speaker": "Kwame", "line": "Let's create a Human Rights Wall in the corridor with facts and quotes."},
                {"speaker": "Elif", "line": "And I could film interviews with students about which rights they think are most important."},
                {"speaker": "Carlos", "line": "Rights come with responsibilities too. We should respect others' rights every day."},
                {"speaker": "Kwame", "line": "Agreed. Even small actions like standing up against bullying make a difference."}
            ],
            "practice_prompts": [
                "Choose three human rights from the Universal Declaration and explain why they matter to you.",
                "Discuss: 'What responsibilities come with the right to education?'",
                "Plan a school campaign to raise awareness about a human rights issue."
            ]
        }
    }
}

# =============================================================================
# BANK 6: CULTURE CORNER BANK (80-100 words each)
# =============================================================================
CULTURE_CORNER_BANK = {
    7: {
        1: {
            "title": "The Maori Haka: Identity Through Dance",
            "country": "New Zealand",
            "text": (
                "The Maori people of New Zealand use a powerful dance called the Haka to express their "
                "identity and emotions. Originally performed before battles, the Haka involves strong "
                "stamping, chest beating, and fierce facial expressions. Today, it is performed at "
                "celebrations, funerals, and sports events. The New Zealand rugby team, the All Blacks, "
                "performs the Haka before every match. Each Haka has its own words and meaning. For the "
                "Maori, it is much more than a dance; it represents strength, unity, and cultural pride. "
                "Learning the Haka is an important part of growing up Maori."
            ),
            "did_you_know": "The most famous Haka, 'Ka Mate,' was composed by the warrior chief Te Rauparaha around 1820.",
            "compare_question": "Does your culture have a traditional dance that represents identity? How does it compare to the Haka?"
        },
        2: {
            "title": "Hanami: Japan's Cherry Blossom Tradition",
            "country": "Japan",
            "text": (
                "Every spring, millions of Japanese people take part in Hanami, the tradition of enjoying "
                "cherry blossoms. Families and friends gather in parks under the blooming trees to eat, "
                "drink, and celebrate the beauty of nature. Cherry blossoms bloom for only about two weeks, "
                "making them a symbol of the fleeting nature of life. This idea is called 'mono no aware' "
                "in Japanese, meaning an appreciation for passing beauty. The tradition dates back over a "
                "thousand years to the Nara period. Weather forecasters even track the 'cherry blossom front' "
                "as it moves from south to north across the country."
            ),
            "did_you_know": "Japan has over 200 varieties of cherry blossom trees, but the most common is the Somei Yoshino.",
            "compare_question": "Do you have a tradition connected to a season or natural event? How is it similar to Hanami?"
        },
        3: {
            "title": "Young Entrepreneurs in Kenya",
            "country": "Kenya",
            "text": (
                "Kenya has one of Africa's fastest-growing economies, and young people are leading the way. "
                "Nairobi, the capital, is nicknamed 'Silicon Savannah' because of its booming tech industry. "
                "Many Kenyan teenagers learn coding and app development in free community programmes. "
                "M-Pesa, a mobile money system invented in Kenya, allows people to send and receive money "
                "using basic mobile phones. This innovation has helped millions of people who do not have "
                "bank accounts. Young Kenyans are also creating apps for agriculture, health, and education. "
                "The government supports youth entrepreneurship through competitions and grants."
            ),
            "did_you_know": "M-Pesa processes more transactions per year than PayPal and Western Union combined in Africa.",
            "compare_question": "How do young people in your country prepare for future careers? Are there similar tech programmes?"
        },
        4: {
            "title": "Finland's Media Literacy Education",
            "country": "Finland",
            "text": (
                "Finland is considered a world leader in media literacy education. Finnish students learn "
                "how to identify fake news, understand advertising techniques, and analyse media messages "
                "from primary school. The country's approach focuses on critical thinking rather than "
                "memorisation. Teachers use real-world examples, such as actual news articles, to teach "
                "students how to evaluate sources. Finland also has one of the world's freest press systems, "
                "which supports informed citizenship. Studies show that Finnish people are among the most "
                "resistant to misinformation in Europe. The Finnish model has been studied and copied by "
                "many other countries."
            ),
            "did_you_know": "Finland was ranked number one in Europe for resilience to fake news in a 2019 study by the Open Society Institute.",
            "compare_question": "How is media literacy taught in your school? What could be improved?"
        },
        5: {
            "title": "Blue Zones: Where People Live the Longest",
            "country": "Multiple (Japan, Italy, Costa Rica, Greece, USA)",
            "text": (
                "Blue Zones are regions where people live significantly longer than average. Scientists "
                "have identified five Blue Zones: Okinawa in Japan, Sardinia in Italy, Nicoya in Costa Rica, "
                "Ikaria in Greece, and Loma Linda in California. What do these places have in common? "
                "People there eat mostly plant-based diets, stay physically active throughout life, have "
                "strong social connections, and have a sense of purpose. They also tend to experience less "
                "stress and spend more time with family. Interestingly, none of these communities follow "
                "extreme exercise programmes. Instead, movement is naturally built into their daily routines, "
                "like walking and gardening."
            ),
            "did_you_know": "In Okinawa, people follow a rule called 'hara hachi bu,' which means they stop eating when they are 80% full.",
            "compare_question": "Which Blue Zone habits do people in your community already follow? Which ones could you adopt?"
        },
        6: {
            "title": "India's Space Programme: Reaching Mars on a Budget",
            "country": "India",
            "text": (
                "In 2014, India's space agency ISRO made history by successfully sending a spacecraft to Mars "
                "on its very first attempt. The Mars Orbiter Mission, also known as Mangalyaan, cost only "
                "74 million dollars, less than the budget of many Hollywood films. This made India the first "
                "Asian country to reach Mars and the most cost-effective space mission ever. ISRO is known "
                "for its innovative, low-cost approach to space exploration. The agency has also launched "
                "over 100 satellites for various countries. In 2023, India became the fourth country to "
                "successfully land on the Moon with its Chandrayaan-3 mission."
            ),
            "did_you_know": "Mangalyaan cost less per kilometre than an auto-rickshaw ride in some Indian cities!",
            "compare_question": "Does your country have a space programme? How does it compare to ISRO's achievements?"
        },
        7: {
            "title": "Germany's Welcome Culture (Willkommenskultur)",
            "country": "Germany",
            "text": (
                "In 2015, Germany welcomed over one million refugees, mostly from Syria, Afghanistan, and "
                "Iraq. This policy, led by Chancellor Angela Merkel, became known as Willkommenskultur, or "
                "'welcome culture.' Thousands of German volunteers helped newcomers by teaching language "
                "classes, donating clothing, and providing legal advice. Integration centres were set up "
                "across the country to help refugees learn German and find jobs. While the policy was "
                "controversial and faced criticism, it also showed the power of community solidarity. "
                "Many refugees have since become successful workers, students, and even business owners "
                "in Germany."
            ),
            "did_you_know": "By 2022, about 50% of Syrian refugees in Germany had found employment, many in healthcare and technology.",
            "compare_question": "How does your country welcome immigrants or refugees? What more could be done?"
        },
        8: {
            "title": "Nollywood: Nigeria's Film Industry",
            "country": "Nigeria",
            "text": (
                "Nollywood is the name given to Nigeria's film industry, and it is the second-largest "
                "in the world by number of films produced, after India's Bollywood. Nollywood produces "
                "about 2,500 films per year, mostly in English and Yoruba. The industry started in the "
                "1990s when filmmakers began shooting movies on video cameras with very small budgets. "
                "Despite limited resources, Nollywood tells uniquely African stories about family, love, "
                "tradition, and modern life. Today, Nigerian films are watched across Africa and by "
                "diaspora communities worldwide. Streaming platforms have helped Nollywood reach even "
                "larger global audiences."
            ),
            "did_you_know": "Nollywood contributes about 2.3% of Nigeria's GDP and employs over one million people.",
            "compare_question": "How does your country's film industry compare to Nollywood? What stories does it typically tell?"
        },
        9: {
            "title": "Estonia: The World's Most Digital Country",
            "country": "Estonia",
            "text": (
                "Estonia is often called the most digitally advanced country in the world. Since 2005, "
                "Estonian citizens can vote online in national elections. Almost all government services "
                "are available digitally, from paying taxes to registering a business. The country even "
                "offers 'e-Residency,' allowing people from any country to start an Estonian company "
                "online. Estonian schools teach coding from age seven, and digital literacy is a core "
                "part of the curriculum. The country's success with technology is remarkable considering "
                "it only has 1.3 million people. Estonia's digital transformation began after independence "
                "from the Soviet Union in 1991."
            ),
            "did_you_know": "Skype, the video calling platform, was created by Estonian developers in 2003.",
            "compare_question": "How digital is your daily life compared to an Estonian citizen's? What digital services would you like?"
        },
        10: {
            "title": "South Africa's Constitutional Court",
            "country": "South Africa",
            "text": (
                "South Africa's Constitutional Court, established in 1995, is one of the most progressive "
                "in the world. After the end of apartheid, South Africa wrote a new constitution that "
                "protects a wide range of human rights, including equality, dignity, freedom of expression, "
                "and the right to education and healthcare. The court building in Johannesburg was built on "
                "the site of a former prison, symbolising the transformation from oppression to justice. "
                "The court has made landmark decisions on issues like equality and children's rights. "
                "South Africa's constitution is often called one of the most progressive in the world and "
                "has inspired other nations."
            ),
            "did_you_know": "The South African constitution was one of the first in the world to explicitly protect LGBTQ+ rights.",
            "compare_question": "What rights does your country's constitution protect? Are there any you think should be added?"
        }
    }
}

# =============================================================================
# BANK 7: FUN FACTS BANK
# =============================================================================
FUN_FACTS_BANK = {
    7: {
        1: {
            "facts": [
                "Your brain creates a new neural pathway every time you learn something new, physically changing its structure.",
                "Identical twins have the same DNA but different fingerprints, showing that identity goes beyond genetics.",
                "The concept of a 'teenager' as a distinct life stage only became widely recognised in the 1940s."
            ],
            "source_hint": "Neuroscience and identity psychology research"
        },
        2: {
            "facts": [
                "In Ethiopia, the New Year is celebrated on September 11th (or 12th in leap years) because they follow a different calendar.",
                "The world's longest wedding ceremony lasted 53 hours and took place in India in 2022.",
                "In Denmark, if you are unmarried on your 25th birthday, friends throw cinnamon at you as a funny tradition."
            ],
            "source_hint": "World cultures and traditions databases"
        },
        3: {
            "facts": [
                "The most in-demand job skill worldwide is not coding or finance; it is complex problem-solving.",
                "A YouTuber was not a real job title until 2005, and now some earn more than doctors or lawyers.",
                "By 2030, it is estimated that 800 million jobs worldwide could be automated by machines."
            ],
            "source_hint": "World Economic Forum and McKinsey Global Institute reports"
        },
        4: {
            "facts": [
                "The average person sees between 6,000 and 10,000 advertisements every single day.",
                "A false story on social media is 70% more likely to be shared than a true one, according to MIT research.",
                "The word 'news' stands for Notable Events, Weather, and Sports (though this is debated by etymologists)."
            ],
            "source_hint": "MIT Media Lab and digital marketing research"
        },
        5: {
            "facts": [
                "Laughing for 15 minutes burns approximately 40 calories, about the same as a small apple.",
                "Teenagers need more sleep than adults because their brains are undergoing major development.",
                "Walking in nature for just 20 minutes has been scientifically shown to reduce stress hormones."
            ],
            "source_hint": "Health and neuroscience journals"
        },
        6: {
            "facts": [
                "A day on Venus is longer than a year on Venus because it rotates so slowly on its axis.",
                "There are more stars in the observable universe than grains of sand on all of Earth's beaches.",
                "The footprints left by Apollo astronauts on the Moon will remain visible for at least 100 million years because there is no wind."
            ],
            "source_hint": "NASA and European Space Agency educational resources"
        },
        7: {
            "facts": [
                "About 3.6% of the world's population, roughly 281 million people, live outside their country of birth.",
                "The longest border in the world, between Canada and the USA, is largely unguarded and is called the 'longest undefended border.'",
                "Albert Einstein, Sigmund Freud, and Freddie Mercury were all refugees or immigrants."
            ],
            "source_hint": "United Nations Migration Agency (IOM) data"
        },
        8: {
            "facts": [
                "The first film ever made was only 2 seconds long and showed workers leaving a factory in France in 1895.",
                "The longest film ever made is 'Logistics' (2012), which runs for 857 hours, or about 35 days.",
                "India produces more films per year than Hollywood, with Bollywood releasing over 1,500 films annually."
            ],
            "source_hint": "Film history archives and industry statistics"
        },
        9: {
            "facts": [
                "The first computer programmer was Ada Lovelace, a woman who wrote algorithms in the 1840s, long before modern computers existed.",
                "More data has been created in the last two years than in the entire previous history of the human race.",
                "AI can now compose music, write poetry, and create artwork, but it cannot truly understand what it creates."
            ],
            "source_hint": "Computer science history and AI research publications"
        },
        10: {
            "facts": [
                "The Universal Declaration of Human Rights has been translated into over 500 languages, more than any other document.",
                "Malala Yousafzai was 17 when she won the Nobel Peace Prize, making her the youngest ever laureate.",
                "The word 'democracy' comes from the Greek words 'demos' (people) and 'kratos' (power), meaning 'power of the people.'"
            ],
            "source_hint": "United Nations and Nobel Prize historical records"
        }
    }
}

# =============================================================================
# BANK 8: PROGRESS CHECK BANK
# =============================================================================
PROGRESS_CHECK_BANK = {
    7: {
        1: {
            "can_do": [
                "I can describe my personal identity using at least five characteristics.",
                "I can use the Present Perfect Continuous to talk about ongoing activities.",
                "I can ask and answer questions about hobbies and interests.",
                "I can compare my identity with someone from a different background.",
                "I can write a paragraph about what makes me unique."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "Think about the different parts of your identity. Which part are you most proud of, and why?"
        },
        2: {
            "can_do": [
                "I can describe traditions and customs from different cultures.",
                "I can use the Past Perfect to sequence past events.",
                "I can compare and contrast celebrations from different countries.",
                "I can explain the importance of preserving traditions.",
                "I can present a cultural tradition to an audience."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "Which tradition from another culture would you most like to experience? What attracts you to it?"
        },
        3: {
            "can_do": [
                "I can talk about different careers and the skills they require.",
                "I can use the Second Conditional to discuss imaginary situations.",
                "I can interview someone about their job using appropriate questions.",
                "I can describe my dream career and explain why I chose it.",
                "I can identify skills I need to develop for my future career."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "After learning about new careers, has your idea of a dream job changed? How and why?"
        },
        4: {
            "can_do": [
                "I can distinguish between reliable and unreliable news sources.",
                "I can use the Passive Voice to report news and facts.",
                "I can apply the SIFT method to evaluate information.",
                "I can explain why media literacy is important in the digital age.",
                "I can identify common techniques used in fake news."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "Have you ever shared something online that turned out to be false? What would you do differently now?"
        },
        5: {
            "can_do": [
                "I can discuss health and wellbeing topics in English.",
                "I can use relative clauses (who/which/that/where) correctly.",
                "I can give advice about healthy habits using appropriate language.",
                "I can explain the connection between sleep and learning.",
                "I can describe a wellness plan for managing exam stress."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "What is one health habit you want to improve? What specific steps will you take this week?"
        },
        6: {
            "can_do": [
                "I can talk about space, planets, and scientific discoveries.",
                "I can use Reported Speech to relay what someone said.",
                "I can explain basic concepts like the habitable zone and exoplanets.",
                "I can discuss the importance of space exploration.",
                "I can present scientific information clearly to classmates."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "If you could ask an astronaut one question, what would it be? Why is that question important to you?"
        },
        7: {
            "can_do": [
                "I can discuss migration and immigration using appropriate vocabulary.",
                "I can use 'too' and 'enough' correctly in sentences.",
                "I can explain the difference between a migrant and a refugee.",
                "I can describe challenges that immigrants face in a new country.",
                "I can suggest ways to help newcomers feel welcome."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "How would you feel if you had to leave your country and start a new life somewhere else? What would you miss most?"
        },
        8: {
            "can_do": [
                "I can discuss films and cinema using relevant vocabulary.",
                "I can use gerunds and infinitives correctly after different verbs.",
                "I can write a short film review including my opinion and reasons.",
                "I can explain how films influence society and culture.",
                "I can plan and describe the roles needed to make a short film."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "If you could make a documentary about any topic, what would it be about and who would you interview?"
        },
        9: {
            "can_do": [
                "I can discuss digital technology and AI using topic-specific vocabulary.",
                "I can use common phrasal verbs related to technology and daily life.",
                "I can explain what algorithms and filter bubbles are.",
                "I can discuss the benefits and risks of artificial intelligence.",
                "I can propose rules for responsible technology use."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "Do you think AI will make the world better or worse in the next ten years? Explain your reasoning."
        },
        10: {
            "can_do": [
                "I can discuss human rights and social justice issues in English.",
                "I can use tag questions correctly in conversation.",
                "I can identify and explain key articles from the Universal Declaration of Human Rights.",
                "I can describe the achievements of young activists.",
                "I can express my opinion about fairness and equality with supporting arguments."
            ],
            "self_rate_labels": ["I can do it!", "I need more practice", "I need help"],
            "reflection_prompt": "Which human right do you think is most important, and what would you do to protect it?"
        }
    }
}

# ---------------------------------------------------------------------------
#  PART 2 – Remaining 14 content banks for Grade 7
# ---------------------------------------------------------------------------

PROJECT_BANK = {
    7: {
        1: {
            "title": "My Identity Collage",
            "goal": "Create a visual collage that represents your personal identity and present it to the class.",
            "steps": [
                "Brainstorm words and images that describe who you are.",
                "Collect photos, magazine cut-outs, or drawings for your collage.",
                "Arrange them on a poster board with short English captions.",
                "Write a 60-word paragraph explaining your collage.",
                "Present your collage to the class in a 2-minute talk."
            ],
            "materials": ["poster board", "magazines/printed photos", "glue and scissors", "coloured markers"],
            "outcome": "Students practise describing personal qualities, hobbies, and values using A2+ vocabulary."
        },
        2: {
            "title": "Traditions Around the World Fair",
            "goal": "Research a cultural tradition from another country and present it at a class fair.",
            "steps": [
                "Choose a tradition from a country you are curious about.",
                "Research key facts: origin, when it is celebrated, and what people do.",
                "Create an informative poster with images and bullet points.",
                "Prepare a short spoken explanation (2 minutes).",
                "Set up your poster at the class fair and answer visitors' questions."
            ],
            "materials": ["A3 paper or cardboard", "coloured pens", "printed images", "sticky notes for visitor comments"],
            "outcome": "Students compare traditions and practise using present simple for routines and customs."
        },
        3: {
            "title": "Career Interview Project",
            "goal": "Interview someone about their job and report findings to the class.",
            "steps": [
                "Choose a person whose job interests you (family member, neighbour, etc.).",
                "Write at least 8 interview questions about their daily tasks and skills.",
                "Conduct the interview and take notes in English.",
                "Create a one-page profile of the person and their career.",
                "Present the career profile to classmates."
            ],
            "materials": ["notebook and pen", "interview question template", "A4 paper for profile", "optional: voice recorder"],
            "outcome": "Students use question forms, job vocabulary, and reported speech basics."
        },
        4: {
            "title": "Media Fact-Check Report",
            "goal": "Analyse a news article or social media post and determine if it is reliable.",
            "steps": [
                "Select a news story from an online source or social media.",
                "Identify the source, author, and date of publication.",
                "Check the claims using at least two other sources.",
                "Write a short report: reliable or unreliable, with evidence.",
                "Share your findings with the class using a simple slideshow."
            ],
            "materials": ["internet access", "fact-check worksheet", "notebook", "presentation software"],
            "outcome": "Students develop critical reading skills and practise expressing opinions with evidence."
        },
        5: {
            "title": "Healthy Living Guide",
            "goal": "Design a mini-magazine page about healthy habits for teenagers.",
            "steps": [
                "Research healthy eating, exercise, and sleep tips for teens.",
                "Write short articles (40-60 words each) on three health topics.",
                "Add illustrations or clip art to make the page attractive.",
                "Include a 'Did You Know?' fact box with statistics.",
                "Display finished pages on the classroom notice board."
            ],
            "materials": ["A3 paper", "coloured pencils and markers", "ruler", "health fact sheets"],
            "outcome": "Students use should/shouldn't, imperatives, and health vocabulary in context."
        },
        6: {
            "title": "Space Mission Brochure",
            "goal": "Create a travel brochure for a planet or moon in our solar system.",
            "steps": [
                "Choose a planet or moon and research basic facts about it.",
                "Write persuasive descriptions as if advertising space tourism.",
                "Design the brochure with sections: Getting There, What to See, Fun Facts.",
                "Add illustrations or printed images of the celestial body.",
                "Present your brochure and convince classmates to 'visit' your destination."
            ],
            "materials": ["A4 paper folded into thirds", "coloured pens", "printed space images", "glue stick"],
            "outcome": "Students practise future tenses, descriptive adjectives, and persuasive language."
        },
        7: {
            "title": "Migration Stories Timeline",
            "goal": "Research a real migration story and create an illustrated timeline.",
            "steps": [
                "Choose a historical or modern migration story (individual or group).",
                "Identify at least 6 key events in chronological order.",
                "Write a sentence for each event using past simple tense.",
                "Draw or print images for each event on a timeline poster.",
                "Present the timeline to the class, explaining causes and effects."
            ],
            "materials": ["long strip of paper or cardboard", "markers", "printed photos", "timeline template"],
            "outcome": "Students use past tenses, sequence words, and cause-effect language."
        },
        8: {
            "title": "Mini Film Festival",
            "goal": "Write a short film review and participate in a class film festival.",
            "steps": [
                "Watch a short film or movie clip approved by your teacher.",
                "Take notes on characters, plot, and your personal opinion.",
                "Write a 100-word review with a star rating (1-5).",
                "Design a movie poster for the film you reviewed.",
                "Present your review at the class film festival."
            ],
            "materials": ["film review template", "A3 paper for poster", "coloured markers", "star rating cards"],
            "outcome": "Students practise expressing opinions, using adjectives, and writing structured reviews."
        },
        9: {
            "title": "AI Helper Prototype",
            "goal": "Design a concept for an AI assistant that solves a school problem.",
            "steps": [
                "Identify a problem at school that technology could help solve.",
                "Brainstorm features your AI helper would have.",
                "Draw the interface and write sample dialogues with the AI.",
                "Create a poster explaining how your AI works.",
                "Pitch your AI helper idea to the class."
            ],
            "materials": ["large poster paper", "markers and rulers", "dialogue template", "sticky notes"],
            "outcome": "Students use conditional sentences, technology vocabulary, and persuasive speaking."
        },
        10: {
            "title": "Human Rights Awareness Campaign",
            "goal": "Design a campaign poster and speech about a human right you care about.",
            "steps": [
                "Choose one human right from the Universal Declaration of Human Rights.",
                "Research why this right is important and where it is challenged.",
                "Design a campaign poster with a powerful slogan and image.",
                "Write a 1-minute persuasive speech supporting this right.",
                "Deliver your speech and display your poster in the school corridor."
            ],
            "materials": ["poster board", "markers and paint", "printed statistics", "speech outline template"],
            "outcome": "Students practise persuasive writing, passive voice basics, and public speaking."
        }
    }
}

SONG_BANK = {
    7: {
        1: {
            "title": "This Is Me",
            "lyrics": "Verse 1:\nI wake up every morning, look into the mirror bright,\nI see a face that's changing, but my heart knows what is right.\nI've got my own opinions, my own style and my own way,\nI'm learning who I am a little more with every day.\n\nVerse 2:\nMy name tells a story, my hobbies show my heart,\nI love to read and draw and sing — each one is a part.\nI come from a big family, my friends are by my side,\nTogether we are different, and we wear that fact with pride.\n\nVerse 3:\nSometimes I feel confused, not sure which way to go,\nBut deep inside I trust myself — I'm stronger than I know.\nI'll try new things, I'll make mistakes, I'll pick myself back up,\nBecause being truly me is always quite enough.\n\nVerse 4:\nSo clap your hands and say it loud: 'This is who I am!'\nI'm proud of every little thing that makes me who I am.\nNo need to be like anyone, no need to play a part,\nJust be yourself and let the world see what is in your heart.",
            "actions": "Clap on the beat during the chorus line. Point to yourself when singing 'This is who I am.' Do a thumbs-up gesture on the last line of each verse.",
            "vocab_focus": ["identity", "opinion", "proud", "trust", "unique"]
        },
        2: {
            "title": "Celebrate Our Ways",
            "lyrics": "Verse 1:\nAround the world there are so many things to celebrate,\nFrom lantern lights to harvest feasts — traditions that are great.\nIn Turkey we have bayram days with candy and with tea,\nIn India they light up lamps for all the world to see.\n\nVerse 2:\nIn Mexico the Day of the Dead remembers those we love,\nWith flowers, songs, and coloured skulls beneath the stars above.\nIn Japan they watch the cherry trees and have a picnic there,\nEach custom tells a story of the people and their care.\n\nVerse 3:\nWe wear our special costumes, we cook our special food,\nWe gather with our families and share a grateful mood.\nThough every land is different, one thing remains the same:\nWe celebrate together and we're glad that no one's tame.\n\nVerse 4:\nSo let us learn each other's ways, with open hearts and minds,\nThe more traditions that we know, the more connection finds.\nLet's dance and sing and share our world, from east to west we'll go,\nBecause the more we celebrate, the more our friendships grow.",
            "actions": "Mime lighting a lamp in verse 2. Pretend to eat in verse 3. Wave hands side to side during the final verse.",
            "vocab_focus": ["tradition", "celebrate", "custom", "gather", "connection"]
        },
        3: {
            "title": "What Will You Be?",
            "lyrics": "Verse 1:\nWhen you grow up, what will you be? A doctor or a vet?\nA pilot flying through the clouds — the highest you can get?\nMaybe you'll design a building, tall and shining bright,\nOr write a book that people read beneath the reading light.\n\nVerse 2:\nYou could become a scientist and find a brand-new cure,\nOr be a firefighter, brave and strong and sure.\nPerhaps you'll teach a classroom full of children just like you,\nOr travel round the world and film the things that animals do.\n\nVerse 3:\nIt doesn't matter what you choose, just follow what you love,\nWork hard and keep on learning — that's what dreams are made of.\nAsk questions, be creative, never be afraid to try,\nBecause the future's waiting and your hopes are way up high.\n\nVerse 4:\nSo close your eyes and picture it, the life you want to lead,\nThen open them and take a step — that's all you really need.\nThe world has room for all of us, for every kind of dream,\nSo raise your voice and sing along: the future's bright, it seems!",
            "actions": "Mime different jobs in verses 1-2 (stethoscope, flying, writing). Point forward on 'the future's waiting.' Stand up and march in place during verse 4.",
            "vocab_focus": ["career", "scientist", "creative", "future", "dream"]
        },
        4: {
            "title": "Don't Believe Everything",
            "lyrics": "Verse 1:\nI saw it on a website, I read it on my phone,\nA headline screaming loudly, but the facts were not well-known.\nBefore I hit the share button, I stopped and thought it through,\nIs this really accurate? Is this story even true?\n\nVerse 2:\nCheck the source, check the date, see who wrote the piece,\nLook for other articles — let the evidence increase.\nA photo can be edited, a quote can be made up,\nSo fill your mind with knowledge like you're filling up a cup.\n\nVerse 3:\nAdvertisements are tricky, they want to sell you things,\nThey promise you'll be happy with the product that fame brings.\nBut think about the message — is it honest, is it fair?\nA smart consumer questions what is really truly there.\n\nVerse 4:\nSo be a media detective, use your brain before your thumb,\nDon't let the fake news fool you — you are smarter than you think, oh come!\nRead between the lines, my friend, and always ask out 'Why?'\nBecause a well-informed young mind can see through any lie.",
            "actions": "Wag finger on 'Don't believe everything.' Mime scrolling a phone in verse 1. Put on imaginary detective glasses in verse 4.",
            "vocab_focus": ["source", "accurate", "evidence", "advertisement", "consumer"]
        },
        5: {
            "title": "Feel Good, Live Well",
            "lyrics": "Verse 1:\nEat your fruit and vegetables, drink your water every day,\nMove your body, stretch your legs, go outside and play.\nSleep at least eight hours so your brain can rest and grow,\nHealthy habits make you shine — let everybody know!\n\nVerse 2:\nWhen you're feeling worried, talk to someone that you trust,\nSharing how you feel inside is really quite a must.\nTake a breath, count to ten, let the stress just fade away,\nMental health is just as key as what you eat each day.\n\nVerse 3:\nDon't skip your breakfast, start the day with energy and light,\nLimit screens before your bedtime, say goodnight, sleep tight.\nWash your hands and brush your teeth, these small things really count,\nEvery healthy choice you make adds up to a great amount.\n\nVerse 4:\nSo let's make a promise now, to treat ourselves with care,\nTo eat well, sleep well, move around, and breathe in fresh clean air.\nYour body is your home, my friend, the only one you've got,\nSo love it, feed it, rest it well — give health your best shot!",
            "actions": "Mime eating fruit in verse 1. Deep breathing gesture in verse 2. Stretch arms wide in verse 4.",
            "vocab_focus": ["nutrition", "mental health", "exercise", "habit", "wellbeing"]
        },
        6: {
            "title": "Beyond the Stars",
            "lyrics": "Verse 1:\nLook up at the sky tonight, a billion stars are there,\nEach one is a burning sun, floating in the air.\nThe moon is Earth's companion on its journey through the dark,\nAnd every shooting star you see has left a glowing mark.\n\nVerse 2:\nMars is red and Jupiter is big beyond compare,\nSaturn wears its famous rings like jewellery in its hair.\nAstronauts are heroes who explore the great unknown,\nThey float inside their spaceships far away from home.\n\nVerse 3:\nOne day we might visit Mars and walk upon its ground,\nBuild a station on the moon where science can be found.\nThe universe is endless, full of mysteries to chase,\nAnd every generation takes another step through space.\n\nVerse 4:\nSo dream about the galaxies, imagine what's out there,\nPerhaps you'll be the astronaut who breathes in Martian air.\nThe cosmos is our classroom, and the stars our guiding light,\nKeep wondering, keep wandering — the future's burning bright!",
            "actions": "Point up at the sky in verse 1. Make ring shapes with arms for Saturn. Mime floating in zero gravity in verse 2.",
            "vocab_focus": ["universe", "astronaut", "galaxy", "explore", "cosmos"]
        },
        7: {
            "title": "A New Beginning",
            "lyrics": "Verse 1:\nThey packed their bags and said goodbye to everyone they knew,\nThey left behind their hometown for a land completely new.\nThe journey wasn't easy, there were mountains, seas, and rain,\nBut hope kept burning in their hearts through all the fear and pain.\n\nVerse 2:\nThey arrived in a new city where the language wasn't theirs,\nThe food was very different and they got some funny stares.\nBut slowly, day by day, they learned to find their way around,\nAnd little acts of kindness were the best things that they found.\n\nVerse 3:\nA neighbour brought them cookies, a classmate said 'Hello,'\nA teacher smiled and helped them — that's how friendships start to grow.\nThey shared their food and music, told their stories from back home,\nAnd soon they felt that this new place was not so far from their own.\n\nVerse 4:\nSo if you see a newcomer who looks lonely or afraid,\nRemember what a difference just a simple smile has made.\nWe all deserve a welcome and a chance to start anew,\nBecause the world is big enough for me and it's enough for you.",
            "actions": "Wave goodbye in verse 1. Mime knocking on a door in verse 3. Smile and wave at a classmate during verse 4.",
            "vocab_focus": ["migration", "journey", "newcomer", "welcome", "belonging"]
        },
        8: {
            "title": "Lights, Camera, Action!",
            "lyrics": "Verse 1:\nThe lights go down, the screen lights up, the magic starts to play,\nA story told in moving frames can take your breath away.\nThe actors speak their dialogue, the music sets the mood,\nA scary scene, a funny part — the cinema is good!\n\nVerse 2:\nThe director calls the shots and says exactly what to do,\nThe camera operator finds the very best of views.\nThe editor then cuts the film and puts it all in place,\nAnd suddenly a simple script becomes a work of grace.\n\nVerse 3:\nI love a good adventure with a hero brave and true,\nOr maybe a detective film — a mystery with a clue.\nComedies can make me laugh until my belly aches,\nAnd animated movies show us worlds that no one makes.\n\nVerse 4:\nSo grab your popcorn, find your seat, the movie's set to start,\nEvery film's a little window opening to art.\nFrom Hollywood to Yesilcam, the stories never end,\nSo let's enjoy the cinema with family and friends!",
            "actions": "Mime holding a clapperboard in verse 2. Pretend to eat popcorn in verse 4. Act scared then laugh in verse 3.",
            "vocab_focus": ["director", "dialogue", "scene", "animated", "cinema"]
        },
        9: {
            "title": "Digital World Song",
            "lyrics": "Verse 1:\nWe live inside a digital world of codes and glowing screens,\nWhere AI helps us learn and play and shows us what it means.\nWe search for information in a second — maybe less,\nThe internet connects us all from east to west, I guess.\n\nVerse 2:\nBut with great power comes great care, we must be safe online,\nDon't share your private details — keep your passwords strong and fine.\nA robot cannot feel like us, it doesn't laugh or cry,\nSo balance screen time with real life beneath the open sky.\n\nVerse 3:\nAI can write a poem, AI can play a game,\nBut creativity from humans will never be the same.\nWe program the computers, we teach them what to do,\nSo learn to code, learn to think — the digital needs you.\n\nVerse 4:\nSo use technology wisely, let it help you grow and learn,\nBut don't forget the real world — there's a balance you must earn.\nThe future's full of gadgets, but the heart of it is clear:\nIt's people who make magic when technology is here.",
            "actions": "Mime typing on a keyboard in verse 1. Wag finger for 'don't share' in verse 2. Point to your heart in verse 4.",
            "vocab_focus": ["artificial intelligence", "digital", "password", "technology", "code"]
        },
        10: {
            "title": "Rights for Everyone",
            "lyrics": "Verse 1:\nEvery child deserves a home, a school, a place to play,\nEvery person has the right to have a voice and say.\nNo matter where you come from, your colour, faith, or name,\nHuman rights belong to all — we all deserve the same.\n\nVerse 2:\nThe right to education means that every child can learn,\nThe right to healthcare means that help is there at every turn.\nFreedom means you speak your mind without the fear of blame,\nAnd equality reminds us: no two people are the same.\n\nVerse 3:\nSome children work in factories instead of going to school,\nSome people face injustice — and that simply is not cool.\nWe can raise our voices, we can stand up for what's right,\nEven one small action is a powerful beam of light.\n\nVerse 4:\nSo let us sing together for a fair and peaceful land,\nWhere every human being can reach out and hold a hand.\nRights are not a privilege for the lucky or the few,\nThey belong to everyone — to me and yes, to you.",
            "actions": "Hold hands up in verse 1. Make a megaphone gesture in verse 3. Hold hands with neighbours in verse 4.",
            "vocab_focus": ["rights", "equality", "freedom", "justice", "education"]
        }
    }
}

LISTENING_SCRIPT_BANK = {
    7: {
        1: {
            "title": "Meeting New Classmates",
            "script": "Hello everyone! My name is Elif, and I'm twelve years old. I'm from Ankara, Turkey. I have brown hair and I love drawing in my free time. This is Kwame. He's from Ghana and he's really good at football. Mei is from China — she enjoys reading science fiction books. And here's Carlos from Mexico. He plays the guitar and wants to be a musician. We are all in the same class this year. Our teacher, Mr. Demir, says we should learn about each other's hobbies and interests. I think this year is going to be amazing because we are all so different but we already get along really well.",
            "tasks": [
                {"type": "matching", "instruction": "Match each person to their hobby or interest.", "items": ["Elif — drawing", "Kwame — football", "Mei — reading sci-fi", "Carlos — playing guitar"]},
                {"type": "true_false", "instruction": "Write True or False for each statement.", "items": ["Elif is from Istanbul. (False)", "Kwame is good at football. (True)", "Mei likes science fiction. (True)", "Carlos wants to be a teacher. (False)", "Mr. Demir is their teacher. (True)"]}
            ]
        },
        2: {
            "title": "A Special Holiday",
            "script": "Mr. Demir asked us to talk about our favourite traditions. Elif told us about Ramadan Bayram in Turkey. She said families visit each other, children kiss the hands of elders, and everyone eats special sweets and baklava. Kwame described a festival in Ghana called Homowo, where people celebrate the harvest with music and dancing. Mei talked about the Mid-Autumn Festival in China. Families eat mooncakes and watch the full moon together. Carlos shared his experience of Dia de los Muertos in Mexico, where families remember loved ones who have passed away. They make colourful altars with flowers and photos. Mr. Demir said every tradition teaches us something valuable about respect and community.",
            "tasks": [
                {"type": "fill_in", "instruction": "Complete the sentences with the correct word.", "items": ["In Turkey, children kiss the hands of ____. (elders)", "In Ghana, Homowo celebrates the ____. (harvest)", "Chinese families eat ____ during the Mid-Autumn Festival. (mooncakes)", "In Mexico, families make colourful ____ with flowers. (altars)"]},
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": ["What does Mr. Demir say traditions teach us? a) cooking b) respect and community c) dancing (b)", "Which festival involves watching the full moon? a) Homowo b) Bayram c) Mid-Autumn Festival (c)"]}
            ]
        },
        3: {
            "title": "Career Day at School",
            "script": "Today was Career Day at our school. Three professionals came to talk to us. First, Dr. Ayse, a surgeon, explained that she studies for many years to save lives. She said you need patience and steady hands. Next, Mr. Tanaka, a software engineer, told us he writes code to build apps and websites. He said maths and problem-solving are very important in his job. Finally, Ms. Rivera, a journalist, described how she travels to different countries to report the news. She said being curious and a good writer helps a lot. After the talks, Mei said she wants to be a scientist, Carlos still wants to be a musician, and Kwame is now thinking about becoming an engineer. Elif is interested in journalism because she loves writing.",
            "tasks": [
                {"type": "matching", "instruction": "Match the professional to their key skill.", "items": ["Dr. Ayse — patience and steady hands", "Mr. Tanaka — maths and problem-solving", "Ms. Rivera — curiosity and good writing"]},
                {"type": "ordering", "instruction": "Put the events in the correct order.", "items": ["1. Dr. Ayse talked about being a surgeon.", "2. Mr. Tanaka explained software engineering.", "3. Ms. Rivera described journalism.", "4. Students shared their career interests."]}
            ]
        },
        4: {
            "title": "Is This News Real?",
            "script": "In our Media Literacy class, Mr. Demir showed us two news articles on the screen. The first article said that a new planet was discovered near our solar system. It came from a well-known science website and had the journalist's name and the date. The second article claimed that eating chocolate every day makes you a genius. It had no author name, no date, and the website looked strange. Mr. Demir asked us which article we trusted more. Everyone chose the first one. He taught us to always check the source, the author, and the date before believing any news. Elif said she would never share news without checking it first. Kwame agreed and said social media can spread false information very quickly.",
            "tasks": [
                {"type": "true_false", "instruction": "Write True or False.", "items": ["The first article was about a new planet. (True)", "The second article had the author's name. (False)", "Mr. Demir said we should always check the source. (True)", "Kwame said social media is always accurate. (False)", "Both articles looked trustworthy. (False)"]},
                {"type": "multiple_choice", "instruction": "Choose the best answer.", "items": ["What three things should you check in a news article? a) colour, size, font b) source, author, date c) pictures, likes, shares (b)", "Why did students trust the first article more? a) It had bright colours b) It was about chocolate c) It had a known source, author, and date (c)"]}
            ]
        },
        5: {
            "title": "Healthy Habits Discussion",
            "script": "Our school nurse, Ms. Demir, visited our class today to talk about healthy living. She said teenagers need eight to ten hours of sleep every night. She also told us to eat five portions of fruit and vegetables each day. Kwame asked about exercise, and she said at least sixty minutes of physical activity every day is ideal. Mei wanted to know about screen time. Ms. Demir recommended no more than two hours of recreational screen time per day. She also talked about mental health. She said it is important to talk to someone you trust when you feel stressed or sad. Carlos asked about breakfast, and she said skipping breakfast can make you tired and unfocused at school. Elif promised to start eating a healthy breakfast every day.",
            "tasks": [
                {"type": "fill_in", "instruction": "Fill in the blanks with the correct number or word.", "items": ["Teenagers need ____ to ten hours of sleep. (eight)", "We should eat ____ portions of fruit and vegetables daily. (five)", "Recommended daily exercise is at least ____ minutes. (sixty)", "Screen time should be no more than ____ hours. (two)"]},
                {"type": "true_false", "instruction": "True or False?", "items": ["Ms. Demir is the school nurse. (True)", "She said six hours of sleep is enough. (False)", "Skipping breakfast can make you tired. (True)", "Mental health is not important. (False)"]}
            ]
        },
        6: {
            "title": "A Trip to the Planetarium",
            "script": "Last week, our class went on a trip to the planetarium. The guide, Mr. Yildiz, showed us a film about the solar system. We learned that the Sun is a star and that Earth is the third planet from it. Jupiter is the largest planet and it has a giant red spot, which is actually a huge storm. Saturn is famous for its beautiful rings made of ice and rock. Mr. Yildiz told us that astronauts on the International Space Station see sixteen sunrises every day because they orbit Earth so fast. Mei was fascinated by black holes. Carlos wanted to know if humans could live on Mars one day. Mr. Yildiz said scientists are working on it. Elif bought a small model of Saturn from the gift shop.",
            "tasks": [
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": ["What is Jupiter's red spot? a) a volcano b) a storm c) a lake (b)", "How many sunrises do astronauts see per day? a) 4 b) 10 c) 16 (c)", "What are Saturn's rings made of? a) gas b) ice and rock c) dust (b)"]},
                {"type": "matching", "instruction": "Match the person to their interest or action.", "items": ["Mei — fascinated by black holes", "Carlos — asked about living on Mars", "Elif — bought a Saturn model", "Mr. Yildiz — guided the planetarium tour"]}
            ]
        },
        7: {
            "title": "Ahmet's Story",
            "script": "Mr. Demir invited a guest speaker to our class. His name was Ahmet, and he moved to Germany from Turkey when he was ten years old. He said the first months were very difficult because he didn't speak German. He felt lonely at school and missed his friends in Turkey. But then a classmate named Lukas invited him to play football after school. That small act of kindness changed everything. Ahmet started learning German faster because he had friends to practise with. He also taught his classmates some Turkish words. Now Ahmet is twenty-five and works as a translator. He speaks Turkish, German, and English fluently. He told us that moving to a new country is hard, but with support and courage, you can build a wonderful new life.",
            "tasks": [
                {"type": "ordering", "instruction": "Put the events in order.", "items": ["1. Ahmet moved to Germany from Turkey.", "2. He felt lonely at school.", "3. Lukas invited him to play football.", "4. Ahmet started learning German faster.", "5. Ahmet became a translator."]},
                {"type": "true_false", "instruction": "True or False?", "items": ["Ahmet moved to Germany when he was 15. (False)", "Lukas was kind to Ahmet. (True)", "Ahmet now speaks three languages. (True)", "Ahmet said moving was easy. (False)"]}
            ]
        },
        8: {
            "title": "At the Cinema",
            "script": "Elif and her friends went to the cinema last Saturday. They watched an animated film called 'The Lost Robot.' The film was about a small robot named Pixel who got separated from its family in a big city. Pixel had to solve puzzles and make new friends to find its way home. Kwame said the special effects were amazing, especially the flying scenes. Mei thought the story was touching because it was about never giving up. Carlos liked the soundtrack because it had exciting music during the action scenes. After the film, they rated it. Kwame gave it five stars, Mei gave four, Carlos gave four, and Elif gave five. They all agreed it was one of the best films they had seen this year.",
            "tasks": [
                {"type": "fill_in", "instruction": "Complete the sentences.", "items": ["The film was called 'The Lost ____.' (Robot)", "The robot's name was ____. (Pixel)", "Kwame liked the special ____. (effects)", "Carlos enjoyed the ____. (soundtrack)"]},
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": ["What was the film about? a) a lost cat b) a lost robot c) a lost boy (b)", "Who gave the film 4 stars? a) Elif and Kwame b) Mei and Carlos c) Kwame and Carlos (b)"]}
            ]
        },
        9: {
            "title": "Our Digital Lives",
            "script": "In our technology class, Mr. Demir asked each student how they use digital devices. Elif said she uses her tablet for homework and researching topics for school projects. Kwame uses his computer mainly for coding — he is learning Python programming. Mei watches educational videos online and uses an app to practise her English. Carlos uses his phone to record music and edit videos. Mr. Demir reminded us about digital safety. He said we should never share our passwords with anyone except our parents. He also said we should be kind online, just like we are in person. Cyberbullying is a serious problem, and we should always report it to a trusted adult. Everyone agreed to follow the class digital citizenship rules.",
            "tasks": [
                {"type": "matching", "instruction": "Match each person to their digital activity.", "items": ["Elif — homework and research", "Kwame — coding in Python", "Mei — educational videos and English app", "Carlos — recording music and editing videos"]},
                {"type": "true_false", "instruction": "True or False?", "items": ["Mr. Demir said sharing passwords is okay. (False)", "Cyberbullying should be reported to a trusted adult. (True)", "Kwame is learning to code. (True)", "Carlos uses his phone for cooking. (False)"]}
            ]
        },
        10: {
            "title": "Children's Rights Day",
            "script": "November 20th is Universal Children's Day. Mr. Demir explained that on this day, we celebrate the rights of every child in the world. He read some rights from the UN Convention on the Rights of the Child. Every child has the right to education, healthcare, and protection from harm. Every child has the right to play and rest. Every child has the right to express their opinions and be listened to. Elif said she thinks the right to education is the most important because without it, children cannot build their futures. Kwame said he believes the right to be protected from violence is crucial. Mei chose the right to healthcare, and Carlos chose freedom of expression. Mr. Demir said all rights are equally important and that we should work together to make sure every child can enjoy them.",
            "tasks": [
                {"type": "fill_in", "instruction": "Complete the sentences.", "items": ["Universal Children's Day is on November ____. (20th)", "Every child has the right to education, healthcare, and ____ from harm. (protection)", "Elif thinks ____ is the most important right. (education)", "Mr. Demir said all rights are equally ____. (important)"]},
                {"type": "matching", "instruction": "Match each student to the right they chose as most important.", "items": ["Elif — education", "Kwame — protection from violence", "Mei — healthcare", "Carlos — freedom of expression"]}
            ]
        }
    }
}

MODEL_WRITING_BANK = {
    7: {
        1: {
            "genre": "personal profile",
            "title": "All About Me",
            "model_text": "My name is Elif and I am twelve years old. I live in Ankara with my parents and my younger brother. I am a curious and creative person. My favourite hobby is drawing — I especially love drawing animals and nature scenes. I also enjoy reading mystery novels. At school, my favourite subject is Art, but I am also quite good at English. My friends say I am kind and helpful. In the future, I want to become a journalist because I love writing and telling stories. I believe everyone has a unique story to tell, and I want to share mine with the world.",
            "structure_notes": [
                "Start with basic personal information (name, age, location).",
                "Describe personality traits and hobbies.",
                "Mention school-related interests and strengths.",
                "End with a future goal or personal belief."
            ],
            "writing_prompt": "Write a personal profile (80-100 words) about yourself. Include your name, hobbies, personality, and a future dream."
        },
        2: {
            "genre": "descriptive paragraph",
            "title": "A Special Tradition in My Family",
            "model_text": "One of my favourite traditions is celebrating Ramadan Bayram with my family. On the first morning, we wake up early and wear our nicest clothes. My grandparents welcome us with big smiles and kisses. The house always smells like fresh baklava and Turkish coffee. We sit together in the living room and the elders give us pocket money. After lunch, we visit our neighbours and share sweets. The children play games in the garden while the adults drink tea and chat. I love this tradition because it brings our whole family together and reminds us to be grateful.",
            "structure_notes": [
                "Name the tradition and when it happens.",
                "Describe what people do step by step.",
                "Use sensory details (smells, sights, sounds).",
                "Explain why this tradition is important to you."
            ],
            "writing_prompt": "Describe a tradition in your family or country (80-100 words). What happens and why is it special to you?"
        },
        3: {
            "genre": "informal letter",
            "title": "A Letter About My Dream Job",
            "model_text": "Dear Kwame,\n\nI hope you are doing well! I wanted to tell you about my dream job. I want to become a wildlife photographer. I love animals and nature, and I think taking photos of wild animals in their natural habitat would be the most amazing job in the world. I would need to learn about photography, travel to national parks, and be very patient. My mum says I should also study biology to understand animals better. What about you? What do you want to be when you grow up? Write back and tell me!\n\nBest wishes,\nElif",
            "structure_notes": [
                "Use informal greeting and friendly opening.",
                "State the dream job clearly and explain why.",
                "Mention skills or qualifications needed.",
                "Ask the reader a question and close warmly."
            ],
            "writing_prompt": "Write a letter to a friend (80-100 words) about your dream job. Explain what it is, why you want it, and what skills you need."
        },
        4: {
            "genre": "opinion paragraph",
            "title": "Should We Trust Social Media News?",
            "model_text": "In my opinion, we should not trust all the news we see on social media. First of all, anyone can post information online, and it is not always checked by experts. For example, I once saw a post saying that fish can fly, but when I searched on a science website, it was completely false. Secondly, some people share fake news on purpose to get more likes and followers. Therefore, I believe we should always check the source before believing or sharing any news. We can use trusted news websites and ask our teachers or parents for help.",
            "structure_notes": [
                "State your opinion clearly in the first sentence.",
                "Give at least two reasons with examples.",
                "Use linking words (First of all, Secondly, Therefore).",
                "End with a recommendation or call to action."
            ],
            "writing_prompt": "Write an opinion paragraph (80-100 words): 'Should young people get their news from social media?' Give reasons for your answer."
        },
        5: {
            "genre": "advice leaflet",
            "title": "Top Tips for a Healthy Life",
            "model_text": "Do you want to feel great every day? Here are some tips for a healthy life! First, eat a balanced diet with plenty of fruit, vegetables, and whole grains. Try to avoid too much sugar and junk food. Second, exercise for at least sixty minutes every day. You can walk, ride a bike, or play a sport you enjoy. Third, get eight to ten hours of sleep each night so your body and mind can rest. Finally, take care of your mental health. Talk to a friend or family member when you feel worried. Remember, small changes lead to big results!",
            "structure_notes": [
                "Start with an engaging question or statement.",
                "Organise tips using sequence words (First, Second, Finally).",
                "Use imperatives (Eat, Try, Get, Talk).",
                "End with an encouraging closing sentence."
            ],
            "writing_prompt": "Write an advice leaflet (80-100 words) giving teenagers tips on how to stay healthy. Include at least three tips."
        },
        6: {
            "genre": "informative paragraph",
            "title": "The Red Planet: Mars",
            "model_text": "Mars is the fourth planet from the Sun and is often called the Red Planet because of its reddish colour. It is about half the size of Earth. Mars has the tallest volcano in the solar system — Olympus Mons — which is almost three times higher than Mount Everest. Scientists believe that Mars once had water on its surface, and they are still searching for signs of life there. Several space agencies, including NASA, have sent robots called rovers to explore Mars. Many people dream of sending humans to Mars in the future. It would be the greatest adventure in the history of space exploration.",
            "structure_notes": [
                "Introduce the topic with a key fact.",
                "Include at least three interesting details.",
                "Use present simple for general facts.",
                "End with a forward-looking or inspiring statement."
            ],
            "writing_prompt": "Write an informative paragraph (80-100 words) about a planet or moon. Include at least three interesting facts."
        },
        7: {
            "genre": "narrative paragraph",
            "title": "Starting Over in a New Country",
            "model_text": "When Yusuf was eleven, his family moved from Syria to Turkey. The first day at his new school was terrifying. He could not understand what the teacher was saying, and the other students stared at him curiously. During lunch break, he sat alone under a tree. Then a boy named Burak walked up and offered him half of his sandwich. Burak pointed to himself and said his name slowly. Yusuf smiled and said his own name. From that day, they became best friends. Burak helped Yusuf learn Turkish, and Yusuf taught Burak some Arabic words. Sometimes, all you need is one kind person to make a new place feel like home.",
            "structure_notes": [
                "Set the scene (who, where, when).",
                "Describe the problem or challenge.",
                "Show a turning point through a small action.",
                "End with a reflection or moral."
            ],
            "writing_prompt": "Write a short narrative (80-100 words) about someone who moves to a new place. What challenges do they face and how do they overcome them?"
        },
        8: {
            "genre": "film review",
            "title": "Review: The Lost Robot",
            "model_text": "Last weekend, I watched an animated film called 'The Lost Robot.' It is about a small robot named Pixel who gets lost in a big city and tries to find its family. The animation was colourful and the characters were lovable. My favourite scene was when Pixel learned to fly using old helicopter parts. The soundtrack was exciting, especially during the chase scenes. I think the message of the film is important: never give up, even when things seem impossible. I would recommend this film to anyone who loves adventure and technology. I give it four and a half stars out of five.",
            "structure_notes": [
                "Give the title, genre, and a brief plot summary.",
                "Describe what you liked (visuals, characters, music).",
                "Mention the film's message or theme.",
                "End with a recommendation and rating."
            ],
            "writing_prompt": "Write a review (80-100 words) of a film you have watched recently. Include the title, what it is about, what you liked, and a rating."
        },
        9: {
            "genre": "for-and-against paragraph",
            "title": "Is AI Good for Students?",
            "model_text": "Artificial intelligence is becoming a big part of education, but is it good for students? On the one hand, AI can help students learn faster. For example, AI apps can give personalised exercises based on what you need to practise. They can also answer questions instantly, which saves time. On the other hand, some people worry that students will become lazy and stop thinking for themselves. If AI does all the work, we might not learn how to solve problems on our own. In my opinion, AI is a useful tool, but we should use it wisely and never stop using our own brains.",
            "structure_notes": [
                "Introduce the topic with a question.",
                "Present arguments for (On the one hand).",
                "Present arguments against (On the other hand).",
                "Give your own balanced opinion at the end."
            ],
            "writing_prompt": "Write a for-and-against paragraph (80-100 words): 'Is technology helping or harming young people?' Give both sides and your opinion."
        },
        10: {
            "genre": "persuasive paragraph",
            "title": "Every Child Deserves Education",
            "model_text": "I strongly believe that every child in the world deserves access to education. Education gives children knowledge, skills, and confidence to build a better future. Without it, millions of children cannot escape poverty or fulfil their potential. According to UNICEF, around 244 million children worldwide are not in school. This is unacceptable. Governments should invest more money in building schools and training teachers, especially in rural areas. We, as students, can also help by raising awareness and supporting organisations that provide education to children in need. Together, we can make sure that no child is left behind.",
            "structure_notes": [
                "State your opinion strongly in the opening sentence.",
                "Explain why the issue matters with facts or statistics.",
                "Suggest what should be done (call to action).",
                "End with a hopeful or powerful closing statement."
            ],
            "writing_prompt": "Write a persuasive paragraph (80-100 words) about a human right you feel strongly about. State your opinion, give reasons, and suggest a solution."
        }
    }
}

PRONUNCIATION_BANK = {
    7: {
        1: {
            "focus": "Word stress in two-syllable words",
            "explanation": "In English, two-syllable nouns usually have stress on the first syllable (e.g., HObby), while two-syllable verbs often have stress on the second syllable (e.g., deCIDE). Getting the stress right helps people understand you more easily.",
            "examples": ["HObby (noun)", "PERson (noun)", "deCIDE (verb)", "beLIEVE (verb)", "CREAtive (first syllable stress)"],
            "tongue_twister": "Peter's perfect personal profile proves his proud personality.",
            "practice_words": ["hobby", "person", "believe", "decide", "value", "describe", "unique", "respect"]
        },
        2: {
            "focus": "The /θ/ and /ð/ sounds (th)",
            "explanation": "English has two 'th' sounds. The voiceless /θ/ (as in 'think') and the voiced /ð/ (as in 'this'). Put your tongue gently between your teeth and blow air for /θ/, or add your voice for /ð/. Many languages don't have these sounds, so practice is important.",
            "examples": ["think /θ/", "this /ð/", "together /ð/", "thousand /θ/", "the /ð/"],
            "tongue_twister": "These three thoughtful brothers gathered their things together on Thursday.",
            "practice_words": ["tradition", "the", "them", "think", "both", "weather", "thankful", "together"]
        },
        3: {
            "focus": "Silent letters",
            "explanation": "English has many words with silent letters — letters that are written but not pronounced. For example, the 'k' in 'know' and the 'w' in 'write' are silent. Learning these helps your reading and spelling.",
            "examples": ["know (silent k)", "write (silent w)", "listen (silent t)", "science (silent c)", "design (silent g)"],
            "tongue_twister": "The knight knew he should knock on the knob with his knuckles.",
            "practice_words": ["knowledge", "write", "listen", "design", "science", "half", "would", "psychology"]
        },
        4: {
            "focus": "Sentence stress and content words",
            "explanation": "In English sentences, content words (nouns, main verbs, adjectives, adverbs) are stressed, while function words (articles, prepositions, pronouns) are usually unstressed. This creates the natural rhythm of English.",
            "examples": ["I READ the NEWS on my PHONE.", "She CHECKED the SOURCE of the ARTICLE.", "FAKE news SPREADS very QUICKLY.", "We SHOULD be CAREFUL ONLINE.", "The MEDIA can INFLUENCE our THINKING."],
            "tongue_twister": "Six sharp smart sharks share short shocking stories on social media.",
            "practice_words": ["media", "article", "source", "believe", "reliable", "accurate", "headline", "information"]
        },
        5: {
            "focus": "Short and long vowel sounds: /ɪ/ vs /iː/",
            "explanation": "The short /ɪ/ (as in 'fit') and long /iː/ (as in 'feet') sound similar but change word meanings. For /iː/, spread your lips wider and hold the sound longer. For /ɪ/, keep it short and relaxed.",
            "examples": ["fit /ɪ/ vs feet /iː/", "sit /ɪ/ vs seat /iː/", "live /ɪ/ vs leave /iː/", "ship /ɪ/ vs sheep /iː/", "hill /ɪ/ vs heal /iː/"],
            "tongue_twister": "She sits and eats sweet treats to feel fit and keep her teeth clean.",
            "practice_words": ["sleep", "sick", "fitness", "eat", "drink", "still", "breathe", "feeling"]
        },
        6: {
            "focus": "Stress in three-syllable words",
            "explanation": "Three-syllable words can have stress on any syllable. Pay attention to where the stress falls: UNiverse (first), asTRONaut (first), disCOVer (second), underSTAND (third). Dictionaries show stress with a mark (') before the stressed syllable.",
            "examples": ["Universe (U-ni-verse)", "asTROnaut (as-TRO-naut)", "disCOVer (dis-COV-er)", "PLANet (PLA-net)", "teLEScope (TE-le-scope)"],
            "tongue_twister": "The astronaut discovered the universe through a telescope from a satellite.",
            "practice_words": ["universe", "astronaut", "discover", "satellite", "galaxy", "telescope", "atmosphere", "gravity"]
        },
        7: {
            "focus": "Connected speech: linking sounds",
            "explanation": "In natural English, words are often linked together. When a word ends in a consonant and the next word starts with a vowel, they connect smoothly: 'moved_away' sounds like 'moovdaway'. This makes speech flow naturally.",
            "examples": ["moved away → moov-daway", "pick up → pi-kup", "an old friend → a-nold friend", "come in → co-min", "left out → lef-tout"],
            "tongue_twister": "An old immigrant arrived in an unfamiliar area and asked about an apartment.",
            "practice_words": ["moved", "arrived", "left", "welcome", "belong", "accepted", "adapted", "community"]
        },
        8: {
            "focus": "Intonation: rising and falling patterns",
            "explanation": "In English, statements and wh-questions use falling intonation (voice goes down at the end). Yes/no questions use rising intonation (voice goes up). Getting this right makes you sound more natural and helps listeners understand if you are asking or telling.",
            "examples": ["I loved the film. (falling ↘)", "Did you like it? (rising ↗)", "What was your favourite scene? (falling ↘)", "Was it exciting? (rising ↗)", "The acting was brilliant. (falling ↘)"],
            "tongue_twister": "Was the film fantastic? The film was absolutely fantastic!",
            "practice_words": ["film", "cinema", "review", "recommend", "acting", "exciting", "favourite", "brilliant"]
        },
        9: {
            "focus": "The schwa sound /ə/",
            "explanation": "The schwa /ə/ is the most common vowel sound in English. It appears in unstressed syllables and sounds like a short, lazy 'uh'. For example: computer → com-PYOO-tə, digital → DI-gi-təl. Recognising it helps your listening and pronunciation.",
            "examples": ["computer /kəmˈpjuːtər/", "digital /ˈdɪdʒɪtəl/", "internet /ˈɪntənet/", "problem /ˈprɒbləm/", "support /səˈpɔːt/"],
            "tongue_twister": "A computer can support a digital system to solve a common problem.",
            "practice_words": ["computer", "digital", "internet", "about", "problem", "system", "artificial", "password"]
        },
        10: {
            "focus": "Emphatic stress for meaning",
            "explanation": "In English, you can change the meaning of a sentence by stressing different words. 'EVERY child deserves education' (emphasises all children). 'Every child DESERVES education' (emphasises the right). This is very useful in persuasive speaking.",
            "examples": ["EVERY child deserves education. (all children, not just some)", "Every child DESERVES education. (it's their right)", "Every child deserves EDUCATION. (education specifically)", "We MUST protect human rights. (it's necessary)", "Human rights are for EVERYONE. (no exceptions)"],
            "tongue_twister": "EVERY person DESERVES respect, EVERY voice DESERVES to be heard, EVERYWHERE.",
            "practice_words": ["rights", "freedom", "justice", "equality", "deserve", "protect", "everyone", "important"]
        }
    }
}

WORKBOOK_BANK = {
    7: {
        1: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete the sentences with the correct word from the box: creative, hobby, unique, personality, confident.", "items": ["Drawing is my favourite ____. (hobby)", "She has a very friendly ____. (personality)", "Everyone is ____ in their own way. (unique)", "He is very ____ when he speaks in public. (confident)", "Elif is a ____ person who loves art. (creative)"]},
                {"type": "matching", "instruction": "Match the adjectives to their meanings.", "items": ["curious — wanting to learn new things", "generous — willing to share with others", "patient — able to wait without getting angry", "reliable — someone you can trust", "ambitious — having big goals for the future"]},
                {"type": "multiple_choice", "instruction": "Choose the correct option to complete each sentence.", "items": ["I ____ drawing since I was five. (a) enjoy b) enjoys c) enjoying) → a", "She is ____ person in our class. (a) most creative b) the most creative c) more creative) → b", "My brother and I are very ____ from each other. (a) different b) difference c) differ) → a"]},
                {"type": "ordering", "instruction": "Put the words in the correct order to make sentences.", "items": ["am / I / a / person / curious / very → I am a very curious person.", "hobbies / What / your / are / ? → What are your hobbies?", "in / is / the future / She / interested → She is interested in the future."]},
                {"type": "writing", "instruction": "Write three sentences about yourself using the words below.", "items": ["Use: personality, hobby, dream", "Example: My personality is friendly and cheerful.", "Write about what makes you unique."]}
            ]
        },
        2: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete the text about traditions with the correct words: celebrate, customs, gather, traditional, respect.", "items": ["In Turkey, families ____ together during Bayram. (gather)", "We ____ special holidays with food and music. (celebrate)", "Every country has its own ____ and habits. (customs)", "People wear ____ clothes on special days. (traditional)", "We should ____ all cultures and beliefs. (respect)"]},
                {"type": "true_false", "instruction": "Read the statements and write True or False.", "items": ["Traditions are the same in every country. (False)", "Customs can include food, clothing, and music. (True)", "Festivals are only celebrated in Turkey. (False)", "Respecting other cultures is important. (True)", "Traditional clothes are never worn today. (False)"]},
                {"type": "matching", "instruction": "Match each country to its tradition.", "items": ["Turkey — Ramadan Bayram", "China — Mid-Autumn Festival", "Mexico — Day of the Dead", "India — Diwali", "Japan — Cherry Blossom Viewing"]},
                {"type": "multiple_choice", "instruction": "Choose the correct preposition.", "items": ["We celebrate Bayram ____ spring. (a) at b) in c) on) → b", "The festival takes place ____ March 21st. (a) in b) at c) on) → c", "Families get together ____ special occasions. (a) on b) in c) at) → a"]},
                {"type": "writing", "instruction": "Write a short paragraph (4-5 sentences) about a tradition you enjoy.", "items": ["Include: what it is called, when it happens, what you do, why you like it."]}
            ]
        },
        3: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete each sentence with a job title: architect, surgeon, journalist, software engineer, veterinarian.", "items": ["A ____ designs buildings and structures. (architect)", "A ____ writes news articles and reports. (journalist)", "A ____ operates on patients in hospitals. (surgeon)", "A ____ creates computer programmes. (software engineer)", "A ____ takes care of sick animals. (veterinarian)"]},
                {"type": "matching", "instruction": "Match each job to the skill it requires.", "items": ["Teacher — patience and communication", "Pilot — concentration and quick thinking", "Chef — creativity and attention to detail", "Nurse — compassion and physical stamina", "Translator — language skills and accuracy"]},
                {"type": "multiple_choice", "instruction": "Choose the correct future form.", "items": ["I ____ a doctor when I grow up. (a) will be b) am being c) was) → a", "She ____ medicine at university next year. (a) studies b) is going to study c) studied) → b", "They ____ their career project tomorrow. (a) present b) are going to present c) presented) → b"]},
                {"type": "ordering", "instruction": "Put these career steps in a logical order.", "items": ["1. Finish secondary school.", "2. Go to university.", "3. Get a degree.", "4. Apply for a job.", "5. Start your career."]},
                {"type": "writing", "instruction": "Write about your dream job in 4-5 sentences.", "items": ["Include: what job, why you want it, what skills you need, what you will do."]}
            ]
        },
        4: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete with: headline, source, reliable, fake, advertisement.", "items": ["Always check the ____ of a news article before you believe it. (source)", "A ____ tries to sell you a product or service. (advertisement)", "The ____ of a news story should give you a clear idea of the topic. (headline)", "A ____ website has accurate and checked information. (reliable)", "____ news is information that is not true. (fake)"]},
                {"type": "true_false", "instruction": "True or False?", "items": ["Every website on the internet is reliable. (False)", "You should check at least two sources before sharing news. (True)", "Advertisements always tell the complete truth. (False)", "A good news article has an author and a date. (True)", "Social media posts are always verified by experts. (False)"]},
                {"type": "matching", "instruction": "Match the media terms to their definitions.", "items": ["bias — showing only one side of a story", "clickbait — a sensational headline to get clicks", "fact-check — to verify if something is true", "editorial — an opinion piece by an editor", "viral — content that spreads very quickly online"]},
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": ["Which is the most reliable source? (a) a random blog b) an encyclopedia c) a social media post) → b", "What should a good news article include? (a) lots of emojis b) the author, date, and sources c) only pictures) → b", "What does 'fact-check' mean? (a) to write facts b) to verify information c) to count facts) → b"]},
                {"type": "writing", "instruction": "Write 4-5 sentences explaining how to identify fake news.", "items": ["Use words like: source, check, reliable, author, evidence."]}
            ]
        },
        5: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete with: balanced, exercise, mental, nutrition, hygiene.", "items": ["Eating a ____ diet means having different types of food. (balanced)", "Physical ____ keeps your body strong and healthy. (exercise)", "____ health is about how you feel emotionally. (Mental)", "Good ____ means keeping your body clean. (hygiene)", "____ is the study of food and how it affects our body. (Nutrition)"]},
                {"type": "matching", "instruction": "Match the health tip to the correct category.", "items": ["Eat five portions of fruit and vegetables — Nutrition", "Walk or run for 60 minutes daily — Exercise", "Sleep 8-10 hours per night — Rest", "Talk to someone when you feel sad — Mental Health", "Wash your hands before eating — Hygiene"]},
                {"type": "multiple_choice", "instruction": "Choose the correct modal verb.", "items": ["You ____ eat breakfast every morning. (a) should b) shouldn't c) mustn't) → a", "Teenagers ____ skip meals regularly. (a) should b) shouldn't c) must) → b", "We ____ drink at least six glasses of water a day. (a) shouldn't b) mustn't c) should) → c"]},
                {"type": "true_false", "instruction": "True or False?", "items": ["Teenagers need only four hours of sleep. (False)", "Junk food is part of a balanced diet if eaten in moderation. (True)", "Exercise is only important for adults. (False)", "Mental health is as important as physical health. (True)", "You should never talk about your feelings. (False)"]},
                {"type": "writing", "instruction": "Write a daily health routine (4-5 sentences).", "items": ["Include: what time you wake up, what you eat, how you exercise, when you sleep."]}
            ]
        },
        6: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete with: orbit, gravity, atmosphere, rover, galaxy.", "items": ["Earth's ____ is the layer of gases that surrounds it. (atmosphere)", "The Moon takes about 27 days to ____ the Earth. (orbit)", "____ is the force that keeps us on the ground. (Gravity)", "NASA sent a ____ to explore the surface of Mars. (rover)", "The Milky Way is the ____ that contains our solar system. (galaxy)"]},
                {"type": "matching", "instruction": "Match the planet to the fact.", "items": ["Mercury — closest to the Sun", "Venus — hottest planet", "Mars — called the Red Planet", "Jupiter — largest planet", "Neptune — farthest from the Sun"]},
                {"type": "ordering", "instruction": "Put the planets in order from the Sun (closest to farthest).", "items": ["1. Mercury", "2. Venus", "3. Earth", "4. Mars", "5. Jupiter"]},
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": ["How many planets are in our solar system? (a) 7 b) 8 c) 9) → b", "What is the Sun? (a) a planet b) a moon c) a star) → c", "What force keeps planets in orbit? (a) magnetism b) gravity c) wind) → b"]},
                {"type": "writing", "instruction": "Imagine you are an astronaut. Write 4-5 sentences about a day in space.", "items": ["Include: what you see, what you eat, how you move, what experiment you do."]}
            ]
        },
        7: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete with: immigrant, refugee, adapt, belong, community.", "items": ["An ____ is someone who moves to another country to live. (immigrant)", "A ____ leaves their country because of war or danger. (refugee)", "It takes time to ____ to a new culture and language. (adapt)", "Everyone wants to ____ and feel accepted. (belong)", "A welcoming ____ helps newcomers feel at home. (community)"]},
                {"type": "matching", "instruction": "Match the words to their opposites.", "items": ["welcome — reject", "arrive — depart", "include — exclude", "friend — stranger", "courage — fear"]},
                {"type": "multiple_choice", "instruction": "Choose the correct past tense form.", "items": ["They ____ to a new country last year. (a) move b) moved c) moving) → b", "She ____ lonely on her first day. (a) feel b) feels c) felt) → c", "The family ____ a small apartment near the school. (a) find b) found c) finding) → b"]},
                {"type": "true_false", "instruction": "True or False?", "items": ["Migration only happened in the past. (False)", "Refugees leave their homes by choice. (False)", "Learning a new language helps immigrants adapt. (True)", "Immigrants can only speak one language. (False)", "Being kind to newcomers costs nothing. (True)"]},
                {"type": "writing", "instruction": "Write 4-5 sentences about how you would help a new student in your class.", "items": ["Use: welcome, help, show, introduce, friend."]}
            ]
        },
        8: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete with: soundtrack, plot, genre, character, scene.", "items": ["The ____ of the film was very exciting with many twists. (plot)", "My favourite ____ in the movie is when the hero escapes. (scene)", "The ____ had beautiful music that matched the emotions perfectly. (soundtrack)", "Action is a popular film ____. (genre)", "The main ____ was a brave young girl named Luna. (character)"]},
                {"type": "matching", "instruction": "Match the film genre to its description.", "items": ["comedy — a film that makes you laugh", "horror — a film that scares you", "documentary — a film about real events or topics", "animation — a film made with drawings or computer graphics", "science fiction — a film about future technology or space"]},
                {"type": "multiple_choice", "instruction": "Choose the correct adjective.", "items": ["The film was really ____. I couldn't stop watching! (a) bored b) boring c) gripping) → c", "I was ____ by the sad ending. (a) touched b) touching c) touch) → a", "The special effects were ____! (a) amazed b) amazing c) amaze) → b"]},
                {"type": "ordering", "instruction": "Put these steps for making a film in order.", "items": ["1. Write the script.", "2. Choose the actors.", "3. Film the scenes.", "4. Edit the film.", "5. Show it to the audience."]},
                {"type": "writing", "instruction": "Write a short film review (4-5 sentences).", "items": ["Include: film title, genre, what you liked, your rating out of 5."]}
            ]
        },
        9: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete with: algorithm, cyberbullying, download, password, artificial intelligence.", "items": ["____ is when computers can think and learn like humans. (Artificial intelligence)", "Never share your ____ with strangers. (password)", "____ is bullying that happens online. (Cyberbullying)", "You can ____ apps and games from the internet. (download)", "An ____ is a set of instructions that a computer follows. (algorithm)"]},
                {"type": "matching", "instruction": "Match the digital term to its meaning.", "items": ["browser — software used to access websites", "cloud storage — saving files on the internet", "coding — writing instructions for computers", "firewall — security system that protects networks", "hashtag — a word preceded by # to categorise content"]},
                {"type": "true_false", "instruction": "True or False?", "items": ["AI can learn from data. (True)", "You should use the same password for everything. (False)", "Cyberbullying is not a real problem. (False)", "Coding is only for adults. (False)", "Screen time should be balanced with outdoor activities. (True)"]},
                {"type": "multiple_choice", "instruction": "Choose the correct answer.", "items": ["What does AI stand for? (a) Auto Internet b) Artificial Intelligence c) Advanced Information) → b", "Which is a safe online practice? (a) sharing your address b) using strong passwords c) clicking every link) → b", "What is an algorithm? (a) a type of computer b) a set of instructions c) a social media app) → b"]},
                {"type": "writing", "instruction": "Write 4-5 sentences about how you use technology safely.", "items": ["Include: what devices you use, how you protect your privacy, your screen time rules."]}
            ]
        },
        10: {
            "exercises": [
                {"type": "fill_in", "instruction": "Complete with: equality, freedom, protection, justice, discrimination.", "items": ["____ means treating everyone fairly, regardless of differences. (Equality)", "Every person has the right to ____ of speech. (freedom)", "Children have the right to ____ from violence and abuse. (protection)", "____ means that laws are applied fairly to everyone. (Justice)", "____ means treating someone unfairly because of who they are. (Discrimination)"]},
                {"type": "matching", "instruction": "Match each right to an example.", "items": ["Right to education — Every child can go to school.", "Right to healthcare — Sick people can see a doctor.", "Freedom of expression — You can share your opinions.", "Right to play — Children have time for games and rest.", "Right to identity — Every child has a name and nationality."]},
                {"type": "true_false", "instruction": "True or False?", "items": ["Human rights only apply to adults. (False)", "The UN Declaration of Human Rights was adopted in 1948. (True)", "Discrimination is acceptable in some situations. (False)", "Children have the right to be heard. (True)", "Everyone is born free and equal in dignity. (True)"]},
                {"type": "multiple_choice", "instruction": "Choose the correct passive form.", "items": ["Human rights ____ protected by international law. (a) is b) are c) was) → b", "The Declaration ____ signed by many countries. (a) is b) were c) was) → c", "Children ____ be protected from all forms of violence. (a) can b) must c) might) → b"]},
                {"type": "writing", "instruction": "Write 4-5 sentences about a human right that is important to you.", "items": ["Include: which right, why it matters, what we can do to protect it."]}
            ]
        }
    }
}

TURKEY_CORNER_BANK = {
    7: {
        1: {
            "title": "Famous Turkish Figures",
            "text": "Turkey has many inspiring people who have shaped history and culture. Mustafa Kemal Ataturk founded the modern Turkish Republic in 1923 and brought many important reforms, including equal rights for women. Aziz Sancar, a Turkish scientist, won the Nobel Prize in Chemistry in 2015 for his research on DNA repair. Barish Mancho was a beloved musician who sang folk-rock songs that people still enjoy today. These individuals show that with hard work and determination, you can achieve great things and inspire the world.",
            "image_desc": "A collage showing portraits of Ataturk, Aziz Sancar, and Barish Mancho with a Turkish flag in the background.",
            "discussion_q": "Which Turkish person do you admire the most and why?"
        },
        2: {
            "title": "Turkish Wedding Traditions",
            "text": "Turkish weddings are full of beautiful customs. Before the wedding day, there is a henna night where the bride's hands are decorated with henna patterns while guests sing emotional songs. On the wedding day, the groom's family arrives with a convoy of cars honking their horns. At the ceremony, guests pin gold coins or banknotes on the bride and groom as gifts. Traditional foods like rice pilaf, kebab, and baklava are served. Dancing to folk music, especially the halay, brings everyone together. These traditions show the importance of family and community in Turkish culture.",
            "image_desc": "A joyful Turkish wedding scene with guests dancing halay, the bride with henna on her hands, and gold coins pinned on ribbons.",
            "discussion_q": "What are some wedding traditions in your culture? How are they similar to or different from Turkish ones?"
        },
        3: {
            "title": "Traditional Turkish Professions",
            "text": "Turkey has a rich history of traditional professions that are still valued today. Coppersmiths in Gaziantep and Mardin hammer beautiful plates, trays, and coffee pots by hand. Carpet weavers in Hereke and Kayseri create world-famous handmade carpets with intricate patterns. Baklava masters in Gaziantep learn their craft over many years to produce perfectly thin layers of pastry. Ebru artists create stunning marbled paper art by floating paints on water. These traditional professions keep Turkish heritage alive and show that craftsmanship is a career worth respecting.",
            "image_desc": "A split image showing a coppersmith at work, a carpet weaver at a loom, and an ebru artist creating marbled patterns.",
            "discussion_q": "Would you like to learn a traditional Turkish craft? Which one interests you?"
        },
        4: {
            "title": "TRT and Turkish Media History",
            "text": "TRT, the Turkish Radio and Television Corporation, started broadcasting radio in 1927 and television in 1968. For many years, TRT was the only TV channel in Turkey. Today, Turkey has hundreds of TV channels, newspapers, and online news platforms. Turkish TV series, known as 'diziler,' are now popular in over 150 countries. Shows like 'Ertugrul' have millions of fans worldwide. Turkey is the second-largest exporter of TV series after the United States. Turkish media has grown from one radio station to a global entertainment powerhouse.",
            "image_desc": "A timeline showing the evolution of Turkish media from a vintage radio to modern TV screens displaying popular Turkish series.",
            "discussion_q": "Do you watch any Turkish TV series? What do you think makes them popular internationally?"
        },
        5: {
            "title": "Turkish Cuisine and Health",
            "text": "Turkish cuisine is one of the healthiest in the world because it uses fresh ingredients and balanced combinations. A traditional Turkish breakfast includes olives, cheese, tomatoes, cucumbers, eggs, and fresh bread — all nutritious and delicious. Yoghurt, which originated in Central Asia and became a staple in Turkey, is excellent for digestion. Lentil soup is a favourite across the country and is rich in protein and iron. Ayran, a drink made from yoghurt, water, and salt, is a natural and refreshing way to stay hydrated. The Mediterranean diet, common in southern Turkey, is considered one of the healthiest in the world.",
            "image_desc": "A colourful spread of a traditional Turkish breakfast with olives, cheese, bread, and a glass of ayran.",
            "discussion_q": "What is your favourite Turkish food? Do you think Turkish cuisine is healthy? Why or why not?"
        },
        6: {
            "title": "Turkey's Space Programme",
            "text": "Turkey has been investing in space technology and research. The Turkish Space Agency (TUA) was established in 2018 with the goal of developing Turkey's own satellite systems and contributing to space exploration. Turkey has already launched several communication and observation satellites, including Turksat and GOKTURK series. In 2023, Alper Gezeravci became the first Turkish astronaut to go to space as part of a mission to the International Space Station. Turkey's national space programme aims to send a Turkish-made rover to the Moon. These achievements show that Turkey is reaching for the stars.",
            "image_desc": "An illustration of a satellite orbiting Earth with the Turkish flag, and a photo of Alper Gezeravci in an astronaut suit.",
            "discussion_q": "Would you like to be an astronaut? What do you think Turkey's space programme should focus on?"
        },
        7: {
            "title": "Turkey: A Land of Migration",
            "text": "Throughout history, Turkey has been both a source and destination of migration. In the 1960s, many Turkish workers moved to Germany, the Netherlands, and other European countries for better job opportunities. They are known as 'gurbetciler.' Today, their descendants form large communities in Europe. In recent years, Turkey has welcomed millions of refugees, especially from Syria, making it the country hosting the largest refugee population in the world. Turkish culture has always valued hospitality, known as 'misafirperverlik.' Helping newcomers and sharing food and shelter are deeply rooted in Turkish traditions.",
            "image_desc": "A map showing migration routes from Turkey to Europe, and a warm scene of a Turkish family welcoming neighbours with tea.",
            "discussion_q": "Why do you think hospitality is such an important value in Turkish culture?"
        },
        8: {
            "title": "Yesilcam: Turkish Cinema",
            "text": "Yesilcam is the name given to the golden age of Turkish cinema, roughly from the 1950s to the 1980s. The name comes from a street in Istanbul where many film studios were located. During this period, hundreds of films were produced every year. Stars like Turkan Shoray, Kemal Sunal, and Adile Nasit became household names. Kemal Sunal was especially famous for his comedy films that made audiences laugh while also carrying social messages. Today, Turkish cinema continues to grow with internationally acclaimed directors like Nuri Bilge Ceylan, who won the Palme d'Or at the Cannes Film Festival.",
            "image_desc": "A vintage film reel with classic Yesilcam movie posters and a modern cinema screen showing a Nuri Bilge Ceylan film.",
            "discussion_q": "Have you watched any classic Turkish films? Which Turkish actor or director would you like to learn more about?"
        },
        9: {
            "title": "Technology Start-ups in Turkey",
            "text": "Turkey has a growing technology scene with many successful start-ups. Istanbul, Ankara, and Izmir are home to hundreds of tech companies. Trendyol, one of Turkey's biggest e-commerce platforms, became internationally known after expanding its services. Peak Games, a Turkish mobile gaming company, was sold for over a billion dollars. Turkey also has a strong community of young coders and software developers. Organisations like Habitat and coding boot camps teach programming skills to young people across the country. The Turkish government supports technology with programmes in technoparks at universities.",
            "image_desc": "A modern co-working space in Istanbul with young developers at computers, surrounded by screens showing apps and code.",
            "discussion_q": "Would you like to create your own app or start a technology company? What problem would your app solve?"
        },
        10: {
            "title": "Children's Rights in Turkey",
            "text": "April 23rd is both National Sovereignty Day and Children's Day in Turkey, making it unique in the world. Ataturk dedicated this day to children because he believed they are the future of the nation. On this day, children from many countries visit Turkey and participate in celebrations. They take seats in the Turkish parliament, symbolising children's voices in democracy. Turkey was one of the first countries to sign the UN Convention on the Rights of the Child in 1990. Turkish schools teach human rights as part of the curriculum, and organisations like UNICEF Turkey work to protect every child's right to education, health, and safety.",
            "image_desc": "Children sitting in the Turkish Grand National Assembly on April 23rd, waving small flags from different countries.",
            "discussion_q": "Why do you think Ataturk dedicated April 23rd to children? What does this day mean to you?"
        }
    }
}

COMIC_STRIP_BANK = {
    7: {
        1: {
            "title": "Who Am I?",
            "panels": [
                {"panel": 1, "scene": "Classroom. Mr. Demir writes 'Personal Identity' on the board.", "dialogue": "Mr. Demir: Today we will explore who we really are. Elif, can you start?"},
                {"panel": 2, "scene": "Elif stands up, holding a notebook with drawings.", "dialogue": "Elif: My name is Elif. I love drawing and I am very curious about everything!"},
                {"panel": 3, "scene": "Kwame raises his hand excitedly.", "dialogue": "Kwame: I'm Kwame. I play football and I'm from Ghana. I like learning about different cultures."},
                {"panel": 4, "scene": "Mei and Carlos smile at each other.", "dialogue": "Mei: I'm Mei — I love science fiction! Carlos: And I'm Carlos — music is my life!"},
                {"panel": 5, "scene": "All four students stand together, smiling. Mr. Demir nods proudly.", "dialogue": "Mr. Demir: See? We are all unique, and that's what makes our class wonderful!"}
            ]
        },
        2: {
            "title": "The Festival Mix-Up",
            "panels": [
                {"panel": 1, "scene": "School hallway. Poster says 'International Culture Day'.", "dialogue": "Elif: I brought baklava for our culture fair! Kwame: And I have some Ghanaian jollof rice!"},
                {"panel": 2, "scene": "Mei is carrying a box of mooncakes, but she trips and almost drops them.", "dialogue": "Mei: Oh no, my mooncakes! Carlos: I've got you! (catches the box)"},
                {"panel": 3, "scene": "They set up a table with foods from all four countries.", "dialogue": "Carlos: I brought Mexican tamales. Let's put everything together on one big table!"},
                {"panel": 4, "scene": "Students from other classes gather around the table, excited.", "dialogue": "Student: Wow, so many different foods! Can I try everything? Elif: Of course! That's the whole point!"},
                {"panel": 5, "scene": "Everyone eating and laughing together.", "dialogue": "Mr. Demir: This is beautiful. Different traditions, one happy table. That's what culture is about!"}
            ]
        },
        3: {
            "title": "Career Day Surprise",
            "panels": [
                {"panel": 1, "scene": "Classroom decorated with 'Career Day' banner. Students sit eagerly.", "dialogue": "Mr. Demir: Today we have three guests to talk about their jobs!"},
                {"panel": 2, "scene": "A woman in a lab coat enters.", "dialogue": "Dr. Ayse: I'm a surgeon. I save lives every day. You need patience and steady hands."},
                {"panel": 3, "scene": "Kwame whispers to Carlos.", "dialogue": "Kwame: I thought I only wanted to be a footballer, but engineering sounds cool too! Carlos: I know, right?"},
                {"panel": 4, "scene": "Ms. Rivera shows photos from her travels.", "dialogue": "Ms. Rivera: As a journalist, I travel the world to find the truth. Elif: That's my dream job!"},
                {"panel": 5, "scene": "After the talks, students write their dream jobs on sticky notes for a wall display.", "dialogue": "Mei: I wrote scientist. What about you, Carlos? Carlos: Musician AND engineer! Why not both?"}
            ]
        },
        4: {
            "title": "The Fake News Detective",
            "panels": [
                {"panel": 1, "scene": "Kwame is looking at his phone with a shocked face.", "dialogue": "Kwame: Guys, look at this! It says chocolate makes you a genius!"},
                {"panel": 2, "scene": "Elif looks over his shoulder skeptically.", "dialogue": "Elif: Wait... who wrote that article? Is there an author's name? Kwame: Hmm, no..."},
                {"panel": 3, "scene": "Mei opens her laptop.", "dialogue": "Mei: Let me check a science website. Nope — it's completely false! There's no evidence."},
                {"panel": 4, "scene": "Carlos points at the screen.", "dialogue": "Carlos: Look, the website has lots of pop-up ads. That's usually a bad sign."},
                {"panel": 5, "scene": "Mr. Demir gives a thumbs up.", "dialogue": "Mr. Demir: Excellent detective work! Always check the source, the author, and the date. Never share without checking!"}
            ]
        },
        5: {
            "title": "The Breakfast Challenge",
            "panels": [
                {"panel": 1, "scene": "Morning. Carlos yawns in class, looking tired.", "dialogue": "Mr. Demir: Carlos, did you eat breakfast today? Carlos: No, I woke up too late..."},
                {"panel": 2, "scene": "School nurse Ms. Demir visits the class with a food chart.", "dialogue": "Ms. Demir: Skipping breakfast makes you tired and unfocused. Your brain needs fuel!"},
                {"panel": 3, "scene": "Elif shows her lunchbox.", "dialogue": "Elif: I always have cheese, bread, and tomatoes in the morning. It gives me energy all day!"},
                {"panel": 4, "scene": "Students make a 'Healthy Breakfast Challenge' poster.", "dialogue": "Kwame: Let's all eat a healthy breakfast every day for two weeks! Mei: I'll track it on a chart!"},
                {"panel": 5, "scene": "Two weeks later. Carlos is energetic and smiling.", "dialogue": "Carlos: I can't believe the difference! I feel so much better. Thanks, team! Ms. Demir: I'm so proud of you all!"}
            ]
        },
        6: {
            "title": "Mission to Mars",
            "panels": [
                {"panel": 1, "scene": "Science class. A model of the solar system hangs from the ceiling.", "dialogue": "Mr. Demir: Imagine you could visit any planet. Where would you go? Mei: Mars! Definitely Mars!"},
                {"panel": 2, "scene": "Mei draws a rocket on the board.", "dialogue": "Mei: Mars has the tallest volcano in the solar system — Olympus Mons! Carlos: How tall is it?"},
                {"panel": 3, "scene": "Kwame looks up facts on a tablet.", "dialogue": "Kwame: It's almost three times higher than Mount Everest! Elif: That's incredible!"},
                {"panel": 4, "scene": "Students build a model Mars rover from cardboard.", "dialogue": "Carlos: Let's name our rover 'Yildiz' — it means 'star' in Turkish! All: Perfect!"},
                {"panel": 5, "scene": "They present their rover to the class.", "dialogue": "Mr. Demir: Outstanding work! Maybe one of you will build a real Mars rover someday. Keep dreaming big!"}
            ]
        },
        7: {
            "title": "The New Student",
            "panels": [
                {"panel": 1, "scene": "A new student stands nervously at the classroom door.", "dialogue": "Mr. Demir: Class, this is Yara. She just moved here from another country. Let's make her feel welcome."},
                {"panel": 2, "scene": "Yara sits down quietly. She looks at her desk.", "dialogue": "Yara (thinking): I don't know anyone here. I'm scared. Will they like me?"},
                {"panel": 3, "scene": "Elif walks over with a smile and a notebook.", "dialogue": "Elif: Hi Yara! Would you like to sit with us at lunch? Yara: (surprised) Really? Yes, please!"},
                {"panel": 4, "scene": "At lunch, the group chats and laughs.", "dialogue": "Kwame: Where are you from, Yara? Yara: I'm from Jordan. Carlos: Cool! Tell us about it!"},
                {"panel": 5, "scene": "After school, Yara waves goodbye with a big smile.", "dialogue": "Yara: Thank you all so much. I was so worried, but you made me feel like I belong here. Mei: That's what friends are for!"}
            ]
        },
        8: {
            "title": "Lights, Camera, Chaos!",
            "panels": [
                {"panel": 1, "scene": "The group decides to make a short film for a school competition.", "dialogue": "Carlos: Let's make a film! I'll do the music! Elif: I'll write the script! Kwame: I'll act! Mei: I'll direct!"},
                {"panel": 2, "scene": "Filming in the schoolyard. Kwame keeps forgetting his lines.", "dialogue": "Mei: Action! Kwame: 'To be or not to be...' wait, what comes next? Everyone: (laughs)"},
                {"panel": 3, "scene": "Carlos accidentally drops the camera into a bush.", "dialogue": "Carlos: Oops! Don't worry, it's still working! Elif: That's going in the bloopers!"},
                {"panel": 4, "scene": "They watch the edited film together on a laptop.", "dialogue": "Mei: Actually, the bloopers are funnier than the real film! Kwame: Let's submit both!"},
                {"panel": 5, "scene": "Award ceremony. They win 'Funniest Film' trophy.", "dialogue": "Mr. Demir: Congratulations! Making mistakes is part of the creative process. All: We couldn't agree more!"}
            ]
        },
        9: {
            "title": "The AI Debate",
            "panels": [
                {"panel": 1, "scene": "Mr. Demir shows a chatbot on the classroom screen.", "dialogue": "Mr. Demir: This AI can write essays, answer questions, and even create art. What do you think?"},
                {"panel": 2, "scene": "Mei looks amazed. Kwame looks worried.", "dialogue": "Mei: That's amazing! It could help us learn faster! Kwame: But will it replace us?"},
                {"panel": 3, "scene": "Elif raises her hand.", "dialogue": "Elif: I think AI is a tool, like a calculator. It helps, but we still need to think for ourselves."},
                {"panel": 4, "scene": "Carlos tries asking the AI to write a song.", "dialogue": "Carlos: The AI wrote lyrics, but they don't have any real feeling. Real creativity comes from the heart."},
                {"panel": 5, "scene": "Mr. Demir summarises on the board.", "dialogue": "Mr. Demir: AI is powerful, but it needs us to guide it. Use it wisely, and never stop thinking! All: Got it!"}
            ]
        },
        10: {
            "title": "Voices That Matter",
            "panels": [
                {"panel": 1, "scene": "Mr. Demir hands out copies of the UN Declaration of Human Rights.", "dialogue": "Mr. Demir: Every person is born with rights. Today, we'll discuss which ones matter most to you."},
                {"panel": 2, "scene": "Elif reads from the document.", "dialogue": "Elif: 'Everyone has the right to education.' I think this is the most important one."},
                {"panel": 3, "scene": "Kwame stands up passionately.", "dialogue": "Kwame: I choose the right to be protected from violence. Every child should feel safe!"},
                {"panel": 4, "scene": "Mei and Carlos share their choices.", "dialogue": "Mei: Healthcare for everyone! Carlos: Freedom of expression — everyone should have a voice!"},
                {"panel": 5, "scene": "Students create a 'Rights Wall' display in the corridor.", "dialogue": "Mr. Demir: Your voices matter. When you speak up for rights, you make the world a better place. Keep going!"}
            ]
        }
    }
}

GAMIFICATION_BANK = {
    7: {
        "levels": [
            {"level": 1, "title": "Language Explorer", "xp_needed": 0},
            {"level": 2, "title": "Word Warrior", "xp_needed": 500},
            {"level": 3, "title": "Grammar Guardian", "xp_needed": 1200},
            {"level": 4, "title": "Fluency Fighter", "xp_needed": 2500},
            {"level": 5, "title": "English Champion", "xp_needed": 5000}
        ],
        "unit_badges": {
            1: {"name": "Identity Star", "desc": "Completed all Personal Identity activities and described yourself confidently."},
            2: {"name": "Culture Connector", "desc": "Explored traditions from different countries and compared customs."},
            3: {"name": "Career Pathfinder", "desc": "Researched future careers and interviewed a professional."},
            4: {"name": "Media Detective", "desc": "Identified fake news and evaluated media sources like a pro."},
            5: {"name": "Wellness Warrior", "desc": "Mastered health vocabulary and created a healthy living guide."},
            6: {"name": "Space Voyager", "desc": "Explored the solar system and presented space facts with confidence."},
            7: {"name": "Empathy Ambassador", "desc": "Showed understanding of migration stories and welcomed newcomers."},
            8: {"name": "Film Critic", "desc": "Reviewed a film and participated in the class film festival."},
            9: {"name": "Digital Citizen", "desc": "Demonstrated safe online behaviour and discussed AI responsibly."},
            10: {"name": "Rights Defender", "desc": "Advocated for human rights and created an awareness campaign."}
        },
        "bonus_xp": [
            {"task": "Help a classmate understand a difficult grammar point", "xp": 50},
            {"task": "Use five new vocabulary words correctly in one day", "xp": 40},
            {"task": "Complete a bonus reading challenge outside class", "xp": 60},
            {"task": "Present a topic to the class without reading from notes", "xp": 75},
            {"task": "Write a creative story using this unit's vocabulary", "xp": 80}
        ]
    }
}

MISSION_BANK = {
    7: {
        1: {
            "title": "Mission: Know Yourself",
            "objective": "Discover and share what makes you unique by completing identity challenges.",
            "tasks": [
                "Write a 'personal fact file' with 10 facts about yourself in English.",
                "Interview a classmate and create a short profile about them.",
                "Draw a self-portrait and label it with five personality adjectives.",
                "Record a 1-minute spoken introduction of yourself."
            ],
            "reward": "Identity Star badge + 100 XP"
        },
        2: {
            "title": "Mission: Culture Explorer",
            "objective": "Research and present traditions from at least two different countries.",
            "tasks": [
                "Choose two countries and list three traditions from each.",
                "Create a Venn diagram comparing the traditions of the two countries.",
                "Write five sentences using 'In (country), people usually...' structures.",
                "Teach a classmate one interesting fact about a tradition they didn't know."
            ],
            "reward": "Culture Connector badge + 100 XP"
        },
        3: {
            "title": "Mission: Future Me",
            "objective": "Explore career options and plan your steps toward a dream job.",
            "tasks": [
                "Research three different careers and list the skills each one needs.",
                "Write a letter to your future self describing the job you want.",
                "Create a career roadmap poster showing steps from school to your dream job.",
                "Present your dream career to a partner in a 2-minute talk."
            ],
            "reward": "Career Pathfinder badge + 100 XP"
        },
        4: {
            "title": "Mission: Truth Seeker",
            "objective": "Become a fact-checking expert by analysing news articles and media content.",
            "tasks": [
                "Find one real news article and one fake one — explain the differences.",
                "Create a 'How to Spot Fake News' infographic with five tips.",
                "Analyse an advertisement and identify the persuasion techniques used.",
                "Quiz a classmate on media literacy vocabulary (at least 8 words)."
            ],
            "reward": "Media Detective badge + 100 XP"
        },
        5: {
            "title": "Mission: Wellness Week",
            "objective": "Track and improve your health habits over one week.",
            "tasks": [
                "Keep a health diary for five days: record meals, exercise, and sleep.",
                "Design a healthy meal plan for one day (breakfast, lunch, dinner, snacks).",
                "Do a 10-minute exercise routine and teach it to a classmate.",
                "Write five tips for managing stress and share them on a class poster."
            ],
            "reward": "Wellness Warrior badge + 100 XP"
        },
        6: {
            "title": "Mission: Star Gazer",
            "objective": "Become a space expert by researching the solar system and beyond.",
            "tasks": [
                "Create a fact card for each of the eight planets in our solar system.",
                "Write a diary entry as an astronaut spending a day on the ISS.",
                "Build a simple model of the solar system from recycled materials.",
                "Present three 'mind-blowing space facts' to the class."
            ],
            "reward": "Space Voyager badge + 100 XP"
        },
        7: {
            "title": "Mission: Welcome Committee",
            "objective": "Create resources to help newcomers feel welcome at your school.",
            "tasks": [
                "Write a welcome letter in English for a new student arriving from another country.",
                "Create a 'Survival Guide' for your school: key places, rules, and tips.",
                "Role-play a situation where you help a new student on their first day.",
                "Design a multilingual welcome poster with greetings in at least five languages."
            ],
            "reward": "Empathy Ambassador badge + 100 XP"
        },
        8: {
            "title": "Mission: Film Buff",
            "objective": "Explore the world of cinema by reviewing, creating, and discussing films.",
            "tasks": [
                "Watch a short film and write a review with title, summary, opinion, and rating.",
                "Create a movie poster for an imaginary film with a title, tagline, and image.",
                "Write a short dialogue (10 lines) for a scene in your imaginary film.",
                "Debate with a partner: 'Are animated films only for children?' — argue your position."
            ],
            "reward": "Film Critic badge + 100 XP"
        },
        9: {
            "title": "Mission: Digital Guardian",
            "objective": "Demonstrate responsible digital citizenship through practical tasks.",
            "tasks": [
                "Create a 'Digital Safety Rules' poster with at least six rules.",
                "Design a concept for an educational app — draw the screens and explain features.",
                "Write a short story (60-80 words) about a world where AI does everything.",
                "Present the pros and cons of social media in a 2-minute class talk."
            ],
            "reward": "Digital Citizen badge + 100 XP"
        },
        10: {
            "title": "Mission: Rights Champion",
            "objective": "Advocate for human rights through creative and persuasive projects.",
            "tasks": [
                "Choose a human right and write a persuasive paragraph explaining its importance.",
                "Design a campaign poster with a powerful slogan and illustration.",
                "Research a real person who fought for human rights and present their story.",
                "Write a class petition for a cause you believe in and collect signatures."
            ],
            "reward": "Rights Defender badge + 100 XP"
        }
    }
}

FAMILY_CORNER_BANK = {
    7: {
        1: {
            "title": "Discovering Your Child's Identity",
            "parent_tip": "Encourage your child to talk about their strengths, interests, and values. Ask open-ended questions like 'What do you enjoy most about yourself?' rather than yes/no questions.",
            "home_activity": "Create a family 'identity board' together. Each family member writes five words that describe themselves and shares why those words are important.",
            "conversation_starter": "What are three things that make you proud of who you are?"
        },
        2: {
            "title": "Sharing Family Traditions",
            "parent_tip": "Talk to your child about your family's traditions and their origins. Children at this age are curious about culture, and sharing stories from your own childhood makes learning personal and meaningful.",
            "home_activity": "Cook a traditional family recipe together and discuss its history. Ask your child to write the recipe in English and describe why it is special.",
            "conversation_starter": "What is your favourite family tradition, and what would you like to pass on to your own children one day?"
        },
        3: {
            "title": "Talking About the Future",
            "parent_tip": "Ask about your child's career interests without judgment. At 12-13, they are starting to think about the future. Support exploration rather than pushing specific paths.",
            "home_activity": "Together, research a career your child is interested in. Find out what education is needed, what a typical day looks like, and what skills are important.",
            "conversation_starter": "If you could spend a day doing any job in the world, what would you choose and why?"
        },
        4: {
            "title": "Media Literacy at Home",
            "parent_tip": "Discuss news stories with your child regularly. Ask them where they get their information and whether they check if it is true. Model critical thinking by questioning sources yourself.",
            "home_activity": "Find a news story together online. Check it against two other sources. Discuss whether the story seems reliable and how you can tell.",
            "conversation_starter": "Have you ever seen something online that turned out to be false? How did you find out?"
        },
        5: {
            "title": "Building Healthy Habits Together",
            "parent_tip": "Be a role model for healthy living. Children are more likely to eat well, exercise, and manage stress if they see their parents doing the same.",
            "home_activity": "Plan a 'family health week' where everyone tracks their water intake, sleep hours, and physical activity. Compare results at the end of the week.",
            "conversation_starter": "What is one healthy habit you would like our family to start this month?"
        },
        6: {
            "title": "Exploring Space Together",
            "parent_tip": "Your child is learning about the universe at school. Show interest by watching a space documentary together or visiting a planetarium. Curiosity about space often sparks broader scientific thinking.",
            "home_activity": "On a clear night, go outside and try to identify constellations or planets. Use a free stargazing app to help. Talk about what your child has learned in class.",
            "conversation_starter": "If you could travel anywhere in space, where would you go and what would you hope to discover?"
        },
        7: {
            "title": "Understanding Migration",
            "parent_tip": "Talk to your child about empathy and what it feels like to be new somewhere. If your family has a migration story, share it. This helps children understand migration is a human experience, not just a news topic.",
            "home_activity": "Watch a short documentary or read a story about migration together. Discuss how the people in the story might have felt and what helped them.",
            "conversation_starter": "How would you feel if you had to move to a completely new country where you didn't speak the language?"
        },
        8: {
            "title": "Family Film Night",
            "parent_tip": "Watch a film together and discuss it afterwards. Ask your child about the characters, the message, and their favourite scenes. This builds analytical thinking and vocabulary.",
            "home_activity": "After watching a film together, each family member writes a short review (3-4 sentences) and shares their star rating. Compare opinions!",
            "conversation_starter": "What was the last film that made you think differently about something? What was the message?"
        },
        9: {
            "title": "Digital Safety at Home",
            "parent_tip": "Have regular conversations about online safety. Know which apps and websites your child uses. Set clear rules about screen time and privacy together, explaining the reasons behind each rule.",
            "home_activity": "Review your family's digital habits together. Create a 'Family Digital Agreement' with rules everyone follows — parents included!",
            "conversation_starter": "What would you do if someone you don't know sent you a message online asking for personal information?"
        },
        10: {
            "title": "Rights Begin at Home",
            "parent_tip": "Discuss human rights in an age-appropriate way. Children at 12-13 are developing a strong sense of fairness. Encourage them to think about equality and justice in everyday situations.",
            "home_activity": "Read the simplified version of the UN Convention on the Rights of the Child together. Choose three rights and discuss how they apply to your child's life.",
            "conversation_starter": "If you could change one thing to make the world fairer for children, what would it be?"
        }
    }
}

SEL_BANK = {
    7: {
        1: {
            "title": "Understanding My Emotions",
            "skill": "Self-awareness",
            "scenario": "Elif is about to present her identity collage to the class. She notices her heart is beating fast and her hands are shaking. She feels nervous because she is worried that people might not like her presentation.",
            "reflection_questions": [
                "Can you name a time when you felt nervous like Elif? What caused that feeling?",
                "What physical signs does your body give you when you are anxious?",
                "How can recognising your emotions help you deal with them better?"
            ],
            "activity": "Emotion mapping: Draw an outline of a body and mark where you feel different emotions (butterflies in stomach for nervousness, tight chest for anxiety, warm face for embarrassment). Share with a partner."
        },
        2: {
            "title": "Respecting Differences",
            "skill": "Social awareness",
            "scenario": "Carlos brings tamales to the culture fair, but a classmate laughs and says the food looks 'weird.' Carlos feels hurt and embarrassed. He worked hard to prepare the dish with his grandmother.",
            "reflection_questions": [
                "How do you think Carlos felt when his classmate laughed? Why?",
                "Have you ever felt judged for something from your culture? How did it make you feel?",
                "What could you say to someone who makes fun of another person's tradition?"
            ],
            "activity": "Role-play in pairs: One person shares something from their culture while the other practises active listening and asking respectful questions. Then switch roles."
        },
        3: {
            "title": "Dealing with Uncertainty",
            "skill": "Self-management",
            "scenario": "Kwame is confused about his future career. His father wants him to be a doctor, but Kwame loves engineering and football. He feels pressured and doesn't know how to tell his father about his true interests.",
            "reflection_questions": [
                "Is it okay to feel unsure about your future at age 12-13? Why?",
                "How can you communicate your feelings to someone who has different expectations?",
                "What is one step Kwame could take to explore his interests while still respecting his father?"
            ],
            "activity": "Write a letter (not to send) to someone who has expectations of you. Express how you feel honestly. Then write what you wish they would say back."
        },
        4: {
            "title": "Thinking Before Sharing",
            "skill": "Responsible decision-making",
            "scenario": "Mei sees a shocking post on social media claiming that their school is closing down. She wants to share it immediately because it seems urgent. But then she remembers what Mr. Demir taught about fake news and decides to check the facts first.",
            "reflection_questions": [
                "Why is it important to think before sharing information online?",
                "What could happen if Mei had shared the false news without checking?",
                "Can you think of a time when pausing before acting saved you from a mistake?"
            ],
            "activity": "Create a personal 'STOP-THINK-CHECK-SHARE' card. Decorate it and keep it near your device as a reminder to always verify before sharing."
        },
        5: {
            "title": "Asking for Help",
            "skill": "Self-management",
            "scenario": "Carlos has been feeling tired and stressed lately because he stays up late watching videos and skips breakfast every morning. He knows his habits are unhealthy, but he finds it hard to change. He feels embarrassed to ask for help.",
            "reflection_questions": [
                "Why do you think Carlos feels embarrassed about asking for help?",
                "Is asking for help a sign of weakness or strength? Why?",
                "Who are three trusted people you could talk to if you needed help with your wellbeing?"
            ],
            "activity": "Draw a 'support circle' with yourself in the middle and the people you can turn to around you (friends, family, teacher, counsellor). Write one way each person could help you."
        },
        6: {
            "title": "Embracing Curiosity",
            "skill": "Self-awareness",
            "scenario": "Mei is fascinated by black holes but feels shy about asking questions in class because she thinks her questions might sound silly. She worries that other students will think she is strange for being so interested in space.",
            "reflection_questions": [
                "Why might someone feel shy about asking questions in class?",
                "How does curiosity help us learn and grow?",
                "What would you say to encourage Mei to ask her questions?"
            ],
            "activity": "Write three questions about any topic you are curious about. Share them in a small group. Notice: there are no silly questions! Vote on the most interesting question in your group."
        },
        7: {
            "title": "Walking in Someone Else's Shoes",
            "skill": "Social awareness / Empathy",
            "scenario": "A new student named Yara joins the class from another country. She speaks very little English and sits alone at lunch. Some students ignore her, but Elif remembers how scared she felt on her first day at a new summer camp.",
            "reflection_questions": [
                "How do you think Yara feels on her first day at a new school?",
                "What emotions might someone experience when they move to a new country?",
                "What are three simple things you could do to make a newcomer feel welcome?"
            ],
            "activity": "Empathy journal entry: Write a short paragraph from Yara's perspective describing her first day. Try to include her thoughts, feelings, and hopes."
        },
        8: {
            "title": "Handling Disagreements",
            "skill": "Relationship skills",
            "scenario": "Kwame and Carlos disagree about their group film project. Kwame wants to make an action film, but Carlos wants a comedy. They start arguing and Mei and Elif feel uncomfortable. The project is due in three days.",
            "reflection_questions": [
                "What could Kwame and Carlos do to resolve their disagreement?",
                "How can you disagree with someone while still showing respect?",
                "What role can Mei and Elif play as mediators in this situation?"
            ],
            "activity": "In groups of four, role-play the scenario. Try three different endings: 1) one person gives in, 2) they compromise, 3) they find a creative new idea. Discuss which ending felt best."
        },
        9: {
            "title": "Balancing Screen Time and Real Life",
            "skill": "Self-management",
            "scenario": "Kwame realises he has spent four hours on his phone after school every day this week. He missed football practice, didn't finish his homework, and even forgot to call his grandmother on her birthday. He feels guilty but doesn't know how to change.",
            "reflection_questions": [
                "How does too much screen time affect other parts of your life?",
                "What strategies could Kwame use to reduce his screen time?",
                "What activities could you replace some screen time with?"
            ],
            "activity": "Create a 'Weekly Balance Plan' with columns for: screen time, physical activity, family time, study time, and free time. Fill it in for one week and check your balance."
        },
        10: {
            "title": "Standing Up for What's Right",
            "skill": "Responsible decision-making",
            "scenario": "Elif sees an older student bullying a younger child in the playground, calling them names and pushing them. Some students watch but do nothing. Elif feels scared to get involved, but she knows it's wrong.",
            "reflection_questions": [
                "What would you do if you witnessed bullying? Why?",
                "Why is it sometimes difficult to stand up for others?",
                "How can one person's action inspire others to do the right thing?"
            ],
            "activity": "Create a class 'Stand Up Charter' with five commitments everyone agrees to follow. Examples: 'We will not be bystanders.' 'We will report bullying to a trusted adult.' Display it in the classroom."
        }
    }
}

STEAM_BANK = {
    7: {
        1: {
            "title": "Identity Infographic",
            "subject_link": "Art + Technology + Maths",
            "activity": "Create a digital or hand-drawn infographic about your class. Survey classmates about their hobbies, favourite subjects, and personality traits. Present the data in charts and graphs.",
            "materials": ["survey template", "graph paper or digital tool", "coloured markers", "ruler"],
            "steps": [
                "Design a survey with five questions about identity (hobbies, traits, favourites).",
                "Collect responses from at least ten classmates.",
                "Organise the data into categories and count the results.",
                "Create bar charts or pie charts to show the results visually.",
                "Add illustrations and present your infographic to the class."
            ],
            "learning_outcome": "Students apply data collection, mathematical representation, and design skills to explore personal identity."
        },
        2: {
            "title": "Cultural Pattern Art",
            "subject_link": "Art + Maths + Social Studies",
            "activity": "Research geometric patterns from different cultures (Turkish tiles, African kente cloth, Chinese lattice) and create your own pattern using mathematical symmetry.",
            "materials": ["coloured paper", "compass and ruler", "scissors", "glue"],
            "steps": [
                "Research two cultural patterns from different countries online or in books.",
                "Identify the geometric shapes and symmetry used in each pattern.",
                "Sketch your own pattern on graph paper using similar principles.",
                "Transfer your design to coloured paper and cut out the shapes.",
                "Assemble your pattern and write a paragraph explaining the cultural connection."
            ],
            "learning_outcome": "Students connect mathematical concepts of symmetry and geometry to cultural artistic traditions."
        },
        3: {
            "title": "Build a Career Quiz App",
            "subject_link": "Technology + Logic + English",
            "activity": "Design a simple career quiz on paper or using a free tool. Users answer questions about their skills and interests, and the quiz suggests a career match.",
            "materials": ["paper and pencils", "career research notes", "optional: Scratch or Google Forms", "coloured markers"],
            "steps": [
                "List ten different careers and the key skills each one needs.",
                "Write eight quiz questions like 'Do you enjoy working with numbers?'",
                "Create a scoring system that links answers to career categories.",
                "Design the quiz layout with clear instructions and options.",
                "Test your quiz with classmates and discuss the results."
            ],
            "learning_outcome": "Students apply logical thinking, decision-tree design, and career vocabulary in a creative project."
        },
        4: {
            "title": "Fake News Detection Experiment",
            "subject_link": "Science + Media Studies + Critical Thinking",
            "activity": "Conduct an experiment to test how easily people believe fake headlines. Show classmates a mix of real and fake headlines and record their ability to identify which is which.",
            "materials": ["printed headline cards (mix of real and fake)", "recording sheet", "timer", "graph paper for results"],
            "steps": [
                "Collect five real news headlines and create five fake but realistic headlines.",
                "Mix them together and number each headline 1-10.",
                "Ask at least ten classmates to identify each headline as real or fake.",
                "Record the results and calculate the percentage of correct answers.",
                "Present your findings in a graph and discuss what made fake headlines convincing."
            ],
            "learning_outcome": "Students apply the scientific method to media literacy, collecting and analysing data about information credibility."
        },
        5: {
            "title": "Heart Rate Investigation",
            "subject_link": "Science + Maths + PE",
            "activity": "Investigate how different types of physical activity affect heart rate. Measure pulse before and after various exercises and create data displays.",
            "materials": ["stopwatch or phone timer", "recording sheet", "graph paper", "coloured pencils"],
            "steps": [
                "Learn how to measure your pulse (count beats for 15 seconds, multiply by 4).",
                "Record your resting heart rate.",
                "Do three different activities: walking, jogging, and star jumps (1 minute each).",
                "Measure and record your heart rate after each activity.",
                "Create a line graph showing how your heart rate changed and write a conclusion."
            ],
            "learning_outcome": "Students connect physical education with biology and mathematics through data collection and analysis."
        },
        6: {
            "title": "Build a Constellation Viewer",
            "subject_link": "Science + Engineering + Art",
            "activity": "Build a simple constellation viewer using a cardboard tube and black paper. Poke holes in the paper to create star patterns of real constellations.",
            "materials": ["cardboard tube (paper towel roll)", "black paper", "pin or needle", "torch/flashlight"],
            "steps": [
                "Research three constellations and sketch their star patterns.",
                "Cut circles of black paper to fit the end of the cardboard tube.",
                "Poke holes in each paper circle matching a constellation pattern.",
                "Attach a paper circle to one end of the tube with tape.",
                "Look through the tube toward a light source — or shine a torch through it in a dark room to project stars on the wall."
            ],
            "learning_outcome": "Students combine astronomy knowledge with engineering and hands-on construction skills."
        },
        7: {
            "title": "Migration Map Visualisation",
            "subject_link": "Geography + Maths + Art",
            "activity": "Create a visual migration map showing movement of people around the world. Use colour-coded arrows and data to show major migration routes.",
            "materials": ["large world map printout", "coloured string or markers", "data sheet with migration statistics", "pins or tape"],
            "steps": [
                "Research three major migration routes in the world (past or present).",
                "Mark the origin and destination countries on your map.",
                "Draw colour-coded arrows showing the direction of migration.",
                "Add data labels showing approximate numbers of migrants.",
                "Present your map and explain the reasons behind each migration route."
            ],
            "learning_outcome": "Students integrate geography, data visualisation, and social studies to understand global migration patterns."
        },
        8: {
            "title": "Foley Sound Effects Workshop",
            "subject_link": "Science + Art + Technology",
            "activity": "Learn how sound effects (Foley) are created for films. Experiment with everyday objects to recreate common movie sounds.",
            "materials": ["various household objects (rice, cellophane, coconut shells, etc.)", "recording device (phone)", "film clip without sound", "notebook"],
            "steps": [
                "Watch a short film clip with the sound turned off.",
                "List five sounds that should be in the clip (footsteps, rain, doors, etc.).",
                "Experiment with everyday objects to recreate each sound.",
                "Record your sound effects using a phone or device.",
                "Play your sounds alongside the film clip and evaluate how realistic they are."
            ],
            "learning_outcome": "Students explore sound science and creative problem-solving while learning about the filmmaking process."
        },
        9: {
            "title": "Simple Chatbot Design",
            "subject_link": "Technology + Logic + English",
            "activity": "Design a simple chatbot on paper using a decision-tree flowchart. The chatbot should be able to have a basic conversation and answer questions about your school.",
            "materials": ["large paper", "markers", "ruler", "sticky notes for edits"],
            "steps": [
                "Write a greeting message for your chatbot.",
                "Think of five common questions someone might ask about your school.",
                "Create a flowchart: for each question, draw boxes with the chatbot's response.",
                "Add 'if-then' branches for follow-up questions.",
                "Test your chatbot with a partner: one person asks questions, the other follows the flowchart to answer."
            ],
            "learning_outcome": "Students develop computational thinking, logic design, and English communication skills through chatbot prototyping."
        },
        10: {
            "title": "Rights Through Data",
            "subject_link": "Maths + Social Studies + Art",
            "activity": "Research data about children's rights worldwide (school enrolment, child labour, healthcare access) and create informative data posters.",
            "materials": ["printed statistics from UNICEF or similar sources", "poster paper", "coloured markers", "ruler"],
            "steps": [
                "Choose one children's right to investigate (education, healthcare, or protection).",
                "Find statistics from at least three different countries.",
                "Create comparison charts or infographics showing the data.",
                "Add a section explaining what the data means and why it matters.",
                "Present your poster and suggest one action people can take to help."
            ],
            "learning_outcome": "Students use mathematical data representation to understand and communicate about global human rights issues."
        }
    }
}

PODCAST_BANK = {
    7: {
        1: {
            "title": "What Makes You, YOU?",
            "description": "Elif and Kwame discuss what personal identity means, how people express themselves, and why being unique is a strength.",
            "script": "Elif: Welcome to our podcast! I'm Elif. Kwame: And I'm Kwame. Today we're talking about personal identity. Elif: So, what does identity mean to you? Kwame: I think it's everything that makes you who you are — your name, your culture, your hobbies, your values. Elif: That's a great definition. For me, being creative is a huge part of my identity. I love drawing and writing. Kwame: And for me, it's football and my Ghanaian roots. But identity isn't just about hobbies, is it? Elif: No, it's also about your personality. Am I kind? Am I honest? Those things matter too. Kwame: Exactly. And the cool thing is, your identity can grow and change as you get older. Elif: So the big message is: be proud of who you are! Kwame: And never be afraid to be yourself. Thanks for listening, everyone!",
            "discussion_questions": [
                "What three words would you use to describe your identity?",
                "How has your identity changed since you were younger?",
                "Why is it important to respect other people's identities?"
            ],
            "vocabulary": ["identity", "personality", "unique", "values", "roots"]
        },
        2: {
            "title": "Traditions That Connect Us",
            "description": "Mei and Carlos explore how traditions bring people together and share customs from their own cultures.",
            "script": "Mei: Hi everyone! Welcome to today's episode. I'm Mei. Carlos: And I'm Carlos. Today we're exploring traditions and customs from around the world. Mei: Carlos, what's your favourite tradition from Mexico? Carlos: Definitely Dia de los Muertos. We remember our loved ones with colourful altars, flowers, and special bread. What about you, Mei? Mei: In China, I love the Mid-Autumn Festival. We eat mooncakes and watch the full moon with our family. Carlos: That sounds beautiful. I think traditions are important because they connect us to our past. Mei: And to our families. Even if you move to a new country, you can keep your traditions alive. Carlos: That's a great point. Traditions are like bridges between generations. Mei: And between cultures too. When we share our traditions, we learn to appreciate each other. Carlos: So tell us, listeners — what's a tradition you'd like to share with the world?",
            "discussion_questions": [
                "What is one tradition from your family that you would explain to a foreign visitor?",
                "How do traditions connect people across generations?",
                "What would happen if all traditions disappeared?"
            ],
            "vocabulary": ["tradition", "custom", "generation", "celebrate", "heritage"]
        },
        3: {
            "title": "Dream Jobs and Real Skills",
            "description": "The group discusses career goals and what skills you need to develop now to reach them.",
            "script": "Elif: Welcome back! Today, we're talking about careers. What do you want to be when you grow up? Kwame: I used to say only footballer, but now I'm interested in engineering too. Carlos: For me, it's still music. But I know I need to study hard to make it work. Mei: I want to be a scientist. I love experiments and asking questions. Elif: I'm thinking about journalism. I love writing and finding out the truth. Kwame: The interesting thing is, all our dream jobs need different skills. Mei: Yes! A scientist needs critical thinking. A journalist needs good communication. Carlos: A musician needs creativity and practice. An engineer needs maths and problem-solving. Elif: So the message is: discover what you love, and then work on the skills you need. Kwame: And don't be afraid to change your mind. Your dream job at twelve doesn't have to be your job at thirty!",
            "discussion_questions": [
                "What skills do you already have that could help in your dream career?",
                "Do you think it is okay to change your career goal? Why?",
                "What is one new skill you would like to learn this year?"
            ],
            "vocabulary": ["career", "skill", "qualification", "creative", "communicate"]
        },
        4: {
            "title": "Is Seeing Believing?",
            "description": "Elif and Mei discuss how to evaluate information in the digital age and why media literacy is essential.",
            "script": "Elif: Today's topic is media literacy. Mei, have you ever believed something online that turned out to be false? Mei: Yes! I once read that goldfish have a three-second memory. I told everyone. Then I found out it's completely untrue. Elif: That happens to all of us. The internet has amazing information, but also a lot of rubbish. Mei: So how do we know what to trust? Elif: Mr. Demir taught us three steps: check the source, check the author, check the date. Mei: And look for the same information on at least two other websites. Elif: Exactly. If only one website says it, be suspicious. Mei: What about advertisements? They can be misleading too. Elif: Right. Ads are designed to sell, not to inform. Always ask: what are they trying to make me feel or buy? Mei: The bottom line is: think before you click, and definitely think before you share. Elif: Well said. Stay smart, stay curious, listeners!",
            "discussion_questions": [
                "Have you ever shared something online that turned out to be false?",
                "What are the three steps to check if information is reliable?",
                "Why do you think fake news spreads so quickly on social media?"
            ],
            "vocabulary": ["reliable", "source", "misleading", "verify", "critical thinking"]
        },
        5: {
            "title": "Mind, Body, Balance",
            "description": "Carlos and Kwame discuss teenage health, the importance of sleep, nutrition, exercise, and mental wellbeing.",
            "script": "Carlos: Hey listeners! Today we're talking about health and wellbeing. Kwame, what does being healthy mean to you? Kwame: It's not just about being fit physically. It's also about feeling good mentally. Carlos: I agree. I used to skip breakfast every day and I was always tired at school. Kwame: What changed? Carlos: Our school nurse explained that your brain needs fuel in the morning. So I started eating a proper breakfast. Kwame: And did it make a difference? Carlos: Huge difference! I had more energy and could concentrate better. Kwame: Sleep is another big one. Teenagers need eight to ten hours, but most of us don't get that. Carlos: Because of phones and screens before bed. Kwame: Exactly. And let's not forget exercise. Even thirty minutes of walking or playing a sport helps. Carlos: And if you're feeling stressed or sad, talk to someone. There's no shame in asking for help. Kwame: Great advice. Take care of your body and your mind, listeners!",
            "discussion_questions": [
                "How many hours of sleep do you usually get? Is it enough?",
                "What healthy change could you make this week?",
                "Why is mental health just as important as physical health?"
            ],
            "vocabulary": ["nutrition", "wellbeing", "concentrate", "mental health", "balanced"]
        },
        6: {
            "title": "Counting Stars and Asking Questions",
            "description": "Mei and Elif explore fascinating facts about space and discuss why space exploration matters.",
            "script": "Mei: Welcome to our space episode! I'm so excited about this one. Elif: Me too! Mei, what's the most amazing space fact you know? Mei: There are more stars in the universe than grains of sand on all of Earth's beaches. Elif: That's mind-blowing! Here's mine: a day on Venus is longer than a year on Venus. Mei: Wait, what? How is that possible? Elif: Venus rotates so slowly that it takes longer to spin once than to go around the Sun. Mei: Space is full of surprises. Did you know that astronauts on the ISS see sixteen sunrises every day? Elif: Incredible. So, why does space exploration matter? Mei: Because it teaches us about our own planet. Satellites help us predict weather and study climate change. Elif: And it inspires us to dream bigger. Maybe one of our listeners will be the first person on Mars! Mei: That would be amazing. Keep looking up at the stars, everyone!",
            "discussion_questions": [
                "What is the most surprising space fact you have learned?",
                "Why should countries invest money in space exploration?",
                "Would you volunteer for a one-way trip to Mars? Why or why not?"
            ],
            "vocabulary": ["universe", "satellite", "orbit", "exploration", "astronaut"]
        },
        7: {
            "title": "Home Is Where the Heart Is",
            "description": "Kwame and Carlos discuss what it means to move to a new place and how small acts of kindness can change lives.",
            "script": "Kwame: Today we're talking about migration — moving to a new country or city. Carlos: It's a topic close to many people's hearts. Kwame, has anyone in your family migrated? Kwame: Yes, my uncle moved to the UK for work. He said the first year was the hardest. Carlos: What was difficult? Kwame: Everything — the language, the food, missing home. But he said the kindness of his neighbours made all the difference. Carlos: That's powerful. I think when someone is new, even a simple hello can mean the world. Kwame: We had a guest speaker, Ahmet, who moved from Turkey to Germany as a child. One classmate invited him to play football, and it changed everything. Carlos: It shows that you don't need to do something big. Small actions matter. Kwame: If you see a new student at your school, say hello. Invite them to sit with you. Carlos: Be the reason someone feels they belong. Kwame: Beautifully said, Carlos. Thanks for listening, everyone!",
            "discussion_questions": [
                "What is one thing you could do to help a newcomer at your school?",
                "Why is belonging important for a person's happiness?",
                "What can communities do to be more welcoming to immigrants?"
            ],
            "vocabulary": ["migration", "immigrant", "belong", "adapt", "community"]
        },
        8: {
            "title": "Behind the Scenes",
            "description": "Elif and Carlos talk about how films are made, their favourite genres, and why cinema is a powerful art form.",
            "script": "Elif: Lights, camera, podcast! Today we're talking about films and cinema. Carlos, what's your favourite film genre? Carlos: I love comedies because they make me forget my worries. But I also enjoy sci-fi. You? Elif: I'm a big fan of adventure films. The stories take you to amazing places. Carlos: Did you know that making a film involves hundreds of people? Elif: Really? Like who? Carlos: Directors, camera operators, editors, sound designers, costume designers, and many more. Elif: It's like a huge team project. Carlos: Exactly! And every person's role is important. Without good sound, even a great story falls flat. Elif: Our class made a short film last month. We learned that filming is way harder than it looks! Carlos: True! Kwame kept forgetting his lines. But the bloopers were hilarious. Elif: The point is, cinema is a combination of art, technology, and teamwork. Carlos: So next time you watch a film, think about all the people who made it possible. Enjoy the show, listeners!",
            "discussion_questions": [
                "What is your favourite film genre and why?",
                "Which job in filmmaking would you most like to try?",
                "How can films help us understand different cultures and perspectives?"
            ],
            "vocabulary": ["genre", "director", "soundtrack", "script", "animation"]
        },
        9: {
            "title": "Living in a Digital World",
            "description": "Mei and Kwame explore how technology and AI are changing our lives, and how to be responsible digital citizens.",
            "script": "Mei: Welcome to our digital world episode! Kwame, how much time do you spend on screens every day? Kwame: Probably about three hours after school. Is that too much? Mei: The recommended limit is two hours for fun, but most of us go over that. Kwame: True. But we also use technology for school — research, apps, videos. Mei: Right, so it's about balance. What do you think about AI? Kwame: AI is amazing. It can help with homework, translate languages, even create art. Mei: But some people worry it will replace human jobs. Kwame: I think AI is a tool. It can help us, but it can't replace human creativity and emotions. Mei: Good point. We also need to be careful online. Strong passwords, no sharing personal details, and being kind. Kwame: Cyberbullying is a serious problem. If you see it, report it. Mei: And remember, the person behind every screen is a real human being. Treat them with respect. Kwame: The digital world is our world. Let's make it a good one!",
            "discussion_questions": [
                "How much screen time do you have per day? Do you think it's balanced?",
                "What is one positive and one negative thing about AI?",
                "What rules should everyone follow to be a good digital citizen?"
            ],
            "vocabulary": ["artificial intelligence", "cyberbullying", "digital citizen", "privacy", "algorithm"]
        },
        10: {
            "title": "Rights, Respect, and Responsibility",
            "description": "All four friends discuss human rights, why they matter, and what young people can do to make a difference.",
            "script": "Elif: This is our final episode, and it's about something really important — human rights. Kwame: Every person is born with rights, no matter who they are or where they come from. Mei: The right to education, healthcare, freedom of expression, and protection from harm. Carlos: But sadly, not everyone enjoys these rights equally. Elif: That's why it's important to speak up. If you see injustice, don't stay silent. Kwame: Even small actions count. You can write a letter, make a poster, or simply be kind to someone in need. Mei: Turkey celebrates Children's Day on April 23rd. Ataturk believed children are the future. Carlos: And the UN Convention on the Rights of the Child says every child has the right to be heard. Elif: So use your voice! Whether it's at school, at home, or online. Kwame: And remember, with rights come responsibilities. Respect others' rights too. Mei: Thank you for listening to our podcast series. Carlos: Go out there and make the world a better place. All: Goodbye!",
            "discussion_questions": [
                "Which human right do you think is most important and why?",
                "What is one thing young people can do to stand up for human rights?",
                "How are rights and responsibilities connected?"
            ],
            "vocabulary": ["human rights", "justice", "equality", "responsibility", "convention"]
        }
    }
}

# ==============================================================================
# ESCAPE ROOM BANK - Grade 7 (Ages 12-13 / A2+ CEFR)
# ==============================================================================

ESCAPE_ROOM_BANK = {
    7: {
        1: {
            "title": "The Mirror Maze",
            "story": "You are trapped in a funhouse mirror maze! Each mirror shows a distorted reflection. To find the exit, you must solve puzzles about appearance and personality. Only someone who truly understands people can escape!",
            "puzzles": [
                {"type": "vocabulary", "question": "What adjective describes someone who is friendly, warm, and easy to talk to?", "answer": "outgoing", "hint": "The opposite of shy."},
                {"type": "grammar", "question": "Choose: 'She is ___ than her sister.' (tall/taller/tallest)", "answer": "taller", "hint": "Comparing two people uses the comparative form."},
                {"type": "reading", "question": "Read: 'Jake is tall with curly brown hair. He is very generous and always shares his things. His friends say he is reliable because he never breaks a promise.' What personality trait means Jake keeps his promises?", "answer": "reliable", "hint": "Look at the last sentence."},
                {"type": "maths", "question": "In a class of 30 students, 40% have brown eyes. How many students have brown eyes?", "answer": "12", "hint": "30 × 0.40 = ?"},
                {"type": "riddle", "question": "I can be curly, straight, long, or short. I grow on your head. You wash me with shampoo. What am I?", "answer": "hair", "hint": "People style me differently every day."}
            ],
            "final_code": "MIRROR7",
            "reward": "You escaped the mirror maze! +40 XP! Badge: Identity Expert"
        },
        2: {
            "title": "The Championship Locker Room",
            "story": "The championship game starts in 10 minutes, but the locker room is locked! The coach left puzzles about sports for the team to solve. Answer them all to unlock the door, grab your gear, and win the game!",
            "puzzles": [
                {"type": "vocabulary", "question": "What do you call the person who leads and trains a sports team?", "answer": "coach", "hint": "This person creates the game strategy and motivates players."},
                {"type": "grammar", "question": "Fill in: 'He ___ football every Saturday since he was five.' (plays/has played/played)", "answer": "has played", "hint": "The action started in the past and continues — use present perfect."},
                {"type": "reading", "question": "Read: 'Basketball was invented by James Naismith in 1891. He was a Canadian physical education teacher. He created the game to keep students active during winter.' Why did Naismith invent basketball?", "answer": "to keep students active during winter", "hint": "The reason is in the last sentence."},
                {"type": "maths", "question": "A football match has two 45-minute halves. There is a 15-minute break. How long is the total match time including the break?", "answer": "105", "hint": "45 + 45 + 15 = ?"},
                {"type": "riddle", "question": "I have a net but catch no fish. I have a court but no judge. People bounce a ball and try to score through me. What am I?", "answer": "a basketball hoop", "hint": "Think about a sport played on a court."}
            ],
            "final_code": "GOAL777",
            "reward": "Game time! You won the championship! +40 XP! Badge: Sports Champion"
        },
        3: {
            "title": "The Time Capsule Vault",
            "story": "A 100-year-old time capsule has been found under your school! It is locked with a code that requires knowledge about famous people from history. Solve the biography puzzles to open the capsule and see what is inside!",
            "puzzles": [
                {"type": "vocabulary", "question": "What is the written story of a person's life called?", "answer": "biography", "hint": "Auto-___ means you write it about yourself."},
                {"type": "grammar", "question": "Choose: 'Mozart ___ his first symphony when he was eight years old.' (composed/has composed/composes)", "answer": "composed", "hint": "This happened at a specific time in the past — use simple past."},
                {"type": "reading", "question": "Read: 'Frida Kahlo was a Mexican artist born in 1907. She is famous for her self-portraits. She had a difficult life but used art to express her feelings and pain.' What is Frida Kahlo famous for?", "answer": "her self-portraits", "hint": "Look at the second sentence."},
                {"type": "maths", "question": "A famous scientist was born in 1643 and lived for 84 years. In what year did he die?", "answer": "1727", "hint": "1643 + 84 = ? (This is Isaac Newton!)"},
                {"type": "riddle", "question": "I was deaf but composed the most beautiful music in history. My 9th Symphony is world-famous. Who am I?", "answer": "Beethoven", "hint": "A German composer from the Classical era."}
            ],
            "final_code": "PAST100",
            "reward": "The time capsule is open! +40 XP! Badge: History Detective"
        },
        4: {
            "title": "The Safari Rescue",
            "story": "A baby elephant is lost in the African savanna! To find and rescue it, you must follow clues about wild animals, their habitats, and survival skills. Every correct answer brings you closer to the elephant!",
            "puzzles": [
                {"type": "vocabulary", "question": "What word describes animals that live in nature, not as pets or on farms?", "answer": "wild", "hint": "Lions, tigers, and wolves are all ___ animals."},
                {"type": "grammar", "question": "Fill in: 'If we ___ the forests, many animals will lose their homes.' (destroy/destroyed/will destroy)", "answer": "destroy", "hint": "First conditional: If + present simple, ... will + base form."},
                {"type": "reading", "question": "Read: 'The Arctic fox changes its fur color with the seasons. In winter, its fur turns white to blend with the snow. In summer, it becomes brown or grey.' Why does the Arctic fox's fur turn white in winter?", "answer": "to blend with the snow", "hint": "Look for the reason after 'to'."},
                {"type": "maths", "question": "A cheetah runs at 120 km/h. A lion runs at 80 km/h. How much faster is the cheetah?", "answer": "40", "hint": "120 - 80 = ?"},
                {"type": "riddle", "question": "I am the largest land animal. I have a trunk and big ears. I never forget. What am I?", "answer": "an elephant", "hint": "You are trying to rescue my baby in this story!"}
            ],
            "final_code": "SAFARI4",
            "reward": "Baby elephant rescued! +40 XP! Badge: Wildlife Protector"
        },
        5: {
            "title": "The TV Studio Blackout",
            "story": "You are visiting a TV studio when suddenly all the lights go out! The backup generator needs a code to restart. Solve television-themed puzzles to restore power and save today's live broadcast!",
            "puzzles": [
                {"type": "vocabulary", "question": "What is a TV show that follows real people in real situations (not actors)?", "answer": "reality show", "hint": "Survivor and Big Brother are examples."},
                {"type": "grammar", "question": "Choose: 'The documentary ___ at 8 PM tonight.' (starts/is starting/started) — scheduled event.", "answer": "starts", "hint": "For schedules and timetables, use present simple."},
                {"type": "reading", "question": "Read: 'A survey asked 200 teenagers about their favourite TV genres. 35% chose comedy, 25% chose action, 20% chose documentary, and 20% chose drama.' Which genre was the most popular?", "answer": "comedy", "hint": "Which percentage is the highest?"},
                {"type": "maths", "question": "A TV series has 6 seasons. Each season has 12 episodes. Each episode is 45 minutes. How many total hours of content is that?", "answer": "54", "hint": "6 × 12 × 45 = 3240 minutes. Divide by 60."},
                {"type": "riddle", "question": "I have a screen but I am not a computer. I have channels but I am not a river. You watch me from your sofa. What am I?", "answer": "a television", "hint": "You use a remote control to operate me."}
            ],
            "final_code": "TV2024",
            "reward": "The studio is back on air! +40 XP! Badge: TV Producer"
        },
        6: {
            "title": "The Party Planner's Panic",
            "story": "You are organizing a surprise birthday party, but the invitation codes are locked! Each puzzle relates to celebrations and traditions around the world. Solve them all to send the invitations before the guest of honor arrives!",
            "puzzles": [
                {"type": "vocabulary", "question": "What is a special meal with lots of food for a celebration called?", "answer": "feast", "hint": "Thanksgiving dinner in the USA is a big ___."},
                {"type": "grammar", "question": "Fill in: 'We ___ a party next Saturday. Everything is planned!' (are having/have/had)", "answer": "are having", "hint": "A planned future event uses present continuous."},
                {"type": "reading", "question": "Read: 'In Japan, people celebrate New Year by eating special noodles called toshikoshi soba. The long noodles represent a long and healthy life.' What do the long noodles represent?", "answer": "a long and healthy life", "hint": "Look at the second sentence."},
                {"type": "maths", "question": "You need 3 balloons per guest. There are 18 guests. Balloons come in packs of 10. How many packs do you need to buy?", "answer": "6", "hint": "18 × 3 = 54 balloons. 54 ÷ 10 = 5.4, so round up."},
                {"type": "riddle", "question": "I am on top of a cake. You light me and then blow me out while making a wish. What am I?", "answer": "a candle", "hint": "One for each year of your life on a birthday cake."}
            ],
            "final_code": "PARTY10",
            "reward": "Surprise! The party is ready! +40 XP! Badge: Celebration Planner"
        },
        7: {
            "title": "The Dream Catcher's Quest",
            "story": "You fall asleep and enter a dream world! To wake up, you must navigate through five dream chambers, each with a puzzle about hopes, dreams, and the future. Only a true dreamer can find the way out!",
            "puzzles": [
                {"type": "vocabulary", "question": "What word means 'a strong desire to achieve something in the future'?", "answer": "ambition", "hint": "Having goals and working hard shows ___."},
                {"type": "grammar", "question": "Choose: 'When I grow up, I ___ be a doctor.' (will/am going to/would) — a prediction.", "answer": "will", "hint": "For general predictions about the future, use this modal."},
                {"type": "reading", "question": "Read: 'Malala Yousafzai dreamed of education for all girls. Despite being attacked, she continued fighting for this dream. In 2014, she became the youngest Nobel Prize winner.' What was Malala's dream?", "answer": "education for all girls", "hint": "It is in the first sentence."},
                {"type": "maths", "question": "If you save 15 dollars every week for your dream trip, how much will you have after 8 weeks?", "answer": "120", "hint": "15 × 8 = ?"},
                {"type": "riddle", "question": "I happen when you sleep. Sometimes I am scary, sometimes wonderful. You forget me when you wake up. What am I?", "answer": "a dream", "hint": "This is the theme of Unit 7!"}
            ],
            "final_code": "DREAM77",
            "reward": "You woke up from the dream! +40 XP! Badge: Dream Chaser"
        },
        8: {
            "title": "The Town Hall Treasure Hunt",
            "story": "The mayor has hidden a golden key somewhere in the town! Each clue is connected to a public building. Visit the library, hospital, post office, and more by solving puzzles to find the golden key!",
            "puzzles": [
                {"type": "vocabulary", "question": "What public building do you go to when you are sick or injured?", "answer": "hospital", "hint": "Doctors and nurses work here."},
                {"type": "grammar", "question": "Fill in: 'You ___ turn left at the traffic lights to reach the library.' (must/mustn't/can't)", "answer": "must", "hint": "This is a necessary direction — an obligation."},
                {"type": "reading", "question": "Read: 'The new community centre has a swimming pool, a gym, a library, and a cafeteria. It is open from 7 AM to 10 PM every day except Sundays.' When is the community centre closed?", "answer": "Sundays", "hint": "Look at the last part: 'except...'."},
                {"type": "maths", "question": "The post office is 800 meters from school. The library is twice as far. How far is the library from school in kilometers?", "answer": "1.6", "hint": "800 × 2 = 1600 meters = ? km."},
                {"type": "riddle", "question": "I have thousands of books but I am not a shop. You can borrow from me but you must return. What am I?", "answer": "a library", "hint": "You need a membership card to borrow books from me."}
            ],
            "final_code": "TOWN888",
            "reward": "You found the golden key! +40 XP! Badge: Town Navigator"
        },
        9: {
            "title": "The Green Planet Mission",
            "story": "Earth is sending a team to save a polluted planet! To power up the spaceship's environmental shield, you must solve puzzles about the environment, pollution, and sustainability. The planet is counting on you!",
            "puzzles": [
                {"type": "vocabulary", "question": "What is the process of converting waste materials into new products called?", "answer": "recycling", "hint": "You put paper, plastic, and glass in separate bins for this."},
                {"type": "grammar", "question": "Choose: 'If everyone ___ less plastic, the oceans will be cleaner.' (uses/used/will use)", "answer": "uses", "hint": "First conditional: If + present simple, ... will..."},
                {"type": "reading", "question": "Read: 'Deforestation destroys about 10 million hectares of forest every year. This causes habitat loss, increases carbon dioxide, and contributes to climate change.' Name one effect of deforestation mentioned in the text.", "answer": "habitat loss", "hint": "Three effects are listed after 'This causes...'."},
                {"type": "maths", "question": "A school recycles 25 kg of paper per week. How many kg will they recycle in one school year (40 weeks)?", "answer": "1000", "hint": "25 × 40 = ?"},
                {"type": "riddle", "question": "I am a layer around the Earth. I protect you from the sun's harmful rays. I have a hole that scientists worry about. What am I?", "answer": "the ozone layer", "hint": "I am in the stratosphere."}
            ],
            "final_code": "GREEN99",
            "reward": "Planet saved! +40 XP! Badge: Eco Warrior"
        },
        10: {
            "title": "The Space Station Lockdown",
            "story": "You are an astronaut on the International Space Station, but a meteor shower has caused a system malfunction! To restore power, you must solve puzzles about planets, space, and the solar system. The countdown has begun!",
            "puzzles": [
                {"type": "vocabulary", "question": "What is the force that keeps planets in orbit around the sun?", "answer": "gravity", "hint": "Isaac Newton discovered this with a falling apple."},
                {"type": "grammar", "question": "Fill in: 'Mars ___ often called the Red Planet.' (is/are/has)", "answer": "is", "hint": "Passive voice: subject + is/are + past participle."},
                {"type": "reading", "question": "Read: 'Jupiter is the largest planet in our solar system. It has at least 95 known moons. The Great Red Spot on Jupiter is a storm that has been raging for over 300 years.' How long has the Great Red Spot existed?", "answer": "over 300 years", "hint": "Look at the last sentence."},
                {"type": "maths", "question": "Light from the Sun takes 8 minutes to reach Earth. How many seconds is that?", "answer": "480", "hint": "8 × 60 = ?"},
                {"type": "riddle", "question": "I have rings but I am not a phone. I am the second largest planet. I am made mostly of gas. What am I?", "answer": "Saturn", "hint": "My rings are made of ice and rock."}
            ],
            "final_code": "SPACE10",
            "reward": "Station restored! +40 XP! Badge: Space Commander"
        }
    }
}
