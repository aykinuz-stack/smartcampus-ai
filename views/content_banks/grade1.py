# -*- coding: utf-8 -*-
"""Content banks for Grade 1 (Primary Lower / Ages 6-7 / Pre-A1 CEFR).

Primary-lower tier sections (11):
  story, vocabulary, reading, grammar, listening, speaking, writing,
  song, culture, project, review.

Curriculum units (10 units, 36 weeks):
  Unit 1  (W1-4):   Greetings / Classroom / Numbers 1-10 / Colours Review
  Unit 2  (W5-8):   My Family / Body Parts / Feelings / Clothes
  Unit 3  (W9-12):  Animals / Food & Drink / Fruit / Vegetables
  Unit 4  (W13-16): My House / Rooms / Furniture / Toys Review
  Unit 5  (W17-20): Transport / Actions / Weather Review / Seasons Review
  Unit 6  (W21-24): School Subjects / Daily Routines / Time / Days Review
  Unit 7  (W25-27): Sports / Hobbies / Music
  Unit 8  (W28-30): At the Park / At the Shop / Healthy Food
  Unit 9  (W31-33): Jobs / Community / Helping Others
  Unit 10 (W34-36): Summer / Holidays / Year Review

All content is age-appropriate for 6-7 year olds, using 3-5 word
sentences and Pre-A1 vocabulary.  Dict keys: grade -> unit -> content.
"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. STORY CHARACTERS
# ══════════════════════════════════════════════════════════════════════════════

STORY_CHARACTERS = {
    1: {
        "main": [
            {"name": "Lily", "age": "7", "desc": "A kind girl who loves colours and drawing. She always helps her friends.", "emoji": "👧"},
            {"name": "Tom", "age": "7", "desc": "A brave boy who likes animals and sport. He is always smiling.", "emoji": "🧒"},
            {"name": "Buddy", "age": "3 (dog years)", "desc": "A friendly brown puppy who follows Lily and Tom everywhere.", "emoji": "🐶"},
            {"name": "Bella", "age": "1 (bird years)", "desc": "A small blue bird who sings English words and flies around the classroom.", "emoji": "🐦"},
        ],
        "teacher": {"name": "Mr. Sun", "desc": "A cheerful teacher who uses games, songs and picture cards to teach English."},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 2. STORY BANK — 10 episodes (5-6 sentences each)
# ══════════════════════════════════════════════════════════════════════════════

STORY_BANK = {
    1: {
        1: {
            "title": "Hello, New Friends!",
            "previously": None,
            "episode": (
                "It is the first day of school. Lily walks into the classroom. "
                "'Hello! My name is Lily,' she says. A boy waves. 'Hi! I am Tom!' "
                "A small puppy runs in. 'Woof! Woof!' Tom laughs. 'This is Buddy!' "
                "A blue bird flies to the window. 'Hello! Hello!' sings Bella. "
                "Mr. Sun smiles. 'Welcome, everyone! Let us count to ten!'"
            ),
            "cliffhanger": "Can you count to ten with Mr. Sun?",
            "vocab_tie": ["hello", "hi", "name", "friend", "goodbye"],
        },
        2: {
            "title": "My Family Photo",
            "previously": "Lily, Tom, Buddy and Bella met at school.",
            "episode": (
                "Mr. Sun says, 'Show me your family!' Lily holds up a photo. "
                "'This is my mum. This is my dad. This is my baby brother!' "
                "Tom shows his photo too. 'My mum, my dad and my sister!' "
                "Buddy barks. Bella sings, 'Family! Family!' "
                "Mr. Sun says, 'I love your families!' Everyone claps."
            ),
            "cliffhanger": "How many people are in your family?",
            "vocab_tie": ["mother", "father", "sister", "brother", "family"],
        },
        3: {
            "title": "Buddy Sees Animals",
            "previously": "Lily and Tom showed their family photos.",
            "episode": (
                "The class goes to the school garden. Buddy sees a cat. 'Woof!' "
                "'Look! A cat!' says Lily. 'Meow!' says the cat. "
                "Tom sees a bird. 'A bird! Like Bella!' Bella sings, 'Tweet tweet!' "
                "They see a fish in the pond. 'One, two, three fish!' counts Tom. "
                "Mr. Sun says, 'Animals are our friends!'"
            ),
            "cliffhanger": "What animals can you see near your school?",
            "vocab_tie": ["cat", "dog", "bird", "fish", "rabbit"],
        },
        4: {
            "title": "Lily's House",
            "previously": "Buddy and the class saw animals in the garden.",
            "episode": (
                "Lily draws her house. 'This is my house. It is big!' "
                "'This is the kitchen. My mum cooks here.' "
                "'This is my bedroom. I have a bed and a desk.' "
                "Tom draws too. 'My house has a garden!' "
                "Buddy sits on Tom's picture. 'Woof!' Everyone laughs. "
                "Bella sings, 'My house, my home, I love my home!'"
            ),
            "cliffhanger": "Can you draw your house?",
            "vocab_tie": ["house", "kitchen", "bedroom", "garden", "door"],
        },
        5: {
            "title": "Let's Go by Bus!",
            "previously": "Lily and Tom drew their houses.",
            "episode": (
                "Today the class goes on a trip. 'We go by bus!' says Mr. Sun. "
                "Lily looks out the window. 'I see a car! I see a bike!' "
                "Tom says, 'Look! A big plane in the sky!' "
                "Buddy sleeps on the bus seat. Bella flies next to the bus. "
                "'Bus, car, bike, plane!' sings Bella. 'I love the bus!'"
            ),
            "cliffhanger": "How do you go to school?",
            "vocab_tie": ["bus", "car", "bike", "plane", "train"],
        },
        6: {
            "title": "Tom's School Day",
            "previously": "The class went on a bus trip.",
            "episode": (
                "Tom wakes up early. 'Good morning!' he says. "
                "He brushes his teeth. He puts on his uniform. "
                "'What day is it?' asks Lily. 'It is Monday!' says Tom. "
                "'We have English today!' says Mr. Sun. Everyone cheers. "
                "Buddy wags his tail. Bella sings, 'Monday, Tuesday, fun fun fun!'"
            ),
            "cliffhanger": "What is your favourite day of the week?",
            "vocab_tie": ["morning", "Monday", "English", "school", "day"],
        },
        7: {
            "title": "Sports Day",
            "previously": "Tom and Lily learned about days of the week.",
            "episode": (
                "It is Sports Day! 'I can run fast!' says Tom. "
                "Lily says, 'I can jump high!' They go outside. "
                "Tom kicks a ball. 'Football! I love football!' "
                "Lily throws a ball. 'I like basketball!' "
                "Buddy runs with them. Bella sings, 'Run, jump, play!'"
            ),
            "cliffhanger": "What sport do you like?",
            "vocab_tie": ["run", "jump", "football", "basketball", "play"],
        },
        8: {
            "title": "At the Park",
            "previously": "Lily and Tom played sports at school.",
            "episode": (
                "After school, Lily and Tom go to the park. "
                "'I like the swing!' says Lily. 'I like the slide!' says Tom. "
                "They see a man selling fruit. 'Apples! Bananas!' "
                "'Can I have an apple, please?' says Lily. 'Here you are!' "
                "Buddy eats a biscuit. Bella sings, 'Yummy yummy in my tummy!'"
            ),
            "cliffhanger": "What do you eat at the park?",
            "vocab_tie": ["park", "swing", "apple", "banana", "please"],
        },
        9: {
            "title": "Helpers in Our Town",
            "previously": "Lily and Tom played in the park.",
            "episode": (
                "Mr. Sun asks, 'Who helps us?' Lily says, 'The doctor!' "
                "Tom says, 'The firefighter!' 'The police officer!' says Lily. "
                "They visit the fire station. 'Wow! A big red fire truck!' "
                "Buddy barks at the truck. Bella sings, 'Thank you, helpers!' "
                "Mr. Sun says, 'Helpers keep us safe and happy!'"
            ),
            "cliffhanger": "Who is your favourite helper?",
            "vocab_tie": ["doctor", "firefighter", "police", "nurse", "help"],
        },
        10: {
            "title": "Happy Summer!",
            "previously": "Lily and Tom learned about helpers.",
            "episode": (
                "It is the last day of school. Lily is a little sad. "
                "'Don't be sad!' says Tom. 'It is summer! We can play!' "
                "'I will go to the beach!' says Lily. 'I will visit my grandma!' says Tom. "
                "Mr. Sun gives everyone a gold star. 'You are all amazing!' "
                "Buddy wags his tail. Bella sings, 'Goodbye, friends! See you soon!'"
            ),
            "cliffhanger": "",
            "vocab_tie": ["summer", "beach", "goodbye", "holiday", "star"],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 3. READING BANK — 10 passages (40-60 words) + 3-4 questions each
# ══════════════════════════════════════════════════════════════════════════════

READING_BANK = {
    1: {
        1: {
            "title": "Hello! I Am Lily",
            "text": (
                "Hello! My name is Lily. I am seven years old. I go to school. "
                "My teacher is Mr. Sun. He is kind. I have a friend. His name is Tom. "
                "I have a dog. His name is Buddy. Buddy is brown. "
                "I say hello to my friends every day. Goodbye!"
            ),
            "questions": [
                {"type": "mcq", "q": "How old is Lily?", "opts": ["a) Six", "b) Seven", "c) Eight"], "answer": "b"},
                {"type": "tf", "q": "Lily's teacher is Mr. Moon.", "answer": "F"},
                {"type": "open", "q": "What is Lily's dog's name?", "lines": 1},
            ],
        },
        2: {
            "title": "My Family",
            "text": (
                "I have a big family. My mum is kind. My dad is tall. "
                "I have a sister. Her name is Eda. She is five. "
                "I have a brother. His name is Can. He is a baby. "
                "My grandma makes cookies. I love my family."
            ),
            "questions": [
                {"type": "mcq", "q": "How old is Eda?", "opts": ["a) Four", "b) Five", "c) Six"], "answer": "b"},
                {"type": "tf", "q": "Can is a baby.", "answer": "T"},
                {"type": "open", "q": "Who makes cookies?", "lines": 1},
            ],
        },
        3: {
            "title": "Animals I Like",
            "text": (
                "I like animals. I have a cat. My cat is white. "
                "Tom has a dog. His dog is big. At school we have a fish tank. "
                "There are three fish. They are orange. Bella the bird is blue. "
                "I like all animals. Animals are my friends."
            ),
            "questions": [
                {"type": "mcq", "q": "What colour is the cat?", "opts": ["a) Black", "b) Orange", "c) White"], "answer": "c"},
                {"type": "tf", "q": "There are four fish in the tank.", "answer": "F"},
                {"type": "open", "q": "What colour is Bella the bird?", "lines": 1},
                {"type": "tf", "q": "Tom has a dog.", "answer": "T"},
            ],
        },
        4: {
            "title": "My House",
            "text": (
                "My house is small and nice. It has a red door. "
                "I have a bedroom. My bed is blue. I have a desk too. "
                "The kitchen is big. My mum cooks there. "
                "We have a garden. I play in the garden with Buddy."
            ),
            "questions": [
                {"type": "mcq", "q": "What colour is the door?", "opts": ["a) Blue", "b) Green", "c) Red"], "answer": "c"},
                {"type": "tf", "q": "The kitchen is small.", "answer": "F"},
                {"type": "open", "q": "Where does Lily play with Buddy?", "lines": 1},
            ],
        },
        5: {
            "title": "Going to School",
            "text": (
                "I go to school by bus. The bus is yellow. "
                "Tom goes to school by car. Lily walks to school. "
                "We see bikes on the road. We see a big plane in the sky. "
                "I like the bus. The bus driver is nice. Hello, bus driver!"
            ),
            "questions": [
                {"type": "mcq", "q": "What colour is the bus?", "opts": ["a) Red", "b) Yellow", "c) Green"], "answer": "b"},
                {"type": "tf", "q": "Tom goes to school by bus.", "answer": "F"},
                {"type": "open", "q": "What do they see in the sky?", "lines": 1},
                {"type": "tf", "q": "Lily walks to school.", "answer": "T"},
            ],
        },
        6: {
            "title": "My School Day",
            "text": (
                "I wake up at seven. I brush my teeth. I eat breakfast. "
                "I go to school at eight. I have English on Monday. "
                "I have Maths on Tuesday. I like Art on Wednesday. "
                "School finishes at three. I go home and play."
            ),
            "questions": [
                {"type": "mcq", "q": "What time does she wake up?", "opts": ["a) Six", "b) Seven", "c) Eight"], "answer": "b"},
                {"type": "tf", "q": "She has English on Tuesday.", "answer": "F"},
                {"type": "open", "q": "What does she do after school?", "lines": 1},
            ],
        },
        7: {
            "title": "I Like Sports",
            "text": (
                "I like sports. I can run fast. I can jump high. "
                "Tom plays football. Lily plays tennis. "
                "We swim in the summer. Swimming is fun. "
                "On Sports Day we run and jump. I get a gold star!"
            ),
            "questions": [
                {"type": "mcq", "q": "What does Tom play?", "opts": ["a) Tennis", "b) Football", "c) Basketball"], "answer": "b"},
                {"type": "tf", "q": "They swim in the winter.", "answer": "F"},
                {"type": "open", "q": "What does the child get on Sports Day?", "lines": 1},
            ],
        },
        8: {
            "title": "At the Park",
            "text": (
                "I go to the park with Tom. I play on the swing. "
                "Tom goes on the slide. We see flowers. They are pink and yellow. "
                "We buy ice cream. My ice cream is chocolate. "
                "Tom's ice cream is strawberry. The park is fun!"
            ),
            "questions": [
                {"type": "mcq", "q": "What does Lily play on?", "opts": ["a) Slide", "b) Swing", "c) Bike"], "answer": "b"},
                {"type": "tf", "q": "Tom's ice cream is chocolate.", "answer": "F"},
                {"type": "open", "q": "What colour are the flowers?", "lines": 1},
                {"type": "tf", "q": "They see flowers in the park.", "answer": "T"},
            ],
        },
        9: {
            "title": "Helpers",
            "text": (
                "There are many helpers in our town. The doctor helps sick people. "
                "The nurse helps the doctor. The firefighter puts out fires. "
                "The police officer keeps us safe. The teacher helps us learn. "
                "I want to be a doctor. What do you want to be?"
            ),
            "questions": [
                {"type": "mcq", "q": "Who puts out fires?", "opts": ["a) Doctor", "b) Police", "c) Firefighter"], "answer": "c"},
                {"type": "tf", "q": "The nurse helps the teacher.", "answer": "F"},
                {"type": "open", "q": "What does the child want to be?", "lines": 1},
            ],
        },
        10: {
            "title": "Summer Holidays",
            "text": (
                "It is summer! School is finished. I am happy. "
                "I go to the beach with my family. The sea is blue. "
                "I play in the sand. I eat watermelon. It is yummy. "
                "I see my friends in the park. Summer is the best!"
            ),
            "questions": [
                {"type": "mcq", "q": "Where does the child go?", "opts": ["a) Mountain", "b) Beach", "c) Forest"], "answer": "b"},
                {"type": "tf", "q": "The sea is green.", "answer": "F"},
                {"type": "open", "q": "What fruit does the child eat?", "lines": 1},
                {"type": "tf", "q": "The child is happy.", "answer": "T"},
            ],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 4. GRAMMAR BANK — 10 very basic rules + 4 exercises each
# ══════════════════════════════════════════════════════════════════════════════

GRAMMAR_BANK = {
    1: {
        1: {
            "title": "This is / What is this?",
            "rule": "Use 'This is' to name things near you. Ask 'What is this?' to learn new words.",
            "formula": "This is a ___.\nWhat is this? — It is a ___.",
            "examples": [
                ("This is a book.", "+"),
                ("What is this? It is a pencil.", "?"),
                ("This is my teacher.", "+"),
                ("What is this? It is a desk.", "?"),
            ],
            "exercises": [
                ("This _____ a pen.", "is"),
                ("What is _____? It is a bag.", "this"),
                ("_____ is a chair.", "This"),
                ("This is _____ ruler.", "a"),
            ],
        },
        2: {
            "title": "I have / You have",
            "rule": "Use 'I have' to say what you own. Use 'You have' to talk about your friend.",
            "formula": "I have a ___.\nYou have a ___.\nDo you have a ___?",
            "examples": [
                ("I have a sister.", "+"),
                ("You have a brother.", "+"),
                ("I have a big family.", "+"),
                ("Do you have a pet?", "?"),
            ],
            "exercises": [
                ("I _____ a mother and a father.", "have"),
                ("_____ you have a sister?", "Do"),
                ("I have _____ baby brother.", "a"),
                ("You _____ a nice family.", "have"),
            ],
        },
        3: {
            "title": "I like / I don't like",
            "rule": "Use 'I like' for things you enjoy. Use 'I don't like' for things you do not enjoy.",
            "formula": "I like ___.\nI don't like ___.\nDo you like ___?",
            "examples": [
                ("I like cats.", "+"),
                ("I don't like snakes.", "-"),
                ("Do you like fish?", "?"),
                ("I like animals.", "+"),
            ],
            "exercises": [
                ("I _____ dogs.", "like"),
                ("I _____ like spiders.", "don't"),
                ("_____ you like rabbits?", "Do"),
                ("I like _____. (cats/snakes)", "cats"),
            ],
        },
        4: {
            "title": "There is / There are",
            "rule": "Use 'there is' for one thing. Use 'there are' for many things.",
            "formula": "There is a ___. (one)\nThere are ___ ___. (many)",
            "examples": [
                ("There is a bed in my room.", "+"),
                ("There are two chairs.", "+"),
                ("There is a big window.", "+"),
                ("There are toys on the floor.", "+"),
            ],
            "exercises": [
                ("There _____ a table in the kitchen.", "is"),
                ("There _____ three books on the desk.", "are"),
                ("There is _____ door.", "a"),
                ("There _____ flowers in the garden.", "are"),
            ],
        },
        5: {
            "title": "I go by ___",
            "rule": "Use 'by' to say how you travel. Walk is different: 'I walk to school.'",
            "formula": "I go to school by ___.\nI walk to ___.",
            "examples": [
                ("I go to school by bus.", "+"),
                ("She goes by car.", "+"),
                ("He walks to school.", "+"),
                ("We go by train.", "+"),
            ],
            "exercises": [
                ("I go to school _____ bus.", "by"),
                ("She _____ to school. (walk)", "walks"),
                ("We go _____ car.", "by"),
                ("Tom goes to school _____ bike.", "by"),
            ],
        },
        6: {
            "title": "Simple present: I + verb",
            "rule": "Use simple present for things you do every day. Use the base verb with I/you/we/they.",
            "formula": "I wake up / eat / go / play.\nI don't + verb.",
            "examples": [
                ("I wake up at seven.", "+"),
                ("I eat breakfast.", "+"),
                ("I go to school.", "+"),
                ("I don't watch TV in the morning.", "-"),
            ],
            "exercises": [
                ("I _____ up at seven. (wake)", "wake"),
                ("I _____ my teeth. (brush)", "brush"),
                ("I _____ to school at eight. (go)", "go"),
                ("I _____ play after dinner. (negative)", "don't"),
            ],
        },
        7: {
            "title": "I can / I can't",
            "rule": "Use 'can' for things you are able to do. Use 'can't' for things you cannot do.",
            "formula": "I can ___.\nI can't ___.\nCan you ___?",
            "examples": [
                ("I can run.", "+"),
                ("I can't fly.", "-"),
                ("Can you swim?", "?"),
                ("She can jump.", "+"),
            ],
            "exercises": [
                ("I _____ run fast.", "can"),
                ("I _____ fly. (negative)", "can't"),
                ("_____ you swim?", "Can"),
                ("He _____ kick a ball.", "can"),
            ],
        },
        8: {
            "title": "Can I have ___?",
            "rule": "Use 'Can I have' to ask for things politely. Say 'please' and 'thank you'.",
            "formula": "Can I have a ___, please?\nHere you are. / Thank you.",
            "examples": [
                ("Can I have an apple, please?", "?"),
                ("Here you are!", "+"),
                ("Can I have water, please?", "?"),
                ("Thank you!", "+"),
            ],
            "exercises": [
                ("_____ I have a banana, please?", "Can"),
                ("Can I _____ an ice cream?", "have"),
                ("Here you _____!", "are"),
                ("_____ you!", "Thank"),
            ],
        },
        9: {
            "title": "He is / She is",
            "rule": "Use 'he is' for a man or boy. Use 'she is' for a woman or girl.",
            "formula": "He is a ___.\nShe is a ___.\nIs he/she a ___?",
            "examples": [
                ("He is a doctor.", "+"),
                ("She is a teacher.", "+"),
                ("Is he a firefighter?", "?"),
                ("She is kind.", "+"),
            ],
            "exercises": [
                ("_____ is a police officer. (boy)", "He"),
                ("_____ is a nurse. (girl)", "She"),
                ("He _____ a farmer.", "is"),
                ("_____ she a doctor?", "Is"),
            ],
        },
        10: {
            "title": "I am + feeling / It is + weather",
            "rule": "Use 'I am' to say how you feel. Use 'It is' to say the weather.",
            "formula": "I am happy/sad/hot.\nIt is sunny/rainy/cold.",
            "examples": [
                ("I am happy.", "+"),
                ("It is sunny.", "+"),
                ("I am hot!", "+"),
                ("It is rainy today.", "+"),
            ],
            "exercises": [
                ("I _____ happy today.", "am"),
                ("It _____ sunny outside.", "is"),
                ("I am _____. (sad/pencil)", "sad"),
                ("_____ is cold in winter.", "It"),
            ],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 5. SONG BANK — 10 songs / chants
# ══════════════════════════════════════════════════════════════════════════════

SONG_BANK = {
    1: {
        1: {
            "title": "Hello, What's Your Name?",
            "type": "Song",
            "lyrics": (
                "Hello, hello, what's your name?\n"
                "Hello, hello, what's your name?\n"
                "My name is ___, my name is ___,\n"
                "Nice to meet you!\n\n"
                "Goodbye, goodbye, see you soon!\n"
                "Goodbye, goodbye, see you soon!\n"
                "One, two, three, four, five,\n"
                "Six, seven, eight, nine, ten!"
            ),
            "activity": "Stand in a circle. When you sing, say your name and wave. Count on your fingers at the end.",
        },
        2: {
            "title": "The Family Song",
            "type": "Song",
            "lyrics": (
                "This is my mum, this is my dad,\n"
                "This is my sister, I am glad!\n"
                "This is my brother, small and sweet,\n"
                "This is my family, can't be beat!\n\n"
                "I love my mum, I love my dad,\n"
                "I love my family, I am glad!\n"
                "Clap your hands, stamp your feet,\n"
                "Family, family, can't be beat!"
            ),
            "activity": "Hold up family finger puppets or photos while singing each line.",
        },
        3: {
            "title": "The Animal Parade",
            "type": "Chant",
            "lyrics": (
                "Cat, cat, meow meow meow!\n"
                "Dog, dog, woof woof woof!\n"
                "Bird, bird, tweet tweet tweet!\n"
                "Fish, fish, splash splash splash!\n\n"
                "Cow, cow, moo moo moo!\n"
                "Duck, duck, quack quack quack!\n"
                "Horse, horse, clip clop clip!\n"
                "Animals, animals, I like that!"
            ),
            "activity": "Make the animal sounds and do the actions. Walk like each animal around the room.",
        },
        4: {
            "title": "My House Chant",
            "type": "Chant",
            "lyrics": (
                "This is my house, come inside!\n"
                "Kitchen, bedroom, open wide!\n"
                "Living room, bathroom too,\n"
                "Garden, garden, flowers grew!\n\n"
                "Bed and table, chair and door,\n"
                "Toys and books upon the floor!\n"
                "This is my house, it's so nice,\n"
                "Come and visit once or twice!"
            ),
            "activity": "Point to pictures of rooms. Pretend to open a door and walk into each room.",
        },
        5: {
            "title": "Wheels on the Bus",
            "type": "Song",
            "lyrics": (
                "The wheels on the bus go round and round,\n"
                "Round and round, round and round!\n"
                "The wheels on the bus go round and round,\n"
                "All through the town!\n\n"
                "The driver on the bus says 'Move along!'\n"
                "The children on the bus say 'Let us sing!'\n"
                "The horn on the bus goes beep beep beep!\n"
                "All through the town!"
            ),
            "activity": "Do the wheel motion with your arms. Pretend to drive and beep the horn.",
        },
        6: {
            "title": "Days of the Week",
            "type": "Rap",
            "lyrics": (
                "Monday, Tuesday, here we go! (clap clap)\n"
                "Wednesday, Thursday, say hello! (clap clap)\n"
                "Friday, Friday, almost done! (clap clap)\n"
                "Saturday, Sunday, time for fun! (clap clap)\n\n"
                "Seven days, seven days,\n"
                "In a week, in a week!\n"
                "Seven days, seven days,\n"
                "Let us speak, let us speak!"
            ),
            "activity": "Clap the rhythm and point to the day cards on the wall. March around for each day.",
        },
        7: {
            "title": "I Can Do It!",
            "type": "Song",
            "lyrics": (
                "I can run, I can jump,\n"
                "I can kick, I can pump!\n"
                "I can swim, I can throw,\n"
                "Ready, steady, let us go!\n\n"
                "Can you run? Yes, I can!\n"
                "Can you jump? Yes, I can!\n"
                "Can you swim? Yes, I can!\n"
                "I can, I can, yes I can!"
            ),
            "activity": "Do each action as you sing. Ask friends 'Can you ___?' and do it together.",
        },
        8: {
            "title": "The Shopping Song",
            "type": "Song",
            "lyrics": (
                "Can I have an apple, please?\n"
                "Here you are! Here you are!\n"
                "Can I have a banana, please?\n"
                "Here you are! Thank you!\n\n"
                "Apples, bananas, oranges too,\n"
                "Grapes and strawberries just for you!\n"
                "Yummy, yummy in my tummy,\n"
                "Healthy food is really yummy!"
            ),
            "activity": "Set up a pretend shop. Take turns being the shopkeeper and the customer.",
        },
        9: {
            "title": "The Helper Song",
            "type": "Chant",
            "lyrics": (
                "Doctor, doctor, helps you feel well!\n"
                "Teacher, teacher, has a story to tell!\n"
                "Firefighter, firefighter, brave and strong!\n"
                "Police officer, police officer, all day long!\n\n"
                "Nurse, nurse, kind and caring!\n"
                "Farmer, farmer, always sharing!\n"
                "Thank you, helpers, big and small,\n"
                "We love you, we love you all!"
            ),
            "activity": "Pretend to be each helper. Put on pretend hats and act out the job.",
        },
        10: {
            "title": "Summer Goodbye",
            "type": "Song",
            "lyrics": (
                "Goodbye school, hello sun!\n"
                "Summer, summer, here we come!\n"
                "Beach and ice cream, sand and sea,\n"
                "Summer, summer, you and me!\n\n"
                "Goodbye friends, see you soon,\n"
                "See you under the summer moon!\n"
                "We learned and played all year long,\n"
                "Now let us sing the goodbye song!"
            ),
            "activity": "Wave goodbye to friends. Draw a picture of what you will do in summer.",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 6. CULTURE CORNER BANK — 10 culture notes (2-3 sentences)
# ══════════════════════════════════════════════════════════════════════════════

CULTURE_CORNER_BANK = {
    1: {
        1: {
            "title": "Greetings Around the World",
            "text": (
                "People say hello in many ways! In Japan, people bow. "
                "In France, people kiss cheeks. In Turkey, children kiss the hand of elders. "
                "In England, people shake hands and say 'Hello!'"
            ),
            "question": "How do you say hello in your family?",
            "country_flag": "JP, FR, TR, GB",
            "recipe": None,
        },
        2: {
            "title": "Families Big and Small",
            "text": (
                "Families are different everywhere! In Turkey, grandparents often live with the family. "
                "In China, families can be very big. In some countries, families are small. "
                "All families love each other!"
            ),
            "question": "How many people are in your family?",
            "country_flag": "TR, CN",
            "recipe": None,
        },
        3: {
            "title": "Pets Around the World",
            "text": (
                "Many children have pets! In England, dogs and cats are popular pets. "
                "In Japan, people keep fish as pets. In Australia, some people have pet kangaroos! "
                "In Turkey, cats are loved in every city."
            ),
            "question": "Do you have a pet? What kind?",
            "country_flag": "GB, JP, AU, TR",
            "recipe": None,
        },
        4: {
            "title": "Houses Around the World",
            "text": (
                "Houses look different in every country! In Turkey, old houses are colourful. "
                "In Japan, some houses have paper doors. In Africa, some houses are round. "
                "Every house is a home!"
            ),
            "question": "What does your house look like?",
            "country_flag": "TR, JP",
            "recipe": None,
        },
        5: {
            "title": "How Children Go to School",
            "text": (
                "Children go to school in many ways! In Holland, children ride bikes. "
                "In Japan, children walk in groups. In some places, children go by boat! "
                "In Turkey, many children go by school bus or walk."
            ),
            "question": "How do you go to school?",
            "country_flag": "NL, JP, TR",
            "recipe": None,
        },
        6: {
            "title": "School Around the World",
            "text": (
                "Schools are different everywhere! In England, children wear uniforms. "
                "In Finland, school starts at nine o'clock. In Brazil, some children have school in the afternoon. "
                "In Turkey, school starts at half past eight."
            ),
            "question": "What time does your school start?",
            "country_flag": "GB, FI, BR, TR",
            "recipe": None,
        },
        7: {
            "title": "Popular Sports",
            "text": (
                "Every country loves sport! In Brazil, everyone plays football. "
                "In America, baseball and basketball are very popular. In India, people love cricket. "
                "In Turkey, football is the most popular sport."
            ),
            "question": "What is your favourite sport?",
            "country_flag": "BR, US, IN, TR",
            "recipe": None,
        },
        8: {
            "title": "Markets and Bazaars",
            "text": (
                "People buy food in different places! In Turkey, there are open bazaars with fresh fruit. "
                "In England, people go to supermarkets. In Morocco, bazaars have many colours and smells. "
                "Shopping is fun everywhere!"
            ),
            "question": "Where does your family buy food?",
            "country_flag": "TR, GB, MA",
            "recipe": None,
        },
        9: {
            "title": "Firefighters Around the World",
            "text": (
                "Firefighters are heroes everywhere! In America, fire trucks are big and red. "
                "In Japan, firefighters practise on very tall towers. In Turkey, we call 110 for the fire service. "
                "Firefighters are brave and help everyone!"
            ),
            "question": "What number do you call for firefighters in Turkey?",
            "country_flag": "US, JP, TR",
            "recipe": None,
        },
        10: {
            "title": "Summer Holidays",
            "text": (
                "Children love summer holidays! In Turkey, many families go to the seaside. "
                "In Italy, children eat gelato every day in summer. In Australia, summer is in December! "
                "Summer is a time for fun and family."
            ),
            "question": "What do you do in summer?",
            "country_flag": "TR, IT, AU",
            "recipe": None,
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 7. PROJECT BANK — 10 craft / activity projects
# ══════════════════════════════════════════════════════════════════════════════

PROJECT_BANK = {
    1: {
        1: {
            "title": "My Hello Card",
            "desc": "Make a card to give to a new friend that says hello!",
            "steps": [
                "Fold a piece of card in half.",
                "Write 'Hello! My name is ___' on the front.",
                "Draw a picture of yourself inside.",
                "Colour it with your favourite colours.",
                "Give the card to a friend and say hello!",
            ],
            "materials": "Card, crayons, pencils, stickers",
        },
        2: {
            "title": "Family Tree Poster",
            "desc": "Make a family tree with pictures of your family!",
            "steps": [
                "Draw a big tree on paper.",
                "Draw or stick photos of your family on the branches.",
                "Write 'mum', 'dad', 'sister', 'brother' under each picture.",
                "Decorate with hearts and flowers.",
                "Present your family tree: 'This is my mum. Her name is ___.'",
            ],
            "materials": "Large paper, family photos or drawings, glue, crayons",
        },
        3: {
            "title": "Animal Mask",
            "desc": "Make an animal mask and act like that animal!",
            "steps": [
                "Choose your favourite animal.",
                "Draw the animal face on card.",
                "Cut it out and cut eye holes.",
                "Colour and decorate your mask.",
                "Wear it and make the animal sound: 'I am a ___! ___!'",
            ],
            "materials": "Card, scissors, crayons, elastic band, glue",
        },
        4: {
            "title": "My Dream House",
            "desc": "Build a model of your dream house from a shoebox!",
            "steps": [
                "Use a shoebox as the house.",
                "Cut a door and windows.",
                "Make furniture from small boxes and card.",
                "Label each room: kitchen, bedroom, bathroom.",
                "Show your house: 'This is the kitchen. There is a table.'",
            ],
            "materials": "Shoebox, small boxes, card, scissors, glue, crayons",
        },
        5: {
            "title": "Transport Collage",
            "desc": "Make a collage of different transport from magazines!",
            "steps": [
                "Find pictures of transport in magazines.",
                "Cut them out carefully.",
                "Stick them on a big paper in groups: road, sky, sea.",
                "Write the English name under each: bus, plane, boat.",
                "Show your collage: 'This is a bus. I go by bus.'",
            ],
            "materials": "Old magazines, scissors, glue, large paper, markers",
        },
        6: {
            "title": "My Weekly Timetable",
            "desc": "Make a colourful timetable of your school week!",
            "steps": [
                "Draw a table with 5 columns for Monday to Friday.",
                "Write each day at the top.",
                "Draw or write your lessons for each day.",
                "Colour each subject a different colour.",
                "Tell your partner: 'On Monday I have ___.'",
            ],
            "materials": "Paper, ruler, crayons, coloured pencils",
        },
        7: {
            "title": "Sports Day Trophy",
            "desc": "Make a trophy cup for Sports Day!",
            "steps": [
                "Cut a cup shape from yellow card.",
                "Write 'Sports Day Champion' on it.",
                "Decorate with stars and glitter.",
                "Tape a stick to the back as a handle.",
                "Hold it up and say: 'I can run! I can jump! I am the champion!'",
            ],
            "materials": "Yellow card, scissors, glitter, star stickers, tape, stick",
        },
        8: {
            "title": "Healthy Food Plate",
            "desc": "Make a paper plate showing healthy food!",
            "steps": [
                "Draw a big circle on paper as your plate.",
                "Divide it into four parts.",
                "Draw fruit, vegetables, bread and milk in each part.",
                "Label each food in English.",
                "Present: 'I eat apples. I drink milk. This is healthy!'",
            ],
            "materials": "Paper plate or paper, crayons, markers",
        },
        9: {
            "title": "Helper Puppets",
            "desc": "Make stick puppets of community helpers!",
            "steps": [
                "Draw a doctor, firefighter, teacher, nurse and police officer on card.",
                "Colour them and cut them out.",
                "Tape a stick to the back of each.",
                "Use your puppets to act out a story.",
                "Say: 'I am a doctor. I help sick people.'",
            ],
            "materials": "Card, crayons, scissors, tape, sticks",
        },
        10: {
            "title": "My Year Book",
            "desc": "Make a mini book about everything you learned this year!",
            "steps": [
                "Fold 5 papers in half and staple them.",
                "On each page, draw something you learned: colours, animals, family, etc.",
                "Write the English word under each picture.",
                "Decorate the cover with your name and stars.",
                "Show your book to your family: 'I learned English!'",
            ],
            "materials": "Paper, stapler, crayons, stickers, pencils",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 8. LISTENING SCRIPT BANK — 10 scripts + 3 tasks each
# ══════════════════════════════════════════════════════════════════════════════

LISTENING_SCRIPT_BANK = {
    1: {
        1: {
            "title": "Hello and Goodbye",
            "script": (
                "Narrator: Listen and point to the correct picture.\n\n"
                "Mr. Sun: Good morning, children!\n"
                "Children: Good morning, Mr. Sun!\n"
                "Mr. Sun: What is your name?\n"
                "Lily: My name is Lily. Hello!\n"
                "Mr. Sun: Hello, Lily! And you?\n"
                "Tom: Hi! My name is Tom.\n"
                "Mr. Sun: Now let us count! One, two, three!\n"
                "Children: Four, five, six, seven, eight, nine, ten!"
            ),
            "tasks": [
                "Point to the child who says 'My name is Lily.'",
                "Count from one to ten with the children.",
                "Say hello and goodbye to your partner.",
            ],
        },
        2: {
            "title": "My Family",
            "script": (
                "Narrator: Listen and circle the correct family member.\n\n"
                "Lily: This is my family. This is my mum.\n"
                "Mr. Sun: What is her name?\n"
                "Lily: Her name is Ayse.\n"
                "Mr. Sun: And your dad?\n"
                "Lily: This is my dad. His name is Ali.\n"
                "Mr. Sun: Do you have a sister?\n"
                "Lily: Yes! This is my sister, Eda. She is five.\n"
                "Mr. Sun: What a lovely family!"
            ),
            "tasks": [
                "Circle Lily's mum in the picture.",
                "How old is Lily's sister?",
                "Draw your family and tell a friend.",
            ],
        },
        3: {
            "title": "Animal Sounds",
            "script": (
                "Narrator: Listen to the sounds. What animal is it?\n\n"
                "Mr. Sun: Listen! What is this? (Meow!)\n"
                "Children: A cat!\n"
                "Mr. Sun: And this? (Woof woof!)\n"
                "Children: A dog!\n"
                "Mr. Sun: This one? (Moo!)\n"
                "Children: A cow!\n"
                "Mr. Sun: Last one! (Quack quack!)\n"
                "Children: A duck!\n"
                "Mr. Sun: Very good! You know your animals!"
            ),
            "tasks": [
                "Match each sound to the animal picture.",
                "Which animal says 'Moo'?",
                "Make an animal sound for your friend to guess.",
            ],
        },
        4: {
            "title": "In My Room",
            "script": (
                "Narrator: Listen and tick the things you hear.\n\n"
                "Tom: This is my bedroom. I have a big bed.\n"
                "Mr. Sun: What colour is your bed?\n"
                "Tom: It is blue. I have a desk too. And a chair.\n"
                "Mr. Sun: What is on your desk?\n"
                "Tom: My books and my pencils. Oh, and a teddy bear!\n"
                "Mr. Sun: Very nice room, Tom!"
            ),
            "tasks": [
                "Tick: bed, desk, chair, books, teddy bear.",
                "What colour is Tom's bed?",
                "What is on Tom's desk?",
            ],
        },
        5: {
            "title": "How Do You Go to School?",
            "script": (
                "Narrator: Listen and draw a line to the correct transport.\n\n"
                "Mr. Sun: How do you go to school, Lily?\n"
                "Lily: I walk to school.\n"
                "Mr. Sun: And you, Tom?\n"
                "Tom: I go by bus.\n"
                "Mr. Sun: How about Eda?\n"
                "Lily: She goes by car with my dad.\n"
                "Mr. Sun: Do you see any planes?\n"
                "Tom: Yes! There is a plane in the sky! It is big!"
            ),
            "tasks": [
                "Draw a line: Lily - walking, Tom - bus, Eda - car.",
                "What does Tom see in the sky?",
                "How do you go to school? Tell a friend.",
            ],
        },
        6: {
            "title": "My School Day",
            "script": (
                "Narrator: Listen and number the pictures in order.\n\n"
                "Lily: I wake up at seven. I brush my teeth.\n"
                "Then I eat breakfast. I eat bread and cheese.\n"
                "I go to school at eight. Today is Monday.\n"
                "I have English today. I love English!\n"
                "School finishes at three. I go home.\n"
                "I play with Buddy in the garden."
            ),
            "tasks": [
                "Number the pictures: 1-wake up, 2-breakfast, 3-school, 4-play.",
                "What day is it?",
                "What does Lily eat for breakfast?",
            ],
        },
        7: {
            "title": "Sports Day",
            "script": (
                "Narrator: Listen and tick the sports you hear.\n\n"
                "Mr. Sun: Today is Sports Day! Are you ready?\n"
                "Tom: Yes! I can run fast!\n"
                "Lily: I can jump high!\n"
                "Mr. Sun: First, we run! Ready, set, go!\n"
                "Mr. Sun: Now, kick the ball! Football!\n"
                "Tom: I love football!\n"
                "Mr. Sun: Now throw the ball! Basketball!\n"
                "Lily: I like basketball!\n"
                "Mr. Sun: Well done, everyone!"
            ),
            "tasks": [
                "Tick the sports: running, football, basketball.",
                "Who likes football — Lily or Tom?",
                "What sport do you like? Tell a friend.",
            ],
        },
        8: {
            "title": "At the Fruit Shop",
            "script": (
                "Narrator: Listen and colour the fruit.\n\n"
                "Lily: Can I have an apple, please?\n"
                "Shopkeeper: Here you are! A red apple.\n"
                "Tom: Can I have a banana, please?\n"
                "Shopkeeper: Here you are! A yellow banana.\n"
                "Lily: And two oranges, please!\n"
                "Shopkeeper: Two oranges. Here you are!\n"
                "Tom: Thank you!\n"
                "Shopkeeper: You are welcome!"
            ),
            "tasks": [
                "Colour the apple red and the banana yellow.",
                "How many oranges do they buy?",
                "Practise: 'Can I have a ___, please?'",
            ],
        },
        9: {
            "title": "Who Helps Us?",
            "script": (
                "Narrator: Listen and match the helper to the picture.\n\n"
                "Mr. Sun: Who helps when you are sick?\n"
                "Children: The doctor!\n"
                "Mr. Sun: Who teaches you at school?\n"
                "Children: The teacher!\n"
                "Mr. Sun: Who puts out fires?\n"
                "Children: The firefighter!\n"
                "Mr. Sun: Who keeps us safe?\n"
                "Children: The police officer!\n"
                "Mr. Sun: Who helps in the hospital too?\n"
                "Children: The nurse!"
            ),
            "tasks": [
                "Match each helper to their picture.",
                "Who puts out fires?",
                "Draw a helper you want to be.",
            ],
        },
        10: {
            "title": "Goodbye, School!",
            "script": (
                "Narrator: Listen to the goodbye messages.\n\n"
                "Lily: Goodbye, Tom! Have a nice summer!\n"
                "Tom: Goodbye, Lily! See you in September!\n"
                "Lily: I will go to the beach!\n"
                "Tom: I will visit my grandma!\n"
                "Mr. Sun: Goodbye, children! You are all stars!\n"
                "Everyone: Goodbye, Mr. Sun! Thank you!\n"
                "Buddy: Woof woof!\n"
                "Bella: See you! See you!"
            ),
            "tasks": [
                "Who will go to the beach?",
                "When will they see each other again?",
                "Say goodbye to your friends in English.",
            ],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 9. MODEL WRITING BANK — 10 models (2-3 sentences)
# ══════════════════════════════════════════════════════════════════════════════

MODEL_WRITING_BANK = {
    1: {
        1: {
            "type": "Label",
            "title": "About Me",
            "text": "My name is Lily. I am seven. I go to school.",
            "task": "Write three sentences about you: your name, your age, your school.",
        },
        2: {
            "type": "Label",
            "title": "My Family",
            "text": "This is my mum. Her name is Ayse. I love my family.",
            "task": "Write about one person in your family. Use 'This is my ___.'",
        },
        3: {
            "type": "Label",
            "title": "My Pet",
            "text": "I have a cat. My cat is white. I like my cat.",
            "task": "Write about an animal you like. Use 'I have / I like'.",
        },
        4: {
            "type": "Label",
            "title": "My Room",
            "text": "This is my room. There is a bed. There is a desk.",
            "task": "Write about your room. Use 'There is a ___.'",
        },
        5: {
            "type": "Label",
            "title": "How I Go to School",
            "text": "I go to school by bus. The bus is yellow. I like the bus.",
            "task": "Write how you go to school. Use 'I go by ___.'",
        },
        6: {
            "type": "Label",
            "title": "My Monday",
            "text": "Today is Monday. I have English. I like English.",
            "task": "Write about one day. Use 'Today is ___. I have ___.'",
        },
        7: {
            "type": "Label",
            "title": "I Can!",
            "text": "I can run. I can jump. I can swim.",
            "task": "Write three things you can do. Use 'I can ___.'",
        },
        8: {
            "type": "Label",
            "title": "At the Shop",
            "text": "I like apples. I like bananas. They are yummy.",
            "task": "Write about two foods you like. Use 'I like ___.'",
        },
        9: {
            "type": "Label",
            "title": "A Helper",
            "text": "He is a doctor. He helps people. He is kind.",
            "task": "Write about a helper. Use 'He/She is a ___.'",
        },
        10: {
            "type": "Label",
            "title": "Summer",
            "text": "It is summer. I go to the beach. I am happy.",
            "task": "Write about summer. Use 'It is ___. I go to ___.'",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 10. FUN FACTS BANK — 10 x 3 fun facts
# ══════════════════════════════════════════════════════════════════════════════

FUN_FACTS_BANK = {
    1: {
        1: [
            "People say hello in over 7,000 languages!",
            "The word 'hello' was first used about 200 years ago!",
            "In some countries, children bow to say hello!",
        ],
        2: [
            "Elephants live in big families with grandmas too!",
            "Sea horses — the dad takes care of the babies!",
            "Penguins stay with the same partner forever!",
        ],
        3: [
            "A cat sleeps about 16 hours a day!",
            "Dogs can understand about 250 words!",
            "A parrot can live for 80 years!",
        ],
        4: [
            "The biggest house in the world has 27 floors!",
            "Some houses in Turkey are in caves!",
            "In Japan, some houses can move during earthquakes!",
        ],
        5: [
            "The fastest train can go 600 kilometres per hour!",
            "The first car was made in 1886!",
            "Some school buses are boats!",
        ],
        6: [
            "In some countries, children go to school on Saturdays!",
            "The word 'Monday' means 'Moon day'!",
            "Children in Finland do not start school until age seven!",
        ],
        7: [
            "Running is the oldest sport in the world!",
            "A football is made of 32 pieces!",
            "Swimming is one of the best exercises for your body!",
        ],
        8: [
            "Bananas are actually berries!",
            "Strawberries have about 200 seeds on the outside!",
            "Carrots were first purple, not orange!",
        ],
        9: [
            "Firefighters used to slide down poles to save time!",
            "The first nurses helped soldiers in wars!",
            "Police dogs can find people by smell!",
        ],
        10: [
            "The longest summer holiday in the world is 14 weeks!",
            "In Australia, Christmas is in summer!",
            "Ice cream was invented in China over 2,000 years ago!",
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 11. GAMIFICATION BANK — levels, 10 badges, bonus XP
# ══════════════════════════════════════════════════════════════════════════════

GAMIFICATION_BANK = {
    1: {
        "levels": [
            {"name": "Little Learner", "xp_min": 0, "xp_max": 49, "icon": "🌱"},
            {"name": "Rising Star", "xp_min": 50, "xp_max": 149, "icon": "⭐"},
            {"name": "Super Student", "xp_min": 150, "xp_max": 299, "icon": "🌟"},
            {"name": "English Champion", "xp_min": 300, "xp_max": 500, "icon": "🏆"},
        ],
        "unit_badges": {
            1: {"badge": "Hello Hero", "desc": "Say hello and goodbye to 5 people in English!", "xp": 20},
            2: {"badge": "Family Star", "desc": "Name all your family members in English!", "xp": 20},
            3: {"badge": "Animal Friend", "desc": "Name 8 animals and make their sounds!", "xp": 25},
            4: {"badge": "House Builder", "desc": "Name 5 rooms and 5 furniture items!", "xp": 25},
            5: {"badge": "Travel Expert", "desc": "Name 5 types of transport in English!", "xp": 20},
            6: {"badge": "Routine Master", "desc": "Say all 7 days and describe your routine!", "xp": 25},
            7: {"badge": "Sports Champion", "desc": "Name 5 sports and say 'I can ___!'", "xp": 25},
            8: {"badge": "Healthy Eater", "desc": "Name 8 healthy foods in English!", "xp": 20},
            9: {"badge": "Community Helper", "desc": "Name 5 helpers and say what they do!", "xp": 25},
            10: {"badge": "Year-End Graduate", "desc": "Complete all units and sing the goodbye song!", "xp": 30},
        },
        "bonus_xp": [
            {"action": "Sing a song perfectly in English", "xp": 10},
            {"action": "Help a friend learn 3 new words", "xp": 10},
            {"action": "Say 5 English words at home to family", "xp": 10},
            {"action": "Draw a picture and label it in English", "xp": 15},
            {"action": "Read a short English sentence out loud", "xp": 15},
        ],
    },
}

# ---------------------------------------------------------------------------
# PROGRESS CHECK BANK  (Review questions per unit, ages 6-7)
# ---------------------------------------------------------------------------
PROGRESS_CHECK_BANK = {
    1: {
        1: {
            "vocab": ["hello", "goodbye", "teacher", "school", "pencil", "book", "desk", "red", "blue", "seven"],
            "grammar": ["This is a ___.", "What is this? It is a ___.", "My name is ___."],
            "reading": ["What is the girl's name?", "How old is Lily?", "Who is Mr. Sun?"],
            "writing": ["Write 'Hello! My name is ___.'", "Draw your classroom and label two things."],
        },
        2: {
            "vocab": ["mother", "father", "sister", "brother", "baby", "family", "grandma", "grandpa", "tall", "kind"],
            "grammar": ["I have a ___.", "You have a ___.", "Do you have a ___?"],
            "reading": ["How old is Eda?", "Who makes cookies?", "Is Can a baby?"],
            "writing": ["Write about your family: 'I have a ___ and a ___.'", "Draw your family."],
        },
        3: {
            "vocab": ["cat", "dog", "fish", "bird", "rabbit", "big", "small", "white", "orange", "like"],
            "grammar": ["I like ___.", "I don't like ___.", "Do you like ___?"],
            "reading": ["What colour is the cat?", "How many fish are in the tank?", "What colour is Bella?"],
            "writing": ["Write 'I like ___.' with an animal.", "Draw your favourite animal and label it."],
        },
        4: {
            "vocab": ["house", "bedroom", "kitchen", "door", "window", "bed", "table", "chair", "garden", "sofa"],
            "grammar": ["There is a ___.", "There are two ___.", "Is there a ___?"],
            "reading": ["What colour is the door?", "What colour is the bed?", "Is the house big or small?"],
            "writing": ["Write 'There is a ___ in my house.'", "Draw your bedroom and label three things."],
        },
        5: {
            "vocab": ["bus", "car", "bike", "walk", "train", "go", "school", "fast", "slow", "stop"],
            "grammar": ["I go by ___.", "She goes by ___.", "How do you go to school?"],
            "reading": ["How does Tom go to school?", "Is the bus fast or slow?", "What is the weather?"],
            "writing": ["Write 'I go to school by ___.'", "Draw your way to school."],
        },
        6: {
            "vocab": ["Monday", "Tuesday", "morning", "afternoon", "lunch", "Maths", "English", "Art", "read", "write"],
            "grammar": ["I ___ every day.", "She ___ in the morning.", "Do you ___ at school?"],
            "reading": ["What day is it?", "What does Tom do in the morning?", "What is his favourite subject?"],
            "writing": ["Write 'On Monday I have ___.'", "Draw your school timetable for one day."],
        },
        7: {
            "vocab": ["football", "basketball", "run", "jump", "swim", "play", "catch", "throw", "fast", "winner"],
            "grammar": ["I can ___.", "I can't ___.", "Can you ___?"],
            "reading": ["What sport does Tom play?", "Can Lily swim?", "Who is the winner?"],
            "writing": ["Write 'I can ___ and I can ___.'", "Draw yourself playing a sport."],
        },
        8: {
            "vocab": ["park", "shop", "tree", "flower", "ice cream", "apple", "bread", "buy", "please", "thank you"],
            "grammar": ["Can I have ___, please?", "Here you are.", "Thank you!"],
            "reading": ["Where do they go?", "What does Lily buy?", "Is the park big?"],
            "writing": ["Write 'Can I have ___, please?'", "Draw a shop and label three things you can buy."],
        },
        9: {
            "vocab": ["doctor", "teacher", "police officer", "fire fighter", "farmer", "nurse", "help", "kind", "brave", "work"],
            "grammar": ["He is a ___.", "She is a ___.", "What do you want to be?"],
            "reading": ["Who helps sick people?", "What does the farmer do?", "Is the fire fighter brave?"],
            "writing": ["Write 'I want to be a ___.'", "Draw a helper and write what they do."],
        },
        10: {
            "vocab": ["summer", "holiday", "beach", "swim", "happy", "sun", "play", "friend", "goodbye", "see you"],
            "grammar": ["I am ___.", "It is ___.", "I feel ___."],
            "reading": ["Where do they go in summer?", "Is everyone happy?", "What do they do at the beach?"],
            "writing": ["Write 'In summer I like to ___.'", "Draw your favourite summer activity."],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 13. DIALOGUE BANK — short 3-5 line dialogues per unit
# ══════════════════════════════════════════════════════════════════════════════

DIALOGUE_BANK = {
    1: {
        1: {
            "setting": "First day at school – classroom door",
            "characters": ["Lily", "Tom", "Mr. Sun"],
            "lines": [
                ("Lily", "Hello! I am Lily."),
                ("Tom", "Hi, Lily! I am Tom."),
                ("Mr. Sun", "Good morning, children! Welcome to school!"),
                ("Lily", "Good morning, Mr. Sun!"),
                ("Tom", "Good morning!"),
            ],
            "focus_language": "Hello / Hi / Good morning / I am ___.",
            "task": "Practise with a partner. Say hello and tell your name.",
        },
        2: {
            "setting": "Maths corner – counting table",
            "characters": ["Lily", "Tom"],
            "lines": [
                ("Lily", "How many apples? Let's count!"),
                ("Tom", "One, two, three, four, five!"),
                ("Lily", "Five apples! What shape is this?"),
                ("Tom", "It is a circle!"),
            ],
            "focus_language": "How many? / One to ten / What shape is this? / It is a ___.",
            "task": "Count objects on your desk. Tell your partner the number and shape.",
        },
        3: {
            "setting": "Art room – painting time",
            "characters": ["Lily", "Tom", "Bella"],
            "lines": [
                ("Lily", "What colour is this?"),
                ("Tom", "It is red!"),
                ("Bella", "Tweet! I see blue!"),
                ("Lily", "My pencil is yellow."),
                ("Tom", "I like green!"),
            ],
            "focus_language": "What colour is this? / It is ___. / I like ___.",
            "task": "Point to things in the classroom. Ask: 'What colour is this?'",
        },
        4: {
            "setting": "School tour – in the corridor",
            "characters": ["Lily", "Tom", "Mr. Sun"],
            "lines": [
                ("Mr. Sun", "This is the library."),
                ("Lily", "I like books!"),
                ("Tom", "Where is the playground?"),
                ("Mr. Sun", "It is over there!"),
                ("Tom", "Thank you, Mr. Sun!"),
            ],
            "focus_language": "This is ___. / Where is ___? / It is over there. / Thank you.",
            "task": "Walk around class. Point and say: 'This is the ___.'",
        },
        5: {
            "setting": "Lily's house – living room",
            "characters": ["Lily", "Tom"],
            "lines": [
                ("Lily", "This is my mum."),
                ("Tom", "Hello! Nice to meet you!"),
                ("Lily", "And this is my dad."),
                ("Tom", "Hi! I am Tom."),
                ("Lily", "We are a happy family!"),
            ],
            "focus_language": "This is my ___. / Nice to meet you! / We are ___.",
            "task": "Draw your family. Tell your partner: 'This is my ___.'",
        },
        6: {
            "setting": "School canteen – lunch time",
            "characters": ["Lily", "Tom", "Buddy"],
            "lines": [
                ("Lily", "I like apples. Do you like apples?"),
                ("Tom", "Yes! I like bananas too."),
                ("Lily", "Look! Carrots and tomatoes!"),
                ("Tom", "Yummy! I like carrots."),
                ("Buddy", "Woof! Woof!"),
            ],
            "focus_language": "I like ___. / Do you like ___? / Yes! / Yummy!",
            "task": "Ask your partner: 'Do you like ___?' Use fruit or vegetable words.",
        },
        7: {
            "setting": "Park – looking at animals",
            "characters": ["Lily", "Tom", "Bella"],
            "lines": [
                ("Tom", "Look! A cat!"),
                ("Lily", "It is small. I like cats."),
                ("Bella", "Tweet! I am a bird!"),
                ("Tom", "Can you see the dog?"),
                ("Lily", "Yes! It is big!"),
            ],
            "focus_language": "Look! A ___. / It is big/small. / Can you see ___?",
            "task": "Use animal flashcards. Say: 'Look! A ___! It is ___.'",
        },
        8: {
            "setting": "PE lesson – in the gym",
            "characters": ["Lily", "Tom", "Mr. Sun"],
            "lines": [
                ("Mr. Sun", "Touch your head!"),
                ("Lily", "This is my head!"),
                ("Mr. Sun", "Clap your hands!"),
                ("Tom", "One, two, three – clap!"),
                ("Mr. Sun", "Well done! Stamp your feet!"),
            ],
            "focus_language": "Touch your ___! / This is my ___. / Clap / Stamp.",
            "task": "Play 'Simon Says' with body parts. Listen and move!",
        },
        9: {
            "setting": "Classroom – morning circle",
            "characters": ["Lily", "Tom", "Mr. Sun"],
            "lines": [
                ("Mr. Sun", "What day is it today?"),
                ("Lily", "It is Monday!"),
                ("Mr. Sun", "What is the weather?"),
                ("Tom", "It is sunny!"),
                ("Lily", "I like sunny days!"),
            ],
            "focus_language": "What day is it? / It is ___. / What is the weather?",
            "task": "Look outside. Tell your partner the day and weather.",
        },
        10: {
            "setting": "Classroom – last day of school",
            "characters": ["Lily", "Tom", "Mr. Sun", "Bella", "Buddy"],
            "lines": [
                ("Mr. Sun", "It is the last day. Well done, everyone!"),
                ("Lily", "I am happy! Summer is here!"),
                ("Tom", "Goodbye, Mr. Sun! See you!"),
                ("Bella", "Tweet! Bye-bye!"),
                ("Buddy", "Woof!"),
            ],
            "focus_language": "Goodbye! / See you! / I am happy. / Summer is here.",
            "task": "Say goodbye to three friends. Use: 'Goodbye! See you!'",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 14. PRONUNCIATION BANK — target sounds, word lists, chants & TPR actions
# ══════════════════════════════════════════════════════════════════════════════

PRONUNCIATION_BANK = {
    1: {
        1: {
            "sound": "/h/ as in hello",
            "words": ["hello", "happy", "hat", "hand", "house"],
            "chant": "Hello, hello, happy hat! Hello, hello, clap-clap-clap!",
            "action": "Wave your hand every time you hear /h/.",
        },
        2: {
            "sound": "/n/ as in number",
            "words": ["number", "nine", "new", "nose", "nut"],
            "chant": "One, two, three – number fun! Four, five, six – we all run!",
            "action": "Tap the table for each number you say.",
        },
        3: {
            "sound": "/k/ as in colour",
            "words": ["colour", "cat", "cup", "car", "cake"],
            "chant": "Colour, colour, what do you see? Red and blue and yellow – three!",
            "action": "Hold up a coloured crayon when you hear /k/.",
        },
        4: {
            "sound": "/s/ as in school",
            "words": ["school", "sit", "sun", "star", "seven"],
            "chant": "School, school, time for school! Sit and learn – that's the rule!",
            "action": "Pretend to sit down on the /s/ sound.",
        },
        5: {
            "sound": "/m/ as in mum",
            "words": ["mum", "me", "my", "milk", "moon"],
            "chant": "My mum, my mum, I love my mum! Mmm-mmm-mmm – yum yum yum!",
            "action": "Rub your tummy and say 'Mmm' together.",
        },
        6: {
            "sound": "/f/ as in fruit",
            "words": ["fruit", "five", "fun", "fish", "foot"],
            "chant": "Fruit is fun! Fruit is yummy! Fruit is good inside my tummy!",
            "action": "Pretend to bite a fruit on each /f/ word.",
        },
        7: {
            "sound": "/æ/ as in cat",
            "words": ["cat", "bat", "hat", "rat", "map"],
            "chant": "Cat and bat, hat and rat – sit on the mat, just like that!",
            "action": "Wiggle your fingers like whiskers when you say /æ/.",
        },
        8: {
            "sound": "/b/ as in body",
            "words": ["body", "ball", "big", "book", "bed"],
            "chant": "Body, body, bounce the ball! Big and small – I love them all!",
            "action": "Bounce an imaginary ball for every /b/ word.",
        },
        9: {
            "sound": "/d/ as in day",
            "words": ["day", "dog", "duck", "door", "dance"],
            "chant": "Day by day, we dance and play! Monday, Tuesday – hooray!",
            "action": "Dance in place when you hear /d/.",
        },
        10: {
            "sound": "/s/ as in summer",
            "words": ["summer", "sun", "sea", "sand", "swim"],
            "chant": "Summer sun, summer fun! Swim and play – everyone!",
            "action": "Pretend to swim when you say the /s/ words.",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 15. WORKBOOK BANK — trace, match, circle activities per unit
# ══════════════════════════════════════════════════════════════════════════════

WORKBOOK_BANK = {
    1: {
        1: {
            "activities": [
                {"type": "trace", "instruction": "Trace the words: 'Hello' and 'Goodbye'."},
                {"type": "match", "instruction": "Match the picture to the greeting: Hello / Goodbye / Good morning."},
                {"type": "circle", "instruction": "Circle the happy face when people say 'Hello'."},
            ],
        },
        2: {
            "activities": [
                {"type": "trace", "instruction": "Trace the numbers 1 to 10."},
                {"type": "match", "instruction": "Match the number to the group of objects (e.g., 3 stars, 5 balls)."},
                {"type": "circle", "instruction": "Circle all the triangles in the picture."},
            ],
        },
        3: {
            "activities": [
                {"type": "trace", "instruction": "Trace the colour words: red, blue, yellow, green."},
                {"type": "match", "instruction": "Match the colour word to the correct crayon."},
                {"type": "circle", "instruction": "Circle the objects that are red."},
            ],
        },
        4: {
            "activities": [
                {"type": "trace", "instruction": "Trace: 'This is my school.'"},
                {"type": "match", "instruction": "Match the school place to its picture: classroom, library, playground."},
                {"type": "circle", "instruction": "Circle the things you can find in a classroom."},
            ],
        },
        5: {
            "activities": [
                {"type": "trace", "instruction": "Trace the family words: mum, dad, brother, sister."},
                {"type": "match", "instruction": "Match each family member to their picture."},
                {"type": "circle", "instruction": "Circle the family picture that has four people."},
            ],
        },
        6: {
            "activities": [
                {"type": "trace", "instruction": "Trace: apple, banana, carrot, tomato."},
                {"type": "match", "instruction": "Match the fruit/vegetable to its colour."},
                {"type": "circle", "instruction": "Circle all the fruits. Cross out the vegetables."},
            ],
        },
        7: {
            "activities": [
                {"type": "trace", "instruction": "Trace the animal words: cat, dog, bird, fish."},
                {"type": "match", "instruction": "Match the animal to the sound it makes."},
                {"type": "circle", "instruction": "Circle the animals that live on a farm."},
            ],
        },
        8: {
            "activities": [
                {"type": "trace", "instruction": "Trace the body parts: head, hand, foot, arm, leg."},
                {"type": "match", "instruction": "Match the body part word to the correct place on the picture."},
                {"type": "circle", "instruction": "Circle the body parts you use to clap."},
            ],
        },
        9: {
            "activities": [
                {"type": "trace", "instruction": "Trace the days: Monday, Tuesday, Wednesday."},
                {"type": "match", "instruction": "Match the weather word to the picture: sunny, rainy, cloudy."},
                {"type": "circle", "instruction": "Circle today's weather in the picture row."},
            ],
        },
        10: {
            "activities": [
                {"type": "trace", "instruction": "Trace: 'Happy Summer!' and 'Goodbye!'"},
                {"type": "match", "instruction": "Match the season word to the picture: summer, winter, spring."},
                {"type": "circle", "instruction": "Circle the things you do in summer: swim, play, read."},
            ],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 16. TURKEY CORNER BANK — fun facts about Türkiye per unit
# ══════════════════════════════════════════════════════════════════════════════

TURKEY_CORNER_BANK = {
    1: {
        1: {
            "title": "How Do Children in Türkiye Say Hello?",
            "fact": "In Türkiye, children say 'Merhaba!' to greet friends and teachers.",
            "activity": "Say 'Merhaba!' to five friends today. Then say 'Hello!' in English.",
        },
        2: {
            "title": "Numbers Everywhere!",
            "fact": "Turkish children count 'bir, iki, üç' just like you count 'one, two, three'!",
            "activity": "Count your crayons in English and then try in Turkish: bir, iki, üç!",
        },
        3: {
            "title": "The Colourful Bazaars",
            "fact": "In Türkiye, big markets called 'bazaars' are full of colourful things to buy.",
            "activity": "Draw a bazaar stall. Colour it red, blue, yellow and green. Label the colours in English.",
        },
        4: {
            "title": "Schools in Türkiye",
            "fact": "Children in Türkiye wear school uniforms and start school at age 6, just like you!",
            "activity": "Draw yourself in a school uniform. Write 'My School' on top.",
        },
        5: {
            "title": "Turkish Families Love Tea",
            "fact": "Families in Türkiye often drink tea together in small tulip-shaped glasses.",
            "activity": "Draw a tulip-shaped glass. Write 'My family drinks ___.' and fill the blank.",
        },
        6: {
            "title": "Delicious Turkish Fruits",
            "fact": "Türkiye grows lots of cherries, apricots and pomegranates!",
            "activity": "Draw a cherry, an apricot and a pomegranate. Label them in English.",
        },
        7: {
            "title": "Kangal Dogs of Türkiye",
            "fact": "The Kangal is a big, strong dog from Türkiye. It protects sheep on farms!",
            "activity": "Draw a Kangal dog. Write: 'It is big. It is strong.'",
        },
        8: {
            "title": "Turkish Children Love Football",
            "fact": "Football is the most popular sport in Türkiye. Children play it at every break time!",
            "activity": "Draw yourself playing football. Label: head, foot, hand.",
        },
        9: {
            "title": "Weather in Türkiye",
            "fact": "In Antalya it is sunny almost every day. In the east, it can snow a lot in winter!",
            "activity": "Draw two pictures: sunny Antalya and snowy east. Write the weather word.",
        },
        10: {
            "title": "Bayram – Time to Celebrate!",
            "fact": "During Bayram holidays, children visit family and get sweets and pocket money!",
            "activity": "Draw a Bayram celebration. Write 'Happy Bayram!' in your picture.",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 17. COMIC STRIP BANK — 3-4 panel comics per unit
# ══════════════════════════════════════════════════════════════════════════════

COMIC_STRIP_BANK = {
    1: {
        1: {
            "title": "Lily's First Day",
            "panels": [
                {"scene": "Lily stands at the school gate with her backpack.", "speech": "Hello! I am Lily!"},
                {"scene": "Tom waves from the classroom door.", "speech": "Hi! I am Tom! Come in!"},
                {"scene": "Mr. Sun smiles at the class.", "speech": "Good morning, everyone!"},
                {"scene": "All children wave and smile.", "speech": "Good morning, Mr. Sun!"},
            ],
            "drawing_task": "Draw yourself in panel 1. Write 'Hello! I am ___.'",
            "language_focus": "Greetings: Hello, Hi, Good morning, I am ___.",
        },
        2: {
            "title": "The Counting Race",
            "panels": [
                {"scene": "Lily and Tom look at a jar of marbles.", "speech": "How many marbles?"},
                {"scene": "Tom counts on his fingers.", "speech": "One, two, three, four, five!"},
                {"scene": "Lily holds up a triangle card.", "speech": "Look! A triangle!"},
                {"scene": "Both jump and cheer.", "speech": "We can count and name shapes!"},
            ],
            "drawing_task": "Draw a jar with 7 marbles. Write the number.",
            "language_focus": "Numbers 1-10, shape names.",
        },
        3: {
            "title": "Rainbow Surprise",
            "panels": [
                {"scene": "It starts to rain. Lily and Tom look out the window.", "speech": "Oh! It is raining!"},
                {"scene": "The rain stops. A rainbow appears.", "speech": "Look! A rainbow!"},
                {"scene": "Lily points at the colours.", "speech": "Red, orange, yellow, green, blue!"},
                {"scene": "Both smile happily.", "speech": "I love colours!"},
            ],
            "drawing_task": "Draw and colour a rainbow. Label three colours.",
            "language_focus": "Colour words, Look!, I love ___.",
        },
        4: {
            "title": "Where Is the Library?",
            "panels": [
                {"scene": "Tom stands in the corridor looking confused.", "speech": "Where is the library?"},
                {"scene": "Lily points to the right.", "speech": "It is there! Come with me!"},
                {"scene": "They enter the library. Books everywhere!", "speech": "Wow! So many books!"},
                {"scene": "They sit and read together.", "speech": "I like my school!"},
            ],
            "drawing_task": "Draw your favourite room at school. Write its name.",
            "language_focus": "Where is ___? / It is there. / I like ___.",
        },
        5: {
            "title": "Family Photo",
            "panels": [
                {"scene": "Lily shows Tom a photo.", "speech": "This is my family!"},
                {"scene": "She points to people in the photo.", "speech": "This is my mum. This is my dad."},
                {"scene": "Tom shows his photo too.", "speech": "This is my sister!"},
                {"scene": "Both hold their photos up smiling.", "speech": "We love our families!"},
            ],
            "drawing_task": "Draw your family photo. Label each person in English.",
            "language_focus": "This is my ___. / Family vocabulary.",
        },
        6: {
            "title": "Fruit Salad Day",
            "panels": [
                {"scene": "Mr. Sun puts fruit on the table.", "speech": "Let's make fruit salad!"},
                {"scene": "Lily holds an apple and a banana.", "speech": "I have an apple and a banana!"},
                {"scene": "Tom holds strawberries.", "speech": "I have strawberries!"},
                {"scene": "They all eat together.", "speech": "Yummy! I like fruit salad!"},
            ],
            "drawing_task": "Draw your fruit salad. Write the fruit names.",
            "language_focus": "I have ___. / Fruit vocabulary / Yummy!",
        },
        7: {
            "title": "A Day at the Farm",
            "panels": [
                {"scene": "Lily and Tom arrive at a farm.", "speech": "Look! Animals!"},
                {"scene": "A cow says 'Moo'. Tom laughs.", "speech": "The cow is big!"},
                {"scene": "Lily pets a rabbit.", "speech": "The rabbit is soft!"},
                {"scene": "Buddy runs with the chickens.", "speech": "Buddy is funny!"},
            ],
            "drawing_task": "Draw a farm animal. Write: 'The ___ is ___.'",
            "language_focus": "Animal names, adjectives: big, small, soft, funny.",
        },
        8: {
            "title": "Head, Shoulders, Knees and Toes",
            "panels": [
                {"scene": "Mr. Sun stands in front of the class.", "speech": "Touch your head!"},
                {"scene": "All children touch their heads.", "speech": "This is my head!"},
                {"scene": "Mr. Sun points down.", "speech": "Now touch your toes!"},
                {"scene": "Everyone bends down laughing.", "speech": "Ha ha! My toes!"},
            ],
            "drawing_task": "Draw a person. Label five body parts in English.",
            "language_focus": "Body parts, Touch your ___!, This is my ___.",
        },
        9: {
            "title": "The Weather Report",
            "panels": [
                {"scene": "Lily stands by the window with a chart.", "speech": "What is the weather today?"},
                {"scene": "Tom looks outside – sun is shining.", "speech": "It is sunny!"},
                {"scene": "Lily puts a sun sticker on Monday.", "speech": "Monday – sunny!"},
                {"scene": "Both give a thumbs up.", "speech": "I like sunny days!"},
            ],
            "drawing_task": "Draw a weather chart for three days. Use weather pictures.",
            "language_focus": "Days of the week, weather words, It is ___.",
        },
        10: {
            "title": "Goodbye Party",
            "panels": [
                {"scene": "The classroom is decorated with balloons.", "speech": "It is our last day!"},
                {"scene": "Lily hugs her friends.", "speech": "Thank you for a great year!"},
                {"scene": "Tom waves happily.", "speech": "Goodbye, friends! See you!"},
                {"scene": "Everyone throws confetti.", "speech": "Happy summer!"},
            ],
            "drawing_task": "Draw the goodbye party. Write 'Goodbye!' and 'See you!'",
            "language_focus": "Goodbye, See you, Thank you, Happy summer.",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 18. MISSION BANK — gamified weekly missions with XP rewards
# ══════════════════════════════════════════════════════════════════════════════

MISSION_BANK = {
    1: {
        1: {
            "title": "The Greeting Champion",
            "mission": "Say 'Hello' and 'Good morning' to three different people today.",
            "evidence": "Draw three smiley faces – one for each person you greeted.",
            "xp": 15,
            "difficulty": "Easy",
        },
        2: {
            "title": "Number Detective",
            "mission": "Find and count five things at home. Write the numbers 1-5 next to each thing.",
            "evidence": "Draw or stick pictures of the five things with numbers.",
            "xp": 15,
            "difficulty": "Easy",
        },
        3: {
            "title": "Colour Collector",
            "mission": "Find one object for each colour: red, blue, yellow, green. Bring or draw them.",
            "evidence": "Draw or photograph four objects. Label the colours in English.",
            "xp": 20,
            "difficulty": "Easy",
        },
        4: {
            "title": "School Explorer",
            "mission": "Walk around school. Find three places: classroom, library, playground. Say their names.",
            "evidence": "Draw a simple map with the three places labelled in English.",
            "xp": 20,
            "difficulty": "Easy",
        },
        5: {
            "title": "Family Reporter",
            "mission": "Tell a family member three sentences in English about your family.",
            "evidence": "Draw your family and write: 'This is my ___.' for each person.",
            "xp": 20,
            "difficulty": "Easy",
        },
        6: {
            "title": "Fruit & Veggie Chef",
            "mission": "Ask for three fruits or vegetables in English at home: 'Can I have a ___, please?'",
            "evidence": "Draw the three items you asked for. Write their English names.",
            "xp": 20,
            "difficulty": "Medium",
        },
        7: {
            "title": "Animal Sound Master",
            "mission": "Name five animals and make their English sounds (e.g., dog – woof, cat – meow).",
            "evidence": "Draw five animals. Write the animal name and its sound.",
            "xp": 15,
            "difficulty": "Easy",
        },
        8: {
            "title": "Body Part Robot",
            "mission": "Make a robot from paper or recycled materials. Label five body parts in English.",
            "evidence": "Bring or photograph your robot with labels.",
            "xp": 25,
            "difficulty": "Medium",
        },
        9: {
            "title": "Weather Watcher",
            "mission": "Check the weather for three days. Each day say: 'Today is ___.'",
            "evidence": "Draw three weather pictures with the day name and weather word.",
            "xp": 20,
            "difficulty": "Easy",
        },
        10: {
            "title": "Summer Memory Book",
            "mission": "Draw three things you want to do in summer. Write one English sentence for each.",
            "evidence": "A mini book (3 pages) with drawings and sentences.",
            "xp": 25,
            "difficulty": "Medium",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 19. ESCAPE ROOM BANK — simple treasure-hunt puzzles per unit
# ══════════════════════════════════════════════════════════════════════════════

ESCAPE_ROOM_BANK = {
    1: {
        1: {
            "title": "The Lost Name Tag",
            "story": "Oh no! Lily lost her name tag. Help her find it by solving the puzzles!",
            "puzzles": [
                {"type": "unscramble", "question": "Unscramble: O-L-L-E-H", "answer": "HELLO", "hint": "We say this when we meet someone."},
                {"type": "match", "question": "Match the picture of a waving hand to the correct word.", "answer": "Hello", "hint": "It starts with H."},
                {"type": "listen", "question": "Listen to the teacher say a greeting. Which one is it?", "answer": "Good morning", "hint": "We say this in the morning."},
            ],
            "final_code": "HELLO LILY",
            "reward": "A 'Super Greeter' sticker!",
        },
        2: {
            "title": "The Number Treasure",
            "story": "A treasure chest is locked! Count and solve to find the code!",
            "puzzles": [
                {"type": "count", "question": "Count the stars in the picture. How many?", "answer": "7", "hint": "It is between 6 and 8."},
                {"type": "shape", "question": "What shape has 3 sides?", "answer": "triangle", "hint": "Tri- means three."},
                {"type": "order", "question": "Put in order: 3, 1, 5, 2, 4", "answer": "1, 2, 3, 4, 5", "hint": "Start from the smallest."},
            ],
            "final_code": "7-TRIANGLE-12345",
            "reward": "A gold star sticker!",
        },
        3: {
            "title": "The Colour Key",
            "story": "The art room door is locked! Match the colours to unlock it!",
            "puzzles": [
                {"type": "colour_match", "question": "What colour is the sky?", "answer": "blue", "hint": "It rhymes with 'glue'."},
                {"type": "colour_match", "question": "What colour is a banana?", "answer": "yellow", "hint": "It starts with Y."},
                {"type": "mix", "question": "Red + yellow = ?", "answer": "orange", "hint": "It is the name of a fruit too!"},
            ],
            "final_code": "BLUE-YELLOW-ORANGE",
            "reward": "A rainbow sticker!",
        },
        4: {
            "title": "Mystery at School",
            "story": "Something is missing from the classroom! Follow the clues around school!",
            "puzzles": [
                {"type": "riddle", "question": "I have books but I am not a bag. What am I?", "answer": "library", "hint": "You go here to read quietly."},
                {"type": "match", "question": "Match: 'We play here' → ___", "answer": "playground", "hint": "Play + ground."},
                {"type": "yes_no", "question": "Is a whiteboard in the classroom? Yes or No?", "answer": "Yes", "hint": "The teacher writes on it."},
            ],
            "final_code": "LIBRARY-PLAYGROUND-YES",
            "reward": "A 'School Explorer' badge sticker!",
        },
        5: {
            "title": "The Family Album",
            "story": "Lily's family photo album is mixed up! Help her sort the photos!",
            "puzzles": [
                {"type": "match", "question": "Who is 'mum'? Match the word to the picture.", "answer": "mum", "hint": "She takes care of you at home."},
                {"type": "fill", "question": "This is my ___. (picture of a dad)", "answer": "dad", "hint": "He is mum's partner."},
                {"type": "count", "question": "How many people are in Lily's family picture?", "answer": "4", "hint": "Mum, Dad, Lily and her brother."},
            ],
            "final_code": "MUM-DAD-4",
            "reward": "A family heart sticker!",
        },
        6: {
            "title": "The Hungry Caterpillar's Lunch",
            "story": "A caterpillar is hungry! Feed it by naming the fruits and vegetables!",
            "puzzles": [
                {"type": "name", "question": "Name this red fruit (picture of apple).", "answer": "apple", "hint": "It starts with A."},
                {"type": "sort", "question": "Sort: apple, carrot, banana, tomato → Fruit or Vegetable?", "answer": "Fruit: apple, banana / Vegetable: carrot, tomato", "hint": "Fruits are usually sweet."},
                {"type": "colour_match", "question": "What colour is a carrot?", "answer": "orange", "hint": "Same as the colour of the sunset."},
            ],
            "final_code": "APPLE-SORT-ORANGE",
            "reward": "A fruit basket sticker!",
        },
        7: {
            "title": "The Animal Safari",
            "story": "Buddy is lost in the safari park! Follow animal clues to find him!",
            "puzzles": [
                {"type": "sound", "question": "'Moo!' – What animal am I?", "answer": "cow", "hint": "It gives us milk."},
                {"type": "riddle", "question": "I can fly. I am small. I say 'tweet'. What am I?", "answer": "bird", "hint": "Bella is one!"},
                {"type": "count", "question": "A cat has ___ legs.", "answer": "4", "hint": "Same as a dog."},
            ],
            "final_code": "COW-BIRD-4",
            "reward": "A 'Safari Star' sticker!",
        },
        8: {
            "title": "The Body Parts Puzzle",
            "story": "Mr. Sun's robot is broken! Put the body parts back to fix it!",
            "puzzles": [
                {"type": "label", "question": "What is on top of your body?", "answer": "head", "hint": "You wear a hat on it."},
                {"type": "match", "question": "Match: 'You use these to clap' → ___", "answer": "hands", "hint": "They have fingers."},
                {"type": "action", "question": "Touch your nose! Now touch your ears! What did you touch?", "answer": "nose and ears", "hint": "Both are on your face."},
            ],
            "final_code": "HEAD-HANDS-NOSE",
            "reward": "A 'Robot Builder' sticker!",
        },
        9: {
            "title": "The Weather Station",
            "story": "The weather machine is broken! Fix it by answering the weather puzzles!",
            "puzzles": [
                {"type": "match", "question": "Match the umbrella picture to the weather word.", "answer": "rainy", "hint": "You need an umbrella when it is ___."},
                {"type": "order", "question": "Put the days in order: Wednesday, Monday, Tuesday", "answer": "Monday, Tuesday, Wednesday", "hint": "Monday is first."},
                {"type": "yes_no", "question": "Do we wear sunglasses on a sunny day?", "answer": "Yes", "hint": "The sun is bright!"},
            ],
            "final_code": "RAINY-MON-TUE-WED-YES",
            "reward": "A sunshine sticker!",
        },
        10: {
            "title": "The Summer Key",
            "story": "The door to summer holiday is locked! Answer the review puzzles to open it!",
            "puzzles": [
                {"type": "vocab", "question": "Name three things you do at the beach.", "answer": "swim, play, build (sandcastle)", "hint": "Think about water and sand."},
                {"type": "greeting", "question": "How do you say goodbye to a friend?", "answer": "Goodbye / See you!", "hint": "The opposite of Hello."},
                {"type": "feelings", "question": "How do you feel about summer? 'I am ___.'", "answer": "happy", "hint": "😊"},
            ],
            "final_code": "SWIM-GOODBYE-HAPPY",
            "reward": "A 'Summer Superstar' medal sticker!",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 20. FAMILY CORNER BANK — parent–child activities per unit
# ══════════════════════════════════════════════════════════════════════════════

FAMILY_CORNER_BANK = {
    1: {
        1: {
            "title": "Hello at Home!",
            "activity": "Practise English greetings at home: say 'Good morning' at breakfast and 'Good night' at bedtime.",
            "together": "Take turns greeting each other in English for one whole day.",
            "parent_question": "Ask your child: 'How do you say hello in English?' Watch them demonstrate!",
            "signature": True,
        },
        2: {
            "title": "Counting Fun",
            "activity": "Count objects at home together in English: spoons, shoes, books (1-10).",
            "together": "Have a counting race: who can count to 10 fastest in English?",
            "parent_question": "Hold up some fingers and ask: 'How many?' Let your child answer in English.",
            "signature": True,
        },
        3: {
            "title": "Colour Hunt",
            "activity": "Go on a colour hunt at home! Find something red, blue, yellow and green.",
            "together": "Take turns: 'I spy something ___.' (say a colour) and find it!",
            "parent_question": "Point to something and ask: 'What colour is this?' Praise every English answer!",
            "signature": True,
        },
        4: {
            "title": "School Talk",
            "activity": "Ask your child to tell you three English words they learned about school.",
            "together": "Draw a picture of the classroom together. Your child labels items in English.",
            "parent_question": "Ask: 'What is your favourite place at school?' Help them answer in English.",
            "signature": True,
        },
        5: {
            "title": "Family Tree",
            "activity": "Make a simple family tree together. Your child writes: mum, dad, sister, brother.",
            "together": "Point to family members in a photo. Child says: 'This is my ___.'",
            "parent_question": "Ask: 'Who is in our family?' Encourage full English sentences.",
            "signature": True,
        },
        6: {
            "title": "Kitchen English",
            "activity": "Open the fridge together. Name five fruits or vegetables in English.",
            "together": "Make a simple salad. Child names each ingredient in English before adding it.",
            "parent_question": "At dinner, point to food and ask: 'What is this in English?'",
            "signature": True,
        },
        7: {
            "title": "Animal Sounds",
            "activity": "Name five animals in English. Make the sounds together (woof, meow, moo).",
            "together": "Play an animal guessing game: make a sound – child guesses the English animal name.",
            "parent_question": "Ask: 'What is your favourite animal? Why?' Help them answer.",
            "signature": True,
        },
        8: {
            "title": "Body Song",
            "activity": "Sing 'Head, Shoulders, Knees and Toes' together at home.",
            "together": "Play 'Simon Says' with body parts in English. Take turns being Simon!",
            "parent_question": "Touch a body part and ask: 'What is this in English?'",
            "signature": True,
        },
        9: {
            "title": "Weather Report",
            "activity": "Look out the window every morning. Child says the weather in English: 'It is ___.'",
            "together": "Make a weekly weather chart together. Child draws and writes the weather each day.",
            "parent_question": "Ask: 'What day is it today? What is the weather?' every morning.",
            "signature": True,
        },
        10: {
            "title": "Summer English Goals",
            "activity": "Make a list of three English words your child will practise over summer.",
            "together": "Create a mini 'English diary' for summer: one drawing + one English word per day.",
            "parent_question": "Ask: 'What was your favourite thing you learned in English this year?'",
            "signature": True,
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 21. SEL BANK — Social-Emotional Learning per unit
# ══════════════════════════════════════════════════════════════════════════════

SEL_BANK = {
    1: {
        1: {
            "emotion": "Happy",
            "prompt": "How do you feel on the first day of school? Draw a happy face!",
            "activity": "Stand up and smile at three friends. Say: 'I am happy to see you!'",
            "mindfulness": "Close your eyes. Take three deep breaths. Think of something that makes you happy.",
            "discussion": "When do you feel happy? Tell your partner one thing.",
        },
        2: {
            "emotion": "Curious",
            "prompt": "Numbers are everywhere! What do you want to count today?",
            "activity": "Draw a 'curiosity jar'. Put inside three things you want to learn about.",
            "mindfulness": "Close your eyes. Listen carefully. How many sounds can you count?",
            "discussion": "What are you curious about? Ask your partner one question.",
        },
        3: {
            "emotion": "Excited",
            "prompt": "Colours make the world beautiful! What is your favourite colour?",
            "activity": "Draw how 'excited' looks. Use lots of bright colours!",
            "mindfulness": "Breathe in a rainbow: red, orange, yellow, green, blue. Breathe out slowly.",
            "discussion": "What makes you feel excited? Share with your partner.",
        },
        4: {
            "emotion": "Proud",
            "prompt": "You are a school star! What are you proud of at school?",
            "activity": "Draw a star and write one thing you are good at inside it.",
            "mindfulness": "Sit tall like a proud tree. Feel your feet on the ground. You are strong!",
            "discussion": "Tell your partner: 'I am proud because I can ___.'",
        },
        5: {
            "emotion": "Loved",
            "prompt": "Your family loves you! How do you show love?",
            "activity": "Make a heart card for someone in your family. Write 'I love you!' in English.",
            "mindfulness": "Put your hand on your heart. Feel it beat. Think of someone you love.",
            "discussion": "Who do you love? Say: 'I love my ___.' Tell your partner.",
        },
        6: {
            "emotion": "Grateful",
            "prompt": "We have yummy food! What food are you thankful for?",
            "activity": "Draw three foods you are thankful for. Say 'Thank you!' for each one.",
            "mindfulness": "Before you eat, close your eyes and say 'Thank you' quietly.",
            "discussion": "Tell your partner: 'I am thankful for ___.'",
        },
        7: {
            "emotion": "Kind",
            "prompt": "Animals need kindness too! How can we be kind to animals?",
            "activity": "Draw yourself being kind to an animal. Write: 'Be kind!'",
            "mindfulness": "Imagine you are holding a tiny bird. Be very gentle and quiet.",
            "discussion": "How can we be kind? Tell your partner two ideas.",
        },
        8: {
            "emotion": "Brave",
            "prompt": "Trying new things takes bravery! When were you brave?",
            "activity": "Draw a 'bravery shield'. Inside, draw something brave you did.",
            "mindfulness": "Stand like a superhero: hands on hips, chin up. Say: 'I am brave!'",
            "discussion": "Tell your partner: 'I was brave when I ___.'",
        },
        9: {
            "emotion": "Calm",
            "prompt": "Rainy days can be calm and peaceful. How do you feel when it rains?",
            "activity": "Draw a rainy day. Colour it with soft, cool colours (blue, grey, green).",
            "mindfulness": "Listen to the rain (or imagine rain). Breathe slowly: in... out... in... out...",
            "discussion": "What helps you feel calm? Share one idea with your partner.",
        },
        10: {
            "emotion": "Hopeful",
            "prompt": "Summer is coming! What do you hope to do?",
            "activity": "Draw a 'hope balloon'. Inside, write one thing you hope for.",
            "mindfulness": "Close your eyes. Imagine a sunny summer day. Smile and feel the warmth.",
            "discussion": "Tell your partner: 'I hope ___.' What are your summer dreams?",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 22. STEAM BANK — cross-curricular Science/Tech/Engineering/Art/Maths tasks
# ══════════════════════════════════════════════════════════════════════════════

STEAM_BANK = {
    1: {
        1: {
            "subject": "Art",
            "title": "Name Tag Design",
            "task": "Design a colourful name tag with your name in English. Decorate it with drawings of things you like.",
            "vocab": ["name", "hello", "colour", "draw", "cut", "stick"],
        },
        2: {
            "subject": "Maths",
            "title": "Shape Robots",
            "task": "Build a robot using cut-out shapes: circles, squares, triangles. Count and label each shape.",
            "vocab": ["circle", "square", "triangle", "rectangle", "how many", "count"],
        },
        3: {
            "subject": "Science",
            "title": "Colour Mixing Magic",
            "task": "Mix red + yellow paint. What colour do you get? Try blue + yellow. Record your results!",
            "vocab": ["mix", "red", "yellow", "blue", "orange", "green", "purple"],
        },
        4: {
            "subject": "Engineering",
            "title": "Build a Mini School",
            "task": "Use boxes, paper and glue to build a mini school model. Label the rooms in English.",
            "vocab": ["classroom", "library", "playground", "door", "window", "build"],
        },
        5: {
            "subject": "Art",
            "title": "Family Puppet Show",
            "task": "Make stick puppets of your family from paper. Perform a short puppet show using English: 'This is my ___.'",
            "vocab": ["mum", "dad", "brother", "sister", "baby", "family"],
        },
        6: {
            "subject": "Science",
            "title": "Seed Growing Experiment",
            "task": "Plant a bean seed in a cup. Water it and watch it grow. Draw what happens each week. Label in English.",
            "vocab": ["seed", "water", "sun", "grow", "leaf", "plant"],
        },
        7: {
            "subject": "Technology",
            "title": "Animal Photo Book",
            "task": "Take photos (or draw pictures) of five animals. Make a mini book. Write the animal name under each picture.",
            "vocab": ["cat", "dog", "bird", "fish", "rabbit", "photo", "book"],
        },
        8: {
            "subject": "Maths",
            "title": "Body Measurement",
            "task": "Use your hands to measure things: 'The desk is ___ hands long.' Record five measurements.",
            "vocab": ["hand", "long", "short", "measure", "how many", "desk"],
        },
        9: {
            "subject": "Engineering",
            "title": "Weather Wheel",
            "task": "Make a spinning weather wheel from cardboard. Write the weather words: sunny, rainy, cloudy, windy, snowy.",
            "vocab": ["sunny", "rainy", "cloudy", "windy", "snowy", "spin", "wheel"],
        },
        10: {
            "subject": "Art",
            "title": "Summer Memory Collage",
            "task": "Make a collage of your favourite memories from this year using drawings, stickers and words in English.",
            "vocab": ["summer", "favourite", "memory", "draw", "stick", "write", "fun"],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 23. PODCAST BANK — simple audio-style episodes per unit
# ══════════════════════════════════════════════════════════════════════════════

PODCAST_BANK = {
    1: {
        1: {
            "title": "Episode 1: Hello, World!",
            "host": "Mr. Sun",
            "summary": "Our first episode! We learn how to say hello, goodbye and good morning in English. Lily and Tom help us practise!",
            "segments": [
                "Welcome Song: 'Hello, Hello, How Are You?'",
                "Word of the Day: 'Hello' – say it loud, say it quiet, say it fast!",
                "Story Time: Lily says hello to everyone on her first day.",
                "Repeat After Me: 'Good morning! / Hello! / Goodbye!'",
                "Challenge: Say hello to three people today in English!",
            ],
            "student_task": "Listen and repeat all the greetings. Draw yourself saying 'Hello!'",
        },
        2: {
            "title": "Episode 2: Count With Me!",
            "host": "Mr. Sun",
            "summary": "Let's count from 1 to 10! We also learn shape names. Tap, clap and count along!",
            "segments": [
                "Counting Song: 'One, Two, Buckle My Shoe' (simplified)",
                "Word of the Day: 'Circle' – find circles around you!",
                "Shape Chant: 'Circle, square, triangle – clap, clap, clap!'",
                "Repeat After Me: Count 1 to 10 slowly, then fast.",
                "Challenge: Count five things on your desk right now!",
            ],
            "student_task": "Count 1-10 with the episode. Draw three shapes and name them.",
        },
        3: {
            "title": "Episode 3: A Rainbow of Colours!",
            "host": "Mr. Sun",
            "summary": "Today we learn colour words! Red, blue, yellow, green and more. Grab your crayons!",
            "segments": [
                "Colour Song: 'Red and Yellow and Pink and Green'",
                "Word of the Day: 'Rainbow' – how many colours?",
                "Colour Quiz: 'The sky is ___. A banana is ___.'",
                "Repeat After Me: Say all the colour words clearly.",
                "Challenge: Draw a rainbow and label every colour in English!",
            ],
            "student_task": "Sing along to the colour song. Draw and label your rainbow.",
        },
        4: {
            "title": "Episode 4: My Super School!",
            "host": "Mr. Sun",
            "summary": "We explore school places: classroom, library, playground. Where is your favourite place?",
            "segments": [
                "School Song: 'This Is My School – I Love It!'",
                "Word of the Day: 'Classroom' – what is in your classroom?",
                "Guessing Game: 'I read books here. Where am I?' – Library!",
                "Repeat After Me: 'Classroom, library, playground.'",
                "Challenge: Draw your school and label two places in English!",
            ],
            "student_task": "Listen and guess each school place. Draw and label your school.",
        },
        5: {
            "title": "Episode 5: My Wonderful Family!",
            "host": "Mr. Sun",
            "summary": "We talk about our families! Mum, dad, brother, sister – who is in your family?",
            "segments": [
                "Family Song: 'Mum and Dad and Sister and Brother'",
                "Word of the Day: 'Family' – it means the people you love!",
                "Story Time: Tom tells us about his family.",
                "Repeat After Me: 'This is my mum. This is my dad.'",
                "Challenge: Tell a friend about your family in English!",
            ],
            "student_task": "Draw your family. Write 'This is my ___.' for each person.",
        },
        6: {
            "title": "Episode 6: Yummy Fruits and Veggies!",
            "host": "Mr. Sun",
            "summary": "Today we learn fruit and vegetable words. What do you like to eat? Let's find out!",
            "segments": [
                "Food Song: 'Apples, Bananas, Carrots – Yum!'",
                "Word of the Day: 'Apple' – red, green or yellow?",
                "Sorting Game: 'Is a carrot a fruit or a vegetable?'",
                "Repeat After Me: 'Apple, banana, carrot, tomato.'",
                "Challenge: Open your fridge and name three things in English!",
            ],
            "student_task": "Sing along. Draw your favourite fruit and vegetable. Label them.",
        },
        7: {
            "title": "Episode 7: Amazing Animals!",
            "host": "Mr. Sun",
            "summary": "Cats, dogs, birds and fish! We learn animal names and sounds. Can you guess the animal?",
            "segments": [
                "Animal Song: 'Old MacDonald' (4 animals only)",
                "Word of the Day: 'Dog' – Buddy is a dog! Woof!",
                "Sound Quiz: 'Moo! What animal am I?'",
                "Repeat After Me: 'Cat, dog, bird, fish, rabbit.'",
                "Challenge: Make five animal sounds. Ask a friend to guess!",
            ],
            "student_task": "Listen and guess each animal. Draw your favourite and write its name.",
        },
        8: {
            "title": "Episode 8: My Amazing Body!",
            "host": "Mr. Sun",
            "summary": "Head, shoulders, knees and toes! Touch, move and name your body parts in English!",
            "segments": [
                "Action Song: 'Head, Shoulders, Knees and Toes'",
                "Word of the Day: 'Hands' – clap your hands!",
                "Simon Says: 'Touch your nose! Touch your ears!'",
                "Repeat After Me: 'Head, hand, foot, arm, leg.'",
                "Challenge: Play Simon Says with your family tonight!",
            ],
            "student_task": "Sing and do the actions. Draw a person and label five body parts.",
        },
        9: {
            "title": "Episode 9: Days and Weather Fun!",
            "host": "Mr. Sun",
            "summary": "Monday, Tuesday... what day is it? Sunny, rainy, cloudy – what is the weather? Let's learn!",
            "segments": [
                "Days Song: 'Monday, Tuesday, Wednesday – Hey!'",
                "Word of the Day: 'Sunny' – the sun is shining!",
                "Weather Report: 'Today is ___. Tomorrow will be ___.'",
                "Repeat After Me: 'Monday, Tuesday, Wednesday, Thursday, Friday.'",
                "Challenge: Be a weather reporter! Tell your family the weather in English!",
            ],
            "student_task": "Learn the days song. Draw today's weather and write the word.",
        },
        10: {
            "title": "Episode 10: Hooray for Summer!",
            "host": "Mr. Sun",
            "summary": "Our last episode! We review everything and get ready for a fun summer. Goodbye, friends!",
            "segments": [
                "Review Song: 'We Learned So Much This Year!'",
                "Best Moments: Lily and Tom's favourite English words.",
                "Quick Quiz: 'Say hello / Count to 5 / Name 3 colours.'",
                "Repeat After Me: 'Goodbye! See you! Happy summer!'",
                "Summer Challenge: Say one English word every day this summer!",
            ],
            "student_task": "Sing the goodbye song. Draw your favourite memory from English class. Write one sentence about it.",
        },
    },
}
