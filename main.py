# Телеграм-бот v.004
import json
from gettext import find
from io import BytesIO

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import requests
import bs4
import BotGames  # бот-игры, файл BotGames.py
from menuBot import Menu  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню
import DZ  # домашнее задание от первого урока
from voice import get_mp3_file  #для перевода текста в аудио
from parser import get_article_language #для перевода текста в аудио
import os
import time

bot = telebot.TeleBot('5571270108:AAFx75xdYqi7haRhNpNcwMKT0WVjbfC7kjk')  # Создаем экземпляр бота
game21 = None  # класс игры в 21, экземпляр создаём только при начале игры


# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python."
    bot.send_message(message.chat.id, text=txt_message, reply_markup=Menu.getMenu("Главное меню").markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global game21

    chat_id = message.chat.id
    ms_text = message.text

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Прислать котика":
            contents = requests.get('https://aws.random.cat/meow').json()
            urlCAT = contents['file']
            time.sleep(5)
            bot.send_photo(chat_id, photo=urlCAT, caption='Получай! (´• ω •)ノ～♡')

        elif ms_text == "Прислать анекдот":
            bot.send_message(chat_id, text=get_anekdot())

        elif ms_text == "Прислать фильм":
            send_film(chat_id)

        elif ms_text == "Курсы валют":
            bot.send_message(chat_id,
                             text="Чтобы узнать наличный курс, выберите название валюты:".format(
                                 message.from_user), reply_markup=Menu.getMenu("Курсы валют").markup)


        elif ms_text == "Карту!":
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return

        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return

        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание-4":
            DZ.dz4(bot, chat_id, message)

        elif ms_text == "Задание-5":
            DZ.dz5(bot, chat_id)

        elif ms_text == "Задание-6":
            DZ.dz6(bot, chat_id)

        elif ms_text == "Текст в аудио":
            voice_msg(chat_id, message)

        elif ms_text == 'USD' or 'RUR' or 'EUR' or 'BTC':
            get_kurs(chat_id, ms_text)

    else:
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")

# ...........................................................................................................

def get_kurs(chat_id, message):
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
    if response.status_code == 200:
        try:
            response.json()
            markup = types.ReplyKeyboardMarkup(selective=False)
            for coin in response:
                if (message == coin['ccy']):
                    bot.send_message(chat_id, printCoin(coin['buy'], coin['sale']))

        except Exception:
            bot.reply_to(message, "Возникла ошибка.")
    else:
        bot.send_message(chat_id, text='Извините, не удалось получить информацию.')


def printCoin(buy, sale):
    return 'Курс покупки - ' + str(buy) + '\nКурс продажи - ' + str(sale)

# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки, использовать методы Menu.getExtPar() и Menu.setExtPar()
    pass
    # if call.data == "ManOrNot_GoToSite": #call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    #
    #     # После обработки каждого запроса нужно вызвать метод answer_callback_query, чтобы Telegram понял, что запрос обработан.
    #     bot.answer_callback_query(call.id)

# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            global game21
            game21 = BotGames.Game21()  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        return True
    else:
        return False


# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias


# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Татяна")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/autistanya")
    markup.add(btn1)
    img = open('8.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

# -----------------------------------------------------------------------
def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# -----------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""

# -----------------------------------------------------------------------


# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

# ---------------------------------------------------------------------
def voice_msg(chat_id, message):
    bot.send_message(chat_id, text='Введите текст, который хотите перевести в аудиофайл:')

    @bot.message_handler(content_types=['text'])
    def forward_message(message):
        article_text = str(message.text)
        article_language = get_article_language(article_text)

        if article_language == False:
            bot.send_message(chat_id, text='Не удалось распознать язык.')
        else:
            bot.send_message(message.from_user.id, f"Язык текста определён как: {article_language[0]}.")
            bot.send_message(message.from_user.id, "Отправляю аудиофайл...")
            file_name = 'audiofile.mp3'
            get_mp3_file(file_name, article_text, article_language[1])
            time.sleep(10)
            audio_file = open('audiofile.mp3', 'rb')
            bot.send_audio(chat_id, audio=audio_file)
            os.remove(file_name)

    bot.register_next_step_handler(message, forward_message)



bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()



# var token = '5261138323:AAG_66FwSIwVOLk0BRkZGI95RxzzY-OdnRY';
# var telegramUrl = 'https://api.telegram.org/bot' + token;
# var webAppUrl = 'https://script.google.com/macros/s/AKfycbzdIarwD9lbxE6W6-1kwGvqmA22J_D4ggPbDfiJCSmdwQupfSY2FhMmpO-w6JNd_2CG/exec'
#
# function getMe() {
#   var url = telegramUrl + '/getMe';
#   var response = UrlFetchApp.fetch(url);
#   Logger.log(response.getContentText());
# }
#
# function setWebhook() {
#   var url = telegramUrl + '/setWebhook?url=' + webAppUrl;
#   var response = UrlFetchApp.fetch(url);
#   Logger.log(response.getContentText());
# }
#
# function doGet(e) {
#   return HtmlService.createHtmlOutput('Hi there!');
# }
#
# function doPost(e) {
#   GmailApp.sendEmail(Session.getEffectiveUser().getEmail(), 'Message sent to bot', JSON.stringify(e,null,4));
# }


#5261138323:AAG_66FwSIwVOLk0BRkZGI95RxzzY-OdnRY
#https://script.google.com/macros/s/AKfycbwJZafbclIYoSq4bCGSvrPmQfJvekrJK8LK4d1KHbC4Y64NCJn13lRxc7jVeA-NxaNj/exec