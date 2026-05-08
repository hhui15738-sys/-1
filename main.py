from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import random

# ============ 你的专属配置 ============
BOT_TOKEN = "在这里填你的机器人TOKEN"
MASTER_ID = 8684151999
START_TEXT = "✅ 空投机器人已成功开启，邀请赚USDT、抽奖功能上线🎯"

# 邀请奖励 金额+概率
INVITE_REWARD = [
    {"amount":0.1, "rate":40},
    {"amount":0.3, "rate":30},
    {"amount":0.6, "rate":20},
    {"amount":1.0, "rate":10},
]
MIN_LOTTERY = 100
MIN_RED = 50
POOL = 1025
# =====================================

bot_on = False
user_db = {}

menu = [
    [KeyboardButton("个人中心"), KeyboardButton("邀请赚钱")],
    [KeyboardButton("提现USDT"), KeyboardButton("排行榜")]
]
keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)

def init_user(uid):
    if uid not in user_db:
        user_db[uid] = {
            "balance":8.00, "airdrop":0.00,
            "invite":0, "active":0, "plane":False
        }

def check_plane(user):
    txt = (user.full_name + (user.username or "")).lower()
    return any(tag in txt for tag in ["✈","飞机","✈️","plane"])

def get_random_money():
    pool = []
    for item in INVITE_REWARD:
        pool += [item['amount']] * item['rate']
    return round(random.choice(pool),2)

async def turn_on(update:Update):
    global bot_on
    uid = update.effective_user.id
    if uid == MASTER_ID and update.message.text.strip() == "开启":
        bot_on = True
        await update.message.reply_text(START_TEXT, reply_markup=keyboard)

async def user_center(update:Update):
    uid = update.effective_user.id
    u = update.effective_user
    init_user(uid)
    d = user_db[uid]
    plane_tag = "✅ 飞机会员" if d['plane'] else "❌ 普通用户"
    text = f"""
🤖 空投机器
昵称：{u.full_name}
ID：{uid}
余额：{d['balance']:.2f} USDT
空投余额：{d['airdrop']:.2f} USDT
已邀请：{d['invite']} 人
身份：{plane_tag}

🔥 全局奖池：{POOL}.00 USDT
"""
    await update.message.reply_text(text)

async def lottery(update:Update, ctx):
    if not bot_on:
        return
    chat = update.effective_chat
    members = await ctx.bot.get_chat_members(chat.id)
    valid = []
    for m in members:
        if m.user.is_bot:
            continue
        uid = m.user.id
        init_user(uid)
        user_db[uid]['plane'] = check_plane(m.user)
        if user_db[uid]['plane'] and user_db[uid]['invite'] >= MIN_LOTTERY:
            valid.append(uid)
    if not va...