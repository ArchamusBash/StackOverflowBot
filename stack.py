import telebot
import os

#bot API token and other stuff
API = "5137897681:AAGNSIgRqLbD0gvzNgvcJVviE9SVxJerNOs"
#admin =
#channel =
arr = ["APPLE", "HOME", "ANON"]
#bot object initialization
bot = telebot.TeleBot(API)

#/start command greet
@bot.message_handler(commands=["start"])
def Start(message):
    bot.send_message(message.chat.id, "Welcome! I will help you find questions and answers in StackOverflow! Put @FStackOverflowBot in command line I will show you the results accordingly.")

@bot.inline_handler(lambda query: query.query == arr)
def Inline(inline_query):
    print(True)


bot.polling()
