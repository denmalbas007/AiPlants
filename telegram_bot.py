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


# Создание экземпляра бота
bot = telebot.TeleBot('6043547925:AAGRqG1Cqr-0mdZFqd7qm93XmgLpe5OpFaE')

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
    # Отправка сообщения с выбранным значением
    bot.send_message(chat_id=message.chat.id, text=f"Вы выбрали: {message.text}\nТоп 5 растений по данному ареалу:\n1. {recs['first']}\n2. {recs['second']}\n3. {recs['third']}\n 4. {recs['fourth']}\n5. {recs['fifth']}")

# Запуск бота
bot.polling()
