import json
import random
import telebot
import traceback
from pygments.lexers import q

smaili = ["🧐","🙃","😀","😆","🤗","🤔","🤯"]
bot = telebot.TeleBot("8024613378:AAFS3oC0sWiXhNGo1K5nuH-q37o8vYOzQLk")
shop = {}
mode = "holodilnik"
ER_ID = "-1002668725339"

while True:
    try:
        #holodilnik = {"/iogurti":"🟩", "/konserva":"🟥", "/ris":"🟨"}
        with open('.venv/holodilnik.txt', 'r', encoding='utf-8') as file:
            holodilnik = json.load(file)


        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")
            bot.reply_to(message, "команды:'/holodilnik','/shop','/start','/new','/smaili'")

        @bot.message_handler(commands=['holodilnik'])
        def send_welcome(message):
            # bot.reply_to(message,"холодильник")
            bot.reply_to(message, str(holodilnik))


        @bot.message_handler(commands=['er'])
        def eror(message):
            bot.reply_to(message, str(4/0))

        @bot.message_handler(commands=['smaili'])
        def send_welcome(message):
            bot.reply_to(message, random.choice(smaili))

        # shop
        @bot.message_handler(commands=['shop'])
        def shop_(message):
            global shop
            shop = {}
            for key, v in holodilnik.items():
                if v == "🟨" or v == "🟥":
                    shop[key + "_"] = v
            bot.reply_to(message, str(shop))

        @bot.message_handler(commands=['new'])
        def send_welcome(message):
            global mode
            bot.reply_to(message, "введите название нового продукта английскими буквами например: колбаса kolbasa")
            mode = "new"

        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            global shop, mode
            # bot.reply_to(message, str(shop))
            # bot.reply_to(message, message.text)
            if message.text in holodilnik:
                if holodilnik[message.text] == "🟨":
                    holodilnik[message.text] = "🟥"
                elif holodilnik[message.text] == "🟩":
                    holodilnik[message.text] = "🟨"
                else:
                    holodilnik[message.text] = "🟩"
                # bot.reply_to(message, "холодильник")
                bot.reply_to(message, str(holodilnik))
                # bot.reply_to(message, holodilnik[message.text])
            elif message.text in shop:
                holodilnik[message.text[0:-1]] = "🟩"
                shop = {}
                for key, v in holodilnik.items():
                    if v == "🟨" or v == "🟥":
                        shop[key + "_"] = v
                bot.reply_to(message, str(shop))
            else:
                if mode == "holodilnik":
                    bot.reply_to(message, ("не то ввёл: "))
                    bot.reply_to(message, message.text)
                else:
                    holodilnik["/" + message.text] = "🟥"
                    mode = "holodilnik"
                    bot.reply_to(message, str(holodilnik))
            with open('.venv/holodilnik.txt', 'w', encoding='utf-8') as file:
                json.dump(holodilnik, file, ensure_ascii=False, indent=4)




        bot.polling()
#bot.reply_to(message, ", ".join(holodilnik))
    except Exception as error:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        error_type = type(error).__name__  # Тип ошибки, например ZeroDivisionError
        error_message = str(error)  # Сообщение, например "division by zero"
        error_args = repr(error.args)  # Аргументы ошибки
        error_trace = traceback.format_exc()  # Полный текст с местом возникновения
        bot.send_message(ER_ID, (error_type + "    " + error_message + "    " + error_args + "    " + error_trace))

