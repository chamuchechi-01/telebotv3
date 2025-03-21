import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")  # Make sure this matches the variable name in Railway
bot = telebot.TeleBot(TOKEN)

levels = ["Elementary 1", "Elementary 2", "Pre-Intermediate", "Intermediate"]
grades = [f"Grade {i}" for i in range(5, 12)]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

fixed_schedules = {
    "Elementary 1": {
        "Monday": ["English", "Math", "Japanese"],
        "Tuesday": ["Math", "Japanese", "English"],
        "Wednesday": ["Japanese", "English", "Math"],
        "Thursday": ["Math", "Japanese", "English"],
        "Friday": ["Japanese", "English", "Dotoku"]
    },
    "Elementary 2": {
        "Monday": ["Japanese", "Math", "English"],
        "Tuesday": ["English", "Math", "Dotoku"],
        "Wednesday": ["English", "Math", "Dotoku"],
        "Thursday": ["Japanese", "Math", "English"],
        "Friday": ["Math", "Japanese", "English"]
    },
    "Pre-Intermediate": {
        "Monday": ["Math", "Japanese", "English"],
        "Tuesday": ["Japanese", "English", "Math"],
        "Wednesday": ["Math", "English", "Dotoku"],
        "Thursday": ["Japanese", "English", "Math"],
        "Friday": ["Japanese", "English", "English"]
    },
    "Intermediate": {
        "Monday": ["Japanese", "Math", "English", "English"],
        "Tuesday": ["English", "Math", "English", "English"],
        "Wednesday": ["Japanese", "Math", "English", "English"],
        "Thursday": ["English", "Math", "English", "English"],
        "Friday": ["English", "English", "Japanese", "Japanese"]
    },
    "Grade 5": {
        "Monday": ["IT", "Russian", "Robotics", "Uzbek"],
        "Tuesday": ["Math", "Science", "Russian", "History"],
        "Wednesday": ["Science", "Bushido", "PE", "PE"],
        "Thursday": ["Math", "Geography", "Literature", "History"],
        "Friday": ["Bushido", "Robotics", "PE", "PE"]
    },
    "Grade 6": {
        "Monday": ["Russian", "History", "Uzbek", "IT"],
        "Tuesday": ["Robotics", "Math", "Bushido", "Science"],
        "Wednesday": ["Bushido", "Science", "PE", "PE"],
        "Thursday": ["Geography", "Math", "Uzbek", "Robotics"],
        "Friday": ["Class", "History", "PE", "PE"]
    },
    "Grade 7": {
        "Monday": ["Uzbek", "IT", "PE", "PE"],
        "Tuesday": ["Literature", "Bushido", "Biology", "Robotics"],
        "Wednesday": ["Russian", "Math", "Chemistry", "History"],
        "Thursday": ["History", "Russian", "Geography", "Uzbek"],
        "Friday": ["Russian", "Math", "Physics", "Bushido"]
    },
    "Grade 8": {
        "Monday": ["KIA", "Uzbek", "PE", "PE"],
        "Tuesday": ["Biology", "IT", "History", "Bushido"],
        "Wednesday": ["Math", "Russian", "Robotics", "Chemistry"],
        "Thursday": ["Russian", "Uzbek", "IT", "Geography"],
        "Friday": ["Math", "Bushido", "History", "Physics"]
    },
    "Grade 9": {
        "Monday": ["KIA", "Uzbek", "PE", "PE"],
        "Tuesday": ["Biology", "IT", "History", "Bushido"],
        "Wednesday": ["Math", "Russian", "Robotics", "Chemistry"],
        "Thursday": ["Russian", "Uzbek", "IT", "Geography"],
        "Friday": ["Math", "Bushido", "History", "Physics"]
    },
    "Grade 10": {
        "Monday": ["Math", "IELTS", "IELTS"],
        "Tuesday": ["IELTS", "IT"],
        "Wednesday": ["Robotics", "IELTS", "IELTS"],
        "Thursday": ["IELTS", "SAT", "IELTS", "IELTS"],
        "Friday": ["Physics", "IELTS", "IELTS"]
    },
    "Grade 11": {
        "Monday": ["Math", "IELTS", "IELTS"],
        "Tuesday": ["IELTS", "IT"],
        "Wednesday": ["Robotics", "IELTS", "IELTS"],
        "Thursday": ["IELTS", "SAT", "IELTS", "IELTS"],
        "Friday": ["Physics", "IELTS", "IELTS"]
    }
}

user_data = {}

def create_markup(options, back_option=None):
    """Helper function to create a reply keyboard with options and a 'Back' button."""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        markup.add(option)
    if back_option:
        markup.add("⬅ Back")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    """Starts the bot and asks the user to choose between Schedule and Events."""
    chat_id = message.chat.id
    user_data[chat_id] = {}  # Initialize user data
    bot.send_message(chat_id, "Welcome! Choose an option:", reply_markup=create_markup(["📅 Schedule", "🎉 Events"]))

@bot.message_handler(func=lambda message: message.text in ["📅 Schedule", "🎉 Events"])
def handle_choice(message):
    """Handles the user's choice between Schedule and Events."""
    chat_id = message.chat.id
    if message.text == "📅 Schedule":
        bot.send_message(chat_id, "Choose your level:", reply_markup=create_markup(levels, back_option=True))
    elif message.text == "🎉 Events":
        bot.send_message(chat_id, "Select the month:", reply_markup=create_markup(months, back_option=True))

@bot.message_handler(func=lambda message: message.text in levels or message.text == "⬅ Back")
def select_level(message):
    """Handles the selection of the level."""
    chat_id = message.chat.id
    if message.text == "⬅ Back":
        return start(message)

    user_data[chat_id]['level'] = message.text
    bot.send_message(chat_id, "Select your grade:", reply_markup=create_markup(grades, back_option=True))

@bot.message_handler(func=lambda message: message.text in grades or message.text == "⬅ Back")
def select_grade(message):
    """Handles the selection of the grade."""
    chat_id = message.chat.id
    if message.text == "⬅ Back":
        return select_level(message)

    user_data[chat_id]['grade'] = message.text
    bot.send_message(chat_id, "Select the day of the week:", reply_markup=create_markup(days_of_week, back_option=True))

@bot.message_handler(func=lambda message: message.text in days_of_week or message.text == "⬅ Back")
def show_schedule(message):
    """Displays the schedule based on level, grade, and day."""
    chat_id = message.chat.id
    if message.text == "⬅ Back":
        return select_grade(message)

    level = user_data[chat_id].get('level', 'Unknown')
    grade = user_data[chat_id].get('grade', 'Unknown')
    day = message.text

    schedule_level = fixed_schedules.get(level, {}).get(day, [])
    schedule_grade = fixed_schedules.get(grade, {}).get(day, [])
    schedule = schedule_level + schedule_grade

    schedule_text = f"📚 **Schedule for {level} - {grade} on {day}:**\n" + "\n".join(f"- {s}" for s in schedule)
    bot.send_message(chat_id, schedule_text)

bot.polling()
