from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import random

# ===== 基础配置 在这里修改 =====
BOT_TOKEN = "这里填你的机器人TOKEN"
MASTER_ID = 8684151999
START_MSG = "✅ 空投机器人已启动，发送「开启」激活全部功能"

# 邀请奖励配置
INVITE_REWARD_LIST = [
    {"money": 0.1, "percent": 40},
    {"money": 0.3, "percent": 30},
    {"money": 0.6, "percent": 20},
    {"money": 1.0, "percent": 10},
]
# 解锁门槛
LOTTERY_LIMIT = 100
RED_LIMIT = 50
TOTAL_POOL = 1025
# =============================

bot_active = False
user_data = {}

# 底部功能菜单
main_keyboard = [
    [KeyboardButton("个人中心"), KeyboardButton("邀请赚钱")],
    [KeyboardButton("提现USDT"), KeyboardButton("实时排行榜")]
]
reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# 初始化新用户
def init_user(uid: int):
    if uid not in user_data:
        user_data[uid] = {
            "balance": 8.00,
            "airdrop": 0.00,
            "invite_num": 0,
            "active": 0,
            "is_vip": False
        }

# 检测飞机会员
def check_plane_vip(user):
    name_text = (user.full_name + (user.username or "")).lower()
    return any(word in name_text for word in ["✈", "飞机", "✈️", "plane"])

# 随机邀请奖励
def get_invite_bonus():
    pool = []
    for item in INVITE_REWARD_LIST:
        pool += [item["money"]] * item["percent"]
    return round(random.choice(pool), 2)

# 管理员开启机器人
async def power_on(update: Update):
    global bot_active
    user_id = update.effective_user.id
    text = update.message.text.strip()
    if user_id == MASTER_ID and text == "开启":
        bot_active = True
        await update.message.reply_text(START_MSG, reply_markup=reply_markup)

# 个人中心
async def my_center(update: Update):
    uid = update.effective_user.id
    user = update.effective_user
    init_user(uid)
    info = user_data[uid]
    vip_tag = "✅ 飞机会员" if info["is_vip"] else "❌ 普通用户"
    res = f"""🤖 空投机器个人中心
昵称：{user.full_name}
ID：{uid}
可用余额：{info['balance']:.2f} USDT
空投余额：{info['airdrop']:.2f} USDT
成功邀请：{info['invite_num']} 人
会员身份：{vip_tag}

🔥 当前全局奖池：{TOTAL_POOL}.00 USDT
"""
    await update.message.reply_text(res)

# 抽奖功能
async def lottery_draw(update: Update, context):
    if not bot_active:
        return
    chat = update.effective_chat
    members = await context.bot.get_chat_members(chat.id)
    eligible_users = []
    for member in members:
        if member.user.is_bot:
            continue
        uid = member.user.id
        init_user(uid)
        user_data[uid]["is_vip"] = check_plane_vip(member.user)
        if user_data[uid]["is_vip"] and user_data[uid]["invite_num"] >= LOTTERY_LIMIT:
            eligible_users.append(uid)
    if not eligible_users:
        await update.message.reply_text("❌ 暂无可参与抽奖的达标飞机会员")
        return
    weight_pool = []
    for uid in eligible_users:
        weight = 1 + user_data[uid]["invite_num"] / 10 * 3
        if user_data[uid]["active"] > 10:
            weight *= 2
        weight_pool.extend([uid] * int(weight))
    winner_uid = random.choice(weight_pool)
    winner = await context.bot.get_chat_member(chat.id, winner_uid)
    await update.message.reply_text(
        f"🎊 恭喜 {winner.user.mention_html()} 成功瓜分大奖！",
        parse_mode="HTML"
    )

# 全局消息分发
async def message_handler(update: Update, context):
    global bot_active
    text = update.message.text.strip()
    uid = update.effective_user.id
    await power_on(update)
    if not bot_active:
        return
    init_user(uid)
    user_data[uid]["active"] += 1
    user_data[uid]["is_vip"] = check_plane_vip(update.effective_user)

    if text == "个人中心":
        await my_center(update)
    elif text == "邀请赚钱":
        await update.message.reply_text("🔗 邀请活跃飞机会员进群，每成功1人随机获得 0.1~1 USDT，邀请越多抽奖中奖概率越高！")
    elif text == "提现USDT":
        if user_data[uid]["balance"] < 1:
            await update.message.reply_text("❌ 余额不足1USDT，暂时无法发起提现")
        else:
            await update.message.reply_text("✅ 提现申请已提交，请等待管理员审核处理")

# 程序入口
def main():
    print("🤖 机器人启动中...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(CommandHandler("抽奖", lottery_draw))
    app.run_polling()

if __name__ == "__main__":
    main()