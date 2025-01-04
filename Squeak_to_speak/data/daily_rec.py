import random

habit_changes = [
    "Sleep at least 8 hours every night",
    "Drink a glass of water first thing in the morning",
    "Take a 10-minute walk after meals",
    "Stretch for 5 minutes every morning",
    "Replace one sugary drink with water daily",
    "Eat one extra serving of fruits or vegetables daily",
    "Practice mindful eating by chewing slowly",
    "Limit screen time before bed",
    "Try a breathing exercise for 2 minutes daily",
    "Stand up and stretch every hour if sitting for long periods",
    "Do 10 push-ups or squats every morning",
    "Take the stairs instead of the elevator",
    "Park farther away to get extra steps in",
    "Practice yoga or light stretching weekly",
    "Replace 10 minutes of sitting with light physical activity",
    "Write down your top three priorities for the day",
    "Set a timer for 25 minutes and focus on one task (Pomodoro technique)",
    "Check emails at designated times instead of constantly",
    "Keep a clean desk to improve focus",
    "Plan your day the night before",
    "Write down one thing you're grateful for each day",
    "Take 5 deep breaths when feeling stressed",
    "Spend 10 minutes journaling about your thoughts or goals",
    "Replace negative self-talk with affirmations",
    "Spend 10 minutes daily in silence or meditation",
    "Read 10 pages of a book daily",
    "Listen to an educational podcast while commuting",
    "Learn one new word every day",
    "Practice a foreign language for 5 minutes daily",
    "Watch one video or tutorial to learn a new skill weekly",
    "Send a kind message to someone you care about weekly",
    "Schedule a weekly call with a friend or family member",
    "Practice active listening in conversations",
    "Compliment someone sincerely every day",
    "Dedicate 15 minutes daily to spending time with loved ones",
    "Track one expense daily",
    "Save spare change or small amounts daily",
    "Avoid unnecessary online shopping by waiting 24 hours before purchase",
    "Cancel unused subscriptions",
    "Plan meals to save money and reduce waste",
    "Make your bed every morning",
    "Declutter one small area weekly",
    "Create a to-do list to prioritize tasks",
    "Turn off lights and unplug devices when not in use",
    "Set out your clothes the night before",
    "Spend 10 minutes daily on a creative hobby like drawing or writing",
    "Try a new recipe weekly",
    "Take a photo of something beautiful daily",
    "Play a musical instrument for a few minutes",
    "Practice a new skill or craft weekly"
]


def select_random_habits(habits=habit_changes, n=5):
    return random.sample(habits, n)




