import telebot
import os
#I will leave it the way it is for now, im tired

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

bot.polling()
