# # # import random
# # # import telebot
# # # from pygments.lexers import q
# # #
# # #
# # # bluda = ["Пелемени🥟","Колбаса🥩", "Хлеб 'Harris'🍞","Огурцы🥒","Картофель🥔"]
# # # # bluda = ["Пелемени","Колбаса", "Хлеб 'Harris'","Огурцы","Картофель"]
# # # bot = telebot.TeleBot("7619692489:AAHDkybkufqW3uGGSiCjMneYfOn1uQxj0-Y")
# # #
# # #
# # # @bot.message_handler(commands=['start'])
# # # def send_welcome(message):
# # #     bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")
# # #     bot.reply_to(message, "команды:'/k🥩','/kКолбаса🥩','/start','/1', '/2','/hello','/bye','/bluda','/help'")
# # #
# # # @bot.message_handler(commands=['help'])
# # # def send_welcome(message):
# # #     bot.reply_to(message, "команды:'/start','/1', '/2','/hello','/bye','/bluda','/help'")
# # #
# # #
# # # @bot.message_handler(commands=['1', '2'])
# # # def send_welcome(message):
# # #     bot.reply_to(message, "12346")
# # #
# # # @bot.message_handler(commands=['hello'])
# # # def send_hello(message):
# # #     bot.reply_to(message, "Привет! Как дела?")
# # #
# # #
# # # @bot.message_handler(commands=['bye'])
# # # def send_bye(message):
# # #     bot.reply_to(message, "Пока! Удачи!")
# # #
# # # @bot.message_handler(commands=['bluda'])
# # # def send_bye(message):
# # #     bot.reply_to(message, random.choice(bluda))
# # #
# # # @bot.message_handler(func=lambda message: True)
# # # def echo_all(message):
# # #     bot.reply_to(message, ("не то ввёл: "))
# # #     bot.reply_to(message, message.text)
# # #
# # #
# # # bot.polling()
# # import telebot
# #
# # # Инициализация бота с использованием его токена
# # bot = telebot.TeleBot("7619692489:AAHDkybkufqW3uGGSiCjMneYfOn1uQxj0-Y")
# #
# #
# # # Обработчик команды '/start' и '/hello'
# # @bot.message_handler(commands=['start', 'hello'])
# # def send_welcome(message):
# #     bot.reply_to(message, f'Привет! Я бот {bot.get_me().first_name}!')
# #
# # #{bot.get_me().first_name}
# # # Обработчик команды '/heh'
# # @bot.message_handler(commands=['heh'])
# # def send_heh(message):
# #     count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
# #     bot.reply_to(message, "he" * count_heh)
# #     bot.send_message(message.chat.id, 'Just use /find command!')
# #
# #
# # # Запуск бота
# # bot.polling()
# # This bot is needed to connect two people and their subsequent anonymous communication
# #
# # Avaiable commands:
# # `/start` - Just send you a messsage how to start
# # `/find` - Find a person you can contact
# # `/stop` - Stop active conversation
#
# import telebot
# from telebot import types
#
# # Initialize bot with your token
# bot = telebot.TeleBot('7619692489:AAHDkybkufqW3uGGSiCjMneYfOn1uQxj0-Y')
#
# # The `users` variable is needed to contain chat ids that are either in the search or in the active dialog, like {chat_id, chat_id}
# users = {}
# # The `freeid` variable is needed to contain chat id, that want to start conversation
# # Or, in other words: chat id of user in the search
# freeid = None
#
#
# # `/start` command handler
# #
# # That command only sends you 'Just use /find command!'
# @bot.message_handler(commands=['start'])
# def start(message: types.Message):
#     bot.send_message(message.chat.id, 'Just use /find command!')
#
#
# # `/find` command handler
# #
# # That command finds opponent for you
# #
# # That command according to the following principle:
# # 1. You have written `/find` command
# # 2. If you are already in the search or have an active dialog, bot sends you 'Shut up!'
# # 3. If not:
# #   3.1. Bot sends you 'Finding...'
# #   3.2. If there is no user in the search:
# #       3.2.2. `freeid` updated with `your_chat_id`
# #   3.3. If there is user in the search:
# #       3.3.1. Both you and the user in the search recieve the message 'Founded!'
# #       3.3.2. `users` updated with a {user_in_the_search_chat_id, your_chat_id}
# #       3.3.3. `users` updated with a {your_chat_id, user_in_the_search_id}
# #       3.3.4. `freeid` updated with `None`
# @bot.message_handler(commands=['find'])
# def find(message: types.Message):
#     global freeid
#
#     if message.chat.id not in users:
#         bot.send_message(message.chat.id, 'Finding...')
#
#         if freeid is None:
#             freeid = message.chat.id
#         else:
#             # Question:
#             # Is there any way to simplify this like `bot.send_message([message.chat.id, freeid], 'Founded!')`?
#             bot.send_message(message.chat.id, 'Founded!')
#             bot.send_message(freeid, 'Founded!')
#
#             users[freeid] = message.chat.id
#             users[message.chat.id] = freeid
#             freeid = None
#
#         print(users, freeid)  # Debug purpose, you can remove that line
#     else:
#         bot.send_message(message.chat.id, 'Shut up!')
#
#
# # `/stop` command handler
# #
# # That command stops your current conversation (if it exist)
# #
# # That command according to the following principle:
# # 1. You have written `/stop` command
# # 2. If you are not have active dialog or you are not in search, bot sends you 'You are not in search!'
# # 3. If you are in active dialog:
# #   3.1. Bot sends you 'Stopping...'
# #   3.2. Bot sends 'Your opponent is leavin`...' to your opponent
# #   3.3. {your_opponent_chat_id, your_chat_id} removes from `users`
# #   3.4. {your_chat_id, your_opponent_chat_id} removes from `users`
# # 4. If you are only in search:
# #   4.1. Bot sends you 'Stopping...'
# #   4.2. `freeid` updated with `None`
# @bot.message_handler(commands=['stop'])
# def stop(message: types.Message):
#     global freeid
#
#     if message.chat.id in users:
#         bot.send_message(message.chat.id, 'Stopping...')
#         bot.send_message(users[message.chat.id], 'Your opponent is leavin`...')
#
#         del users[users[message.chat.id]]
#         del users[message.chat.id]
#
#         print(users, freeid)  # Debug purpose, you can remove that line
#     elif message.chat.id == freeid:
#         bot.send_message(message.chat.id, 'Stopping...')
#         freeid = None
#
#         print(users, freeid)  # Debug purpose, you can remove that line
#     else:
#         bot.send_message(message.chat.id, 'You are not in search!')
#
#
# # message handler for conversation
# #
# # That handler needed to send message from one opponent to another
# # If you are not in `users`, you will recieve a message 'No one can hear you...'
# # Otherwise all your messages are sent to your opponent
# #
# # Questions:
# # 1. Is there any way to improve readability like `content_types=['all']`?
# # 2. Is there any way to register this message handler only when i found the opponent?
# @bot.message_handler(
#     content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text',
#                    'venue', 'video', 'video_note', 'voice'])
# def chatting(message: types.Message):
#     if message.chat.id in users:
#         bot.copy_message(users[message.chat.id], users[users[message.chat.id]], message.id)
#     else:
#         bot.send_message(message.chat.id, 'No one can hear you...')
#
#
# bot.infinity_polling(skip_pending=True)
#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     # with open('ред.png', 'rb') as f:
#     #     bot.send_photo(message.chat.id, f)
#     img_name = random.choice(os.listdir('images'))
#     with open(f'images/{img_name}', 'rb') as f:
#         bot.send_photo(message.chat.id, f)
# #https://randomfox.ca/floof/           link
# #https://random-d.uk/api/random        url
# #https://random.dog/woof.json          url
#
# def get_duck_image_url():
#     url = 'https://random-d.uk/api/random'
#     res = requests.get(url)
#     data = res.json()
#     return data['url']
#
# def get_fox_image_url():
#     url = 'https://randomfox.ca/floof/'
#     res = requests.get(url)
#     data = res.json()
#     return data['link']
#
# def get_dog_image_url():
#     url = 'https://random.dog/woof.json'
#     res = requests.get(url)
#     data = res.json()
#     return data['url']
#
# @bot.message_handler(commands=['duck'])
# def duck(message):
#     '''По команде duck вызывает функцию get_duck_image_url и отправляет URL изображения утки'''
#     image_url = get_duck_image_url()
#     bot.reply_to(message, image_url)
#
# @bot.message_handler(commands=['fox'])
# def duck(message):
#     '''По команде duck вызывает функцию get_duck_image_url и отправляет URL изображения утки'''
#     image_url = get_fox_image_url()
#     bot.reply_to(message, image_url)
#
# @bot.message_handler(commands=['dog'])
# def duck(message):
#     '''По команде duck вызывает функцию get_duck_image_url и отправляет URL изображения утки'''
#     image_url = get_dog_image_url()
#     bot.reply_to(message, image_url)
#
#
import telebot
from pygments.lexers import q
import os
import random
import requests
bot = telebot.TeleBot("7619692489:AAHDkybkufqW3uGGSiCjMneYfOn1uQxj0-Y")
@bot.message_handler(commands=['botle'])
def send_welcome(message):
    bot.reply_to(message, "Бутылки бывают разные. бывают пластиковые, а бывают стеклянные. Если у вас стеклянная бутылка")
    bot.reply_to(message, "То можно сдать в пункт приёма стеклотары, ну или сделать фонарь. Ну, засовываем в стеклянную бутылку свечу и ставим куда-то вот вам и фонарь. А если у вас пластиковая бутылка")
bot.polling()
