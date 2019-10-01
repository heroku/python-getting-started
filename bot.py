import telebot
import random

bot = telebot.TeleBot('977550028:AAHAAWBOo1J9x3Db6MWiufcZzjkviU8rM0g')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Start')
#keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, этот бот создан для выведения рандомного числа', reply_markup=keyboard1)
 
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'start':
        bot.send_message(message.chat.id, 'Введите числа в пределах которых будет осуществляться нахождение рандомного числа')
        bot.send_message(message.chat.id, 'Введите сначало первое число-"граница"')
        def send_text(message):
            while message.text == int:
                a=message.text
                bot.send_message(message.chat.id, 'Теперь введите второе число-"граница"')               
                def send_text(message):
                    while message.text.lower() == int:
                        b=message.text
                        bot.send_message(message.chat.id, 'Рандомное число это...')
                        r=random.randint(a, b)
                        bot.send_message(message.chat.id, r)
                    else:
                        bot.send_message(message.chat.id, "Введите число!")
            else:
                bot.send_message(message.chat.id, "Введите число!")
                 
                
bot.polling()
