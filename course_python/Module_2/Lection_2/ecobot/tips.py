import random

eco_tips = [
    "Bring a reusable bag when shopping 🛍️",
    "Use a reusable water bottle 💧",
    "Avoid plastic packaging whenever possible ♻️",
    "Plan your meals to reduce food waste 🍽️",
    "Repair items instead of throwing them away 🔧",
    "Use reusable containers for take-away food 🥡",
    "Separate your waste correctly 🚮"
]

def get_tip():
    return random.choice(eco_tips)
