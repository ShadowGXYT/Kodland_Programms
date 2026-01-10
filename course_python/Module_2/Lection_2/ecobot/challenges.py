import random

eco_challenges = [
    "Avoid single-use plastic today ♻️",
    "Drink only from a reusable bottle today 💧",
    "Buy at least one product without packaging 🥕",
    "Throw away zero food today 🍎",
    "Reuse something instead of buying new 🔁",
    "Use public transport, bike, or walk today 🚶‍♂️",
    "Sort all your waste correctly today 🚮"
]

def get_challenge():
    return random.choice(eco_challenges)
