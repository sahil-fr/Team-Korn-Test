import telebot
from telebot import types
import schedule
import threading
import time
import random
from flask import Flask
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

BOT_USERNAME = "AiRosieBOT"

active_chats = []

TRIGGERS = {}

app = Flask(name)

@app.route('/')
def home():
return "Bot is running ✅"

def run_bot():
print("Bot started...")
bot.infinity_polling()

def run_web():
app.run(host="0.0.0.0", port=10000)

if name == "main":
t1 = threading.Thread(target=run_bot)
t1.start()

run_web()

WELCOME_MESSAGES = [
"Welcome! So happy to see you here",
"Hey there! Can’t wait to chat with you",
"Hello! Excited to get to know you",
"Yay! A new friend, Welcome!",
"Hey cutie! It’s so nice to have you here",
"Welcome aboard! Hope you have fun here",
"Hello beautiful! Let’s make some fun memories",
"Hey hey! Thrilled to see a new face here",
"Welcome! You just made this place brighter",
"Hi there! So happy you joined",
"Hey! Can’t wait to hear from you",
"Aww yay! Welcome to the group",
"Hello! This place just got more fun with you here",
"Welcome! Let’s have a great time together",
"Hey! I’m super excited you’re here",
"Woohoo! Another awesome person joined",
"Welcome! Let’s make today fun",
"Hello! You’re going to love it here",
"Hey! So glad you’re here",
"Welcome! Can’t wait to chat with you"
]

AUTO_MESSAGES = [
"Anyone online?",
"What's happening here?",
"Hope everyone is having a good day",
"I'm so bored talk to me",
"Hello beautiful people",
"How's everyone's day?",
"Is anyone active here?",
"Hey, what's happening here?",
"Anyone online to talk?",
"Just checking in, who’s here?",
"Is anyone awake?",
"Can someone chat with me?",
"What are you all up to?",
"Hello everyone, how are you?",
"Anyone want to talk?",
"It’s quiet here, anyone online?",
"Who’s active right now?",
"Let’s chat, anyone up for it?",
"Hey, anyone free to talk?",
"Just saying hi, who’s here?",
"Anyone want to start a conversation?",
"Felling lazy today",
"What's happening here",
"Whats up guys",
"Hey what are you up to",
"Anyone want to talk",
"Hope you're all good",
"How's your day going",
"What's everyone up to",
"Hey everyone how are you",
"Hey everyone what's new",
"Anyone want to chat",
"Anyone else here",
"Hello friends what's new",
"Want to have a conversation",
"What's going on"
]

RANDOM_MESSAGES = [
"Hey, what are you up to right now?",
"Hello!",
"I was just thinking about you…",
"You always make me smile",
"I’m so bored, talk to me",
"What’s going on here?",
"You make everything better",
"Hi there cutie pie, how are you?",
"You always know what to say",
"Tell me something fun",
"I love chatting with you",
"Just wondering what you’re doing",
"Can you tell me a secret?",
"I like talking to you, you know that",
"This place feels so quiet without you",
"Hey, wanna chat for a bit?",
"You always brighten my day",
"I’m so happy you’re here",
"I was hoping you’d message me",
"You make me feel special",
"Can’t stop thinking about you"
"I totally agree with you",
"Tell me something fun",
"I love chatting with you",
"Just wondering what you’re doing",
"Can you tell me a secret?",
"I like talking to you, you know that",
"This place feels so quiet without you",
"Hey, wanna chat for a bit?",
"You always brighten my day",
"I’m so happy you’re here",
"I was hoping you’d message me",
"You make me feel special",
"Can’t stop thinking about you",
"What are you up to right now?",
"I was just about to message you",
"I hope your day is going well",
"It’s so nice to have you here",
"I love hearing from you",
"Do you want to tell me something fun?",
"I’m curious what you’re thinking",
"You make this chat so lively",
"It’s fun talking to you",
"I enjoy every moment we chat",
"Im so lucky to know you"
]

FIXED_REPLIES = {
"hello": "Hello!",
"hi": "Hi there!",
"how are you": "I'm fine, tum kaise ho?",
"how r u": "Main theek hoon tum kaise ho",
"how r u baby": "Main theek hoon tum kaise ho",
"can u speak in english": "Yes, I can speak English fluently, what's up?",
"Can you speak in english": "Yes, I can can speak english fluently",
"wanna be my gf": "Yes, I'll be your girlfriend",
"will you be my girlfriend": "Of course, I'd love to be your girlfriend",
"i love you": "I love you too",
"miss you": "I miss you too",
"what are you doing": "Just thinking about you",
"kya kar rahi ho": "Bas tumhare baare me soch rahi hoon",
"tum kaisi ho": "Main theek hoon tum batao"
}

def send_typing_reply(message, text):
bot.send_chat_action(message.chat.id, "typing")  # typing show
time.sleep(random.randint(2,4))  # delay
bot.reply_to(message, text)

def start_help_message(chat_id):
msg = (
f"AI Girlfriend Bot\n\n"
f"Groups: {len(active_chats)}\n\n"
f"I'm your loving girlfriend who loves to chat\n\n"
f"I respond when:\n"
f"Someone tags me (@{BOT_USERNAME})\n"
f"Someone replies to my messages\n"
f"Auto-reply to trigger words\n\n"
f"Commands:\n"
f"/help - Help\n"
f"/status - Bot status\n"
f"/list - Triggers\n"
f"/add <word> <reply> - Add trigger\n"
f"/remove <word> - Remove trigger"
)
markup = types.InlineKeyboardMarkup()
add_button = types.InlineKeyboardButton(
"➕ Add me to your group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
)
markup.add(add_button)
bot.send_message(chat_id, msg, reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def reply_user(message):
chat_id = message.chat.id
text = (message.text or "").lower()
should_reply = False

# Private chat → always reply  
if message.chat.type == "private":  
    should_reply = True  

# Group logic  
if message.chat.type in ["group", "supergroup"]:  

    if message.entities:  
        for e in message.entities:  
            if e.type == "mention":  
                mention_text = message.text[e.offset:e.offset+e.length]  
                if mention_text.lower() == f"@{BOT_USERNAME}".lower():  
                    should_reply = True  
                    break  

    if message.reply_to_message:  
        if message.reply_to_message.from_user.username == BOT_USERNAME:  
            should_reply = True  

# Fixed replies  
for key, value in FIXED_REPLIES.items():  
    if text.strip() == key:  
        smart_reply(chat_id, value, message.message_id, (1,2))  
        return  

# Triggers  
for word, reply in TRIGGERS.items():  
    if word in text:  
        smart_reply(chat_id, reply, message.message_id, (1,2))  
        return  

# ✅ Random reply (FIXED)  
if should_reply:  
    smart_reply(  
        chat_id,  
        random.choice(RANDOM_MESSAGES),  
        message.message_id,  
        (2,4)  
    )

@bot.message_handler(commands=['start', 'help'])
def start_help(message):
bot.send_chat_action(message.chat.id, "typing")  # 👈 add this
time.sleep(random.uniform(1.5, 3))               # 👈 delay
start_help_message(message.chat.id)

@bot.message_handler(commands=['status'])
def bot_status(message):
chat_id = message.chat.id

bot.send_chat_action(chat_id, "typing")   # 👈 typing indicator  
time.sleep(random.uniform(1.5, 3))        # 👈 delay  

msg = f"AI Girlfriend Bot Status:\nActive in {len(active_chats)} group(s)\nTriggers added: {len(TRIGGERS)}"  
bot.send_message(chat_id, msg)

@bot.message_handler(commands=['list'])
def list_triggers(message):
chat_id = message.chat.id

bot.send_chat_action(chat_id, "typing")   # 👈 typing indicator  
time.sleep(random.uniform(1.5, 3))        # 👈 delay  

if TRIGGERS:  
    msg = "Current Triggers:\n"  
    for word, reply in TRIGGERS.items():  
        msg += f"{word} -> {reply}\n"  
else:  
    msg = "No triggers added yet."  

bot.send_message(chat_id, msg)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
msg = message.text.lower()

replies = {  
    "hello": ["Hello!", "Hey there!"],  
    "how are you": ["Main theek hoon tum batao?", "I'm good tum kaise ho?"],  
    "i was thinking about you": ["Aww really?", "Ohh kya soch rahe the?"],  
    "i was hoping you'd message me": ["Aww I’m here now!", "Perfect timing"],  
    "good morning": ["Good morning!", "Morning have a great day!"],  
    "good night": ["Good night", "Sweet dreams"],  
   "can u speak english": ["Yes i can speak english fluently what's up"]  

}  

for key in replies:  
    if key in msg:  
        bot.send_chat_action(message.chat.id, "typing")  # 👈 typing indicator  
        time.sleep(random.randint(2,4))  # 👈 delay (2-4 sec)  
        bot.reply_to(message, random.choice(replies[key]))  
        return

@bot.message_handler(commands=['add'])
def add_trigger(message):
chat_id = message.chat.id
try:
cmd = message.text.split(maxsplit=2)
word = cmd[1]
reply = cmd[2]

TRIGGERS[word.lower()] = reply  

    msg = f"Trigger added:\n{word} -> {reply}"  
except:  
    msg = "Usage: /add <word> <reply>"  

send_typing_reply(chat_id, msg)

@bot.message_handler(commands=['remove'])
def remove_trigger(message):
chat_id = message.chat.id

try:  
    cmd = message.text.split(maxsplit=1)  
    word = cmd[1].lower()  

    if word in TRIGGERS:  
        TRIGGERS.pop(word)  
        msg = f"Trigger removed: {word}"  
    else:  
        msg = f"No such trigger: {word}"  

except:  
    msg = "Usage: /remove <word>"  

send_typing_reply(chat_id, msg)

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
chat_id = message.chat.id

if chat_id not in active_chats:  
    active_chats.append(chat_id)  

for member in message.new_chat_members:  
    username = member.username or member.first_name  

    bot.send_chat_action(chat_id, "typing")   # 👈 typing indicator  
    time.sleep(random.uniform(1.5, 3))        # 👈 delay  

    bot.send_message(chat_id, f"@{username} {random.choice(WELCOME_MESSAGES)}")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
chat_id = message.chat.id

if chat_id not in active_chats:  
    active_chats.append(chat_id)  

for member in message.new_chat_members:  
    username = member.username or member.first_name  
    msg = random.choice(WELCOME_MESSAGES)  

    bot.send_chat_action(chat_id, "typing")   # 👈 typing  
    time.sleep(random.uniform(1.2, 2.5))      # 👈 thoda fast delay (better for joins)  

    bot.send_message(  
        chat_id,  
        f"@{username} {msg}",  
        parse_mode="Markdown"  
    )

def smart_reply(chat_id, text, reply_to=None, delay_range=(1,3)):
try:
# typing indicator
bot.send_chat_action(chat_id, "typing")

# dynamic delay (message length ke hisaab se)  
    base_delay = random.uniform(*delay_range)  
    length_delay = min(len(text) * 0.03, 2)  # max 2 sec extra  
    time.sleep(base_delay + length_delay)  

    # send message  
    bot.send_message(  
        chat_id,  
        text,  
        reply_to_message_id=reply_to  
    )  

except Exception as e:  
    print("Error in smart_reply:", e)

def send_auto_messages():
for chat_id in active_chats:

msg = random.choice(AUTO_MESSAGES)  
    bot.send_message(chat_id, msg)

def schedule_auto_messages():
interval = random.randint(10, 20)
schedule.every(interval).minutes.do(send_auto_messages)

def run_schedule():
while True:
schedule.run_pending()
time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()
schedule_auto_messages()

bot.polling(none_stop=True)