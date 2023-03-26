import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from send_at_email import sed_message
import telebot
from telebot import types
from config import API_TOKEN
import os

bot = telebot.TeleBot(API_TOKEN)

blank = {}


@bot.message_handler(commands=["service_request"])
def send_fio(message):
    user_nik = f'{message.from_user.first_name}'
    bot.send_message(message.chat.id,
                     f"Приветствую вас, {user_nik}, я бот записывающий вашу заявку и передающий в Службу"
                     f" поддержки\nПопрошу вас ввести некоторые данные....")

    fio = bot.reply_to(message, "Введите пожалуйста ФИО")

    bot.register_next_step_handler(fio, send_phone_number)


@bot.message_handler(content_types=['text'])
def send_phone_number(message):
    try:
        blank["FIO"] = message.text

        # Содание кнопки отправик номера телефона
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, 'Номер телефона', reply_markup=keyboard)
        bot.register_next_step_handler(message, save_phone_number)
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так на записи номера телефона")


@bot.message_handler(content_types=['contact', 'text'])
def save_phone_number(message):
    if message.contact is not None:
        blank["Phone"] = message.contact.phone_number

        # удаление прошлой кнопки
        kb = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите тип оборудования и серийный номер", reply_markup=kb)
        bot.register_next_step_handler(message, save_ser_number)
    else:
        blank["Phone"] = message.text

        # удаление прошлой кнопки
        kb = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите тип оборудования и серийный номер", reply_markup=kb)
        bot.register_next_step_handler(message, save_ser_number)


@bot.message_handler(content_types=['text', 'photo'])
def save_ser_number(message):
    if message.photo is not None:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)
        # src = message.photo[1].file_id
        if os.path.exists('data'):
            if os.path.exists(f'data/{message.from_user.id}_db'):
                with open(f'data/{message.from_user.id}_db/Тип оборудования и серийный номер.jpg', 'wb') as new_file:
                    new_file.write(downloaded_file)
            else:
                os.mkdir(f'data/{message.from_user.id}_db')
                with open(f'data/{message.from_user.id}_db/Тип оборудования и серийный номер.jpg', 'wb') as new_file:
                    new_file.write(downloaded_file)
        else:
            os.mkdir('data')
            os.mkdir(f'data/{message.from_user.id}_db')
            with open(f'data/{message.from_user.id}_db/Тип оборудования и серийный номер.jpg', 'wb') as new_file:
                new_file.write(downloaded_file)

        blank["Ser_number and typy product"] = 'photo in db'
    else:
        blank["Ser_number and typy product"] = message.text

    # Создание кнопки Геолокации
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_local = types.KeyboardButton(text='Геолокация', request_location=True)
    kb.add(button_local)
    bot.send_message(message.chat.id, "Введи геолокацию", reply_markup=kb)
    bot.register_next_step_handler(message, save_country_and_city)


@bot.message_handler(content_types=['text', 'location'])
def save_country_and_city(message):
    if message.location is not None:
        blank["County and city"] = f"longitude: {message.location.longitude} latitude: {message.location.latitude}"

        # Удаление кнопки геолокации
        kb = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Пошли дальше", reply_markup=kb)
        bot.register_next_step_handler(message, button_send)
    else:
        blank["County and city"] = message.text

        # удаление кнопки геолокации
        kb = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Пошли дальше", reply_markup=kb)
        bot.register_next_step_handler(message, button_send)


@bot.message_handler(content_types=['text'])
def button_send(message):
    print("Кнопка отправить")
    print(blank)


bot.polling(none_stop=True)
