import telebot
import os

# --- فقط توکن ربات خود را اینجا وارد کنید ---
TOKEN = "8296716466:AAHEX-JkyHBO3HIY4W2KCBAl_SS489wZEjM"

bot = telebot.TeleBot(TOKEN)
print("Bot started successfully with pyTelegramBotAPI!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! لطفا یک ویدیو برای من بفرستید تا آن را به ویدیو مسیج تبدیل کنم. (نسخه نهایی و قطعی)")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        # Send a waiting message
        waiting_message = bot.reply_to(message, "لطفا کمی صبر کنید، در حال تبدیل ویدیو...")

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the video to a temporary file
        temp_video_path = f"{message.video.file_id}.mp4"
        with open(temp_video_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Open the saved file and send it as a video note
        with open(temp_video_path, 'rb') as video_note:
            bot.send_video_note(message.chat.id, video_note, reply_to_message_id=message.message_id)

        # Delete the waiting message
        bot.delete_message(message.chat.id, waiting_message.message_id)

        # Clean up the temporary file
        os.remove(temp_video_path)

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"متاسفم، مشکلی پیش آمد: {e}")

# Start listening for messages
bot.polling()
