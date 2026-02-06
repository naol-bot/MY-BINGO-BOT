import telebot
from telebot import types

# 1. ቶከንህን እዚህ " " ውስጥ አስገባ
BOT_TOKEN = "8247568982:AAERohgxWH-vvh6TKVk-KEDwTdPPgzJDJF4"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. ያንተ መረጃዎች (Wasihun) - አሁን በትክክል ተስተካክሏል
ADMIN_ID = 7467537727 
ADMIN_PHONE = "0979596741"
ADMIN_NAME = "Wasihun"

# 3. የጨዋታህ ሊንክ
GAME_URL = "https://naol-bot.github.io/MY-BINGO-BOT/"

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # 'Open App' ቁልፍ
    play_btn = types.InlineKeyboardButton(
        text="Open App 🎮", 
        web_app=types.WebAppInfo(url=GAME_URL)
    )
    
    deposit_btn = types.InlineKeyboardButton("DEPOSIT 📥", callback_data="deposit")
    withdraw_btn = types.InlineKeyboardButton("WITHDRAW 📤", callback_data="withdraw")
    register_btn = types.InlineKeyboardButton("REGISTER 📝", callback_data="register")
    support_btn = types.InlineKeyboardButton("SUPPORT 🎧", callback_data="support")
    
    markup.add(play_btn)
    markup.add(deposit_btn, withdraw_btn)
    markup.add(register_btn, support_btn)
    
    welcome_text = (
        "እንኳን ወደ ETHIO BINGO በደህና መጡ! 🎰\n\n"
        "💰 ቀሪ ሂሳብ: 0.00 ETB\n"
        "👤 ሁኔታ: Verified ✅\n\n"
        "ለመጫወት Open App የሚለውን ይጫኑ።"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "deposit":
        # የአጭር ጽሁፍ መመሪያ
        instructions = (
            "የሚያጋጥሟችሁን የክፍያ ችግር፦\n"
            "@Ethiobingo01 ላይ ፃፉልን።\n\n"
            "1️⃣ ከታች ባለው የቴሌብር አካውንት 50 ብር ያስገቡ\n"
            f"📱 Phone: {ADMIN_PHONE}\n"
            f"👤 Name: {ADMIN_NAME}\n\n"
            "2️⃣ የከፈሉበትን አጭር የጽሁፍ መልዕክት (Message) copy በማድረግ እዚህ ላይ Paste አድርገው ያስገቡና ይላኩ 👇👇👇"
        )
        bot.send_message(call.message.chat.id, instructions)

# ተጫዋቾች ማስረጃ ሲልኩ ለአድሚኑ (ለዋሲሁን) እንዲተላለፍ
@bot.message_handler(content_types=['text', 'photo'])
def handle_payment_proof(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "✅ ማስረጃው ደርሶናል! ዋሲሁን እስኪያረጋግጥ ጥቂት ደቂቃ ይጠብቁ።")
        
        admin_markup = types.InlineKeyboardMarkup()
        approve_btn = types.InlineKeyboardButton("✅ አጽድቅ (Approve)", callback_data=f"app_{message.chat.id}")
        reject_btn = types.InlineKeyboardButton("❌ ሰርዝ (Reject)", callback_data=f"rej_{message.chat.id}")
        admin_markup.add(approve_btn, reject_btn)
        
        if message.content_type == 'text':
            bot.send_message(ADMIN_ID, f"🔔 አዲስ ክፍያ ከ {message.chat.first_name}:\n\n{message.text}", reply_markup=admin_markup)
        else:
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"🔔 አዲስ ፎቶ ከ {message.chat.first_name}", reply_markup=admin_markup)

bot.polling()
