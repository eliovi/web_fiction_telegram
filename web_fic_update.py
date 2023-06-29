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


TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']


def get_fic_update():
    # a list of the novel links
    novel_links = {}
    for novel_id in novels:
        link = 'https://www.royalroad.com/fiction/{0}'.format(novel_id)
        novel_links[novel_id] = link

    # a list of all the responses obtained from opening the links
    responses = {}
    for novel_id in novel_links:
        response = requests.get(novel_links[novel_id], timeout=3)
        responses[novel_id] = response

    # a list of the contents obtained from accessing each response
    contents = {}
    for novel_id in responses:
        content = BeautifulSoup(responses[novel_id].content, "html.parser")
        contents[novel_id] = content

    # storing the latest chapter name for each novel ID
    latest = {}
    for novel_id in contents:
        chapters = ['']
        for tag in contents[novel_id].find_all(style="cursor: pointer"):
            for tag_2 in tag.find('td'):
                chapters.append(tag_2)
        length = len(chapters)
        latest[novel_id] = chapters[length-2]['href']

    # reading the previous links stored in file
    chap_file = open('chapter_list.txt', 'r')
    previous = chap_file.read().splitlines()
    chap_file.close()

    i = 0
    message_list = []
    for i, novel_id in enumerate(latest):
        try:
            if previous[i] != latest[novel_id]:
                text = 'https://www.royalroad.com' + latest[novel_id]
                subject = 'New chapter for {0}'.format(novels[novel_id])
                print(subject)
                print(text)
                message = subject + '\n' + text
            else:
                message = f'No new chapter for {novels[novel_id]} )-:'
            i += 1
        except:
            print('No previous record of {0}. New record created'.format(novels[novel_id]))
            message = f'No previous record of {novels[novel_id]}. New record created'
        message_list.append(message)

    # overriding the previous file to store the latest chapter links
    chap_file = open('chapter_list.txt', 'w')
    for novel_id in latest:
        chap_file.write(latest[novel_id]+'\n')
    chap_file.close()
    return message_list


async def send_message_to_user_now_direct(bot):
    message_list = get_fic_update()
    for message in message_list:
        if 'No new chapter' in message:
            continue
        await bot.send_message(chat_id=CHAT_ID, text=message)


async def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    await send_message_to_user_now_direct(application.bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

