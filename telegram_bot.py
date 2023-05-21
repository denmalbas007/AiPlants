import pandas as pd
import telebot
from telebot import types
from simple_recsys import get_recs

def areas(path):
    plants = pd.read_excel(path)
    plants['Ареалы произрастания'] = plants['Ареалы произрастания'].str.lstrip()
    plants['col_split'] = plants['Ареалы произрастания'].str.split(', ')
    df_exploded = plants.explode('col_split')
    unique = df_exploded['col_split'].unique()
    return unique

id_key = '6032665394:AAGJJW2ael1pY42fl-FKaTjp9qYj48DSC2M'

# Создание экземпляра бота
bot = telebot.TeleBot(id_key)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создание списка значений для кнопок
    options = areas('Plants.xlsx')

    # Создание объекта клавиатуры с кнопками
    keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    buttons = [types.KeyboardButton(option) for option in options]
    keyboard.add(*buttons)

    # Отправка приветственного сообщения с клавиатурой
    bot.send_message(chat_id=message.chat.id, text='Привет! Выбери ареал произрастания:', reply_markup=keyboard)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    recs = get_recs(message.text)
    columns = ['Название лекарственной культуры', 'В каких медицинских препаратах содержится, наименование', 'Ежегодная потребность лекарственного сырья, тонны', 'Timedelta_plant']
    # Отправка сообщения с выбранным значением
    output = ''
    for k, v in recs.items():
        output += f'''{k + 1}. Название лекарственной культуры: {v['Название лекарственной культуры']}\n
        В каких медицинских препаратах содержится: {v['В каких медицинских препаратах содержится, наименование']}\n
        Ежегодная потребность лекарственного сырья: {v['Ежегодная потребность лекарственного сырья, тонны']}\n
        Период посева, мес: {v['meantime_plant']}\n 
        Период сбора урожая, мес: {v['meantime_collect']}\n'''
    bot.send_message(chat_id=message.chat.id, text=f"Вы выбрали: {message.text}\nТоп 5 растений по данному ареалу:\n {output}")

# Запуск бота
bot.polling()
