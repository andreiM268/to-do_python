import telebot
import bdhandler
from telebot import types
from pathlib import Path
from PIL import Image

file = open(Path().absolute() / 'token.txt')
token = str(file.read())
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, "Привет, пользователь!")


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, "Я могу записывать задачи и выводить их по запросу. \n "
                                           "/new_task <задача> - команда позволяет записать задачу. \n"
                                           "Можно отправлять и с фотографиями \n"
                                           "/all - команда выводит все записанные задачи \n"
                                           "/delete <Номер задачи> - команда удляет команду по номеру \n"
                                           "/buttons - Выводит список доступных кнопо")


@bot.message_handler(commands=['new_task'], content_types=['text'])                 #Обработка задач с текстом
def new_item_text_handler(message):
    task_text = message.text[10:]
    id = int(str(bdhandler.numberoftasks(str(message.from_user.id)))) + 1
    newtask = (id, message.from_user.id, task_text, 'NULL')
    bdhandler.addtask(newtask)


@bot.message_handler(content_types=['photo'])                                           #Обработка задач с фотографиями
def new_item_photo_handler(message):
    try:
        if str(message.caption[0:9]) == '/new_task':
            file = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file.file_path)
            filename = message.photo[1].file_id
            src = (Path().absolute() / "photos" / filename).with_suffix(".jpg")
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            id = int(str(bdhandler.numberoftasks(str(message.from_user.id)))) + 1
            newtask = (id, message.from_user.id, message.caption[10:], str(src))
            bdhandler.addtask(newtask)                                                      #вызывает функцию записи в БД
            bot.send_message(message.from_user.id, "Запись сделана")
        else:
            bot.send_message(message.from_user.id, "Я не понимаю")
    except TypeError as err:
        bot.send_message(message.from_user.id, "Используй команды")


@bot.message_handler(commands=['all'])                                                  #Вывод всех записей
def all_handler(message):
    bot.send_message(message.from_user.id, "Список записей \n ____________________")
    rows = bdhandler.showall(str(message.from_user.id))
    out = ''
    for row in rows:
        out = str(row[0]) + ' | ' +  str(row[1])
        imageadr = row[2]
        if imageadr == 'NULL':
            bot.send_message(message.from_user.id, out)
        else:
            photo = open(str(row[2]), 'rb')
            bot.send_photo(message.from_user.id, photo,  out)


@bot.message_handler(commands=['delete'], content_types=['text'])               #Обработка команды delete
def delete_handler(message):
    delid = message.text[8:]
    idtask = (delid, message.from_user.id)
    file_path = Path(bdhandler.photopath(idtask))
    try:
        file_path.unlink()
    except OSError as e:
        print("Ошибка: %s : %s" % (file_path, e.strerror))
    bdhandler.deltask(idtask)


@bot.message_handler(commands=['buttons'])                                      #Обработка команды buttons
def button_handler(message):
    markup = types.ReplyKeyboardMarkup()

    item_start = types.KeyboardButton('/start')
    item_all = types.KeyboardButton('/all')
    item_help = types.KeyboardButton('/help')

    markup.row(item_start, item_all, item_help)
    bot.send_message(message.from_user.id, "Доступные кнопки", reply_markup = markup)


bot.polling()

