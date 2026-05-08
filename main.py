from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import random

BOT_TOKEN = "你的机器人TOKEN"
MASTER_ID = 你的TG数字ID

bot_on = False

async def start_bot(update: Update, context):
    global bot_on
    if update.effective_user.id == MASTER_ID and update.message.text == "开启":
        bot_on = True
        kb = [["个人中心","邀请赚钱"],["提现USDT"]]
        mark = ReplyKeyboardMarkup(kb, resize_keyboard=True)
        await update.message.reply_text("机器人已启动", reply_markup=mark)

async def reply_msg(update: Update, context):
    if not bot_on:
        return
    txt = update.message.text
    if txt == "个人中心":
        await update.message.reply_text("个人中心页面")
    elif txt == "邀请赚钱":
        await update.message.reply_text("邀请1人随机0.1~1USDT")
    elif txt == "提现USDT":
        await update.message.reply_text("余额满1USDT可提现")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, start_bot))
    app.add_handler(MessageHandler(filters.TEXT, reply_msg))
    app.run_polling()

if __name__ == "__main__":
    main()