import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

# TOKENGIZNI TO'G'RIDAN-TO'G'RI QO'SHTIRNOQ ICHIGA YOZING:
BOT_TOKEN = "9176290858:AAHqWelGkamtdmFkrcMPFnx-fxxaLtW3Q4w"  # O'z tokeningizni yozing

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

# Eslatma yuboruvchi funksiya
async def send_remind(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=f"⏰ **Eslatma:**\n{text}", parse_mode="Markdown")

# Toq kunlar (Dushanba, Chorshanba, Juma) uchun eslatmalar
def setup_odd_days_reminders(chat_id: int):
    days = 'mon,wed,fri'

    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=6,
        minute=20,
        args=[chat_id, "🌅 Ertalabki ibodat vaqti bo'ldi!"]
    )
    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=13,
        minute=20,
        args=[chat_id, "☀️ Kunduzgi ibodat vaqti bo'ldi!"]
    )
    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=20,
        minute=30,
        args=[chat_id, "💪 Trenirovka vaqti! Yarim soat faol harakat qilamiz."]
    )
    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=21,
        minute=0,
        args=[chat_id, "🌙 Kech bo'ldi, uxlash vaqti keldi. Marhamat, dam oling!"]
    )

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    setup_odd_days_reminders(message.chat.id)
    await message.answer(
        "👋 Assalomu alaykum! Sizning **Dushanba, Chorshanba, Juma** kunlari uchun rejangiz muvaffaqiyatli ulandi:\n\n"
        "📿 **06:20** — Ibodat qilish\n"
        "📿 **13:20** — Ibodat qilish\n"
        "🏋️‍♂️ **20:30** — Trenirovka (30 minut)\n"
        "🛌 **21:00** — Uxlash\n\n"
        "Belgilangan vaqtlarda o'zim sizga eslatib turaman!",
        parse_mode="Markdown"
    )

# Render veb-serveri uchun kichik handler (Portni band qilish uchun)
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render taqdim etadigan PORT raqamini olamiz
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    scheduler.start()
    # Veb-serverni ishga tushiramiz (Render talabi)
    await start_web_server()
    # Botni ishga tushiramiz
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())