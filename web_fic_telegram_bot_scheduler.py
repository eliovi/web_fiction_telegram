import asyncio

import pytz
from novel_list import novels
from bs4 import BeautifulSoup
import requests
from telegram.ext import CallbackContext, JobQueue, CommandHandler
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from datetime import datetime, time, timedelta
import os
from web_fic_update import get_fic_update

TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']


# Function to send a message to a specific user
async def send_message_to_user(data):
    message_list = get_fic_update()
    for message in message_list:
        if 'No new chapter' in message:
            continue
        await data.bot.send_message(chat_id=CHAT_ID, text=message)


async def send_message_to_user_now(update: Update, context: CallbackContext):
    message_list = get_fic_update()
    for message in message_list:
        await update.message.reply_text(text=message)


def schedule_daily_messages(job_queue: JobQueue, bot):
    job_queue.run_daily(
        send_message_to_user,
        time(hour=11, minute=32, tzinfo=pytz.timezone('Asia/Jerusalem')),
        data=bot,
        days=(0, 1, 2, 3, 4, 5),  # Sunday to Friday
        name=str(CHAT_ID),
    )


async def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Schedule daily messages for user
    schedule_daily_messages(application.job_queue, application.bot)

    application.add_handler(CommandHandler("check", send_message_to_user_now))

    # # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

