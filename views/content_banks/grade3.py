# -*- coding: utf-8 -*-
"""Content banks for Grade 3 (Primary Upper / Ages 8-9 / A1 CEFR).

Primary_upper tier sections (19): story, vocabulary, reading, grammar,
listening, writing, pronunciation, dialogue, song, culture, turkey,
project, steam, review, comic, workbook, mission, family, gamification.

Units:
  1  Friends & Feelings      (W1-4)
  2  Our City                (W5-8)
  3  Food Around the World   (W9-12)
  4  Earth & Nature          (W13-16)
  5  Inventions & Technology (W17-20)
  6  Arts & Music            (W21-24)
  7  Space                   (W25-27)
  8  Health & Hygiene        (W28-30)
  9  Legends & Folk Tales    (W31-33)
  10 End of Year Show        (W34-36)
"""

# ---------------------------------------------------------------------------
# 1. STORY CHARACTERS
# ---------------------------------------------------------------------------
STORY_CHARACTERS = {
    3: {
        "main": [
            {"name": "Mia", "age": "9", "desc": "A cheerful girl who loves reading and helping friends.", "emoji": "📚"},
            {"name": "Can", "age": "9", "desc": "A curious boy who enjoys science and building things.", "emoji": "🔧"},
            {"name": "Zehra", "age": "8", "desc": "A creative girl who paints, sings and tells stories.", "emoji": "🎨"},
            {"name": "Leo", "age": "9", "desc": "A sporty boy from London who moved to Turkey last year.", "emoji": "⚽"},
        ],
        "teacher": {"name": "Mr Demir", "desc": "A kind and fun teacher who uses projects and games to teach English."},
    },
}

# ---------------------------------------------------------------------------
# 2. STORY BANK  (10 episodes, 8-10 sentences each)
# ---------------------------------------------------------------------------
STORY_BANK = {
    3: {
        1: {
            "title": "New Friends Day",
            "previously": None,
            "episode": (
                "It was the first day of school. Mia walked into the classroom. "
                "She saw a new boy. 'Hi! I am Mia,' she said. "
                "'Hello! My name is Leo,' said the boy. 'I am from London.' "
                "Can came in with a big smile. 'Welcome, Leo!' he said. "
                "Zehra gave Leo a drawing of the class. 'This is for you!' "
                "Leo felt happy. 'Thank you! You are very kind,' he said. "
                "Mr Demir said, 'Let us be good friends this year.' "
                "They all shook hands and sat together."
            ),
            "cliffhanger": "Will Leo like his new school? Let us find out!",
            "vocab_tie": ["friend", "kind", "happy", "welcome", "together"],
        },
        2: {
            "title": "The City Map",
            "previously": "Leo joined the class and met Mia, Can and Zehra.",
            "episode": (
                "Mr Demir brought a big map of the city. 'Where is the park?' he asked. "
                "Mia pointed. 'It is next to the library!' she said. "
                "Can found the hospital. 'The hospital is behind the school,' he said. "
                "Zehra drew a red line on the map. 'This is the way to my house!' "
                "Leo looked surprised. 'Your city is very big!' he said. "
                "'There is a mosque, a museum and a cinema,' said Mr Demir. "
                "They coloured different buildings on the map. "
                "At the end, they hung the map on the wall."
            ),
            "cliffhanger": "Can Leo find the bakery on the map?",
            "vocab_tie": ["map", "library", "hospital", "museum", "next to"],
        },
        3: {
            "title": "A Taste of the World",
            "previously": "The class explored the city map together.",
            "episode": (
                "It was World Food Day at school. Mr Demir said, 'Bring your favourite food!' "
                "Mia brought baklava. 'This is a Turkish dessert,' she said. "
                "Leo brought fish and chips. 'This is from England!' he smiled. "
                "Can brought rice and chicken. 'My mum makes the best rice!' "
                "Zehra brought fruit salad. 'Fruit is healthy and delicious!' "
                "They put all the food on a big table. 'Let us share!' said Mr Demir. "
                "Everyone tasted a little of everything. "
                "'Food brings people together,' said Mia. Everyone agreed."
            ),
            "cliffhanger": "What food will they cook next time?",
            "vocab_tie": ["food", "delicious", "healthy", "share", "dessert"],
        },
        4: {
            "title": "The Weather Project",
            "previously": "The class had a World Food Day and shared dishes.",
            "episode": (
                "Mr Demir said, 'Let us study the weather this week.' "
                "On Monday it was sunny. 'I love sunny days!' said Can. "
                "On Tuesday it was cloudy. 'Look at the grey clouds,' said Zehra. "
                "On Wednesday it rained. 'We need our umbrellas!' said Mia. "
                "On Thursday it was windy. Leo's hat flew away! "
                "'Catch my hat!' he shouted. Can ran fast and caught it. "
                "On Friday, Mr Demir asked, 'What did you learn?' "
                "'The weather changes every day,' said Mia. 'We must be ready!'"
            ),
            "cliffhanger": "Will they learn about recycling next?",
            "vocab_tie": ["sunny", "cloudy", "rainy", "windy", "weather"],
        },
        5: {
            "title": "The Time Machine Story",
            "previously": "The class tracked the weather for a whole week.",
            "episode": (
                "Can built a model from boxes. 'This is a time machine!' he said. "
                "Zehra laughed. 'Can we go to the past?' she asked. "
                "'In the past, there were no computers,' said Mr Demir. "
                "'People wrote letters with pens,' said Mia. "
                "'There were no phones or tablets,' said Leo. 'How did they talk?' "
                "'They visited each other,' said Can. 'Face to face!' "
                "Mr Demir smiled. 'Technology makes life easier today.' "
                "The class made a poster: Past vs Present."
            ),
            "cliffhanger": "What inventions will they discover next?",
            "vocab_tie": ["invention", "computer", "past", "present", "technology"],
        },
        6: {
            "title": "The School Concert",
            "previously": "The class learned about inventions past and present.",
            "episode": (
                "Mr Demir had exciting news. 'We will have a school concert!' "
                "Zehra wanted to sing. 'I can sing a folk song!' she said. "
                "Can said, 'I can play the drum.' Leo chose the guitar. "
                "Mia wanted to dance. 'I will do a traditional dance!' "
                "They practised every day after school. "
                "Zehra painted the stage decorations too. "
                "'Art and music make us happy,' said Mr Demir. "
                "The children could not wait for the big night."
            ),
            "cliffhanger": "Will the concert go well? Stay tuned!",
            "vocab_tie": ["concert", "sing", "dance", "instrument", "stage"],
        },
        7: {
            "title": "Looking at the Stars",
            "previously": "The class prepared for the school concert.",
            "episode": (
                "Mr Demir took the class to the school garden at night. "
                "'Look up!' he said. 'What do you see?' "
                "'Stars! Thousands of stars!' said Mia. "
                "Can pointed at a bright dot. 'Is that a planet?' "
                "'Yes! That is Jupiter,' said Mr Demir. "
                "Zehra saw the Moon. 'The Moon is so beautiful tonight!' "
                "Leo said, 'In London, I could not see many stars.' "
                "'We are lucky,' said Can. 'The sky is very clear here.'"
            ),
            "cliffhanger": "Will they build a model of the solar system?",
            "vocab_tie": ["star", "planet", "Moon", "sky", "bright"],
        },
        8: {
            "title": "The Health Week",
            "previously": "The class looked at the stars in the school garden.",
            "episode": (
                "It was Health Week at school. A nurse visited the class. "
                "'Wash your hands before every meal,' she said. "
                "Mia asked, 'How many times a day?' 'At least five times!' "
                "Can said, 'I always brush my teeth twice a day.' "
                "The nurse smiled. 'Eat fruit and vegetables too!' "
                "Zehra made a poster about healthy habits. "
                "Leo said, 'I drink eight glasses of water every day.' "
                "'You are all very healthy children!' said the nurse."
            ),
            "cliffhanger": "What will they learn about first aid?",
            "vocab_tie": ["healthy", "wash", "brush", "fruit", "water"],
        },
        9: {
            "title": "The Legend of Nasreddin Hodja",
            "previously": "The class learned about health and hygiene.",
            "episode": (
                "Mr Demir opened a big storybook. 'Today, I will read a legend.' "
                "'A legend? What is that?' asked Leo. "
                "'It is a very old and famous story,' said Mia. "
                "Mr Demir read about Nasreddin Hodja and his donkey. "
                "Hodja rode the donkey backwards. People laughed. "
                "'Why are you sitting backwards?' they asked. "
                "'I am not backwards. The donkey is backwards!' said Hodja. "
                "The whole class laughed. 'He is very funny and clever!' said Zehra."
            ),
            "cliffhanger": "What other legends will they discover?",
            "vocab_tie": ["legend", "story", "clever", "funny", "famous"],
        },
        10: {
            "title": "The End of Year Show",
            "previously": "The class read the legend of Nasreddin Hodja.",
            "episode": (
                "It was the last week of school. 'Let us do a big show!' said Mr Demir. "
                "Mia wrote a short play. Can built the stage. "
                "Zehra painted the decorations. Leo chose the music. "
                "On the big day, parents came to watch. "
                "The show was wonderful! Everyone clapped. "
                "Mr Demir said, 'You learned so much this year!' "
                "Mia said, 'We are a great team!' "
                "'See you next year, friends!' said Leo with a big smile."
            ),
            "cliffhanger": "",
            "vocab_tie": ["show", "team", "wonderful", "parents", "memories"],
        },
    },
}

# ---------------------------------------------------------------------------
# 3. READING BANK  (10 passages, 70-100 words + 5 questions)
# ---------------------------------------------------------------------------
READING_BANK = {
    3: {
        1: {
            "title": "My Best Friend",
            "passage": (
                "My best friend is Elif. She is nine years old. She has long brown hair "
                "and big green eyes. Elif is very kind and funny. We go to the same school. "
                "We sit next to each other in class. After school, we play in the park. "
                "Elif likes drawing and I like reading. We share our lunch every day. "
                "Sometimes we are sad, but we always help each other. "
                "A good friend makes you happy. I am lucky to have Elif."
            ),
            "questions": [
                {"type": "mcq", "q": "How old is Elif?", "options": ["Eight", "Nine", "Ten", "Seven"], "answer": "Nine"},
                {"type": "tf", "q": "Elif has blue eyes.", "answer": False},
                {"type": "mcq", "q": "Where do they play after school?", "options": ["At home", "In the park", "At school", "In the library"], "answer": "In the park"},
                {"type": "tf", "q": "They share their lunch.", "answer": True},
                {"type": "open", "q": "What makes a good friend? Write one sentence.", "answer": "A good friend makes you happy."},
            ],
        },
        2: {
            "title": "Our Town",
            "passage": (
                "I live in a small town. There is a big park in the centre. "
                "Next to the park, there is a library. I go there every Saturday. "
                "The hospital is behind the school. There is a bakery on Main Street. "
                "The bread there is very fresh and delicious. My favourite place is "
                "the bookshop. It is between the bank and the post office. "
                "Our town is not very big, but it is beautiful and clean. "
                "I love living here."
            ),
            "questions": [
                {"type": "mcq", "q": "Where is the library?", "options": ["Next to the park", "Behind the school", "On Main Street", "Next to the bank"], "answer": "Next to the park"},
                {"type": "tf", "q": "The hospital is next to the bakery.", "answer": False},
                {"type": "mcq", "q": "How often does the writer go to the library?", "options": ["Every day", "Every Saturday", "Every Monday", "Every Sunday"], "answer": "Every Saturday"},
                {"type": "tf", "q": "The town is big.", "answer": False},
                {"type": "open", "q": "What is the writer's favourite place?", "answer": "The bookshop."},
            ],
        },
        3: {
            "title": "Pizza from Italy",
            "passage": (
                "Pizza comes from Italy. Italian people eat pizza every week. "
                "You need flour, water, tomatoes and cheese to make pizza. "
                "First, you make the dough. Then you put tomato sauce on it. "
                "Next, you add cheese on top. You can also add vegetables or meat. "
                "After that, you bake it in a hot oven. It takes about fifteen minutes. "
                "Pizza is popular all around the world. Children love it! "
                "In Turkey, lahmacun is a bit like pizza."
            ),
            "questions": [
                {"type": "mcq", "q": "Where does pizza come from?", "options": ["France", "Italy", "Turkey", "Spain"], "answer": "Italy"},
                {"type": "tf", "q": "You need butter to make pizza.", "answer": False},
                {"type": "mcq", "q": "How long does it take to bake pizza?", "options": ["Five minutes", "Ten minutes", "Fifteen minutes", "Twenty minutes"], "answer": "Fifteen minutes"},
                {"type": "tf", "q": "Pizza is popular all around the world.", "answer": True},
                {"type": "open", "q": "What Turkish food is like pizza?", "answer": "Lahmacun."},
            ],
        },
        4: {
            "title": "Save Our Planet",
            "passage": (
                "Our planet Earth is beautiful. It has oceans, forests and mountains. "
                "But our planet needs help. We must protect it. "
                "First, we can recycle paper, plastic and glass. "
                "Second, we can save water. Turn off the tap when you brush your teeth. "
                "Third, we can plant trees. Trees give us clean air. "
                "We should not throw rubbish on the ground. We should use less plastic. "
                "If we all help, our planet will be clean and healthy. "
                "Every small action counts!"
            ),
            "questions": [
                {"type": "mcq", "q": "What can we recycle?", "options": ["Food", "Paper, plastic and glass", "Water", "Trees"], "answer": "Paper, plastic and glass"},
                {"type": "tf", "q": "Trees give us clean air.", "answer": True},
                {"type": "mcq", "q": "When should we turn off the tap?", "options": ["When we eat", "When we sleep", "When we brush our teeth", "When we read"], "answer": "When we brush our teeth"},
                {"type": "tf", "q": "We should use more plastic.", "answer": False},
                {"type": "open", "q": "Why should we plant trees?", "answer": "Trees give us clean air."},
            ],
        },
        5: {
            "title": "The First Telephone",
            "passage": (
                "Alexander Graham Bell invented the telephone in 1876. "
                "Before the telephone, people sent letters. Letters took many days. "
                "The first telephone was very big and heavy. "
                "Today, phones are small and light. We carry them in our pockets. "
                "We can send messages, take photos and watch videos with our phones. "
                "In the past, only rich people had telephones. "
                "Now, almost everyone has a mobile phone. "
                "Technology changes our lives every day."
            ),
            "questions": [
                {"type": "mcq", "q": "Who invented the telephone?", "options": ["Thomas Edison", "Alexander Graham Bell", "Albert Einstein", "Nikola Tesla"], "answer": "Alexander Graham Bell"},
                {"type": "tf", "q": "The first telephone was small.", "answer": False},
                {"type": "mcq", "q": "What did people use before the telephone?", "options": ["E-mail", "Letters", "Computers", "Radio"], "answer": "Letters"},
                {"type": "tf", "q": "Today, phones are big and heavy.", "answer": False},
                {"type": "open", "q": "What can we do with our phones today?", "answer": "We can send messages, take photos and watch videos."},
            ],
        },
        6: {
            "title": "Musical Instruments",
            "passage": (
                "Music is everywhere in the world. People play different instruments. "
                "The piano has black and white keys. You press the keys to make sound. "
                "The guitar has six strings. You can play rock or folk music with it. "
                "The flute is a wind instrument. You blow into it to make beautiful sounds. "
                "Drums are very loud! You hit them with sticks. "
                "In Turkey, the saz is a traditional instrument. "
                "Music makes people happy. Everyone can learn an instrument."
            ),
            "questions": [
                {"type": "mcq", "q": "How many strings does a guitar have?", "options": ["Four", "Five", "Six", "Seven"], "answer": "Six"},
                {"type": "tf", "q": "You blow into a piano.", "answer": False},
                {"type": "mcq", "q": "What is a traditional Turkish instrument?", "options": ["Piano", "Guitar", "Saz", "Flute"], "answer": "Saz"},
                {"type": "tf", "q": "Drums are very quiet.", "answer": False},
                {"type": "open", "q": "How does the flute make sound?", "answer": "You blow into it."},
            ],
        },
        7: {
            "title": "Our Solar System",
            "passage": (
                "Our solar system has eight planets. They go around the Sun. "
                "Mercury is the closest planet to the Sun. It is very hot. "
                "Earth is the third planet. We live on Earth. It has water and air. "
                "Mars is red. Scientists want to visit Mars one day. "
                "Jupiter is the biggest planet. Saturn has beautiful rings. "
                "The Moon goes around Earth. We can see it at night. "
                "Space is very big and full of stars. There is so much to learn!"
            ),
            "questions": [
                {"type": "mcq", "q": "How many planets are in our solar system?", "options": ["Six", "Seven", "Eight", "Nine"], "answer": "Eight"},
                {"type": "tf", "q": "Mars is blue.", "answer": False},
                {"type": "mcq", "q": "Which planet is the biggest?", "options": ["Earth", "Saturn", "Mars", "Jupiter"], "answer": "Jupiter"},
                {"type": "tf", "q": "Earth has water and air.", "answer": True},
                {"type": "open", "q": "Which planet has rings?", "answer": "Saturn."},
            ],
        },
        8: {
            "title": "Healthy Habits",
            "passage": (
                "Being healthy is very important. There are many healthy habits. "
                "First, wash your hands with soap before you eat. "
                "Second, brush your teeth twice a day, morning and night. "
                "Third, eat lots of fruit and vegetables every day. "
                "Fourth, drink water, not fizzy drinks. "
                "Fifth, sleep eight to ten hours every night. "
                "Sixth, play outside and exercise for one hour a day. "
                "If you follow these habits, you will feel strong and happy!"
            ),
            "questions": [
                {"type": "mcq", "q": "How often should you brush your teeth?", "options": ["Once a day", "Twice a day", "Three times a day", "Once a week"], "answer": "Twice a day"},
                {"type": "tf", "q": "You should drink fizzy drinks.", "answer": False},
                {"type": "mcq", "q": "How many hours should children sleep?", "options": ["Five to six", "Six to seven", "Eight to ten", "Twelve"], "answer": "Eight to ten"},
                {"type": "tf", "q": "Exercise makes you feel strong.", "answer": True},
                {"type": "open", "q": "What should you wash your hands with?", "answer": "Soap."},
            ],
        },
        9: {
            "title": "Keloglan and the Giant",
            "passage": (
                "Keloglan is a famous Turkish folk hero. He is a bald boy. "
                "He is clever and kind. One day, a giant came to his village. "
                "The giant was big and scary. Everyone was afraid. "
                "But Keloglan was not afraid. He had a clever plan. "
                "He tricked the giant with a riddle. The giant could not answer. "
                "'You are too clever for me!' said the giant and he left. "
                "The village was safe again. Everyone thanked Keloglan. "
                "Sometimes, being clever is better than being strong."
            ),
            "questions": [
                {"type": "mcq", "q": "What is Keloglan?", "options": ["A giant", "A bald boy", "A king", "A teacher"], "answer": "A bald boy"},
                {"type": "tf", "q": "Everyone was afraid of the giant.", "answer": True},
                {"type": "mcq", "q": "How did Keloglan trick the giant?", "options": ["He fought", "He ran away", "He used a riddle", "He hid"], "answer": "He used a riddle"},
                {"type": "tf", "q": "The giant stayed in the village.", "answer": False},
                {"type": "open", "q": "What is the lesson of this story?", "answer": "Being clever is better than being strong."},
            ],
        },
        10: {
            "title": "Our Best Memories",
            "passage": (
                "This year was wonderful! We learned many things in English class. "
                "We made new friends and worked as a team. We read stories and legends. "
                "We studied planets and learned about healthy habits. "
                "We cooked food from different countries and drew beautiful pictures. "
                "We sang songs and played instruments at the school concert. "
                "The best memory was our end of year show. "
                "Our parents were very proud. We will never forget this year. "
                "Have a great summer, everyone!"
            ),
            "questions": [
                {"type": "mcq", "q": "What did they do at the school concert?", "options": ["Cooked food", "Sang songs and played instruments", "Read books", "Played football"], "answer": "Sang songs and played instruments"},
                {"type": "tf", "q": "The best memory was a field trip.", "answer": False},
                {"type": "mcq", "q": "Who came to the end of year show?", "options": ["Friends", "Parents", "Neighbours", "Police"], "answer": "Parents"},
                {"type": "tf", "q": "They learned about planets.", "answer": True},
                {"type": "open", "q": "What is your best memory from this year?", "answer": "Answers will vary."},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 4. GRAMMAR BANK  (10 rules + 5 exercises each)
# ---------------------------------------------------------------------------
GRAMMAR_BANK = {
    3: {
        1: {
            "rule": "Present Simple - be (am/is/are)",
            "explanation": "Use 'am' with I, 'is' with he/she/it, 'are' with you/we/they.",
            "examples": ["I am happy.", "She is kind.", "They are my friends."],
            "exercises": [
                {"type": "fill", "q": "I ___ nine years old.", "answer": "am"},
                {"type": "fill", "q": "She ___ my best friend.", "answer": "is"},
                {"type": "fill", "q": "We ___ in the same class.", "answer": "are"},
                {"type": "correct", "q": "He are funny. (Find the mistake.)", "answer": "He is funny."},
                {"type": "choose", "q": "They ___ happy. (is / are)", "answer": "are"},
            ],
        },
        2: {
            "rule": "There is / There are",
            "explanation": "Use 'there is' for one thing. Use 'there are' for more than one.",
            "examples": ["There is a park.", "There are two schools.", "Is there a library?"],
            "exercises": [
                {"type": "fill", "q": "There ___ a hospital in our town.", "answer": "is"},
                {"type": "fill", "q": "There ___ three bakeries.", "answer": "are"},
                {"type": "choose", "q": "___ there a cinema? (Is / Are)", "answer": "Is"},
                {"type": "correct", "q": "There are a bank. (Find the mistake.)", "answer": "There is a bank."},
                {"type": "fill", "q": "There ___ many buildings in the city.", "answer": "are"},
            ],
        },
        3: {
            "rule": "Countable & Uncountable Nouns (some / any)",
            "explanation": "Use 'some' in positive sentences. Use 'any' in questions and negatives.",
            "examples": ["I have some apples.", "Do you have any milk?", "There isn't any bread."],
            "exercises": [
                {"type": "fill", "q": "I want ___ water, please.", "answer": "some"},
                {"type": "fill", "q": "Do you have ___ cheese?", "answer": "any"},
                {"type": "choose", "q": "There are ___ tomatoes. (some / any)", "answer": "some"},
                {"type": "fill", "q": "We don't have ___ sugar.", "answer": "any"},
                {"type": "correct", "q": "Is there some milk? (Find the mistake.)", "answer": "Is there any milk?"},
            ],
        },
        4: {
            "rule": "Present Continuous",
            "explanation": "Use am/is/are + verb-ing for actions happening now.",
            "examples": ["I am reading.", "She is raining.", "They are playing."],
            "exercises": [
                {"type": "fill", "q": "It ___ raining now. (rain)", "answer": "is raining"},
                {"type": "fill", "q": "We ___ trees. (plant)", "answer": "are planting"},
                {"type": "choose", "q": "She ___ the flowers. (is watering / are watering)", "answer": "is watering"},
                {"type": "correct", "q": "He are recycling paper. (Find the mistake.)", "answer": "He is recycling paper."},
                {"type": "fill", "q": "I ___ about the weather. (learn)", "answer": "am learning"},
            ],
        },
        5: {
            "rule": "Past Simple - was / were",
            "explanation": "Use 'was' with I/he/she/it. Use 'were' with you/we/they.",
            "examples": ["It was fun.", "They were old.", "There was no phone."],
            "exercises": [
                {"type": "fill", "q": "There ___ no computers in the past.", "answer": "were"},
                {"type": "fill", "q": "It ___ a great invention.", "answer": "was"},
                {"type": "choose", "q": "People ___ different then. (was / were)", "answer": "were"},
                {"type": "correct", "q": "She were happy. (Find the mistake.)", "answer": "She was happy."},
                {"type": "fill", "q": "The telephone ___ very big.", "answer": "was"},
            ],
        },
        6: {
            "rule": "Can / Can't (ability)",
            "explanation": "Use 'can' to say someone is able to do something. Use 'can't' for not able.",
            "examples": ["I can play the guitar.", "She can't sing.", "Can you dance?"],
            "exercises": [
                {"type": "fill", "q": "He ___ play the piano very well.", "answer": "can"},
                {"type": "fill", "q": "I ___ play the drum. It is too hard.", "answer": "can't"},
                {"type": "choose", "q": "___ you sing a song? (Can / Does)", "answer": "Can"},
                {"type": "correct", "q": "She can plays the flute. (Find the mistake.)", "answer": "She can play the flute."},
                {"type": "fill", "q": "They ___ dance very well.", "answer": "can"},
            ],
        },
        7: {
            "rule": "Prepositions of Place (in, on, under, between, next to)",
            "explanation": "Prepositions tell us WHERE something is.",
            "examples": ["The book is on the table.", "The cat is under the chair.", "Mars is between Earth and Jupiter."],
            "exercises": [
                {"type": "fill", "q": "The Moon is ___ the sky.", "answer": "in"},
                {"type": "fill", "q": "The rocket is ___ the launch pad.", "answer": "on"},
                {"type": "choose", "q": "Earth is ___ Venus and Mars. (between / under)", "answer": "between"},
                {"type": "fill", "q": "The stars are ___ to the Moon.", "answer": "next"},
                {"type": "correct", "q": "The book is at the table. (Find the mistake.)", "answer": "The book is on the table."},
            ],
        },
        8: {
            "rule": "Imperatives (commands and advice)",
            "explanation": "Use the base form of the verb for commands. Add 'Don't' for negative.",
            "examples": ["Wash your hands!", "Don't eat too much sugar.", "Drink water every day."],
            "exercises": [
                {"type": "fill", "q": "___ your teeth twice a day.", "answer": "Brush"},
                {"type": "fill", "q": "___ touch your face with dirty hands.", "answer": "Don't"},
                {"type": "choose", "q": "___ lots of fruit. (Eat / Eats)", "answer": "Eat"},
                {"type": "correct", "q": "Don't drinks fizzy drinks. (Find the mistake.)", "answer": "Don't drink fizzy drinks."},
                {"type": "fill", "q": "___ eight hours every night.", "answer": "Sleep"},
            ],
        },
        9: {
            "rule": "Past Simple - Regular Verbs (-ed)",
            "explanation": "Add -ed to regular verbs for the past. Example: walk -> walked.",
            "examples": ["He lived in a village.", "She helped the people.", "They laughed loudly."],
            "exercises": [
                {"type": "fill", "q": "Keloglan ___ the giant. (trick)", "answer": "tricked"},
                {"type": "fill", "q": "The villagers ___ Keloglan. (thank)", "answer": "thanked"},
                {"type": "choose", "q": "The giant ___ the village. (visited / visit)", "answer": "visited"},
                {"type": "correct", "q": "She help everyone yesterday. (Find the mistake.)", "answer": "She helped everyone yesterday."},
                {"type": "fill", "q": "They ___ a long time ago. (live)", "answer": "lived"},
            ],
        },
        10: {
            "rule": "Comparatives (-er / more)",
            "explanation": "Use -er for short adjectives. Use 'more' for long adjectives.",
            "examples": ["She is taller than me.", "This year was better.", "The show was more exciting."],
            "exercises": [
                {"type": "fill", "q": "Summer is ___ than winter. (hot)", "answer": "hotter"},
                {"type": "fill", "q": "The show was ___ than last year. (good)", "answer": "better"},
                {"type": "choose", "q": "English is ___ than maths. (funner / more fun)", "answer": "more fun"},
                {"type": "correct", "q": "She is more tall than him. (Find the mistake.)", "answer": "She is taller than him."},
                {"type": "fill", "q": "This book is ___ than that one. (easy)", "answer": "easier"},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 5. DIALOGUE BANK  (10 dialogues: title, setting, 6 lines as tuples, task)
# ---------------------------------------------------------------------------
DIALOGUE_BANK = {
    3: {
        1: {
            "title": "Meeting a New Friend",
            "setting": "School playground, first day of school",
            "lines": [
                ("Mia", "Hi! What is your name?"),
                ("Leo", "Hello! My name is Leo."),
                ("Mia", "Where are you from, Leo?"),
                ("Leo", "I am from London. And you?"),
                ("Mia", "I am from Istanbul. Welcome!"),
                ("Leo", "Thank you! You are very kind."),
            ],
            "task": "Practise with a friend. Introduce yourself.",
        },
        2: {
            "title": "Asking for Directions",
            "setting": "On the street, near the town centre",
            "lines": [
                ("Leo", "Excuse me. Where is the library?"),
                ("Mia", "Go straight. Then turn left."),
                ("Leo", "Is it far from here?"),
                ("Mia", "No, it is not far. Five minutes."),
                ("Leo", "Is it next to the park?"),
                ("Mia", "Yes! It is next to the park."),
            ],
            "task": "Give directions to a place in your town.",
        },
        3: {
            "title": "Ordering Food",
            "setting": "A restaurant, lunchtime",
            "lines": [
                ("Waiter", "Good afternoon. What would you like?"),
                ("Can", "I would like some soup, please."),
                ("Waiter", "And to drink?"),
                ("Can", "Orange juice, please."),
                ("Waiter", "Would you like any dessert?"),
                ("Can", "Yes, chocolate cake, please. Thank you!"),
            ],
            "task": "Order your favourite meal at a restaurant.",
        },
        4: {
            "title": "Talking About the Weather",
            "setting": "Classroom, looking out the window",
            "lines": [
                ("Zehra", "Look outside! What is the weather like?"),
                ("Can", "It is cloudy and cold today."),
                ("Zehra", "Do you think it will rain?"),
                ("Can", "Maybe. I have my umbrella."),
                ("Zehra", "I like rainy days. They are cosy."),
                ("Can", "Me too! We can read inside."),
            ],
            "task": "Talk about today's weather with a friend.",
        },
        5: {
            "title": "Past and Present",
            "setting": "Classroom, during a history lesson",
            "lines": [
                ("Mr Demir", "What was life like in the past?"),
                ("Mia", "There were no computers."),
                ("Leo", "People wrote letters with pens."),
                ("Mr Demir", "And now? What is different?"),
                ("Can", "Now we have phones and tablets."),
                ("Zehra", "Technology makes life easier!"),
            ],
            "task": "Tell your friend about one old and one new invention.",
        },
        6: {
            "title": "Talking About Music",
            "setting": "Music room, after school",
            "lines": [
                ("Zehra", "Can you play an instrument?"),
                ("Leo", "Yes, I can play the guitar."),
                ("Zehra", "That is great! I can sing."),
                ("Leo", "Let us practise for the concert!"),
                ("Zehra", "Good idea! What song shall we play?"),
                ("Leo", "How about a folk song?"),
            ],
            "task": "Ask your friend about their favourite instrument.",
        },
        7: {
            "title": "Looking at the Night Sky",
            "setting": "School garden, at night",
            "lines": [
                ("Can", "Wow! Look at all the stars!"),
                ("Mia", "Can you see the Moon?"),
                ("Can", "Yes! It is very bright tonight."),
                ("Mia", "Which planet is that bright dot?"),
                ("Can", "I think it is Jupiter."),
                ("Mia", "Space is amazing, isn't it?"),
            ],
            "task": "Talk about what you can see in the night sky.",
        },
        8: {
            "title": "At the Doctor",
            "setting": "Doctor's office",
            "lines": [
                ("Doctor", "Good morning. What is the problem?"),
                ("Leo", "I have a headache and a cough."),
                ("Doctor", "Do you have a fever?"),
                ("Leo", "Yes, I feel hot."),
                ("Doctor", "Drink lots of water and rest."),
                ("Leo", "Thank you, doctor. Goodbye!"),
            ],
            "task": "Pretend you are at the doctor. Describe how you feel.",
        },
        9: {
            "title": "Telling a Story",
            "setting": "Reading corner in the classroom",
            "lines": [
                ("Zehra", "Do you know Nasreddin Hodja?"),
                ("Leo", "No. Who is he?"),
                ("Zehra", "He is a famous folk hero from Turkey."),
                ("Leo", "What did he do?"),
                ("Zehra", "He was very clever and funny."),
                ("Leo", "Tell me a story about him, please!"),
            ],
            "task": "Tell a short folk story to your friend.",
        },
        10: {
            "title": "Saying Goodbye",
            "setting": "Classroom, last day of school",
            "lines": [
                ("Mia", "I can't believe it is the last day!"),
                ("Leo", "This year was the best!"),
                ("Mia", "I will miss you in summer."),
                ("Leo", "Me too! But we can write letters."),
                ("Mia", "Great idea! Have a nice summer!"),
                ("Leo", "You too! See you next year!"),
            ],
            "task": "Say goodbye to your classmates for the summer.",
        },
    },
}

# ---------------------------------------------------------------------------
# 6. SONG BANK  (10 songs)
# ---------------------------------------------------------------------------
SONG_BANK = {
    3: {
        1: {
            "title": "The Friendship Song",
            "type": "Song",
            "lyrics": (
                "Friends, friends, we are friends,\n"
                "Together from beginning to end!\n"
                "Happy, sad, or in between,\n"
                "You are the best friend I have seen!\n\n"
                "Kind and funny, brave and true,\n"
                "I am so glad I have you!\n"
                "Friends, friends, we are friends,\n"
                "Together from beginning to end!"
            ),
            "activity": "Hold hands with a friend and sing together.",
        },
        2: {
            "title": "Around the Town",
            "type": "Song",
            "lyrics": (
                "Turn left, turn right, go straight ahead,\n"
                "Past the bakery with yummy bread!\n"
                "The library is on the right,\n"
                "The park is such a pretty sight!\n\n"
                "Where is the school? Where is the shop?\n"
                "Walking around, we never stop!\n"
                "Turn left, turn right, go straight ahead,\n"
                "Our town is great, just like I said!"
            ),
            "activity": "Walk around the classroom and follow the directions in the song.",
        },
        3: {
            "title": "Yummy Yummy Food",
            "type": "Song",
            "lyrics": (
                "Yummy, yummy, yummy in my tummy!\n"
                "Pizza, pasta, rice and bread,\n"
                "All the food that keeps me fed!\n\n"
                "Fruit and veg are good for me,\n"
                "Apples, carrots, one, two, three!\n"
                "Yummy, yummy, yummy in my tummy!\n"
                "Eating well makes life so sunny!"
            ),
            "activity": "Clap when you hear a food you like!",
        },
        4: {
            "title": "The Weather Rap",
            "type": "Rap",
            "lyrics": (
                "What's the weather like today? (Hey! Hey!)\n"
                "Is it sunny? Let's go play! (Hey! Hey!)\n"
                "Is it rainy? That's okay! (Hey! Hey!)\n"
                "Grab your coat and on your way! (Hey! Hey!)\n\n"
                "Cloudy, windy, cold or hot,\n"
                "We love the weather that we've got!\n"
                "What's the weather like today?\n"
                "Tell me, tell me, hip hooray!"
            ),
            "activity": "Do actions for each weather type while you rap.",
        },
        5: {
            "title": "Old and New",
            "type": "Song",
            "lyrics": (
                "In the past, they wrote with pens,\n"
                "Rode on horses, lived in dens.\n"
                "No computers, no TV,\n"
                "Life was different, can you see?\n\n"
                "Now we have phones and cars that go,\n"
                "Tablets, rockets, what a show!\n"
                "Old and new, both are cool,\n"
                "We learn about them all at school!"
            ),
            "activity": "Draw something old and something new while singing.",
        },
        6: {
            "title": "Music Makes Me Happy",
            "type": "Song",
            "lyrics": (
                "La la la, music makes me happy!\n"
                "Sing a song, clap along, snappy!\n"
                "Piano, guitar, drum and flute,\n"
                "Every instrument is cute!\n\n"
                "Dance and spin and tap your feet,\n"
                "Music gives a groovy beat!\n"
                "La la la, music makes me happy!\n"
                "Sing a song, clap along, snappy!"
            ),
            "activity": "Pretend to play an instrument while you sing.",
        },
        7: {
            "title": "Rocket to the Stars",
            "type": "Song",
            "lyrics": (
                "Five, four, three, two, one — BLAST OFF!\n"
                "Rocket to the stars, we're gone!\n"
                "Mercury, Venus, Earth and Mars,\n"
                "Flying past the shining stars!\n\n"
                "Jupiter, Saturn, way out there,\n"
                "Uranus, Neptune, everywhere!\n"
                "Eight planets round the Sun we go,\n"
                "Space is the greatest show!"
            ),
            "activity": "Count down from five and jump up at BLAST OFF!",
        },
        8: {
            "title": "Healthy Me",
            "type": "Chant",
            "lyrics": (
                "Wash your hands! (wash, wash, wash!)\n"
                "Brush your teeth! (brush, brush, brush!)\n"
                "Eat your fruit! (munch, munch, munch!)\n"
                "Drink your water! (gulp, gulp, gulp!)\n\n"
                "Sleep all night! (zzz, zzz, zzz!)\n"
                "Play outside! (run, run, run!)\n"
                "Healthy me, healthy you,\n"
                "Healthy habits, through and through!"
            ),
            "activity": "Do the actions for each healthy habit.",
        },
        9: {
            "title": "The Legend Song",
            "type": "Song",
            "lyrics": (
                "Long, long ago in a land so old,\n"
                "Heroes were brave and stories were told.\n"
                "Clever and kind, they saved the day,\n"
                "Listen to the legends, come and play!\n\n"
                "Keloglan, Hodja, heroes so bright,\n"
                "They used their brains and did what was right.\n"
                "Long, long ago in a land so old,\n"
                "These are the stories that must be told!"
            ),
            "activity": "Act out your favourite legend character while singing.",
        },
        10: {
            "title": "Summer Goodbye",
            "type": "Song",
            "lyrics": (
                "Goodbye, goodbye, see you soon!\n"
                "Summer is here, under the moon!\n"
                "Swimming, running, having fun,\n"
                "Playing games under the sun!\n\n"
                "We learned so much, we grew so tall,\n"
                "English class was best of all!\n"
                "Goodbye, goodbye, see you in September,\n"
                "This year is one we will always remember!"
            ),
            "activity": "Wave and hug your friends as you sing goodbye.",
        },
    },
}

# ---------------------------------------------------------------------------
# 7. CULTURE CORNER BANK  (10 entries)
# ---------------------------------------------------------------------------
CULTURE_CORNER_BANK = {
    3: {
        1: {
            "title": "Friendship Bracelets",
            "text": (
                "In many countries, children give friendship bracelets to their best friends. "
                "In Brazil, children make colourful bracelets from thread. "
                "In Japan, children exchange friendship charms called 'omamori'. "
                "In Turkey, children sometimes give 'nazar' beads to friends for good luck. "
                "Friendship is the same everywhere!"
            ),
            "question": "Do you give anything to your best friend?",
            "country_flag": "BR, JP, TR",
            "recipe": None,
        },
        2: {
            "title": "Famous Cities",
            "text": (
                "Every country has famous cities. London is in England. "
                "It has Big Ben and red buses. Paris is in France. "
                "It has the Eiffel Tower. Tokyo is in Japan. It is very modern. "
                "Istanbul is in Turkey. It has the Bosphorus and beautiful mosques. "
                "Which city would you like to visit?"
            ),
            "question": "What famous building is in your city or town?",
            "country_flag": "GB, FR, JP, TR",
            "recipe": None,
        },
        3: {
            "title": "School Lunches Around the World",
            "text": (
                "Children eat different food at school around the world. "
                "In Japan, children eat rice, fish and soup for lunch. "
                "In Italy, children eat pasta with vegetables. "
                "In India, children eat rice and lentils called 'dal'. "
                "In Turkey, children eat soup, rice and meat. "
                "Healthy food helps children learn!"
            ),
            "question": "What is your favourite school lunch?",
            "country_flag": "JP, IT, IN, TR",
            "recipe": None,
        },
        4: {
            "title": "Earth Day",
            "text": (
                "Every year on April 22nd, people celebrate Earth Day. "
                "People all over the world plant trees and clean parks. "
                "In the USA, children do recycling projects at school. "
                "In Kenya, people plant millions of trees. "
                "In Turkey, schools organise 'green walks' and clean-up days. "
                "We can all help our planet!"
            ),
            "question": "What can you do to help the Earth?",
            "country_flag": "US, KE, TR",
            "recipe": None,
        },
        5: {
            "title": "Great Inventions",
            "text": (
                "Many inventions changed the world. The wheel was invented thousands of years ago. "
                "The printing press was invented in 1440 by Gutenberg. "
                "The light bulb was invented by Thomas Edison in 1879. "
                "The internet was invented in the 1990s. "
                "Turkish people invented yoghurt and Turkish coffee!"
            ),
            "question": "What invention do you think is the most important?",
            "country_flag": "DE, US, TR",
            "recipe": None,
        },
        6: {
            "title": "Music and Dance Around the World",
            "text": (
                "Every country has its own music and dance. "
                "In Spain, people dance flamenco with red dresses. "
                "In Ireland, people do fast tap dancing called 'Riverdance'. "
                "In Africa, people play drums and dance together. "
                "In Turkey, people dance the 'halay' and 'horon'. "
                "Music connects people everywhere!"
            ),
            "question": "Can you show a dance from your culture?",
            "country_flag": "ES, IE, TR",
            "recipe": None,
        },
        7: {
            "title": "Space Exploration",
            "text": (
                "Many countries explore space. The USA sent the first man to the Moon in 1969. "
                "Russia sent the first person to space in 1961. His name was Yuri Gagarin. "
                "China has a space station in space. "
                "Turkey is also working on space projects now. "
                "One day, humans may live on Mars!"
            ),
            "question": "Would you like to go to space?",
            "country_flag": "US, RU, CN, TR",
            "recipe": None,
        },
        8: {
            "title": "Healthy Food Around the World",
            "text": (
                "Different countries have different healthy foods. "
                "In Greece, people eat lots of olive oil and vegetables. "
                "In Japan, people eat fish and seaweed. "
                "In Mexico, people eat beans and corn. "
                "In Turkey, people eat yoghurt, fresh fruit and vegetables. "
                "Eating healthy food keeps us strong!"
            ),
            "question": "What healthy food do you eat at home?",
            "country_flag": "GR, JP, MX, TR",
            "recipe": None,
        },
        9: {
            "title": "Folk Heroes of the World",
            "text": (
                "Many countries have famous folk heroes. "
                "Robin Hood is from England. He helped poor people. "
                "Pippi Longstocking is from Sweden. She is very strong and funny. "
                "Anansi the spider is from West Africa. He is very clever. "
                "In Turkey, Nasreddin Hodja and Keloglan are famous folk heroes. "
                "All these heroes teach us to be good and clever."
            ),
            "question": "Who is your favourite hero from a story?",
            "country_flag": "GB, SE, GH, TR",
            "recipe": None,
        },
        10: {
            "title": "Summer Holidays Around the World",
            "text": (
                "Children around the world love summer holidays! "
                "In Australia, summer is in December and January. "
                "In America, children go to summer camp. "
                "In Italy, families go to the beach. "
                "In Turkey, children visit grandparents in the village. "
                "No matter where you are, summer is fun!"
            ),
            "question": "What do you do in summer?",
            "country_flag": "AU, US, IT, TR",
            "recipe": None,
        },
    },
}

# ---------------------------------------------------------------------------
# 8. TURKEY CORNER BANK  (10 entries)
# ---------------------------------------------------------------------------
TURKEY_CORNER_BANK = {
    3: {
        1: {
            "title": "Turkish Tea and Friendship",
            "text": (
                "In Turkey, friends drink tea together. Turkish tea is dark red. "
                "People serve it in small glasses. When a friend visits, you always offer tea. "
                "Tea means friendship and kindness in Turkey."
            ),
            "famous_person": "Yunus Emre - a famous Turkish poet who wrote about love and friendship.",
            "activity": "Draw a Turkish tea glass and write 'Friendship' on it.",
            "recipe": {"name": "Turkish Tea", "steps": ["Boil water.", "Put tea leaves in the small pot.", "Pour hot water.", "Wait five minutes.", "Serve in small glasses."]},
        },
        2: {
            "title": "Istanbul - City of Two Continents",
            "text": (
                "Istanbul is the only city in the world on two continents. "
                "Asia is on one side. Europe is on the other side. "
                "The Bosphorus is the water between them. "
                "Istanbul has mosques, bazaars and beautiful bridges."
            ),
            "famous_person": "Mimar Sinan - a famous architect who built beautiful mosques.",
            "activity": "Draw the Bosphorus Bridge and colour it.",
            "recipe": {"name": "Simit", "steps": ["Make dough with flour and water.", "Shape into a ring.", "Cover with sesame seeds.", "Bake in the oven.", "Eat with cheese and tea!"]},
        },
        3: {
            "title": "Turkish Breakfast",
            "text": (
                "Turkish breakfast is famous around the world. "
                "There is cheese, olives, tomatoes, cucumbers, eggs and honey. "
                "People eat fresh bread with butter and jam. "
                "Turkish people love a big breakfast with family on Sundays."
            ),
            "famous_person": "Dede Korkut - a legendary storyteller who told tales at meals.",
            "activity": "Draw your favourite Turkish breakfast items.",
            "recipe": {"name": "Menemen", "steps": ["Chop tomatoes and peppers.", "Cook them in a pan with oil.", "Add eggs and stir.", "Add salt.", "Eat with bread!"]},
        },
        4: {
            "title": "Cappadocia - Land of Fairy Chimneys",
            "text": (
                "Cappadocia is in central Turkey. It has amazing rock formations. "
                "People call them 'fairy chimneys'. In the past, people lived inside the rocks. "
                "Today, tourists fly in hot air balloons over Cappadocia. It is very beautiful."
            ),
            "famous_person": "Evliya Celebi - a famous Turkish traveller who explored Turkey.",
            "activity": "Draw a hot air balloon over fairy chimneys.",
            "recipe": {"name": "Pottery Kebab", "steps": ["Put meat and vegetables in a clay pot.", "Seal the top.", "Bake in the oven.", "Break the pot to serve!", "Eat with bread."]},
        },
        5: {
            "title": "Turkish Inventions",
            "text": (
                "Turkish people invented many things. Yoghurt is a Turkish word! "
                "Turkish coffee is famous around the world. "
                "The first hospital was built in Turkey by the Seljuks. "
                "Today, Turkey makes cars, planes and technology."
            ),
            "famous_person": "Aziz Sancar - a Turkish scientist who won the Nobel Prize.",
            "activity": "Make a poster about a Turkish invention.",
            "recipe": {"name": "Turkish Coffee", "steps": ["Put fine coffee in a cezve.", "Add water and sugar.", "Heat slowly.", "Do not boil.", "Pour into small cups."]},
        },
        6: {
            "title": "Turkish Folk Music",
            "text": (
                "Turkey has rich folk music. The saz is a string instrument. "
                "The davul is a large drum. The zurna is a wind instrument. "
                "In weddings, people play davul and zurna and dance the halay. "
                "Music is a big part of Turkish culture."
            ),
            "famous_person": "Baris Manco - a beloved Turkish musician and TV presenter.",
            "activity": "Listen to a Turkish folk song and clap the rhythm.",
            "recipe": None,
        },
        7: {
            "title": "Turkey's Space Goals",
            "text": (
                "Turkey wants to explore space. Turkey has its own satellite programme. "
                "In 2023, Turkey's first astronaut went to space. "
                "Turkish students study science and space at universities. "
                "Maybe one day, a Turkish astronaut will walk on the Moon!"
            ),
            "famous_person": "Alper Gezeravci - Turkey's first astronaut.",
            "activity": "Draw a Turkish flag on the Moon.",
            "recipe": None,
        },
        8: {
            "title": "Turkish Baths - Hamam",
            "text": (
                "Turkish baths are called 'hamam'. They are hundreds of years old. "
                "People go to the hamam to wash, relax and stay clean. "
                "The water is warm and steamy. "
                "Hamams are an important part of Turkish health culture."
            ),
            "famous_person": "Hippocrates - ancient doctor; Turkish hamams follow his health ideas.",
            "activity": "Write three healthy habits from Turkish culture.",
            "recipe": None,
        },
        9: {
            "title": "Nasreddin Hodja - A Turkish Legend",
            "text": (
                "Nasreddin Hodja lived in Aksehir about 800 years ago. "
                "He was very clever and funny. He told stories with a lesson. "
                "People around the world know his stories. "
                "Every year, there is a Nasreddin Hodja festival in Aksehir."
            ),
            "famous_person": "Nasreddin Hodja - wise, funny folk hero loved by everyone.",
            "activity": "Read a Hodja story and draw your favourite part.",
            "recipe": {"name": "Aksehir Kebab", "steps": ["Season the meat.", "Put on skewers.", "Grill over charcoal.", "Serve with onion and parsley.", "Eat with lavash bread."]},
        },
        10: {
            "title": "Summer in Turkey",
            "text": (
                "Summer in Turkey is warm and sunny. Families go to the beach. "
                "Antalya, Bodrum and Cesme are popular holiday places. "
                "Children eat watermelon and swim in the sea. "
                "Summer is the best time for family and fun in Turkey!"
            ),
            "famous_person": "Mustafa Kemal Ataturk - founder of modern Turkey who loved the Turkish coast.",
            "activity": "Draw your dream summer holiday place in Turkey.",
            "recipe": {"name": "Watermelon Juice", "steps": ["Cut watermelon into pieces.", "Remove the seeds.", "Blend in a blender.", "Add ice.", "Drink and enjoy!"]},
        },
    },
}

# ---------------------------------------------------------------------------
# 9. PROJECT BANK  (10 projects)
# ---------------------------------------------------------------------------
PROJECT_BANK = {
    3: {
        1: {
            "title": "Friendship Poster",
            "desc": "Make a poster about what makes a good friend.",
            "steps": [
                "Write 'A Good Friend is...' at the top.",
                "Draw pictures of friends doing kind things.",
                "Write five adjectives: kind, funny, helpful, honest, caring.",
                "Add photos or drawings of you and your friends.",
                "Present your poster to the class.",
            ],
            "materials": "Large poster paper, markers, photos, glue, stickers",
        },
        2: {
            "title": "3D City Map",
            "desc": "Build a 3D map of your town or city.",
            "steps": [
                "Draw streets on a big card.",
                "Make buildings from small boxes: school, hospital, library.",
                "Label each building in English.",
                "Add small trees and cars from paper.",
                "Give directions to a friend using your map.",
            ],
            "materials": "Large cardboard, small boxes, paint, markers, glue",
        },
        3: {
            "title": "International Recipe Book",
            "desc": "Create a recipe book with food from different countries.",
            "steps": [
                "Choose five foods from five countries.",
                "Write the recipe name and country.",
                "Draw each food on a page.",
                "Write the ingredients list.",
                "Staple the pages to make a book.",
            ],
            "materials": "Paper, stapler, coloured pencils, markers",
        },
        4: {
            "title": "Recycling Station",
            "desc": "Create a recycling station for your classroom.",
            "steps": [
                "Get three boxes or bins.",
                "Label them: Paper, Plastic, Glass.",
                "Decorate each box with the right colour.",
                "Make a poster explaining what goes in each bin.",
                "Use the station every day!",
            ],
            "materials": "Three boxes, paint, labels, markers",
        },
        5: {
            "title": "Then and Now Timeline",
            "desc": "Make a timeline showing inventions from the past and present.",
            "steps": [
                "Draw a long line on card.",
                "Mark dates: 1800, 1900, 2000, Now.",
                "Draw old inventions on the left: candle, horse cart, letter.",
                "Draw new inventions on the right: light bulb, car, phone.",
                "Present your timeline to the class.",
            ],
            "materials": "Long card, markers, rulers, printed pictures",
        },
        6: {
            "title": "Musical Instrument",
            "desc": "Make a musical instrument from recycled materials.",
            "steps": [
                "Choose an instrument: drum, guitar or shaker.",
                "Collect recycled materials: boxes, rubber bands, bottles.",
                "Build your instrument.",
                "Decorate it with paint and stickers.",
                "Play it for the class!",
            ],
            "materials": "Recycled boxes, rubber bands, bottles, rice, paint",
        },
        7: {
            "title": "Solar System Model",
            "desc": "Build a model of the solar system.",
            "steps": [
                "Make the Sun from a big yellow ball.",
                "Make eight planets from different sized balls or clay.",
                "Paint each planet the right colour.",
                "Hang them in order from the Sun.",
                "Label each planet in English.",
            ],
            "materials": "Styrofoam balls or clay, paint, string, wire hanger",
        },
        8: {
            "title": "Healthy Habits Board Game",
            "desc": "Create a board game about healthy habits.",
            "steps": [
                "Draw a path with 20 squares on card.",
                "Write healthy habits on green squares: +2 spaces.",
                "Write unhealthy habits on red squares: -2 spaces.",
                "Make a dice from paper.",
                "Play with your friends!",
            ],
            "materials": "Large card, markers, small tokens, paper dice",
        },
        9: {
            "title": "Legend Storybook",
            "desc": "Write and illustrate your own legend storybook.",
            "steps": [
                "Choose a folk hero: Keloglan, Hodja or your own hero.",
                "Write a short story (8-10 sentences).",
                "Draw a picture for each page.",
                "Design a colourful cover.",
                "Read your story to the class.",
            ],
            "materials": "Paper, stapler, coloured pencils, markers",
        },
        10: {
            "title": "Memory Scrapbook",
            "desc": "Make a scrapbook of your best memories from this year.",
            "steps": [
                "Collect photos, drawings and notes from the year.",
                "Write a sentence about each memory in English.",
                "Glue everything into a notebook.",
                "Decorate with stickers and drawings.",
                "Share it with your family.",
            ],
            "materials": "Notebook or paper, glue, photos, stickers, markers",
        },
    },
}

# ---------------------------------------------------------------------------
# 10. STEAM BANK  (10 entries)
# ---------------------------------------------------------------------------
STEAM_BANK = {
    3: {
        1: {
            "subject": "Social Studies",
            "title": "Emotion Faces",
            "task": "Draw six faces showing different emotions: happy, sad, angry, scared, surprised, excited. Label each one in English.",
            "vocab": ["happy", "sad", "angry", "scared", "excited"],
        },
        2: {
            "subject": "Mathematics",
            "title": "Building Shapes City",
            "task": "Use 2D shapes (squares, rectangles, triangles, circles) to design a city on paper. Count how many of each shape you use.",
            "vocab": ["square", "rectangle", "triangle", "circle", "building"],
        },
        3: {
            "subject": "Science",
            "title": "Food Groups Sorting",
            "task": "Cut out pictures of food from magazines. Sort them into groups: fruit, vegetables, grains, protein, dairy. Make a poster.",
            "vocab": ["fruit", "vegetable", "grain", "protein", "dairy"],
        },
        4: {
            "subject": "Science",
            "title": "Mini Weather Station",
            "task": "Make a simple rain gauge from a plastic bottle. Measure the rain for one week. Record the results in a chart.",
            "vocab": ["rain", "measure", "chart", "result", "weather"],
        },
        5: {
            "subject": "Technology",
            "title": "Paper Bridge Challenge",
            "task": "Build the strongest bridge using only paper and tape. Test it by putting coins on top. Which design holds the most coins?",
            "vocab": ["bridge", "strong", "design", "test", "weight"],
        },
        6: {
            "subject": "Art",
            "title": "Sound Painting",
            "task": "Listen to three different pieces of music. Paint what you feel when you hear each one. Use colours and shapes.",
            "vocab": ["sound", "colour", "shape", "painting", "music"],
        },
        7: {
            "subject": "Science",
            "title": "Planet Fact Cards",
            "task": "Make a fact card for each planet. Write the name, colour, size (big/small) and one fun fact. Arrange them in order from the Sun.",
            "vocab": ["planet", "Sun", "size", "fact", "order"],
        },
        8: {
            "subject": "Science",
            "title": "Germ Experiment",
            "task": "Put glitter on your hands. Shake hands with a friend. See how the 'germs' spread. Then wash your hands and see the difference!",
            "vocab": ["germ", "spread", "wash", "soap", "clean"],
        },
        9: {
            "subject": "English",
            "title": "Story Map",
            "task": "Read a folk tale. Draw a story map with Beginning, Middle and End. Write one sentence for each part.",
            "vocab": ["beginning", "middle", "end", "character", "story"],
        },
        10: {
            "subject": "Engineering",
            "title": "Stage Design",
            "task": "Design a stage for the end of year show. Draw it from the front. Label the parts: stage, curtain, lights, seats, speakers.",
            "vocab": ["stage", "curtain", "lights", "seats", "design"],
        },
    },
}

# ---------------------------------------------------------------------------
# 11. LISTENING SCRIPT BANK  (10 scripts + 3 tasks each)
# ---------------------------------------------------------------------------
LISTENING_SCRIPT_BANK = {
    3: {
        1: {
            "title": "My New Friend",
            "script": (
                "Narrator: Listen and answer the questions.\n\n"
                "Leo: Hello! My name is Leo. I am nine years old.\n"
                "Leo: I am from London, but I live in Turkey now.\n"
                "Leo: I have brown hair and blue eyes.\n"
                "Leo: I like football and reading.\n"
                "Leo: My best friend is Can. He is very funny.\n"
                "Leo: We play together every day after school."
            ),
            "tasks": [
                "How old is Leo?",
                "Where is Leo from?",
                "Who is Leo's best friend?",
            ],
        },
        2: {
            "title": "Finding the Bookshop",
            "script": (
                "Narrator: Listen to the directions.\n\n"
                "Man: Excuse me. Where is the bookshop?\n"
                "Woman: Go straight ahead. Then turn right.\n"
                "Man: Turn right. Okay.\n"
                "Woman: The bookshop is next to the bank.\n"
                "Man: Is it far?\n"
                "Woman: No, it is five minutes from here.\n"
                "Man: Thank you very much!\n"
                "Woman: You're welcome!"
            ),
            "tasks": [
                "Where is the man going?",
                "Does he turn left or right?",
                "How far is the bookshop?",
            ],
        },
        3: {
            "title": "At the Restaurant",
            "script": (
                "Narrator: Listen to the conversation.\n\n"
                "Waiter: Good afternoon! What would you like?\n"
                "Girl: I would like some chicken and rice, please.\n"
                "Waiter: And to drink?\n"
                "Girl: Apple juice, please.\n"
                "Waiter: Would you like any dessert?\n"
                "Girl: Yes! Chocolate cake, please.\n"
                "Waiter: Very good. Coming right up!"
            ),
            "tasks": [
                "What food does the girl order?",
                "What does she drink?",
                "What dessert does she want?",
            ],
        },
        4: {
            "title": "The Weather Report",
            "script": (
                "Narrator: Listen to the weather report.\n\n"
                "Reporter: Good morning! Here is today's weather.\n"
                "Reporter: It is sunny in Antalya. Temperature: 28 degrees.\n"
                "Reporter: It is cloudy in Ankara. Temperature: 18 degrees.\n"
                "Reporter: It is rainy in Istanbul. Take your umbrella!\n"
                "Reporter: Tomorrow will be windy in all cities.\n"
                "Reporter: Have a nice day, everyone!"
            ),
            "tasks": [
                "What is the weather in Antalya?",
                "Which city is rainy?",
                "What will the weather be like tomorrow?",
            ],
        },
        5: {
            "title": "Life in the Past",
            "script": (
                "Narrator: Listen to Grandpa talk about the past.\n\n"
                "Grandpa: When I was young, there were no computers.\n"
                "Grandpa: We wrote letters to our friends.\n"
                "Grandpa: We listened to the radio, not TV.\n"
                "Grandpa: We walked to school every day.\n"
                "Grandpa: There were no mobile phones.\n"
                "Grandpa: Life was different, but it was good!"
            ),
            "tasks": [
                "Were there computers when Grandpa was young?",
                "How did Grandpa go to school?",
                "What did they listen to?",
            ],
        },
        6: {
            "title": "The School Concert",
            "script": (
                "Narrator: Listen and answer.\n\n"
                "Teacher: Our concert is on Friday at six o'clock.\n"
                "Teacher: Zehra will sing a folk song.\n"
                "Teacher: Can will play the drum.\n"
                "Teacher: Leo will play the guitar.\n"
                "Teacher: Mia will do a traditional dance.\n"
                "Teacher: Please invite your parents!"
            ),
            "tasks": [
                "When is the concert?",
                "What will Zehra do?",
                "What instrument will Leo play?",
            ],
        },
        7: {
            "title": "Planet Quiz",
            "script": (
                "Narrator: Listen to the quiz.\n\n"
                "Teacher: Question one: Which planet is closest to the Sun?\n"
                "Student: Mercury!\n"
                "Teacher: Correct! Question two: Which planet is red?\n"
                "Student: Mars!\n"
                "Teacher: Well done! Question three: Which planet has rings?\n"
                "Student: Saturn!\n"
                "Teacher: Excellent! Three out of three!"
            ),
            "tasks": [
                "Which planet is closest to the Sun?",
                "What colour is Mars?",
                "How many questions did the student answer correctly?",
            ],
        },
        8: {
            "title": "The School Nurse",
            "script": (
                "Narrator: Listen to the nurse.\n\n"
                "Nurse: Good morning, children! I am the school nurse.\n"
                "Nurse: Today I will talk about healthy habits.\n"
                "Nurse: First, wash your hands before meals.\n"
                "Nurse: Second, eat fruit and vegetables every day.\n"
                "Nurse: Third, brush your teeth twice a day.\n"
                "Nurse: Fourth, sleep at least nine hours.\n"
                "Nurse: If you do these things, you will be healthy!"
            ),
            "tasks": [
                "When should you wash your hands?",
                "How often should you brush your teeth?",
                "How many hours should you sleep?",
            ],
        },
        9: {
            "title": "The Story of Keloglan",
            "script": (
                "Narrator: Listen to the story.\n\n"
                "Storyteller: Long ago, there was a boy called Keloglan.\n"
                "Storyteller: He was bald and he was very clever.\n"
                "Storyteller: One day, a rich man tried to trick Keloglan.\n"
                "Storyteller: But Keloglan was too smart.\n"
                "Storyteller: He tricked the rich man instead!\n"
                "Storyteller: Everyone in the village laughed and cheered."
            ),
            "tasks": [
                "Who is Keloglan?",
                "Who tried to trick Keloglan?",
                "What happened at the end?",
            ],
        },
        10: {
            "title": "Our Year Together",
            "script": (
                "Narrator: Listen to the children talk about the year.\n\n"
                "Mia: This year was wonderful! I loved reading stories.\n"
                "Can: I liked the science projects best.\n"
                "Zehra: I loved the school concert.\n"
                "Leo: My favourite was learning about space.\n"
                "Mia: We learned so much together!\n"
                "All: Have a great summer, everyone!"
            ),
            "tasks": [
                "What did Mia love doing?",
                "What was Leo's favourite topic?",
                "What did the children say at the end?",
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 12. MODEL WRITING BANK  (10 entries)
# ---------------------------------------------------------------------------
MODEL_WRITING_BANK = {
    3: {
        1: {
            "type": "Description",
            "title": "My Best Friend",
            "text": (
                "My best friend is Ayse. She is nine years old. "
                "She has long black hair and brown eyes. "
                "She is kind and very funny. We play in the park after school. "
                "I am happy because Ayse is my friend."
            ),
            "focus": "Using adjectives to describe a person.",
        },
        2: {
            "type": "Directions",
            "title": "How to Get to the Library",
            "text": (
                "Go out of the school gate. Turn left. "
                "Go straight for two minutes. Turn right at the traffic lights. "
                "The library is on the left, next to the park. "
                "It is a big white building. You can't miss it!"
            ),
            "focus": "Using direction words: left, right, straight, next to.",
        },
        3: {
            "type": "Recipe",
            "title": "My Favourite Sandwich",
            "text": (
                "First, take two slices of bread. "
                "Then put some cheese on one slice. "
                "Next, add tomato and lettuce. "
                "After that, put the other slice on top. "
                "Finally, cut it in half. Enjoy your sandwich!"
            ),
            "focus": "Using sequence words: first, then, next, after that, finally.",
        },
        4: {
            "type": "Paragraph",
            "title": "My Favourite Season",
            "text": (
                "My favourite season is spring. The weather is warm and sunny. "
                "The flowers are beautiful. The birds sing in the trees. "
                "I play outside with my friends. "
                "I love spring because everything is green and happy."
            ),
            "focus": "Writing about preferences with reasons.",
        },
        5: {
            "type": "Comparison",
            "title": "Past and Present",
            "text": (
                "In the past, people rode horses. Now, we drive cars. "
                "In the past, people wrote letters. Now, we send messages. "
                "In the past, there was no TV. Now, we watch TV every day. "
                "Life was different in the past, but both times are interesting."
            ),
            "focus": "Comparing past and present with simple sentences.",
        },
        6: {
            "type": "Report",
            "title": "Our School Concert",
            "text": (
                "Our school had a concert on Friday. "
                "Zehra sang a beautiful song. Can played the drum. "
                "Leo played the guitar and Mia danced. "
                "The parents clapped and smiled. It was a great concert!"
            ),
            "focus": "Writing a simple report about a school event.",
        },
        7: {
            "type": "Fact File",
            "title": "Planet Earth",
            "text": (
                "Earth is the third planet from the Sun. "
                "It has water and air. It is the only planet with life. "
                "Earth has one Moon. It takes one year to go around the Sun. "
                "We must take care of our beautiful planet."
            ),
            "focus": "Writing factual information in short sentences.",
        },
        8: {
            "type": "Advice",
            "title": "How to Stay Healthy",
            "text": (
                "Do you want to be healthy? Here is my advice. "
                "Wash your hands with soap. Eat fruit and vegetables. "
                "Drink lots of water. Brush your teeth twice a day. "
                "Sleep well and play outside every day!"
            ),
            "focus": "Using imperative sentences to give advice.",
        },
        9: {
            "type": "Story Retell",
            "title": "The Story of Nasreddin Hodja",
            "text": (
                "One day, Hodja was riding his donkey backwards. "
                "People asked, 'Why are you sitting backwards?' "
                "Hodja said, 'I am not backwards. The donkey is!' "
                "Everyone laughed. Hodja was very clever and funny."
            ),
            "focus": "Retelling a short story in your own words.",
        },
        10: {
            "type": "Letter",
            "title": "A Letter to My Friend",
            "text": (
                "Dear Leo,\n"
                "Thank you for a wonderful year! I had so much fun. "
                "My favourite memory is the school concert. "
                "I hope you have a great summer. "
                "See you in September!\n"
                "Your friend,\nMia"
            ),
            "focus": "Writing a friendly letter with greeting and closing.",
        },
    },
}

# ---------------------------------------------------------------------------
# 13. PRONUNCIATION BANK  (10 entries)
# ---------------------------------------------------------------------------
PRONUNCIATION_BANK = {
    3: {
        1: {
            "focus": "/f/ vs /v/ sounds",
            "rule": "/f/ is voiceless (no vibration). /v/ is voiced (throat vibrates).",
            "examples": [("friend", "/frend/"), ("very", "/veri/"), ("fun", "/fan/"), ("village", "/vilij/")],
            "practice": ["friend", "five", "vine", "very", "fun"],
            "tongue_twister": "Five very funny friends flew to the village.",
        },
        2: {
            "focus": "/th/ sound (voiced: this, that)",
            "rule": "Put your tongue between your teeth and push air out.",
            "examples": [("this", "/dhis/"), ("that", "/dhat/"), ("there", "/dher/"), ("the", "/dhe/")],
            "practice": ["this", "that", "there", "the", "them"],
            "tongue_twister": "This is the thing that they think about.",
        },
        3: {
            "focus": "Short /i/ vs Long /i:/ (sit vs seat)",
            "rule": "Short /i/ is quick. Long /i:/ is stretched.",
            "examples": [("sit", "/sit/"), ("seat", "/si:t/"), ("ship", "/ship/"), ("sheep", "/shi:p/")],
            "practice": ["sit", "seat", "ship", "sheep", "his", "cheese"],
            "tongue_twister": "Six sheep sit on six cheap seats.",
        },
        4: {
            "focus": "Silent letters",
            "rule": "Some English words have letters you do not say.",
            "examples": [("know", "/no/"), ("write", "/rait/"), ("climb", "/klaim/"), ("island", "/ailand/")],
            "practice": ["know", "knee", "write", "wrong", "climb"],
            "tongue_twister": "I know the knight knelt on his knee.",
        },
        5: {
            "focus": "/w/ sound",
            "rule": "Round your lips and say /w/. It is like blowing out a candle.",
            "examples": [("water", "/woter/"), ("wind", "/wind/"), ("wash", "/wosh/"), ("week", "/wi:k/")],
            "practice": ["water", "wind", "weather", "was", "week"],
            "tongue_twister": "Will the wind wash the wet windows?",
        },
        6: {
            "focus": "/r/ vs /l/ sounds",
            "rule": "/r/: tongue does not touch. /l/: tongue touches the top of your mouth.",
            "examples": [("right", "/rait/"), ("light", "/lait/"), ("rain", "/rein/"), ("lane", "/lein/")],
            "practice": ["right", "light", "rain", "lane", "red", "led"],
            "tongue_twister": "Red lorry, yellow lorry, red lorry, yellow lorry.",
        },
        7: {
            "focus": "/s/ vs /sh/ sounds",
            "rule": "/s/ is sharp like a snake. /sh/ is soft like asking for quiet.",
            "examples": [("sun", "/san/"), ("ship", "/ship/"), ("star", "/star/"), ("she", "/shi:/")],
            "practice": ["sun", "ship", "star", "she", "sea", "shine"],
            "tongue_twister": "She sells shiny shells by the sea shore.",
        },
        8: {
            "focus": "/h/ sound",
            "rule": "Push air out from your throat. Like breathing on a mirror.",
            "examples": [("healthy", "/helthi/"), ("hand", "/hand/"), ("happy", "/hapi/"), ("help", "/help/")],
            "practice": ["healthy", "hand", "happy", "hot", "help"],
            "tongue_twister": "Harry's happy horse hops high on hills.",
        },
        9: {
            "focus": "Word stress (two-syllable words)",
            "rule": "One syllable is louder. HE-ro, not he-RO. LE-gend, not le-GEND.",
            "examples": [("hero", "/HE-ro/"), ("legend", "/LE-jend/"), ("clever", "/KLE-ver/"), ("story", "/STO-ri/")],
            "practice": ["hero", "legend", "clever", "story", "famous"],
            "tongue_twister": "The clever hero told a famous legend story.",
        },
        10: {
            "focus": "Linking words together",
            "rule": "When one word ends with a consonant and the next starts with a vowel, link them.",
            "examples": [("see you", "/si:yu/"), ("come in", "/kamin/"), ("good afternoon", "/gudaftenu:n/"), ("an apple", "/anapel/")],
            "practice": ["see you", "come in", "turn off", "pick up", "put on"],
            "tongue_twister": "Turn on an old orange lamp and sit on an arm chair.",
        },
    },
}

# ---------------------------------------------------------------------------
# 14. COMIC STRIP BANK  (10 entries, 4 panels each)
# ---------------------------------------------------------------------------
COMIC_STRIP_BANK = {
    3: {
        1: {
            "title": "The Kind Friend",
            "grammar_point": "Present Simple - be",
            "panels": [
                {"scene": "School yard. Leo looks sad, sitting alone.", "speech": "Leo: I am new. I am lonely.", "thought": "Leo thinks: 'I miss my friends in London.'"},
                {"scene": "Mia walks over with a big smile.", "speech": "Mia: Hi! I am Mia. Are you okay?", "thought": "Mia thinks: 'He looks sad.'"},
                {"scene": "Can and Zehra join them.", "speech": "Can: We are happy to meet you!", "thought": "Zehra thinks: 'He is nice!'"},
                {"scene": "They all sit together and laugh.", "speech": "Leo: You are very kind! I am happy now!", "thought": "Leo thinks: 'This school is great!'"},
            ],
            "your_turn": "Draw a comic about meeting a new friend. Use am, is, are.",
        },
        2: {
            "title": "Where Is the Park?",
            "grammar_point": "There is / There are + Directions",
            "panels": [
                {"scene": "Leo looks at a map, confused.", "speech": "Leo: Where is the park?", "thought": "Leo thinks: 'This map is hard!'"},
                {"scene": "Mia points to the map.", "speech": "Mia: There is a park next to the library.", "thought": "Mia thinks: 'I know this town well.'"},
                {"scene": "They walk past buildings.", "speech": "Mia: There are two shops on the left.", "thought": "Leo thinks: 'I can see them!'"},
                {"scene": "They arrive at the park.", "speech": "Leo: There it is! Thank you, Mia!", "thought": "Leo thinks: 'This town is nice!'"},
            ],
            "your_turn": "Draw a comic about finding a place. Use 'there is' and 'there are'.",
        },
        3: {
            "title": "The Food Fair",
            "grammar_point": "Some / Any",
            "panels": [
                {"scene": "A table full of food at school.", "speech": "Mr Demir: Do you have any food to share?", "thought": "Mr Demir thinks: 'This will be fun!'"},
                {"scene": "Mia puts baklava on the table.", "speech": "Mia: I have some baklava!", "thought": "Mia thinks: 'Everyone will love this!'"},
                {"scene": "Leo looks for his food.", "speech": "Leo: I don't have any food! I forgot!", "thought": "Leo thinks: 'Oh no!'"},
                {"scene": "Mia shares with Leo.", "speech": "Mia: Here, have some of mine!", "thought": "Leo thinks: 'She is so kind!'"},
            ],
            "your_turn": "Draw a comic about sharing food. Use 'some' and 'any'.",
        },
        4: {
            "title": "The Weather Surprise",
            "grammar_point": "Present Continuous",
            "panels": [
                {"scene": "Children in class. Sun shines outside.", "speech": "Can: Look! The sun is shining!", "thought": "Can thinks: 'Let us play outside!'"},
                {"scene": "Dark clouds appear quickly.", "speech": "Zehra: Oh no! It is raining now!", "thought": "Zehra thinks: 'The weather is changing!'"},
                {"scene": "Children grab umbrellas.", "speech": "Mia: I am opening my umbrella!", "thought": "Leo thinks: 'I am getting wet!'"},
                {"scene": "A rainbow appears.", "speech": "All: Look! A rainbow is appearing!", "thought": "Everyone thinks: 'Beautiful!'"},
            ],
            "your_turn": "Draw a comic about changing weather. Use -ing verbs.",
        },
        5: {
            "title": "Grandpa's Story",
            "grammar_point": "Past Simple - was / were",
            "panels": [
                {"scene": "Grandpa sits with the children.", "speech": "Grandpa: Life was very different in the past.", "thought": "Children think: 'Tell us more!'"},
                {"scene": "Grandpa holds an old photo.", "speech": "Grandpa: There were no phones. We were always outside.", "thought": "Can thinks: 'No phones?!'"},
                {"scene": "Children look surprised.", "speech": "Leo: Was it boring without TV?", "thought": "Leo thinks: 'I can't imagine!'"},
                {"scene": "Grandpa smiles.", "speech": "Grandpa: No! We were very happy playing games!", "thought": "Grandpa thinks: 'Good old days!'"},
            ],
            "your_turn": "Draw a comic about life in the past. Use was and were.",
        },
        6: {
            "title": "The Talent Show",
            "grammar_point": "Can / Can't",
            "panels": [
                {"scene": "Mr Demir announces the talent show.", "speech": "Mr Demir: What can you do for the show?", "thought": "Mr Demir thinks: 'So many talents!'"},
                {"scene": "Zehra raises her hand.", "speech": "Zehra: I can sing! But I can't play the guitar.", "thought": "Zehra thinks: 'I love singing!'"},
                {"scene": "Can raises his hand.", "speech": "Can: I can play the drum!", "thought": "Can thinks: 'Boom boom!'"},
                {"scene": "Leo looks shy.", "speech": "Leo: I can't dance, but I can play the guitar!", "thought": "Leo thinks: 'I will try my best!'"},
            ],
            "your_turn": "Draw a comic about your talents. Use can and can't.",
        },
        7: {
            "title": "Space Adventure",
            "grammar_point": "Prepositions of Place",
            "panels": [
                {"scene": "Children look at a space poster.", "speech": "Can: Earth is between Venus and Mars.", "thought": "Can thinks: 'Space is cool!'"},
                {"scene": "Zehra points at the Sun.", "speech": "Zehra: The Sun is in the centre.", "thought": "Zehra thinks: 'It is so big!'"},
                {"scene": "Mia finds Saturn.", "speech": "Mia: Saturn is next to Jupiter.", "thought": "Mia thinks: 'I love the rings!'"},
                {"scene": "Leo pretends to be an astronaut.", "speech": "Leo: I am on the Moon! Under the stars!", "thought": "Leo thinks: 'One day!'"},
            ],
            "your_turn": "Draw the planets and write where they are. Use in, on, next to, between.",
        },
        8: {
            "title": "The Germ Monster",
            "grammar_point": "Imperatives",
            "panels": [
                {"scene": "A cartoon germ monster appears.", "speech": "Germ: Ha ha! I am on your hands!", "thought": "Germ thinks: 'They can't see me!'"},
                {"scene": "The nurse arrives.", "speech": "Nurse: Wash your hands with soap!", "thought": "Nurse thinks: 'We must stop the germs!'"},
                {"scene": "Children wash their hands.", "speech": "Children: Don't touch your face!", "thought": "Germ thinks: 'Oh no! Soap!'"},
                {"scene": "The germ monster disappears.", "speech": "Nurse: Good job! Eat healthy food! Stay clean!", "thought": "Children think: 'We won!'"},
            ],
            "your_turn": "Draw a comic about fighting germs. Use imperative sentences.",
        },
        9: {
            "title": "Keloglan's Trick",
            "grammar_point": "Past Simple - Regular Verbs",
            "panels": [
                {"scene": "A giant arrives at the village.", "speech": "Giant: I want all your food!", "thought": "Villagers think: 'Help!'"},
                {"scene": "Keloglan walks up calmly.", "speech": "Keloglan: I have a riddle for you.", "thought": "Keloglan thinks: 'I have a plan.'"},
                {"scene": "The giant looks confused.", "speech": "Giant: I... I don't know the answer!", "thought": "Giant thinks: 'This boy tricked me!'"},
                {"scene": "The giant runs away. People cheer.", "speech": "Villagers: Keloglan saved us! We thanked him!", "thought": "Keloglan thinks: 'Brains beat muscles!'"},
            ],
            "your_turn": "Draw a folk tale comic. Use past tense verbs with -ed.",
        },
        10: {
            "title": "The Best Year Ever",
            "grammar_point": "Comparatives",
            "panels": [
                {"scene": "Last day of school. Children chat.", "speech": "Mia: This year was better than last year!", "thought": "Mia thinks: 'So many memories!'"},
                {"scene": "Leo holds his report card.", "speech": "Leo: My English is stronger than before!", "thought": "Leo thinks: 'I worked hard!'"},
                {"scene": "Can shows his projects.", "speech": "Can: This project is bigger than my first one!", "thought": "Can thinks: 'I improved so much!'"},
                {"scene": "Group hug.", "speech": "Zehra: Friends are more important than anything!", "thought": "Everyone thinks: 'Best friends forever!'"},
            ],
            "your_turn": "Draw a comic comparing this year to last year. Use comparatives.",
        },
    },
}

# ---------------------------------------------------------------------------
# 15. WORKBOOK BANK  (10 entries, exercises list)
# ---------------------------------------------------------------------------
WORKBOOK_BANK = {
    3: {
        1: {
            "exercises": [
                {"type": "match", "instr": "Match the emotion to the face.", "items": [("happy", "smiling face"), ("sad", "crying face"), ("angry", "red face"), ("scared", "shaking face"), ("excited", "jumping face")]},
                {"type": "fill", "instr": "Fill in the blanks with am, is, or are.", "items": ["I ___ happy today.", "She ___ my friend.", "We ___ in the same class.", "He ___ from London.", "They ___ very kind."]},
                {"type": "write", "instr": "Write three sentences about your best friend.", "items": ["My best friend is ___.", "He/She is ___ and ___.", "We like to ___ together."]},
                {"type": "circle", "instr": "Circle the correct word.", "items": ["She is (kind / unkind) to everyone.", "I (am / is) nine years old.", "They (is / are) my friends."]},
                {"type": "draw", "instr": "Draw your best friend and write their name.", "items": ["Draw here.", "Name: ___", "Age: ___"]},
            ],
        },
        2: {
            "exercises": [
                {"type": "match", "instr": "Match the building to its picture.", "items": [("hospital", "red cross building"), ("library", "books building"), ("school", "flag building"), ("bakery", "bread building"), ("park", "trees and bench")]},
                {"type": "fill", "instr": "Fill in with there is or there are.", "items": ["___ a park in our town.", "___ three schools.", "___ a library next to the park.", "___ many shops.", "___ a hospital behind the school."]},
                {"type": "trace", "instr": "Trace the route on the map from school to the library.", "items": ["Start at the school.", "Go straight.", "Turn left.", "The library is on the right."]},
                {"type": "write", "instr": "Write directions from your house to your school.", "items": ["Go ___.", "Turn ___.", "My school is ___."]},
                {"type": "circle", "instr": "Circle the preposition.", "items": ["The bank is (next to / under) the shop.", "The school is (behind / inside) the park.", "The library is (between / above) the bank and the post office."]},
            ],
        },
        3: {
            "exercises": [
                {"type": "match", "instr": "Match the food to the country.", "items": [("pizza", "Italy"), ("fish and chips", "England"), ("sushi", "Japan"), ("baklava", "Turkey"), ("tacos", "Mexico")]},
                {"type": "fill", "instr": "Fill in with some or any.", "items": ["I have ___ apples.", "Do you have ___ bread?", "There isn't ___ milk.", "Can I have ___ water?", "She has ___ cheese."]},
                {"type": "order", "instr": "Put the recipe steps in order.", "items": ["__ Add cheese on top.", "__ Make the dough.", "__ Bake in the oven.", "__ Put tomato sauce.", "__ Eat and enjoy!"]},
                {"type": "write", "instr": "Write your favourite recipe.", "items": ["My favourite food is ___.", "First, ___.", "Then, ___.", "Finally, ___."]},
                {"type": "circle", "instr": "Circle the healthy food.", "items": ["(apple / cake)", "(water / fizzy drink)", "(carrot / candy)", "(rice / chips)", "(fish / ice cream)"]},
            ],
        },
        4: {
            "exercises": [
                {"type": "match", "instr": "Match the weather to the picture.", "items": [("sunny", "sun icon"), ("rainy", "rain drops"), ("cloudy", "grey cloud"), ("windy", "blowing trees"), ("snowy", "snowflakes")]},
                {"type": "fill", "instr": "Fill in with the present continuous.", "items": ["It ___ (rain) now.", "The sun ___ (shine) today.", "We ___ (plant) trees.", "She ___ (recycle) paper.", "They ___ (clean) the park."]},
                {"type": "sort", "instr": "Sort into Recycle / Do Not Recycle.", "items": ["paper (Recycle)", "banana peel (Do Not Recycle)", "plastic bottle (Recycle)", "glass jar (Recycle)", "food waste (Do Not Recycle)"]},
                {"type": "write", "instr": "Write about your favourite season.", "items": ["My favourite season is ___.", "The weather is ___.", "I like it because ___."]},
                {"type": "draw", "instr": "Draw today's weather and write a sentence.", "items": ["Today is ___.", "I can see ___."]},
            ],
        },
        5: {
            "exercises": [
                {"type": "match", "instr": "Match the invention to the time.", "items": [("candle", "Past"), ("light bulb", "Present"), ("horse", "Past"), ("car", "Present"), ("letter", "Past")]},
                {"type": "fill", "instr": "Fill in with was or were.", "items": ["There ___ no computers.", "Life ___ different.", "People ___ happy.", "The telephone ___ very big.", "There ___ no planes."]},
                {"type": "compare", "instr": "Write Past or Present.", "items": ["Mobile phone: ___", "Horse and cart: ___", "E-mail: ___", "Handwritten letter: ___", "Television: ___"]},
                {"type": "write", "instr": "Compare past and present.", "items": ["In the past, people ___.", "Now, people ___.", "I think ___ is better because ___."]},
                {"type": "circle", "instr": "Circle the old invention.", "items": ["(candle / lamp)", "(horse / car)", "(pen / computer)", "(radio / TV)", "(map / GPS)"]},
            ],
        },
        6: {
            "exercises": [
                {"type": "match", "instr": "Match the instrument to its type.", "items": [("guitar", "string"), ("drum", "percussion"), ("flute", "wind"), ("piano", "keyboard"), ("saz", "string")]},
                {"type": "fill", "instr": "Fill in with can or can't.", "items": ["She ___ sing very well.", "I ___ play the drum. It is hard.", "He ___ play the guitar.", "We ___ dance. We love dancing!", "___ you play an instrument?"]},
                {"type": "sort", "instr": "Sort: String / Wind / Percussion.", "items": ["guitar (String)", "flute (Wind)", "drum (Percussion)", "violin (String)", "trumpet (Wind)"]},
                {"type": "write", "instr": "Write about music.", "items": ["I can play ___.", "I can't play ___.", "My favourite music is ___."]},
                {"type": "draw", "instr": "Draw your favourite instrument and label it.", "items": ["Instrument: ___", "Type: ___"]},
            ],
        },
        7: {
            "exercises": [
                {"type": "match", "instr": "Match the planet to the description.", "items": [("Mercury", "closest to the Sun"), ("Earth", "has water and air"), ("Mars", "the red planet"), ("Jupiter", "the biggest planet"), ("Saturn", "has rings")]},
                {"type": "fill", "instr": "Fill in with the correct preposition.", "items": ["Earth is ___ Venus and Mars.", "The Moon goes ___ Earth.", "Stars are ___ the sky.", "The Sun is ___ the centre.", "We live ___ Earth."]},
                {"type": "order", "instr": "Put the planets in order from the Sun.", "items": ["__ Earth", "__ Mercury", "__ Venus", "__ Mars", "__ Jupiter"]},
                {"type": "write", "instr": "Write three facts about a planet.", "items": ["Planet: ___", "It is ___.", "It has ___."]},
                {"type": "tf", "instr": "True or False?", "items": ["The Sun is a planet. (___)", "Earth has two moons. (___)", "Mars is red. (___)", "Jupiter is the smallest planet. (___)", "Saturn has rings. (___)"]},
            ],
        },
        8: {
            "exercises": [
                {"type": "match", "instr": "Match the healthy habit to the picture.", "items": [("wash hands", "soap and water"), ("brush teeth", "toothbrush"), ("eat fruit", "apple"), ("drink water", "glass of water"), ("sleep well", "bed")]},
                {"type": "fill", "instr": "Complete with the imperative.", "items": ["___ your hands before meals. (Wash)", "___ eat too much sugar. (Don't)", "___ your teeth twice a day. (Brush)", "___ lots of water. (Drink)", "___ outside every day. (Play)"]},
                {"type": "sort", "instr": "Sort: Healthy / Unhealthy.", "items": ["eat fruit (Healthy)", "eat candy every day (Unhealthy)", "drink water (Healthy)", "sleep four hours (Unhealthy)", "exercise (Healthy)"]},
                {"type": "write", "instr": "Write five healthy rules.", "items": ["1. ___", "2. ___", "3. ___", "4. ___", "5. ___"]},
                {"type": "circle", "instr": "Circle the healthy choice.", "items": ["(water / cola)", "(apple / chips)", "(sleep early / stay up late)", "(play outside / watch TV all day)", "(wash hands / don't wash hands)"]},
            ],
        },
        9: {
            "exercises": [
                {"type": "match", "instr": "Match the character to the story.", "items": [("Keloglan", "Turkish folk tale"), ("Robin Hood", "English legend"), ("Hodja", "Turkish folk tale"), ("Pippi", "Swedish story"), ("Anansi", "African folk tale")]},
                {"type": "fill", "instr": "Fill in with the past tense.", "items": ["Keloglan ___ the giant. (tricked)", "The villagers ___ Keloglan. (thanked)", "The giant ___ away. (walked)", "Everyone ___ and cheered. (laughed)", "He ___ in a small village. (lived)"]},
                {"type": "order", "instr": "Put the story in order.", "items": ["__ The giant left the village.", "__ A giant came to the village.", "__ Keloglan told a riddle.", "__ Everyone was afraid.", "__ The villagers thanked Keloglan."]},
                {"type": "write", "instr": "Write a short folk tale.", "items": ["Once upon a time, ___.", "One day, ___.", "In the end, ___."]},
                {"type": "draw", "instr": "Draw your favourite folk hero.", "items": ["Name: ___", "From: ___", "He/She is ___."]},
            ],
        },
        10: {
            "exercises": [
                {"type": "match", "instr": "Match the memory to the unit.", "items": [("Friends", "Unit 1"), ("City Map", "Unit 2"), ("World Food", "Unit 3"), ("Weather", "Unit 4"), ("Space", "Unit 7")]},
                {"type": "fill", "instr": "Fill in with comparatives.", "items": ["This year was ___ than last year. (better)", "My English is ___ now. (stronger)", "I am ___ than before. (taller)", "The show was ___ than expected. (bigger)", "Friends are ___ than anything. (more important)"]},
                {"type": "rate", "instr": "Rate each unit: Loved it / Liked it / It was okay.", "items": ["Friends & Feelings: ___", "Our City: ___", "Food: ___", "Space: ___", "Legends: ___"]},
                {"type": "write", "instr": "Write a letter to next year's class.", "items": ["Dear new students,", "This year you will learn about ___.", "My favourite unit was ___.", "Have a great year!"]},
                {"type": "draw", "instr": "Draw your best memory from this year.", "items": ["My best memory is ___.", "It was in Unit ___."]},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 16. MISSION BANK  (10 missions)
# ---------------------------------------------------------------------------
MISSION_BANK = {
    3: {
        1: {
            "title": "Friendship Ambassador",
            "mission": "Say hello to three new people today. Learn their names and one thing they like.",
            "evidence": "Write their names and what they like in your notebook.",
            "xp": 20,
            "difficulty": "easy",
        },
        2: {
            "title": "City Explorer",
            "mission": "Walk around your neighbourhood. Find five buildings and write their English names.",
            "evidence": "Take photos or draw the buildings with English labels.",
            "xp": 25,
            "difficulty": "medium",
        },
        3: {
            "title": "World Chef",
            "mission": "Find a recipe from another country. Write the ingredients in English.",
            "evidence": "Bring the recipe to class with the English ingredient list.",
            "xp": 25,
            "difficulty": "medium",
        },
        4: {
            "title": "Eco Warrior",
            "mission": "Recycle five items at home this week. Sort them by type.",
            "evidence": "Take a photo of your sorted recycling bins.",
            "xp": 30,
            "difficulty": "medium",
        },
        5: {
            "title": "Time Traveller",
            "mission": "Interview a grandparent about life in the past. Write five differences.",
            "evidence": "Write five sentences: In the past... Now...",
            "xp": 30,
            "difficulty": "medium",
        },
        6: {
            "title": "Music Star",
            "mission": "Learn an English song by heart and sing it to your family.",
            "evidence": "Record a video or get a parent signature.",
            "xp": 25,
            "difficulty": "easy",
        },
        7: {
            "title": "Space Detective",
            "mission": "Find three facts about a planet and share them with the class.",
            "evidence": "Write a fact card with the planet name and three facts.",
            "xp": 30,
            "difficulty": "medium",
        },
        8: {
            "title": "Health Inspector",
            "mission": "Follow all six healthy habits for one week. Check them off each day.",
            "evidence": "Complete a weekly health checklist.",
            "xp": 35,
            "difficulty": "hard",
        },
        9: {
            "title": "Story Keeper",
            "mission": "Ask a family member to tell you a folk tale. Retell it in English.",
            "evidence": "Write the story in your own words (6-8 sentences).",
            "xp": 35,
            "difficulty": "hard",
        },
        10: {
            "title": "Memory Maker",
            "mission": "Create a memory page about this year with drawings and sentences.",
            "evidence": "Bring your memory page to the last class.",
            "xp": 30,
            "difficulty": "medium",
        },
    },
}

# ---------------------------------------------------------------------------
# 17. FAMILY CORNER BANK  (10 entries)
# ---------------------------------------------------------------------------
FAMILY_CORNER_BANK = {
    3: {
        1: {
            "title": "Friendship at Home",
            "activity": "Talk about friendship with your child. Who are their friends?",
            "together": "Draw a picture of your child and their best friend together. Write three adjectives in English.",
            "parent_question": "Who was your best friend when you were a child?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        2: {
            "title": "Our Neighbourhood Walk",
            "activity": "Walk around your neighbourhood with your child.",
            "together": "Find five buildings and say their English names: school, hospital, shop, mosque, park.",
            "parent_question": "What is your favourite place in your neighbourhood?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        3: {
            "title": "Cook Together",
            "activity": "Cook a simple meal with your child.",
            "together": "Say the ingredients in English while cooking. Write the recipe together.",
            "parent_question": "What is your child's favourite food?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        4: {
            "title": "Nature Walk",
            "activity": "Go for a walk in a park or garden.",
            "together": "Find five things in nature and say them in English: tree, flower, bird, cloud, leaf.",
            "parent_question": "What season do you like best? Tell your child in English!",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        5: {
            "title": "Old Photos Night",
            "activity": "Look at old family photos together.",
            "together": "Talk about how life was different in the past. Write three differences in English.",
            "parent_question": "What technology did you not have when you were young?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        6: {
            "title": "Family Music Time",
            "activity": "Listen to different types of music together.",
            "together": "Dance and sing to an English song. Try to learn the words together.",
            "parent_question": "What is your favourite song? Can you say the name in English?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        7: {
            "title": "Stargazing Night",
            "activity": "Look at the night sky together on a clear night.",
            "together": "Try to find the Moon, a planet and a star. Say their English names.",
            "parent_question": "Did you ever look at the stars when you were young?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        8: {
            "title": "Healthy Habits Check",
            "activity": "Review healthy habits with your child.",
            "together": "Make a family health chart. Check off: wash hands, eat fruit, drink water, sleep early.",
            "parent_question": "What healthy habit does your family do well?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        9: {
            "title": "Story Time",
            "activity": "Tell your child a folk tale or legend from your family's culture.",
            "together": "Help your child retell the story in simple English sentences.",
            "parent_question": "What is your favourite story from your childhood?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
        10: {
            "title": "Year in Review",
            "activity": "Talk about what your child learned this year in English class.",
            "together": "Write a 'Thank You' card in English to your child's teacher.",
            "parent_question": "What are you most proud of about your child this year?",
            "signature": "Parent/Guardian: ___  Date: ___",
        },
    },
}

# ---------------------------------------------------------------------------
# 18. GAMIFICATION BANK  (levels, 10 badges, bonus XP)
# ---------------------------------------------------------------------------
GAMIFICATION_BANK = {
    3: {
        "levels": [
            {"name": "Beginner Explorer", "xp_min": 0, "xp_max": 49, "icon": "🌱"},
            {"name": "Rising Star", "xp_min": 50, "xp_max": 149, "icon": "⭐"},
            {"name": "Knowledge Knight", "xp_min": 150, "xp_max": 299, "icon": "🛡️"},
            {"name": "Word Wizard", "xp_min": 300, "xp_max": 449, "icon": "🧙"},
            {"name": "English Champion", "xp_min": 450, "xp_max": 600, "icon": "🏆"},
        ],
        "unit_badges": {
            1: {"badge": "Friendship Star", "desc": "Describe three friends using English adjectives!", "xp": 20},
            2: {"badge": "City Navigator", "desc": "Give directions to three places in English!", "xp": 25},
            3: {"badge": "World Foodie", "desc": "Name five foods from five different countries!", "xp": 25},
            4: {"badge": "Eco Hero", "desc": "Explain three ways to help the planet in English!", "xp": 30},
            5: {"badge": "Time Traveller", "desc": "Compare five things from past and present!", "xp": 25},
            6: {"badge": "Music Maestro", "desc": "Name five instruments and say what you can play!", "xp": 25},
            7: {"badge": "Space Cadet", "desc": "Name all eight planets in order!", "xp": 30},
            8: {"badge": "Health Champion", "desc": "List six healthy habits in English!", "xp": 25},
            9: {"badge": "Legend Keeper", "desc": "Retell a folk tale in English with past tense!", "xp": 30},
            10: {"badge": "Year Champion", "desc": "Complete all missions and the end of year show!", "xp": 35},
        },
        "bonus_xp": [
            {"action": "Read an English book at home", "xp": 15},
            {"action": "Write a diary entry in English", "xp": 15},
            {"action": "Teach a family member five English words", "xp": 10},
            {"action": "Complete all workbook exercises for a unit", "xp": 20},
            {"action": "Present a project to the class in English", "xp": 20},
        ],
    },
}

# ---------------------------------------------------------------------------
# 19. FUN FACTS BANK  (10 x 3 facts)
# ---------------------------------------------------------------------------
FUN_FACTS_BANK = {
    3: {
        1: [
            "Dolphins call each other by name!",
            "Smiling uses 17 muscles but frowning uses 43!",
            "A group of friends is called a 'crew' or a 'squad'!",
        ],
        2: [
            "Tokyo is the biggest city in the world!",
            "Venice in Italy has canals instead of streets!",
            "The oldest city in the world is Damascus in Syria!",
        ],
        3: [
            "People eat about 35 tonnes of food in a lifetime!",
            "Honey never goes bad - it lasts forever!",
            "The most popular food in the world is rice!",
        ],
        4: [
            "Lightning is five times hotter than the Sun's surface!",
            "A cloud can weigh as much as 100 elephants!",
            "One tree can produce enough oxygen for two people!",
        ],
        5: [
            "The first computer was as big as a room!",
            "The internet was invented for scientists to share information!",
            "Yoghurt is a Turkish word used all over the world!",
        ],
        6: [
            "Music can make plants grow faster!",
            "The oldest instrument is a flute made from bone!",
            "Cows give more milk when they listen to slow music!",
        ],
        7: [
            "The Sun is so big that one million Earths could fit inside!",
            "A day on Venus is longer than a year on Venus!",
            "Footprints on the Moon will stay for millions of years!",
        ],
        8: [
            "Your body has about 206 bones!",
            "You use 200 muscles to take one step!",
            "Your nose can remember 50,000 different smells!",
        ],
        9: [
            "The word 'legend' comes from Latin and means 'to read'!",
            "Nasreddin Hodja stories are told in over 50 countries!",
            "The oldest fairy tale is over 6,000 years old!",
        ],
        10: [
            "The average person laughs 15 times a day!",
            "Your brain is more active when you sleep than when you watch TV!",
            "Children ask about 300 questions a day!",
        ],
    },
}

# ---------------------------------------------------------------------------
# PROGRESS CHECK BANK  (Review questions per unit, ages 8-9, A1 CEFR)
# ---------------------------------------------------------------------------
PROGRESS_CHECK_BANK = {
    3: {
        1: {
            "vocab": ["friend", "kind", "shy", "happy", "sad", "angry", "excited", "worried", "brave", "share"],
            "grammar": ["I feel ___ today.", "She is ___ because ___.", "Are you happy or sad?", "He feels ___ when ___."],
            "reading": ["How does Leo feel on his first day?", "Who gives Leo a drawing?", "Why is Mia kind?"],
            "writing": ["Write about your best friend (3 sentences).", "Describe how you feel today and why."],
        },
        2: {
            "vocab": ["city", "map", "museum", "cinema", "restaurant", "bridge", "square", "straight", "opposite", "corner"],
            "grammar": ["Go straight and turn ___.", "The museum is ___ the park.", "Where is the ___?", "It is on ___ Street."],
            "reading": ["Where is the cinema?", "How do you get to the museum?", "What is in the town square?"],
            "writing": ["Write directions from your house to school.", "Describe your town in four sentences."],
        },
        3: {
            "vocab": ["pizza", "sushi", "curry", "chocolate", "spicy", "sweet", "sour", "recipe", "ingredient", "traditional"],
            "grammar": ["I would like some ___.", "She prefers ___ to ___.", "What is your favourite food?", "It tastes ___."],
            "reading": ["Where does pizza come from?", "What ingredients are in the recipe?", "Is curry sweet or spicy?"],
            "writing": ["Write your favourite recipe (ingredients and steps).", "Describe a meal from another country."],
        },
        4: {
            "vocab": ["planet", "recycle", "pollution", "forest", "ocean", "endangered", "protect", "climate", "solar", "waste"],
            "grammar": ["We should ___ to help the planet.", "We must not ___.", "If we recycle, we ___.", "The Earth needs ___."],
            "reading": ["Why should we recycle?", "What animals are endangered?", "How can we save water?"],
            "writing": ["Write three ways to protect the environment.", "Make a poster message about saving trees."],
        },
        5: {
            "vocab": ["telephone", "computer", "electricity", "inventor", "robot", "machine", "screen", "battery", "discover", "future"],
            "grammar": ["___ was invented by ___.", "In the past, people ___.", "In the future, we will ___.", "It was invented in ___."],
            "reading": ["Who invented the telephone?", "How did people communicate before phones?", "What will robots do in the future?"],
            "writing": ["Describe an invention you would like to create.", "Write about how technology helps us at school."],
        },
        6: {
            "vocab": ["guitar", "piano", "drums", "painting", "sculpture", "gallery", "performance", "concert", "rhythm", "melody"],
            "grammar": ["I can play the ___.", "She enjoys ___ing.", "What instrument do you play?", "The concert was ___."],
            "reading": ["What instruments are in the story?", "Who plays the guitar?", "When is the school concert?"],
            "writing": ["Write about your favourite type of art or music.", "Describe a concert or show you watched."],
        },
        7: {
            "vocab": ["star", "moon", "planet", "astronaut", "rocket", "solar system", "telescope", "orbit", "gravity", "explore"],
            "grammar": ["The Moon orbits the ___.", "There are ___ planets.", "An astronaut is a person who ___.", "Mars is ___ than Earth."],
            "reading": ["How many planets are in the solar system?", "What does an astronaut do?", "Which planet is the biggest?"],
            "writing": ["Write a diary entry as an astronaut in space.", "Describe the solar system in four sentences."],
        },
        8: {
            "vocab": ["healthy", "exercise", "hygiene", "germs", "vitamins", "toothbrush", "soap", "medicine", "rest", "balanced"],
            "grammar": ["You should ___ every day.", "You shouldn't ___.", "To stay healthy, we must ___.", "How often do you ___?"],
            "reading": ["Why is exercise important?", "How do germs spread?", "What is a balanced diet?"],
            "writing": ["Write five healthy habits.", "Create a daily health routine for a student."],
        },
        9: {
            "vocab": ["legend", "tale", "hero", "giant", "wise", "trick", "village", "once upon a time", "moral", "character"],
            "grammar": ["Once upon a time, there was ___.", "The hero ___ the giant.", "The moral of the story is ___.", "Long ago, people ___."],
            "reading": ["Who is the hero of the story?", "What trick does Nasreddin Hodja play?", "What is the moral?"],
            "writing": ["Retell a folk tale in your own words.", "Write a short legend with a moral."],
        },
        10: {
            "vocab": ["show", "performance", "audience", "stage", "memory", "certificate", "speech", "applause", "proud", "celebrate"],
            "grammar": ["This year I learned ___.", "My favourite memory is ___.", "I am proud because ___.", "Next year I want to ___."],
            "reading": ["What do the students perform at the show?", "Who gives the speech?", "What is Mia's best memory?"],
            "writing": ["Write about your best school memory this year.", "Write a short thank-you speech for your teacher."],
        },
    },
}

# ============================================================================
# ESCAPE ROOM BANK - Grade 3
# ============================================================================
ESCAPE_ROOM_BANK = {
    3: {
        1: {
            "title": "Escape from the Classroom!",
            "story": "Oh no! The classroom door is locked! Solve 5 puzzles to find the code and get out!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: L-L-E-H-O. What word is it?", "answer": "HELLO", "hint": "You say this when you meet someone."},
                {"type": "grammar", "question": "Fill in: 'My name ___ Ali.' (am / is / are)", "answer": "is", "hint": "Use 'is' with he, she, it, or a name."},
                {"type": "reading", "question": "Read: 'Hi! I am Zeynep. I am 8.' How old is Zeynep?", "answer": "8", "hint": "Look at the number after 'I am'."},
                {"type": "maths", "question": "How many letters are in the word 'GOODBYE'?", "answer": "7", "hint": "Count each letter: G-O-O-D-B-Y-E."},
                {"type": "riddle", "question": "I am the first thing you say in the morning to your teacher. What am I?", "answer": "Good morning", "hint": "Good ___!"},
            ],
            "final_code": "HELLO-is-8-7-MORNING",
            "reward": "You escaped! +40 XP! Badge: Classroom Escape Artist"
        },
        2: {
            "title": "Escape from the Family House!",
            "story": "You are visiting a big family house but the gate is locked! Answer 5 puzzles to open it!",
            "puzzles": [
                {"type": "vocabulary", "question": "Who is your mother's mother?", "answer": "grandmother", "hint": "Grand + mother."},
                {"type": "grammar", "question": "Fill in: 'She ___ my sister.' (am / is / are)", "answer": "is", "hint": "'She' uses 'is'."},
                {"type": "reading", "question": "Read: 'This is my father. His name is Ahmet.' What is the father's name?", "answer": "Ahmet", "hint": "Look after 'His name is'."},
                {"type": "maths", "question": "I have 2 brothers and 1 sister. How many siblings do I have?", "answer": "3", "hint": "2 + 1 = ?"},
                {"type": "riddle", "question": "I am your parents' son, but I am not you. Who am I?", "answer": "brother", "hint": "A boy in your family."},
            ],
            "final_code": "GRANDMOTHER-is-AHMET-3-BROTHER",
            "reward": "You escaped! +40 XP! Badge: Family House Explorer"
        },
        3: {
            "title": "Escape from the Haunted House!",
            "story": "You are trapped in a spooky house! Solve 5 puzzles to find the key and run outside!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: C-K-I-T-H-E-N. What room is it?", "answer": "KITCHEN", "hint": "You cook food here."},
                {"type": "grammar", "question": "Fill in: 'There ___ a sofa in the living room.' (is / are)", "answer": "is", "hint": "'A sofa' is one thing, so use 'is'."},
                {"type": "reading", "question": "Read: 'My bedroom is big. There is a bed and a desk.' What is in the bedroom?", "answer": "a bed and a desk", "hint": "Look after 'There is'."},
                {"type": "maths", "question": "The house has 3 bedrooms, 1 kitchen, and 2 bathrooms. How many rooms?", "answer": "6", "hint": "3 + 1 + 2 = ?"},
                {"type": "riddle", "question": "I have a door and windows but I am not a car. What am I?", "answer": "house", "hint": "People live in me."},
            ],
            "final_code": "KITCHEN-is-BED-6-HOUSE",
            "reward": "You escaped! +40 XP! Badge: Haunted House Survivor"
        },
        4: {
            "title": "Escape from the Toy Factory!",
            "story": "You are locked inside a toy factory! Solve 5 puzzles to start the machine and open the door!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: L-O-D-L. What toy is it?", "answer": "DOLL", "hint": "A toy that looks like a small person."},
                {"type": "grammar", "question": "Fill in: 'I ___ a teddy bear.' (have / has)", "answer": "have", "hint": "'I' always goes with 'have'."},
                {"type": "reading", "question": "Read: 'Can I play with your ball? Yes, you can!' Can you play with the ball?", "answer": "Yes", "hint": "Look at the answer in the text."},
                {"type": "maths", "question": "You have 4 toy cars and get 3 more. How many toy cars do you have?", "answer": "7", "hint": "4 + 3 = ?"},
                {"type": "riddle", "question": "I am round and you kick me. What am I?", "answer": "ball", "hint": "A toy you play with outside."},
            ],
            "final_code": "DOLL-have-YES-7-BALL",
            "reward": "You escaped! +40 XP! Badge: Toy Factory Master"
        },
        5: {
            "title": "Escape from the Hospital!",
            "story": "The hospital doors are stuck! Solve 5 health puzzles to call for help and get out!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: E-A-H-D. What body part is it?", "answer": "HEAD", "hint": "It is on top of your body."},
                {"type": "grammar", "question": "Fill in: 'I ___ a headache.' (have / has)", "answer": "have", "hint": "'I' goes with 'have'."},
                {"type": "reading", "question": "Read: 'Wash your hands before eating.' What should you wash?", "answer": "hands", "hint": "Look after 'Wash your'."},
                {"type": "maths", "question": "You have 2 hands. Each hand has 5 fingers. How many fingers in total?", "answer": "10", "hint": "2 × 5 = ?"},
                {"type": "riddle", "question": "I help you see but I am not a window. What am I?", "answer": "eyes", "hint": "You have two of them on your face."},
            ],
            "final_code": "HEAD-have-HANDS-10-EYES",
            "reward": "You escaped! +40 XP! Badge: Hospital Hero"
        },
        6: {
            "title": "Escape from the Fashion Show!",
            "story": "You are backstage at a fashion show and the exit is locked! Solve 5 puzzles to find the way out!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: S-S-E-D-R. What is it?", "answer": "DRESS", "hint": "Girls often wear this."},
                {"type": "grammar", "question": "Fill in: 'She ___ wearing a hat.' (is / are)", "answer": "is", "hint": "'She' goes with 'is'."},
                {"type": "reading", "question": "Read: 'Put on your jacket. It is cold outside.' Why do you need a jacket?", "answer": "It is cold", "hint": "Look at the second sentence."},
                {"type": "maths", "question": "You have 2 shoes, 3 t-shirts, and 1 hat. How many clothes in total?", "answer": "6", "hint": "2 + 3 + 1 = ?"},
                {"type": "riddle", "question": "I keep your feet warm. You wear two of me. What am I?", "answer": "socks", "hint": "You wear them inside your shoes."},
            ],
            "final_code": "DRESS-is-COLD-6-SOCKS",
            "reward": "You escaped! +40 XP! Badge: Fashion Show Star"
        },
        7: {
            "title": "Escape from the Zoo!",
            "story": "The zoo gates are closed! Solve 5 animal puzzles to find the secret exit!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: P-H-E-L-A-N-E-T. What animal is it?", "answer": "ELEPHANT", "hint": "The biggest land animal with a long trunk."},
                {"type": "grammar", "question": "Fill in: 'Cats ___ four legs.' (have / has)", "answer": "have", "hint": "'Cats' is plural, so use 'have'."},
                {"type": "reading", "question": "Read: 'The parrot is green. It can fly and talk.' What can the parrot do?", "answer": "fly and talk", "hint": "Look after 'It can'."},
                {"type": "maths", "question": "There are 3 lions and 4 monkeys in the zoo. How many animals?", "answer": "7", "hint": "3 + 4 = ?"},
                {"type": "riddle", "question": "I am black and white and I eat bamboo. What am I?", "answer": "panda", "hint": "I live in China and I am a bear."},
            ],
            "final_code": "ELEPHANT-have-FLY-7-PANDA",
            "reward": "You escaped! +40 XP! Badge: Zoo Adventurer"
        },
        8: {
            "title": "Escape from the Forest!",
            "story": "You are lost in a magical forest! Solve 5 nature puzzles to find the path home!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: P-R-I-S-N-G. What season is it?", "answer": "SPRING", "hint": "Flowers bloom in this season."},
                {"type": "grammar", "question": "Fill in: 'It ___ rainy today.' (is / are)", "answer": "is", "hint": "'It' goes with 'is'."},
                {"type": "reading", "question": "Read: 'In autumn, leaves fall from trees. They are red and yellow.' What colour are the leaves?", "answer": "red and yellow", "hint": "Look at the last sentence."},
                {"type": "maths", "question": "There are 4 seasons in a year. How many seasons in 2 years?", "answer": "8", "hint": "4 × 2 = ?"},
                {"type": "riddle", "question": "I fall from the sky but I am not a bird. I am white and cold. What am I?", "answer": "snow", "hint": "You see me in winter."},
            ],
            "final_code": "SPRING-is-RED-8-SNOW",
            "reward": "You escaped! +40 XP! Badge: Forest Explorer"
        },
        9: {
            "title": "Escape from the Castle!",
            "story": "A wizard locked you in a fairy tale castle! Solve 5 puzzles to break the spell!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: N-C-P-I-R-E-S-S. Who is she?", "answer": "PRINCESS", "hint": "She lives in a castle and wears a crown."},
                {"type": "grammar", "question": "Fill in: 'Once upon a time, there ___ a king.' (was / were)", "answer": "was", "hint": "'A king' is one person, so use 'was'."},
                {"type": "reading", "question": "Read: 'The frog turned into a prince. The princess was very happy.' Who did the frog become?", "answer": "a prince", "hint": "Look after 'turned into'."},
                {"type": "maths", "question": "The princess has 5 jewels. She finds 3 more. How many jewels now?", "answer": "8", "hint": "5 + 3 = ?"},
                {"type": "riddle", "question": "I am tall and made of stone. A king lives inside me. What am I?", "answer": "castle", "hint": "Princesses and kings live here."},
            ],
            "final_code": "PRINCESS-was-PRINCE-8-CASTLE",
            "reward": "You escaped! +40 XP! Badge: Castle Spell Breaker"
        },
        10: {
            "title": "Escape from the Playground!",
            "story": "School is over but the playground gate is locked! Solve 5 puzzles for the last time this year!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: D-R-I-F-E-N. Who is this person?", "answer": "FRIEND", "hint": "Someone you like and play with."},
                {"type": "grammar", "question": "Fill in: 'We ___ best friends.' (am / is / are)", "answer": "are", "hint": "'We' goes with 'are'."},
                {"type": "reading", "question": "Read: 'Let's play together! I like hide and seek.' What game does the child like?", "answer": "hide and seek", "hint": "Look after 'I like'."},
                {"type": "maths", "question": "You have 10 friends. 3 go home. How many friends are still here?", "answer": "7", "hint": "10 - 3 = ?"},
                {"type": "riddle", "question": "I am a special day at the end of the school year. Everyone is happy and sad. What am I?", "answer": "last day of school", "hint": "It is when summer holiday starts."},
            ],
            "final_code": "FRIEND-are-SEEK-7-SCHOOL",
            "reward": "You escaped! +40 XP! Badge: Playground Champion"
        },
    },
}

# ============================================================================
# SEL (Social-Emotional Learning) BANK - Grade 3
# ============================================================================
SEL_BANK = {
    3: {
        1: {
            "emotion": "Happy / Excited",
            "prompt": "It is the first day of school! How do you feel?",
            "activity": "Draw a face and write: I feel ___ because ___.",
            "mindfulness": "Close your eyes. Take 3 deep breaths. Think of something that makes you happy.",
            "discussion": "Tell your partner: What makes you happy at school?"
        },
        2: {
            "emotion": "Love / Belonging",
            "prompt": "Think about your family. Who makes you feel safe and loved?",
            "activity": "Draw your family. Write: I love my ___ because ___.",
            "mindfulness": "Close your eyes. Think of a happy moment with your family. Smile and breathe slowly.",
            "discussion": "Tell your partner: What do you like doing with your family?"
        },
        3: {
            "emotion": "Comfortable / Calm",
            "prompt": "You are in your room at home. What makes your room special?",
            "activity": "Draw your favourite room. Write: I feel ___ in my ___ because ___.",
            "mindfulness": "Close your eyes. Imagine you are in your favourite room. What do you see? What do you hear?",
            "discussion": "Tell your partner: Where do you feel most comfortable at home?"
        },
        4: {
            "emotion": "Joy / Sharing",
            "prompt": "Your friend wants to play with your favourite toy. How do you feel?",
            "activity": "Draw two children sharing a toy. Write: Sharing makes me feel ___.",
            "mindfulness": "Close your eyes. Think of a time you shared something. How did it feel?",
            "discussion": "Tell your partner: Is it easy or hard to share? Why?"
        },
        5: {
            "emotion": "Worried / Brave",
            "prompt": "You feel sick and you need to go to the doctor. How do you feel?",
            "activity": "Draw a 'worry monster' and a 'brave shield'. Write: I am brave when ___.",
            "mindfulness": "Put your hand on your heart. Breathe in for 4 counts, out for 4 counts. Say: I am brave.",
            "discussion": "Tell your partner: What do you do when you are scared or worried?"
        },
        6: {
            "emotion": "Confident / Proud",
            "prompt": "You picked your own clothes today and you look great! How do you feel?",
            "activity": "Draw yourself in your favourite outfit. Write: I feel ___ when I wear ___.",
            "mindfulness": "Stand tall like a superhero. Take 3 big breaths. Say: I am amazing!",
            "discussion": "Tell your partner: When do you feel proud of yourself?"
        },
        7: {
            "emotion": "Caring / Empathy",
            "prompt": "You see a lost kitten in the rain. How do you feel? What do you do?",
            "activity": "Draw a picture of you helping an animal. Write: I can help animals by ___.",
            "mindfulness": "Close your eyes. Think of an animal you love. Send it a kind thought.",
            "discussion": "Tell your partner: How can we be kind to animals?"
        },
        8: {
            "emotion": "Peaceful / Grateful",
            "prompt": "You are sitting in a beautiful garden with flowers and birds. How do you feel?",
            "activity": "Draw a nature scene. Write 3 things you are thankful for: I am thankful for ___.",
            "mindfulness": "Go outside or look out the window. Take 5 slow breaths. Notice 3 beautiful things.",
            "discussion": "Tell your partner: What is your favourite thing about nature?"
        },
        9: {
            "emotion": "Imagination / Wonder",
            "prompt": "If you were a character in a fairy tale, who would you be? Why?",
            "activity": "Draw yourself as a fairy tale character. Write: I would be ___ because ___.",
            "mindfulness": "Close your eyes. Imagine a magical world. What do you see? Who is there with you?",
            "discussion": "Tell your partner: What is the best fairy tale? Why do you like it?"
        },
        10: {
            "emotion": "Sad / Hopeful",
            "prompt": "The school year is ending. You will miss your friends. How do you feel?",
            "activity": "Make a friendship card. Write: I will miss ___ but I am happy because ___.",
            "mindfulness": "Close your eyes. Think of your best memory this year. Smile. Say: Thank you for this year.",
            "discussion": "Tell your partner: What was your best memory this year? What do you want to do next year?"
        },
    },
}

# ============================================================================
# PODCAST BANK - Grade 3
# ============================================================================
PODCAST_BANK = {
    3: {
        1: {
            "title": "Episode 1: Hello, World!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali introduce themselves and greet listeners from around the world.",
            "segments": [
                "Intro (0:00): Welcome to our podcast!",
                "Topic (0:30): How to say hello in 5 languages",
                "Game (2:00): Greeting race - who can say hello the fastest?",
                "Fun Fact (2:30): In Japan, people bow when they say hello!",
                "Challenge (3:00): Say hello to 5 people today!"
            ],
            "student_task": "Record yourself saying hello in English. Say your name and age."
        },
        2: {
            "title": "Episode 2: My Super Family!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali talk about their families and who they live with.",
            "segments": [
                "Intro (0:00): Welcome back! Today is about family!",
                "Topic (0:30): Zeynep talks about her mum, dad, and brother",
                "Game (2:00): Family word quiz - who is your mum's sister?",
                "Fun Fact (2:30): Some families are very big - 10 or more people!",
                "Challenge (3:00): Draw your family tree and name everyone in English!"
            ],
            "student_task": "Record yourself saying: This is my family. I have a ___ and a ___."
        },
        3: {
            "title": "Episode 3: Tour of My House!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep gives a tour of her house and Ali describes his room.",
            "segments": [
                "Intro (0:00): Welcome! Today we explore our houses!",
                "Topic (0:30): Zeynep's house - kitchen, bedroom, living room",
                "Game (2:00): Room guessing game - I cook food here. What room?",
                "Fun Fact (2:30): Some houses in the world are made of ice!",
                "Challenge (3:00): Describe your room using 3 sentences!"
            ],
            "student_task": "Record yourself saying: In my room there is a ___, a ___, and a ___."
        },
        4: {
            "title": "Episode 4: Toy Time!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali share their favourite toys and games.",
            "segments": [
                "Intro (0:00): Welcome! Let's talk about toys and games!",
                "Topic (0:30): Ali's favourite toy is a robot, Zeynep loves puzzles",
                "Game (2:00): Toy guessing - I am round and you kick me. What am I?",
                "Fun Fact (2:30): The oldest toy in the world is a doll from 4000 years ago!",
                "Challenge (3:00): Tell a friend about your favourite toy in English!"
            ],
            "student_task": "Record yourself saying: My favourite toy is a ___. I like it because ___."
        },
        5: {
            "title": "Episode 5: My Amazing Body!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali learn about body parts and how to stay healthy.",
            "segments": [
                "Intro (0:00): Welcome! Today is about our bodies!",
                "Topic (0:30): Head, shoulders, knees, and toes - body parts song",
                "Game (2:00): Simon Says - touch your nose, clap your hands!",
                "Fun Fact (2:30): Your heart beats about 100,000 times a day!",
                "Challenge (3:00): Do 10 jumping jacks and name 5 body parts!"
            ],
            "student_task": "Record yourself pointing to body parts and saying: This is my ___."
        },
        6: {
            "title": "Episode 6: What Are You Wearing?",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali describe their clothes and talk about dressing for the weather.",
            "segments": [
                "Intro (0:00): Welcome! What are you wearing today?",
                "Topic (0:30): Ali is wearing a blue t-shirt and jeans",
                "Game (2:00): Colour and clothes quiz - what colour are your shoes?",
                "Fun Fact (2:30): In Scotland, some men wear skirts called kilts!",
                "Challenge (3:00): Describe what you are wearing right now!"
            ],
            "student_task": "Record yourself saying: I am wearing a ___ and ___. They are ___."
        },
        7: {
            "title": "Episode 7: Animal Planet!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali talk about their favourite animals and animal sounds.",
            "segments": [
                "Intro (0:00): Welcome! Today we love animals!",
                "Topic (0:30): Ali likes dogs, Zeynep likes cats - why?",
                "Game (2:00): Animal sound quiz - who makes this sound?",
                "Fun Fact (2:30): A cheetah can run as fast as a car!",
                "Challenge (3:00): Name 10 animals in English in 30 seconds!"
            ],
            "student_task": "Record yourself saying: My favourite animal is a ___. It can ___."
        },
        8: {
            "title": "Episode 8: Seasons and Weather!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali explore the four seasons and describe today's weather.",
            "segments": [
                "Intro (0:00): Welcome! What is the weather like today?",
                "Topic (0:30): Spring, summer, autumn, winter - what happens in each?",
                "Game (2:00): Season guessing - leaves fall, it is cool. What season?",
                "Fun Fact (2:30): In some countries it never snows! In others, it snows every day!",
                "Challenge (3:00): Look outside and describe the weather in 3 sentences!"
            ],
            "student_task": "Record yourself saying: Today it is ___. My favourite season is ___ because ___."
        },
        9: {
            "title": "Episode 9: Once Upon a Time!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali retell a famous fairy tale and create their own ending.",
            "segments": [
                "Intro (0:00): Welcome! Do you like fairy tales?",
                "Topic (0:30): The Three Little Pigs - short version in English",
                "Game (2:00): Character quiz - who lives in a house of straw?",
                "Fun Fact (2:30): Fairy tales are thousands of years old!",
                "Challenge (3:00): Change the ending of a fairy tale - what happens?"
            ],
            "student_task": "Record yourself retelling a short fairy tale: Once upon a time, there was a ___."
        },
        10: {
            "title": "Episode 10: Best Friends Forever!",
            "host": "Zeynep & Ali",
            "summary": "Zeynep and Ali talk about friendship, memories, and say goodbye for the summer.",
            "segments": [
                "Intro (0:00): Welcome to our last episode this year!",
                "Topic (0:30): Our best school memories - what we loved this year",
                "Game (2:00): Friendship quiz - what makes a good friend?",
                "Fun Fact (2:30): Studies show having friends makes you healthier!",
                "Challenge (3:00): Write a thank-you note to your best friend!"
            ],
            "student_task": "Record yourself saying: My best friend is ___. This year I learned ___. Thank you!"
        },
    },
}
