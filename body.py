import telebot
import os
import requests
from telebot import types
from dotenv import load_dotenv
import songsterrAPI as ssrt
import XML_parser as xmlprs
import json
import geniusAPI as geniusAPI
import time

config = load_dotenv()

bot = telebot.TeleBot(os.getenv("tgapikey"))


@bot.message_handler(commands=['start', 'cancel'])
def send_welcome(message):
    try:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name, reply_markup=markup,
                         parse_mode='MARKDOWN')
        time.sleep(1)
        bot.send_message(message.chat.id,
                         "При написании этого бота автор столкнулся с особенностями API сервиса Songsterr, с которыми так и не удалось совладать. В связи с этим очень просим по возможности не тестировать бот на прочность и не отправлять что-то абсурдное. В случае ошибки в написании названия песни или артиста вызовите команду */artist_name* повторно. (Регистр учитывается)",
                         reply_markup=markup, parse_mode='MARKDOWN')
        time.sleep(1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('/artist_name')
        markup.add(itembtn1)

        bot.send_message(message.chat.id,
                         "*Выберите действие:*\n" + "*artist_name* - ``` вывести список песен автора```", reply_markup=markup, parse_mode='MARKDOWN')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте еще раз.')


@bot.message_handler(commands=["artist_name"])
def artist_name(message):
    try:
        chat_id = message.chat.id
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id,
                               'Укажите *имя исполнителя* или *название группы*, а мы покажем список его песен с доступными табами',
                               reply_markup=markup, parse_mode='MARKDOWN')
        bot.register_next_step_handler(msg, input_artist_name)
    except Exception as e:
        bot.send_message(message.chat.id, 'Кажется, такого нет :( Проверьте правильность написания и попробуйте ещё раз.')


def input_artist_name(message):
    try:
        chat_id = message.chat.id
        user_id = str(chat_id)
        markup = types.ReplyKeyboardRemove(selective=False)
        artist_name = str(message.text)
        file_name = "./users_files/" + user_id + "-songs.txt"
        json_file = "./users_files/" + user_id + "-user.json"

        user_dict = {"artist": ""}
        user_dict['artist'] = artist_name

        with open(json_file, 'w') as f:
            json.dump(user_dict, f)

        ssrt.artxml(artist_name=artist_name, user_id=user_id)
        xmlprs.xml_songs_parser(user_id=str(chat_id))
        doc = open(file_name, 'rb')
        bot.send_document(message.chat.id, doc)
        msg = bot.send_message(message.chat.id,
                               'Выберите *название песни* и напишите его нам, а мы предложим доступные табы.',
                               reply_markup=markup, parse_mode='MARKDOWN')
        bot.register_next_step_handler(msg, input_song_name)
    except Exception as e:
        bot.send_message(message.chat.id, 'Кажется, такого нет :( Проверьте правильность написания и попробуйте ещё раз.')


def input_song_name(message):
    try:
        chat_id = message.chat.id
        user_id = str(chat_id)

        json_file = "./users_files/" + user_id + "-user.json"

        song_name = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        itembtn1 = types.KeyboardButton('/artist_name')
        itembtn2 = types.KeyboardButton('/get_lyrics')
        itembtn3 = types.KeyboardButton('/get_artist_info')
        markup.add(itembtn1, itembtn2, itembtn3)

        with open(json_file) as f:
            file_content = f.read()
            templates = json.loads(file_content)

        artist = templates['artist']

        user_dict = {"artist": "", "song": ""}

        user_dict['artist'] = artist
        user_dict['song'] = song_name

        with open(json_file, 'w') as f:
            json.dump(user_dict, f)

        song_id = xmlprs.xml_songid_parser(name=song_name, user_id=user_id)
        link = ssrt.songstr(song_id=str(song_id))

        bot.send_message(message.chat.id, "*Ссылка на табы: *\n" + link, reply_markup=markup, parse_mode='MARKDOWN')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте ещё раз.')


@bot.message_handler(commands=['get_lyrics'])
def get_lyrics(message):
    try:
        chat_id = message.chat.id
        user_id = str(chat_id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('/artist_name')
        itembtn2 = types.KeyboardButton('/get_artist_info')
        markup.add(itembtn1, itembtn2)

        res = bot.send_message(message.chat.id, "Genius уже выгружает текст, это может занять несколько секунд.",
                               reply_markup=markup, parse_mode='MARKDOWN')

        json_file = "./users_files/" + user_id + "-user.json"

        with open(json_file) as f:
            file_content = f.read()
            templates = json.loads(file_content)

        message_str = geniusAPI.get_lyrics(artist=templates['artist'], songname=templates['song'])

        bot.send_message(message.chat.id, " ``` " + message_str + " ``` ", reply_markup=markup, parse_mode='MARKDOWN')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте ещё раз.')


@bot.message_handler(commands=['get_artist_info'])
def get_artist_info(message):
    try:
        chat_id = message.chat.id
        user_id = str(chat_id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('/artist_name')
        itembtn2 = types.KeyboardButton('/get_lyrics')
        markup.add(itembtn1, itembtn2)

        json_file = "./users_files/" + user_id + "-user.json"

        with open(json_file) as f:
            file_content = f.read()
            templates = json.loads(file_content)

        message_str = geniusAPI.get_artist_description(artist=templates['artist'])

        bot.send_message(message.chat.id, ' ``` ' + message_str + ' ``` ', reply_markup=markup, parse_mode='MARKDOWN')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте ещё раз.')


bot.polling()
