import random
import telebot
from telebot import types
import requests
import bs4

bot = telebot.TeleBot('5261138323:AAG_66FwSIwVOLk0BRkZGI95RxzzY-OdnRY')

name = ""
age = 0
qq = 0

@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Главное меню')
    btn2 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2)

    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я тестовый бот для курса программирования на языке Python".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    if 'главное' and 'меню' in ms_text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('возможности')
        btn2 = types.KeyboardButton('управление')
        btn3 = types.KeyboardButton('WEB-камера')
        btn4 = types.KeyboardButton('дз 1 урок')
        btn5 = types.KeyboardButton('помощь')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(chat_id, text="нажмите на кнопочку ヽ( ・ω・ )ﾉ", reply_markup=markup)

    elif ms_text == "помощь" or ms_text == "/help":
        bot.send_message(chat_id, "автор: Муравейник Татьяна 1-МД-8")
        key1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="нажми, чтобы связаться со мной", url="https://t.me/autistanya")
        key1.add(btn1)
        bot.send_photo(message.chat.id, photo='https://i.pinimg.com/564x/de/6e/ce/de6ecef8b4c0ba58829f48eb52f5c86a.jpg', reply_markup=key1)

    elif ms_text == "возможности":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("прислать котика")
        btn3 = types.KeyboardButton("прислать анекдот")
        # btn4 = types.KeyboardButton("прислать картинку")
        btn5 = types.KeyboardButton("курсы валют")
        back = types.KeyboardButton("вернуться в главное меню")
        markup.add(btn1, btn3, btn5, back)
        bot.send_message(chat_id, text="нажмите на кнопочку ヽ( ・ω・ )ﾉ", reply_markup=markup)

    elif ms_text == "прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "прислать котика":
        contents = requests.get('https://aws.random.cat/meow').json()
        urlCAT = contents['file']
        bot.send_photo(chat_id, photo=urlCAT, caption='получай! (´• ω •)ノ～♡')

    elif ms_text == "WEB-камера":
        bot.send_message(chat_id, text="еще не готово...")

    elif ms_text == "управление":  # ...................................................................................
        bot.send_message(chat_id, text="еще не готово...")

    elif ms_text == "дз 1 урок":
        bot.send_message(chat_id, text="Ваше имя?")
        bot.register_next_step_handler(message, dzx)

    elif ms_text == "курсы валют":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('USD')
        btn2 = types.KeyboardButton('EUR')
        btn3 = types.KeyboardButton('RUR')
        btn4 = types.KeyboardButton('BTC')
        back = types.KeyboardButton("вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(chat_id,
                         text="чтобы узнать наличный курс, выберите название валюты:".format(
                             message.from_user), reply_markup=markup)

    elif ms_text == 'USD' or 'RUR' or 'EUR' or 'BTC':
        get_kurs(message)

    else:
        bot.send_message(chat_id, text="я тебя слышу! Ваше сообщение: " + ms_text)


def dzx(message):
    chat_id = message.chat.id
    global name
    name = message.text

    try:
        age = int(message.text)
    except ValueError:
        bot.send_message(chat_id, name * 5)

        list(name)
        bot.send_message(chat_id, name[::-1])
        bot.send_message(chat_id, name[1:-1])
        bot.send_message(chat_id, name[len(name) - 3:])
        bot.send_message(chat_id, name[0:4])

        bot.send_message(chat_id, name.upper())
        bot.send_message(chat_id, name.lower())

        bot.send_message(chat_id, text="Ваш возраст?")
        bot.register_next_step_handler(message, dzz)
    else:
        bot.send_message(chat_id, text="Возраст указан неправильно! Введите снова")
        bot.register_next_step_handler(message, dzx)

def dzz(message):
    chat_id = message.chat.id
    global age
    age = message.text

    try:
        age = int(message.text)
    except ValueError:
        bot.send_message(chat_id, text="Возраст указан неправильно! Введите снова")
        bot.register_next_step_handler(message, dzz)
    else:
        if int(age) <= 0 or int(age) > 150:
            n = "ты указал неверный возраст."
        elif int(age) <= 7:
            n = "первый период детства."
        elif int(age) > 7 and int(age) < 13:
            n = "второй период детства."
        elif int(age) > 12 and int(age) < 17:
            n = "подростковый возраст."
        elif int(age) > 16 and int(age) < 22:
            n = "юношеский возраст."
        elif int(age) > 21 and int(age) < 36:
            n = "первый период зрелого возраста."
        elif int(age) > 35 and int(age) < 61:
            n = "второй период зрелого возраста."
        elif int(age) > 60 and int(age) < 76:
            n = "пожилой возраст."
        elif int(age) > 75 and int(age) < 91:
            n = "старческий возраст."
        elif int(age) > 90:
            n = "долгожитель. Поздравляю!"
        else:
            n = "Ошибка"
        bot.send_message(chat_id, text = "Привет, " + name + "! Твой возрастной период - " + n)

        bot.send_message(chat_id, text="Сколько будет 2*2+2 ?")
        bot.register_next_step_handler(message, dzq)

def dzq(message):
    chat_id = message.chat.id
    global qq
    qq = message.text

    try:
        qq = int(message.text)
    except Exception:
        bot.send_message(chat_id, text="Нужно ввести численное значение!")
        bot.register_next_step_handler(message, dzq)
    else:
        if int(qq) == (2 * 2 + 2):
            bot.send_message(chat_id, text = "Правильно!\nЗадание выполнено.")
        else:
            bot.send_message(chat_id, text = "Неравильно!\nПопробуйте еще раз - ")
            bot.register_next_step_handler(message, dzq)

def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(req_anek.text, 'html.parser')
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]

def get_kurs(message):
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11').json()
    try:
        markup = types.ReplyKeyboardMarkup(selective=False)
        for coin in response:
            if (message.text == coin['ccy']):
                bot.send_message(message.chat.id, printCoin(coin['buy'], coin['sale']), reply_markup=markup, parse_mode='Markdown')

    except Exception:
        bot.reply_to(message, "sorry, error")

def printCoin(buy, sale):
    return 'Курс покупки - ' + str(buy) + '\nКурс продажи - ' + str(sale)




# def get_icons():
#     array_anekdots = []
#     req_anek = requests.get('https://vk.com/im?sel=178941779&v=')
#     soup = bs4.BeautifulSoup(req_anek.text, 'html.parser')
#     result_find = soup.findAll('im-mess--text wall_module _im_log_body')
#     for result in result_find:
#         array_anekdots.append(result.getText().strip())
#     return array_anekdots[0]

# def get_icon():
#     array_icons = []
#     req_icon = requests.get('https://www.pinterest.ru/iriska332455/icons/')
#     soup = bs4.BeautifulSoup(req_icon.content)
#     result_f = soup.select('img', class_='hCL kVc L4E MIw')
#     for result in result_f:
#         lnk = result['src']
#         with open( basename(lnk), " wb") as array_icons:
#             array_icons.append(requests.get(lnk).content)
#     return array_icons[0]

bot.polling(none_stop=True, interval=0)
