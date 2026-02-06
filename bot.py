import telebot
from telebot import types

# 1. ቶከንህን ከ @BotFather አምጥተህ እዚህ ተካ
BOT_TOKEN = "8247568982:AAERohgxWH-vvh6TKVk-KEDwTdPPgzJDJF4"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. ያንተን ID ከ @userinfobot አምጥተህ እዚህ ተካ
ADMIN_ID =  7467537727

# የጨዋታህ ሊንክ
GAME_URL = "https://naol-bot.github.io/MY-BINGO-BOT/"

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    play_btn = types.InlineKeyboardButton("PLAY 10 🎮", web_app=types.WebAppInfo(url=GAME_URL))
    deposit_btn = types.InlineKeyboardButton("DEPOSIT 📥", callback_data="deposit")
    withdraw_btn = types.InlineKeyboardButton("WITHDRAW 📤", callback_data="withdraw")
    
    markup.add(play_btn)
    markup.add(deposit_btn, withdraw_btn)
    
    bot.send_message(message.chat.id, "እንኳን ወደ ETHIO BINGO መጡ! 🎰\n💰 ቀሪ ሂሳብ: 60.00 ETB", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "deposit":
        # በፎቶው ላይ ያየኸው የክፍያ መመሪያ
        instructions = (
            "የሚያጋጥሟችሁን የክፍያ ችግር፦\n"
            "@Ethiobingo01 ላይ ፃፉልን።\n\n"
            "1️⃣ ከታች ባለው የቴሌብር አካውንት  ብር ያስገቡ\n"
            "📱 Phone: 0979596741\n"
            "👤 Name: Wasihun\n\n"
            "2️⃣ የከፈሉበትን አጭር የጽሁፍ መልዕክት ኮፒ አድርገው እዚህ ይላኩ 👇👇👇"
        )
        bot.send_message(call.message.chat.id, instructions)

bot.polling()
