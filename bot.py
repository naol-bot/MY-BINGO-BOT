import telebot
from telebot import types
import cards 

# 1. ቶከንህን እዚህ አስገባ
BOT_TOKEN = "8247568982:AAERohgxWH-vvh6TKVk-KEDwTdPPgzJDJF4"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. ያንተ መረጃዎች (Wasihun)
ADMIN_ID = 7467537727 
ADMIN_PHONE = "0979596741" 
ADMIN_NAME = "Wasihun"

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # አዝራሮች ከ icons ጋር
    play_btn = types.InlineKeyboardButton("PLAY 🎮", web_app=types.WebAppInfo(url="https://naol-bot.github.io/MY-BINGO-BOT/"))
    reg_btn = types.InlineKeyboardButton("REGISTER 📝", callback_data="register")
    bal_btn = types.InlineKeyboardButton("BALANCE 💰", callback_data="balance")
    dep_btn = types.InlineKeyboardButton("DEPOSIT 📥", callback_data="deposit")
    with_btn = types.InlineKeyboardButton("WITHDRAW 📤", callback_data="withdraw")
    trans_btn = types.InlineKeyboardButton("TRANSFER 💸", callback_data="transfer")
    inv_btn = types.InlineKeyboardButton("INVITE 👥", callback_data="invite")
    sup_btn = types.InlineKeyboardButton("SUPPORT 🎧", callback_data="support")
    inst_btn = types.InlineKeyboardButton("INSTRUCTION 📖", callback_data="instruction") # አዲሱ ቁልፍ
    
    markup.add(play_btn)
    markup.add(reg_btn, bal_btn)
    markup.add(dep_btn, with_btn)
    markup.add(trans_btn, inv_btn)
    markup.add(sup_btn, inst_btn)
    
    welcome_text = (
        "እንኳን ወደ ETHIO BINGO በደህና መጡ! 🎰\n\n"
        "💰 ቀሪ ሂሳብ: 0.00 ETB\n"
        "👤 ሁኔታ: Verified ✅\n\n"
        "ለመጀመር PLAY የሚለውን ይጫኑ ወይም መመሪያውን ያንብቡ።"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "instruction":
        guide = (
            "📖 **ኢትዮ ቢንጎን እንዴት መጫወት ይቻላል?**\n\n"
            "1️⃣ **መመዝገብ**: በመጀመሪያ REGISTER የሚለውን ተጭነው ይመዝገቡ።\n"
            "2️⃣ **ብር ማስገባት**: DEPOSIT የሚለውን በመጫን በተቀመጠው ስልክ ቁጥር ብር ያስገቡና ደረሰኙን ለቦቱ ይላኩ።\n"
            "3️⃣ **መጫወት**: ባላንስዎ ላይ ብር ሲኖር PLAY የሚለውን ተጭነው ጨዋታውን ይጀምሩ።\n"
            "4️⃣ **ማሸነፍ**: በጨዋታው ላይ ቢንጎ ሲሰሩ ያሸነፉት ብር በቀጥታ ባላንስዎ ላይ ይጨመራል።\n"
            "5️⃣ **ብር ማውጣት**: ያሸነፉትን ብር በማንኛውም ጊዜ WITHDRAW በሚለው ቁልፍ ማውጣት ይችላሉ።\n\n"
            "ጥያቄ ካለዎት SUPPORT የሚለውን ይጫኑ።"
        )
        bot.send_message(call.message.chat.id, guide, parse_mode="Markdown")
    
    elif call.data == "deposit":
        bot.send_message(call.message.chat.id, f"💳 በ {0979596741} ({WASIHUN})  ብር ከፍለው የደረሰኝ ፎቶ ወይም አጭር መልእክት እዚህ ይላኩ።")

    # የቀሩት ቁልፎች ምላሽ እዚህ ይቀጥላል...
    else:
        bot.send_message(call.message.chat.id, "ይህ አገልግሎት በቅርብ ቀን ይጀምራል።")

bot.polling()
