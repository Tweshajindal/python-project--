import re
import random
from datetime import datetime

# ── NLP Helpers ───────────────────────────────────────────────────────────────

def normalize(text):
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text):
    """Split normalized text into word tokens."""
    return normalize(text).split()


def keyword_match(tokens, keywords):
    """Return True if any keyword (or phrase) matches the token list."""
    joined = " ".join(tokens)
    for kw in keywords:
        if kw in joined:
            return True
    return False


def extract_name(text):
    """Try to pull a name after 'my name is' / 'i am' / 'call me'."""
    patterns = [
        r"my name is ([a-zA-Z]+)",
        r"i am ([a-zA-Z]+)",
        r"call me ([a-zA-Z]+)",
        r"i'm ([a-zA-Z]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).capitalize()
    return None


def get_sentiment(tokens):
    """Detect basic sentiment from tokens."""
    positive = {"good", "great", "happy", "awesome", "fantastic",
                "excellent", "wonderful", "fine", "nice", "amazing"}
    negative = {"bad", "sad", "terrible", "awful", "horrible",
                "depressed", "angry", "upset", "frustrated", "stressed"}
    if any(t in positive for t in tokens):
        return "positive"
    if any(t in negative for t in tokens):
        return "negative"
    return "neutral"


# ── Response Rules ────────────────────────────────────────────────────────────

RULES = [
    {
        "keywords": ["hello", "hi", "hey", "howdy", "greetings", "good morning",
                     "good afternoon", "good evening"],
        "responses": [
            "Hey there! How can I help you today?",
            "Hello! Great to see you. What's on your mind?",
            "Hi! I'm here and ready to chat.",
        ],
        "tag": "greeting"
    },
    {
        "keywords": ["bye", "goodbye", "see you", "take care", "quit", "exit",
                     "later", "farewell"],
        "responses": [
            "Goodbye! Have a wonderful day!",
            "See you later! Take care.",
            "Bye! It was nice chatting with you.",
        ],
        "tag": "farewell"
    },
    {
        "keywords": ["how are you", "how do you do", "how are things",
                     "whats up", "what's up", "hows it going"],
        "responses": [
            "I'm doing great, thanks for asking! How about you?",
            "All systems running smoothly! How are you doing?",
            "Feeling chatty and helpful! What about you?",
        ],
        "tag": "how_are_you"
    },
    {
        "keywords": ["your name", "who are you", "what are you",
                     "introduce yourself", "what should i call you"],
        "responses": [
            "I'm Aria, your rule-based chatbot assistant!",
            "They call me Aria — here to chat and help!",
            "My name is Aria. Nice to meet you!",
        ],
        "tag": "identity"
    },
    {
        "keywords": ["help", "support", "assist", "what can you do",
                     "features", "capabilities"],
        "responses": [
            "I can chat, answer questions, tell jokes, share the time/date, and more. Just ask!",
            "I'm here to help! Try asking me for a joke, the time, or just have a conversation.",
        ],
        "tag": "help"
    },
    {
        "keywords": ["time", "what time", "current time", "clock"],
        "responses": ["__TIME__"],
        "tag": "time"
    },
    {
        "keywords": ["date", "today", "what day", "current date"],
        "responses": ["__DATE__"],
        "tag": "date"
    },
    {
        "keywords": ["joke", "funny", "make me laugh", "tell me a joke"],
        "responses": ["__JOKE__"],
        "tag": "joke"
    },
    {
        "keywords": ["weather", "temperature", "forecast", "raining", "sunny"],
        "responses": [
            "I can't check live weather yet, but I hope it's sunny where you are!",
            "I don't have internet access, but try weather.com for a forecast.",
        ],
        "tag": "weather"
    },
    {
        "keywords": ["age", "how old are you", "when were you born", "your age"],
        "responses": [
            "I was born the moment someone ran this Python script!",
            "Age is just a variable — mine is always 0 at startup.",
        ],
        "tag": "age"
    },
    {
        "keywords": ["python", "programming", "code", "coding", "developer",
                     "software", "program"],
        "responses": [
            "Python is awesome! This chatbot is built entirely with Python.",
            "I love Python — clean syntax, powerful libraries, and fun to write!",
            "Coding is a superpower. Python makes it even better!",
        ],
        "tag": "python"
    },
    {
        "keywords": ["thanks", "thank you", "appreciate", "cheers", "helpful"],
        "responses": [
            "You're welcome! Happy to help.",
            "Glad I could assist!",
            "Anytime! That's what I'm here for.",
        ],
        "tag": "thanks"
    },
    {
        "keywords": ["sorry", "apologize", "my bad", "oops", "mistake"],
        "responses": [
            "No worries at all! How can I help?",
            "No problem! Let's keep going.",
        ],
        "tag": "apology"
    },
    {
        "keywords": ["favorite color", "favourite color", "like color"],
        "responses": [
            "I'd say blue — calm, clear, and like a perfect sky.",
            "Green! Like a well-commented block of code.",
        ],
        "tag": "color"
    },
    {
        "keywords": ["favorite food", "favourite food", "eat", "hungry", "food"],
        "responses": [
            "I don't eat, but if I could, I'd pick pizza every time.",
            "Bots don't eat — but I hear coffee fuels most programmers!",
        ],
        "tag": "food"
    },
    {
        "keywords": ["meaning of life", "purpose", "why are we here", "42"],
        "responses": [
            "42. (If you know, you know.)",
            "To learn, to grow, and to occasionally debug Python at 2 AM.",
        ],
        "tag": "philosophy"
    },
]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
    "Why was the math book sad? It had too many problems.",
    "A SQL query walks into a bar, approaches two tables and asks... 'Can I JOIN you?'",
    "Why do Python programmers wear glasses? Because they can't C#!",
    "How do you comfort a JavaScript bug? You console it.",
    "Why did the developer go broke? Because he used up all his cache.",
]

FALLBACK = [
    "Hmm, I'm not sure about that. Try asking me something else!",
    "I didn't quite catch that. Can you rephrase?",
    "Interesting! But I don't have a response for that yet.",
    "I'm still learning! Could you ask me something different?",
    "That's beyond my current rules. Try asking about time, jokes, or coding!",
]


# ── Response Engine ───────────────────────────────────────────────────────────

def get_response(user_input, context):
    """Match user input against rules and return an appropriate response."""
    tokens = tokenize(user_input)

    # Name detection
    name = extract_name(user_input)
    if name:
        context["name"] = name
        return f"Nice to meet you, {name}! How can I help you today?"

    # Feeling / mood detection
    if keyword_match(tokens, ["i feel", "feeling", "im feeling", "i am feeling"]):
        sentiment = get_sentiment(tokens)
        if sentiment == "positive":
            return random.choice([
                "That's great to hear! Keep that energy up!",
                "Awesome! Positivity is contagious.",
            ])
        elif sentiment == "negative":
            name_str = f", {context['name']}" if context.get("name") else ""
            return random.choice([
                f"I'm sorry to hear that{name_str}. I hope things get better soon.",
                "That sounds tough. I'm here if you want to talk.",
            ])

    # Rule matching
    for rule in RULES:
        if keyword_match(tokens, rule["keywords"]):
            response = random.choice(rule["responses"])

            # Dynamic placeholders
            if response == "__TIME__":
                return f"The current time is {datetime.now().strftime('%I:%M %p')}."
            if response == "__DATE__":
                return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
            if response == "__JOKE__":
                return random.choice(JOKES)

            # Personalise greeting with name if known
            if rule["tag"] == "greeting" and context.get("name"):
                return f"Hey {context['name']}! {response}"

            return response

    # Fallback
    return random.choice(FALLBACK)


# ── Chat Loop ─────────────────────────────────────────────────────────────────

def chat():
    print("=" * 52)
    print("          Aria — Rule-Based Chatbot")
    print("=" * 52)
    print("  Type 'bye' or 'quit' to exit.\n")

    context = {}   # stores session data like user's name

    while True:
        try:
            user_input = input("  You  : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Aria : Goodbye! Take care.")
            break

        if not user_input:
            print("  Aria : Say something — I'm all ears!\n")
            continue

        tokens = tokenize(user_input)

        # Exit condition
        if keyword_match(tokens, ["bye", "goodbye", "quit", "exit",
                                   "see you", "take care"]):
            name_str = f", {context['name']}" if context.get("name") else ""
            print(f"  Aria : Goodbye{name_str}! Have a great day!\n")
            break

        response = get_response(user_input, context)
        print(f"  Aria : {response}\n")


if __name__ == "__main__":
    chat()