import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from send_at_email import sed_message
import telebot
from telebot import types

bot = telebot.TeleBot("")

blank = {}


@bot.message_handler(commands=["service_request"])
def send_fio(message):
    user_nik = f'{message.from_user.first_name}'
    bot.send_message(message.chat.id,
                     f"Приветствую вас, {user_nik}, я бот записывающий вашу заявку и передающий в Службу"
                     f" поддержки\nПопрошу вас ввести некоторые данные....")

    fio = bot.reply_to(message, "Введите пожалуйста ФИО")

    bot.register_next_step_handler(fio, send_phone_number)


def send_phone_number(message):
    try:
        #запись в словарь
        message_to_save = message.text
        blank["FIO"] = message_to_save

        phone = bot.reply_to(message,"Введите номер телефона вручную или же кнопкой")

        #Хотел сделать так чтобы по кнопке определялся номер телефона но на выходе значение NONE
        #kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        #botton = types.KeyboardButton(text="Запрос телефона", request_contact=True)
        #kb.add(botton)
        #bot.send_message(message.chat.id,"Номер телефона", reply_markup=kb)

        bot.register_next_step_handler(phone, country_and_city)

    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так на записи номера телефона")


def country_and_city(message):
    try:
        message_to_save = message.text
        blank["Phone"]= message_to_save

        local = bot.reply_to(message, "Введите страну и город через пробел")
        bot.register_next_step_handler(local, type_vid_device)
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так с определением")


def type_vid_device(message):
    message_to_save = message.text
    blank["Country and City"] = message_to_save

    inf_about_device = bot.reply_to(message, "Введите тип оборудования и серийный номер")
    bot.register_next_step_handler(inf_about_device, send_in_email)

def send_in_email(message):
    message_to_save = message.text
    blank["info about device"] = message_to_save



#отвечает юзеру по его нику
@bot.message_handler(commands=["start"])
def start(message):
    mess = f'{message.from_user.first_name}'
    bot.send_message(message.chat.id, mess, )


# @bot.message_handler()
# def get_user_text(message):
# bot.send_message(message.chat.id, message)


# встроенная в сообщение кнопка
@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Сайт", url="https://github.com/hishnik64/TestWeatherAPI"))
    bot.send_message(message.chat.id, "перейти на сайт", reply_markup=markup)


# Тут две кнопки которые красиво выглядят и работают исправно
@bot.message_handler(commands=["service"])
def service(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    botton_service = types.KeyboardButton("В тех поддержку")
    botton_service2 = types.KeyboardButton("Куда-нибудь ещё")
    markup.add(botton_service, botton_service2)
    bot.send_message(message.chat.id, "Перейти на сайт", reply_markup=markup)


# Получить ввод пользователя

@bot.message_handler(commands=["text"])
def iinput(message):
    send = bot.reply_to(message, "Отсавить отзыв")
    bot.register_next_step_handler(send, review)


def review(message):
    message_to_save = message.text
    print(message_to_save)


#########################################################


# Запрос телефона и геолокации

@bot.message_handler(commands=["help"])
def phone_namber(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    botton = types.KeyboardButton(text="Запрос телефона", request_contact=True)
    botton2 = types.KeyboardButton(text="Запрос геолокации", request_location=True)
    kb.add(botton, botton2)
    bot.send_message(message.chat.id, "номер телефона", reply_markup=kb)


@bot.message_handler(commands=["contact"])
def check_contact(message):
    bot.send_message(message.chat.id, message.contact.phone_number)


bot.polling(none_stop=True)
