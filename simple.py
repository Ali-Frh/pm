# -*- coding: utf-8 -*-
import telebot
import random
from telebot import types
from telebot import util
from random import randint
import json
import redis
import logging
import urllib
import time
import logging
import subprocess
import requests
import os
token = "Our_Token" #token
sudo = 205906514 #admin
bot = telebot.TeleBot(token)
db = "https://api.telegram.org/bot{}/getMe?".format(token)
res = urllib.request.urlopen(db)
res_body = res.read()
parsed_json = json.loads(res_body.decode("utf-8"))
botid = parsed_json['result']['id']
botuser = parsed_json['result']['username']
R = redis.StrictRedis(host='localhost', port=6379, db=0)
bhash = "banned:users:{}".format(botuser)
mhash = "pmresan:users:{}".format(botuser)
if R.get("logchat:{}".format(botuser)) :
    logchat = int(R.get("logchat:{}".format(botuser)))
else:
    logchat = sudo
@bot.message_handler(commands=['setwlc'])
def shstart(m):
    try:
        if m.chat.id == logchat :
            text = m.text.replace('/setwlc ','')
            R.set("welcome:{}".format(str(botid)),text)
            bot.send_message(m.chat.id,"*متن خوش آمدگویی تنظیم شد به :*\n{}".format(text),parse_mode='Markdown')
    except :
        print("Error")
@bot.message_handler(commands=['setanswer'])
def show_alert(m):
    try:
        if m.chat.id == logchat :
            text = m.text.replace('/setanswer ','')
            R.set("wait:{}".format(str(botid)),text)
            bot.send_message(m.chat.id,"*متن پاسخ تغییر یافت به:*\n{}".format(text),parse_mode='Markdown')
    except Exception as e:
        print(e)
@bot.message_handler(commands=['setflood'])
def sflood(m):
    try:
        if m.chat.id == logchat :
            text = m.text.replace('/setflood ','')
            R.set("maxmsgs:{}".format(botuser),int(text))
            bot.send_message(m.chat.id,"*تعداد پیام تکراری تنظیم شد به{}*".format(text),parse_mode='Markdown')
    except Exception as e:
        print(e)
@bot.message_handler(commands=['setfloodtime'])
def sft(m):
    try:
        if m.chat.id == logchat :
            text = m.text.replace('/setfloodtime ','')
            R.set("maxflood:{}".format(botuser),int(text))
            bot.send_message(m.chat.id,"*زمان پیام تکراری تنظیم شد به {}*".format(text),parse_mode='Markdown')
    except Exception as e:
        print(e)
@bot.message_handler(commands=['setlog'])
def setlog(m):
    try:
        if m.from_user.id == sudo :
            R.set("logchat:{}".format(botuser),m.chat.id)
            bot.send_message(m.chat.id,"*New Log Chat Set*\n`ID` : _{}_".format(m.chat.id),parse_mode='Markdown')
    except Exception as e:
        print(e)
@bot.message_handler(commands=['dellog'])
def remlog(m):
    try:
        if m.from_user.id == sudo :
            R.set("logchat:{}".format(botuser),sudo)
            bot.send_message(m.chat.id,"*Old Log Chat Deleted*",parse_mode='Markdown')
    except Exception as e:
        print(e)
@bot.message_handler(commands=['start','help'])
def start(m):
    try :
        if m.chat.id == logchat :
            text = 'سلام رئیس 👋\nدستورات از این قراره:\n\n/setwlc <text>\nتنظیم متن شروع با قابلیت مارکداون\n/setanswer <text>\nتنظیم متن ارسالی به کاربر بعد از پیام های وی با قابلیت مارکدون\n/sik <on reply/id>\nبن کردن یک نفر از پیام رسان\n/unsik <on reply/id>\nآن بن کردن یک نفر از پیام رسان\n/users\nتعداد کاربران\n/bans\nتعداد افراد بن شده\n/showstart\nنمایش متن استارت فعلی\n/showwait\nدریافت متن انتظار فعلی\n/setlog <in group or private>\nتنظیم یک گروه به عنوان گروه ادمین\n/dellog\nحذف گروه ادمین\n/sendtoall <text>\nارسال یک متن به تمامی کاربران\n/fwdtoall <on reply>\nفوروارد یک پیام به تمامی اعضا\n/setflood <num>\nتنظیم تعداد پیام های ارسالی برای تشخیص اسپم (پیشفرض : ۵ در ۴ ثانیه)\n/setfloodtime <num>\nتنظیم زمان محدودیت ارسال پیام(پیشفرض : ۴)\n/msg <id> <text>\nفرستادن یک پیام به یک شخص از طریق آیدی\n\nنکته :‌برای جواب دادن به اشخاص روی پیام آنها ریپلای کنید\nنکته : پیشنهاد میشه تنظیمات فلود رو دستکاری نکنید \n\nبا آروزی خوشحالی برای شما\nمنتظر سورپرایز ها در ورژن بعدی باشید\n[ThinkTeam](https://telegram.me/ThinkTeam)'
            bot.send_message(logchat,text,parse_mode='Markdown')
        elif not m.chat.id == logchat :
            markup =  types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('ربات خود را بسازید!', url='https://telegram.me/ThinkTeam'))
            if R.get("welcome:{}".format(str(botid))) :
                tex3 = R.get("welcome:{}".format(str(botid)))
            else :
                tex3 = "*Welcome Dude ,*\n_I'll Forward Your Message To Bot Owner_"                
            if R.get("ads:{}".format(botuser)):
                bot.send_message(m.chat.id,tex3,parse_mode='Markdown',reply_markup=markup)
            else:
                bot.send_message(m.chat.id,tex3,parse_mode='Markdown')
    except Exception as e:
        print(e)
@bot.message_handler(commands=['sendall'])
def sendall(m):
    if m.chat.id == logchat :
        text = m.text.replace('/sendall ','')
        ids = R.smembers(mhash)
        for id in ids:
            try:
                bot.send_message(id,text)
            except:
                R.srem(mhash,id)
@bot.message_handler(commands=['fwdtoall'])
def fwdall(m):
    if m.chat.id == logchat :
        if m.reply_to_message:
            mid = m.reply_to_message.message_id
            ids = R.smembers(mhash)
            for id in ids:
                try:
                    bot.forward_message(id,m.chat.id,mid)
                except:
                    R.srem(mhash,id)
@bot.message_handler(commands=['unsik'])
def unban(m):
    if not m.reply_to_message :
        if m.chat.id == logchat :
            try :
                if m.reply_to_message:
                    if m.reply_to_message.forward_from :
                        user = m.reply_to_message.forward_from
                        R.srem(bhash,user)
                        bot.send_message(logchat,"Az Halat SikTir Dar Umad :/\/")
                else:
                    id = m.text.replace("/unsik ","")
                    R.srem(bhash,int(id))
                    bot.send_message(logchat,"A Halat SikTir Dar Umad :/\/")
            except Exception as e:
                print(e)
@bot.message_handler(commands=['sik'])
def unban(m):
    if not m.reply_to_message :
        if m.chat.id == logchat :
            try :
                if m.reply_to_message:
                    if m.reply_to_message.forward_from :
                        user = m.reply_to_message.forward_from
                        R.srem(bhash,user)
                        bot.send_message(logchat,"kir shod :D")
                else:
                    id = m.text.replace("/sik ","")
                    R.sadd(bhash,int(id))
                    bot.send_message(logchat,"Kir Shod Dawsh :D")
            except Exception as e:
                print(e)
@bot.message_handler(commands=['msg'])
def smsg(m):
    if not m.reply_to_message :
        if m.chat.id == logchat :
            try :
                id = m.text.split()[1]
                text = m.text.split()[2]
                receiver = int(id)
                bot.send_message(logchat,"ارسال شد به *{}*".format(id),parse_mode='Markdown')
                bot.send_message(receiver,text)
            except :
                bot.send_message(logchat,"پیام ارسال نشد شاید شمارا بلاک کرده باشد")
@bot.message_handler(content_types=['video','photo','sticker','document','audio','voice','text'])
def mfwdr(m):
    try:
        if m.text :
            if m.chat.id == logchat :
                if m.reply_to_message :
                    text = m.text
                    user = m.reply_to_message.forward_from.id
                    if m.text == '/ban' :
                        return None
                    elif m.text == '/unban' :
                        return None
                    else:
                        bot.send_message(user,text)
                        bot.send_message(m.chat.id,"Message Sent")
                elif not m.reply_to_message :
                    if m.text == '/bans' :
                        res = R.scard(bhash)
                        tex = "Banned Users : {}".format(str(res))
                        bot.send_message(logchat,tex)
                    elif m.text == '/users' :
                        res2 = R.scard(mhash)
                        tex2 = "Bot Users : {}".format(str(res2))
                        bot.send_message(logchat,tex2)
                    elif m.text == '/showstart' :
                        if R.get("welcome:{}".format(str(botid))) :
                            tex3 = R.get("welcome:{}".format(str(botid)))
                        else :
                            tex3 = "*Welcome Dude ,*\n_I'll Forward Your Message To Bot Owner_"
                            bot.send_message(m.chat.id,tex3,parse_mode='Markdown')
                    elif m.text == '/showwait' :
                        if R.get("wait:{}".format(str(botid))) :
                            tex3 = R.get("wait:{}".format(str(botid)))
                        else :
                            tex3 = "*Message Sent*"
                            bot.send_message(m.chat.id,tex3,parse_mode='Markdown')
            elif not m.chat.id == logchat :
                _hash = "anti_flood:{}:{}".format(botuser,m.from_user.id)
                msgs = 0
                max_time = 5
                if R.get(_hash):
                    msgs = int(R.get(_hash))
                    max_time = R.ttl(_hash)
                else:
                    if R.get("maxflood:{}".format(botuser)) :
                        max_time = R.get("maxflood:{}".format(botuser))
                R.setex(_hash, max_time, int(msgs) + 1)
                if m.chat.type == 'private' :
                    if R.sismember(bhash,m.chat.id) :
                        bot.send_message(m.chat.id,"شما محروم هستید")
                    elif not R.sismember(bhash,m.chat.id) :
                        if not m.text == '/start' or not m.text == '/help' :
                            if not R.sismember(mhash,m.from_user.id):
                                if R.get("wait:{}".format(str(botid))) :
                                    tex3 = R.get("wait:{}".format(str(botid)))
                                else :
                                    tex3 = "*ارسال شد*"
                                R.sadd(mhash,m.from_user.id)
                                bot.forward_message(logchat,m.chat.id,m.message_id)
                                bot.send_message(m.chat.id,tex3,parse_mode='Markdown')
                            elif R.sismember(mhash,m.from_user.id):
                                if R.get("wait:{}".format(str(botid))) :
                                    tex3 = R.get("wait:{}".format(str(botid)))
                                else :
                                    tex3 = "*ارسال شد*"
                                bot.forward_message(logchat,m.chat.id,m.message_id)
                                bot.send_message(m.chat.id,tex3,parse_mode='Markdown')
        else:
            if m.chat.id == logchat:
                if m.reply_to_message:
                    user = m.reply_to_message.forward_from.id
                    if m.photo:
                        file_id = m.photo[1].file_id
                        bot.send_photo(user,file_id)
                    elif m.video:
                        file_id = m.video.file_id
                        bot.send_video(user,file_id)
                    elif m.sticker:
                        file_id = m.sticker.file_id
                        bot.send_sticker(user,file_id)
                    elif m.document:
                        file_id = m.document.file_id
                        bot.send_document(user,file_id)
                    elif m.audio:
                        file_id = m.audio.file_id
                        bot.send_audio(user,file_id)
                    elif m.voice:
                        file_id = m.voice.file_id
                        bot.send_voice(user,file_id)
                    bot.send_message(m.chat.id,"Message Sent")
            elif not m.chat.id == logchat :
                bot.forward_message(logchat,m.chat.id,m.message_id)
                if R.get("wait:{}".format(str(botid))) :
                    tex3 = R.get("wait:{}".format(str(botid)))
                else :
                    tex3 = "*Message Sent*"
                bot.send_message(logchat,"Message Sent by {} - @{}".format(m.from_user.first_name,m.from_user.username))
                bot.send_message(m.chat.id,tex3,parse_mode='Markdown')
    except Exception as e:
        print(e)
@bot.message_handler(func=lambda message: True)
def fwdr(m):
    try:
        _hash = "anti_flood:{}:{}".format(botuser,m.from_user.id)
        msgs = 0
        if R.get(_hash):
            msgs = int(R.get(_hash))
        max_msgs = 5
        if R.get("maxmsgs:{}".format(botuser)) :
            max_msgs = R.get("maxmsgs:{}".format(botuser))
        if msgs > max_msgs:
            R.sadd(bhash,m.from_user.id)
            text = "کاربر {} - @{} iفلود کرد.format(m.from_user.first_name,m.from_user.username)
            text2 = "شما محروم شدید"
            bot.send_message(logchat,text)
            bot.send_message(m.from_user.id,text2)
    except Exception as e:
        print(e)
bot.polling(True)
