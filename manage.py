#!/usr/bin/env python
import requests,telebot,flask
from telebot import types
from flask import Flask
from threading import Thread
import random


app = Flask('')

@app.route('/')
def home():
	return 'I am tofe x - Running'

def run():
  app.run(
		host='0.0.0.0',
		port=random.randint(2000,9000)
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()
status__new = "✅"
status__ch = "✅"
ch_sta = True
new_member = True
channel = "py_iq" # channel username without @  /  @ يوزر القناة بدون 
bot = telebot.TeleBot("5427304351:AAEUwt_Q86zScdQH2KST2nFvRweSjuVd07U")

keep_alive()
@bot.message_handler(commands=['start'])
def send_tool(message):
        k = open("admins.txt","r").read()
        new_mem_ch = open("users.txt","r").read()
        m = bot.get_chat_member(f"@{channel}",message.from_user.id).status
        if ch_sta == True:
                if str(message.chat.id) in str(k) or str(m) == str("creator") or str(m) == str("administrator"):
                    bot.send_message(message.chat.id,"HELLO SIR ! send /admin") #رسالة الادمن
                elif bot.get_chat_member(f"@{channel}",message.from_user.id).status == "member" and new_member != True:
                    if str(message.chat.id) in new_mem_ch:
                        bot.send_message(message.chat.id,"hello man") # ثاني رسالة للمستخدم
                    else:
                        with open("users.txt","a") as new: new.write(f"{message.chat.id}\n")
                        new.close()
                        bot.send_message(message.chat.id,"hello man") # اول رسالة للمستخدم
                elif bot.get_chat_member(f"@{channel}",message.from_user.id).status == "member" and new_member == True:
                    if str(message.chat.id) in new_mem_ch and new_member == True:
                        bot.send_message(message.chat.id,"hello man")
                    elif str(message.from_user.id) not in new_mem_ch:
                        with open("users.txt","a") as new: new.write(f"{message.chat.id}\n")
                        new.close()
                        bot.send_message(message.chat.id,"hello man")
                        for x in open("admins.txt","r").readlines():
                            bot.send_message(x,f"new member\n-------------\nname : {message.from_user.first_name}\nid : {message.from_user.id}")
                elif bot.get_chat_member(f"@{channel}",message.from_user.id).status == "left":
                    bot.send_message(message.chat.id,f"channel : @{channel}") # رسالة الاشتراك الاجباري
                else: 
                    bot.send_message(message.chat.id,f"channel : @{channel}") # رسالة الاشتراك الاجباري
        elif ch_sta == False:
                if str(message.chat.id) in str(new_mem_ch):
                    bot.send_message(message.chat.id,"hello") # ثاني رسالة للمستخدم
                elif str(message.chat.id) not in str(new_mem_ch) and new_member == False:
                    with open("users.txt","a") as new: new.write(f"{message.chat.id}\n")
                    new.close()
                    bot.send_message(message.chat.id,"hello") # اول رسالة للمستخدم
                elif str(message.chat.id) not in str(new_mem_ch) and new_member == True:
                    with open("users.txt","a") as new: new.write(f"{message.chat.id}\n")
                    new.close()
                    for x in open("admins.txt","r").readlines():
                        bot.send_message(x,f"new member\n-------------\nname : {message.from_user.first_name}\nid : {message.from_user.id}")
                    bot.send_message(message.chat.id,"hello") # ثاني رسالة للمستخدم
@bot.message_handler(commands=['admin'])
def send_tool(message):
    global ch_sta,new_member,status__bott
    keyo = types.InlineKeyboardMarkup(row_width =	1)
    itembtn1 = types.InlineKeyboardButton('تفعيل الاشتراك الاجباري', callback_data="start_ch")
    itembtn2 = types.InlineKeyboardButton('تعطيل الاشتراك الاجباري',callback_data="stop_ch")
    itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
    itembtn4 = types.InlineKeyboardButton('تعطيل تنبيه الدخول',callback_data="stop_m")
    status_new = types.InlineKeyboardButton(f'حالة تنبيه الدخول : {status__new}',callback_data="a123fsac")
    status_ch = types.InlineKeyboardButton(f'حالة الاشتراك الاجباري {status__ch}',callback_data="ae1e")
    itembtn5 = types.InlineKeyboardButton('أرسال نسخة احتياطية',callback_data="send_users")
    itembtn6 = types.InlineKeyboardButton('اذاعة',callback_data="send_all")
    keyo.add(itembtn1,itembtn2,status_ch,itembtn3,itembtn4,status_new,itembtn5,itembtn6)
    ch_admin = open("admins.txt","r").read()
    if str(message.from_user.id) in ch_admin: 
         bot.send_message(message.chat.id, "- admin 💳 " , reply_markup = keyo)
@bot.callback_query_handler(func=lambda call: True )
def answer(call):
    global ch_sta,new_member,status__ch,status__new,status__bott
    ch_admin = ch_admin = open("admins.txt","r").read()
    try: 
        if call.data == 'stop_ch' and str(call.message.chat.id) in ch_admin:
            ch_sta = False
            status__ch = "❌"
            keyoo = types.InlineKeyboardMarkup(row_width =	1)
            itembtn1 = types.InlineKeyboardButton('تفعيل الاشتراك الاجباري', callback_data="start_ch")
            itembtn2 = types.InlineKeyboardButton('تعطيل الاشتراك الاجباري',callback_data="stop_ch")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn4 = types.InlineKeyboardButton('تعطيل تنبيه الدخول',callback_data="stop_m")
            status_new = types.InlineKeyboardButton(f'حالة تنبيه الدخول : {status__new}',callback_data="adasd2134dc")
            status_ch = types.InlineKeyboardButton(f'حالة الاشتراك الاجباري {status__ch}',callback_data="aqwe12ed")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn5 = types.InlineKeyboardButton('أرسال نسخة احتياطية',callback_data="send_users")
            itembtn6 = types.InlineKeyboardButton('اذاعة',callback_data="send_all")
            keyoo.add(itembtn1,itembtn2,status_ch,itembtn3,itembtn4,status_new,itembtn5,itembtn6)
            bot.edit_message_text(chat_id=call.message.chat.id,text="- admin 💳 ",message_id=call.message.message_id,reply_markup=keyoo)
    except:
        pass
    try :
        if call.data == 'start_ch' and str(call.message.chat.id) in ch_admin:
            ch_sta = True
            status__ch = "✅"
            keyooo = types.InlineKeyboardMarkup(row_width =	1)
            itembtn1 = types.InlineKeyboardButton('تفعيل الاشتراك الاجباري', callback_data="start_ch")
            itembtn2 = types.InlineKeyboardButton('تعطيل الاشتراك الاجباري',callback_data="stop_ch")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn4 = types.InlineKeyboardButton('تعطيل تنبيه الدخول',callback_data="stop_m")
            status_new = types.InlineKeyboardButton(f'حالة تنبيه الدخول : {status__new}',callback_data="mu1st3af4a")
            status_ch = types.InlineKeyboardButton(f'حالة الاشتراك الاجباري {status__ch}',callback_data="asasdofeq213")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn5 = types.InlineKeyboardButton('أرسال نسخة احتياطية',callback_data="send_users")
            itembtn6 = types.InlineKeyboardButton('اذاعة',callback_data="send_all")
            keyooo.add(itembtn1,itembtn2,status_ch,itembtn3,itembtn4,status_new,itembtn5,itembtn6)
            bot.edit_message_text(chat_id=call.message.chat.id,text="- admin 💳 ",message_id=call.message.message_id,reply_markup=keyooo)
    except : pass
    try:
        if call.data == 'start_m' and str(call.message.chat.id) in ch_admin:
            new_member = True
            status__new = "✅"
            keyooo = types.InlineKeyboardMarkup(row_width =	1)
            itembtn1 = types.InlineKeyboardButton('تفعيل الاشتراك الاجباري', callback_data="start_ch")
            itembtn2 = types.InlineKeyboardButton('تعطيل الاشتراك الاجباري',callback_data="stop_ch")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn4 = types.InlineKeyboardButton('تعطيل تنبيه الدخول',callback_data="stop_m")
            status_new = types.InlineKeyboardButton(f'حالة تنبيه الدخول : {status__new}',callback_data="aasd543")
            status_ch = types.InlineKeyboardButton(f'حالة الاشتراك الاجباري {status__ch}',callback_data="amc9d")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn5 = types.InlineKeyboardButton('أرسال نسخة احتياطية',callback_data="send_users")
            itembtn6 = types.InlineKeyboardButton('اذاعة',callback_data="send_all")
            keyooo.add(itembtn1,itembtn2,status_ch,itembtn3,itembtn4,status_new,itembtn5,itembtn6)
            bot.edit_message_text(chat_id=call.message.chat.id,text="- admin 💳 ",message_id=call.message.message_id,reply_markup=keyooo)
    except: pass
    try:
        if call.data == 'stop_m' and str(call.message.chat.id) in ch_admin:
            new_member = False
            status__new = "❌"
            keyooo = types.InlineKeyboardMarkup(row_width =	1)
            itembtn1 = types.InlineKeyboardButton('تفعيل الاشتراك الاجباري', callback_data="start_ch")
            itembtn2 = types.InlineKeyboardButton('تعطيل الاشتراك الاجباري',callback_data="stop_ch")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn4 = types.InlineKeyboardButton('تعطيل تنبيه الدخول',callback_data="stop_m")
            status_new = types.InlineKeyboardButton(f'حالة تنبيه الدخول : {status__new}',callback_data="aqwed22")
            status_ch = types.InlineKeyboardButton(f'حالة الاشتراك الاجباري {status__ch}',callback_data="a123dq")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn5 = types.InlineKeyboardButton('أرسال نسخة احتياطية',callback_data="send_users")
            itembtn6 = types.InlineKeyboardButton('اذاعة',callback_data="send_all")
            keyooo.add(itembtn1,itembtn2,status_ch,itembtn3,itembtn4,status_new,itembtn5,itembtn6)
            bot.edit_message_text(chat_id=call.message.chat.id,text="- admin 💳 ",message_id=call.message.message_id,reply_markup=keyooo)
    except: pass
    try:
        if call.data == "send_users" and str(call.message.chat.id) in ch_admin:
            bot.send_document(chat_id=call.message.chat.id,data =open("users.txt","rb"),caption="تم انشاء نسخة احتياطية")
            keyoooo = types.InlineKeyboardMarkup(row_width =	1)
            itembtn1 = types.InlineKeyboardButton('تفعيل الاشتراك الاجباري', callback_data="start_ch")
            itembtn2 = types.InlineKeyboardButton('تعطيل الاشتراك الاجباري',callback_data="stop_ch")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn4 = types.InlineKeyboardButton('تعطيل تنبيه الدخول',callback_data="stop_m")
            status_new = types.InlineKeyboardButton(f'حالة تنبيه الدخول : {status__new}',callback_data="aadsf")
            status_ch = types.InlineKeyboardButton(f'حالة الاشتراك الاجباري {status__ch}',callback_data="a3gw")
            itembtn3 = types.InlineKeyboardButton('تفعيل تنبيه الدخول',callback_data="start_m")
            itembtn5 = types.InlineKeyboardButton('أرسال نسخة احتياطية',callback_data="send_users")
            itembtn6 = types.InlineKeyboardButton('اذاعة',callback_data="send_all")
            keyoooo.add(itembtn1,itembtn2,status_ch,itembtn3,itembtn4,status_new,itembtn5,itembtn6)
            bot.edit_message_text(chat_id=call.message.chat.id,text="- admin 💳 ",message_id=call.message.message_id,reply_markup=keyoooo)
    except: pass
    try:
        if call.data == "send_all" and str(call.message.chat.id) in ch_admin: 
            bot.send_message(call.message.chat.id,"أرسل `اذاعة`",parse_mode="MARKDOWN")
    except: pass
@bot.message_handler(func=(lambda message: True))#Tofe_x #trprogram
def handle_text(message):
    if message.text == "اذاعة":
        cid = message.chat.id
        msgPrice = bot.send_message(cid, 'أرسل الرسالة لأقوم بأرسالها للمستخدمين')
        bot.register_next_step_handler(msgPrice , step_Set_Price)
def step_Set_Price(message):
    cid = message.chat.id
    msg_bod= message.text
    for x in open("users.txt","r").readlines():
        try:
            bot.send_message(x,msg_bod)
        except:
            pass
bot.polling(none_stop=True)