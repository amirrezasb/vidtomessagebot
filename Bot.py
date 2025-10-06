import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# --- فقط توکن ربات خود را اینجا وارد کنید ---
TOKEN = "8296716466:AAHEX-JkyHBO3HIY4W2KCBAl_SS489wZEjM"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('سلام! لطفا یک ویدیو بفرستید تا آن را به ویدیو مسیج تبدیل کنم. (نسخه نهایی و قطعی)')

def convert_to_video_note(update: Update, context: CallbackContext) -> None:
    """Downloads the video and sends it back as a video note."""
    message = update.message
    if message.video:
        try:
            waiting_message = message.reply_text('لطفا کمی صبر کنید، در حال دانلود و تبدیل ویدیو...')

            # Get the file object
            video_file = context.bot.get_file(message.video.file_id)

            # Download the video to a temporary path
            temp_video_path = f"{message.video.file_id}.mp4"
            video_file.download(temp_video_path)

            # Get video dimensions for the video note
            dimension = min(message.video.width, message.video.height)

            # Open the downloaded file and send it as a video note
            with open(temp_video_path, 'rb') as video_stream:
                context.bot.send_video_note(
                    chat_id=message.chat_id,
                    video_note=video_stream,
                    duration=message.video.duration,
                    length=dimension,
                    reply_to_message_id=message.message_id
                )

            # Delete the waiting message
            context.bot.delete_message(chat_id=message.chat_id, message_id=waiting_message.message_id)

            # Clean up the downloaded file
            os.remove(temp_video_path)

        except Exception as e:
            logger.error(f"Error processing video: {e}")
            message.reply_text(f'متاسفم، مشکلی پیش آمد: {e}')
    else:
        message.reply_text('این یک ویدیو نیست.')

def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.video, convert_to_video_note))
    logger.info("Bot started successfully!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
