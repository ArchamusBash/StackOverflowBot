import telebot
import os
import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
#bot API token and other stuff
API = os.getenv("API")

#bot object initialization
bot = telebot.TeleBot(API)

#/start command greet
@bot.message_handler(commands=["start"])
def Start(message):
    bot.send_message(message.chat.id, "Welcome! I will help you find questions and answers in StackOverflow! Put @FStackOverflowBot in command line I will show you the results accordingly.")

#Inline query
@bot.inline_handler(lambda query: query.query == "text")
def Inline(inline_query):
    return

#
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

def main():    
    bot.polling() #waiting for messages

if __name__ == '__main__':
    main() 
