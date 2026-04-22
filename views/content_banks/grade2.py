# -*- coding: utf-8 -*-
"""Content banks for Grade 2 (Primary Lower / Ages 7-8 / Pre-A1+ CEFR).

Primary_lower tier sections: story, vocabulary, reading, grammar, listening,
speaking, writing, song, culture, project, review.

Curriculum themes (CURRICULUM_GRADE2):
    Unit 1  (W1-4):   My School / Classroom Objects / School Rules / Timetable
    Unit 2  (W5-8):   My Town / Directions / Shops / Places
    Unit 3  (W9-12):  Food / Meals / Healthy Eating / Cooking
    Unit 4  (W13-16): Animals Wild / Habitats / Zoo / Pets
    Unit 5  (W17-20): My Body / Senses / Health / Exercise
    Unit 6  (W21-24): Holidays / Celebrations / Seasons / Calendar
    Unit 7  (W25-27): Transport / Travel / Road Safety
    Unit 8  (W28-30): Nature / Plants / Environment
    Unit 9  (W31-33): Stories / Books / Characters
    Unit 10 (W34-36): Talent Show / Graduation / Summer Plans
"""

# ---------------------------------------------------------------------------
# 1. STORY_CHARACTERS
# ---------------------------------------------------------------------------
STORY_CHARACTERS = {
    2: {
        "main": [
            {"name": "Milo", "age": "7", "desc": "A clever boy who loves maps and exploring his town.", "emoji": "\U0001F9D2"},
            {"name": "Elif", "age": "8", "desc": "A kind girl who likes cooking and taking care of animals.", "emoji": "\U0001F467"},
            {"name": "Ziggy", "age": "3 (dog years)", "desc": "A playful brown dog who can sniff out clues and loves treats.", "emoji": "\U0001F436"},
            {"name": "Cleo", "age": "2 (cat years)", "desc": "A curious white cat who reads books and tells stories.", "emoji": "\U0001F431"},
        ],
        "teacher": {"name": "Mr. Robin", "desc": "A cheerful teacher who uses adventures and projects to teach English."},
    },
}

# ---------------------------------------------------------------------------
# 2. STORY_BANK  (10 episodes, 6-8 sentences each)
# ---------------------------------------------------------------------------
STORY_BANK = {
    2: {
        1: {
            "title": "The New Classroom",
            "previously": None,
            "episode": (
                "It was the first day of school. Milo walked in and saw a big, bright classroom. "
                "'Wow! Look at the board!' said Milo. Elif was sitting at a desk. "
                "'Hello! I am Elif,' she said. 'I am Milo. Nice to meet you!' "
                "A brown dog ran inside. 'Woof! Woof!' 'That is Ziggy!' laughed Milo. "
                "Mr. Robin smiled. 'Welcome, everyone! This is our classroom.' "
                "A white cat jumped onto the bookshelf. 'And that is Cleo,' said Elif. "
                "Mr. Robin said, 'Let's learn our school rules today!'"
            ),
            "cliffhanger": "What rules will the class learn? Find out next time!",
            "vocab_tie": ["classroom", "desk", "board", "bookshelf", "ruler"],
        },
        2: {
            "title": "The Town Map",
            "previously": "Milo, Elif and their pets started a new school year.",
            "episode": (
                "Mr. Robin put a big map on the wall. 'This is our town!' he said. "
                "Milo pointed. 'There is the school!' Elif found the park. 'The park is next to the shop.' "
                "Ziggy barked at the map. 'Is there a pet shop?' asked Elif. "
                "'Yes! Go straight and turn left,' said Mr. Robin. "
                "Cleo put her paw on the library. 'Cleo likes books!' laughed Milo. "
                "They drew a path from the school to the park. "
                "'Our town is great!' said Elif."
            ),
            "cliffhanger": "Where will the class visit first? Let's see!",
            "vocab_tie": ["town", "map", "school", "park", "shop"],
        },
        3: {
            "title": "The Cooking Day",
            "previously": "The class explored a map of the town.",
            "episode": (
                "Today was Cooking Day! Mr. Robin brought fruit and bread. "
                "'Let's make a healthy sandwich!' he said. Elif washed the tomatoes. "
                "Milo cut the cheese carefully. 'I like cheese!' he said. "
                "Ziggy wanted to eat everything. 'No, Ziggy! Wait!' said Elif. "
                "They put bread, cheese, tomato and lettuce together. "
                "Cleo sniffed the milk. 'Cats like milk!' said Milo. "
                "Everyone sat down and ate. 'Yummy!' said the whole class."
            ),
            "cliffhanger": "What will they cook next week?",
            "vocab_tie": ["bread", "cheese", "tomato", "lettuce", "milk"],
        },
        4: {
            "title": "The Zoo Trip",
            "previously": "The class made healthy sandwiches together.",
            "episode": (
                "The class went to the zoo! 'Look! A lion!' said Milo. "
                "The lion was big and golden. 'It lives in the grassland,' said Mr. Robin. "
                "Elif saw a monkey. 'The monkey is climbing a tree!' she said. "
                "Ziggy was scared of the snake. 'Don't worry, Ziggy!' said Milo. "
                "They watched penguins swim in cold water. 'Penguins are funny!' said Elif. "
                "Cleo looked at a parrot. The parrot said, 'Hello! Hello!' "
                "Everyone laughed. 'This is the best trip!' said Milo."
            ),
            "cliffhanger": "Which animal does Elif want as a pet?",
            "vocab_tie": ["lion", "monkey", "snake", "penguin", "parrot"],
        },
        5: {
            "title": "The Five Senses Game",
            "previously": "The class visited the zoo and saw many animals.",
            "episode": (
                "Mr. Robin had a surprise game. 'Close your eyes!' he said. "
                "'What can you hear?' 'I hear a bird!' said Elif. "
                "'Now touch this. What is it?' 'It is soft. A teddy bear!' said Milo. "
                "Ziggy used his nose. 'Ziggy can smell food!' laughed Elif. "
                "'Now taste this,' said Mr. Robin. 'Sweet! An apple!' said Milo. "
                "'Open your eyes! What do you see?' 'I see my friends!' said Elif. "
                "Mr. Robin clapped. 'Five senses! See, hear, smell, taste, touch!'"
            ),
            "cliffhanger": "Can Ziggy use all five senses too?",
            "vocab_tie": ["see", "hear", "smell", "taste", "touch"],
        },
        6: {
            "title": "The Spring Festival",
            "previously": "The class played a five senses game.",
            "episode": (
                "Spring was here! The class planned a festival. "
                "'We need flowers and balloons,' said Elif. "
                "Milo made a calendar. 'The festival is on Friday!' he said. "
                "They painted eggs in many colours. 'Red, blue, yellow!' said Milo. "
                "Ziggy wore a flower crown. 'So cute!' said Elif. "
                "Cleo helped decorate the classroom with ribbons. "
                "On Friday, they danced and sang. 'Happy Spring!' said everyone. "
                "Mr. Robin smiled. 'Every season is special!'"
            ),
            "cliffhanger": "What will summer bring for the class?",
            "vocab_tie": ["spring", "festival", "balloon", "flower", "calendar"],
        },
        7: {
            "title": "The Bus Ride",
            "previously": "The class celebrated a spring festival.",
            "episode": (
                "The class went on a bus ride around the town. "
                "'Look! A red bus!' said Milo. They sat near the window. "
                "Elif saw a bicycle. 'A girl is riding a bicycle!' she said. "
                "The bus stopped at a traffic light. 'Red means stop,' said Mr. Robin. "
                "'Green means go!' said Milo. They saw a train at the station. "
                "Ziggy barked at a motorbike. 'Ziggy, be quiet!' laughed Elif. "
                "'Always look left and right before you cross,' said Mr. Robin. "
                "They arrived at the park safely."
            ),
            "cliffhanger": "What will they discover in the park?",
            "vocab_tie": ["bus", "bicycle", "train", "traffic light", "cross"],
        },
        8: {
            "title": "The Garden Project",
            "previously": "The class took a bus ride and learned road safety.",
            "episode": (
                "Mr. Robin gave everyone a small pot and some seeds. "
                "'Let's grow a plant!' he said. Milo put soil in his pot. "
                "Elif planted a sunflower seed. 'Water it every day,' said Mr. Robin. "
                "Ziggy dug a hole in the garden. 'No, Ziggy! Not there!' said Milo. "
                "Cleo watched a butterfly in the garden. 'Beautiful!' said Elif. "
                "After one week, tiny green leaves appeared. 'It's growing!' said Milo. "
                "'Trees give us clean air,' said Mr. Robin. 'Nature is amazing!'"
            ),
            "cliffhanger": "How tall will the sunflower grow?",
            "vocab_tie": ["seed", "plant", "soil", "leaf", "butterfly"],
        },
        9: {
            "title": "Cleo's Story Time",
            "previously": "The class started a garden project.",
            "episode": (
                "It was raining outside. 'Let's read a story!' said Mr. Robin. "
                "Cleo sat on a big storybook. 'Cleo wants to help!' said Elif. "
                "The story was about a brave knight and a dragon. "
                "'The knight was strong and kind,' read Mr. Robin. "
                "'The dragon was not scary. It was friendly!' said Milo. "
                "Elif drew the characters. 'I like the princess too!' she said. "
                "Ziggy fell asleep during the story. Everyone laughed quietly. "
                "'Books take us to magical places,' said Mr. Robin."
            ),
            "cliffhanger": "Will the class write their own story?",
            "vocab_tie": ["book", "story", "knight", "dragon", "princess"],
        },
        10: {
            "title": "The Talent Show",
            "previously": "The class read stories and drew characters.",
            "episode": (
                "It was the last week of school! Mr. Robin said, 'Let's have a talent show!' "
                "Milo played the drums. 'Boom boom boom!' everyone clapped. "
                "Elif sang a beautiful song about summer. "
                "Ziggy did funny tricks. He rolled over and shook hands! "
                "Cleo walked on a ribbon like a circus cat. 'Wow!' said the class. "
                "Mr. Robin gave everyone a gold star. 'You are all amazing!' he said. "
                "'Have a wonderful summer! Read books and be kind!' "
                "'Goodbye, Mr. Robin! See you next year!' said Milo and Elif."
            ),
            "cliffhanger": "",
            "vocab_tie": ["talent", "summer", "star", "goodbye", "amazing"],
        },
    },
}

# ---------------------------------------------------------------------------
# 3. READING_BANK  (10 passages, 50-70 words, 4 questions each)
# ---------------------------------------------------------------------------
READING_BANK = {
    2: {
        1: {
            "title": "My Classroom",
            "text": (
                "My classroom is big and bright. There are twenty desks and twenty chairs. "
                "The board is on the wall. There is a clock above the board. "
                "We have a bookshelf with many books. Our teacher, Mr. Robin, has a big desk. "
                "There are colourful posters on the walls. I like my classroom. "
                "We learn English here every day. My favourite thing is the computer."
            ),
            "questions": [
                {"type": "mcq", "q": "How many desks are there?", "options": ["Ten", "Twenty", "Thirty", "Forty"], "answer": "Twenty"},
                {"type": "tf", "q": "The clock is under the board.", "answer": False},
                {"type": "mcq", "q": "What is on the bookshelf?", "options": ["Toys", "Books", "Shoes", "Hats"], "answer": "Books"},
                {"type": "open", "q": "What is your favourite thing in your classroom?", "sample_answer": "My favourite thing is the board."},
            ],
        },
        2: {
            "title": "My Town",
            "text": (
                "I live in a small town. There is a school, a park and a hospital. "
                "The bakery is next to the school. I can smell fresh bread every morning. "
                "The library is across from the park. I go there to read books. "
                "There is a big supermarket on Main Street. My mum buys fruit there. "
                "I love my town because it is clean and quiet."
            ),
            "questions": [
                {"type": "mcq", "q": "What is next to the school?", "options": ["The park", "The bakery", "The hospital", "The library"], "answer": "The bakery"},
                {"type": "tf", "q": "The library is next to the bakery.", "answer": False},
                {"type": "mcq", "q": "Where does mum buy fruit?", "options": ["At the park", "At the bakery", "At the supermarket", "At school"], "answer": "At the supermarket"},
                {"type": "open", "q": "What is in your town?", "sample_answer": "There is a school and a park in my town."},
            ],
        },
        3: {
            "title": "A Healthy Lunch",
            "text": (
                "Today I have a healthy lunch. There is a sandwich with cheese and tomato. "
                "I have an apple and a banana too. My water bottle is blue. "
                "I do not eat sweets at school. Mr. Robin says fruit is good for us. "
                "Elif has soup and bread for lunch. Milo has rice and chicken. "
                "We eat together in the school cafeteria. Lunch time is fun!"
            ),
            "questions": [
                {"type": "mcq", "q": "What is in the sandwich?", "options": ["Meat and egg", "Cheese and tomato", "Jam and butter", "Fish and rice"], "answer": "Cheese and tomato"},
                {"type": "tf", "q": "The water bottle is red.", "answer": False},
                {"type": "mcq", "q": "What does Elif have for lunch?", "options": ["A sandwich", "Soup and bread", "Rice and chicken", "Pizza"], "answer": "Soup and bread"},
                {"type": "open", "q": "What do you eat for lunch?", "sample_answer": "I eat a sandwich and an apple for lunch."},
            ],
        },
        4: {
            "title": "At the Zoo",
            "text": (
                "We go to the zoo on Saturday. There are many animals at the zoo. "
                "The lions are big and yellow. They live in a large area with grass. "
                "The monkeys are funny. They jump from tree to tree. "
                "I like the penguins best. They walk in a funny way. "
                "The zoo has a gift shop. I buy a toy elephant. It is a great day!"
            ),
            "questions": [
                {"type": "mcq", "q": "When do they go to the zoo?", "options": ["Monday", "Friday", "Saturday", "Sunday"], "answer": "Saturday"},
                {"type": "tf", "q": "The lions are small and green.", "answer": False},
                {"type": "mcq", "q": "What does the child buy?", "options": ["A toy lion", "A toy elephant", "A toy monkey", "A toy penguin"], "answer": "A toy elephant"},
                {"type": "open", "q": "Which zoo animal do you like best?", "sample_answer": "I like the monkeys best."},
            ],
        },
        5: {
            "title": "My Body",
            "text": (
                "My body is amazing. I have two eyes to see and two ears to hear. "
                "I have one nose to smell flowers. I have one mouth to eat and talk. "
                "I have two hands. I can clap and write with my hands. "
                "I have two feet. I can run and jump. "
                "I brush my teeth every morning and night. I wash my hands before I eat. "
                "Exercise makes my body strong and healthy."
            ),
            "questions": [
                {"type": "mcq", "q": "How many ears do you have?", "options": ["One", "Two", "Three", "Four"], "answer": "Two"},
                {"type": "tf", "q": "We have two noses.", "answer": False},
                {"type": "mcq", "q": "When do you brush your teeth?", "options": ["Only at night", "Only in the morning", "Morning and night", "After lunch"], "answer": "Morning and night"},
                {"type": "open", "q": "What can you do with your hands?", "sample_answer": "I can write and clap with my hands."},
            ],
        },
        6: {
            "title": "Four Seasons",
            "text": (
                "There are four seasons in a year. In spring, flowers grow and birds sing. "
                "In summer, it is hot. We go to the beach and eat ice cream. "
                "In autumn, leaves fall from the trees. They are orange and brown. "
                "In winter, it is cold. Sometimes it snows. We wear coats and scarves. "
                "I like spring best because I can play outside. Every season is beautiful."
            ),
            "questions": [
                {"type": "mcq", "q": "How many seasons are there?", "options": ["Two", "Three", "Four", "Five"], "answer": "Four"},
                {"type": "tf", "q": "In summer, it is cold.", "answer": False},
                {"type": "mcq", "q": "What happens in autumn?", "options": ["It snows", "Flowers grow", "Leaves fall", "We swim"], "answer": "Leaves fall"},
                {"type": "open", "q": "Which season do you like best? Why?", "sample_answer": "I like summer because I can swim."},
            ],
        },
        7: {
            "title": "Going to School",
            "text": (
                "Every morning I go to school. Some children take the bus. "
                "My friend Milo walks to school. Elif rides her bicycle. "
                "We must be careful on the road. We look left and right before we cross. "
                "We use the zebra crossing. The traffic light helps us. "
                "Red means stop. Green means go. We always wear our seat belts in the car. "
                "Road safety is very important."
            ),
            "questions": [
                {"type": "mcq", "q": "How does Elif go to school?", "options": ["By bus", "By car", "She walks", "She rides her bicycle"], "answer": "She rides her bicycle"},
                {"type": "tf", "q": "Red means go.", "answer": False},
                {"type": "mcq", "q": "What do we use to cross the road?", "options": ["A bridge", "A zebra crossing", "A tunnel", "A rope"], "answer": "A zebra crossing"},
                {"type": "open", "q": "How do you go to school?", "sample_answer": "I go to school by bus."},
            ],
        },
        8: {
            "title": "In the Garden",
            "text": (
                "Our school has a beautiful garden. There are many flowers and trees. "
                "We planted sunflower seeds last month. Now they are growing tall. "
                "There are butterflies and bees in the garden. Bees make honey. "
                "We water the plants every day. Mr. Robin says plants need water and sun. "
                "We must not pick the flowers. We must take care of nature. "
                "The garden makes our school pretty."
            ),
            "questions": [
                {"type": "mcq", "q": "What did they plant?", "options": ["Rose seeds", "Sunflower seeds", "Apple seeds", "Carrot seeds"], "answer": "Sunflower seeds"},
                {"type": "tf", "q": "Bees make milk.", "answer": False},
                {"type": "mcq", "q": "What do plants need?", "options": ["Toys and books", "Water and sun", "Music and paint", "Chairs and desks"], "answer": "Water and sun"},
                {"type": "open", "q": "What flowers do you like?", "sample_answer": "I like roses and sunflowers."},
            ],
        },
        9: {
            "title": "My Favourite Book",
            "text": (
                "I love reading books. My favourite book is about a brave girl and a magic tree. "
                "The girl climbs the tree and finds a castle in the clouds. "
                "She meets a friendly giant. The giant gives her a golden key. "
                "She opens a treasure box with the key. Inside there are beautiful stones. "
                "I read this book three times. I want to write my own story one day. "
                "Books are the best friends!"
            ),
            "questions": [
                {"type": "mcq", "q": "Where is the castle?", "options": ["Under the sea", "In the forest", "In the clouds", "On a mountain"], "answer": "In the clouds"},
                {"type": "tf", "q": "The giant is scary and mean.", "answer": False},
                {"type": "mcq", "q": "What does the giant give the girl?", "options": ["A book", "A golden key", "A flower", "A hat"], "answer": "A golden key"},
                {"type": "open", "q": "What is your favourite book?", "sample_answer": "My favourite book is about animals."},
            ],
        },
        10: {
            "title": "Summer Plans",
            "text": (
                "School is almost over. Summer holiday is coming! "
                "Milo wants to visit his grandparents. They live near the sea. "
                "Elif wants to go to summer camp. She will learn to swim. "
                "I want to read five books this summer. I also want to ride my bicycle. "
                "We will miss our teacher, Mr. Robin. He says, 'Have fun and be safe!' "
                "We say goodbye to our friends. See you next year!"
            ),
            "questions": [
                {"type": "mcq", "q": "Where do Milo's grandparents live?", "options": ["In the city", "Near the sea", "In the mountains", "Near the forest"], "answer": "Near the sea"},
                {"type": "tf", "q": "Elif wants to learn to dance.", "answer": False},
                {"type": "mcq", "q": "How many books does the child want to read?", "options": ["Three", "Four", "Five", "Six"], "answer": "Five"},
                {"type": "open", "q": "What are your summer plans?", "sample_answer": "I want to go to the beach."},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 4. GRAMMAR_BANK  (10 rules + 4 exercises each)
# ---------------------------------------------------------------------------
GRAMMAR_BANK = {
    2: {
        1: {
            "title": "There is / There are",
            "rule": "'There is' is used for one thing. 'There are' is used for more than one thing.",
            "formula": "There is + a/an + singular noun. | There are + number/some + plural noun.",
            "examples": [
                ("There is a desk.", "Bir sira var."),
                ("There are two books.", "Iki kitap var."),
                ("There is an apple.", "Bir elma var."),
                ("There are five pencils.", "Bes kalem var."),
            ],
            "exercises": [
                ("fill", "___ a clock on the wall.", "There is"),
                ("fill", "___ three chairs.", "There are"),
                ("choose", "There (is/are) a teacher.", "is"),
                ("rewrite", "books / There / five / are", "There are five books."),
            ],
        },
        2: {
            "title": "Prepositions of Place (in, on, under, next to)",
            "rule": "We use prepositions to say WHERE something is.",
            "formula": "Subject + is/are + preposition + noun.",
            "examples": [
                ("The cat is on the table.", "Kedi masanin ustunde."),
                ("The ball is under the chair.", "Top sandalyenin altinda."),
                ("The book is in the bag.", "Kitap cantanin icinde."),
                ("The shop is next to the park.", "Dukkan parkin yaninda."),
            ],
            "exercises": [
                ("fill", "The dog is ___ the bed. (altinda)", "under"),
                ("fill", "The pen is ___ the box. (icinde)", "in"),
                ("choose", "The school is (on/next to) the library.", "next to"),
                ("match", "on the desk / in the bag / under the table / next to the door", "preposition + place"),
            ],
        },
        3: {
            "title": "Countable Nouns (a/an, some)",
            "rule": "Use 'a' before consonant sounds and 'an' before vowel sounds. Use 'some' for more than one.",
            "formula": "a + consonant word | an + vowel word | some + plural noun.",
            "examples": [
                ("a banana", "bir muz"),
                ("an egg", "bir yumurta"),
                ("some apples", "birkac elma"),
                ("an orange", "bir portakal"),
            ],
            "exercises": [
                ("fill", "I want ___ apple. (bir)", "an"),
                ("fill", "She has ___ tomatoes. (birkac)", "some"),
                ("choose", "There is (a/an) umbrella.", "an"),
                ("rewrite", "egg / an / is / There", "There is an egg."),
            ],
        },
        4: {
            "title": "Can / Can't (Animals)",
            "rule": "'Can' means ability. 'Can't' means not able to do something.",
            "formula": "Subject + can/can't + verb. | Can + subject + verb?",
            "examples": [
                ("A lion can run.", "Bir aslan kosabilir."),
                ("A fish can swim.", "Bir balik yuzebilir."),
                ("A penguin can't fly.", "Bir penguen ucamaz."),
                ("Can a monkey climb?", "Bir maymun tirmanabilir mi?"),
            ],
            "exercises": [
                ("fill", "A bird ___ fly.", "can"),
                ("fill", "A cat ___ swim very well.", "can't"),
                ("choose", "A snake (can/can't) walk.", "can't"),
                ("rewrite", "swim / A / can / dolphin", "A dolphin can swim."),
            ],
        },
        5: {
            "title": "Have got / Has got (Body Parts)",
            "rule": "'Have got' is used with I/you/we/they. 'Has got' is used with he/she/it.",
            "formula": "I/You/We/They + have got + noun. | He/She/It + has got + noun.",
            "examples": [
                ("I have got two eyes.", "Iki gozum var."),
                ("She has got long hair.", "Onun uzun saci var."),
                ("We have got ten fingers.", "On parmagimiz var."),
                ("It has got a tail.", "Onun kuyrugu var."),
            ],
            "exercises": [
                ("fill", "I ___ got two hands.", "have"),
                ("fill", "He ___ got brown eyes.", "has"),
                ("choose", "The dog (have/has) got four legs.", "has"),
                ("rewrite", "She / ears / two / got / has", "She has got two ears."),
            ],
        },
        6: {
            "title": "Present Simple (Seasons & Habits)",
            "rule": "We use present simple for things that happen regularly or are always true.",
            "formula": "I/You/We/They + verb. | He/She/It + verb + s.",
            "examples": [
                ("I like summer.", "Yazi severim."),
                ("She plays outside.", "O disarida oynar."),
                ("We celebrate holidays.", "Biz tatilleri kutlariz."),
                ("It rains in autumn.", "Sonbaharda yagmur yagar."),
            ],
            "exercises": [
                ("fill", "He ___ (play) football every day.", "plays"),
                ("fill", "They ___ (celebrate) New Year.", "celebrate"),
                ("choose", "She (like/likes) spring.", "likes"),
                ("rewrite", "go / We / in / swimming / summer", "We go swimming in summer."),
            ],
        },
        7: {
            "title": "Present Continuous (Actions Now)",
            "rule": "We use present continuous for things happening right now.",
            "formula": "Subject + am/is/are + verb + -ing.",
            "examples": [
                ("I am walking.", "Yuruyorum."),
                ("She is riding a bicycle.", "O bisiklet suruyor."),
                ("They are waiting for the bus.", "Otobusu bekliyorlar."),
                ("He is driving.", "O suruyor."),
            ],
            "exercises": [
                ("fill", "She ___ (run) to school.", "is running"),
                ("fill", "We ___ (wait) for the train.", "are waiting"),
                ("choose", "I (am/is) reading a book.", "am"),
                ("rewrite", "riding / He / is / bicycle / a", "He is riding a bicycle."),
            ],
        },
        8: {
            "title": "Plurals (-s, -es, -ies)",
            "rule": "We add -s to most nouns. We add -es to nouns ending in s, sh, ch, x. We change y to -ies.",
            "formula": "flower -> flowers | bus -> buses | butterfly -> butterflies.",
            "examples": [
                ("one tree, two trees", "bir agac, iki agac"),
                ("one bush, two bushes", "bir cali, iki cali"),
                ("one butterfly, two butterflies", "bir kelebek, iki kelebek"),
                ("one leaf, two leaves", "bir yaprak, iki yaprak"),
            ],
            "exercises": [
                ("fill", "one flower, three ___", "flowers"),
                ("fill", "one box, five ___", "boxes"),
                ("choose", "one baby, two (babys/babies)", "babies"),
                ("rewrite", "Make plural: one watch -> two ___", "watches"),
            ],
        },
        9: {
            "title": "Adjectives (Describing Words)",
            "rule": "Adjectives describe nouns. They come before the noun.",
            "formula": "Subject + is/are + adjective. | adjective + noun.",
            "examples": [
                ("The dragon is big.", "Ejderha buyuk."),
                ("She is a brave girl.", "O cesur bir kiz."),
                ("It is a funny story.", "Bu komik bir hikaye."),
                ("The castle is old.", "Kale eski."),
            ],
            "exercises": [
                ("fill", "The knight is very ___. (cesur)", "brave"),
                ("fill", "It is a ___ book. (guzel)", "beautiful"),
                ("choose", "The princess is (happy/happily).", "happy"),
                ("rewrite", "tall / The / is / giant", "The giant is tall."),
            ],
        },
        10: {
            "title": "Going to (Future Plans)",
            "rule": "We use 'going to' to talk about future plans.",
            "formula": "Subject + am/is/are + going to + verb.",
            "examples": [
                ("I am going to swim.", "Yuzecegim."),
                ("She is going to sing.", "O sarkI soyleyecek."),
                ("We are going to have fun.", "Eglencegiz."),
                ("They are going to travel.", "Seyahat edecekler."),
            ],
            "exercises": [
                ("fill", "I ___ going to read books.", "am"),
                ("fill", "He ___ going to visit grandma.", "is"),
                ("choose", "We (am/are) going to play.", "are"),
                ("rewrite", "going / She / dance / to / is", "She is going to dance."),
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 5. SONG_BANK  (10 songs/chants)
# ---------------------------------------------------------------------------
SONG_BANK = {
    2: {
        1: {
            "title": "The Classroom Song",
            "type": "Song",
            "lyrics": (
                "This is my classroom, my classroom!\n"
                "Desks and chairs everywhere!\n"
                "Books and pencils, rulers too,\n"
                "I love learning here with you!\n\n"
                "Where is the board? On the wall!\n"
                "Where is the clock? It is tall!\n"
                "This is my classroom, my classroom!\n"
                "The best place of all!"
            ),
            "activity": "Point to each object in the classroom as you sing about it.",
        },
        2: {
            "title": "The Town Chant",
            "type": "Chant",
            "lyrics": (
                "Go straight, go straight! (march march)\n"
                "Turn left, turn right! (point point)\n"
                "Where is the shop? Where is the park?\n"
                "Let's find them all before it's dark!\n\n"
                "School, library, hospital too,\n"
                "Bakery, park — I'll show you!\n"
                "Go straight, go straight! (march march)\n"
                "Turn left, turn right! (point point)"
            ),
            "activity": "March in place and point left or right when the chant says so.",
        },
        3: {
            "title": "The Food Song",
            "type": "Song",
            "lyrics": (
                "Apples, bananas, one, two, three!\n"
                "Healthy food is good for me!\n"
                "Bread and cheese and tomato too,\n"
                "Eat your veggies, that's what I do!\n\n"
                "Milk for breakfast, soup for lunch,\n"
                "Carrots are great — crunch, crunch, crunch!\n"
                "Apples, bananas, one, two, three!\n"
                "Healthy food is good for me!"
            ),
            "activity": "Pretend to eat each food as you sing. Crunch loudly for carrots!",
        },
        4: {
            "title": "The Animal Rap",
            "type": "Rap",
            "lyrics": (
                "Lion, lion, ROAR ROAR ROAR! (clap)\n"
                "Monkey, monkey, climb some more! (clap)\n"
                "Penguin, penguin, waddle low! (clap)\n"
                "Parrot, parrot, say HELLO! (clap)\n\n"
                "Animals here, animals there,\n"
                "Animals, animals everywhere!\n"
                "Big or small, fast or slow,\n"
                "To the zoo we love to go!"
            ),
            "activity": "Act like each animal. Roar for the lion, waddle for the penguin!",
        },
        5: {
            "title": "Head, Shoulders, Knees and Toes",
            "type": "Song",
            "lyrics": (
                "Head, shoulders, knees and toes,\n"
                "Knees and toes!\n"
                "Head, shoulders, knees and toes,\n"
                "Knees and toes!\n\n"
                "Eyes and ears and mouth and nose,\n"
                "Head, shoulders, knees and toes,\n"
                "Knees and toes!\n\n"
                "Touch them fast, touch them slow,\n"
                "Ready, steady, here we go!"
            ),
            "activity": "Touch each body part as you sing. Get faster each round!",
        },
        6: {
            "title": "The Seasons Song",
            "type": "Song",
            "lyrics": (
                "Spring is here, the flowers bloom! (sniff sniff)\n"
                "Summer's hot, we need more room! (fan fan)\n"
                "Autumn leaves are falling down! (flutter hands)\n"
                "Winter snow is on the ground! (shiver)\n\n"
                "Spring, summer, autumn, winter,\n"
                "Every season makes me happy!\n"
                "Holidays and celebrations,\n"
                "All year round with friends and family!"
            ),
            "activity": "Do the actions for each season. Draw your favourite season after.",
        },
        7: {
            "title": "The Transport Song",
            "type": "Song",
            "lyrics": (
                "Bus, bus, beep beep beep!\n"
                "Train, train, on the track!\n"
                "Bicycle, bicycle, ring ring ring!\n"
                "Car, car, going fast!\n\n"
                "Stop at red, go at green,\n"
                "Look both ways, that's the scene!\n"
                "Bus, train, bicycle, car,\n"
                "Take me near or take me far!"
            ),
            "activity": "Pretend to drive each vehicle. Stop when you hear 'red'!",
        },
        8: {
            "title": "The Nature Chant",
            "type": "Chant",
            "lyrics": (
                "Plant a seed, watch it grow! (crouch and rise)\n"
                "Water, water, nice and slow! (sprinkle fingers)\n"
                "Sun is shining, leaves are green! (arms up)\n"
                "The prettiest garden I have seen! (look around)\n\n"
                "Flowers, trees, butterflies too,\n"
                "Nature is beautiful, just like you!\n"
                "Take care of the earth every day,\n"
                "Reduce, reuse, recycle — hooray!"
            ),
            "activity": "Do the actions in brackets. Plant a real seed after the chant!",
        },
        9: {
            "title": "The Story Time Rap",
            "type": "Rap",
            "lyrics": (
                "Open a book, turn the page! (clap clap)\n"
                "Knights and dragons on the stage! (clap clap)\n"
                "Princesses brave, giants tall, (clap clap)\n"
                "Stories, stories, I love them all! (clap clap)\n\n"
                "Read, read, read with me,\n"
                "A, B, C, one, two, three!\n"
                "Books are magic, books are fun,\n"
                "Reading time for everyone!"
            ),
            "activity": "Clap the rhythm and hold up your favourite book at the end.",
        },
        10: {
            "title": "The Goodbye Summer Song",
            "type": "Song",
            "lyrics": (
                "School is over, summer's here!\n"
                "Time for fun throughout the year!\n"
                "Swim and play and read a book,\n"
                "Go outside and have a look!\n\n"
                "Goodbye, friends! Goodbye, teacher!\n"
                "Every day was such a treasure!\n"
                "See you soon, we'll meet again,\n"
                "Best of friends until the end!"
            ),
            "activity": "Wave goodbye and hug your friends. Sing loudly on the last line!",
        },
    },
}

# ---------------------------------------------------------------------------
# 6. CULTURE_CORNER_BANK  (10 culture notes, 3-4 sentences)
# ---------------------------------------------------------------------------
CULTURE_CORNER_BANK = {
    2: {
        1: {
            "title": "Schools Around the World",
            "text": (
                "Schools look different around the world! In Japan, students clean their own classrooms. "
                "In Finland, children start school at age seven. In Turkey, students wear uniforms. "
                "But everywhere, children love to learn and play with friends!"
            ),
            "question": "Do you wear a uniform at school?",
            "country_flag": "JP, FI, TR",
            "recipe": None,
        },
        2: {
            "title": "Famous Towns",
            "text": (
                "Every country has interesting towns and cities. London has big red buses. "
                "Paris has the Eiffel Tower. Istanbul has the Bosphorus between two continents. "
                "What makes your town special?"
            ),
            "question": "Can you draw something special about your town?",
            "country_flag": "GB, FR, TR",
            "recipe": None,
        },
        3: {
            "title": "Food from Different Countries",
            "text": (
                "Children eat different food around the world! In Italy, children love pizza and pasta. "
                "In Japan, children eat sushi and rice. In Turkey, we eat kebabs, borek and fresh bread. "
                "Healthy eating is important in every country!"
            ),
            "question": "What is your favourite food? Is it from Turkey?",
            "country_flag": "IT, JP, TR",
            "recipe": "Simple sandwich: bread + cheese + tomato + lettuce = a healthy lunch!",
        },
        4: {
            "title": "Animals in Different Countries",
            "text": (
                "Different animals live in different countries! Kangaroos live in Australia. "
                "Pandas live in China. Camels live in Turkey and other warm countries. "
                "Every country has special animals to protect and love!"
            ),
            "question": "Which animal from another country do you want to see?",
            "country_flag": "AU, CN, TR",
            "recipe": None,
        },
        5: {
            "title": "Keeping Healthy Everywhere",
            "text": (
                "Children around the world play sports to stay healthy! In Brazil, children play football. "
                "In India, children play cricket. In Turkey, children do gymnastics and play basketball. "
                "Exercise and fresh air are good for everyone!"
            ),
            "question": "What sport do you play to stay healthy?",
            "country_flag": "BR, IN, TR",
            "recipe": None,
        },
        6: {
            "title": "Celebrations Around the World",
            "text": (
                "People celebrate in many ways! In China, they have Chinese New Year with dragons and fireworks. "
                "In America, they celebrate Thanksgiving with turkey. "
                "In Turkey, children celebrate 23 Nisan with songs and dances. "
                "Every country has special holidays!"
            ),
            "question": "What is your favourite holiday?",
            "country_flag": "CN, US, TR",
            "recipe": None,
        },
        7: {
            "title": "Transport Around the World",
            "text": (
                "People travel in different ways! In Venice, Italy, people use boats called gondolas. "
                "In the Netherlands, many people ride bicycles. In Turkey, people use ferries to cross the Bosphorus. "
                "How people travel depends on where they live!"
            ),
            "question": "How do you get to school?",
            "country_flag": "IT, NL, TR",
            "recipe": None,
        },
        8: {
            "title": "Nature and Trees",
            "text": (
                "Trees are important all over the world! The Amazon rainforest in Brazil has millions of trees. "
                "Japan has beautiful cherry blossom trees. Turkey has ancient olive trees. "
                "Trees give us clean air, so we must plant more!"
            ),
            "question": "Have you ever planted a tree or a seed?",
            "country_flag": "BR, JP, TR",
            "recipe": None,
        },
        9: {
            "title": "Stories from Different Lands",
            "text": (
                "Every country has famous stories! England has stories of King Arthur and knights. "
                "Germany has fairy tales by the Brothers Grimm. Turkey has the funny stories of Nasreddin Hodja. "
                "Stories teach us about the world and make us laugh!"
            ),
            "question": "Do you know a Nasreddin Hodja story?",
            "country_flag": "GB, DE, TR",
            "recipe": None,
        },
        10: {
            "title": "Summer Fun Worldwide",
            "text": (
                "Children love summer everywhere! In Spain, children play on the beach until late. "
                "In America, children go to summer camp. In Turkey, families visit seaside towns. "
                "Summer is a time for fun, family and friends!"
            ),
            "question": "What do you like to do in summer?",
            "country_flag": "ES, US, TR",
            "recipe": None,
        },
    },
}

# ---------------------------------------------------------------------------
# 7. PROJECT_BANK  (10 projects)
# ---------------------------------------------------------------------------
PROJECT_BANK = {
    2: {
        1: {
            "title": "My Classroom Map",
            "desc": "Draw a map of your classroom and label everything in English!",
            "steps": [
                "Draw the shape of your classroom on paper.",
                "Draw the desks, chairs, board and door.",
                "Write the English name next to each thing.",
                "Add your favourite spot with a star.",
                "Present your map to the class in English!",
            ],
            "materials": "Large paper, ruler, coloured pencils, eraser",
        },
        2: {
            "title": "My Town Poster",
            "desc": "Create a poster of your town with important places!",
            "steps": [
                "Draw a simple map of your town.",
                "Add the school, park, hospital, shop and library.",
                "Write the name of each place in English.",
                "Draw arrows and write 'go straight' or 'turn left/right'.",
                "Show your poster to the class!",
            ],
            "materials": "Poster paper, markers, stickers, ruler",
        },
        3: {
            "title": "Healthy Food Plate",
            "desc": "Make a paper plate with healthy foods from each group!",
            "steps": [
                "Get a paper plate and divide it into four parts.",
                "Draw and label: fruit, vegetables, protein, grains.",
                "Colour each section a different colour.",
                "Add a cup of water or milk on the side.",
                "Tell your class what you eat every day!",
            ],
            "materials": "Paper plate, crayons, scissors, glue, magazines",
        },
        4: {
            "title": "Animal Fact Cards",
            "desc": "Make fact cards about five wild animals!",
            "steps": [
                "Choose five animals: lion, monkey, penguin, snake, parrot.",
                "Draw each animal on a card.",
                "Write three facts: name, where it lives, what it can do.",
                "Decorate the cards with colours.",
                "Play a guessing game with your friends!",
            ],
            "materials": "Index cards, coloured pencils, markers",
        },
        5: {
            "title": "My Body Poster",
            "desc": "Draw your body and label the parts in English!",
            "steps": [
                "Lie on a big paper and trace your body shape.",
                "Write the body parts: head, arms, legs, hands, feet.",
                "Add the senses: eyes (see), ears (hear), nose (smell).",
                "Colour your body poster.",
                "Present it and point to each part as you say it!",
            ],
            "materials": "Large paper, markers, crayons, tape",
        },
        6: {
            "title": "Seasons Wheel",
            "desc": "Make a spinning wheel showing all four seasons!",
            "steps": [
                "Cut two circles from card — one big, one small.",
                "Divide the big circle into four parts.",
                "Draw spring, summer, autumn and winter in each part.",
                "Write one sentence about each season.",
                "Attach the small circle on top with a pin. Spin and read!",
            ],
            "materials": "Card, scissors, split pin, crayons, markers",
        },
        7: {
            "title": "Road Safety Board Game",
            "desc": "Create a board game about road safety rules!",
            "steps": [
                "Draw a path with 20 squares on cardboard.",
                "Write road safety rules on some squares.",
                "Add 'Go forward 2' and 'Go back 1' squares.",
                "Make a dice and player pieces from paper.",
                "Play the game with friends and read the rules aloud!",
            ],
            "materials": "Cardboard, markers, paper, scissors, small coins for pieces",
        },
        8: {
            "title": "Seed Diary",
            "desc": "Plant a seed and write a diary about how it grows!",
            "steps": [
                "Plant a seed in a small pot with soil.",
                "Water it every day.",
                "Draw a picture each week showing the plant.",
                "Write one sentence: 'Day 7: I see a leaf!'",
                "After four weeks, present your diary to the class!",
            ],
            "materials": "Seed, pot, soil, notebook, coloured pencils, water",
        },
        9: {
            "title": "My Story Book",
            "desc": "Write and draw your own short story in English!",
            "steps": [
                "Think of a character: a child, an animal or a magical creature.",
                "Write three pages: beginning, middle and end.",
                "Draw a picture on each page.",
                "Make a colourful cover with a title.",
                "Read your story to the class!",
            ],
            "materials": "Paper, stapler, crayons, pencil, eraser",
        },
        10: {
            "title": "Summer Bucket List",
            "desc": "Make a poster of things you want to do this summer!",
            "steps": [
                "Write 'My Summer Bucket List' at the top.",
                "List five things you want to do in English.",
                "Draw a picture for each activity.",
                "Decorate with suns, stars and colours.",
                "Share your list with the class and say each plan!",
            ],
            "materials": "Poster paper, markers, stickers, glitter",
        },
    },
}

# ---------------------------------------------------------------------------
# 8. LISTENING_SCRIPT_BANK  (10 scripts + 3 tasks each)
# ---------------------------------------------------------------------------
LISTENING_SCRIPT_BANK = {
    2: {
        1: {
            "title": "In the Classroom",
            "script": (
                "Narrator: Listen and point to the correct object.\n\n"
                "Mr. Robin: Good morning, class! What can you see?\n"
                "Milo: I can see a board on the wall.\n"
                "Elif: I can see a bookshelf with books.\n"
                "Mr. Robin: How many desks are there?\n"
                "Milo: There are twenty desks!\n"
                "Mr. Robin: Very good! Is there a clock?\n"
                "Elif: Yes! There is a clock above the board.\n"
                "Mr. Robin: Excellent! Now open your books."
            ),
            "tasks": [
                "Point to the board, the bookshelf and the clock.",
                "How many desks are there? Write the number.",
                "Draw three things in your classroom.",
            ],
        },
        2: {
            "title": "Finding the Library",
            "script": (
                "Narrator: Listen and follow the directions.\n\n"
                "Milo: Excuse me, where is the library?\n"
                "Mr. Robin: Go straight. Then turn left.\n"
                "Milo: Go straight and turn left?\n"
                "Mr. Robin: Yes. The library is next to the park.\n"
                "Elif: I can see it! It is a big building.\n"
                "Milo: Thank you, Mr. Robin!\n"
                "Mr. Robin: You are welcome. Have fun reading!"
            ),
            "tasks": [
                "Where is the library? Circle it on the map.",
                "What is next to the library?",
                "Give your friend directions to the door.",
            ],
        },
        3: {
            "title": "What's for Lunch?",
            "script": (
                "Narrator: Listen and tick the foods you hear.\n\n"
                "Elif: What is for lunch today?\n"
                "Milo: I have a sandwich with cheese.\n"
                "Elif: I have soup and bread.\n"
                "Milo: Do you have any fruit?\n"
                "Elif: Yes! I have an apple and a banana.\n"
                "Milo: I have an orange. Fruit is healthy!\n"
                "Elif: Let's eat together in the cafeteria.\n"
                "Milo: Great idea!"
            ),
            "tasks": [
                "Tick the foods: sandwich, soup, apple, banana, orange.",
                "Who has soup for lunch — Milo or Elif?",
                "Draw your lunch and label the foods in English.",
            ],
        },
        4: {
            "title": "Zoo Animals",
            "script": (
                "Narrator: Listen and match the animal to the picture.\n\n"
                "Mr. Robin: Welcome to the zoo! What can you see?\n"
                "Elif: I can see a lion. It is very big!\n"
                "Milo: Look! A monkey is climbing a tree!\n"
                "Elif: The penguins are walking. They are so funny!\n"
                "Mr. Robin: Can you see the parrot?\n"
                "Milo: Yes! It is green and red. It is saying 'Hello!'\n"
                "Elif: I love the zoo!"
            ),
            "tasks": [
                "Match each animal to its picture: lion, monkey, penguin, parrot.",
                "What colour is the parrot?",
                "Which zoo animal is your favourite? Tell your friend.",
            ],
        },
        5: {
            "title": "Touch Your Head!",
            "script": (
                "Narrator: Listen and do the actions.\n\n"
                "Mr. Robin: Let's play a body game! Touch your head!\n"
                "Children: (touch heads)\n"
                "Mr. Robin: Touch your shoulders!\n"
                "Children: (touch shoulders)\n"
                "Mr. Robin: Touch your knees!\n"
                "Children: (touch knees)\n"
                "Mr. Robin: Now clap your hands two times!\n"
                "Children: (clap clap)\n"
                "Mr. Robin: Stamp your feet three times!\n"
                "Children: (stamp stamp stamp)\n"
                "Mr. Robin: Well done! You know your body parts!"
            ),
            "tasks": [
                "Do the actions: head, shoulders, knees, clap, stamp.",
                "How many times do you clap? Write the number.",
                "Say three body parts to your friend.",
            ],
        },
        6: {
            "title": "The Calendar",
            "script": (
                "Narrator: Listen and answer the questions.\n\n"
                "Elif: What month is it, Mr. Robin?\n"
                "Mr. Robin: It is April. Spring is here!\n"
                "Milo: When is the spring festival?\n"
                "Mr. Robin: It is on Friday, the fifteenth of April.\n"
                "Elif: What season comes after spring?\n"
                "Mr. Robin: Summer! June, July and August.\n"
                "Milo: I love summer! We go on holiday!\n"
                "Mr. Robin: First, let's enjoy spring!"
            ),
            "tasks": [
                "What month is it? Write the answer.",
                "When is the spring festival? Circle the date.",
                "Name the four seasons in order.",
            ],
        },
        7: {
            "title": "On the Road",
            "script": (
                "Narrator: Listen and circle the correct answer.\n\n"
                "Mr. Robin: We are going on a bus today. Let's remember the rules!\n"
                "Elif: We wear our seat belts.\n"
                "Milo: We look left and right before we cross.\n"
                "Mr. Robin: What does a red light mean?\n"
                "Elif: Stop!\n"
                "Mr. Robin: What does a green light mean?\n"
                "Milo: Go!\n"
                "Mr. Robin: And always use the zebra crossing. Well done!"
            ),
            "tasks": [
                "What does red mean? Circle: stop / go / wait.",
                "Name two road safety rules.",
                "Draw a traffic light and colour it.",
            ],
        },
        8: {
            "title": "In the Garden",
            "script": (
                "Narrator: Listen and number the pictures in order.\n\n"
                "Mr. Robin: Today we are planting seeds! First, put soil in the pot.\n"
                "Elif: I put the soil in. Now what?\n"
                "Mr. Robin: Now put the seed in the soil.\n"
                "Milo: I put the seed in! What next?\n"
                "Mr. Robin: Water the seed. Not too much!\n"
                "Elif: I am watering it. Now we wait?\n"
                "Mr. Robin: Yes! Put it in the sun and wait. A plant will grow!"
            ),
            "tasks": [
                "Number the steps: soil, seed, water, sun.",
                "What do plants need to grow?",
                "Draw a plant growing in four steps.",
            ],
        },
        9: {
            "title": "Story Time",
            "script": (
                "Narrator: Listen to the story and answer.\n\n"
                "Mr. Robin: Once upon a time, there was a little bear.\n"
                "The bear lived in a forest. One day, it found a golden book.\n"
                "The bear opened the book. Inside, there were pictures of stars.\n"
                "The bear wished upon a star. 'I want a friend!' said the bear.\n"
                "The next day, a rabbit came to the forest.\n"
                "'Hello! My name is Rabbit. Can I be your friend?'\n"
                "'Yes!' said the bear. And they were friends for ever."
            ),
            "tasks": [
                "Where does the bear live? In a forest / In a house.",
                "What does the bear find? A book / A toy.",
                "Who becomes the bear's friend? Draw the friend.",
            ],
        },
        10: {
            "title": "Goodbye, Grade 2!",
            "script": (
                "Narrator: Listen to the children say goodbye.\n\n"
                "Mr. Robin: It is the last day of school! I am proud of you all.\n"
                "Elif: Thank you, Mr. Robin! I learned so many words!\n"
                "Milo: I am going to miss everyone.\n"
                "Elif: What are you going to do this summer, Milo?\n"
                "Milo: I am going to visit my grandparents. And you?\n"
                "Elif: I am going to go to summer camp!\n"
                "Mr. Robin: Have a wonderful summer! Read books and be happy!\n"
                "Everyone: Goodbye, Mr. Robin! See you next year!"
            ),
            "tasks": [
                "Where is Milo going this summer?",
                "What is Elif going to do?",
                "What are you going to do this summer? Tell your friend.",
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 9. MODEL_WRITING_BANK  (10 models, 3-5 sentences each)
# ---------------------------------------------------------------------------
MODEL_WRITING_BANK = {
    2: {
        1: {
            "title": "My Classroom",
            "prompt": "Write about your classroom.",
            "model": (
                "My classroom is big. There are twenty desks. "
                "There is a board on the wall. I sit next to my friend. "
                "I like my classroom."
            ),
            "key_structures": ["There is / There are", "I like..."],
        },
        2: {
            "title": "My Town",
            "prompt": "Write about your town.",
            "model": (
                "I live in a nice town. There is a school and a park. "
                "The bakery is next to the school. I go to the park every day. "
                "I love my town."
            ),
            "key_structures": ["There is / There are", "prepositions (next to)"],
        },
        3: {
            "title": "My Favourite Food",
            "prompt": "Write about your favourite food.",
            "model": (
                "My favourite food is pizza. I eat it on Fridays. "
                "I like cheese and tomato on my pizza. "
                "I drink orange juice with it. It is yummy!"
            ),
            "key_structures": ["My favourite ... is", "I like / I eat / I drink"],
        },
        4: {
            "title": "My Favourite Animal",
            "prompt": "Write about your favourite animal.",
            "model": (
                "My favourite animal is the dolphin. Dolphins live in the sea. "
                "They can swim very fast. They are grey and white. "
                "Dolphins are friendly and clever."
            ),
            "key_structures": ["can / can't", "They are + adjective"],
        },
        5: {
            "title": "My Body",
            "prompt": "Write about your body.",
            "model": (
                "I have got two eyes and two ears. I have got ten fingers. "
                "I can run and jump with my legs. I brush my teeth every day. "
                "My body is strong!"
            ),
            "key_structures": ["I have got", "I can + verb"],
        },
        6: {
            "title": "My Favourite Season",
            "prompt": "Write about your favourite season.",
            "model": (
                "My favourite season is summer. It is hot and sunny. "
                "I go to the beach with my family. I eat ice cream every day. "
                "I love summer holidays!"
            ),
            "key_structures": ["My favourite ... is", "Present simple"],
        },
        7: {
            "title": "How I Go to School",
            "prompt": "Write about how you go to school.",
            "model": (
                "I go to school by bus. The bus is yellow. "
                "I look left and right before I cross the road. "
                "I always wear my seat belt. Road safety is important."
            ),
            "key_structures": ["by + transport", "Present simple"],
        },
        8: {
            "title": "My Garden",
            "prompt": "Write about a garden.",
            "model": (
                "I have a small garden at home. There are flowers and a big tree. "
                "I planted a sunflower seed. I water it every day. "
                "Butterflies come to my garden."
            ),
            "key_structures": ["There are", "Present simple", "Past simple (planted)"],
        },
        9: {
            "title": "My Favourite Story",
            "prompt": "Write about your favourite story.",
            "model": (
                "My favourite story is about a brave knight. "
                "The knight helps a princess. They find a treasure. "
                "The story is exciting and fun. I read it many times."
            ),
            "key_structures": ["My favourite ... is", "Present simple"],
        },
        10: {
            "title": "My Summer Plans",
            "prompt": "Write about your plans for summer.",
            "model": (
                "This summer, I am going to visit the beach. "
                "I am going to swim and play in the sand. "
                "I am going to read three books. "
                "I am going to have a great summer!"
            ),
            "key_structures": ["going to + verb", "Future plans"],
        },
    },
}

# ---------------------------------------------------------------------------
# 10. FUN_FACTS_BANK  (10 x 3 facts)
# ---------------------------------------------------------------------------
FUN_FACTS_BANK = {
    2: {
        1: [
            "The longest school day in the world is in South Korea — almost 16 hours!",
            "In Japan, students clean their own classrooms every day!",
            "The word 'school' comes from a Greek word meaning 'free time'!",
        ],
        2: [
            "The tallest building in the world is in Dubai — it has 163 floors!",
            "Venice in Italy has canals instead of roads!",
            "Istanbul is the only city in the world on two continents!",
        ],
        3: [
            "Tomatoes are actually a fruit, not a vegetable!",
            "Honey never goes bad — people found 3000-year-old honey and it was still good!",
            "Carrots were originally purple before orange ones became popular!",
        ],
        4: [
            "A group of flamingos is called a 'flamboyance'!",
            "Elephants are the only animals that can't jump!",
            "A snail can sleep for three years!",
        ],
        5: [
            "Your nose can remember 50,000 different smells!",
            "You blink about 15,000 times a day!",
            "Your brain is more active at night than during the day!",
        ],
        6: [
            "In Sweden, there is a hotel made entirely of ice!",
            "The first calendar was made by the ancient Egyptians!",
            "In Australia, Christmas is in summer because the seasons are reversed!",
        ],
        7: [
            "The first bicycle had no pedals — you pushed it with your feet!",
            "The longest train in the world is in Australia — it is 7 kilometres long!",
            "Traffic lights were invented before cars — they were used for horse carriages!",
        ],
        8: [
            "A sunflower can grow up to 3 metres tall!",
            "Trees can talk to each other through their roots!",
            "One big tree can give enough oxygen for four people!",
        ],
        9: [
            "The first printed book was made in China over 1000 years ago!",
            "There are more public libraries in the USA than McDonald's restaurants!",
            "The longest book ever written has over 13 million words!",
        ],
        10: [
            "The first talent show on TV was in 1948!",
            "Some schools in Italy have no homework!",
            "The word 'summer' comes from an old word meaning 'warm season'!",
        ],
    },
}

# ---------------------------------------------------------------------------
# 11. GAMIFICATION_BANK  (levels, 10 badges, bonus XP)
# ---------------------------------------------------------------------------
GAMIFICATION_BANK = {
    2: {
        "levels": [
            {"name": "Word Sprout", "xp_min": 0, "xp_max": 59, "icon": "\U0001F331"},
            {"name": "Sentence Sapling", "xp_min": 60, "xp_max": 179, "icon": "\U0001F333"},
            {"name": "Story Tree", "xp_min": 180, "xp_max": 349, "icon": "\U0001F334"},
            {"name": "Knowledge Forest", "xp_min": 350, "xp_max": 600, "icon": "\U0001F3C6"},
        ],
        "unit_badges": {
            1: {"badge": "Classroom Captain", "desc": "Name 10 classroom objects in English!", "xp": 20},
            2: {"badge": "Town Explorer", "desc": "Give directions to three places on the map!", "xp": 25},
            3: {"badge": "Healthy Chef", "desc": "Name five healthy foods in English!", "xp": 20},
            4: {"badge": "Animal Expert", "desc": "Say five animals and what they can do!", "xp": 25},
            5: {"badge": "Body Builder", "desc": "Label all body parts on a poster!", "xp": 25},
            6: {"badge": "Season Master", "desc": "Describe all four seasons in English!", "xp": 20},
            7: {"badge": "Road Safety Hero", "desc": "Tell three road safety rules in English!", "xp": 25},
            8: {"badge": "Nature Guardian", "desc": "Plant a seed and keep a diary for two weeks!", "xp": 30},
            9: {"badge": "Story Star", "desc": "Read and retell a story in English!", "xp": 25},
            10: {"badge": "Graduation Champion", "desc": "Complete all units and perform at the talent show!", "xp": 35},
        },
        "bonus_xp": [
            {"action": "Read a book in English at home", "xp": 15},
            {"action": "Help a friend learn a new word", "xp": 10},
            {"action": "Write three sentences without help", "xp": 15},
            {"action": "Sing an English song perfectly", "xp": 10},
            {"action": "Complete a project with extra detail", "xp": 20},
        ],
    },
}

# ---------------------------------------------------------------------------
# PROGRESS CHECK BANK  (Review questions per unit, ages 7-8)
# ---------------------------------------------------------------------------
PROGRESS_CHECK_BANK = {
    2: {
        1: {
            "vocab": ["classroom", "ruler", "scissors", "glue", "eraser", "notebook", "board", "shelf", "tidy", "rules"],
            "grammar": ["There is a ___ on the desk.", "There are ___ in the box.", "Is there a ___ in the classroom?"],
            "reading": ["What is on the desk?", "Where is the notebook?", "How many pencils are there?"],
            "writing": ["Write three classroom rules.", "Draw your classroom and label five objects."],
        },
        2: {
            "vocab": ["town", "library", "hospital", "bakery", "park", "next to", "opposite", "between", "turn left", "turn right"],
            "grammar": ["The library is next to the ___.", "Turn ___ at the corner.", "Where is the ___?"],
            "reading": ["Where is the bakery?", "What is opposite the park?", "How do you get to the library?"],
            "writing": ["Write directions from school to the park.", "Draw a simple town map with labels."],
        },
        3: {
            "vocab": ["breakfast", "lunch", "dinner", "healthy", "fruit", "vegetable", "bread", "cheese", "milk", "delicious"],
            "grammar": ["I like ___.", "She doesn't like ___.", "Do you want some ___?"],
            "reading": ["What does Elif eat for lunch?", "Is the salad healthy?", "What is her favourite fruit?"],
            "writing": ["Write what you eat for breakfast.", "Draw a healthy lunch plate and label the food."],
        },
        4: {
            "vocab": ["lion", "elephant", "monkey", "giraffe", "penguin", "habitat", "jungle", "zoo", "wild", "tail"],
            "grammar": ["A lion can ___.", "Elephants can't ___.", "Can a penguin fly?"],
            "reading": ["Where does the lion live?", "What can monkeys do?", "How many animals are at the zoo?"],
            "writing": ["Write three sentences about your favourite wild animal.", "Draw a zoo and label four animals."],
        },
        5: {
            "vocab": ["head", "arm", "leg", "eye", "ear", "nose", "mouth", "see", "hear", "touch"],
            "grammar": ["I have got ___ eyes.", "She has got ___ hair.", "Have you got ___?"],
            "reading": ["How many senses do we have?", "What do we use our ears for?", "What body part helps us see?"],
            "writing": ["Write about your body: 'I have got ___ and ___.'", "Draw a person and label the body parts."],
        },
        6: {
            "vocab": ["spring", "summer", "autumn", "winter", "festival", "celebration", "month", "calendar", "sunny", "snowy"],
            "grammar": ["In spring, we ___.", "It is ___ in winter.", "What do you do in summer?"],
            "reading": ["What season comes after summer?", "What happens in spring?", "When do we wear coats?"],
            "writing": ["Write your favourite holiday memory.", "Draw the four seasons and write one sentence for each."],
        },
        7: {
            "vocab": ["plane", "ship", "bicycle", "helicopter", "taxi", "ticket", "fast", "slow", "travel", "safety"],
            "grammar": ["I travel by ___.", "A plane is ___ than a car.", "How do you get to ___?"],
            "reading": ["How does Milo travel to school?", "Which is faster, a bus or a plane?", "Why do we wear seatbelts?"],
            "writing": ["Write about a trip: 'I went to ___ by ___.'", "Draw three types of transport and label them."],
        },
        8: {
            "vocab": ["flower", "leaf", "root", "seed", "grow", "water", "soil", "tree", "garden", "nature"],
            "grammar": ["Plants need ___ to grow.", "The flower is ___.", "How many leaves are there?"],
            "reading": ["What do plants need?", "Where do seeds grow?", "What colour are the flowers?"],
            "writing": ["Write how to plant a seed (three steps).", "Draw a plant and label: root, stem, leaf, flower."],
        },
        9: {
            "vocab": ["story", "book", "character", "beginning", "middle", "end", "funny", "brave", "adventure", "read"],
            "grammar": ["The story is about ___.", "The character is ___.", "What happens at the end?"],
            "reading": ["Who is the main character?", "Where does the story take place?", "Is the story funny or scary?"],
            "writing": ["Write the beginning of your own short story.", "Draw your favourite book character."],
        },
        10: {
            "vocab": ["talent", "show", "sing", "dance", "act", "clap", "stage", "audience", "summer", "goodbye"],
            "grammar": ["I am going to ___ this summer.", "She is going to ___.", "Are you going to ___?"],
            "reading": ["What talent does Elif show?", "Who dances on stage?", "What are their summer plans?"],
            "writing": ["Write three things you want to do this summer.", "Draw yourself on stage at the talent show."],
        },
    },
}

# ---------------------------------------------------------------------------
# 14. DIALOGUE_BANK  (4-6 lines per unit, A1 level)
# ---------------------------------------------------------------------------
DIALOGUE_BANK = {
    2: {
        1: {
            "setting": "School playground at break time",
            "characters": ["Milo", "Elif"],
            "lines": [
                ("Milo", "Hello! What is your name?"),
                ("Elif", "Hi! My name is Elif. What is your name?"),
                ("Milo", "I am Milo. Do you want to play?"),
                ("Elif", "Yes! Let's play together. You are my friend!"),
                ("Milo", "Yay! Friends are the best!"),
            ],
            "focus_language": "Greetings and introductions",
            "task": "Practise saying hello and telling your name to a partner.",
        },
        2: {
            "setting": "Walking through the town centre",
            "characters": ["Milo", "Elif"],
            "lines": [
                ("Milo", "Look! There is a big park."),
                ("Elif", "Yes! And there is a bakery next to it."),
                ("Milo", "Where is the school?"),
                ("Elif", "The school is behind the library."),
                ("Milo", "I like our town!"),
            ],
            "focus_language": "Places in town and prepositions",
            "task": "Name three places in your town and say where they are.",
        },
        3: {
            "setting": "At the bus stop",
            "characters": ["Milo", "Ziggy"],
            "lines": [
                ("Milo", "Let's go to the park, Ziggy!"),
                ("Ziggy", "Woof! How do we go?"),
                ("Milo", "We can go by bus."),
                ("Ziggy", "Woof! I like the bus!"),
                ("Milo", "Here comes the bus. Let's get on!"),
            ],
            "focus_language": "Transport vocabulary and 'by + transport'",
            "task": "Tell your partner how you come to school (by bus, by car, on foot).",
        },
        4: {
            "setting": "Inside Elif's house",
            "characters": ["Elif", "Cleo"],
            "lines": [
                ("Elif", "Welcome to my home, Cleo!"),
                ("Cleo", "Meow! It is very nice. Where is the kitchen?"),
                ("Elif", "The kitchen is next to the living room."),
                ("Cleo", "Where is your bedroom?"),
                ("Elif", "It is upstairs. Come and see!"),
            ],
            "focus_language": "Rooms in a house and prepositions of place",
            "task": "Draw your home and tell your partner about the rooms.",
        },
        5: {
            "setting": "At the school nurse's office",
            "characters": ["Milo", "Elif"],
            "lines": [
                ("Milo", "I have a headache today."),
                ("Elif", "Oh no! Did you drink water?"),
                ("Milo", "No, I forgot."),
                ("Elif", "You must drink water every day. It is healthy!"),
                ("Milo", "You are right. I will drink water now."),
            ],
            "focus_language": "Health vocabulary and giving advice",
            "task": "Tell your partner three healthy habits (wash hands, drink water, sleep early).",
        },
        6: {
            "setting": "Getting ready for school in the morning",
            "characters": ["Elif", "Milo"],
            "lines": [
                ("Elif", "What are you wearing today?"),
                ("Milo", "I am wearing a blue T-shirt and black trousers."),
                ("Elif", "I am wearing a red dress and white shoes."),
                ("Milo", "You look nice! Let's go to school."),
                ("Elif", "Thank you! I like your T-shirt too."),
            ],
            "focus_language": "Clothes vocabulary and present continuous",
            "task": "Describe what you are wearing today to your partner.",
        },
        7: {
            "setting": "In the school garden",
            "characters": ["Elif", "Ziggy"],
            "lines": [
                ("Elif", "Look at the flowers, Ziggy!"),
                ("Ziggy", "Woof! They are beautiful! What colour are they?"),
                ("Elif", "The roses are red and the daisies are white."),
                ("Ziggy", "Woof! I can see a butterfly too!"),
                ("Elif", "Nature is wonderful!"),
            ],
            "focus_language": "Nature vocabulary and colours",
            "task": "Name five things you can see in nature and say their colours.",
        },
        8: {
            "setting": "In the classroom reading corner",
            "characters": ["Milo", "Cleo"],
            "lines": [
                ("Milo", "I love this storybook!"),
                ("Cleo", "Meow! Who is your favourite character?"),
                ("Milo", "The brave knight! He helps everyone."),
                ("Cleo", "I like the princess. She is very clever."),
                ("Milo", "Let's read together!"),
            ],
            "focus_language": "Story characters and adjectives",
            "task": "Tell your partner about your favourite storybook character.",
        },
        9: {
            "setting": "Looking at a map of Turkey",
            "characters": ["Milo", "Elif"],
            "lines": [
                ("Milo", "Look at the map! Turkey is very big."),
                ("Elif", "Yes! Ankara is the capital city."),
                ("Milo", "I live in Istanbul. Where do you live?"),
                ("Elif", "I live in Izmir. It is near the sea."),
                ("Milo", "I love my country!"),
            ],
            "focus_language": "Country and city vocabulary",
            "task": "Point to a city on the map and say one thing about it.",
        },
        10: {
            "setting": "Last day of school",
            "characters": ["Milo", "Elif", "Ziggy"],
            "lines": [
                ("Milo", "Summer holiday is here! What are you going to do?"),
                ("Elif", "I am going to swim in the sea!"),
                ("Ziggy", "Woof! I am going to play in the garden!"),
                ("Milo", "I am going to visit my grandma."),
                ("Elif", "Have a great summer, everyone!"),
            ],
            "focus_language": "Summer activities and 'going to' for plans",
            "task": "Tell your partner three things you want to do in summer.",
        },
    },
}

# ---------------------------------------------------------------------------
# 15. PRONUNCIATION_BANK
# ---------------------------------------------------------------------------
PRONUNCIATION_BANK = {
    2: {
        1: {
            "sound": "Short /e/ as in 'friend'",
            "words": ["friend", "hello", "best", "yes", "help", "let"],
            "chant": "Hello, hello, my best friend! Let's play, play until the end!",
            "action": "Wave your hand every time you hear the /e/ sound.",
        },
        2: {
            "sound": "Short /a/ as in 'map'",
            "words": ["map", "park", "bank", "bakery", "market", "back"],
            "chant": "Map, map, follow the map! Park, bank, clap, clap, clap!",
            "action": "Clap your hands when you say each word with the /a/ sound.",
        },
        3: {
            "sound": "Long /uː/ as in 'blue'",
            "words": ["blue", "bus", "tube", "school", "scooter", "moon"],
            "chant": "Blue bus, blue bus, zoom zoom zoom! Take me to the moon!",
            "action": "Make a steering wheel motion and say 'zoom' with the /uː/ sound.",
        },
        4: {
            "sound": "/aʊ/ as in 'house'",
            "words": ["house", "mouse", "couch", "out", "down", "around"],
            "chant": "In the house, on the couch, a little mouse goes out!",
            "action": "Point to things around you as you say each word.",
        },
        5: {
            "sound": "/ɒ/ as in 'doctor'",
            "words": ["doctor", "body", "hot", "stop", "wash", "cough"],
            "chant": "Stop! Wash your hands! See the doctor! Yes, you can!",
            "action": "Pretend to wash your hands when you hear the /ɒ/ sound.",
        },
        6: {
            "sound": "/əʊ/ as in 'coat'",
            "words": ["coat", "clothes", "go", "cold", "home", "show"],
            "chant": "Put on your coat, put on your clothes, when it's cold, home you go!",
            "action": "Pretend to put on a coat when you say the /əʊ/ words.",
        },
        7: {
            "sound": "/iː/ as in 'tree'",
            "words": ["tree", "green", "leaf", "sea", "seed", "bee"],
            "chant": "Green tree, green tree, leaf and bee! Seeds grow by the sea!",
            "action": "Stretch your arms up like a tree when you hear /iː/.",
        },
        8: {
            "sound": "/ɪ/ as in 'king'",
            "words": ["king", "princess", "big", "little", "swim", "fish"],
            "chant": "The king is big, the fish can swim, a princess little and slim!",
            "action": "Point up for 'big' and down for 'little' as you chant.",
        },
        9: {
            "sound": "/ɜː/ as in 'Turkey'",
            "words": ["Turkey", "bird", "first", "work", "world", "girl"],
            "chant": "Turkey, Turkey, what a world! A bird sings for every girl!",
            "action": "Spread your arms like a bird when you hear the /ɜː/ sound.",
        },
        10: {
            "sound": "/ʌ/ as in 'sun'",
            "words": ["sun", "fun", "summer", "run", "jump", "love"],
            "chant": "Sun, sun, summer fun! Run and jump, I love everyone!",
            "action": "Jump up every time you say a word with /ʌ/.",
        },
    },
}

# ---------------------------------------------------------------------------
# 16. WORKBOOK_BANK
# ---------------------------------------------------------------------------
WORKBOOK_BANK = {
    2: {
        1: {
            "activities": [
                {"type": "circle", "instruction": "Circle the picture of children being friends."},
                {"type": "trace", "instruction": "Trace the words: FRIEND, HELLO, PLAY."},
                {"type": "match", "instruction": "Match the greeting to the picture (wave = hello, hug = friend)."},
                {"type": "colour", "instruction": "Colour the two friends playing together."},
            ],
        },
        2: {
            "activities": [
                {"type": "label", "instruction": "Label the places on the town map: park, school, bakery, library."},
                {"type": "draw", "instruction": "Draw your favourite place in your town."},
                {"type": "match", "instruction": "Match the place to what you can do there (park = play, library = read)."},
                {"type": "trace", "instruction": "Trace the words: PARK, SCHOOL, SHOP."},
            ],
        },
        3: {
            "activities": [
                {"type": "circle", "instruction": "Circle the vehicles: bus, car, bike, train, boat."},
                {"type": "colour", "instruction": "Colour the bus blue and the car red."},
                {"type": "match", "instruction": "Match the transport to where it goes (boat = sea, plane = sky)."},
                {"type": "trace", "instruction": "Trace: I go to school by ___."},
            ],
        },
        4: {
            "activities": [
                {"type": "label", "instruction": "Label the rooms: bedroom, kitchen, bathroom, living room."},
                {"type": "draw", "instruction": "Draw your bedroom and label three things in it."},
                {"type": "circle", "instruction": "Circle the things you find in a kitchen (fridge, oven, chair, bed)."},
                {"type": "match", "instruction": "Match the object to the room (bed = bedroom, sink = bathroom)."},
            ],
        },
        5: {
            "activities": [
                {"type": "tick", "instruction": "Tick the healthy habits: wash hands, eat sweets, drink water, sleep late."},
                {"type": "colour", "instruction": "Colour the picture of healthy food green and unhealthy food red."},
                {"type": "trace", "instruction": "Trace: Wash your hands. Brush your teeth."},
                {"type": "circle", "instruction": "Circle the body parts: head, arm, leg, eye, ear."},
            ],
        },
        6: {
            "activities": [
                {"type": "label", "instruction": "Label the clothes: hat, coat, shoes, dress, trousers, T-shirt."},
                {"type": "draw", "instruction": "Draw yourself in your favourite clothes."},
                {"type": "match", "instruction": "Match the clothes to the weather (coat = cold, shorts = hot)."},
                {"type": "colour", "instruction": "Colour the clothes your favourite colours."},
            ],
        },
        7: {
            "activities": [
                {"type": "label", "instruction": "Label the nature picture: tree, flower, river, mountain, sun."},
                {"type": "draw", "instruction": "Draw a nature scene with at least four things."},
                {"type": "circle", "instruction": "Circle the living things: tree, rock, bird, flower, stone."},
                {"type": "colour", "instruction": "Colour the leaves green and the flowers pink and yellow."},
            ],
        },
        8: {
            "activities": [
                {"type": "draw", "instruction": "Draw your favourite storybook character."},
                {"type": "circle", "instruction": "Circle the adjective: The knight is (brave / table / run)."},
                {"type": "match", "instruction": "Match the character to the story (Cinderella = glass shoe, Pinocchio = long nose)."},
                {"type": "trace", "instruction": "Trace: My favourite character is ___."},
            ],
        },
        9: {
            "activities": [
                {"type": "colour", "instruction": "Colour the Turkish flag red and white."},
                {"type": "label", "instruction": "Label the cities on the map: Ankara, Istanbul, Izmir, Antalya."},
                {"type": "draw", "instruction": "Draw something special about Turkey (food, place, animal)."},
                {"type": "trace", "instruction": "Trace: I live in ___. I love Turkey."},
            ],
        },
        10: {
            "activities": [
                {"type": "draw", "instruction": "Draw three summer activities (swim, eat ice cream, play)."},
                {"type": "circle", "instruction": "Circle the summer words: beach, snow, sun, ice cream, cold, swim."},
                {"type": "match", "instruction": "Match the activity to the place (swim = beach, hike = mountain)."},
                {"type": "trace", "instruction": "Trace: In summer, I like to ___."},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 17. TURKEY_CORNER_BANK
# ---------------------------------------------------------------------------
TURKEY_CORNER_BANK = {
    2: {
        1: {
            "title": "Turkish Friendships",
            "fact": "In Turkey, friends often say 'Merhaba' and shake hands or hug when they meet.",
            "activity": "Say 'Merhaba' and 'Hello' to five classmates. Draw yourself with a friend.",
        },
        2: {
            "title": "Turkish Towns and Cities",
            "fact": "Istanbul is the biggest city in Turkey. It has beautiful mosques, bridges, and the Bosphorus Sea.",
            "activity": "Draw a picture of a Turkish town with a mosque, park, and market.",
        },
        3: {
            "title": "Transport in Turkey",
            "fact": "In Istanbul, people can travel by ferry boat across the Bosphorus! There are also trams and a metro.",
            "activity": "Draw three types of transport you can see in Turkey. Label them in English.",
        },
        4: {
            "title": "Turkish Homes",
            "fact": "Many Turkish families live in apartments. Some old Turkish houses have beautiful wooden balconies.",
            "activity": "Draw a Turkish house and label the rooms in English.",
        },
        5: {
            "title": "Healthy Turkish Food",
            "fact": "Turkish people eat a big, healthy breakfast with cheese, tomatoes, cucumbers, olives, and bread.",
            "activity": "Draw a Turkish breakfast plate and label the foods in English.",
        },
        6: {
            "title": "Traditional Turkish Clothes",
            "fact": "On special days, some people in Turkey wear traditional clothes. Children wear costumes on 23 Nisan.",
            "activity": "Draw a child wearing traditional Turkish clothes and label them in English.",
        },
        7: {
            "title": "Beautiful Nature in Turkey",
            "fact": "Turkey has amazing nature: Pamukkale has white travertines, and Cappadocia has fairy chimneys!",
            "activity": "Draw Pamukkale or Cappadocia and colour it. Write one sentence about it.",
        },
        8: {
            "title": "Nasreddin Hodja",
            "fact": "Nasreddin Hodja is a famous funny character from Turkey. He has many clever and funny stories.",
            "activity": "Listen to a Nasreddin Hodja story. Draw your favourite part and write one sentence.",
        },
        9: {
            "title": "The Turkish Flag",
            "fact": "The Turkish flag is red with a white star and crescent moon. It is called 'Ay Yildiz'.",
            "activity": "Draw and colour the Turkish flag. Write: 'This is the flag of Turkey.'",
        },
        10: {
            "title": "Summer in Turkey",
            "fact": "In summer, many Turkish families go to the seaside. Antalya and Bodrum are popular holiday places.",
            "activity": "Draw a summer scene at a Turkish beach. Write two things you can do there.",
        },
    },
}

# ---------------------------------------------------------------------------
# 18. COMIC_STRIP_BANK
# ---------------------------------------------------------------------------
COMIC_STRIP_BANK = {
    2: {
        1: {
            "title": "Making a New Friend",
            "panels": [
                {"scene": "Milo is sitting alone at a bench.", "speech": "Milo: I want a friend to play with."},
                {"scene": "Elif walks up with a ball.", "speech": "Elif: Hello! Do you want to play?"},
                {"scene": "They kick the ball together.", "speech": "Milo: Yes! This is fun!"},
                {"scene": "They high-five and smile.", "speech": "Both: We are friends now!"},
            ],
            "drawing_task": "Draw yourself meeting a new friend. Write what you say.",
            "language_focus": "Greetings and introductions",
        },
        2: {
            "title": "Lost in Town",
            "panels": [
                {"scene": "Milo looks confused, holding a map.", "speech": "Milo: Where is the park?"},
                {"scene": "Elif points down the street.", "speech": "Elif: Go straight and turn left!"},
                {"scene": "They walk past the bakery.", "speech": "Milo: I can see the bakery!"},
                {"scene": "They arrive at the park.", "speech": "Both: We found it! Hooray!"},
            ],
            "drawing_task": "Draw a map of your town. Show where the park and school are.",
            "language_focus": "Directions and places in town",
        },
        3: {
            "title": "The Bus Ride",
            "panels": [
                {"scene": "Milo and Ziggy are at the bus stop.", "speech": "Milo: The bus is coming!"},
                {"scene": "They get on a big red bus.", "speech": "Milo: Two tickets, please!"},
                {"scene": "Ziggy looks out the window happily.", "speech": "Ziggy: Woof! I can see cars and bikes!"},
                {"scene": "They arrive at the park.", "speech": "Milo: This is our stop. Let's get off!"},
            ],
            "drawing_task": "Draw your favourite transport. Write: 'I go to school by ___.'",
            "language_focus": "Transport vocabulary",
        },
        4: {
            "title": "A Tour of My Home",
            "panels": [
                {"scene": "Elif opens the front door.", "speech": "Elif: Welcome to my home!"},
                {"scene": "They look into the kitchen.", "speech": "Elif: This is the kitchen. My mum cooks here."},
                {"scene": "Cleo is sleeping on the sofa.", "speech": "Cleo: Meow... This is the living room."},
                {"scene": "Elif shows her bedroom.", "speech": "Elif: And this is my bedroom. I like it!"},
            ],
            "drawing_task": "Draw your home and label three rooms.",
            "language_focus": "Rooms in a house",
        },
        5: {
            "title": "The Clean Hands Song",
            "panels": [
                {"scene": "Ziggy has dirty paws.", "speech": "Milo: Ziggy! Your paws are dirty!"},
                {"scene": "They go to the bathroom.", "speech": "Elif: Wash your hands with soap and water!"},
                {"scene": "Ziggy washes his paws, bubbles everywhere.", "speech": "Ziggy: Woof! Bubbles are fun!"},
                {"scene": "Everyone has clean hands.", "speech": "All: Clean hands, healthy friends!"},
            ],
            "drawing_task": "Draw the steps to wash your hands. Write: First... Then... Finally...",
            "language_focus": "Health and hygiene vocabulary",
        },
        6: {
            "title": "Getting Dressed",
            "panels": [
                {"scene": "Elif opens her wardrobe.", "speech": "Elif: What should I wear today?"},
                {"scene": "She picks a yellow T-shirt.", "speech": "Elif: I like this yellow T-shirt!"},
                {"scene": "Milo arrives in a blue coat.", "speech": "Milo: It is cold! Wear a coat!"},
                {"scene": "They walk out in colourful clothes.", "speech": "Both: We look great!"},
            ],
            "drawing_task": "Draw yourself in summer clothes and winter clothes. Label them.",
            "language_focus": "Clothes vocabulary",
        },
        7: {
            "title": "A Walk in the Forest",
            "panels": [
                {"scene": "Milo, Elif, and Ziggy walk into a forest.", "speech": "Elif: Look at the tall trees!"},
                {"scene": "A bird sits on a branch.", "speech": "Milo: Listen! The bird is singing!"},
                {"scene": "Ziggy sniffs a flower.", "speech": "Ziggy: Woof! This flower smells nice!"},
                {"scene": "They sit by a river.", "speech": "Elif: Nature is beautiful!"},
            ],
            "drawing_task": "Draw a forest scene with a tree, flower, bird, and river.",
            "language_focus": "Nature vocabulary",
        },
        8: {
            "title": "The Magic Storybook",
            "panels": [
                {"scene": "Cleo finds a shiny storybook.", "speech": "Cleo: Meow! This book looks special!"},
                {"scene": "A knight jumps out of the book.", "speech": "Knight: Hello! I am Sir Brave!"},
                {"scene": "A princess waves from the page.", "speech": "Princess: And I am Princess Clever!"},
                {"scene": "Everyone reads together.", "speech": "Milo: Wow! Storybooks are amazing!"},
            ],
            "drawing_task": "Draw a character from your favourite story. Write two sentences about them.",
            "language_focus": "Story character adjectives",
        },
        9: {
            "title": "Flag Day",
            "panels": [
                {"scene": "Elif holds a small Turkish flag.", "speech": "Elif: This is the flag of Turkey!"},
                {"scene": "Milo points at the star and crescent.", "speech": "Milo: It has a white star and a crescent moon."},
                {"scene": "They colour flags together.", "speech": "Both: Red and white! Ay Yildiz!"},
                {"scene": "They wave their flags proudly.", "speech": "Elif: I love my country!"},
            ],
            "drawing_task": "Draw the Turkish flag and write: 'Turkey is my country.'",
            "language_focus": "Country vocabulary and national symbols",
        },
        10: {
            "title": "Summer Fun",
            "panels": [
                {"scene": "It's the last day of school.", "speech": "Milo: Summer is here!"},
                {"scene": "Elif packs her bag with sunscreen.", "speech": "Elif: I am going to the beach!"},
                {"scene": "Ziggy jumps into a pool.", "speech": "Ziggy: Woof! Splash!"},
                {"scene": "Everyone waves goodbye.", "speech": "All: See you next year! Have fun!"},
            ],
            "drawing_task": "Draw your dream summer holiday. Write three things you want to do.",
            "language_focus": "Summer activities and future plans",
        },
    },
}

# ---------------------------------------------------------------------------
# 19. MISSION_BANK
# ---------------------------------------------------------------------------
MISSION_BANK = {
    2: {
        1: {
            "title": "Mission: Friendship Badge",
            "mission": "Say hello to three classmates in English and learn their names.",
            "evidence": "Write three names: 'My friends are ___, ___, and ___.'",
            "xp": 20,
            "difficulty": "Easy",
        },
        2: {
            "title": "Mission: Town Explorer",
            "mission": "Walk around your school and find five places. Name them in English.",
            "evidence": "Draw a mini-map with five labelled places.",
            "xp": 20,
            "difficulty": "Easy",
        },
        3: {
            "title": "Mission: Transport Spotter",
            "mission": "On the way to school, count how many vehicles you see. Name them in English.",
            "evidence": "Draw four vehicles and write their names: bus, car, bike, truck.",
            "xp": 25,
            "difficulty": "Easy",
        },
        4: {
            "title": "Mission: Home Detective",
            "mission": "Go on a room tour at home. Name every room in English.",
            "evidence": "Draw your home floor plan and label at least four rooms.",
            "xp": 20,
            "difficulty": "Easy",
        },
        5: {
            "title": "Mission: Health Hero",
            "mission": "Follow three healthy habits today: wash hands, drink water, eat fruit.",
            "evidence": "Draw a checklist and tick the habits you did. Write one sentence.",
            "xp": 25,
            "difficulty": "Easy",
        },
        6: {
            "title": "Mission: Fashion Designer",
            "mission": "Design a cool outfit for your favourite character. Label the clothes in English.",
            "evidence": "Draw the outfit and label: hat, shirt, trousers, shoes.",
            "xp": 20,
            "difficulty": "Easy",
        },
        7: {
            "title": "Mission: Nature Collector",
            "mission": "Go outside and find five things from nature. Name them in English.",
            "evidence": "Draw or stick five nature items and write their names.",
            "xp": 25,
            "difficulty": "Easy",
        },
        8: {
            "title": "Mission: Story Writer",
            "mission": "Create a new storybook character. Draw it and write three sentences about it.",
            "evidence": "A drawing with three sentences: name, what they look like, what they can do.",
            "xp": 30,
            "difficulty": "Medium",
        },
        9: {
            "title": "Mission: Country Reporter",
            "mission": "Learn three facts about Turkey and tell your partner in English.",
            "evidence": "Write three sentences: 'Turkey has... Turkey is... In Turkey, people...'",
            "xp": 25,
            "difficulty": "Easy",
        },
        10: {
            "title": "Mission: Summer Planner",
            "mission": "Plan your perfect summer day. Write and draw five activities.",
            "evidence": "A poster with five drawings and sentences: 'I am going to ___.'",
            "xp": 20,
            "difficulty": "Easy",
        },
    },
}

# ---------------------------------------------------------------------------
# 20. ESCAPE_ROOM_BANK
# ---------------------------------------------------------------------------
ESCAPE_ROOM_BANK = {
    2: {
        1: {
            "title": "Escape from the Playground!",
            "story": "Oh no! The playground gate is locked! Solve 4 puzzles to find the code and get out!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: R-F-I-E-N-D", "answer": "FRIEND", "hint": "A person you like to play with."},
                {"type": "grammar", "question": "Fill in: My name ___ Milo. (is/are)", "answer": "is", "hint": "I ___ / He ___"},
                {"type": "reading", "question": "Read: 'She says hello and smiles.' Is she friendly?", "answer": "yes", "hint": "Friendly people smile."},
                {"type": "riddle", "question": "You do this with your hand when you meet someone. What is it?", "answer": "wave", "hint": "Hello! *moves hand*"},
            ],
            "final_code": "FRIEND-is-yes-wave",
            "reward": "Escaped! +30 XP! Badge: Friendship Star",
        },
        2: {
            "title": "Escape from the Map Shop!",
            "story": "You are locked in a map shop! Solve 4 puzzles to open the door!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: P-A-R-K", "answer": "PARK", "hint": "A place with trees where you play."},
                {"type": "grammar", "question": "Fill in: The school is ___ the library. (next to / on)", "answer": "next to", "hint": "Think about position."},
                {"type": "reading", "question": "Read: 'Go straight and turn right.' Where is this?", "answer": "directions", "hint": "Someone telling you how to go."},
                {"type": "riddle", "question": "I show you streets and places. I am made of paper. What am I?", "answer": "map", "hint": "Explorers use me."},
            ],
            "final_code": "PARK-next to-directions-map",
            "reward": "Escaped! +30 XP! Badge: Town Explorer",
        },
        3: {
            "title": "Escape from the Bus!",
            "story": "The bus doors are stuck! Solve 4 puzzles to open them!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: T-R-A-I-N", "answer": "TRAIN", "hint": "It runs on tracks. Choo choo!"},
                {"type": "grammar", "question": "Fill in: I go to school ___ bus. (by/in)", "answer": "by", "hint": "By bus, by car, by bike."},
                {"type": "reading", "question": "Read: 'It has two wheels and you pedal.' What is it?", "answer": "bike", "hint": "You ride it to school."},
                {"type": "riddle", "question": "I fly in the sky. I have wings but I am not a bird. What am I?", "answer": "plane", "hint": "You take me to another country."},
            ],
            "final_code": "TRAIN-by-bike-plane",
            "reward": "Escaped! +30 XP! Badge: Transport Master",
        },
        4: {
            "title": "Escape from the Locked Room!",
            "story": "You are in a room in a big house. Find the key by solving 4 puzzles!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: K-I-T-C-H-E-N", "answer": "KITCHEN", "hint": "You cook food here."},
                {"type": "grammar", "question": "Fill in: The cat is ___ the sofa. (on/by)", "answer": "on", "hint": "Sitting on top of it."},
                {"type": "reading", "question": "Read: 'I sleep here. It has a bed and a pillow.' What room is it?", "answer": "bedroom", "hint": "You dream here at night."},
                {"type": "riddle", "question": "I have a door and windows. People live in me. What am I?", "answer": "house", "hint": "Home sweet ___!"},
            ],
            "final_code": "KITCHEN-on-bedroom-house",
            "reward": "Escaped! +30 XP! Badge: Home Hero",
        },
        5: {
            "title": "Escape from the Doctor's Office!",
            "story": "The door is jammed! Solve 4 health puzzles to get out!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: S-O-A-P", "answer": "SOAP", "hint": "You use this to wash your hands."},
                {"type": "grammar", "question": "Fill in: You ___ wash your hands before eating. (must/can't)", "answer": "must", "hint": "It is very important!"},
                {"type": "reading", "question": "Read: 'Drink water. Eat fruit. Sleep early.' These are ___ habits.", "answer": "healthy", "hint": "Good for your body."},
                {"type": "riddle", "question": "I have bristles. You use me every morning and night on your teeth. What am I?", "answer": "toothbrush", "hint": "Brush, brush, brush!"},
            ],
            "final_code": "SOAP-must-healthy-toothbrush",
            "reward": "Escaped! +30 XP! Badge: Health Champion",
        },
        6: {
            "title": "Escape from the Wardrobe!",
            "story": "You fell into a magic wardrobe! Solve 4 puzzles to get back!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: D-R-E-S-S", "answer": "DRESS", "hint": "Girls sometimes wear this."},
                {"type": "grammar", "question": "Fill in: She is ___ a red hat. (wearing/eating)", "answer": "wearing", "hint": "Clothes go on your body."},
                {"type": "reading", "question": "Read: 'It is cold. Put on your coat and scarf.' What season is it?", "answer": "winter", "hint": "Brrr! It's cold!"},
                {"type": "riddle", "question": "You wear me on your feet. I come in pairs. What am I?", "answer": "shoes", "hint": "Left foot, right foot."},
            ],
            "final_code": "DRESS-wearing-winter-shoes",
            "reward": "Escaped! +30 XP! Badge: Fashion Star",
        },
        7: {
            "title": "Escape from the Forest!",
            "story": "You are lost in a forest! Solve 4 nature puzzles to find your way home!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: F-L-O-W-E-R", "answer": "FLOWER", "hint": "It is beautiful and colourful. Bees like it."},
                {"type": "grammar", "question": "Fill in: The bird is ___ the tree. (in/under)", "answer": "in", "hint": "Sitting on a branch inside the tree."},
                {"type": "reading", "question": "Read: 'It has green leaves and brown bark. It is very tall.' What is it?", "answer": "tree", "hint": "Birds live in me."},
                {"type": "riddle", "question": "I am blue during the day and dark at night. I am above you. What am I?", "answer": "sky", "hint": "Look up!"},
            ],
            "final_code": "FLOWER-in-tree-sky",
            "reward": "Escaped! +30 XP! Badge: Nature Explorer",
        },
        8: {
            "title": "Escape from the Storybook!",
            "story": "You fell into a storybook! Solve 4 puzzles to get back to the real world!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: K-N-I-G-H-T", "answer": "KNIGHT", "hint": "He is brave and wears armour."},
                {"type": "grammar", "question": "Fill in: The princess is very ___. (clever/run)", "answer": "clever", "hint": "An adjective, not a verb."},
                {"type": "reading", "question": "Read: 'Once upon a time, there was a dragon.' This is the ___ of a story.", "answer": "beginning", "hint": "The first part."},
                {"type": "riddle", "question": "I have pages and pictures. Children read me at bedtime. What am I?", "answer": "storybook", "hint": "Once upon a time..."},
            ],
            "final_code": "KNIGHT-clever-beginning-storybook",
            "reward": "Escaped! +30 XP! Badge: Story Hero",
        },
        9: {
            "title": "Escape from the Museum!",
            "story": "You are locked in a Turkey museum! Solve 4 puzzles to get out!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: A-N-K-A-R-A", "answer": "ANKARA", "hint": "The capital city of Turkey."},
                {"type": "grammar", "question": "Fill in: I live ___ Turkey. (in/on)", "answer": "in", "hint": "I live ___ a country."},
                {"type": "reading", "question": "Read: 'The flag is red and white. It has a star and crescent.' Which country?", "answer": "Turkey", "hint": "Ay Yildiz!"},
                {"type": "riddle", "question": "I am a city with a bridge over two continents. What am I?", "answer": "Istanbul", "hint": "Europe and Asia meet here."},
            ],
            "final_code": "ANKARA-in-Turkey-Istanbul",
            "reward": "Escaped! +30 XP! Badge: Country Expert",
        },
        10: {
            "title": "Escape from the Beach Hut!",
            "story": "The beach hut door is stuck! Solve 4 summer puzzles to escape!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: S-W-I-M", "answer": "SWIM", "hint": "You do this in the sea or pool."},
                {"type": "grammar", "question": "Fill in: I am going ___ swim today. (to/at)", "answer": "to", "hint": "I am going ___ + verb."},
                {"type": "reading", "question": "Read: 'It is hot. Children play in the water and eat ice cream.' What season?", "answer": "summer", "hint": "Sunny and warm!"},
                {"type": "riddle", "question": "I am cold and sweet. You lick me on a hot day. What am I?", "answer": "ice cream", "hint": "Yummy! Vanilla or chocolate?"},
            ],
            "final_code": "SWIM-to-summer-ice cream",
            "reward": "Escaped! +30 XP! Badge: Summer Champion",
        },
    },
}

# ---------------------------------------------------------------------------
# 21. FAMILY_CORNER_BANK
# ---------------------------------------------------------------------------
FAMILY_CORNER_BANK = {
    2: {
        1: {
            "title": "Making Friends in English",
            "activity": "Practise saying 'Hello, my name is...' with your child. Take turns being new friends.",
            "together": "Draw a picture of your child's best friend together. Write their name in English.",
            "parent_question": "Who is your best friend? What do you like to do together?",
            "signature": True,
        },
        2: {
            "title": "Our Town Walk",
            "activity": "Go for a short walk and name places you see in English: park, shop, school, bakery.",
            "together": "Draw a simple map of your neighbourhood together. Label at least three places.",
            "parent_question": "What is your favourite place in our town? Why?",
            "signature": True,
        },
        3: {
            "title": "Transport Count",
            "activity": "Look out the window or go outside. Count how many buses, cars, and bikes you see.",
            "together": "Make a transport chart together. Draw each vehicle and write how many you saw.",
            "parent_question": "How do you go to school? By bus, car, or on foot?",
            "signature": True,
        },
        4: {
            "title": "Home Tour in English",
            "activity": "Walk around your home with your child. Name each room in English together.",
            "together": "Draw a floor plan of your home. Label the rooms: bedroom, kitchen, bathroom, living room.",
            "parent_question": "Which room is your favourite? What do you do there?",
            "signature": True,
        },
        5: {
            "title": "Healthy Habits Checklist",
            "activity": "Make a daily healthy habits checklist in English: wash hands, drink water, eat fruit, sleep early.",
            "together": "Tick off the healthy habits together each evening. Say them in English!",
            "parent_question": "Which healthy habit is the hardest for you? Which is the easiest?",
            "signature": True,
        },
        6: {
            "title": "Clothes Sorting Game",
            "activity": "Sort clothes from the wardrobe into summer and winter piles. Name them in English.",
            "together": "Play a guessing game: describe a piece of clothing and let your child guess which one.",
            "parent_question": "What is your favourite thing to wear? Why do you like it?",
            "signature": True,
        },
        7: {
            "title": "Nature Treasure Hunt",
            "activity": "Go outside and find five natural things: a leaf, a stone, a flower, a stick, a feather.",
            "together": "Stick or draw the items on paper. Write their English names next to each one.",
            "parent_question": "What is the most beautiful thing in nature? Why?",
            "signature": True,
        },
        8: {
            "title": "Bedtime Story Night",
            "activity": "Read a short English storybook together before bed. Talk about the characters.",
            "together": "After reading, draw the main character together. Write: 'The character is ___.'",
            "parent_question": "Who is your favourite storybook character? Why do you like them?",
            "signature": True,
        },
        9: {
            "title": "Turkey Facts Night",
            "activity": "Share three fun facts about Turkey in English. Look at photos or a map together.",
            "together": "Colour a Turkish flag together. Write: 'I love Turkey.'",
            "parent_question": "What do you like most about Turkey? Is it the food, the nature, or the people?",
            "signature": True,
        },
        10: {
            "title": "Summer Dream Board",
            "activity": "Make a summer plan poster together. Draw and write five things to do in summer.",
            "together": "Cut pictures from magazines or draw summer activities. Label them in English.",
            "parent_question": "What is the one thing you really want to do this summer?",
            "signature": True,
        },
    },
}

# ---------------------------------------------------------------------------
# 22. SEL_BANK  (Social-Emotional Learning)
# ---------------------------------------------------------------------------
SEL_BANK = {
    2: {
        1: {
            "emotion": "Happy / Friendly",
            "prompt": "How do you feel when you make a new friend?",
            "activity": "Draw a happy face and a sad face. Write one thing that makes you happy.",
            "mindfulness": "Close your eyes. Think about your best friend. Smile and take three slow breaths.",
            "discussion": "Talk to a partner: What makes a good friend?",
        },
        2: {
            "emotion": "Curious / Excited",
            "prompt": "How do you feel when you explore a new place?",
            "activity": "Draw yourself discovering something new in your town. Write: 'I feel ___.'",
            "mindfulness": "Close your eyes. Imagine you are walking in a new, beautiful place. What do you see?",
            "discussion": "Talk to a partner: Have you ever been to a new place? How did you feel?",
        },
        3: {
            "emotion": "Brave / Confident",
            "prompt": "Do you feel brave when you try something new, like riding a bus alone?",
            "activity": "Draw yourself being brave. Write: 'I am brave when I ___.'",
            "mindfulness": "Sit tall like a superhero. Take three deep breaths. Say: 'I am brave!'",
            "discussion": "Talk to a partner: When were you brave? What did you do?",
        },
        4: {
            "emotion": "Safe / Comfortable",
            "prompt": "Where do you feel the safest? Why?",
            "activity": "Draw your favourite room at home. Write: 'I feel safe in my ___.'",
            "mindfulness": "Hug yourself gently. Think about your cozy home. Breathe slowly.",
            "discussion": "Talk to a partner: What makes your home special?",
        },
        5: {
            "emotion": "Caring / Responsible",
            "prompt": "How do you take care of your body?",
            "activity": "Draw three healthy things you do every day. Write: 'I take care of my body by ___.'",
            "mindfulness": "Put your hand on your heart. Feel it beating. Say: 'Thank you, body!'",
            "discussion": "Talk to a partner: Why is it important to be healthy?",
        },
        6: {
            "emotion": "Creative / Proud",
            "prompt": "How do you feel when you choose your own clothes?",
            "activity": "Design your dream outfit. Write: 'I feel ___ when I wear ___.'",
            "mindfulness": "Close your eyes. Imagine wearing your favourite clothes. How do you feel? Smile!",
            "discussion": "Talk to a partner: Does what you wear change how you feel?",
        },
        7: {
            "emotion": "Calm / Peaceful",
            "prompt": "How does nature make you feel?",
            "activity": "Draw a peaceful nature scene. Write: 'Nature makes me feel ___.'",
            "mindfulness": "Close your eyes. Imagine you are sitting under a big tree. Listen to the birds. Breathe slowly.",
            "discussion": "Talk to a partner: What is your favourite thing in nature? Why?",
        },
        8: {
            "emotion": "Imaginative / Dreamy",
            "prompt": "How do you feel when you read a story or hear a fairy tale?",
            "activity": "Draw your dream adventure. Write: 'In my story, I am ___.'",
            "mindfulness": "Close your eyes. You are the hero of a story. What do you do? Imagine and smile.",
            "discussion": "Talk to a partner: If you were in a storybook, what would happen?",
        },
        9: {
            "emotion": "Proud / Grateful",
            "prompt": "What makes you proud to be from Turkey?",
            "activity": "Draw something you love about Turkey. Write: 'I am proud of ___.'",
            "mindfulness": "Close your eyes. Think about your country. What do you love? Say 'thank you' in your heart.",
            "discussion": "Talk to a partner: What is one special thing about Turkey?",
        },
        10: {
            "emotion": "Excited / Hopeful",
            "prompt": "How do you feel about summer? Are you excited or a little sad that school is ending?",
            "activity": "Draw two faces: one excited, one a little sad. Write: 'I feel ___ about summer because ___.'",
            "mindfulness": "Close your eyes. Imagine your perfect summer day. What makes you smile? Breathe and enjoy.",
            "discussion": "Talk to a partner: What are you looking forward to this summer?",
        },
    },
}

# ---------------------------------------------------------------------------
# 23. STEAM_BANK
# ---------------------------------------------------------------------------
STEAM_BANK = {
    2: {
        1: {
            "subject": "Art + Language",
            "title": "Friendship Bracelet",
            "task": "Make a paper friendship bracelet. Write your friend's name on it. Give it and say: 'You are my friend!'",
            "vocab": ["friend", "bracelet", "name", "give", "share"],
        },
        2: {
            "subject": "Geography + Art",
            "title": "My Town Model",
            "task": "Build a tiny town with boxes and paper. Label the places in English: park, school, shop.",
            "vocab": ["town", "map", "build", "place", "label"],
        },
        3: {
            "subject": "Engineering + Maths",
            "title": "Paper Plane Race",
            "task": "Fold a paper plane. Fly it and measure how far it goes. Write: 'My plane flew ___ steps.'",
            "vocab": ["plane", "fly", "measure", "far", "fast"],
        },
        4: {
            "subject": "Technology + Art",
            "title": "Dream Room Design",
            "task": "Design your dream bedroom on paper. Cut out furniture from magazines. Label everything in English.",
            "vocab": ["bedroom", "bed", "desk", "chair", "lamp", "design"],
        },
        5: {
            "subject": "Science + Health",
            "title": "Germ Experiment",
            "task": "Put glitter on your hands (germs!). Touch things. See how glitter spreads. Wash with soap. Write what happens.",
            "vocab": ["germs", "soap", "wash", "clean", "spread"],
        },
        6: {
            "subject": "Art + Design",
            "title": "Fashion Show",
            "task": "Design an outfit on paper for a character. Present it: 'This is a ___ T-shirt and ___ trousers.'",
            "vocab": ["design", "outfit", "colour", "wear", "fashion"],
        },
        7: {
            "subject": "Science + Nature",
            "title": "Leaf Collection",
            "task": "Collect five different leaves. Stick them on paper. Write their colour and size in English.",
            "vocab": ["leaf", "collect", "big", "small", "green", "brown"],
        },
        8: {
            "subject": "Art + Literacy",
            "title": "Mini Storybook",
            "task": "Fold paper to make a tiny book. Draw a character on each page. Write one sentence per page.",
            "vocab": ["book", "page", "draw", "character", "story"],
        },
        9: {
            "subject": "Geography + Art",
            "title": "Turkey Travel Poster",
            "task": "Make a travel poster for Turkey. Draw famous places (Cappadocia, Istanbul). Write: 'Visit Turkey!'",
            "vocab": ["country", "visit", "famous", "beautiful", "poster"],
        },
        10: {
            "subject": "Art + Language",
            "title": "Summer Postcard",
            "task": "Make a postcard. Draw a summer scene on the front. On the back, write: 'Dear ___, I am having fun! Love, ___.'",
            "vocab": ["postcard", "summer", "beach", "fun", "write"],
        },
    },
}

# ---------------------------------------------------------------------------
# 24. PODCAST_BANK
# ---------------------------------------------------------------------------
PODCAST_BANK = {
    2: {
        1: {
            "title": "Episode 1: Hello, New Friends!",
            "host": "Milo & Elif",
            "summary": "Milo and Elif welcome everyone to their podcast! They talk about making friends and saying hello.",
            "segments": [
                "Intro (0:00): Hello, everyone! Welcome to Kids English Fun!",
                "Topic (0:30): How do you make a new friend? Say hello and smile!",
                "Game (1:30): Hello Game - Say 'Hello, I am ___' in a funny voice!",
                "Fun Fact (2:00): Did you know? Children around the world say hello differently!",
                "Challenge (2:30): Say hello to someone new today. Tell us their name!",
            ],
            "student_task": "Record yourself saying: 'Hello! My name is ___. I like ___.'",
        },
        2: {
            "title": "Episode 2: Let's Explore Our Town!",
            "host": "Milo & Elif",
            "summary": "Milo and Elif take a walk around their town. They name all the places they see!",
            "segments": [
                "Intro (0:00): Welcome back, friends! Today, we are explorers!",
                "Topic (0:30): What places do you see in a town? Park, school, bakery...",
                "Game (1:30): I Spy - 'I spy a place where you borrow books.' (Library!)",
                "Fun Fact (2:00): The smallest town in the world has only one person!",
                "Challenge (2:30): Walk around your neighbourhood and name three places in English.",
            ],
            "student_task": "Record yourself naming four places in your town.",
        },
        3: {
            "title": "Episode 3: Beep Beep! Transport Time!",
            "host": "Milo & Ziggy",
            "summary": "Milo and Ziggy talk about all the ways to travel. Ziggy tries to drive a bus!",
            "segments": [
                "Intro (0:00): Hello! Woof! Today we talk about transport!",
                "Topic (0:30): Bus, car, train, bike, boat, plane - how do you travel?",
                "Game (1:30): Sound Quiz - 'Choo choo!' What is it? (Train!)",
                "Fun Fact (2:00): The longest bus in the world is 30 metres!",
                "Challenge (2:30): Count how many cars you see today. Tell your friend!",
            ],
            "student_task": "Record: 'I go to school by ___. My favourite transport is ___.'",
        },
        4: {
            "title": "Episode 4: Welcome to My Home!",
            "host": "Elif & Cleo",
            "summary": "Elif gives Cleo a tour of her home. They name all the rooms and things inside.",
            "segments": [
                "Intro (0:00): Hello! Meow! Today, we are at home!",
                "Topic (0:30): What rooms are in your home? Bedroom, kitchen, bathroom...",
                "Game (1:30): Where Am I? - 'I have a bed and a pillow.' (Bedroom!)",
                "Fun Fact (2:00): Some houses in Turkey have 200-year-old wooden balconies!",
                "Challenge (2:30): Give your family a home tour in English!",
            ],
            "student_task": "Record yourself naming three rooms in your home.",
        },
        5: {
            "title": "Episode 5: Super Healthy Kids!",
            "host": "Milo & Elif",
            "summary": "Milo and Elif talk about healthy habits. They learn why washing hands and eating fruit is important.",
            "segments": [
                "Intro (0:00): Hello, healthy friends! Let's talk about being healthy!",
                "Topic (0:30): Wash your hands! Drink water! Eat fruit! Sleep well!",
                "Game (1:30): Healthy or Not? - 'Eating candy all day' (Not healthy!)",
                "Fun Fact (2:00): You should wash your hands for 20 seconds - sing the ABC song!",
                "Challenge (2:30): Drink three glasses of water today. Check!",
            ],
            "student_task": "Record: 'I am healthy because I ___ and I ___.'",
        },
        6: {
            "title": "Episode 6: What Are You Wearing?",
            "host": "Elif & Cleo",
            "summary": "Elif and Cleo play a clothes guessing game. They learn summer and winter clothes.",
            "segments": [
                "Intro (0:00): Hello, fashionable friends! Let's talk about clothes!",
                "Topic (0:30): T-shirt, dress, coat, hat, shoes - what do you wear?",
                "Game (1:30): Guess the Clothes - 'I wear it on my head.' (Hat!)",
                "Fun Fact (2:00): In Scotland, some men wear skirts called kilts!",
                "Challenge (2:30): Open your wardrobe and name five things in English.",
            ],
            "student_task": "Record: 'Today I am wearing ___, ___, and ___.'",
        },
        7: {
            "title": "Episode 7: Nature is Amazing!",
            "host": "Milo & Ziggy",
            "summary": "Milo and Ziggy go on a nature walk. They discover trees, flowers, birds, and rivers!",
            "segments": [
                "Intro (0:00): Hello, nature lovers! Let's go outside!",
                "Topic (0:30): Trees, flowers, rivers, mountains, birds - nature is beautiful!",
                "Game (1:30): Nature Sounds - 'Tweet tweet!' What animal? (Bird!)",
                "Fun Fact (2:00): The biggest tree in the world is taller than a 30-floor building!",
                "Challenge (2:30): Find something in nature. Draw it and name it in English.",
            ],
            "student_task": "Record: 'In nature, I can see ___, ___, and ___.'",
        },
        8: {
            "title": "Episode 8: Once Upon a Time...",
            "host": "Cleo & Elif",
            "summary": "Cleo and Elif talk about their favourite storybook characters. They make up a mini story!",
            "segments": [
                "Intro (0:00): Hello, story fans! Do you love stories?",
                "Topic (0:30): Knights, princesses, dragons, wizards - who is your favourite?",
                "Game (1:30): Who Am I? - 'I have a long nose and I am made of wood.' (Pinocchio!)",
                "Fun Fact (2:00): The first storybook for children was written over 300 years ago!",
                "Challenge (2:30): Create your own character. Give it a name and a superpower!",
            ],
            "student_task": "Record: 'My favourite character is ___. He/She is ___.'",
        },
        9: {
            "title": "Episode 9: I Love My Country!",
            "host": "Milo & Elif",
            "summary": "Milo and Elif share fun facts about Turkey. They talk about cities, food, and the flag.",
            "segments": [
                "Intro (0:00): Hello! Today we talk about our beautiful country, Turkey!",
                "Topic (0:30): Ankara is the capital. Istanbul is the biggest city. The flag is red and white.",
                "Game (1:30): True or False? - 'Istanbul is the capital of Turkey.' (False! It's Ankara!)",
                "Fun Fact (2:00): Turkey has seas on three sides: Black Sea, Mediterranean, and Aegean!",
                "Challenge (2:30): Tell your family one fact about Turkey in English.",
            ],
            "student_task": "Record: 'I live in Turkey. My favourite thing about Turkey is ___.'",
        },
        10: {
            "title": "Episode 10: Summer Fun is Coming!",
            "host": "Milo, Elif & Ziggy",
            "summary": "The last episode of the year! Everyone shares their summer plans and says goodbye.",
            "segments": [
                "Intro (0:00): Hello, friends! This is our last episode! Summer is coming!",
                "Topic (0:30): Swim, play, eat ice cream, visit grandma - what are your plans?",
                "Game (1:30): Summer Wish - 'I wish I could go to ___!' What is your wish?",
                "Fun Fact (2:00): The longest day of the year in summer has about 15 hours of sun!",
                "Challenge (2:30): Make a summer bucket list with five things. Read it in English!",
            ],
            "student_task": "Record: 'This summer, I am going to ___. Goodbye, friends! See you next year!'",
        },
    },
}
