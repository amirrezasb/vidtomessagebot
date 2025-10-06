import os
import asyncio
from telethon import TelegramClient, events

# --- از این مقادیر عمومی استفاده می‌کنیم ---
# این مقادیر برای دور زدن خطای ساخت اپلیکیشن تلگرام است.
API_ID = 21724  # API ID عمومی برای اپلیکیشن دسکتاپ تلگرام
API_HASH = '3e03d13b31354f9d747a48c5a242f310'  # API Hash عمومی

# --- این خط مهم‌ترین بخش است! ---
# فقط توکن ربات خود را که از BotFather گرفته‌اید، در اینجا وارد کنید.
BOT_TOKEN = '8296716466:AAHEX-JkyHBO3HIY4W2KCBAl_SS489wZEjM' # اینجا توکن ربات خود را وارد کنید

# ایجاد یک کلاینت تلگرام
bot = TelegramClient('bot_session', API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.reply('سلام! لطفا یک ویدیو برای من بفرستید تا آن را به ویدیو مسیج (دایره‌ای) تبدیل کنم. (نسخه نهایی و قطعی)')

@bot.on(events.NewMessage(func=lambda e: e.video))
async def video_handler(event):
    """Handles video messages and converts them to video notes."""
    try:
        waiting_message = await event.reply('لطفا کمی صبر کنید، در حال تبدیل ویدیو...')
        video_path = await event.download_media()
        await bot.send_file(
            event.chat_id,
            video_path,
            video_note=True, # این کلید جادویی است!
            reply_to=event.id
        )
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
        await waiting_message.delete()
    except Exception as e:
        print(f"Error: {e}")
        await event.reply('متاسفم، در هنگام تبدیل ویدیو مشکلی پیش آمد. لطفاً دوباره تلاش کنید.')

async def main():
    """Start the bot."""
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot started successfully with Telethon!")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
