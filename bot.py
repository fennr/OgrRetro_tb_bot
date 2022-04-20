import telebot
from telebot import types
from dataclasses import dataclass
from enum import IntEnum
from typing import Callable
import os

TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)

user_dict = {}

lang = 'ru'

@dataclass(frozen=True)
class Answers:
    yes: list
    no: list

answer = Answers(
    yes=['✅ Да', 'Да', 'Yes'],
    no=['❌ Нет', 'Нет', 'No'],
)


class EndingType(IntEnum):
    emotional = 1
    priority = 2
    creation = 3
    overall = 4
    question = 5


class User:
    def __init__(self, ending):
        self.ending = ending
        self.intramural = None
        self.long = None

    def __str__(self):
        print(f'Ending: {self.ending}, Int: {self.intramural}, Long: {self.long}')



@dataclass(frozen=True)
class Messages:
    start: dict
    q_01: dict
    q_02: dict
    q_03: dict
    q_04: dict
    q_05: dict
    q_06: dict
    q_07: dict
    q_08: dict
    end_01: dict
    end_02: dict
    end_03: dict
    end_04: dict
    end_05: dict
    ending_01: dict
    ending_02: dict
    error: dict
    restart: dict
    end: dict
    result: dict
    bye: dict
    no_ans: dict


texts = Messages(
    start={'ru': 'Вас привествует бот "Организуй Ретроспективу".'},
    q_01={
        'ru': '''Являются ли какие-либо из перечисленных ниже целей приоритетными целями ретроспективы?\n
* Определить настрой команды и эмоциональное состояние в целом\n
* Определить отношение команды к ретроспективе\n
* Определить удовлетворенность команды ходом и итогами спринта\n
* Собрать обратную связь о работе менеджера проекта
    '''},
    q_02={'ru': 'Ставите ли Вы перед собой какие-либо другие цели?'},
    q_03={'ru': 'Ставите ли Вы перед собой как приоритет на планируемую ретроспективу '
                'цель сгенерировать рекомендации по улучшению результативности команды?'},
    q_04={'ru': 'Является ли для Вас приоритетным проведение тимбилдинга '
                'для повышения мотивации и сплоченности команды, повышения уровня доверия'},
    q_05={'ru': 'Ставите ли Вы перед собой какие-либо другие цели?'},
    q_06={'ru': 'Являются ли выявление корня проблемы и разработка рекомендаций по улучшению работы '
                'приоритетными целями на планируемую ретроспективу?'},
    q_07={'ru': 'Ставите ли Вы перед собой какие-либо другие цели?'},
    q_08={'ru': 'Является ли для Вас приоритетным проведение самоанализа участников '
                'для выявления их сильных и слабых сторон, ожиданий и т.д.?'},
    end_01={'ru': 'Эмоционально-аналитические'},
    end_02={'ru': 'Приоритезирующие'},
    end_03={'ru': 'Творческие'},
    end_04={'ru': 'Для формирования общей картины'},
    end_05={'ru': 'На основе вопросов'},
    ending_01={'ru': 'Будет ли ретроспектива проводиться очно?'},
    ending_02={'ru': 'Имеете ли Вы возможность проводить на каждом этапе ретроспективы упражнения '
                     'длительностью более 20 минут?'},
    error={'ru': 'Произошла ошибка'},
    restart={'ru': 'Хотите подобрать ретроспективу еще раз?'},
    result={'ru': 'Для вас подобраны следующие упражнения'},
    end={'ru': 'Завершение работы'},
    bye={'ru': 'Хорошего дня!'},
    no_ans={'ru': 'Пожалуйста, выберите ответ с помощью клавиатуры или напишите "Да"/"Нет"'}
)


def step_pattern(message, this_process: Callable, yes_process: Callable, yes_text, no_process: Callable, no_text):
    try:
        ans = message.text
        if ans in answer.yes:
            print(yes_process)
            msg = bot.send_message(message.chat.id, yes_text)
            bot.register_next_step_handler(msg, yes_process)
        elif ans in answer.no:
            print(no_process)
            msg = bot.send_message(message.chat.id, no_text)
            bot.register_next_step_handler(msg, no_process)
        else:
            msg = bot.send_message(message.chat.id, texts.no_ans[lang])
            bot.register_next_step_handler(msg, this_process)
    except Exception as e:
        bot.send_message(message.chat.id, texts.error[lang])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print('start')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(answer.yes[0])
    markup.add(answer.no[0])
    msg = bot.send_message(message.chat.id, texts.start[lang], reply_markup=markup)
    msg = bot.send_message(message.chat.id, texts.q_01[lang])
    bot.register_next_step_handler(msg, process_01_step)


def process_no_step(message):
    pass  # msg = bot.send_message(message.chat.id, texts.bye[lang])


def process_restart_step(message):
    print('restart')
    step_pattern(message=message,
                 this_process=process_restart_step,
                 yes_process=process_01_step,
                 yes_text=texts.q_01[lang],
                 no_process=process_no_step,
                 no_text=texts.end[lang]
                 )


def process_01_step(message):
    print('01')
    step_pattern(message=message,
                 this_process=process_01_step,
                 yes_process=process_02_step,
                 yes_text=texts.q_02[lang],
                 no_process=process_03_step,
                 no_text=texts.q_03[lang]
                 )


def process_02_step(message):
    print('02')
    step_pattern(message=message,
                 this_process=process_02_step,
                 yes_process=process_end04_step,
                 yes_text=texts.ending_01[lang],
                 no_process=process_end01_step,
                 no_text=texts.ending_01[lang]
                 )


def process_03_step(message):
    print('03')
    step_pattern(message=message,
                 this_process=process_03_step,
                 yes_process=process_04_step,
                 yes_text=texts.q_04[lang],
                 no_process=process_06_step,
                 no_text=texts.q_06[lang]
    )


def process_04_step(message):
    print('04')
    step_pattern(message=message,
                 this_process=process_04_step,
                 yes_process=process_05_step,
                 yes_text=texts.q_05[lang],
                 no_process=process_end02_step,
                 no_text=texts.ending_01[lang]
                 )


def process_05_step(message):
    print('05')
    step_pattern(message=message,
                 this_process=process_05_step,
                 yes_process=process_end04_step,
                 yes_text=texts.ending_01[lang],
                 no_process=process_end03_step,
                 no_text=texts.ending_01[lang]
                 )


def process_06_step(message):
    print('06')
    step_pattern(message=message,
                 this_process=process_06_step,
                 yes_process=process_07_step,
                 yes_text=texts.q_07[lang],
                 no_process=process_08_step,
                 no_text=texts.q_08[lang]
                 )


def process_07_step(message):
    print('07')
    step_pattern(message=message,
                 this_process=process_07_step,
                 yes_process=process_end04_step,
                 yes_text=texts.ending_01[lang],
                 no_process=process_end05_step,
                 no_text=texts.ending_01[lang]
                 )


def process_08_step(message):
    print('08')
    step_pattern(message=message,
                 this_process=process_03_step,
                 yes_process=process_end04_step,
                 yes_text=texts.ending_01[lang],
                 no_process=process_end03_step,
                 no_text=texts.ending_01[lang],
                 )


def process_end01_step(message):
    ending01(message, 1)


def process_end02_step(message):
    ending01(message, 2)


def process_end03_step(message):
    ending01(message, 3)


def process_end04_step(message):
    ending01(message, 4)


def process_end05_step(message):
    ending01(message, 5)


def ending01(message, endng):
    print('end01')
    user = User(endng)
    user_dict[message.chat.id] = user
    intramural = message.text
    try:
        if intramural in answer.yes:
            user.intramural = 1
        elif intramural in answer.no:
            user.intramural = 0
        else:
            raise Exception("Выберите Да или Нет")
        msg = bot.send_message(message.chat.id, texts.ending_02[lang])
        bot.register_next_step_handler(msg, ending02_pattern)
    except Exception:
        bot.send_message(message.chat.id, texts.error[lang])


def ending02_pattern(message):
    print('end02')
    long = message.text
    user = user_dict[message.chat.id]
    try:
        if long in answer.yes:
            user.long = 1
        elif long in answer.no:
            user.long = 0
        else:
            raise Exception("Выберите Да или Нет")
        end_last_pattern(message)
    except Exception:
        bot.send_message(message.chat.id, texts.error[lang])





def end_last_pattern(message):
    print('finish')
    user = user_dict[message.chat.id]
    doc_path = f'data/{user.ending}{user.intramural}{user.long}.docx'
    print(doc_path)
    if os.path.isfile(doc_path):
        bot.send_message(message.chat.id, texts.result[lang])
        with open(doc_path, 'rb') as document:
            bot.send_document(chat_id=message.chat.id, document=document, visible_file_name="Упражнения.docx")
    else:
        bot.send_message(message.chat.id, f'id: {message.chat.id}\nEnding: {user.ending}\n'
                                          f'Int:{user.intramural}\nLong:{user.long}')
    bot.send_message(message.chat.id, texts.restart[lang])
    bot.register_next_step_handler(message, process_restart_step)


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
#bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
#bot.load_next_step_handlers()

print('-----------')
print('Бот запущен')
print('-----------')

bot.infinity_polling(timeout=3, long_polling_timeout=30)
