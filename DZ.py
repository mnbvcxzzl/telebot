
name = "Таня"
age = 18

def dz1(bot, chat_id):
    bot.send_message(chat_id, text=f'Моё имя {name}')
# -----------------------------------------------------------------------
def dz2(bot, chat_id):
    bot.send_message(chat_id, text=f'Мой возраст {age} лет')
# -----------------------------------------------------------------------
def dz3(bot, chat_id):
    bot.send_message(chat_id, text=name * 5)
# -----------------------------------------------------------------------
def dz4(bot, chat_id, message):
    bot.send_message(chat_id, text='Как вас зовут?')

    @bot.message_handler(content_types=['text'])
    def inputName(message):
        user_name = message.text
        try:
            user_name = int(user_name)
        except ValueError:
            bot.send_message(chat_id, text='Сколько вам лет?')
        else:
            bot.send_message(chat_id, text='Вы указали некорректное имя! Сколько вам лет?')
            user_name = ''

        @bot.message_handler(content_types=['text'])
        def inputAge(message):
            user_age = message.text
            try:
                user_age = int(user_age)
            except ValueError:
                bot.send_message(chat_id, text='Вы указали возраст неправильно!')
                n = 'неизвестен.'
            else:
                if int(user_age) <= 0 or int(user_age) > 150:
                    n = "ты указал неверный возраст."
                elif int(user_age) <= 7:
                    n = "первый период детства."
                elif int(user_age) > 7 and int(user_age) < 13:
                    n = "второй период детства."
                elif int(user_age) > 12 and int(user_age) < 17:
                    n = "подростковый возраст."
                elif int(user_age) > 16 and int(user_age) < 22:
                    n = "юношеский возраст."
                elif int(user_age) > 21 and int(user_age) < 36:
                    n = "первый период зрелого возраста."
                elif int(user_age) > 35 and int(user_age) < 61:
                    n = "второй период зрелого возраста."
                elif int(user_age) > 60 and int(user_age) < 76:
                    n = "пожилой возраст."
                elif int(user_age) > 75 and int(user_age) < 91:
                    n = "старческий возраст."
                elif int(user_age) > 90:
                    n = "долгожитель. Поздравляю!"
            bot.send_message(chat_id, text=f'Привет {user_name}! Твой возрастной период - {n}')

        bot.register_next_step_handler(message, inputAge)

    bot.register_next_step_handler(message, inputName)
# -----------------------------------------------------------------------
def dz5(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько вам лет?", dz5_ResponseHandler)

def dz5_ResponseHandler(bot, chat_id, age_int):
    bot.send_message(chat_id, text=f"О! тебе уже {age_int}! \nА через год будет уже {age_int+1}!")
# -----------------------------------------------------------------------
def dz6(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id, f"Привет {message.text}! В твоём имени {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)
# -----------------------------------------------------------------------
def my_inputInt(bot, chat_id, txt, ResponseHandler):

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)
    # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
        # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler

# -----------------------------------------------------------------------