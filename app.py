import telebot
from telebot import types
import json
import sys


sys.path.append('src/poll')
from poll.anket import Anket
from poll.config import questions

anket = Anket(questions)
     
token="6085529638:AAFWmFlZcH8vjqqNOp9PA-IqYhI1nHr_S0o"
bot = telebot.TeleBot(token)

global answers
answers = []


def gen_markup(options, k):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    l = [types.InlineKeyboardButton(x, callback_data='{\"questionNumber\": ' + 
                                    str(k) + ',\"answerText\": "' + x + '"}') 
                                    for x in options]
    markup.add(*l)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    k = 0 # с какого вопроса начинаем опрос
    button_column = anket.config[k]['options']
    global answers
    answers = [] # список ответов (пока пустой)
    bot.send_message(chat_id=message.chat.id, text="Привет, я бот! Ответь на мои вопросы",reply_markup=gen_markup(button_column, k))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global answers  # делаем переменную глобальной
    # Если сообщение из чата с ботом
    req = call.data.split('_')
    print(req)
    #Распарсим полученный JSON
    json_string = json.loads(req[0])
    k = json_string['questionNumber'] + 1
    answer = json_string['answerText']
    if k == 1 and answer == "Нет":
        k = -1
        return bot.edit_message_text(chat_id=call.message.chat.id, 
                                     message_id=call.message.message_id, 
                                     text='На нет и суда нет :)')
    answers.append(answer) # записываем ответ на предыдущий вопрос
    if k == anket.length:
        score = anket.add_answers(answers)
        return bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text=f'спасибо за ответы, вы набрали: {score} баллов')
        
    button_column = anket.config[k]['options']
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text=anket.get_question(k), 
                          reply_markup=gen_markup(button_column, k))        
        
bot.polling()