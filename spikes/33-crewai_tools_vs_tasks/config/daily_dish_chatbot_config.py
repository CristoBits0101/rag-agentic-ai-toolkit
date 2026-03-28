# --- DEPENDENCIAS ---
DEFAULT_CUSTOMER_QUERY = "What are your timings?"
SUPPLEMENTARY_QUERY = "Where are you located and is there parking nearby?"
DEFAULT_TEXT_MODEL = "qwen2.5:7b"

FAQ_ENTRIES = [
    {
        "question": "What are your timings?",
        "answer": "The Daily Dish is open Monday through Thursday from 11:00 AM to 9:00 PM and Friday through Sunday from 10:00 AM to 10:00 PM.",
        "keywords": ["timings", "hours", "open", "closing", "weekend"],
    },
    {
        "question": "What is your phone number?",
        "answer": "You can reach The Daily Dish team at 555 0147 for reservations and special requests.",
        "keywords": ["phone", "number", "call", "reservation", "contact"],
    },
    {
        "question": "Where are you located?",
        "answer": "The Daily Dish is located at 145 Market Street in downtown Austin next to Republic Square.",
        "keywords": ["location", "address", "located", "where", "downtown"],
    },
    {
        "question": "Do you take reservations?",
        "answer": "Yes. We accept reservations for lunch and dinner through phone bookings and our website form.",
        "keywords": ["reservation", "book", "table", "booking"],
    },
    {
        "question": "Do you have vegan options?",
        "answer": "Yes. We offer a rotating vegan bowl a mushroom flatbread and several vegetable sides.",
        "keywords": ["vegan", "vegetarian", "dietary", "options"],
    },
]

WEB_SNIPPETS = [
    {
        "title": "Parking overview",
        "answer": "There is a public parking garage on 3rd Street two minutes away and limited street parking after 6 PM.",
        "keywords": ["parking", "garage", "street", "nearby"],
    },
    {
        "title": "Transit directions",
        "answer": "The nearest light rail stop is Republic Square Station and the restaurant is a five minute walk from there.",
        "keywords": ["transit", "directions", "station", "walk", "map"],
    },
    {
        "title": "Reservation website note",
        "answer": "Online reservations are available until 30 minutes before service through the Daily Dish booking page.",
        "keywords": ["website", "online", "reservation", "booking"],
    },
]

CALCULATOR_PROMPTS = {
    "addition": "please add 4 5 and 6",
    "multiplication": "multiply 7 and 8 also 9 and 10",
}