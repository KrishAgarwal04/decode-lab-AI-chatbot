"""
Project 1: Rule-Based AI Chatbot (Upgraded Version)
Goal: A rule-based chatbot that responds to predefined user inputs,
with smarter keyword matching, varied responses, and basic personalization.
"""

import random
import re

# ---------------------------------------------------------
# Rule Book: keywords -> list of possible responses
# Using lists lets the bot pick a random reply so it feels
# less robotic and repetitive.
# ---------------------------------------------------------
RULES = {
    ("hi", "hello", "hey", "hii", "yo", "wassup"): [
        "Hello! How can I help you today?",
        "Hey there! What's up?",
        "Hi! Good to see you."],
        
    ("how are you", "how r u", "hows it going"): [
        "I'm just code, but I'm doing great! How about you?",
        "Running smoothly! How are you doing?"
    ],
    ("your name", "who are you", "what is your name"): [
        "I'm RuleBot, your friendly rule-based chatbot!",
        "You can call me RuleBot."
    ],
    ("what can you do", "help", "commands"): [
        "I can chat with you, remember your name, and answer a few basic questions. Try asking 'what is your name' or just say 'bye' to leave.",
    ],
    ("who created you", "who made you", "your creator"): [
        "I was built as part of a simple Python chatbot project.",
    ],
    ("thanks", "thank you", "thx"): [
        "You're welcome!",
        "Anytime, happy to help!"
    ],
    ("joke", "make me laugh", "funny"): [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer a joke... no response, it just froze."
    ],
    ("bye", "exit", "quit", "goodbye", "see you"): ["EXIT"],
}

EXIT_KEYWORDS = {"bye", "exit", "quit", "goodbye", "see you"}


def find_response(user_input, user_name=None):
    """
    Matches user input against keywords (substring match, not exact),
    so phrases like 'hey there' or 'what can you do for me' still work.
    Returns a response string, or 'EXIT' if the user wants to leave.
    """
    text = user_input.lower().strip()

    if not text:
        return "Say something! I'm listening."

    # Capture the user's name if they introduce themselves
    if "my name is" in text or "i am " in text or "i'm " in text:
        name = extract_name(text)
        if name:
            return f"Nice to meet you, {name.title()}! I'll remember that."

    # Use user's name in the response if we know it
    for keywords, responses in RULES.items():
        for keyword in keywords:
            # Word-boundary match avoids false positives like "yo" inside "you"
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                if responses == ["EXIT"]:
                    return "EXIT"
                response = random.choice(responses)
                if user_name and keyword in ("hi", "hello", "hey"):
                    response = f"{response} Nice to see you again, {user_name.title()}!"
                return response

    # Fallback for anything unrecognized
    return random.choice([
        "Sorry, I didn't understand that. Could you rephrase?",
        "Hmm, I'm not sure I follow. Try asking something else!",
        "I don't have a rule for that yet. Try 'help' to see what I can do."
    ])


def extract_name(text):
    """Very simple name extraction for phrases like 'my name is X' or 'i am X'."""
    for phrase in ["my name is", "i am ", "i'm "]:
        if phrase in text:
            name = text.split(phrase, 1)[1].strip()
            name = name.split()[0] if name else None
            return name
    return None


def run_chatbot():
    """Runs the chatbot in a continuous loop until the user exits."""
    print("=" * 55)
    print("RuleBot: Hi! I'm a rule-based chatbot.")
    print("RuleBot: Tell me your name, ask me something, or type 'bye' to leave.")
    print("=" * 55)

    user_name = None

    while True:
        user_input = input("You: ")
        text_lower = user_input.lower().strip()

        # Check for exit first
        if any(word in text_lower for word in EXIT_KEYWORDS):
            farewell = f"Goodbye, {user_name.title()}! Have a great day. 👋" if user_name else "Goodbye! Have a great day. 👋"
            print(f"RuleBot: {farewell}")
            break

        # Try to capture name
        name = extract_name(text_lower)
        if name and not user_name:
            user_name = name

        response = find_response(user_input, user_name)
        print(f"RuleBot: {response}")


if __name__ == "__main__":
    run_chatbot()
