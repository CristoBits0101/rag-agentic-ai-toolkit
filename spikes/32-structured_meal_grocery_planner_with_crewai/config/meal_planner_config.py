# --- DEPENDENCIAS ---
DEFAULT_INPUTS = {
    "meal_name": "Chicken Stir Fry",
    "servings": 4,
    "budget": "$25",
    "dietary_restrictions": ["no nuts", "low sodium"],
    "cooking_skill": "beginner",
}

RECIPE_CATALOG = {
    "chicken stir fry": {
        "difficulty_level": "Easy",
        "ingredients": [
            "chicken breast",
            "broccoli",
            "bell peppers",
            "garlic",
            "soy sauce",
            "rice",
        ],
        "shopping_items": [
            ("Chicken Breast", "2 lbs", "$8-10", "Meat"),
            ("Broccoli", "2 heads", "$3-4", "Produce"),
            ("Bell Peppers", "3 pieces", "$3-4", "Produce"),
            ("Garlic", "1 bulb", "$1-2", "Produce"),
            ("Low Sodium Soy Sauce", "1 bottle", "$3-4", "Pantry"),
            ("Rice", "1 bag", "$4-5", "Pantry"),
        ],
        "shopping_tips": [
            "Buy rice in a larger bag if you cook stir fry often.",
            "Use frozen broccoli if fresh prices are high.",
        ],
        "leftover_ideas": [
            "Use leftover chicken and vegetables in fried rice the next day.",
            "Turn leftover stir fry into lettuce wraps for lunch.",
        ],
    },
    "quinoa buddha bowl": {
        "difficulty_level": "Medium",
        "ingredients": [
            "quinoa",
            "chickpeas",
            "sweet potato",
            "spinach",
            "avocado",
            "tahini",
        ],
        "shopping_items": [
            ("Quinoa", "1 bag", "$5-7", "Pantry"),
            ("Chickpeas", "2 cans", "$3-4", "Pantry"),
            ("Sweet Potato", "2 lbs", "$3-4", "Produce"),
            ("Spinach", "1 box", "$3-4", "Produce"),
            ("Avocado", "2 pieces", "$3-5", "Produce"),
            ("Tahini", "1 jar", "$5-6", "Pantry"),
        ],
        "shopping_tips": [
            "Cook extra quinoa for lunches later in the week.",
            "Roast all vegetables in one batch to save oven time.",
        ],
        "leftover_ideas": [
            "Use leftover quinoa in a breakfast bowl with fruit.",
            "Blend extra tahini into a dressing for sandwiches.",
        ],
    },
}