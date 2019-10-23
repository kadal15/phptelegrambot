import os
import telebot
from flask import Flask, request

TOKEN = '<BOT TOKEN>'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

def sendmsg(message,text):
    bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['start'])
def startmsg(message):
    bot.send_message(message.chat.id,'<b>Selamat Datang Di Jejaka Bot Telgram</b>\nSIlahkan Ketikkan <b>Hello</b> Dan dapatkan Balasan Dari Bot Ini',parse_mode='HTML')

@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
    if 'Hello' in message.text.lower():
        sendmsg(message,'Hai, {} Semoga Hari Mu Menyenangkan'.format(message.from_user.first_name))
    elif 'hello' in message.text.lower():
        sendmsg(message, 'Hai, {} Semoga Hari Mu Menyenangkan'.format(message.from_user.first_name))

#bagian server
@server.route('/' + TOKEN,methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return 'ok webhook sudah terpasang !', 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='<HEROKU APP HOST>'+TOKEN)
    return 'ok webhook sudah terpasang !', 200

if __name__ == '__main__':
    server.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))
