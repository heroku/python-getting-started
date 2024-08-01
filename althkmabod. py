
import zipfile
import os
try:
    from telethon.sessions import StringSession
    import asyncio, re, json, shutil
    from kvsqlite.sync import Client as uu
    from telethon.tl.types import KeyboardButtonUrl
    from telethon.tl.types import KeyboardButton, ReplyInlineMarkup
    from telethon import TelegramClient, events, functions, types, Button
    from telethon.tl.types import DocumentAttributeFilename
    from plugins.converter import MangSession
    import time, datetime, random 
    from datetime import timedelta
    from telethon.errors import (
        ApiIdInvalidError,
        PhoneNumberInvalidError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        SessionPasswordNeededError,
        PasswordHashInvalidError
    )
    from plugins import *
    from plugins.messages import *
    from plugins.get_gift import *
except:
    os.system("pip install telethon kvsqlite")
    try:
        from telethon.sessions import StringSession
        import asyncio, re, json, shutil
        from kvsqlite.sync import Client as uu
        from telethon.tl.types import KeyboardButtonUrl
        from telethon.tl.types import KeyboardButton
        from telethon import TelegramClient, events, functions, types, Button
        from telethon.tl.types import DocumentAttributeFilename
        from plugins.converter import MangSession
        import time, datetime, random 
        from datetime import timedelta
        from telethon.errors import (
            ApiIdInvalidError,
            PhoneNumberInvalidError,
            PhoneCodeInvalidError,
            PhoneCodeExpiredError,
            SessionPasswordNeededError,
            PasswordHashInvalidError
        )
        from plugins import *
        from plugins.messages import *
        from plugins.get_gift import *
    except Exception as errors:
        print('An Erorr with: ' + str(errors))
        
        exit(0)

        
if not os.path.isdir('database'):
    os.mkdir('database')

API_ID = "829746"
API_HASH = "98483e947d2d31c28605e52d368b445f"
admin ="6569663552"

# Replace with your bot token
token = "7124198346:AAEGLUcvqbHs-KS2H0zWxSmj7z3Up568obE"
client = TelegramClient('ses', API_ID, API_HASH)
client.start()
bot = client

#Create DataBase
db = uu('database/elhakem.ss', 'bot')

if not db.exists("accounts"):
    db.set("accounts", [])

if not db.exists("bad_guys"):
    db.set("bad_guys", [])

if not db.exists("force"):
   db.set("force", [])
      
@client.on(events.NewMessage(pattern="/start", func = lambda x: x.is_private))
async def start(event):
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    async with bot.conversation(event.chat_id) as x:
        buttons = [
            [
                Button.inline("اضافة حساب", data="add"),
                Button.inline("جلب الروابط", data="get_gift"),
            ],
            [
                Button.inline("الانضمام لقناة", data="join_channel"),
                Button.inline("مغادرة قناة", data="leave_channel"),
            ],
            [
                Button.inline("تسجيل جلسة بايروجرام", data="pyrogram"),
                Button.inline("تسجيل جلسة تليثون", data="telethon"),
            ],
            [
                Button.inline("نسخة احتياطية", data="zip_all"),
                Button.inline("جلب جلسة", data="get_session"),
            ],
            [
                Button.inline("عدد حسابات البوت", data="get_accounts_count"),
            ],
            [
                Button.inline("تنظيف الحسابات", data="check"),
                Button.inline("مغادرة القنوات", data="leave_all"),
            ],
        ]
        await event.reply("**- مرحبا بك في بوت جلب روابط المميز من حساباتك المسجلة 🔗**\n\n- اختر من الازرار ادناه ما تود فعله.", buttons=buttons)
        
        
        
@client.on(events.callbackquery.CallbackQuery())
async def start_lis(event):
    data = event.data.decode('utf-8')
    user_id = event.chat_id
    if data == "pyrogram":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("- ارسل الان سيشن جلسة بايرورجرام")
            txt = await x.get_response()
            session = txt.text
            try:
                Convert_sess = MangSession.PYROGRAM_TO_TELETHON(session)
            except:
                return await x.send_message("- ارسل سيشن بايروجرام بشكل صحيح")
            data = {"phone_number": "لم يتم التعرف", "two-step": "لا يوجد", "session": Convert_sess}
            acc = db.get("accounts")
            acc.append(data)
            db.set("accounts", acc)
            with open('session.txt', 'w') as file:
                file.write(str(session) + '\n')
            await x.send_message("- تم حفظ السيشن بنجاح ✅")
    
    if data == "telethon":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("- ارسل الان سيشن جلسة تليثون")
            txt = await x.get_response()
            session = txt.text
            data = {"phone_number": "لم يتم التعرف", "two-step": "لا يوجد", "session": Convert_sess}
            acc = db.get("accounts")
            acc.append(data)
            db.set("accounts", acc)
            with open('session.txt', 'w') as file:
                file.write(str(session) + '\n')
            await x.send_message("- تم حفظ السيشن بنجاح ✅")
            
    if data == "back" or data == "cancel":
        buttons = [
            [
                Button.inline("اضافة حساب", data="add"),
                Button.inline("جلب الروابط", data="get_gift"),
            ],
            [
                Button.inline("الانضمام لقناة", data="join_channel"),
                Button.inline("مغادرة قناة", data="leave_channel"),
            ],
            [
                Button.inline("تسجيل جلسة بايروجرام", data="pyrogram"),
                Button.inline("تسجيل جلسة تليثون", data="telethon"),
            ],
            [
                Button.inline("نسخة احتياطية", data="zip_all"),
                Button.inline("جلب جلسة", data="get_session"),
            ],
            [
                Button.inline("تنظيف الحسابات", data="check"),
                Button.inline("مغادرة القنوات", data="leave_all"),
            ],
        ]
        await event.edit("**- مرحبا بك في بوت جلب روابط المميز من حساباتك المسجلة 🔗**\n\n- اختر من الازرار ادناه ما تود فعله.", buttons=buttons)

    if data == "add":

        async with bot.conversation(event.chat_id) as x:

            await x.send_message("✔️الان ارسل رقمك مع رمز دولتك , مثال :+201000000000")

            txt = await x.get_response()

            phone_number = txt.text.replace("+", "").replace(" ", "")

            app = TelegramClient(StringSession(), API_ID, API_HASH)

            await app.connect()

            password=None

            try:

                code = await app.send_code_request(phone_number)

            except (ApiIdInvalidError):

                await x.send_message("ʏᴏᴜʀ **ᴀᴩɪ_ɪᴅ** ᴀɴᴅ **ᴀᴩɪ_ʜᴀsʜ** ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ᴅᴏᴇsɴ'ᴛ ᴍᴀᴛᴄʜ ᴡɪᴛʜ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴩᴩs sʏsᴛᴇᴍ.")

                return

            except (PhoneNumberInvalidError):

                await x.send_message("ᴛʜᴇ **ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ** ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ᴅᴏᴇsɴ'ᴛ ʙᴇʟᴏɴɢ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ.")

                return

            await x.send_message("- تم ارسال كود التحقق الخاص بك علي حسابك علي تليجرام.\n\n- ارسل الكود بالتنسيق التالي : 1 2 3 4 5")

            txt = await x.get_response()

            code = txt.text.replace(" ", "")

            try:

                await app.sign_in(phone_number, code, password=None)

                string_session = app.session.save()

                data = {"phone_number": phone_number, "two-step": "لا يوجد", "session": string_session}

                accounts = db.get("accounts")

                accounts.append(data)

                db.set("accounts", accounts)

                await x.send_message("- تم حفظ الحساب بنجاح ✅")

            except (PhoneCodeInvalidError):

                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴡʀᴏɴɢ.**")

                return

            except (PhoneCodeExpiredError):

                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴇxᴩɪʀᴇᴅ.**")

                return

            except (SessionPasswordNeededError):

                await x.send_message("- ارسل رمز التحقق بخطوتين الخاص بحسابك")

                txt = await x.get_response()

                password = txt.text

                try:

                    await app.sign_in(password=password)

                except (PasswordHashInvalidError):

                    await x.send_message("ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ᴡʀᴏɴɢ.")

                    return

                string_session = app.session.save()

                data = {"phone_number": phone_number, "two-step": password, "session": string_session}

                accounts = db.get("accounts")

                accounts.append(data)

                db.set("accounts", accounts)

                await x.send_message("- تم حفظ الحساب بنجاح ✅")

    if data == "get_accounts_count":

        acc = db.get("accounts")

        await event.answer(f"- عدد الحسابات المسجلة ; {len(acc)}", alert=True)

    if data == "get_gift":

        await event.answer(f"- تم بدا جلب روابط المميز من الحسابات برجاء انتظار اشعار", alert=True)

        acc = db.get("accounts")

        count = 0

        for i in acc:

            x = await get_gift(i["session"])

            if x != False:

                text = f"**• رابط تليجرام مميز جديد 🥳**\n\n- الرابط : https://t.me/giftcode/{x}\n- رقم الهاتف : `{i['phone_number']}`"

                count += 1

                await client.send_message(admin, text)

        await client.send_message(admin, f"- تم الانتهاء من فحص الحسابات تم ايجاد {count} روابط")

    if data == "join_channel":

        async with bot.conversation(event.chat_id) as x:

            await x.send_message("- ارسل الان رابط او معرف القناة التي تريد الانضمام لها بكل الحسابات")

            ch = await x.get_response()

            if "@" not in ch.text:

                if "/t.me/" not in ch.text:

                    await x.send_message(f"- ارسل رابط او معرف القناة بشكل صحيح")

                    return 

            channel = ch.text.replace("https://t.me/", "").replace("http://t.me/", "").replace("@", "")

            acc = db.get("accounts")

            true, false = 0, 0

            await x.send_message(f"- تم بدء الانضمام من {len(acc)} حساب")

            for i in acc:

                xx = await join_channel(i["session"], channel)

                if xx is True:

                    true += 1

                else:

                    false += 1

            await x.send_message(f"**- تم انتهاء طلبك بنجاح ✅**\n\n- نجاح : {true}\n- فشل : {false}")

    if data == "leave_channel":

        async with bot.conversation(event.chat_id) as x:

            await x.send_message("- ارسل الان رابط او معرف القناة التي تريد المغادرة منها بكل الحسابات")

            ch = await x.get_response()

            if "@" not in ch.text:

                if "/t.me/" not in ch.text:

                    await x.send_message(f"- ارسل رابط او معرف القناة بشكل صحيح")

                    return 

            channel = ch.text.replace("https://t.me/", "").replace("http://t.me/", "").replace("@", "")

            acc = db.get("accounts")

            true, false = 0, 0

            await x.send_message(f"- تم بدء المغادرة من {len(acc)} حساب")

            for i in acc:

                xx = await leave_channel(i["session"], channel)

                if xx is True:

                    true += 1

                else:

                    false += 1

            await x.send_message(f"**- تم انتهاء طلبك بنجاح ✅**\n\n- نجاح : {true}\n- فشل : {false}")

    if data == 'zip_all':

        folder_path = f"./database"

        zip_file_name = f"database.zip"

        zip_file_nam = f"database"

        try:

            shutil.make_archive(zip_file_nam, 'zip', folder_path)

            with open(zip_file_name, 'rb') as zip_file:

                await client.send_file(user_id, zip_file, attributes=[DocumentAttributeFilename(file_name="database.zip")])

            os.remove(zip_file_name)

        except Exception as a:

            print(a)

    if data == "leave_all":

        buttons = [

            [

                Button.inline("تأكيد ✅", data="leave_all_channels"),

                Button.inline("الغاء ❌", data="cancel"),

            ]

        ]

        await event.edit("**- هل تود فعلاً تأكيد المغادرة من كل الحسابات؟**", buttons=buttons)

    if data == "leave_all_channels":

        async with bot.conversation(event.chat_id) as x:

            acc = db.get("accounts")

            await event.edit(f"**- تم بدء مغادرة كل القنوات من {len(acc)} حساب, سيصلك اشعار عند الانتهاء **")

            true, false = 0, 0

            await x.send_message(f"- تم بدء المغادرة من {len(acc)} حساب")

            for i in acc:

                xx = await leave_all(i["session"])

                if xx is True:

                    true += 1

                else:

                    false += 1

            await x.send_message(f"**- تم انتهاء مغادرة القنوات بنجاح ✅**\n\n- نجاح : {true}\n- فشل : {false}")

    

    if data == "check":

        buttons = [

            [

                Button.inline("تأكيد ✅", data="check_accounts"),

                Button.inline("الغاء ❌", data="cancel"),

            ]

        ]

        await event.edit("**- هل تود فعلاً تأكيد المغادرة من كل الحسابات؟**", buttons=buttons)

    if data == "check_accounts":

        async with bot.conversation(event.chat_id) as x:

            acc = db.get("accounts")

            await event.edit(f"**- تم بدء فحص كل الحسابات من {len(acc)} حساب, سيصلك اشعار عند الانتهاء **")

            true, false = 0, 0

            await x.send_message(f"- تم بدء فحص {len(acc)} حساب")

            for i in acc:

                Convert_sess = MangSession.TELETHON_TO_PYROGRAM(i["session"])

                xx = await check(Convert_sess, client, user_id)

                if xx is True:

                    true += 1

                else:

                    false += 1

                    acc.remove(i)

                    db.set("accounts", acc)

                await event.edit(f"**- جاري فحص الحسابات بنجاح 📂**\n\n- حسابات شغالة : {true}\n- حسابات محذوفة : {false}")

                

            await x.send_message(f"**- تم انتهاء فحص الحسابات بنجاح ✅**\n\n- حسابات شغالة : {true}\n- حسابات محذوفة : {false}")

    if data == "get_session":

        async with bot.conversation(event.chat_id) as x:

            await x.send_message("- ارسل الان رقم الهاتف الذي قمت بتسجيلة للبوت لجلب السيشن منه")

            txt = await x.get_response()

            phone_number = txt.text.replace("+", "").replace(" ", "")

            acc = db.get("accounts")

            for i in acc:

                if phone_number == i['phone_number']:

                    text = f"• رقم الهاتف : {phone_number}\n\n- التحقق بخطوتين : {i['two-step']}\n\n- الجلسة : `{i['session']}"

                    await x.send_message(text)

                    return

            await x.send_message("- لم يتم العثور علي هذا الرقم ضمن قائمة الحسابات")

            

@client.on(events.NewMessage())

async def handle_zip_file(event):

    async with bot.conversation(event.chat_id) as x:

        try:

            if event.media and event.media.document:

                message = event.message

                file = await message.download_media()



                if not os.path.exists('olddata'):

                    os.makedirs('olddata')



                with zipfile.ZipFile(file, 'r') as zip_ref:

                    zip_ref.extractall('olddata')

                    

                os.remove(file)

                await x.send_message('تم فك الضغط عن الملف بنجاح ووضعه في مجلد "olddata".')

                olddb = uu('olddata/data.sqlite', 'fuck')

                accs = db.get("accounts")

                if olddb.exists("sessions") and len(olddb.get("sessions")) > 0:

                    for i in olddb.get("sessions"):

                        Convert_sess = MangSession.PYROGRAM_TO_TELETHON(i)

                        data = {"phone_number": "لم يتم التعرف", "two-step": "لا يوجد", "session": Convert_sess}

                        if data not in accs:

                            accs.append(data)

                            db.set("accounts", accs)

                    await x.send_message(f'تم بنجاح اضافة {len(olddb.get("sessions"))} حساب الي خزن البوت الحالي.')

                else: 

                    await x.send_message(f'• هذا الخزن لا يحتوي علي اي ارقام')

        except Exception as e:

            await x.send_message(f'حدثت مشكلة أثناء فك الضغط: {str(e)}')

        

client.run_until_disconnected()


