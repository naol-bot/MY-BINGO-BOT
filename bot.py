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
