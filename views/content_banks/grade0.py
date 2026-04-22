# -*- coding: utf-8 -*-
"""Content banks for Grade 0 (Preschool / Ages 4-6).

Preschool tier sections: story, vocabulary, listening, speaking, song,
culture, project, review. Content is play-based, song-driven, and highly visual.
"""

STORY_CHARACTERS = {
    0: {
        "main": [
            {"name": "Paws", "age": "3 (cat years)", "desc": "A friendly orange cat who loves to explore and learn English words.", "emoji": "🐱"},
            {"name": "Sunny", "age": "5", "desc": "A cheerful girl who teaches her friends English through songs and games.", "emoji": "🌞"},
            {"name": "Benny", "age": "5", "desc": "A curious boy who loves colours, numbers and animals.", "emoji": "🧒"},
            {"name": "Rainbow", "age": "2 (parrot years)", "desc": "A colourful parrot who repeats English words and sings along.", "emoji": "🦜"},
        ],
        "teacher": {"name": "Miss Lily", "desc": "A kind teacher who uses puppets, songs and games to teach English."},
    },
}

STORY_BANK = {
    0: {
        1: {
            "title": "Paws Says Hello",
            "previously": None,
            "episode": (
                "One sunny morning, a little orange cat named Paws walked into the classroom. "
                "'Hello! Hello!' said Paws. 'My name is Paws. What is your name?' "
                "Sunny smiled and said, 'Hi Paws! My name is Sunny!' "
                "Benny waved and said, 'Hello! I am Benny!' "
                "Rainbow the parrot flew to Paws and said, 'Hello! Hello! Friend! Friend!' "
                "Everyone laughed and sang the Hello Song together."
            ),
            "cliffhanger": "What colour is Paws? Let's find out next time!",
            "vocab_tie": ["hello", "hi", "name", "friend", "bye"],
        },
        2: {
            "title": "The Colour Hunt",
            "previously": "Paws met Sunny, Benny and Rainbow in the classroom.",
            "episode": (
                "Today, Miss Lily had a surprise. 'Let's go on a colour hunt!' she said. "
                "Paws found a RED apple. 'Red! Red!' said Paws. "
                "Sunny pointed at the sky. 'Blue! The sky is blue!' "
                "Benny picked a flower. 'Yellow! A yellow flower!' "
                "Rainbow flew to the grass. 'Green! Green!' he sang. "
                "They found five colours and made a beautiful colour poster."
            ),
            "cliffhanger": "How many colours can you find in your classroom?",
            "vocab_tie": ["red", "blue", "yellow", "green", "orange"],
        },
        3: {
            "title": "Counting Fun",
            "previously": "Paws and friends went on a colour hunt.",
            "episode": (
                "Miss Lily put big toys on the table. 'Let's count!' she said. "
                "'ONE teddy bear,' said Sunny. 'TWO balls,' said Benny. "
                "'THREE cars,' said Paws. 'FOUR blocks,' said Rainbow. "
                "'FIVE crayons!' they all shouted together. "
                "Then Miss Lily said, 'Now let's play a number game!' "
                "She held up fingers and they called out the numbers. "
                "'One, two, three, four, five!' Everyone clapped."
            ),
            "cliffhanger": "Can you count the fingers on one hand?",
            "vocab_tie": ["one", "two", "three", "four", "five"],
        },
        4: {
            "title": "Paws Feels Cold",
            "previously": "Paws and friends learned to count to five.",
            "episode": (
                "It was a rainy day. Paws looked out the window. "
                "'Rain! Rain!' said Paws. 'I am cold!' "
                "Sunny gave Paws a warm hat. 'Here! A hat for you!' "
                "Benny gave Paws socks. 'Socks! Warm socks!' "
                "Rainbow sang, 'Sun, rain, cloud, wind, snow!' "
                "Miss Lily made warm milk for everyone. "
                "'Thank you!' said Paws. 'I am happy now!'"
            ),
            "cliffhanger": "What is the weather like today?",
            "vocab_tie": ["sun", "rain", "cloud", "hat", "socks"],
        },
        5: {
            "title": "The Toy Party",
            "previously": "Paws and friends learned about the weather.",
            "episode": (
                "It was Party Time! Miss Lily brought a big box. "
                "'Surprise!' she said. Inside were toys! "
                "Sunny took a doll. 'A doll! My doll!' "
                "Benny took a car. 'Vroom vroom! A red car!' "
                "Paws played with a ball. 'Ball! Ball!' "
                "Rainbow sat on a puzzle. 'Puzzle! Fun!' "
                "They played and danced. 'Happy party!' said everyone."
            ),
            "cliffhanger": "What is your favourite toy?",
            "vocab_tie": ["ball", "doll", "car", "puzzle", "party"],
        },
        6: {
            "title": "Paws Goes to the Farm",
            "previously": "Paws and friends had a toy party.",
            "episode": (
                "Miss Lily took the class to a farm. 'Look!' said Benny. "
                "'A cow! Moo!' said Paws. 'A sheep! Baa!' said Sunny. "
                "'A horse! Neigh!' said Benny. Rainbow flew to the chickens. "
                "'Cluck cluck!' said Rainbow. "
                "They saw a pink pig too. 'Oink oink!' everyone laughed. "
                "Miss Lily said, 'Five animals! Cow, sheep, horse, chicken, pig!' "
                "They sang the Farm Song all the way home."
            ),
            "cliffhanger": "Which farm animal do you like best?",
            "vocab_tie": ["cow", "sheep", "horse", "chicken", "pig"],
        },
        7: {
            "title": "The Seasons Tree",
            "previously": "Paws and friends visited a farm.",
            "episode": (
                "In the garden, there was a big tree. "
                "'Look,' said Miss Lily. 'In spring, the tree has flowers.' "
                "Sunny drew a green tree. 'Summer! Big green leaves!' "
                "Benny drew an orange tree. 'Autumn! Orange and red leaves!' "
                "Paws drew a white tree. 'Winter! Snow on the tree!' "
                "Rainbow coloured all four seasons. "
                "'Spring, summer, autumn, winter!' they sang together."
            ),
            "cliffhanger": "What season is it now?",
            "vocab_tie": ["spring", "summer", "autumn", "winter", "tree"],
        },
        8: {
            "title": "At the Beach",
            "previously": "Paws and friends painted the four seasons.",
            "episode": (
                "It was summer! Miss Lily took everyone to the beach. "
                "'Sand! Sand!' said Paws, digging with his paws. "
                "Sunny built a sandcastle. 'My castle!' she said. "
                "Benny found a shell. 'Look! A beautiful shell!' "
                "Rainbow flew over the sea. 'Sea! Blue sea!' "
                "They played with a bucket and wore sunglasses. "
                "'I love the beach!' said everyone."
            ),
            "cliffhanger": "What do you like to do at the beach?",
            "vocab_tie": ["sand", "sea", "shell", "bucket", "sunglasses"],
        },
        9: {
            "title": "Helpers All Around",
            "previously": "Paws and friends played at the beach.",
            "episode": (
                "Miss Lily asked, 'Who helps us every day?' "
                "'The doctor helps when we are sick,' said Sunny. "
                "'The teacher helps us learn,' said Benny. "
                "'The police officer keeps us safe,' said Paws. "
                "'The fire fighter is brave!' said Rainbow. "
                "Miss Lily smiled. 'And the cook makes yummy food!' "
                "They played a Helper Game — everyone pretended to be a helper!"
            ),
            "cliffhanger": "What do you want to be when you grow up?",
            "vocab_tie": ["doctor", "teacher", "police", "fire fighter", "cook"],
        },
        10: {
            "title": "The Goodbye Song",
            "previously": "Paws and friends learned about helpers.",
            "episode": (
                "It was the last day of school. Paws was sad. "
                "'Don't be sad!' said Sunny. 'We will see you in summer!' "
                "'Goodbye, friends!' said Benny. 'I will miss you!' "
                "Rainbow sang, 'Goodbye, goodbye, see you soon!' "
                "Miss Lily gave everyone a star. 'You are all stars!' she said. "
                "They sang the Goodbye Song together and hugged. "
                "'See you! See you!' said Paws with a big smile."
            ),
            "cliffhanger": "",
            "vocab_tie": ["goodbye", "see you", "miss you", "summer", "holiday"],
        },
    },
}

SONG_BANK = {
    0: {
        1: {
            "title": "The Hello Song",
            "type": "Song",
            "lyrics": (
                "Hello, hello, hello!\n"
                "What is your name?\n"
                "Hello, hello, hello!\n"
                "Let's play a game!\n\n"
                "My name is ___,\n"
                "My name is ___,\n"
                "Hello, hello, hello!\n"
                "We are friends!"
            ),
            "activity": "Stand in a circle. Sing the song and say your name when it is your turn.",
        },
        2: {
            "title": "The Colour Song",
            "type": "Song",
            "lyrics": (
                "Red, blue, yellow, green,\n"
                "The prettiest colours I have seen!\n"
                "Orange, purple, pink and white,\n"
                "Colours make the world so bright!\n\n"
                "What colour is the sky? BLUE!\n"
                "What colour is the grass? GREEN!\n"
                "What colour is the sun? YELLOW!\n"
                "Colours, colours everywhere!"
            ),
            "activity": "Hold up coloured cards when you hear that colour in the song.",
        },
        3: {
            "title": "The Counting Song",
            "type": "Song",
            "lyrics": (
                "One, two, three, four, five,\n"
                "Once I caught a fish alive!\n"
                "Six, seven, eight, nine, ten,\n"
                "Then I let it go again!\n\n"
                "Why did you let it go?\n"
                "Because it bit my finger so!\n"
                "Which finger did it bite?\n"
                "This little finger on the right!"
            ),
            "activity": "Show your fingers as you count. Do the actions for catching and letting go.",
        },
        4: {
            "title": "The Weather Song",
            "type": "Chant",
            "lyrics": (
                "What's the weather? What's the weather?\n"
                "Look outside! Look outside!\n\n"
                "Is it sunny? (sunny!)\n"
                "Is it rainy? (rainy!)\n"
                "Is it cloudy? (cloudy!)\n"
                "Is it snowy? (snowy!)\n\n"
                "What's the weather today?\n"
                "Let's go out and play!"
            ),
            "activity": "Look out the window and answer. Do actions: sunny = arms up, rainy = fingers wiggle down.",
        },
        5: {
            "title": "The Party Dance",
            "type": "Song",
            "lyrics": (
                "It's a party, it's a party!\n"
                "Clap your hands! (clap clap)\n"
                "It's a party, it's a party!\n"
                "Stamp your feet! (stamp stamp)\n\n"
                "Jump up high! (jump!)\n"
                "Turn around! (wheee!)\n"
                "Sit back down! (phew!)\n\n"
                "It's a party, it's a party!\n"
                "Dance with me!"
            ),
            "activity": "Do all the actions in the song! Try to go faster each time.",
        },
        6: {
            "title": "Old MacDonald Had a Farm",
            "type": "Song",
            "lyrics": (
                "Old MacDonald had a farm, E-I-E-I-O!\n"
                "And on his farm he had a COW, E-I-E-I-O!\n"
                "With a MOO MOO here, and a MOO MOO there,\n"
                "Here a moo, there a moo, everywhere a moo moo!\n"
                "Old MacDonald had a farm, E-I-E-I-O!\n\n"
                "(sheep — BAA BAA)\n"
                "(chicken — CLUCK CLUCK)\n"
                "(pig — OINK OINK)\n"
                "(horse — NEIGH NEIGH)"
            ),
            "activity": "Sing the song with all five animals. Make the animal sounds loudly!",
        },
        7: {
            "title": "The Seasons Rap",
            "type": "Rap",
            "lyrics": (
                "Spring, spring, flowers grow! (clap clap)\n"
                "Summer, summer, to the beach we go! (clap clap)\n"
                "Autumn, autumn, leaves fall down! (clap clap)\n"
                "Winter, winter, snow on the ground! (clap clap)\n\n"
                "Spring, summer, autumn, winter,\n"
                "Four seasons in a year!\n"
                "Spring, summer, autumn, winter,\n"
                "Which one is YOUR favourite? (point)"
            ),
            "activity": "Clap the rhythm and do actions for each season.",
        },
        8: {
            "title": "The Beach Song",
            "type": "Song",
            "lyrics": (
                "Let's go to the beach, the beach, the beach!\n"
                "Sand and sea and shells to reach!\n\n"
                "Build a castle in the sand, (build build)\n"
                "Hold a bucket in your hand, (hold hold)\n"
                "Splash in water, one two three, (splash splash)\n"
                "The beach is fun for you and me!\n\n"
                "Let's go to the beach, the beach, the beach!\n"
                "Sand and sea and shells to reach!"
            ),
            "activity": "Pretend you are at the beach. Do the actions while singing.",
        },
        9: {
            "title": "The Helper Song",
            "type": "Chant",
            "lyrics": (
                "Who can help us? Who can help us?\n"
                "Let me see! Let me see!\n\n"
                "Doctor, doctor, helps us feel better!\n"
                "Teacher, teacher, helps us learn!\n"
                "Police, police, keeps us safe!\n"
                "Fire fighter, fire fighter, so brave!\n"
                "Cook, cook, makes yummy food!\n\n"
                "Thank you, helpers, you are good!"
            ),
            "activity": "Pretend to be each helper. Act out what they do!",
        },
        10: {
            "title": "The Goodbye Song",
            "type": "Song",
            "lyrics": (
                "Goodbye, goodbye, goodbye my friends!\n"
                "Goodbye, goodbye, until we meet again!\n\n"
                "It was fun to learn with you,\n"
                "Sing and play and learn things new!\n"
                "Colours, numbers, animals too,\n"
                "I will always remember you!\n\n"
                "Goodbye, goodbye, goodbye my friends!\n"
                "See you soon! See you soon!"
            ),
            "activity": "Wave goodbye to each friend and give a big hug!",
        },
    },
}

CULTURE_CORNER_BANK = {
    0: {
        1: {
            "title": "Hello Around the World",
            "text": (
                "Children say hello in many languages! In France, children say 'Bonjour!' "
                "In Japan, they say 'Konnichiwa!' In Spain, they say 'Hola!' "
                "In Turkey, we say 'Merhaba!' How many ways can you say hello?"
            ),
            "question": "Can you say hello in three languages?",
            "country_flag": "FR, JP, ES, TR",
            "recipe": None,
        },
        2: {
            "title": "Colours in Nature",
            "text": (
                "Nature is full of colours! Flamingos are pink. The ocean is blue. "
                "Sunflowers are yellow. Parrots can be red, green and blue! "
                "In autumn, leaves turn orange and red. Colours are everywhere!"
            ),
            "question": "What is your favourite colour in nature?",
            "country_flag": "",
            "recipe": None,
        },
        3: {
            "title": "Counting in Different Countries",
            "text": (
                "Children around the world count! In China, children use special symbols for numbers. "
                "In Egypt, people used to draw pictures to count. "
                "In Turkey, children count 'bir, iki, uc, dort, bes!' "
                "Numbers are the same everywhere — one, two, three!"
            ),
            "question": "Can you count to five in Turkish and English?",
            "country_flag": "CN, EG, TR",
            "recipe": None,
        },
        4: {
            "title": "Weather Around the World",
            "text": (
                "Weather is different everywhere! In Africa, it can be very hot and sunny. "
                "In the North Pole, there is lots of snow. In England, it rains a lot! "
                "In Turkey, we have sunny summers and snowy winters."
            ),
            "question": "What weather do you like best — sunny or snowy?",
            "country_flag": "GB, TR",
            "recipe": None,
        },
        5: {
            "title": "Parties Around the World",
            "text": (
                "Children love parties everywhere! In Mexico, children hit a pinata at parties. "
                "In India, they have colourful festivals with lights. "
                "In Turkey, we celebrate bayrams with sweets and family. "
                "What do you do at your parties?"
            ),
            "question": "Draw your favourite party food!",
            "country_flag": "MX, IN, TR",
            "recipe": None,
        },
        6: {
            "title": "Farm Animals Everywhere",
            "text": (
                "Farms look different around the world! In Australia, farms are very big with sheep. "
                "In India, cows are very special. In Holland, there are many dairy cows. "
                "In Turkey, we have farms with cows, sheep, chickens and goats!"
            ),
            "question": "Have you ever visited a farm?",
            "country_flag": "AU, IN, NL, TR",
            "recipe": None,
        },
        7: {
            "title": "Seasons and Festivals",
            "text": (
                "Every season has special celebrations! In spring, people in Japan have cherry blossom festivals. "
                "In summer, children in Turkey go to the beach. "
                "In autumn, Americans celebrate Thanksgiving. "
                "In winter, many countries celebrate with lights and gifts!"
            ),
            "question": "What is your favourite season and why?",
            "country_flag": "JP, TR, US",
            "recipe": None,
        },
        8: {
            "title": "Beaches of the World",
            "text": (
                "There are beautiful beaches everywhere! In the Maldives, the water is very clear. "
                "In Brazil, the beaches are very long. In Turkey, we have amazing beaches in Antalya and Bodrum. "
                "Children all around the world love to play in the sand!"
            ),
            "question": "Have you been to a beach? What did you do?",
            "country_flag": "MV, BR, TR",
            "recipe": None,
        },
        9: {
            "title": "Helpers Everywhere",
            "text": (
                "Every country has helpers! Firefighters in America have big red trucks. "
                "Doctors in Africa help many people in villages. "
                "In Turkey, our helpers work hard to keep us safe and healthy. "
                "Helpers are heroes everywhere!"
            ),
            "question": "Who is your favourite helper? Draw a picture!",
            "country_flag": "US, TR",
            "recipe": None,
        },
        10: {
            "title": "Goodbye Traditions",
            "text": (
                "People say goodbye differently around the world! "
                "In France, people kiss on both cheeks. In Japan, people bow. "
                "In Italy, people say 'Ciao!' In Turkey, we hug and say 'Hosca kal!' "
                "Goodbye is never forever — we always meet again!"
            ),
            "question": "How do you say goodbye to your friends?",
            "country_flag": "FR, JP, IT, TR",
            "recipe": None,
        },
    },
}

PROJECT_BANK = {
    0: {
        1: {
            "title": "My Name Badge",
            "desc": "Make a colourful name badge to wear in class!",
            "steps": ["Write your name on the card.", "Draw a picture of yourself.",
                      "Colour it with your favourite colours.", "Add stickers.",
                      "Wear it and say 'Hello! My name is ___!'"],
            "materials": "Card, crayons, stickers, safety pin",
        },
        2: {
            "title": "Colour Wheel",
            "desc": "Make a spinning colour wheel!",
            "steps": ["Cut a circle from card.", "Divide it into 5 parts.",
                      "Colour each part: red, blue, yellow, green, orange.",
                      "Push a pencil through the middle.",
                      "Spin it and say the colours!"],
            "materials": "Card, crayons, pencil, scissors",
        },
        3: {
            "title": "Number Caterpillar",
            "desc": "Make a caterpillar with numbers 1 to 10!",
            "steps": ["Cut 10 circles from coloured paper.", "Write numbers 1-10 on them.",
                      "Glue them in a line to make a caterpillar.",
                      "Draw a face on number 1.",
                      "Add legs and antennae. Count together!"],
            "materials": "Coloured paper, glue, scissors, markers",
        },
        4: {
            "title": "Weather Chart",
            "desc": "Make a daily weather chart for the classroom!",
            "steps": ["Draw a big chart with 5 days.", "Draw weather symbols: sun, cloud, rain, snow, wind.",
                      "Each day, look outside.", "Put the right symbol on the chart.",
                      "Say 'Today it is ___!'"],
            "materials": "Large paper, markers, blu-tack",
        },
        5: {
            "title": "Party Hat",
            "desc": "Make a party hat for our class party!",
            "steps": ["Roll a piece of card into a cone.", "Tape it together.",
                      "Decorate with stickers and glitter.",
                      "Write 'Happy Party!' on it.",
                      "Wear it and dance!"],
            "materials": "Card, tape, stickers, glitter, elastic band",
        },
        6: {
            "title": "Farm Animal Masks",
            "desc": "Make a farm animal mask and pretend to be that animal!",
            "steps": ["Choose an animal: cow, sheep, horse, chicken, or pig.",
                      "Cut a mask shape from card.",
                      "Draw and colour the animal face.",
                      "Cut eye holes.", "Wear it and make the animal sound!"],
            "materials": "Card, crayons, scissors, elastic band",
        },
        7: {
            "title": "Seasons Poster",
            "desc": "Make a poster showing all four seasons!",
            "steps": ["Fold a big paper into 4 parts.", "Write: Spring, Summer, Autumn, Winter.",
                      "Draw pictures for each season.",
                      "Colour them with matching colours.",
                      "Present your poster to the class!"],
            "materials": "Large paper, crayons, coloured pencils",
        },
        8: {
            "title": "Beach in a Box",
            "desc": "Make a mini beach scene in a shoebox!",
            "steps": ["Put sand (or yellow paper) in the box.",
                      "Add blue paper for the sea.",
                      "Make a tiny sandcastle from play dough.",
                      "Add shells and a paper umbrella.",
                      "Show your beach and say what you see!"],
            "materials": "Shoebox, sand or yellow paper, blue paper, play dough, shells",
        },
        9: {
            "title": "Helper Puppets",
            "desc": "Make finger puppets of community helpers!",
            "steps": ["Cut small rectangles from paper.",
                      "Draw a helper on each: doctor, teacher, police, fire fighter, cook.",
                      "Roll them into finger tubes and tape.",
                      "Put them on your fingers.",
                      "Act out a helper story with your puppets!"],
            "materials": "Paper, markers, tape, scissors",
        },
        10: {
            "title": "My Memory Book",
            "desc": "Make a book of your favourite things from this year!",
            "steps": ["Fold 5 papers in half to make a book.",
                      "On each page, draw something you learned.",
                      "Write the English word under each picture.",
                      "Decorate the cover.",
                      "Share your book with your family!"],
            "materials": "Paper, stapler, crayons, stickers",
        },
    },
}

LISTENING_SCRIPT_BANK = {
    0: {
        1: {
            "title": "Hello, Friends!",
            "script": (
                "Narrator: Listen and point to the correct picture.\n\n"
                "Miss Lily: Hello, children!\n"
                "Children: Hello, Miss Lily!\n"
                "Miss Lily: What is your name?\n"
                "Sunny: My name is Sunny. Hello!\n"
                "Miss Lily: Hello, Sunny! And you?\n"
                "Benny: Hi! My name is Benny.\n"
                "Miss Lily: Very good! Now let's say hello to Paws!\n"
                "Everyone: Hello, Paws!"
            ),
            "tasks": [
                "Point to the person who says 'My name is Sunny.'",
                "How many children say hello?",
                "Say hello to your friend!",
            ],
        },
        2: {
            "title": "I See Colours!",
            "script": (
                "Narrator: Listen and colour the picture.\n\n"
                "Miss Lily: What colour is this?\n"
                "Sunny: Red! It's red!\n"
                "Miss Lily: Very good! And this one?\n"
                "Benny: Blue! Blue!\n"
                "Miss Lily: Excellent! Now this flower?\n"
                "Sunny: Yellow! A yellow flower!\n"
                "Miss Lily: And the tree?\n"
                "Benny: Green! The tree is green!\n"
                "Miss Lily: Well done, everyone!"
            ),
            "tasks": [
                "Colour the apple RED.",
                "Colour the sky BLUE.",
                "What colour is the flower?",
            ],
        },
        3: {
            "title": "Let's Count!",
            "script": (
                "Narrator: Listen and count with Miss Lily.\n\n"
                "Miss Lily: Let's count the animals! How many cats?\n"
                "Children: One! One cat!\n"
                "Miss Lily: How many dogs?\n"
                "Children: Two! Two dogs!\n"
                "Miss Lily: How many birds?\n"
                "Children: Three! Three birds!\n"
                "Miss Lily: How many fish?\n"
                "Children: Four! Four fish!\n"
                "Miss Lily: And how many rabbits?\n"
                "Children: Five! Five rabbits!\n"
                "Miss Lily: One, two, three, four, five! Well done!"
            ),
            "tasks": [
                "Count: how many cats? Write the number.",
                "How many animals in total?",
                "Count five things on your desk!",
            ],
        },
        4: {
            "title": "What's the Weather?",
            "script": (
                "Narrator: Listen and circle the correct weather.\n\n"
                "Miss Lily: Good morning! Look outside. What's the weather today?\n"
                "Sunny: It's sunny! I can see the sun!\n"
                "Miss Lily: Is it rainy?\n"
                "Benny: No! It's not rainy. It's sunny!\n"
                "Miss Lily: Is it cloudy?\n"
                "Sunny: A little bit cloudy, but mostly sunny!\n"
                "Miss Lily: Great! Today is sunny. Let's draw the sun!"
            ),
            "tasks": [
                "Circle the correct weather picture: sunny, rainy or snowy?",
                "Is it cloudy? Yes or no?",
                "Draw today's weather!",
            ],
        },
        5: {
            "title": "Party Time!",
            "script": (
                "Narrator: Listen and do the actions.\n\n"
                "Miss Lily: It's party time! Are you ready?\n"
                "Children: Yes!\n"
                "Miss Lily: Clap your hands! (clap clap clap)\n"
                "Miss Lily: Stamp your feet! (stamp stamp stamp)\n"
                "Miss Lily: Jump up high! (jump!)\n"
                "Miss Lily: Turn around! (wheee!)\n"
                "Miss Lily: Now dance! Dance, dance, dance!\n"
                "Children: Yay! Happy party!"
            ),
            "tasks": [
                "Do the actions: clap, stamp, jump, turn, dance!",
                "What comes first — clap or jump?",
                "What is your favourite party action?",
            ],
        },
        6: {
            "title": "On the Farm",
            "script": (
                "Narrator: Listen to the animal sounds. What animal is it?\n\n"
                "Miss Lily: Shh! Listen! What animal is this?\n"
                "Sound: MOOO!\n"
                "Children: A cow!\n"
                "Miss Lily: And this?\n"
                "Sound: BAAA!\n"
                "Children: A sheep!\n"
                "Miss Lily: This one?\n"
                "Sound: NEIGH!\n"
                "Children: A horse!\n"
                "Miss Lily: Last one!\n"
                "Sound: OINK OINK!\n"
                "Children: A pig!"
            ),
            "tasks": [
                "Match the sound to the animal picture.",
                "Which animal says 'Baa'?",
                "Make a farm animal sound for your friend to guess!",
            ],
        },
        7: {
            "title": "Four Seasons",
            "script": (
                "Narrator: Listen and point to the correct season.\n\n"
                "Miss Lily: In spring, flowers grow. Can you see flowers?\n"
                "Sunny: Yes! Pink and yellow flowers!\n"
                "Miss Lily: In summer, it is hot. We go to the beach!\n"
                "Benny: I love summer!\n"
                "Miss Lily: In autumn, leaves fall from trees.\n"
                "Sunny: Orange and red leaves!\n"
                "Miss Lily: In winter, it snows. We wear coats!\n"
                "Benny: I like snow!"
            ),
            "tasks": [
                "Point to the season with flowers — spring.",
                "When do leaves fall? Circle the picture.",
                "What do we wear in winter?",
            ],
        },
        8: {
            "title": "At the Beach",
            "script": (
                "Narrator: Listen and tick the things you hear.\n\n"
                "Sunny: I can see the sea! Blue sea!\n"
                "Benny: Look! Sand! Let's build a sandcastle!\n"
                "Sunny: I found a shell! A pink shell!\n"
                "Benny: Where is my bucket? Oh, here it is!\n"
                "Sunny: Put on your sunglasses! The sun is bright!\n"
                "Benny: Let's play in the water! Splash!"
            ),
            "tasks": [
                "Tick: sea, sand, shell, bucket, sunglasses.",
                "What colour is the shell?",
                "What do they build?",
            ],
        },
        9: {
            "title": "Who Helps Us?",
            "script": (
                "Narrator: Listen and match the helper to the picture.\n\n"
                "Miss Lily: Who helps us when we are sick?\n"
                "Children: The doctor!\n"
                "Miss Lily: Who teaches us at school?\n"
                "Children: The teacher!\n"
                "Miss Lily: Who keeps us safe on the street?\n"
                "Children: The police!\n"
                "Miss Lily: Who puts out fires?\n"
                "Children: The fire fighter!\n"
                "Miss Lily: Who makes our lunch?\n"
                "Children: The cook!"
            ),
            "tasks": [
                "Match each helper to their picture.",
                "Who helps when we are sick?",
                "Draw a helper you want to be!",
            ],
        },
        10: {
            "title": "Goodbye, See You!",
            "script": (
                "Narrator: Listen to the goodbye messages.\n\n"
                "Sunny: Goodbye, Benny! See you in summer!\n"
                "Benny: Goodbye, Sunny! I will miss you!\n"
                "Paws: Goodbye, friends! Meow!\n"
                "Rainbow: Goodbye! Goodbye! See you! See you!\n"
                "Miss Lily: Goodbye, children! You are all wonderful! "
                "Have a happy holiday!\n"
                "Everyone: Goodbye, Miss Lily! Thank you!"
            ),
            "tasks": [
                "Who says 'I will miss you'?",
                "What does Miss Lily say?",
                "Say goodbye to your friends!",
            ],
        },
    },
}

FUN_FACTS_BANK = {
    0: {
        1: ["A cat can say 'meow' in every language!", "Babies can hear sounds before they are born!", "Some people say 'hello' by touching noses!"],
        2: ["Carrots used to be purple, not orange!", "Dogs can only see blue and yellow!", "Rainbows have seven colours!"],
        3: ["Octopuses have eight arms — more than five!", "A starfish has no brain!", "Ants can carry things 50 times heavier than themselves!"],
        4: ["It can rain frogs! (It really happened!)", "The Sun is a star, not a planet!", "A cloud can weigh as much as 100 elephants!"],
        5: ["Balloons were first made from animal bladders!", "The first birthday cake was from Germany!", "Confetti means 'sweets' in Italian!"],
        6: ["A cow has four stomachs!", "Chickens can run very fast!", "A group of flamingos is called a 'flamboyance'!"],
        7: ["In the Arctic, the sun does not set for months!", "Leaves change colour because they stop making green!", "Some trees are over 5000 years old!"],
        8: ["The ocean is home to the biggest animal — the blue whale!", "Sea horses are fish, not horses!", "Sand is made from tiny broken shells and rocks!"],
        9: ["Firefighters used to ride horses to fires!", "Doctors used to not wash their hands!", "The first police officers did not wear uniforms!"],
        10: ["The word 'goodbye' comes from 'God be with you'!", "Parrots can live for 80 years!", "Elephants never forget their friends!"],
    },
}

GAMIFICATION_BANK = {
    0: {
        "levels": [
            {"name": "Baby Star", "xp_min": 0, "xp_max": 49, "icon": "⭐"},
            {"name": "Shining Star", "xp_min": 50, "xp_max": 149, "icon": "🌟"},
            {"name": "Super Star", "xp_min": 150, "xp_max": 299, "icon": "💫"},
            {"name": "Rainbow Star", "xp_min": 300, "xp_max": 500, "icon": "🌈"},
        ],
        "unit_badges": {
            1: {"badge": "Hello Hero", "desc": "Say hello to 5 friends in English!", "xp": 20},
            2: {"badge": "Colour Champion", "desc": "Name all 5 colours correctly!", "xp": 20},
            3: {"badge": "Number Ninja", "desc": "Count from 1 to 10 without help!", "xp": 25},
            4: {"badge": "Weather Watcher", "desc": "Tell the weather for 3 days in English!", "xp": 20},
            5: {"badge": "Party Star", "desc": "Sing and dance to all the songs!", "xp": 25},
            6: {"badge": "Animal Expert", "desc": "Name all 5 farm animals with sounds!", "xp": 25},
            7: {"badge": "Season Singer", "desc": "Sing the Seasons Rap perfectly!", "xp": 20},
            8: {"badge": "Beach Explorer", "desc": "Name 5 beach things in English!", "xp": 20},
            9: {"badge": "Helper Heart", "desc": "Act out all 5 helpers!", "xp": 25},
            10: {"badge": "Goodbye Graduate", "desc": "Complete the year and say goodbye in English!", "xp": 30},
        },
        "bonus_xp": [
            {"action": "Sing a song perfectly", "xp": 10},
            {"action": "Help a friend learn a word", "xp": 10},
            {"action": "Say 3 English words at home", "xp": 10},
            {"action": "Draw and label a picture in English", "xp": 15},
            {"action": "Bring something from home and name it in English", "xp": 15},
        ],
    },
}

# ---------------------------------------------------------------------------
# READING BANK  (Simple 3-5 sentence texts for preschool, ages 4-6)
# ---------------------------------------------------------------------------
READING_BANK = {
    0: {
        1: {
            "title": "Hello, Paws!",
            "text": (
                "Paws is a cat. Paws is orange. "
                "Paws says hello. Hello, Paws!"
            ),
            "questions": [
                {"type": "mcq", "q": "What is Paws?", "opts": ["a) A dog", "b) A cat", "c) A bird"], "answer": "b"},
                {"type": "tf", "q": "Paws is blue.", "answer": "F"},
                {"type": "open", "q": "What does Paws say?", "lines": 1},
            ],
        },
        2: {
            "title": "I See Colours",
            "text": (
                "I see red. I see blue. I see yellow. "
                "I see green. Colours are fun!"
            ),
            "questions": [
                {"type": "mcq", "q": "How many colours do you see?", "opts": ["a) Three", "b) Four", "c) Five"], "answer": "b"},
                {"type": "tf", "q": "I see purple.", "answer": "F"},
                {"type": "open", "q": "What colour do you like?", "lines": 1},
            ],
        },
        3: {
            "title": "Count With Me",
            "text": (
                "One ball. Two balls. Three balls. "
                "Four balls. Five balls. Let's count!"
            ),
            "questions": [
                {"type": "mcq", "q": "How many balls are there?", "opts": ["a) Three", "b) Four", "c) Five"], "answer": "c"},
                {"type": "tf", "q": "There are six balls.", "answer": "F"},
                {"type": "open", "q": "Can you count to five?", "lines": 1},
            ],
        },
        4: {
            "title": "A Rainy Day",
            "text": (
                "It is rainy. Paws has a hat. "
                "Sunny has socks. They are warm now."
            ),
            "questions": [
                {"type": "mcq", "q": "How is the weather?", "opts": ["a) Sunny", "b) Rainy", "c) Snowy"], "answer": "b"},
                {"type": "tf", "q": "Paws has a hat.", "answer": "T"},
                {"type": "open", "q": "Who has socks?", "lines": 1},
            ],
        },
        5: {
            "title": "The Toy Box",
            "text": (
                "I have a ball. I have a doll. "
                "I have a car. I love my toys!"
            ),
            "questions": [
                {"type": "mcq", "q": "What toys are in the story?", "opts": ["a) Ball, doll, car", "b) Ball, kite, train", "c) Doll, puzzle, robot"], "answer": "a"},
                {"type": "tf", "q": "I have a kite.", "answer": "F"},
                {"type": "open", "q": "What is your favourite toy?", "lines": 1},
            ],
        },
        6: {
            "title": "On the Farm",
            "text": (
                "I see a cow. I see a sheep. "
                "I see a horse. The farm is fun!"
            ),
            "questions": [
                {"type": "mcq", "q": "Where are the animals?", "opts": ["a) At school", "b) On the farm", "c) At the beach"], "answer": "b"},
                {"type": "tf", "q": "I see a dog on the farm.", "answer": "F"},
                {"type": "open", "q": "What animal do you like?", "lines": 1},
            ],
        },
        7: {
            "title": "Four Seasons",
            "text": (
                "Spring has flowers. Summer is hot. "
                "Autumn has leaves. Winter has snow."
            ),
            "questions": [
                {"type": "mcq", "q": "Which season has snow?", "opts": ["a) Spring", "b) Summer", "c) Winter"], "answer": "c"},
                {"type": "tf", "q": "Spring has flowers.", "answer": "T"},
                {"type": "open", "q": "What is your favourite season?", "lines": 1},
            ],
        },
        8: {
            "title": "At the Beach",
            "text": (
                "I see the sea. I see the sand. "
                "I have a bucket. The beach is fun!"
            ),
            "questions": [
                {"type": "mcq", "q": "What do I have?", "opts": ["a) A ball", "b) A bucket", "c) A hat"], "answer": "b"},
                {"type": "tf", "q": "The beach is boring.", "answer": "F"},
                {"type": "open", "q": "Do you like the beach?", "lines": 1},
            ],
        },
        9: {
            "title": "Our Helpers",
            "text": (
                "The doctor helps us. The teacher helps us. "
                "The cook makes food. Helpers are kind!"
            ),
            "questions": [
                {"type": "mcq", "q": "Who makes food?", "opts": ["a) The doctor", "b) The teacher", "c) The cook"], "answer": "c"},
                {"type": "tf", "q": "The teacher helps us.", "answer": "T"},
                {"type": "open", "q": "Who helps you?", "lines": 1},
            ],
        },
        10: {
            "title": "Goodbye, Friends!",
            "text": (
                "It is the last day. We say goodbye. "
                "We are happy. See you soon, friends!"
            ),
            "questions": [
                {"type": "mcq", "q": "What do we say?", "opts": ["a) Hello", "b) Goodbye", "c) Thank you"], "answer": "b"},
                {"type": "tf", "q": "We are sad.", "answer": "F"},
                {"type": "open", "q": "Say goodbye to a friend!", "lines": 1},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# GRAMMAR BANK  (Very basic patterns for preschool, ages 4-6)
# ---------------------------------------------------------------------------
GRAMMAR_BANK = {
    0: {
        1: {
            "title": "Hello! / My name is...",
            "rule": "Say 'Hello!' to greet someone. Say 'My name is ___' to tell your name.",
            "examples": [
                "Hello! My name is Paws.",
                "Hi! My name is Sunny.",
                "Hello! I am Benny.",
            ],
        },
        2: {
            "title": "It is... (Colours)",
            "rule": "Use 'It is ___' to say the colour of something.",
            "examples": [
                "It is red.",
                "It is blue.",
                "It is yellow.",
                "It is green.",
            ],
        },
        3: {
            "title": "This is a... (Numbers & Things)",
            "rule": "Use 'This is a ___' to name something near you.",
            "examples": [
                "This is a ball.",
                "This is a teddy bear.",
                "This is one car.",
                "This is two blocks.",
            ],
        },
        4: {
            "title": "It is... (Weather)",
            "rule": "Use 'It is ___' to talk about the weather.",
            "examples": [
                "It is sunny.",
                "It is rainy.",
                "It is cloudy.",
                "It is cold.",
            ],
        },
        5: {
            "title": "I have a... (Toys)",
            "rule": "Use 'I have a ___' to say what toy you have.",
            "examples": [
                "I have a ball.",
                "I have a doll.",
                "I have a car.",
                "I have a puzzle.",
            ],
        },
        6: {
            "title": "I see a... (Animals)",
            "rule": "Use 'I see a ___' to say what animal you see.",
            "examples": [
                "I see a cow.",
                "I see a sheep.",
                "I see a horse.",
                "I see a chicken.",
            ],
        },
        7: {
            "title": "I like... (Seasons)",
            "rule": "Use 'I like ___' to say your favourite season.",
            "examples": [
                "I like spring.",
                "I like summer.",
                "I like autumn.",
                "I like winter.",
            ],
        },
        8: {
            "title": "I can see... (Beach)",
            "rule": "Use 'I can see ___' to say what you see at the beach.",
            "examples": [
                "I can see the sea.",
                "I can see a shell.",
                "I can see the sand.",
                "I can see a bucket.",
            ],
        },
        9: {
            "title": "This is a... (Helpers)",
            "rule": "Use 'This is a ___' to name a community helper.",
            "examples": [
                "This is a doctor.",
                "This is a teacher.",
                "This is a cook.",
                "This is a police officer.",
            ],
        },
        10: {
            "title": "Goodbye! / See you!",
            "rule": "Say 'Goodbye!' or 'See you!' when you leave.",
            "examples": [
                "Goodbye, friends!",
                "See you soon!",
                "Bye bye!",
                "See you in summer!",
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# PROGRESS CHECK BANK  (Review questions per unit for preschool)
# ---------------------------------------------------------------------------
PROGRESS_CHECK_BANK = {
    0: {
        1: {
            "vocab": ["hello", "hi", "name", "friend", "bye"],
            "grammar": ["Hello!", "My name is ___.", "Hi! I am ___."],
            "reading": ["Who is Paws?", "What does Paws say?"],
            "writing": ["Write your name.", "Draw yourself and write 'Hello!'"],
        },
        2: {
            "vocab": ["red", "blue", "yellow", "green", "orange"],
            "grammar": ["It is red.", "It is blue.", "It is ___."],
            "reading": ["What colours do you see?", "Is there purple in the story?"],
            "writing": ["Colour the picture and write the colour name.", "Draw something red."],
        },
        3: {
            "vocab": ["one", "two", "three", "four", "five"],
            "grammar": ["This is one ball.", "This is two cars.", "I have ___ blocks."],
            "reading": ["How many balls are there?", "Can you count to five?"],
            "writing": ["Write the numbers 1 to 5.", "Draw three stars."],
        },
        4: {
            "vocab": ["sun", "rain", "cloud", "hat", "socks"],
            "grammar": ["It is sunny.", "It is rainy.", "It is cold."],
            "reading": ["How is the weather?", "What does Paws wear?"],
            "writing": ["Draw today's weather.", "Write 'It is ___.'"],
        },
        5: {
            "vocab": ["ball", "doll", "car", "puzzle", "party"],
            "grammar": ["I have a ball.", "I have a doll.", "I have a ___."],
            "reading": ["What toys are in the box?", "What is your favourite toy?"],
            "writing": ["Draw your favourite toy.", "Write 'I have a ___.'"],
        },
        6: {
            "vocab": ["cow", "sheep", "horse", "chicken", "pig"],
            "grammar": ["I see a cow.", "I see a sheep.", "I see a ___."],
            "reading": ["Where are the animals?", "Which animal says 'Moo'?"],
            "writing": ["Draw a farm animal.", "Write 'I see a ___.'"],
        },
        7: {
            "vocab": ["spring", "summer", "autumn", "winter", "tree"],
            "grammar": ["I like spring.", "I like summer.", "I like ___."],
            "reading": ["Which season has snow?", "Which season has flowers?"],
            "writing": ["Draw your favourite season.", "Write 'I like ___.'"],
        },
        8: {
            "vocab": ["sand", "sea", "shell", "bucket", "sunglasses"],
            "grammar": ["I can see the sea.", "I can see a shell.", "I can see ___."],
            "reading": ["What do I have at the beach?", "Is the beach fun?"],
            "writing": ["Draw the beach.", "Write 'I can see ___.'"],
        },
        9: {
            "vocab": ["doctor", "teacher", "police", "fire fighter", "cook"],
            "grammar": ["This is a doctor.", "This is a teacher.", "This is a ___."],
            "reading": ["Who makes food?", "Who helps sick people?"],
            "writing": ["Draw a helper.", "Write 'This is a ___.'"],
        },
        10: {
            "vocab": ["goodbye", "see you", "miss you", "summer", "holiday"],
            "grammar": ["Goodbye!", "See you soon!", "Bye bye!"],
            "reading": ["What do we say on the last day?", "Are we happy or sad?"],
            "writing": ["Write 'Goodbye!' to a friend.", "Draw your best memory from this year."],
        },
    },
}

# ---------------------------------------------------------------------------
# DIALOGUE BANK  (simplified 2-4 line exchanges for ages 4-6)
# ---------------------------------------------------------------------------
DIALOGUE_BANK = {
    0: {
        1: {
            "setting": "Classroom",
            "characters": ["Sunny", "Benny"],
            "lines": [
                ("Sunny", "Hello! What is your name?"),
                ("Benny", "My name is Benny!"),
                ("Sunny", "Nice to meet you!"),
                ("Benny", "Nice to meet you too!"),
            ],
            "focus_language": "Greetings",
            "task": "Say hello to 3 friends!",
        },
        2: {
            "setting": "Art Corner",
            "characters": ["Paws", "Rainbow"],
            "lines": [
                ("Paws", "What colour is this?"),
                ("Rainbow", "It is RED!"),
                ("Paws", "Good! And this one?"),
                ("Rainbow", "It is BLUE!"),
            ],
            "focus_language": "Colours",
            "task": "Point to 3 colours in the classroom and say them!",
        },
        3: {
            "setting": "Playground",
            "characters": ["Sunny", "Paws"],
            "lines": [
                ("Sunny", "Let's count! One, two, three!"),
                ("Paws", "Four, five!"),
                ("Sunny", "How many balls?"),
                ("Paws", "Three balls!"),
            ],
            "focus_language": "Numbers 1-5",
            "task": "Count 5 things on your desk!",
        },
        4: {
            "setting": "Farm",
            "characters": ["Benny", "Rainbow"],
            "lines": [
                ("Benny", "What is that?"),
                ("Rainbow", "It is a cat!"),
                ("Benny", "What sound does it make?"),
                ("Rainbow", "Meow! Meow!"),
            ],
            "focus_language": "Animals",
            "task": "Make 3 animal sounds!",
        },
        5: {
            "setting": "Kitchen",
            "characters": ["Sunny", "Paws"],
            "lines": [
                ("Sunny", "Do you like apples?"),
                ("Paws", "Yes! I like apples!"),
                ("Sunny", "What colour is the banana?"),
                ("Paws", "Yellow!"),
            ],
            "focus_language": "Fruits / Food",
            "task": "Tell a friend your favourite fruit!",
        },
        6: {
            "setting": "Mirror Corner",
            "characters": ["Benny", "Sunny"],
            "lines": [
                ("Benny", "Touch your nose!"),
                ("Sunny", "This is my nose!"),
                ("Benny", "Clap your hands!"),
                ("Sunny", "Clap, clap, clap!"),
            ],
            "focus_language": "Body parts",
            "task": "Touch and say 5 body parts!",
        },
        7: {
            "setting": "Home",
            "characters": ["Paws", "Sunny"],
            "lines": [
                ("Paws", "Who is this?"),
                ("Sunny", "This is my mum!"),
                ("Paws", "And this?"),
                ("Sunny", "This is my dad!"),
            ],
            "focus_language": "Family members",
            "task": "Draw your family and say who they are!",
        },
        8: {
            "setting": "Dress-Up Corner",
            "characters": ["Rainbow", "Benny"],
            "lines": [
                ("Rainbow", "What are you wearing?"),
                ("Benny", "A red hat!"),
                ("Rainbow", "I like your hat!"),
                ("Benny", "Thank you!"),
            ],
            "focus_language": "Clothes",
            "task": "Point to your clothes and say the colour!",
        },
        9: {
            "setting": "Window",
            "characters": ["Sunny", "Rainbow"],
            "lines": [
                ("Sunny", "Look! Is it sunny?"),
                ("Rainbow", "No! It is rainy!"),
                ("Sunny", "We need an umbrella!"),
                ("Rainbow", "Yes! A big umbrella!"),
            ],
            "focus_language": "Weather",
            "task": "Look outside. What is the weather today? Tell a friend!",
        },
        10: {
            "setting": "Classroom",
            "characters": ["Paws", "Benny"],
            "lines": [
                ("Paws", "Goodbye, Benny!"),
                ("Benny", "Goodbye, Paws!"),
                ("Paws", "See you in summer!"),
                ("Benny", "Have fun! Bye bye!"),
            ],
            "focus_language": "Saying goodbye",
            "task": "Say goodbye to everyone in class!",
        },
    },
}

# ---------------------------------------------------------------------------
# MODEL WRITING BANK  (trace + draw for preschool – no real writing)
# ---------------------------------------------------------------------------
MODEL_WRITING_BANK = {
    0: {
        1: {
            "type": "trace_and_draw",
            "model": "Hello! My name is ___.",
            "task": "Trace the word 'Hello'. Draw yourself. Teacher writes your name.",
            "key_words": ["Hello", "name"],
        },
        2: {
            "type": "trace_and_draw",
            "model": "I see RED. I see BLUE.",
            "task": "Trace 'RED' and 'BLUE'. Colour the circles with the right colour.",
            "key_words": ["red", "blue", "green", "yellow"],
        },
        3: {
            "type": "trace_and_draw",
            "model": "1 2 3 4 5",
            "task": "Trace the numbers 1 to 5. Draw that many stars next to each number.",
            "key_words": ["one", "two", "three", "four", "five"],
        },
        4: {
            "type": "trace_and_draw",
            "model": "I like cats. I like dogs.",
            "task": "Trace 'cat' and 'dog'. Draw your favourite animal.",
            "key_words": ["cat", "dog", "bird", "fish"],
        },
        5: {
            "type": "trace_and_draw",
            "model": "I like apples.",
            "task": "Trace the word 'apple'. Draw and colour 3 fruits.",
            "key_words": ["apple", "banana", "orange"],
        },
        6: {
            "type": "trace_and_draw",
            "model": "This is my hand.",
            "task": "Trace the word 'hand'. Put your hand on the paper and draw around it!",
            "key_words": ["hand", "head", "foot"],
        },
        7: {
            "type": "trace_and_draw",
            "model": "I love my family.",
            "task": "Trace the word 'family'. Draw your family. Teacher writes the names.",
            "key_words": ["mum", "dad", "family"],
        },
        8: {
            "type": "trace_and_draw",
            "model": "I have a hat.",
            "task": "Trace 'hat'. Draw yourself wearing your favourite clothes. Colour them!",
            "key_words": ["hat", "shirt", "shoes"],
        },
        9: {
            "type": "trace_and_draw",
            "model": "It is sunny!",
            "task": "Trace 'sunny'. Draw today's weather. Add a big sun or raindrops!",
            "key_words": ["sunny", "rainy", "cloudy"],
        },
        10: {
            "type": "trace_and_draw",
            "model": "Goodbye! See you!",
            "task": "Trace 'Goodbye'. Draw a picture for your friend as a goodbye gift.",
            "key_words": ["goodbye", "see you", "bye"],
        },
    },
}

# ---------------------------------------------------------------------------
# PRONUNCIATION BANK  (sounds, chants, TPR for ages 4-6)
# ---------------------------------------------------------------------------
PRONUNCIATION_BANK = {
    0: {
        1: {
            "sound": "/h/ as in Hello",
            "words": ["hello", "happy", "hat", "hand", "house"],
            "chant": "H-H-Hello! H-H-Happy! H-H-Hat on my head!",
            "action": "Wave your hand when you hear /h/!",
        },
        2: {
            "sound": "/r/ as in Red",
            "words": ["red", "run", "rain", "ring", "rabbit"],
            "chant": "R-R-Red! R-R-Run! R-R-Ring the bell!",
            "action": "Run in place when you hear /r/!",
        },
        3: {
            "sound": "/w/ as in One",
            "words": ["one", "two", "water", "walk", "wave"],
            "chant": "W-W-One! W-W-Walk! W-W-Wave hello!",
            "action": "Wave when you hear /w/!",
        },
        4: {
            "sound": "/k/ as in Cat",
            "words": ["cat", "cow", "cup", "cake", "car"],
            "chant": "K-K-Cat! K-K-Cow! K-K-Cup of milk!",
            "action": "Pretend to be a cat when you hear /k/!",
        },
        5: {
            "sound": "/æ/ as in Apple",
            "words": ["apple", "ant", "alligator", "add", "am"],
            "chant": "A-A-Apple! A-A-Ant! A-A-Am I hungry?",
            "action": "Pretend to eat an apple when you hear /æ/!",
        },
        6: {
            "sound": "/n/ as in Nose",
            "words": ["nose", "neck", "nine", "nut", "net"],
            "chant": "N-N-Nose! N-N-Neck! N-N-Nine little nuts!",
            "action": "Touch your nose when you hear /n/!",
        },
        7: {
            "sound": "/m/ as in Mum",
            "words": ["mum", "moon", "milk", "mouse", "mouth"],
            "chant": "M-M-Mum! M-M-Moon! M-M-Milk for me!",
            "action": "Hug yourself when you hear /m/!",
        },
        8: {
            "sound": "/ʃ/ as in Shirt",
            "words": ["shirt", "shoes", "ship", "shell", "sheep"],
            "chant": "Sh-Sh-Shirt! Sh-Sh-Shoes! Sh-Sh-Shell on the beach!",
            "action": "Put your finger to your lips and say shhhh!",
        },
        9: {
            "sound": "/s/ as in Sun",
            "words": ["sun", "sky", "star", "snow", "sand"],
            "chant": "S-S-Sun! S-S-Sky! S-S-Star up high!",
            "action": "Point to the sky when you hear /s/!",
        },
        10: {
            "sound": "/b/ as in Bye",
            "words": ["bye", "ball", "bus", "blue", "book"],
            "chant": "B-B-Bye! B-B-Ball! B-B-Blue balloon!",
            "action": "Wave goodbye when you hear /b/!",
        },
    },
}

# ---------------------------------------------------------------------------
# WORKBOOK BANK  (colouring, matching, circling – no writing)
# ---------------------------------------------------------------------------
WORKBOOK_BANK = {
    0: {
        1: {
            "activities": [
                {"type": "colour", "instruction": "Colour the apple RED. Colour the sky BLUE."},
                {"type": "match", "instruction": "Match the colour to the object: red → apple, blue → sky, green → grass."},
                {"type": "circle", "instruction": "Circle all the RED things in the picture."},
            ],
        },
        2: {
            "activities": [
                {"type": "colour", "instruction": "Colour the sun YELLOW. Colour the tree GREEN."},
                {"type": "match", "instruction": "Match: yellow → sun, green → tree, orange → fish."},
                {"type": "circle", "instruction": "Circle all the BLUE things in the picture."},
            ],
        },
        3: {
            "activities": [
                {"type": "colour", "instruction": "Colour 3 stars yellow. Colour 2 balls red."},
                {"type": "match", "instruction": "Match the number to the group: 1 → one apple, 3 → three cats, 5 → five dots."},
                {"type": "circle", "instruction": "Circle the group that has 4 things."},
            ],
        },
        4: {
            "activities": [
                {"type": "colour", "instruction": "Colour the cat orange. Colour the bird blue."},
                {"type": "match", "instruction": "Match the animal to its sound: cat → meow, dog → woof, duck → quack."},
                {"type": "circle", "instruction": "Circle all the animals that fly."},
            ],
        },
        5: {
            "activities": [
                {"type": "colour", "instruction": "Colour the banana YELLOW. Colour the apple RED."},
                {"type": "match", "instruction": "Match: apple → red, banana → yellow, grapes → purple."},
                {"type": "circle", "instruction": "Circle the fruits. Cross out the things that are NOT fruits."},
            ],
        },
        6: {
            "activities": [
                {"type": "colour", "instruction": "Colour the eyes BLUE. Colour the hair BROWN."},
                {"type": "match", "instruction": "Match: eyes → see, ears → hear, nose → smell, mouth → eat."},
                {"type": "circle", "instruction": "Circle the body parts you can see in the picture."},
            ],
        },
        7: {
            "activities": [
                {"type": "colour", "instruction": "Colour the mum's hair. Colour the dad's shirt."},
                {"type": "match", "instruction": "Match: mum → woman, dad → man, baby → small, grandma → old."},
                {"type": "circle", "instruction": "Circle the family members in the big picture."},
            ],
        },
        8: {
            "activities": [
                {"type": "colour", "instruction": "Colour the hat RED. Colour the shoes BLUE."},
                {"type": "match", "instruction": "Match: hat → head, shoes → feet, gloves → hands."},
                {"type": "circle", "instruction": "Circle the clothes you wear when it is cold."},
            ],
        },
        9: {
            "activities": [
                {"type": "colour", "instruction": "Colour the sun YELLOW. Colour the rain BLUE."},
                {"type": "match", "instruction": "Match: sunny → sun picture, rainy → rain picture, snowy → snow picture."},
                {"type": "circle", "instruction": "Circle what you need on a rainy day: umbrella, sunglasses, boots, hat."},
            ],
        },
        10: {
            "activities": [
                {"type": "colour", "instruction": "Colour the beach. Use YELLOW for sand, BLUE for sea."},
                {"type": "match", "instruction": "Match: summer → sun, goodbye → hand waving, holiday → beach."},
                {"type": "circle", "instruction": "Circle things you take to the beach: bucket, ball, book, umbrella."},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# TURKEY CORNER BANK  (Turkish culture for little ones)
# ---------------------------------------------------------------------------
TURKEY_CORNER_BANK = {
    0: {
        1: {
            "title": "Turkish Flag",
            "fact": "The Turkish flag is red and white. It has a star and a moon.",
            "activity": "Colour the Turkish flag. Say: RED and WHITE!",
        },
        2: {
            "title": "Turkish Tea",
            "fact": "People in Turkey drink tea every day. They use small glasses.",
            "activity": "Draw a tea glass. Colour the tea BROWN. Say: Tea, please!",
        },
        3: {
            "title": "Counting in Turkish",
            "fact": "In Turkish, one is 'bir', two is 'iki', three is 'üç'.",
            "activity": "Count to 3 in Turkish: bir, iki, üç! Hold up your fingers!",
        },
        4: {
            "title": "Turkish Animals",
            "fact": "In Turkey, there are cats everywhere! Turkish people love cats.",
            "activity": "Draw a Turkish cat. Say: I love cats! Meow!",
        },
        5: {
            "title": "Turkish Breakfast",
            "fact": "Turkish breakfast has cheese, bread, tomatoes and olives.",
            "activity": "Draw a Turkish breakfast plate. Say: Cheese! Bread! Tomato!",
        },
        6: {
            "title": "Nasreddin Hodja",
            "fact": "Nasreddin Hodja is a funny wise man. He rode a donkey backwards!",
            "activity": "Draw Nasreddin Hodja on his donkey. Can you sit backwards on a chair?",
        },
        7: {
            "title": "Turkish Families",
            "fact": "In Turkey, families eat together. They say 'Afiyet olsun!' before eating.",
            "activity": "Draw your family at dinner. Say: Afiyet olsun! (Enjoy your meal!)",
        },
        8: {
            "title": "Turkish Clothes – Fes",
            "fact": "Long ago, people in Turkey wore a red hat called a fes.",
            "activity": "Draw a red fes hat. Put it on a funny face you draw!",
        },
        9: {
            "title": "Seasons in Turkey",
            "fact": "Turkey has 4 seasons: hot summer, cold winter, rainy spring, colourful autumn.",
            "activity": "Draw your favourite season. Say: I like ___ (summer/winter)!",
        },
        10: {
            "title": "Goodbye in Turkish",
            "fact": "In Turkish, 'goodbye' is 'Hoşça kal'. 'See you' is 'Görüşürüz'.",
            "activity": "Wave and say: Hoşça kal! Görüşürüz! Draw a waving hand!",
        },
    },
}

# ---------------------------------------------------------------------------
# COMIC STRIP BANK  (picture stories with minimal text)
# ---------------------------------------------------------------------------
COMIC_STRIP_BANK = {
    0: {
        1: {
            "title": "Paws Says Hello",
            "panels": [
                {"scene": "Paws the cat waves.", "speech": "Hello!"},
                {"scene": "Sunny waves back.", "speech": "Hello, Paws!"},
                {"scene": "They shake hands.", "speech": "Nice to meet you!"},
                {"scene": "Rainbow the parrot flies in.", "speech": "Hello! Hello! Hello!"},
            ],
            "drawing_task": "Draw yourself saying Hello to Paws!",
            "language_focus": "Greetings",
        },
        2: {
            "title": "Rainbow's Colour Mess",
            "panels": [
                {"scene": "Rainbow spills paint.", "speech": "Oh no! RED paint!"},
                {"scene": "Paws steps in blue paint.", "speech": "My paws are BLUE!"},
                {"scene": "Sunny mixes red and yellow.", "speech": "Look! ORANGE!"},
                {"scene": "Everyone is colourful.", "speech": "We are a rainbow!"},
            ],
            "drawing_task": "Draw Rainbow covered in colours!",
            "language_focus": "Colours",
        },
        3: {
            "title": "Benny Counts Balloons",
            "panels": [
                {"scene": "Benny holds 1 balloon.", "speech": "One balloon!"},
                {"scene": "Sunny gives him 2 more.", "speech": "Now you have three!"},
                {"scene": "Rainbow pops one.", "speech": "Pop! Now two!"},
                {"scene": "Miss Lily brings 3 big ones.", "speech": "Five balloons! Hooray!"},
            ],
            "drawing_task": "Draw 5 balloons and colour them!",
            "language_focus": "Numbers 1-5",
        },
        4: {
            "title": "Paws Visits the Farm",
            "panels": [
                {"scene": "Paws sees a cow.", "speech": "What is that? Moo!"},
                {"scene": "A duck swims in the pond.", "speech": "Quack quack!"},
                {"scene": "Paws chases a chicken.", "speech": "Come here, chicken!"},
                {"scene": "All animals sit together.", "speech": "We are all friends!"},
            ],
            "drawing_task": "Draw your favourite farm animal!",
            "language_focus": "Animals and sounds",
        },
        5: {
            "title": "Sunny's Fruit Salad",
            "panels": [
                {"scene": "Sunny picks an apple.", "speech": "A red apple!"},
                {"scene": "Benny brings a banana.", "speech": "A yellow banana!"},
                {"scene": "They cut the fruit.", "speech": "Chop chop chop!"},
                {"scene": "Everyone eats the salad.", "speech": "Yummy! I like fruit!"},
            ],
            "drawing_task": "Draw a big bowl of fruit salad!",
            "language_focus": "Fruits",
        },
        6: {
            "title": "The Body Song",
            "panels": [
                {"scene": "Miss Lily points to her head.", "speech": "Head!"},
                {"scene": "Paws touches his nose.", "speech": "Nose!"},
                {"scene": "Everyone claps.", "speech": "Hands! Clap clap!"},
                {"scene": "They all jump.", "speech": "Feet! Jump jump!"},
            ],
            "drawing_task": "Draw a funny body – big head, little feet!",
            "language_focus": "Body parts",
        },
        7: {
            "title": "Paws Meets the Family",
            "panels": [
                {"scene": "Sunny shows a photo.", "speech": "This is my mum!"},
                {"scene": "Benny shows his photo.", "speech": "This is my dad!"},
                {"scene": "Paws looks sad.", "speech": "I miss my mum cat!"},
                {"scene": "Everyone hugs Paws.", "speech": "We are your family too!"},
            ],
            "drawing_task": "Draw your family and Paws together!",
            "language_focus": "Family members",
        },
        8: {
            "title": "Rainbow's Fashion Show",
            "panels": [
                {"scene": "Rainbow wears a tiny hat.", "speech": "Look at my hat!"},
                {"scene": "Paws puts on shoes.", "speech": "Big shoes!"},
                {"scene": "Sunny wears a scarf.", "speech": "A pink scarf!"},
                {"scene": "They walk on the stage.", "speech": "Fashion show!"},
            ],
            "drawing_task": "Draw your dream outfit!",
            "language_focus": "Clothes",
        },
        9: {
            "title": "Rainy Day Fun",
            "panels": [
                {"scene": "Rain falls outside.", "speech": "It is rainy!"},
                {"scene": "Paws opens an umbrella.", "speech": "I have an umbrella!"},
                {"scene": "Benny jumps in a puddle.", "speech": "Splash! Splash!"},
                {"scene": "Sun comes out.", "speech": "Look! A rainbow!"},
            ],
            "drawing_task": "Draw a rainy day with a big rainbow!",
            "language_focus": "Weather",
        },
        10: {
            "title": "The Last Day",
            "panels": [
                {"scene": "Paws has a suitcase.", "speech": "Time to go!"},
                {"scene": "Sunny gives a card.", "speech": "This is for you!"},
                {"scene": "Everyone waves.", "speech": "Goodbye! See you!"},
                {"scene": "Rainbow flies in a circle.", "speech": "I will miss you!"},
            ],
            "drawing_task": "Draw a goodbye card for your best friend!",
            "language_focus": "Saying goodbye",
        },
    },
}

# ---------------------------------------------------------------------------
# MISSION BANK  (simple real-world tasks for little explorers)
# ---------------------------------------------------------------------------
MISSION_BANK = {
    0: {
        1: {
            "title": "Colour Hunt!",
            "mission": "Find 3 RED things at home. Show them to your family. Say: This is RED!",
            "evidence": "Draw or take a photo of the 3 red things.",
            "xp": 10,
            "difficulty": "Easy",
        },
        2: {
            "title": "Rainbow Spotter!",
            "mission": "Find something RED, BLUE, YELLOW and GREEN at school. Point and say the colour!",
            "evidence": "Draw the 4 things and colour them.",
            "xp": 15,
            "difficulty": "Easy",
        },
        3: {
            "title": "Number Walk!",
            "mission": "Walk around the classroom. Count to 10! Point and count things: 1 door, 2 windows, 3 chairs...",
            "evidence": "Draw 5 things you counted.",
            "xp": 15,
            "difficulty": "Easy",
        },
        4: {
            "title": "Animal Sounds!",
            "mission": "Make 5 animal sounds. Ask your family: What animal am I?",
            "evidence": "Draw the 5 animals and show your family.",
            "xp": 10,
            "difficulty": "Easy",
        },
        5: {
            "title": "Fruit Taster!",
            "mission": "Try a fruit today. Say: I like ___! Or say: I don't like ___!",
            "evidence": "Draw the fruit you tasted. Colour it!",
            "xp": 10,
            "difficulty": "Easy",
        },
        6: {
            "title": "Body Dance!",
            "mission": "Touch your head, shoulders, knees and toes. Say each body part! Do it fast!",
            "evidence": "Do it 3 times and get faster each time!",
            "xp": 10,
            "difficulty": "Easy",
        },
        7: {
            "title": "Family Portrait!",
            "mission": "Draw your family. Show it to someone and say: This is my mum. This is my dad.",
            "evidence": "Bring your family drawing to class!",
            "xp": 15,
            "difficulty": "Easy",
        },
        8: {
            "title": "Dress-Up Day!",
            "mission": "Choose your clothes tomorrow. Say: I am wearing a ___ shirt and ___ shoes.",
            "evidence": "Draw what you wore. Teacher takes a photo!",
            "xp": 10,
            "difficulty": "Easy",
        },
        9: {
            "title": "Weather Reporter!",
            "mission": "Look outside every morning for 3 days. Say: It is sunny / rainy / cloudy!",
            "evidence": "Draw 3 days of weather with smiley suns or rainy clouds.",
            "xp": 20,
            "difficulty": "Medium",
        },
        10: {
            "title": "Goodbye Card!",
            "mission": "Make a goodbye card for a friend. Draw a picture and say: Goodbye! I will miss you!",
            "evidence": "Give the card to your friend on the last day!",
            "xp": 20,
            "difficulty": "Easy",
        },
    },
}

# ---------------------------------------------------------------------------
# ESCAPE ROOM BANK  (treasure hunts with picture clues for preschool)
# ---------------------------------------------------------------------------
ESCAPE_ROOM_BANK = {
    0: {
        1: {
            "title": "Find the Rainbow Treasure!",
            "story": "Rainbow the parrot hid a treasure! Follow the colour clues to find it!",
            "puzzles": [
                {"type": "colour", "question": "What colour is the sky? Point to the BLUE crayon!", "answer": "BLUE", "hint": "Look up!"},
                {"type": "matching", "question": "Match: apple = RED, banana = YELLOW, grass = GREEN", "answer": "correct matching", "hint": "Think about real colours!"},
                {"type": "counting", "question": "How many fingers on one hand?", "answer": "5", "hint": "Count with me: 1, 2, 3..."},
            ],
            "final_code": "BLUE-YELLOW-5",
            "reward": "You found the treasure! A rainbow sticker!",
        },
        2: {
            "title": "The Lost Crayons!",
            "story": "Paws lost his crayons! Help him find them by solving colour puzzles!",
            "puzzles": [
                {"type": "colour", "question": "What colour is grass? Find the GREEN crayon!", "answer": "GREEN", "hint": "Grass is not blue!"},
                {"type": "colour", "question": "What colour is the sun?", "answer": "YELLOW", "hint": "The sun is bright and warm!"},
                {"type": "matching", "question": "Match: RED crayon → strawberry, ORANGE crayon → orange fruit", "answer": "correct matching", "hint": "Fruits have colours too!"},
            ],
            "final_code": "GREEN-YELLOW-RED",
            "reward": "You found all the crayons! A star sticker!",
        },
        3: {
            "title": "Benny's Number Adventure!",
            "story": "Benny hid toys in numbered boxes. Find the right boxes!",
            "puzzles": [
                {"type": "counting", "question": "Count the stars: ★★★. How many?", "answer": "3", "hint": "Point and count!"},
                {"type": "counting", "question": "Show me 7 fingers!", "answer": "7", "hint": "Use both hands!"},
                {"type": "matching", "question": "Match: 2 → two balls, 4 → four cats, 6 → six fish", "answer": "correct matching", "hint": "Count each group!"},
            ],
            "final_code": "3-7-6",
            "reward": "You opened all the boxes! A toy sticker!",
        },
        4: {
            "title": "The Animal Rescue!",
            "story": "Animals are lost! Make the right sounds to call them back!",
            "puzzles": [
                {"type": "sound", "question": "What animal says WOOF? Act it out!", "answer": "dog", "hint": "It has four legs and a tail!"},
                {"type": "matching", "question": "Match: meow → cat, quack → duck, moo → cow", "answer": "correct matching", "hint": "Think about farm animals!"},
                {"type": "colour", "question": "What colour is a frog?", "answer": "GREEN", "hint": "Frogs jump in the green grass!"},
            ],
            "final_code": "DOG-DUCK-GREEN",
            "reward": "All animals are home! An animal sticker!",
        },
        5: {
            "title": "Sunny's Fruit Basket!",
            "story": "Sunny needs to fill her fruit basket. Help her pick the right fruits!",
            "puzzles": [
                {"type": "colour", "question": "What colour is a banana?", "answer": "YELLOW", "hint": "Monkeys love this fruit!"},
                {"type": "counting", "question": "Sunny needs 4 apples. Count them into the basket!", "answer": "4", "hint": "One, two, three..."},
                {"type": "matching", "question": "Match: round → orange, long → banana, small → grape", "answer": "correct matching", "hint": "Think about the shape!"},
            ],
            "final_code": "YELLOW-4-GRAPE",
            "reward": "The basket is full! A fruit sticker!",
        },
        6: {
            "title": "The Body Puzzle!",
            "story": "A silly robot is broken! Put the body parts in the right place!",
            "puzzles": [
                {"type": "matching", "question": "Point to: HEAD on top, FEET at the bottom!", "answer": "correct order", "hint": "Your head is up high!"},
                {"type": "counting", "question": "How many ears do you have?", "answer": "2", "hint": "Touch them!"},
                {"type": "action", "question": "Clap your HANDS 5 times!", "answer": "5 claps", "hint": "Count each clap!"},
            ],
            "final_code": "HEAD-2-HANDS",
            "reward": "Robot is fixed! A robot sticker!",
        },
        7: {
            "title": "The Family Photo!",
            "story": "Miss Lily's family photo is mixed up! Help sort the family!",
            "puzzles": [
                {"type": "matching", "question": "Who is big? MUM and DAD. Who is small? BABY.", "answer": "correct sorting", "hint": "Babies are tiny!"},
                {"type": "counting", "question": "How many people in your family? Show with fingers!", "answer": "varies", "hint": "Count everyone!"},
                {"type": "action", "question": "Hug your friend and say: You are my friend!", "answer": "hug done", "hint": "Open your arms!"},
            ],
            "final_code": "FAMILY-LOVE",
            "reward": "The photo is perfect! A heart sticker!",
        },
        8: {
            "title": "The Clothes Closet!",
            "story": "Paws mixed up all the clothes! Sort them before school!",
            "puzzles": [
                {"type": "matching", "question": "Match: hat → head, shoes → feet, gloves → hands", "answer": "correct matching", "hint": "Where do you wear them?"},
                {"type": "colour", "question": "Find something BLUE that you wear.", "answer": "BLUE clothing item", "hint": "Look at your clothes!"},
                {"type": "action", "question": "Put on an imaginary hat and say: I have a hat!", "answer": "action done", "hint": "Pretend!"},
            ],
            "final_code": "HAT-BLUE-HAT",
            "reward": "All clothes are sorted! A shoe sticker!",
        },
        9: {
            "title": "The Weather Station!",
            "story": "Be a weather detective! Solve puzzles about the weather!",
            "puzzles": [
                {"type": "matching", "question": "Match: umbrella → rainy, sunglasses → sunny, coat → cold", "answer": "correct matching", "hint": "What do you wear?"},
                {"type": "action", "question": "Look outside! Is it sunny, rainy or cloudy? Tell everyone!", "answer": "weather report", "hint": "Look at the sky!"},
                {"type": "colour", "question": "Draw a sun. What colour is it?", "answer": "YELLOW", "hint": "Bright and warm!"},
            ],
            "final_code": "RAIN-SUN-YELLOW",
            "reward": "You are a weather expert! A sun sticker!",
        },
        10: {
            "title": "The Goodbye Party!",
            "story": "It's the last day! Solve the puzzles to start the goodbye party!",
            "puzzles": [
                {"type": "action", "question": "Say GOODBYE to 3 friends!", "answer": "3 goodbyes", "hint": "Wave and smile!"},
                {"type": "matching", "question": "Match: hello → start, goodbye → end, see you → next time", "answer": "correct matching", "hint": "We say goodbye at the end!"},
                {"type": "counting", "question": "How many friends are in your class? Count them!", "answer": "varies", "hint": "Point and count!"},
            ],
            "final_code": "BYE-END-FRIENDS",
            "reward": "Party time! Goodbye sticker and a big group hug!",
        },
    },
}

# ---------------------------------------------------------------------------
# FAMILY CORNER BANK  (parent-child play activities)
# ---------------------------------------------------------------------------
FAMILY_CORNER_BANK = {
    0: {
        1: {
            "title": "Colour Game at Home",
            "activity": "Point to things at home and say their colour in English. RED door! BLUE cup!",
            "together": "Play 'I Spy' with colours: I spy something RED!",
            "parent_question": "Dear parent, point to objects and ask: What colour is this?",
            "signature": True,
        },
        2: {
            "title": "Rainbow Walk",
            "activity": "Go for a walk. Find something for each colour: red, blue, yellow, green, orange!",
            "together": "Make a colour poster together with things you found!",
            "parent_question": "Dear parent, help your child name the colours they find.",
            "signature": True,
        },
        3: {
            "title": "Counting at Home",
            "activity": "Count things at home: 1 TV, 2 shoes, 3 cups, 4 spoons, 5 toys!",
            "together": "Play a counting race: who can count to 10 first?",
            "parent_question": "Dear parent, ask: How many ___ do we have?",
            "signature": True,
        },
        4: {
            "title": "Animal Charades",
            "activity": "Act like an animal. Can your family guess? Meow! Woof! Quack!",
            "together": "Take turns being animals. Say the animal name in English!",
            "parent_question": "Dear parent, play along and ask: What animal are you?",
            "signature": True,
        },
        5: {
            "title": "Kitchen English",
            "activity": "Help in the kitchen. Point to fruits and say: apple, banana, orange!",
            "together": "Make a fruit face on a plate together. Name each fruit!",
            "parent_question": "Dear parent, ask: What fruit is this? Do you like it?",
            "signature": True,
        },
        6: {
            "title": "Body Song Time",
            "activity": "Sing 'Head, Shoulders, Knees and Toes' with your family!",
            "together": "Draw around your hand. Label: fingers, thumb, hand!",
            "parent_question": "Dear parent, touch body parts and ask: What is this?",
            "signature": True,
        },
        7: {
            "title": "Family Tree Drawing",
            "activity": "Draw your family tree. Say: This is my mum. This is my dad.",
            "together": "Look at family photos and name everyone in English.",
            "parent_question": "Dear parent, help your child say: This is my ___.",
            "signature": True,
        },
        8: {
            "title": "Dress-Up Fashion Show",
            "activity": "Choose clothes and say: I am wearing a RED shirt!",
            "together": "Have a fashion show at home. Say the colour and the clothes!",
            "parent_question": "Dear parent, ask: What are you wearing? What colour is it?",
            "signature": True,
        },
        9: {
            "title": "Weather Diary",
            "activity": "Look outside with your family. Say: It is sunny / rainy / cloudy!",
            "together": "Draw today's weather together. Add a sun or clouds!",
            "parent_question": "Dear parent, ask each morning: What is the weather today?",
            "signature": True,
        },
        10: {
            "title": "Summer Fun Plan",
            "activity": "Talk about summer! Say: I like the beach! I like ice cream!",
            "together": "Draw a summer picture together. Write 'SUMMER' on it!",
            "parent_question": "Dear parent, ask: What do you want to do in summer?",
            "signature": True,
        },
    },
}

# ---------------------------------------------------------------------------
# SEL BANK  (Social-Emotional Learning – feelings through faces/drawing)
# ---------------------------------------------------------------------------
SEL_BANK = {
    0: {
        1: {
            "emotion": "Happy",
            "prompt": "Look at the smiley face. Are you happy today?",
            "activity": "Draw a happy face. Colour it yellow!",
            "mindfulness": "Smile as big as you can! Now give someone a high-five!",
            "discussion": "When do you feel happy? Show me your happy face!",
        },
        2: {
            "emotion": "Sad",
            "prompt": "Look at the sad face. Sometimes we feel sad. That's okay.",
            "activity": "Draw a sad face. Colour it blue.",
            "mindfulness": "Take a deep breath. Hug yourself. It's okay to be sad.",
            "discussion": "What makes you feel sad? What helps you feel better?",
        },
        3: {
            "emotion": "Excited",
            "prompt": "Jump up and down! Are you excited?",
            "activity": "Draw an excited face with a big open mouth! Colour it orange!",
            "mindfulness": "Jump 5 times! Shake your hands! Say: I am EXCITED!",
            "discussion": "What makes you excited? A birthday? A holiday?",
        },
        4: {
            "emotion": "Scared",
            "prompt": "Look at the scared face. Everyone feels scared sometimes.",
            "activity": "Draw a scared face. Draw what helps you feel safe (a teddy bear, mum).",
            "mindfulness": "Hold your teddy bear tight. Say: I am safe. I am brave!",
            "discussion": "What makes you scared? Who helps you feel brave?",
        },
        5: {
            "emotion": "Hungry",
            "prompt": "Is your tummy making noises? You might be hungry!",
            "activity": "Draw your favourite food. Colour it! Say: I am hungry! I want ___!",
            "mindfulness": "Rub your tummy. Say: Yummy! I like ___!",
            "discussion": "What is your favourite food? Do you like apples or bananas?",
        },
        6: {
            "emotion": "Tired",
            "prompt": "Are your eyes sleepy? Sometimes our body says: I am tired.",
            "activity": "Draw a sleepy face with closed eyes. Colour it purple.",
            "mindfulness": "Put your head on the desk. Close your eyes for 10 seconds. Rest...",
            "discussion": "When do you feel tired? What do you do when you are sleepy?",
        },
        7: {
            "emotion": "Loving",
            "prompt": "Do you love your family? Your friends? Love is a warm feeling!",
            "activity": "Draw a big red heart. Inside it, draw the people you love.",
            "mindfulness": "Hug yourself. Say: I love my family. I love my friends.",
            "discussion": "Who do you love? Show love with a hug or a smile!",
        },
        8: {
            "emotion": "Proud",
            "prompt": "You did something great! Feel proud! Say: I did it!",
            "activity": "Draw yourself with a big smile. Add a gold star!",
            "mindfulness": "Stand up tall. Put your hands on your hips. Say: I am PROUD!",
            "discussion": "What are you proud of? Tying your shoes? Drawing a picture?",
        },
        9: {
            "emotion": "Surprised",
            "prompt": "Open your eyes wide! Open your mouth! SURPRISE!",
            "activity": "Draw a surprised face with a big 'O' mouth!",
            "mindfulness": "Say: WOW! Play a surprise game: hide something and find it!",
            "discussion": "Do you like surprises? What was a nice surprise?",
        },
        10: {
            "emotion": "Thankful",
            "prompt": "What are you thankful for? Friends, family, sunshine, toys?",
            "activity": "Draw 3 things you are thankful for. Say: Thank you!",
            "mindfulness": "Close your eyes. Think of 3 good things. Smile and say: Thank you!",
            "discussion": "Say thank you to someone today! Who will you thank?",
        },
    },
}

# ---------------------------------------------------------------------------
# STEAM BANK  (simple Science / Technology / Engineering / Art / Maths)
# ---------------------------------------------------------------------------
STEAM_BANK = {
    0: {
        1: {
            "subject": "Art",
            "title": "Rainbow Painting",
            "task": "Mix RED and YELLOW paint. What colour do you get? ORANGE! Paint a rainbow!",
            "vocab": ["mix", "paint", "rainbow", "colour"],
        },
        2: {
            "subject": "Art",
            "title": "Colour Wheel",
            "task": "Mix BLUE and YELLOW. You get GREEN! Mix RED and BLUE. You get PURPLE! Make a colour wheel!",
            "vocab": ["mix", "blue", "yellow", "green", "purple"],
        },
        3: {
            "subject": "Maths",
            "title": "Shape Hunt",
            "task": "Find a CIRCLE (a clock!), a SQUARE (a window!), a TRIANGLE (a roof!). Draw them!",
            "vocab": ["circle", "square", "triangle", "shape"],
        },
        4: {
            "subject": "Science",
            "title": "Animal Babies",
            "task": "Match the animal mum and baby: cat → kitten, dog → puppy, hen → chick. Draw them!",
            "vocab": ["kitten", "puppy", "chick", "baby"],
        },
        5: {
            "subject": "Science",
            "title": "Sink or Float?",
            "task": "Put things in water: a stone, a leaf, a toy. Does it SINK or FLOAT? Draw it!",
            "vocab": ["sink", "float", "water", "heavy", "light"],
        },
        6: {
            "subject": "Art",
            "title": "Hand Print Animals",
            "task": "Dip your hand in paint. Press it on paper. Turn it into a BIRD, a FISH or a TREE!",
            "vocab": ["hand", "print", "paint", "press"],
        },
        7: {
            "subject": "Engineering",
            "title": "Build a House",
            "task": "Use blocks or boxes to build a HOUSE. How many blocks? Count them! Say: My house has ___ blocks!",
            "vocab": ["build", "house", "blocks", "tall", "strong"],
        },
        8: {
            "subject": "Art",
            "title": "Paper Plate Mask",
            "task": "Make a mask from a paper plate. Add EYES, NOSE, MOUTH. Colour your hat and hair!",
            "vocab": ["mask", "eyes", "nose", "mouth", "decorate"],
        },
        9: {
            "subject": "Science",
            "title": "Cloud Watching",
            "task": "Lie on the grass. Look at the clouds. What shape do you see? A rabbit? A car? Draw it!",
            "vocab": ["cloud", "sky", "shape", "fluffy", "white"],
        },
        10: {
            "subject": "Maths",
            "title": "Pattern Necklace",
            "task": "Make a necklace with beads: RED, BLUE, RED, BLUE. What comes next? Make your own pattern!",
            "vocab": ["pattern", "bead", "necklace", "next", "repeat"],
        },
    },
}

# ---------------------------------------------------------------------------
# PODCAST BANK  (sing-along audio episode plans for preschool)
# ---------------------------------------------------------------------------
PODCAST_BANK = {
    0: {
        1: {
            "title": "Episode 1: Hello Song!",
            "host": "Sunny & Paws",
            "summary": "Sunny and Paws sing the Hello Song and learn about colours.",
            "segments": ["Hello Song (0:00)", "Colour Chant (1:00)", "Animal Sound Game (2:00)", "Goodbye Song (3:00)"],
            "student_task": "Sing the Hello Song with your family!",
        },
        2: {
            "title": "Episode 2: Colour Party!",
            "host": "Sunny & Rainbow",
            "summary": "Rainbow teaches all the colours with a funny colour song.",
            "segments": ["Colour Song (0:00)", "I Spy Colours (1:00)", "Rainbow Chant (2:00)", "Bye Bye Song (3:00)"],
            "student_task": "Sing the Colour Song and point to colours!",
        },
        3: {
            "title": "Episode 3: Count With Me!",
            "host": "Benny & Paws",
            "summary": "Benny and Paws count from 1 to 10 with a counting song.",
            "segments": ["Counting Song 1-5 (0:00)", "Number Chant (1:00)", "Counting Song 6-10 (2:00)", "Clap and Count (3:00)"],
            "student_task": "Count to 10 with your fingers and sing along!",
        },
        4: {
            "title": "Episode 4: Animal Sounds!",
            "host": "Paws & Rainbow",
            "summary": "What does the cat say? The dog? The duck? Sing and make animal sounds!",
            "segments": ["Old MacDonald Song (0:00)", "Animal Guess Game (1:00)", "Sound Chant (2:00)", "Animal Dance (3:00)"],
            "student_task": "Make 5 animal sounds and act them out!",
        },
        5: {
            "title": "Episode 5: Yummy Fruits!",
            "host": "Sunny & Benny",
            "summary": "Sunny and Benny sing about their favourite fruits.",
            "segments": ["Fruit Song (0:00)", "I Like / I Don't Like (1:00)", "Fruit Chant (2:00)", "Yummy Dance (3:00)"],
            "student_task": "Tell your family your favourite fruit in English!",
        },
        6: {
            "title": "Episode 6: Head, Shoulders, Knees!",
            "host": "Miss Lily & Everyone",
            "summary": "Sing Head, Shoulders, Knees and Toes! Touch and learn body parts.",
            "segments": ["Body Song (0:00)", "Touch and Say (1:00)", "Fast Version! (2:00)", "Body Freeze Dance (3:00)"],
            "student_task": "Sing the Body Song 3 times – each time faster!",
        },
        7: {
            "title": "Episode 7: My Family!",
            "host": "Sunny & Paws",
            "summary": "Sunny talks about her family. Paws misses his cat family!",
            "segments": ["Family Song (0:00)", "Who Is This? (1:00)", "Family Chant (2:00)", "I Love You Song (3:00)"],
            "student_task": "Draw your family and sing the Family Song!",
        },
        8: {
            "title": "Episode 8: What Am I Wearing?",
            "host": "Rainbow & Benny",
            "summary": "Rainbow tries on funny clothes! Learn clothes words with a song.",
            "segments": ["Clothes Song (0:00)", "What Colour Shoes? (1:00)", "Dress-Up Chant (2:00)", "Fashion Parade (3:00)"],
            "student_task": "Tell someone what you are wearing in English!",
        },
        9: {
            "title": "Episode 9: Weather Dance!",
            "host": "Miss Lily & Everyone",
            "summary": "Is it sunny? Rainy? Cloudy? Sing and dance for each weather!",
            "segments": ["Weather Song (0:00)", "Sun Dance (1:00)", "Rain Dance (2:00)", "Snow Dance / Goodbye (3:00)"],
            "student_task": "Do the weather dance at home!",
        },
        10: {
            "title": "Episode 10: Goodbye Party!",
            "host": "Everyone",
            "summary": "The last episode! Everyone sings their favourite songs and says goodbye.",
            "segments": ["Best Songs Medley (0:00)", "Memory Song (1:00)", "Thank You Chant (2:00)", "Goodbye Forever Song (3:00)"],
            "student_task": "Sing the Goodbye Song to your family and friends!",
        },
    },
}
