import telebot
import wikipedia
import translators as ts

bot = telebot.TeleBot("1651583929:AAFYRHxD5pl7bMfZJ5Onn8kkie79_ahbWTA")

switch_for_answer = int(0)
page_id = "0"
chars_in_wiki = int(1000)
name = "0"


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Я говорю, кто правил в стране некоторое определенное количество лет назад. Чтобы начать, "
                          "введи /start")
    sticker = open("C:\\Users\\Lex\\Desktop\\pythonProject\\wikip.webp", "rb")
    bot.send_sticker(message.chat.id, sticker)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Что ищем?")
        bot.register_next_step_handler(message, get_answer)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def get_answer(message):
    print("Бот работает")
    global page_id
    global name
    wikipedia.set_lang("ru")
    wiki = str(message.text)
    if wiki == "None":
        check_fail(message)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Ссылка на страницу', callback_data=1))
        try:
            raw_data = wikipedia.summary(wiki, chars=1000)
            page_id = wikipedia.page(raw_data).url
            name = wiki
            if len(wikipedia.summary(wiki)) > 1000:
                markup.add(telebot.types.InlineKeyboardButton(text='Следующие 1000 символов', callback_data=2))
                bot.send_message(message.from_user.id, raw_data, reply_markup=markup)
            else:
                bot.send_message(message.from_user.id, raw_data, reply_markup=markup)
        except:
            wiki_foreign = ts.google(wiki)
            try:
                foreign_raw_data = wikipedia.summary(wiki_foreign, chars=1000)
                foreign_raw_data = ts.google(foreign_raw_data, to_language='ru')
                page_id = wikipedia.page(wiki_foreign).url
                name = wiki_foreign
                if len(wikipedia.summary(wiki_foreign)) > 1000:
                    markup.add(telebot.types.InlineKeyboardButton(text='Следующие 1000 символов', callback_data=2))
                    bot.send_message(message.from_user.id, foreign_raw_data, reply_markup=markup)
                else:
                    bot.send_message(message.from_user.id, foreign_raw_data, reply_markup=markup)
            except:
                bot.send_message(message.from_user.id, "Я не знаю ничего про это")
    bot.register_next_step_handler(message, get_answer)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Следующие 1000 символов', callback_data=2))
    global page_id
    global chars_in_wiki
    global name
    if call.data == '1':
        bot.send_message(call.message.chat.id, page_id)
    elif call.data == '2':
        page = wikipedia.summary(name)
        if chars_in_wiki + 1000 < len(page):
            page_na_otp = page[chars_in_wiki:chars_in_wiki + 1000]
            chars_in_wiki = chars_in_wiki + 1000
            bot.send_message(call.message.chat.id, page_na_otp, reply_markup=markup)
        else:
            page_na_otp = page[chars_in_wiki:len(page)]
            chars_in_wiki = 1000
            bot.send_message(call.message.chat.id, page_na_otp)


def check_fail(message):
    global switch_for_answer
    if switch_for_answer == 0:
        bot.send_message(message.chat.id, "Нельзя присылать картинки, стикеры, файлы, и иное, кроме текста")
        switch_for_answer = +1
    elif switch_for_answer == 1:
        sticker = open("C:\\Users\\Lex\\Desktop\\pythonProject\\a.webp", "rb")
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, "Нельзя присылать картинки, стикеры, файлы, и иное, кроме текста")
        switch_for_answer = 2
    elif switch_for_answer == 2:
        sticker = open("C:\\Users\\Lex\\Desktop\\pythonProject\\a.webp", "rb")
        bot.send_sticker(message.chat.id, sticker)
        switch_for_answer = 3
    else:
        i = 0
        page = wikipedia.page("О культе личности и его последствиях").content
        while True:
            if i+1000 < len(page):
                part_page = page[i:i + 1000]
                i += 1000
                bot.send_message(message.chat.id, part_page)
            else:
                part_page = page[i:len(page)-1]
                bot.send_message(message.chat.id, part_page)
                break


bot.polling(none_stop=True, interval=0)
