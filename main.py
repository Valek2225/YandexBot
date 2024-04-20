import time
from PyPDF2 import PdfFileWriter, PdfReader
import requests
from lxml import html
from config import LOGIN, PASSWORD
import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import BOT_TOKEN
from json import loads, dump, load
from pathlib import Path
import urllib
import urllib.request

chatId = -1
count_submissions = 0
status_code = {
    0: 'Полное решение',
    8: 'Полное решение',
    2: 'Ошибка во время исполнения программы',
    3: 'Превышено время выполнения',
    7: 'Превышено время выполнения',
    5: 'Неправильный ответ',
    12: 'Превышено ограничение по памяти',
    1: 'Ошибка компиляции',
}
running_code = [96, 98, 377]
types = ['VSOSH']
stages = ['Final_stage', 'Regional_stage']
years = [str(x) for x in range(2009, 2020)]
days = [str(x) for x in range(1, 3)]
problems = ['A', 'B', 'C', 'D']
langs = {
    'Free Pascal 3.0': 1,
    'GNU C 11.2': 2,
    'GNU C++ 11.2': 3,
    'Turbo Pascal': 7,
    'Java JDK 15': 18,
    'PHP PHP 7.2': 22,
    'Python 3.9': 27,
    'PascalABC 3.7': 30,
}
file_id = open('problems.json', 'r')
id_problems = load(file_id)
file_id.close()

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
# create session
session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
loginPageResp = session.get("https://informatics.msk.ru/login/index.php", stream=True)

loginPageResp.raise_for_status()
loginPageResp.raw.decode_content = True

parser = html.parse(loginPageResp.raw)

loginToken = parser.xpath("//form[@class='mt-3' and @id='login']/input[@name='logintoken']/@value")
login_anchor = parser.xpath("//form[@class='mt-3' and @id='login']/input[@name='anchor']/@value")
if not loginToken: raise ValueError("Field 'logintoken' was not found")

loginTokenVal = loginToken[0]
loginAnchorVal = login_anchor[0]
# login in informatics.msk.ru
loginResp = session.post(
    "https://informatics.msk.ru/login/index.php",
    data={
        'anchor': loginAnchorVal,
        "logintoken": loginTokenVal,
        "username": LOGIN,
        "password": PASSWORD
    }
)


# get chat id
def getChatId():
    req = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates')
    req_json = req.json()
    chat_id = req_json['result'][0]['message']['chat']['id']
    return chat_id


# submit problem
def submit(Document, data):
    global count_submissions
    file_name = Document.file_name
    id_file = Document.file_id
    sessionTg = requests.Session()
    sessionTg.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={id_file}'
    firstRespTg = sessionTg.get(url)
    firstRespTgJson = firstRespTg.json()
    url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{firstRespTgJson['result']['file_path']}"
    extension = Path(file_name).suffix
    f_submit = open(f'submissions/{str(count_submissions)}{extension}', 'wb')
    with urllib.request.urlopen(url) as f:
        f_submit.write(f.read())
    f_submit.close()
    problem_id = id_problems[data['Type']][data['Stage']][data['Year']][data['Day']][data['Problem']]['id']
    if data['Lang'] not in langs.keys():
        return ['К сожалению этот язык пока не поддерживается( мы это исправим']
    submitResp = session.post(f"https://informatics.msk.ru/py/problem/{problem_id}/submit",
                              files={'file': open(f'submissions/{str(count_submissions)}{extension}', 'rb')},
                              data={
                                  'lang_id': langs[data['Lang']],
                                  'file': f'{str(count_submissions)}{extension}'
                              })
    # get request for check status code
    url = (
        f"https://informatics.msk.ru/py/problem/{problem_id}/filter-runs?problem_id={problem_id}&from_timestamp=-1&to_timestamp=-1&"
        "user_id=854350&lang_id=-1&status_id=-1&statement_id=0&count=10&with_comment=&page=1&group_id=0&course_id=0")
    subResp = session.get(url)
    r = subResp.json()
    while r['data'][0]['ejudge_status'] in running_code:
        subResp = session.get(url)
        r = subResp.json()
    ans = r['data'][0]
    count_submissions += 1
    score = ans['ejudge_score']
    return [f"{status_code[ans['ejudge_status']]}",
            f"Баллы: {max(0, score)}"]


# send file statement
def sendDocs(data):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
    data_send = {'chat_id': chatId, 'file': 'Problem.pdf'}
    try:
        url_req = id_problems[data['Type']][data['Stage']][data['Year']][data['Day']][data['Problem']]['statement']
        r = requests.get(url_req)
        with open("Problem.pdf", "wb") as f:
            f.write(r.content)
        files = {'document': open('Problem.pdf', 'rb')}
        response = requests.post(url, data=data_send, files=files)
    except Exception as e:
        print(e)
        return -1
    return 0


# start
async def start(update, context):
    global chatId
    chatId = getChatId()
    reply_keyboard = [types]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите олимпиаду", reply_markup=markup)
    return 1


# selct type
async def selectType(update, context):
    reply_keyboard = [stages]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите этап", reply_markup=markup)
    context.user_data['Type'] = update.message.text
    return 2


# select stage
async def selectStage(update, context):
    reply_keyboard = [years]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите год", reply_markup=markup)
    context.user_data['Stage'] = update.message.text
    return 3


# select year
async def selectYear(update, context):
    reply_keyboard = [days]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите день", reply_markup=markup)
    context.user_data['Year'] = update.message.text
    return 4


# select day
async def selectDay(update, context):
    reply_keyboard = [problems]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    context.user_data['Day'] = update.message.text
    await update.message.reply_text("Выберите задачу", reply_markup=markup)
    return 5


# select problem
async def selectProblem(update, context):
    context.user_data['Problem'] = update.message.text
    req = id_problems[context.user_data['Type']][context.user_data['Stage']][context.user_data['Year']][
        context.user_data['Day']][context.user_data['Problem']]
    id = req['id']
    if id == -1:
        await update.message.reply_text('Упсс... Такой задачи не нашлось')
        return ConversationHandler.END
    else:
        reply_keyboard = [[str(x) for x in langs.keys()]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            f"Задача: {repr(id_problems[context.user_data['Type']][context.user_data['Stage']][context.user_data['Year']][context.user_data['Day']][context.user_data['Problem']]['name'])}")
        if sendDocs(context.user_data) != 0:
            await update.message.reply_text("Кажется условия к этой задаче не нашлось(")
            return ConversationHandler.END
        await update.message.reply_text("Выберите язык", reply_markup=markup)
        return 6


# select lang submission
async def selectLang(update, context):
    context.user_data['Lang'] = update.message.text
    if context.user_data['Lang'] not in langs.keys():
        await update.message.reply_text('Упсс... Такого языка нет...')
        return ConversationHandler.END
    else:
        await update.message.reply_text("Загрузите файл")
        return 7


# select file/answer
async def selectFile(update, context):
    doc = update.message.document
    answer = submit(doc, context.user_data)
    for ans in answer:
        await update.message.reply_text(f'{ans}')
    context.user_data.clear()
    return ConversationHandler.END


# brake dialog
async def stop(update, context):
    markup = ReplyKeyboardRemove()
    await update.message.reply_text("Всего доброго!", reply_markup=markup)
    context.user_data.clear()
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, selectType)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, selectStage)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, selectYear)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, selectDay)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, selectProblem)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, selectLang)],
            7: [MessageHandler(filters.ALL & ~filters.COMMAND, selectFile)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
