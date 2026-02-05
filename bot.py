import telebot
from telebot import types

# ከ BotFather ያገኘኸውን Token እዚህ ነጠላ ሰረዝ ውስጥ አስገባ
TOKEN = '8247568982:AAERohgxWH-vvh6TKVk-KEDwTdPPgzJDJF4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # ቁልፎቹ በፎቶው ላይ ባየኸው አደራደር
    play = types.InlineKeyboardButton("Play 🎮", url="https://t.me/Fair_Bingo_bot/play")
    balance = types.InlineKeyboardButton("Balance 💵", callback_data='balance')
    deposit = types.InlineKeyboardButton("Deposit 💰", callback_data='deposit')
    support = types.InlineKeyboardButton("Contact Support", url="https://t.me/naol_admin") # እዚህ ጋር ዩዘርኔምህን ቀይር
    instruction = types.InlineKeyboardButton("Instruction 📖", callback_data='how_to')
    transfer = types.InlineKeyboardButton("Transfer 🎁", callback_data='transfer')
    withdraw = types.InlineKeyboardButton("Withdraw 🤑", callback_data='withdraw')
    invite = types.InlineKeyboardButton("Invite 🔗", callback_data='invite')
    
    markup.add(play)
    markup.add(balance, deposit)
    markup.add(support, instruction)
    markup.add(transfer, withdraw)
    markup.add(invite)
    
    bot.send_message(message.chat.id, "✅ እንኳን ደህና መጡ! መጫወት ለመጀመር Play የሚለውን ይጫኑ።", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "deposit":
        bot.send_message(call.message.chat.id, "💰 ማስገባት የፈለጉትን የብር መጠን ያስገቡ።")
    elif call.data == "balance":
        bot.send_message(call.message.chat.id, "💵 የአሁኑ ቀሪ ሂሳብዎ 0.00 ETB ነው።")

bot.polling()
# ተጠቃሚው መጠን ሲጽፍ የሚመጣ የክፍያ አማራጭ
@bot.message_handler(func=lambda message: message.text.isdigit())
def deposit_options(message):
    amount = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_tele = types.InlineKeyboardButton("TELEBIRR", callback_data=f"pay_tele_{amount}")
    btn_cbe = types.InlineKeyboardButton("CBE BIRR", callback_data=f"pay_cbe_{amount}")
    btn_cancel = types.InlineKeyboardButton("❌ ሰርዝ (Cancel)", callback_data="cancel_pay")
    
    markup.add(btn_tele, btn_cbe)
    markup.add(btn_cancel)
    
    text = (
        "🏦 የሚፈልጉትን የክፍያ አማራጭ ይምረጡ ፦\n"
        "– ከቴሌ ብር ወደ ቴሌ ብር\n"
        "– ከሲቢኢ ወደ ሲቢኢ ብቻ ያስገቡ"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

# ለቁልፎቹ መልስ የሚሰጥ ክፍል
@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def process_payment(call):
    data = call.data.split('_')
    method = "Telebirr" if data[1] == "tele" else "CBE Birr"
    amount = data[2]
    
    # ስልክ ቁጥርህን እዚህ ጋር ቀይረው
    my_number = "0979596741" 
    
    response = (
        f"✅ የ {method} ክፍያ መርጠዋል።\n\n"
        f"መጠን፦ {amount} ETB\n"
        f"የመክፈያ ቁጥር፦ `{my_number}`\n"
        f"ስም፦ ያንተ ስም\n\n"
        "ክፍያውን ከፈጸሙ በኋላ የደረሰኝ ፎቶ እዚህ ይላኩ።"
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "cancel_pay")
def cancel_payment(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❌ የክፍያ ትዕዛዙ ተሰርዟል።")
