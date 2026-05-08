from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters

# ========= 请修改为你自己的信息 =========
BOT_TOKEN = "在这里粘贴你的Bot Token"
ADMIN_ID = 123456789   # 换成你自己的TG数字ID
# ======================================

bot_on = False

async def handle_all(update: Update, context):
    global bot_on
    text = update.message.text.strip()
    uid = update.effective_user.id

    # 仅管理员发送「开启」启动机器人
    if uid == ADMIN_ID and text == "开启":
        bot_on = True
        keyboard = [
            [KeyboardButton("个人中心"), KeyboardButton("邀请赚钱")],
            [KeyboardButton("提现USDT")]
        ]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("✅ 空投机器人已成功启动，全部功能已激活", reply_markup=markup)
        return

    # 未启动时，不对普通用户做出任何回复
    if not bot_on:
        return

    # 菜单功能响应
    if text == "个人中心":
        await update.message.reply_text("""📋 个人中心
💰 可用余额：8.00 USDT
👥 已邀请：0 人
🏅 会员身份：普通用户""")
    elif text == "邀请赚钱":
        await update.message.reply_text("🎁 邀请1位有效飞机会员，随机获得 0.1 ~ 1 USDT 奖励，多邀多得，中奖概率翻倍！")
    elif text == "提现USDT":
        await update.message.reply_text("💳 提现规则：余额满 1 USDT 即可提交提现，审核后到账")


if __name__ == "__main__":
    print("🤖 机器人正在启动...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_all))
    app.run_polling()