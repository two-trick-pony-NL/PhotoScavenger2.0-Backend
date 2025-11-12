<img src="https://user-images.githubusercontent.com/71013416/183674037-eca7cc9b-4a19-494c-a449-af638fdd869c.png" width="250">

# Photo Scavenger Backend 2.0

This is the backend supporting **PhotoScavenger 2.0**, a multiplayer photo challenge game for iOS and Android.  
It handles object detection in user photos and serves real-time game events for multiplayer rounds.

**Project page:** [https://photoscavenger.petervandoorn.com](https://photoscavenger.petervandoorn.com)

---



**Version:** v2

---

# PhotoScavenger API

PhotoScavenger is a real-time multiplayer photo game backend built with **FastAPI**, **WebSockets**, and **Redis**. Players connect via WebSockets, participate in rounds, and compete on the leaderboard in real time.

---

## Features

- Real-time gameplay using WebSockets
- Redis pub/sub for event broadcasting
- Round countdown and emoji-based challenges
- Leaderboard tracking
- Simple REST API for health checks and future extensions

---

## Requirements

- Python 3.10+
- Redis server
- `pip` for Python dependencies

---

## Installation

1. Clone the repository:

```
git clone <repo-url>
cd PhotoScavenger
``` 

2. Create a virtual environment and install dependencies:

```
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3. Create a .env file with the Redis URL:

`REDIS_URL=redis://localhost:6379/0`

4. Running the Server

Start the FastAPI server with Uvicorn:

`uvicorn main:app --host 0.0.0.0 --port 8000`


Health check: GET / or GET /healthcheck

WebSocket endpoint: ws://localhost:8000/ws

## WebSocket Usage

Clients connect to /ws to participate in the game.

Receive full game state: On connection, clients get the current round status, leaderboard, and emojis.

Real-time updates: Game events and countdowns are broadcast via Redis pub/sub.

Example message structure:
```
{
  "type": "full_state",
  "time_remaining": 45,
  "status": "running",
  "leaderboard": [
    {"name": "Alice", "points": 10},
    {"name": "Bob", "points": 7}
  ],
  "emojis": [
    {"emoji": "📷", "locked_by": null},
    {"emoji": "🖼️", "locked_by": "Alice"}
  ]
}
```

## Project Structure
PhotoScavenger/
├─ main.py                # FastAPI app & startup logic
├─ api/
│  └─ endpoints.py        # REST API routes
├─ game/
│  ├─ countdown.py        # Broadcast round countdown
│  ├─ state.py            # Game state & leaderboard
│  └─ events.py           # Redis integration & analytics
├─ websocket/
│  └─ handler.py          # WebSocket connection handling
├─ requirements.txt
└─ .env

## Environment Variables
Variable	Default	Description
REDIS_URL	redis://localhost:6379/0	Redis connection URL


## Supported classes: 

```

# EMOJI_TO_CLASS = {
#     "🧍🏻‍♂️": "Person",
#     "👟": "Sneakers",
#     "🪑": "Chair",
#     "👞": "Other Shoes",
#     "🧢": "Hat",
#     #"🚗": "Car",
#     "💡": "Lamp",
#     "👓": "Glasses",
#     "🍾": "Bottle",
#     "☕️": "Cup",
#     #"🚦": "Street Lights",
#     "🗄️": "Cabinet/shelf",
#     "👜": "Handbag/Satchel",
#     "📿": "Bracelet",
#     "🍽️": "Plate",
#     "🖼️": "Picture/Frame",
#     "⛑️": "Helmet",
#     "📚": "Book",
#     "🧤": "Gloves",
#     "📦": "Storage box",
#     #"⛵": "Boat",
#     "👞": "Leather Shoes",
#     "🌻": "Flower",
#     "🪴": "Potted Plant",
#     "🥣": "Bowl/Basin",
#     "🚩": "Flag",
#     "🛌": "Pillow",
#     "🥾": "Boots",
#     "🏺": "Vase",
#     #"🎤": "Microphone",
#     "📿": "Necklace",
#     "💍": "Ring",
#     "🍷": "Wine Glass",
#     "📺": "Monitor/TV",
#     "🎒": "Backpack",
#     "☂️": "Umbrella",
#     #"🚥": "Traffic Light",
#     "🔊": "Speaker",
#     "⌚": "Watch",
#     "👔": "Tie",
#     "🗑️": "Trash bin Can",
#     "🩴": "Slippers",
#     #"🚲": "Bicycle",
#     "🪑": "Stool",
#     "🪣": "Barrel/bucket",
#     "🚐": "Van",
#     "🛋️": "Couch",
#     "🩴": "Sandals",
#     "🧺": "Basket",
#     "🛢️": "Drum",
#     "✏️": "Pen/Pencil",
#     #"🚌": "Bus",
#     #"🐦‍⬛": "Wild Bird",
#     "👠": "High Heels",
#     #"🏍️": "Motorcycle",
#     "🎸": "Guitar",
#     "📱": "Cell Phone",
#     "🍞": "Bread",
#     "📷": "Camera",
#     "🥫": "Canned",
#     #"🚛": "Truck",
#     #"🛟": "Lifesaver",
#     "🧻": "Towel",
#     "🧸": "Stuffed Toy",
#     "🕯️": "Candle",
#     #"⛵": "Sailboat",
#     "💻": "Laptop",
#     "🛏️": "Bed",
#     "🚰": "Faucet",
#     #"⛺": "Tent",
#     #"🐴": "Horse",
#     "🪞": "Mirror",
#     "🔌": "Power outlet",
#     "🚿": "Sink",
#     "🍎": "Apple",
#     "🔪": "Knife",
#     #"🏒": "Hockey Stick",
#     #"🛻": "Pickup Truck",
#     "🍴": "Fork",
#     #"🚸": "Traffic Sign",
#     "🎈": "Balloon",
#     #"📷": "Tripod",
#     "🐶": "Dog",
#     "🥄": "Spoon",
#     "🕰️": "Clock",
#     "🫖": "Pot",
#     "🐄": "Cow",
#     "🍰": "Cake",
#     "🐑": "Sheep",
#     "🧻": "Napkin",
#     "🐟": "Other Fish",
#     "🍊": "Orange/Tangerine",
#     "🧴": "Toiletry",
#     "⌨️": "Keyboard",
#     "🍅": "Tomato",
#     "🏮": "Lantern",
#     #"🚜": "Machinery Vehicle",
#     "🥦": "Green Vegetables",
#     "🍌": "Banana",
#     #"✈️": "Airplane",
#     #"🚆": "Train",
#     "🎃": "Pumpkin",
#     "⚽": "Soccer",
#     #"🎿": "Skiboard",
#     "🧳": "Luggage",
#     "🫖": "Tea pot",
#     "☎️": "Telephone",
#     "🛒": "Trolley",
#     "🎧": "Head Phone",
#    # "🏎️": "Sports Car",
#    # "🛑": "Stop Sign",
#     "🍮": "Dessert",
#     #"🛴": "Scooter",
#     #"🏗️": "Crane",
#     "🍋": "Lemon",
#     #"🦆": "Duck",
#     "🐱": "Cat",
#     "🍶": "Jug",
#     "🥦": "Broccoli",
#     "🎹": "Piano",
#     "🍕": "Pizza",
#     #"🐘": "Elephant",
#     "🛹": "Skateboard",
#     #"🏄": "Surfboard",
#     #"⛸️": "Skating and Skiing shoes",
#     "🍩": "Donut",
#     "🥕": "Carrot",
#     "🚽": "Toilet",
#     #"🪁": "Kite",
#     "🍓": "Strawberry",
#     "⚽": "Other Balls",
#     "🪏": "Shovel",
#     "🌶️": "Pepper",
#     "🧻": "Toilet Paper",
#     "🧼": "Cleaning Products",
#     "🥢": "Chopsticks",
#     #"🕊️": "Pigeon",
#     "⚾": "Baseball",
#     "🔪": "Cutting/chopping Board",
#     "✂️": "Scissors",
#     "🖊️": "Marker",
#     "🥧": "Pie",
#     "🪜": "Ladder",
#     #"🏂": "Snowboard",
#     "🍪": "Cookies",
#     "🏀": "Basketball",
#     #"🦓": "Zebra",
#     "🍇": "Grape",
#     #"🦒": "Giraffe",
#     "🥔": "Potato",
#     "🌭": "Sausage",
#     #"🚲": "Tricycle",
#     "🎻": "Violin",
#     "🥚": "Egg",
#     "🧯": "Fire Extinguisher",
#     "🍬": "Candy",
#     #"🚒": "Fire Truck",
#     #"🎱": "Billiards",
#     "🛁": "Bathtub",
#     #"🏌️": "Golf Club",
#     "💼": "Briefcase",
#     "🥒": "Cucumber",
#     "🚬": "Cigar/Cigarette",
#     "🧑🏻‍🎨": "Paint Brush",
#     "🍐": "Pear",
#     #"🚚": "Heavy Truck",
#     "🍔": "Hamburger",
#     "🔌": "Extension Cord",
#     #"🏈": "American Football",
#     "🎧": "earphone",
#     "🫖": "Kettle",
#     "🎾": "Tennis",
#     #"🚢": "Ship",
#     "☕️": "Coffee Machine",
#     "🛝": "Slide",
#     "🧅": "Onion",
#     "🫛": "Green beans",
#     #"📽️": "Projector",
#     #"🥏": "Frisbee",
#     "🧺": "Washing Machine/Drying Machine",
#     #"🐔": "Chicken",
#     "🖨️": "Printer",
#     "🍉": "Watermelon",
#     "🎷": "Saxophone",
#     "🧻": "Tissue",
#     "🪥": "Toothbrush",
#     "🍦": "Ice cream",
#     "🎻": "Cello",
#     "🍟": "French Fries",
#     "⚖️": "Scale",
#     "🏆": "Trophy",
#     "🥬": "Cabbage",
#     "🌭": "Hot dog",
#     "🍑": "Peach",
#     "🍚": "Rice",
#     "👛": "Wallet/Purse",
#     #"🏐": "Volleyball",
#     #"🦌": "Deer",
#     #"🦢": "Goose",
#     "🎺": "Trumpet",
#     "🍍": "Pineapple",
#     #"🏌️‍♂️": "Golf Ball",
#     #"🚑": "Ambulance",
#     "🥭": "Mango",
#     "🗝️": "Key",
#     "🎣": "Fishing Rod",
#     "🥇": "Medal",
#     #"🐧": "Penguin",
#     "📣": "Megaphone",
#     "🌽": "Corn",
#     "🥗": "Lettuce",
#     "🧄": "Garlic",
#     "🦢": "Swan",
#     #"🚁": "Helicopter",
#     "🧅": "Green Onion",
#     "🥪": "Sandwich",
#     "🥜": "Nuts",
#     "🍳": "Induction Cooker",
#     "🧹": "Broom",
#     #"🎺": "Trombone",
#     "🐠": "Goldfish",
#     "🥝": "Kiwi fruit",
#     "🃏": "Poker Card",
#     "🦐": "Shrimp",
#     "🍣": "Sushi",
#     "🧀": "Cheese",
#     "📄": "Notepaper",
#     "🍒": "Cherry",
#     "💿": "CD",
#     "🍝": "Pasta",
#     "🔨": "Hammer",
#     "🎱": "Cue",
#     "🥑": "Avocado",
#     "🍄": "Mushroom",
#     "🪛": "Screwdriver",
#     "🧼": "Soap",
#     #"🐻": "Bear",
#     "🍆": "Eggplant",
#     "🧽": "Board Eraser",
#     "🥥": "Coconut",
#     "📏": "Tape Measure/Ruler",
#     #"🐖": "Pig",
#     "🚿": "Showerhead",
#     "🌍": "Globe",
#     "🍟": "Chips",
#     "🥩": "Steak",
#     #"🚸": "Crosswalk Sign",
#     "🐫": "Camel",
#     #"🏎️": "Formula 1",
#     "🍽️": "Dishwasher",
#     #"🦀": "Crab",
#     "🐬": "Dolphin",
#     "🥧": "Egg tart",
#     "🔥": "Lighter",
#     "🍊": "Grapefruit",
#     "🎲": "Game board",
#     #"🐒": "Monkey",
#     "🐇": "Rabbit",
#     "✏️": "Pencil Case",
#     "🪮": "Comb",
#     "🥟": "Dumpling",
#     "🦪": "Oyster",
#     "🏓": "Table Tennis paddle",
#     "💄": "Cosmetics Brush/Eyeliner Pencil",
#     "🩹": "Eraser",
#     }
```