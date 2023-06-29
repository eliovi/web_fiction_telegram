# web_fiction_telegram
A simple script to check for new chapters for stories on RoyalRoad and send message to the user on telegram for every new chapter. The user can choose to follow multiple stories.

## Usage
The user needs to define the required novels in novel_list.py.
The script saves the last seen chapter on chapter_list.txt. 
If a new chapter is seen, the script sends a telegram message to the user. 


A github actions workflow is defined to run this script according to a cron schedule. 

You must define in the repository secrets the telegram bot token under TOKEN, and the user chat message id under CHAT_ID (If you run the script manually, define these arguments by setting environmnet variables)
