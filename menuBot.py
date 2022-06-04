from telebot import types


# -----------------------------------------------------------------------
class Menu:
    hash = {}  # тут будем накапливать все созданные экземпляры класса
    cur_menu = None  # тут будет находиться текущий экземпляр класса, текущее меню
    extendedParameters = {}  # это место хранения дополнительных параметров для передачи в inline кнопки
    # ПЕРЕПИСАТЬ для хранения параметров привязанных к chat_id и названию кнопки

    def __init__(self, name, buttons=None, parent=None, action=None):
        self.parent = parent
        self.name = name
        self.buttons = buttons
        self.action = action

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        markup.add(*buttons)  # Обратите внимание - звёздочка используется для распаковки списка
        self.markup = markup

        self.__class__.hash[name] = self  # в классе содержится словарь, со всеми экземплярами класса, обновим его

    @classmethod
    def getExtPar(cls, id):
        return cls.extendedParameters.pop(id, None)

    @classmethod
    def setExtPar(cls, parameter):
        import uuid
        id = uuid.uuid4().hex
        cls.extendedParameters[id] = parameter
        return id

    @classmethod
    def getMenu(cls, name):
        menu = cls.hash.get(name)
        if menu != None:
            cls.cur_menu = menu
        return menu


m_main = Menu("Главное меню", buttons=["Развлечения", "Игры", "ДЗ", "Помощь"])

m_games = Menu("Игры", buttons=["Камень, ножницы, бумага", "Игра в 21", "Выход"], parent=m_main)
m_game_21 = Menu("Игра в 21", buttons=["Карту!", "Стоп!", "Выход"], parent=m_games, action="game_21")
m_game_rsp = Menu("Камень, ножницы, бумага", buttons=["Камень", "Ножницы", "Бумага", "Выход"], parent=m_games, action="game_rsp")

m_DZ = Menu("ДЗ", buttons=["Задание-1", "Задание-2", "Задание-3", "Задание-4", "Задание-5", "Задание-6", "Выход"], parent=m_main)

m_fun = Menu("Развлечения", buttons=["Прислать котика", "Прислать анекдот", "Прислать фильм", "Курсы валют", "Текст в аудио", "Выход"], parent=m_main)

m_kurs = Menu('Курсы валют', buttons = ['USD','RUR','EUR','BTC',"Выход"], parent=m_fun)