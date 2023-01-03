# Импортирование всех файлов
import telebot
import string
import json
from telebot import types
from pleyer import pleyers
import client
from text import open_file_txt, main, find_world, finish_spisok, add_pleyer_in_spisok

# Обьявление переменых
bot = telebot.TeleBot(client.token)
pleyers_last = 0  # мой айди
pleyer_1 = {}  # вспомогательная переменная для внесения имен и айди людей в базу данных
pleyer_vubor = []  # переменная для сохранения учасников игры
kol = 0
spisok_slov = ['Узнать результаты', 'Вернуться в меню', 'Информация о игре', 'Играть', 'Выйти из игры', 'Назад в меню',
               'Выбрать еще одного игрока', 'Начать игру', 'Информация о слове']
game_info = ''


# запись базы даных
def write_file(pleyer_1):
    pleyer_temp = open_file()
    with open('pleyer_base.json', 'w') as f:
        pleyer_temp.update(pleyer_1)
        x = pleyer_temp
        json.dump(x, f)


def open_file():
    with open('pleyer_base.json') as f:
        file = f.read()
        temp = json.loads(file)
    return temp


def open_baze():
    with open('russian_nouns_with_definition.json', encoding="utf-8") as f:
        dict_baze = json.load(f)
    return dict_baze


def slovo_information(slovo, id_cyt):
    bot.send_message(id_cyt, open_baze()[slovo]['definition'], reply_markup=keybord_back())


def slovo_information_2_0(slovo, id_cyt):
    bot.send_message(id_cyt, open_baze()[slovo]['definition'], reply_markup=keybord_back())


# Удаляет уже выбраного игрока
def kick_pleyer(pleyer_s):
    for i in pleyers_delet.items():
        if pleyer_s == i[1]:
            pleyer_vubor.append(i[1])
            pleyers_delet.pop(i[0])
            break


def keybord_rez():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_rez = types.KeyboardButton('Узнать результаты')
    button_men = types.KeyboardButton('Вернуться в меню')
    return markup.add(button_rez, button_men)


# Клавиатура меню
def start_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = types.KeyboardButton('Информация о игре')
    button_game = types.KeyboardButton('Играть')
    button_slov = types.KeyboardButton('Толковый словарь')
    markup.add(button_game)
    markup.add(button_info)
    markup.add(button_slov)
    return markup


# Клавиатура на выход из игры
def keybord_bk():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton('Выйти из игры')
    button_info = types.KeyboardButton('Информация о слове')
    return markup.add(button_back, button_info)


# Клавиатура для возращения
def keybord_back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton('Назад в меню')
    return markup.add(button_back)


# Клавиатура для добавления первого человека
def keybord_add_pleyers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    d = []
    for key, value in pleyers_delet.items():
        key = types.KeyboardButton(value)
        d.append(key)
    return markup.add(*d)


# Клавиатура для добавления еще людей используеться на добавление 3 и более людей
def last_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_pleyer = types.KeyboardButton('Выбрать еще одного игрока')
    button_game = types.KeyboardButton('Начать игру')
    return markup.add(button_game, button_pleyer)


# Функция которая выводит кто следущий ходит
def game_raz(pleyer_vubor, chat_id):
    global kol
    if kol != len(pleyer_vubor) - 1:
        bot.send_message(chat_id, f'Сейчас ходит - {pleyer_vubor[kol]}')
        kol += 1
    elif kol == len(pleyer_vubor) - 1:
        bot.send_message(chat_id, f'Сейчас ходит - {pleyer_vubor[kol]}')
        kol = 0


def game_raz_2_0(pleyer_vubor, chat_id):
    global kol
    if kol - 1 != len(pleyer_vubor) - 1:
        bot.send_message(chat_id, f'Сейчас ходит - {pleyer_vubor[kol]}')
    elif kol - 1 == len(pleyer_vubor) - 1:
        bot.send_message(chat_id, f'Сейчас ходит - {pleyer_vubor[kol]}')


def game_prov(pleyer_vubor, pleyer_name, chat_id):
    if pleyer_vubor[kol - 1] != pleyer_name:
        return False
    return True


def information_game(ip_chat):
    for key, value in finish_spisok.items():
        bot.send_message(ip_chat, f"У {key} - {len(value)} баллов", reply_markup=keybord_back())


# Фунцйия которая віводет на какую букву тебе надо написатьслово
def next_word(chat_id, pleyer_sms):
    global next_word_1
    if pleyer_sms[-1] == 'ь' or pleyer_sms[-1] == 'ъ':
        bot.send_message(chat_id, f"Тебе на '{pleyer_sms[-2]}'")
        next_word_1 = pleyer_sms[-2]
    else:
        bot.send_message(chat_id, f"Тебе на '{pleyer_sms[-1]}'")
        next_word_1 = pleyer_sms[-1]


# При нажатие старт твой id сохроняеться
@bot.message_handler(commands=["start"])
def answer(message):
    pleyer_1[str(message.from_user.id)] = message.from_user.first_name.title()
    write_file(pleyers)
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}', reply_markup=start_keyboard())


# При добавление человека он сохраняеться в базе данных
@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    pleyer_1[message.json["new_chat_member"]["id"]] = message.json["new_chat_member"]["first_name"].title()
    write_file(pleyer_1)
    bot.send_message(message.chat.id,
                     f'Добро пожоловать в группу {message.json["new_chat_member"]["first_name"].title()}',
                     reply_markup=start_keyboard())


# Основной код
@bot.message_handler(content_types=['text'])
def get(say):
    global pleyers_last, pleyers_delet, slovo, game_info, pleyer_vubor, world_back
    slovo = ''
    if say.text == 'Информация о игре':
        bot.send_message(say.chat.id, 'Это бот где ты можешь поиграть с друзьями в слова на последнюю букву.',
                         reply_markup=keybord_back())
    elif say.text == 'Назад в меню':
        bot.send_message(say.chat.id, 'Выберите пункт меню.', reply_markup=start_keyboard())
        game_info = ''
    elif say.text == 'Толковый словарь':
        game_info = 'Толковый словарь'
        bot.send_message(say.chat.id, 'Напишите слово о котором вы хотите узнать информацию',
                         reply_markup=keybord_back())
    elif say.text not in spisok_slov and game_info == 'Толковый словарь':
        if say.text.strip(
                string.punctuation + " " + string.digits).lower() in open_file_txt():
            slovo_information_2_0(say.text.strip(
                string.punctuation + " " + string.digits).lower(), say.chat.id)
    elif say.text == 'Играть':
        world_back = []
        pleyer_vubor.append(say.from_user.first_name)
        pleyers_last = str(say.from_user.id)
        pleyers_delet = open_file()
        pleyers_delet.pop(pleyers_last)
        if len(open_file()) == 1:
            bot.send_message(say.chat.id, 'В группе не достаточно игроков')
        else:
            bot.send_message(say.chat.id, 'Выберите с кем вы хотите поиграть', reply_markup=keybord_add_pleyers())
    elif say.text in [*open_file().values()]:
        bot.send_message(say.chat.id, 'Выберите пункт меню.', reply_markup=last_keyboard())
        kick_pleyer(say.text)
    elif say.text == 'Выбрать еще одного игрока':
        if len(pleyers_delet) == 0:
            bot.send_message(say.chat.id, 'Больше игроков на выбор нету')
            bot.send_message(say.chat.id, 'Начните игру')
        else:
            bot.send_message(say.chat.id, 'Выберите с кем вы хотите поиграть', reply_markup=keybord_add_pleyers())
    elif say.text == 'Начать игру':
        bot.send_message(say.chat.id, f'Начинаем игру между - {", ".join(pleyer_vubor)}', reply_markup=keybord_bk())
        add_pleyer_in_spisok(pleyer_vubor)
        game_raz(pleyer_vubor, say.chat.id)
        game_info = 'Начать игру'
    elif say.text.strip(
            string.punctuation + " " + string.digits).lower() not in world_back and say.text not in spisok_slov and game_info == 'Начать игру':
        game_prov(pleyer_vubor, say.from_user.first_name, say.chat.id)
        if game_prov(pleyer_vubor, say.from_user.first_name, say.chat.id):
            if say.text.strip(
                    string.punctuation + " " + string.digits).lower() in open_file_txt():
                if main(say.text, say.from_user.first_name):
                    slovo = say.text.strip(string.punctuation + " " + string.digits).lower()
                    world_back.append(say.text.strip(string.punctuation + " " + string.digits).lower())
                    game_raz(pleyer_vubor, say.chat.id)
                    next_word(say.chat.id, say.text.strip(string.punctuation + " " + string.digits).lower())
            elif say.text not in open_file_txt():
                bot.send_message(say.chat.id, 'Такого слова несуществует')
                bot.send_message(say.chat.id, 'Игра закончена', reply_markup=keybord_rez())
                bot.send_message(say.chat.id, f'Проиграл - {say.from_user.first_name}', reply_markup=keybord_rez())
                pleyer_vubor = []
                game_info = ''
        else:
            bot.send_message(say.chat.id, 'Сейчас не твой ход')
            game_raz_2_0(pleyer_vubor, say.chat.id)
            bot.send_message(say.chat.id, f"Тебе на '{next_word_1}'")
    elif say.text.strip(
            string.punctuation + " " + string.digits).lower() in world_back and say.text not in spisok_slov:
        bot.send_message(say.chat.id, 'Такое слова уже вводили. Напишите другое')
    elif say.text == 'Узнать результаты':
        information_game(say.chat.id)
    elif say.text == 'Выйти из игры':
        pleyer_vubor = []
        game_info = ''
        bot.send_message(say.chat.id, 'Игра закончена', reply_markup=keybord_rez())
        bot.send_message(say.chat.id, f'{say.from_user.first_name} сдался', reply_markup=keybord_rez())
    elif say.text == 'Вернуться в меню':
        bot.send_message(say.chat.id, 'Выберите пункт меню.', reply_markup=start_keyboard())
    elif say.text == 'Информация о слове':
        if len(world_back) == 1:
            slovo_information(world_back[0].strip(
                string.punctuation + " " + string.digits).lower(), say.chat.id)
        if len(world_back) not in [0, 1]:
            slovo_information(world_back[-2].strip(
                string.punctuation + " " + string.digits).lower(), say.chat.id)
        else:
            bot.send_message(say.chat.id, 'Вы еще не написали слово')


bot.polling(none_stop=True, interval=0)
