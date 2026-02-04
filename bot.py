import telebot
from telebot import types

# ከ BotFather ያገኘኸውን Token እዚህ ጋር በዝርዝር አስገባ
TOKEN = 8247568982:(AAHVDdJ82EhphoGeqnUn-vNbSVdiILZSMqs)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # ቁልፎቹን ማዘጋጃ (Markup)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # 1. Play ቁልፍ (ወደ ሰራኸው የዌብ አፕ ይወስዳል)
    play = types.InlineKeyboardButton("Play 🎮", url="https://t.me/Fair_Bingo_bot/play")
    
    # 2. ሌሎች ቁልፎች
    balance = types.InlineKeyboardButton("Balance 💵", callback_data='balance')
    deposit = types.InlineKeyboardButton("Deposit 💰", callback_data='deposit')
    support = types.InlineKeyboardButton("Contact Support", url="https://t.me/naol_admin)
    instruction = types.InlineKeyboardButton("Instruction 📖", callback_data='how_to')
    transfer = types.InlineKeyboardButton("Transfer 🎁", callback_data='transfer')
    withdraw = types.InlineKeyboardButton("Withdraw 🤑", callback_data='withdraw')
    invite = types.InlineKeyboardButton("Invite 🔗", callback_data='invite')
    
    # አደራደሩን ማስተካከል
    markup.add(play)
    markup.add(balance, deposit)
    markup.add(support, instruction)
    markup.add(transfer, withdraw)
    markup.add(invite)
    
    bot.send_message(message.chat.id, "✅ ተመዝግበዋል!", reply_markup=markup)

# ተጠቃሚው ቁልፎቹን ሲጫን የሚሰጠው መልስ
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "deposit":
        bot.send_message(call.message.chat.id, "💰 ማስገባት የፈለጉትን የብር መጠን ከ 10 ብር ጀምሮ ያስገቡ።")
    elif call.data == "balance":
        bot.send_message(call.message.chat.id, "💵 የአሁኑ ቀሪ ሂሳብዎ 0.00 ETB ነው።")

bot.polling()
