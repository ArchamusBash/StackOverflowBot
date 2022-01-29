import telebot
import os
import requests

from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

#bot API token and other stuff
API = os.getenv("API")
channel = os.getenv("CHANNEL")
admin = os.getenv("ADMIN")

#log file
file = open("logs.txt", "w+", encoding=" utf-8").read()

#bot object initialization
bot = telebot.TeleBot(API)

#/start command greet
@bot.message_handler(commands=["start"])
def Start(message):
    """
    bot.send_message(message.chat.id, "Welcome! I will help you find questions and answers in StackOverflow! Put @FStackOverflowBot in command line I will show you the results accordingly.")
    """
    bot.send_message(message.chat.id, "Welcome! This bot is currently under development.")

#/trending command
@bot.message_handler(commands=["trending"])
def Trending(message):
    try:
        url = "https://stackoverflow.com/questions/"
        stack = requests.get(url)
        soup = BeautifulSoup(stack.text, 'html.parser')
        trending = soup.find("a", {'class': 'question-hyperlink', 'href': True}).extract()
        #Block telegram api escape
        title = trending.text.replace("=", "\\=").replace("-", "\\-").replace("+", "\\+")
        bot.send_message(message.chat.id, f"{title}\n [See more](https://stackoverflow.com/{trending['href']})", parse_mode='MarkdownV2')
    except Exception as err: print(f"Error: {err}")

#/info command
@bot.message_handler(commands=["info"])
def Info(message):
    bot.send_message(message.chat.id, "Date Created: 24/01/2022\nThis is a project designed to the dev community in Telegram\nIf you want to contribute, feel free to fork the project on [GitHub](https://github.com/BriggsK/StackOverflowBot)", parse_mode="MarkdownV2")

#/admin command
@bot.message_handler(commands=["admin"])
def Admin(message):
    adm = bot.send_message(message.chat.id, "Enter feedback or bug. Suggestions are welcome.")
    bot.register_next_step_handler(adm, Send)
#forward message to channel admin
def Send(message):
    bot.send_message(message.chat.id, "Thank you for your feedback!")
    bot.forward_message(channel, message.chat.id, message.id)

#TODO: /cancel command
@bot.callback_query_handler(func=lambda call: True)
def Cancel(call):
    return

#TODO: /search command
@bot.message_handler(commands=["search"])
def Search(message):
    return

#logger for "most used time of the day"
@bot.message_handler(func=lambda m: True)
def Logger(message):
    now = datetime.now()
    time = now.strftime(str(f"%H:%M:%S"))
    file = open("logs.txt", "w+", encoding="utf-8")
    file.write(str("| Last Connection: " + time + " |"))
    file.write("\n")
    file.close()
    
#send logs to admin
@bot.message_handler(commands=["sudo"])
def Sudo(message):
    filesend = open("logs.txt", "w+", encoding="utf-8")
    bot.send_document(admin, filesend, "logs.txt")
    bot.send_message(admin, "Logs sent!")
    filesend.close()


def main():    
    bot.polling() #waiting for messages

if __name__ == '__main__':
    main() 
