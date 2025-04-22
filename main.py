import os
import json
import datetime
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("❌ Переменная окружения TELEGRAM_TOKEN не найдена. Убедись, что она задана!")
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Загрузка плана
with open("daily_plan.json", "r", encoding="utf-8") as f:
    study_plan = json.load(f)

def get_today_task():
    day = (datetime.date.today() - datetime.date.fromisoformat(study_plan["start_date"])).days + 1
    if 1 <= day <= 14:
        return f"📅 *День {day}*\n" + study_plan["days"].get(str(day), "Нет задания на сегодня.")
    return "🎉 Обучение завершено! Поздравляю!"

def start(update, context):
    update.message.reply_text("Привет! Я твой помощник по Power BI. Напиши /день, чтобы получить задание на сегодня ✨")

def day(update, context):
    update.message.reply_markdown(get_today_task())

def help_command(update, context):
    update.message.reply_text("""Команды:
/день — задание на сегодня
/помощь — помощь
/совет — случайный совет""")

def tip(update, context):
    update.message.reply_text("💡 Совет: Не забывай сохранять отчет перед публикацией в Power BI Service!")

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("день", day))
    dispatcher.add_handler(CommandHandler("помощь", help_command))
    dispatcher.add_handler(CommandHandler("совет", tip))
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Power BI bot is running"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
