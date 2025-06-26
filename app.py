import telebot
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4")

bot = telebot.TeleBot(7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4)

ADMIN_PASSWORD = "ADNİOBERTİ61"
user_states = {}  # Ulanyjy ýagdaýy: {"12345": "awaiting_token"}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Bot goşmak", "📦 Botlar sanawy")
    markup.add("👨‍💻 Admin Panel", "🚪 Çykmak")
    bot.send_message(message.chat.id, "🎛 *Baş menýu* saýlaň:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "➕ Bot goşmak")
def add_bot(message):
    bot.send_message(message.chat.id, "🤖 Goşmak isleýän botuň *TOKEN*-ini iber:", parse_mode="Markdown")
    user_states[message.chat.id] = "awaiting_token"

@bot.message_handler(func=lambda msg: user_states.get(msg.chat.id) == "awaiting_token")
def save_token(message):
    token = message.text.strip()
    user_id = str(message.chat.id)

    # Faýl ady ulanyjynyň ID-sine görä
    config_path = f"bot_configs/{user_id}.json"
    os.makedirs("bot_configs", exist_ok=True)

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
    else:
        data = {"bots": []}

    data["bots"].append({"token": token})
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)

    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "✅ Bot üstünlikli goşuldy!")

@bot.message_handler(func=lambda msg: msg.text == "📦 Botlar sanawy")
def list_bots(message):
    user_id = str(message.chat.id)
    config_path = f"bot_configs/{user_id}.json"

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            bots = data.get("bots", [])
            if not bots:
                bot.send_message(message.chat.id, "⛔ Hiç hili bot goşulmady.")
                return
            text = "🤖 Goşulan botlaryň sanawy:\n\n"
            for i, b in enumerate(bots, 1):
                text += f"{i}. {b['token'][:20]}...\n"
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "⛔ Hiç hili bot goşulmady.")

@bot.message_handler(func=lambda msg: msg.text == "🚪 Çykmak")
def exit_menu(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "🔒 Panelden çykdyňyz.", reply_markup=markup)

bot.polling()
