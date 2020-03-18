import config
import telebot
import time
import requests
import random

bot = telebot.TeleBot(config.token)

param = False

@bot.message_handler(commands=['start'])
def start_all(message):
    bot.send_message(message.chat.id, "Sup. Вы добавили уникального погодного бота, т.к. он был специально разработан для Нубского Домика. Каждый день вы будете получать информацию о погоде в одном из рандомных городов участников Нубского Домика. Чтобы запустить бота напишите '/weather', чтобы остановить напишите '/stop'. Чтобы запустить повторо опять напишите '/start'.")
    global param
    param = True

@bot.message_handler(commands=['stop'])
def stop_all(message):
    bot.send_message(message.chat.id, 'Вы остановили бота')
    global param
    param = False

@bot.message_handler(commands=['weather'])
def start_message(message):
    bot.send_message(message.chat.id, "Бот запущен, от вас больше ничего не требуется, он большой и самостоятельный.")
    global param
    while param == True:
        z = random.randint(0, len(config.city_l) - 1)
        r_city = config.city_l[z]

        try:
            req = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': r_city, 'units': 'metric', 'lang': 'ru', 'APPID': config.appid})
            data = req.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            city_id = data['list'][0]['id']
        except Exception as e:
            print("Exception (find):", e)
            pass

        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': config.appid})
            data = res.json()
            conditions = str(data['weather'][0]['description'])
            temp = str(data['main']['temp'])
            wind = str(data['wind']['speed'])
        except Exception as e:
            print("Exception (weather):", e)
            pass

        a = random.randint(0, 1)
        if a == 1:
            y = 5 + random.randint(1, 3)
        else:
            y = 5 - random.randint(1, 3)
        bot.send_message(message.chat.id, f'Сейчас в локации {r_city} примерно {temp}°C и {conditions}.\nВетер около {wind}м/с.\nКстати, хочу напомнить, что Семми тупой гей, хе хе хе')
        time.sleep(y)




bot.polling(none_stop=True, interval=0)
