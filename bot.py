#pip install pytelegrambotapi
#pip install telebot

import telebot;

bot = telebot.TeleBot('1006907723:AAFhNie7MF5x9Qevmm7qvhJWLc_p7X1Jx1E');
command = []

# заполнение словаря - надо переделать в функцию
#file = open("D:\input@.txt",encoding="utf-8")
#onstring = file.read().split("\n")[:-1]
#dict = dict()
#for item in onstring:
#    key = item.split("\t")[0]
#    value = item.split("\t")[1:]
#    dict[key] = value
#file.close()
#print(dict)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    command = message.text.split(' ')
    # print(command)
    if (command[0] == "/find"):
        bot.send_message(message.from_user.id, "Запрос на поиск таксюгана по имени "+command[1]+' '+command[2])
        #проверка словаря на попадание запроса - переделать в функцию
        #pk=(command[1]+' '+command[2])
        pk=(command[1]+' '+command[2]).lower()
        #print('-->',pk)
        for key in dict.keys():
            #print(key)
            if key==pk:
                '''for i in dict:
                    str+=dict[i]
                print('-->',dict[key],str)'''
                str=' '.join(dict.get(key))
                bot.send_message(message.from_user.id,str)
                bot.send_photo(message.from_user.id, 'https://cstor.nn2.ru/forum/data/forum/images/2013-04/65753705-driving-licence.jpg')






    elif message.text == "Привет":

        bot.send_message(message.from_user.id, "Привет! Лузеры")

    elif message.text == "/start":

        bot.send_message(message.from_user.id, 'Ну что поболтаем, застранцы')

    elif message.text == "/minenko":

        bot.send_message(message.from_user.id, 'ЭТО липкий тип!')
        # bot.send_video(message.from_user.id,data='http://www.youtube.com/watch?v=idOhGHwNRjI')


    elif message.text == "/privar":

        bot.send_message(message.from_user.id, 'ЭТО лысый тип!')

    elif message.text == "/ponomarev":

        bot.send_message(message.from_user.id, 'ЭТО совратитель ****** тип!')
        bot.send_contact(message.from_user.id, phone_number=89280427565, first_name='Ponomarev',
                         last_name='Vova')
        bot.send_photo(message.from_user.id,
                       photo='https://trikky.ru/wp-content/blogs.dir/1/files/2020/07/10/2020-07-10-09-51-49.jpg')

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "список команд:\n"
                                               "/minenko\n"
                                               "/privar\n"
                                               "/ponomarev\n"
                                               )
    elif message.text == "/find":

        bot.send_message(message.from_user.id, 'Болше параметров>')


    else:

        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

    print('поступила команда:', message.text, 'от', message.from_user.first_name, message.from_user.last_name,
          message.from_user.id)


bot.polling(none_stop=True, interval=0)
