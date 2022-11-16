import telebot
import requests
import time
import socket
import ssl
import datetime

# in TELEGRAM - https://t.me/nazk_up_bot

bot = telebot.TeleBot("5518084108:AAGNt_MEkbPtkvL8GJ_4c1RRgF7DGuVyAE8", parse_mode=None)
sitepack_nazk = ['https://interes.shtab.net/',
                 'https://sanctions.nazk.gov.ua/',
                 'https://vision.nazk.gov.ua/',
                 'https://prosvita.nazk.gov.ua/',
                 'https://antycorportal.nazk.gov.ua/',
                 'https://study.nazk.gov.ua/',
                 'https://wiki.nazk.gov.ua/',
                 'https://nazk.gov.ua/uk/',
                 'https://erp.nazk.gov.ua/',
                 'https://jira.nazk.gov.ua/',
                 'https://confluence.nazk.gov.ua/',
                 'https://cloud.nazk.gov.ua',
                 'https://mail.nazk.gov.ua/mail/?_task=mail&_mbox=INBOX',
                 'https://nacpworkspace.slack.com/']


@bot.message_handler(commands=['start_nazk'])
def start_nazk(message):
    global sitepack_nazk
    global WhileLoopFlag_nazk
    WhileLoopFlag_nazk = True
    while WhileLoopFlag_nazk is True:
        loaded = sitepack_nazk.__len__()
        dict = []
        try:
            for x in sitepack_nazk:
                hostname = x.split("/")
                hostname = hostname[2]

                try:
                    requests.get(x)
                    print(requests.get(x))
                    result_check = ssl_check_nazk(x)
                    result_check_days = str(result_check)
                    # bot.send_message(message.chat.id, ' 🟢LOAD🟢 \n ' + result_check_days)
                    dict.append(result_check_days + '🟢LOAD🟢')
                except OSError:
                    # bot.send_message(message.chat.id, hostname + '  - 🛑FAIL🛑')
                    dict.append(hostname + ' - 🛑FAIL🛑')
                    loaded -= 1
            str_result = ''
            for all in dict:
                str_result += str(all) + '\n'
            str_result += str(loaded) + "/" + str(sitepack_nazk.__len__()) + " - LOADED "
            bot.send_message(message.chat.id, str_result)
            #bot.send_message(message.chat.id, str(loaded) + "/" + str(sitepack_nazk.__len__()) + " - LOADED ")
            if loaded == 0:
                bot.send_message(message.chat.id,"Check bot serverside connection or all urls are failed")
            print(sitepack_nazk.__len__())

        except TypeError:
            bot.send_message(message.chat.id,
                             "TypeError exeption в методі start_nazk(), ")
        time.sleep(60)


def ssl_check_nazk(hostname):
    try:
        if hostname.startswith("https"):
            hostname = hostname.split("/")
            hostname = hostname[2]
            ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
            context = ssl.create_default_context()
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname, )
            conn.settimeout(5.0)
            conn.connect((hostname, 443))
            ssl_info = conn.getpeercert()
            Exp_ON = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
            Days_Remaining = Exp_ON - datetime.datetime.utcnow()
            x = (hostname + " До закінчення SSL: " + (str(Days_Remaining).split(" ")[0]) + " днів.")
            print(x)
            conn.close()
            return x
        else:
            hostname = hostname.split("/")
            hostname = hostname[2] + " - не є сайтом, що містить ssl сертифікат, або починається не з 'https'"
            return hostname
    except Exception:
        x = str(hostname) + ' не вдається завантажити SSL.'
        return x


@bot.message_handler(commands=['stop_nazk'])
def stop_nazk(message):
    global WhileLoopFlag_nazk
    WhileLoopFlag_nazk = False
    bot.send_message(message.chat.id, 'Роботу бота по перевірці ресурсів НАЗК зупинено')


while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue
