import telebot
from bot_logic import gen_pass, gen_emodji, flip_coin  # Импортируем функции из bot_logic
slovar = {"мзда":"Дань или вознаграждение","припона":"Припятствие или переграда", "фигляр":"Шут"}
# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot("TOKEN")

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
    bot.reply_to(message, "/start = Начало бота, /hello = Приветствие, /bye = Просщание, /pass ""КОЛИЧЕСТВО СИМВОЛОВ"" = Гениратор паролей, /emodji = Любой эмоджи, /coin = Подбросить монетку, /heh ""КОЛИЧЕСТВО РАЗ"" = heh🙃, /словарь ""СЛОВО"" = Словарь старых слов.")

@bot.message_handler(commands=['pass'])
def send_password(message):
    words = message.text.split()
    if len(words) < 2:
        password = gen_pass(8)  # Устанавливаем длину пароля, например, 10 символов
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
     # Обработчик команды '/heh'
     
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
        

# Запускаем бота
bot.polling()