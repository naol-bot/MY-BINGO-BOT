import telebot
from telebot import types

# 1. የዋናው ቦትህ ቶከን እዚህ ይግባ (BotFather የሰጠህን)
TOKEN = '8247568982:AAERohgxWH-vvh6TKVk-KEDwTdPPgzJDJF4'
bot = telebot.TeleBot(TOKEN)

# 2. Start - ምዝገባ ሂደት
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reg_btn = types.KeyboardButton("Register 📝 (ስልክዎን ያጋሩ)", request_contact=True)
    markup.add(reg_btn)
    
    welcome_msg = "👋 እንኳን ደህና መጡ! ለመመዝገብ መጀመሪያ 'Register 📝' የሚለውን ቁልፍ ተጭነው ስልክዎን ያጋሩ።"
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

# 3. ምዝገባ ሲጠናቀቅ የሚመጣው መተግበሪያ መሰል ሜኑ
@bot.message_handler(content_types=['contact'])
def handle_registration(message):
    bot.send_message(message.chat.id, "✅ ተመዝግበዋል! አሁን ሁሉንም አገልግሎቶች መጠቀም ይችላሉ።", reply_markup=types.ReplyKeyboardRemove())
    
    inline_markup = types.InlineKeyboardMarkup(row_width=2)
    play = types.InlineKeyboardButton("Play 🎮", url="https://t.me/EthioBingo2") 
    balance = types.InlineKeyboardButton("Balance 💵", callback_data="check_balance")
    deposit = types.InlineKeyboardButton("Deposit 💰", callback_data="start_deposit")
    
    # ሰፖርት ምርጫ (ሁለቱን አዲሶቹን ቦቶች እንዲያመጣ)
    support = types.InlineKeyboardButton("Contact Support ↗️", callback_data="choose_support")
    
    instruction = types.InlineKeyboardButton("Instruction 📖", callback_data="show_info")
    transfer = types.InlineKeyboardButton("Transfer 🎁", callback_data="start_transfer")
    withdraw = types.InlineKeyboardButton("Withdraw 🤑", callback_data="start_withdraw")
    invite = types.InlineKeyboardButton("Invite 🔗", callback_data="start_invite")

    inline_markup.add(play)
    inline_markup.add(balance, deposit)
    inline_markup.add(support, instruction)
    inline_markup.add(transfer, withdraw)
    inline_markup.add(invite)

    bot.send_message(message.chat.id, "የሚፈልጉትን አገልግሎት ይምረጡ፦", reply_markup=inline_markup)

# 4. Support ምርጫ (ሁለቱ አካውንቶች)
@bot.callback_query_handler(func=lambda call: call.data == "choose_support")
def support_options(call):
    markup = types.InlineKeyboardMarkup()
    sup1 = types.InlineKeyboardButton("Support 1 ↗️", url="https://t.me/Ethiobingo01")
    sup2 = types.InlineKeyboardButton("Support 2 ↗️", url="https://t.me/Ethiobingo02")
    markup.add(sup1, sup2)
    bot.send_message(call.message.chat.id, "እባክዎ ማነጋገር የሚፈልጉትን አካውንት ይምረጡ፦", reply_markup=markup)

# 5. Deposit - መጠን ሲያስገቡ የባንክ ምርጫ እንዲመጣ
@bot.callback_query_handler(func=lambda call: call.data == "start_deposit")
def deposit_step(call):
    bot.send_message(call.message.chat.id, "💰 ማስገባት የሚፈልጉትን የብር መጠን ያስገቡ (ለምሳሌ፦ 50)::")

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_amount(message):
    amount = message.text
    markup = types.InlineKeyboardMarkup()
    btn_tele = types.InlineKeyboardButton("TELEBIRR", callback_data=f"pay_tele_{amount}")
    btn_cbe = types.InlineKeyboardButton("CBE BIRR", callback_data=f"pay_cbe_{amount}")
    markup.add(btn_tele, btn_cbe)
    
    bot.send_message(message.chat.id, f"🏦 የ {amount} ETB ክፍያ አማራጭ ይምረጡ፦", reply_markup=markup)

# 6. የክፍያ መመሪያ ከስልክ ቁጥር ጋር
@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def payment_details(call):
    data = call.data.split('_')
    method = "Telebirr" if data[1] == "tele" else "CBE Birr"
    amount = data[2]
    my_number = "0979596741" # ያንተን ስልክ ቁጥር እዚህ ቀይረው
    
    response = (f"✅ የ {method} ክፍያ መርጠዋል።\n\n"
                f"መጠን፦ {amount} ETB\n"
                f"ቁጥር፦ `{my_number}`\n"
                "ስም፦ [ያንተ ስም እዚህ ይግባ]\n\n"
                "ክፍያውን ከፈጸሙ በኋላ የደረሰኝ ፎቶ እዚህ ይላኩ።")
    bot.send_message(call.message.chat.id, response, parse_mode="Markdown")

# 7. Instruction (መመሪያ)
@bot.callback_query_handler(func=lambda call: call.data == "show_info")
def show_instruction(call):
    text = "📖 **መመሪያ**\n\n1. Register ተጭነው ይመዝገቡ\n2. Deposit በማድረግ ብር ያስገቡ\n3. Play ተጭነው ይጫወቱ"
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

# 8. Withdraw & Transfer
@bot.callback_query_handler(func=lambda call: call.data in ["start_withdraw", "start_transfer"])
def other_actions(call):
    if call.data == "start_withdraw":
        bot.send_message(call.message.chat.id, "🤑 ማውጣት የሚፈልጉትን መጠን ይጻፉ (ዝቅተኛ 50 ETB)።")
    elif call.data == "start_transfer":
        bot.send_message(call.message.chat.id, "🎁 ማስተላለፍ የሚፈልጉትን ሰው ስልክ ቁጥር ያስገቡ።")

bot.polling()
