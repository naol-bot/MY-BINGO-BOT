import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# --- መረጃዎች ---
TOKEN = '8247568982:AAERohgxWH-vvh6TKVk-KEDwTdPPgzJDJF4' # የቦትህን ቶክን እዚህ ተካ
ADMIN_ID = 7467537727  # ያንተን የቴሌግራም ID እዚህ ተካ
BET_PRICE = 10 

class BingoBot:
    def __init__(self):
        self.players = {} # {user_id: {"main_bal": 0, "play_bal": 0, "cards": []}}
        self.occupied_cards = {}

bot_logic = BingoBot()

# --- ሜኑዎች (እንደ ምስል 1 እና 2) ---
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Play 🎮", callback_data='play')],
        [InlineKeyboardButton("Balance 💵", callback_data='bal'), InlineKeyboardButton("Deposit 💰", callback_data='dep')],
        [InlineKeyboardButton("Contact Support...", callback_data='sup'), InlineKeyboardButton("Instruction 📖", callback_data='ins')],
        [InlineKeyboardButton("Transfer 🎁", callback_data='tra'), InlineKeyboardButton("Withdraw 🤑", callback_data='wit')],
        [InlineKeyboardButton("Invite 🔗", callback_data='inv')]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- ትዕዛዞች ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in bot_logic.players:
        bot_logic.players[user_id] = {"main_bal": 0, "play_bal": 0, "cards": [], "name": update.effective_user.first_name}
    await update.message.reply_text("👋 እንኳን ወደ ETHIO BINGO በሰላም መጡ!", reply_markup=main_menu())

# --- የቁልፎች ምላሽ ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'ins':
        # በምስል 9 እና 10 ላይ ያሉትን ህጎች በሙሉ ያካትታል
        instructions = (
            "📖 **የቢንጎ ጨዋታ ህጎች**\n\n"
            "**1. ካርድ መምረጥ 🃏**\n"
            "• ከ 1-400 ካርድ ውስጥ አንዱን ይመርጣሉ። በቀይ ቀለም ያለባቸው ቀድሞ የተያዙ ናቸው።\n"
            "**2. ጨዋታው ሲጀመር 🎲**\n"
            "• ከ 1-75 ቁጥሮች ይወጣሉ። ካርድዎ ላይ ካለ ይንኩት (Click)።\n"
            "**3. አሸናፊነት 🏆**\n"
            "• በረድፍ፣ በዓምድ ወይም በሰያፍ ከሞሉ 'Bingo' የሚለውን ይጫኑ።"
        )
        await query.message.reply_text(instructions, parse_mode='Markdown')

    elif query.data == 'dep':
        # እንደ ምስል 4 እና 5
        await query.message.reply_text(
            "💰 **ብር ለማስገባት**\n\n"
            "1. በቴሌብር **0979596741 (Wasihun)** ላይ 10 ብር እና ከዚያ በላይ ያስገቡ።\n"
            "2. የደረሰኝ ቁጥሩን (SMS) ኮፒ አድርገው እዚህ 'Paste' ያድርጉ።",
            parse_mode='Markdown'
        )

    elif query.data == 'bal':
        # እንደ ምስል 11
        p = bot_logic.players[user_id]
        await query.message.reply_text(f"💳 **የእርስዎ ሂሳብ**\n\nMain Wallet: {p['main_bal']} ETB\nPlay Wallet: {p['play_bal']} ETB")

# --- የክፍያ ማረጋገጫ (SMS) ሲላክ ---
async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    
    # የቴሌብር መልዕክት መሆኑን ማረጋገጥ
    if "telebirr" in text.lower() or "received" in text.lower():
        admin_kb = [[InlineKeyboardButton("✅ አጽድቅ (10)", callback_data=f"approve_10_{user.id}"),
                     InlineKeyboardButton("❌ ሰርዝ", callback_data=f"reject_{user.id}")]]
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"💰 አዲስ ክፍያ ከ {user.first_name}:\n\n{text}", reply_markup=InlineKeyboardMarkup(admin_kb))
        await update.message.reply_text("⏳ ማረጋገጫዎ ለአስተዳዳሪ ተልኳል።")

# --- የአስተዳዳሪ ማረጋገጫ ---
async def admin_verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data.startswith("approve_"):
        _, amount, uid = data.split("_")
        bot_logic.players[int(uid)]["main_bal"] += int(amount)
        await context.bot.send_message(chat_id=int(uid), text=f"✅ {amount} ብር በሂሳብዎ ላይ ተጨምሯል!")
        await query.edit_message_text("ክፍያው ጸድቋል ✅")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(ins|dep|bal)$"))
    app.add_handler(CallbackQueryHandler(admin_verify, pattern="^(approve|reject)_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment))
    print("DIL BINGO በ Railway ላይ ለመስራት ዝግጁ ነው!")
    app.run_polling()

if __name__ == '__main__':
    main()
