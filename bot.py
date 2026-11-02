import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Bot tokeningizni shu yerga yozing
BOT_TOKEN = "9176290858:AAHqWelGkamtdmFkrcMPFnx-fxxaLtW3Q4w"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

# Eslatma yuboruvchi funksiya
async def send_remind(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=f"⏰ **Eslatma:**\n{text}", parse_mode="Markdown")

# Toq kunlar (Dushanba, Chorshanba, Juma) uchun eslatmalarni o'rnatish funksiyasi
def setup_odd_days_reminders(chat_id: int):
    # Yakshanba olib tashlandi, faqat: Dushanba, Chorshanba, Juma
    days = 'mon,wed,fri'

    # 1. Soat 06:20 - Ibodat qilish
    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=6,
        minute=20,
        args=[chat_id, "🌅 Ertalabki ibodat vaqti bo'ldi!"]
    )

    # 2. Soat 13:20 - Ibodat qilish
    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=13,
        minute=20,
        args=[chat_id, "☀️ Kunduzgi ibodat vaqti bo'ldi!"]
    )

    # 3. Soat 20:30 - Trenirovka (yarim soat)
    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=20,
        minute=30,
        args=[chat_id, "💪 Trenirovka vaqti! Yarim soat faol harakat qilamiz."]
    )

    # 4. Soat 21:00 - Uxlash
    scheduler.add_job(
        send_remind,
        trigger="cron",
        day_of_week=days,
        hour=21,
        minute=0,
        args=[chat_id, "🌙 Kech bo'ldi, uxlash vaqti keldi. Marhamat, dam oling!"]
    )

# /start komandasi
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

async def main():
    scheduler.start()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())