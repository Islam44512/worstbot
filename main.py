import telebot
import os
import random
import requests


from bot_logic import gen_pass, gen_emodji, flip_coin  # Импортируем функции из bot_logic
slovar = {"мзда":"Дань или вознаграждение","припона":"Припятствие или переграда", "фигляр":"Шут"}
bot = telebot.TeleBot("telegram very good token")
image_mem_it = os.listdir("./image/IT")
image_mem_animals = os.listdir("./image/ANIMALS")

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    if res.status_code == 200 :
        data = res.json()
        return data['url']
    else:
        return "error"
    
def get_anime_image_url(text_from_user):    
    url = 'https://kitsu.io/api/edge/anime?filter[text]='+ text_from_user
    res = requests.get(url)
    if res.status_code == 200 :
        data = res.json()
        return data['data'] [0] ['attributes'] ['posterImage'] ['original']
    else:
        return "error"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши команду /hello, /bye, /pass, /emodji или /coin  ")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, f"Привет! {message.from_user.first_name} Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['help'])
def send_bye(message):
    bot.reply_to(message, "/start = Начало бота, /hello = Приветствие, /bye = Просщание, /pass ""КОЛИЧЕСТВО СИМВОЛОВ"" = Гениратор паролей, /emodji = Любой эмоджи, /coin = Подбросить монетку, /heh )КОЛИЧЕСТВО РАЗ) = heh🙃, /словарь ""СЛОВО"" = Словарь старых слов. /duck = фото рандомного гуся, /anime (КАТЕГОРИЯ) = постер аниме, /mem (КАТЕГОРИЯ) = мемы по категориям")

@bot.message_handler(commands=['pass'])
def send_password(message):
    words = message.text.split()
    if len(words) < 2:
        password = gen_pass(8)
    else:
        password = gen_pass(int(words [1]))
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")
     
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)

@bot.message_handler(commands=['словарь'])
def send_slovar(message):
    text_from_user = message.text.split()
    if text_from_user == ["/словарь"]:
        for i in list(slovar.keys()):
            bot.reply_to(message, f"{i}-{slovar[i]}")
    else:
        text_from_user = str(message.text.split()[1])
        text_from_user_for_screach = text_from_user.lower()
        if text_from_user_for_screach in slovar.keys():
            # Что делать, если слово нашлось?
            bot.reply_to(message, slovar [text_from_user_for_screach])
        else:
            # Что делать, если слово не нашлось?
            bot.reply_to(message, "К сожелению не нашли такое слово! Побробуйте Мзда, Припона, Фигляр.")

@bot.message_handler(commands=["mem"])
def send_mems(message):
    text_from_user = message.text.split()
    if text_from_user == ["/mem"]:
        bot.reply_to(message, "Побробуйте ещё раз и напишите категорию!(Например Animals, IT)")
    else:
        text_from_user = str(message.text.split()[1]).lower()
        if text_from_user == "it":
            with open (f"./image/IT/{random.choice (image_mem_it)}", "rb") as file:
                bot.send_photo (message.chat.id, file)
        if text_from_user == "animals":
            with open (f"./image/ANIMALS/{random.choice (image_mem_animals)}", "rb") as file:
                bot.send_photo (message.chat.id, file)

@bot.message_handler(commands=['duck'])
def duck(message):
    image_url = get_duck_image_url()
    bot.reply_to(message, image_url)

@bot.message_handler(commands=['anime'])
def anime(message):
    text_from_user = message.text.split()
    if len(text_from_user) < 2:
        bot.reply_to(message, "Побробуйте ещё раз и напишите категорию!")
    else:
        text_from_user = str(message.text.split()[1]).lower()
        image_url = get_anime_image_url(text_from_user)
        bot.reply_to(message, image_url)

# Запускаем бота
bot.polling()
