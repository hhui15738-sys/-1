from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters

# ========= 在这里填写你的信息 =========
BOT_TOKEN = "粘贴你的Bot Token"
ADMIN_ID = 填写你的数字ID
# ==================================

bot_ready = False

# 管理员开启机器人
async def handle_message(update: Update, ctx):
    global bot_ready

    text = update.message.text.strip()
    uid = update.effective_user.id

    # 管理员发送「开启」激活
    if uid == ADMIN_ID and text == "开启":
        bot_ready = True
        keyboard = [
            [KeyboardButton("个人中心"), KeyboardButton("邀请赚钱")],
            [KeyboardButton("提现USDT")]
        ]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("✅ 空投机器人已成功启动", reply_markup=markup)
        return

    # 机器人未激活，不回复任何人
    if not bot_ready:
        return

    # 功能菜单响应
    if text == "个人中心":
        await update.message.reply_text("这是你的个人中心页面")
    elif text == "邀请赚钱":
        await update.message.reply_text("邀请1名有效飞机会员，随机获得0.1~1 USDT奖励")
    elif text == "提现USDT":
        await update.message.reply_text("余额满1 USDT即可提交提现")

# 程序入口
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("🤖 机器人正在启动...")
    app.run_polling()