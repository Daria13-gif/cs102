import json
from datetime import datetime
from time import sleep

import gspread
import pandas as pd
import telebot
import validators

bot = telebot.TeleBot("6055195312:AAHUl2VodKXqqT6YxNmd-E16Fg79wxphXLo")
# создаем две переменные ROW и COL и присваиваем им значения 0. В этом случае,
# мы можем использовать эти переменные для хранения значений строк и столбцов
# в таблице
ROW, COL = 0, 0
table = True

# функция, котора опредделят разделитель даты по второму символу
def find_divider(date):
    return date[2]

# функция используется для проверки валидности даты
# Функция принимает два аргумента: строку "date", которая содержит дату для
# проверки, и строку "divider", которая определяет разделитель между днями,
# месяцами и годами в строке даты.
def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    # опеределяем текущую дату
    divider = find_divider(date)
    today = datetime.now()
    # пытаемся преобразовать строку "date" в объект даты с помощью
    # функции "convert_date"
    try:
        date_new = convert_date(date, divider)
    #  Если преобразование даты не удалось, функция возвращает "False"
    except Exception:
        return False
    # Если преобразование прошло успешно, то функция вычисляет разницу
    # между датой "date_new" и текущей датой в днях и сохраняет в
    # переменную "delta".
    delta = (date_new - today).days
    if date_new.date() < today.date() or delta > 365:
        return False
    return True


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    if validators.url(url) is True:
        return validators.url(url)
    else:
        return validators.url("https://" + url)


def convert_date(date: str = "01/01/00", divider: str = "/"):
    """Конвертируем дату из строки в datetime"""
    # Функция начинается с разделения строки "date" на отдельные составляющие
    # (день, месяц, год) с помощью метода split()
    ddmmyyyy = date.split(divider)
    return datetime(day=int(ddmmyyyy[0]), month=int(ddmmyyyy[1]), year=2000 + int(ddmmyyyy[2]))


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = "1RiJ8Q312ZwElswXb-xhKipxdC520b9DV9uXWYzTKCwM"
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")
    sleep(2)
    start(message)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)

        sheet_id = tables[max(tables)]["id"]
        gc = gspread.service_account(filename="credentials.json")
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.sheet1
        ws_values = worksheet.get_all_values()
        df = pd.DataFrame.from_records(ws_values[1:], columns=ws_values[0])
        # Преобразуем Google-таблицу в таблицу pandas
        return worksheet, tables[max(tables)]["url"], df
    except FileNotFoundError:
        return None


# Эта функция вызывается всякий раз, когда пользователь отправляет сообщение боту
def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        msg = bot.send_message(message.chat.id, "Отправь мне полную ссылку на таблицу")
        # регистрируем обработчик для следующего сообщения, отправляемого пользователем,
        # которое будет использоваться для подключения к указанному листу
        bot.register_next_step_handler(msg, connect_table)

    elif message.text == "Редактировать предметы":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Добавить новый предмет")
        markup.row("Изменить информацию о предмете")
        markup.row("Удалить предмет")
        markup.row("Удалить все предметы")
        info = bot.send_message(message.chat.id, "Выбери действие", reply_markup=markup)
        bot.register_next_step_handler(info, choose_subject_action)

    elif message.text == "Редактировать дедлайн":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Добавить новый дедлайн")
        markup.row("Редактировать дедлайн")
        bot.send_message(message.chat.id, "Выбери действие", reply_markup=markup)
        bot.register_next_step_handler(message, choose_subject)

    elif message.text == "Посмотреть дедлайны на этой неделе":
        # создаем объект datetime для текущей даты и времени
        today = datetime.now()
        # вызываем функцию access_current_sheet, которая подключается к Google
        # Sheets API и возвращает данные из текущего листа
        table_data = access_current_sheet()
        # извлекаем данные таблицы в переменную df, которая является экземпляром
        # объекта "pandas.DataFrame"
        df = table_data[2]
        # создаем переменную, которая будет использоваться для подсчета
        # количества дедлайнов на ближайшей неделе
        deadline_count = 0
        # идем по строкам таблицы и по стоблцам (начиная со второго,
        # так как первый содержит названия работ)
        deadlines = ""
        for i in range(df.shape[0]):
            for j in range(2, df.shape[1]):
                # извлекает данные ячейки i, j из df
                cell_data = df.iat[i, j]
                # есть ли данные в ячейке
                if cell_data:
                    date = convert_date(cell_data)
                    delta = date - today
                    # находится ли дедлайн в пределах следующей недели и если по
                    # модулю меньше либо равен 1(для сегодняшнего дедлайна)
                    if 0 <= delta.days < 7 or abs(delta.days) <= 1:
                        # счетчик дедлайнов увеличивается на 1, и бот отправляет сообщение
                        # пользователю с информацией о работе и дедлайне. Сообщение
                        # формируется с помощью метода bot.send_message с использованием
                        # форматирования строк и HTML-разметки
                        deadline_count += 1
                        deadlines += f"{df.iat[i, 0]}. Работа №{j - 1}\nДедлайн <b>{df.iat[i, j]}</b>" + "\n"
        if deadlines:
            bot.send_message(
                message.chat.id,
                deadlines,
                parse_mode="HTML",
            )
        else:
            bot.send_message(message.chat.id, "Дедлайнов на ближайшей неделе нет. Гуляем!")
        sleep(deadline_count)
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить новый предмет":
        info = bot.send_message(message.chat.id, "Введи название предмета, который хочешь добавить")
        bot.register_next_step_handler(info, add_new_subject)

    elif message.text == "Изменить информацию о предмете":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Изменить название предмета")
        markup.row("Изменить ссылку на таблицу с баллами по предмету")
        info = bot.send_message(message.chat.id, "Выбери действие", reply_markup=markup)
        bot.register_next_step_handler(info, choose_subject)

    elif message.text == "Удалить предмет":
        choose_subject(message)

    elif message.text == "Удалить все предметы":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Да, гори оно всё огнём")
        markup.row("Нет, ещё пригодится")
        info = bot.send_message(message.chat.id, "Точно удалить всё?", reply_markup=markup)
        bot.register_next_step_handler(info, choose_removal_option)


def choose_deadline_action(message, action):
    """Выбираем действие в разделе Редактировать дедлайн"""
    # вызываем функцию access_current_sheet, которая подключается к Google
    # Sheets API и возвращает данные из текущего листа
    table_data = access_current_sheet()
    ws = table_data[0]
    global ROW, COL
    # функция ищет ячейку в таблице Google Sheets с помощью метода find(),
    # используя текст, переданный в аргументе message.text
    # Результат сохраняется в переменную cell
    cell = ws.find(message.text)
    # глобальным переменным ROW и COL присваиваются соответствующие
    # значения из найденной ячейки cell
    ROW = cell.row
    COL = cell.col
    info = bot.send_message(message.chat.id, "Введи номер работы")
    bot.register_next_step_handler(info, update_subject_deadline, action)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да, гори оно всё огнём":
        clear_subject_list(message)

    elif message.text == "Нет, ещё пригодится":
        bot.send_message(message.chat.id, "Как скажете-с!")
        sleep(2)
        start(message)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    # создается объект разметки клавиатуры "markup" с помощью класса
    # "telebot.types.ReplyKeyboardMarkup". Это позволяет создать кнопки,
    # которые пользователь может нажимать, чтобы выбрать определенный вариант
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # с помощью функции "access_current_sheet", получаем текущую таблицу данных, извлекаем
    # из нее данные в формате pandas dataframe и итерируемся по ним, добавляя каждый предмет
    # в разметку клавиатуры
    table_data = access_current_sheet()
    # извлекаем данные таблицы в переменную df
    df = table_data[2]
    for i in range(df.shape[0]):
        markup.row(df.at[i, "Subject"])
    # бот отправляет сообщение пользователю с просьбой выбрать предмет с помощью
    # созданной ранее разметки клавиатуры
    info = bot.send_message(message.chat.id, "Выбери предмет", reply_markup=markup)
    if message.text == "Изменить название предмета":
        # функция "bot.register_next_step_handler" будет вызвана, чтобы
        # зарегистрировать следующий шаг обработки сообщения пользователя
        bot.register_next_step_handler(info, update_subject_title)
    elif message.text == "Изменить ссылку на таблицу с баллами по предмету":
        bot.register_next_step_handler(info, update_subject_url)
    elif message.text == "Удалить предмет":
        bot.register_next_step_handler(info, delete_subject)
    elif message.text == "Добавить новый дедлайн" or message.text == "Редактировать дедлайн":
        action = message.text
        bot.register_next_step_handler(info, choose_deadline_action, action)


def update_subject_deadline(message, action):
    """Обновляем дедлайн"""
    global COL
    # функция проверяет, что пользователь ввел целое число в сообщении
    if not message.text.isdigit():
        info = bot.send_message(
            message.chat.id,
            "Ошибочка. Введи номер работы как целое число без дополнительных знаков",
        )
        bot.register_next_step_handler(info, update_subject_deadline)
        return
    # функция проверяет, что введенное число не превышает 100
    if int(message.text) > 100:
        info = bot.send_message(
            message.chat.id,
            "Вряд ли у тебя так много работ. Введи номер работы как целое число, не большее, чем 100",
        )
        bot.register_next_step_handler(info, update_subject_deadline)
        return
    # функция получает доступ к текущему листу таблицы и загружает DataFrame, содержащий информацию
    # о дедлайнах по выбранному предмету
    table_data = access_current_sheet()
    ws = table_data[0]
    # извлекаем данные таблицы в переменную df
    df = table_data[2]
    # если введенный номер работы больше, чем количество работ, уже
    # содержащихся в таблице, то бот отправляет сообщение об ошибке
    if action == "Редактировать дедлайн" and int(message.text) > df.shape[1] - 2:
        info = bot.send_message(
            message.chat.id,
            "Такой работы нет (пока). Попробуй еще раз",
        )
        bot.register_next_step_handler(info, update_subject_deadline, action)
        return
    # функция определяет текущую дату дедлайна для выбранной работы и
    # проверяет, есть ли она в таблице
    current_date = ws.cell(ROW, COL + int(message.text) + 1).value
    # Если есть, то бот запрашивает у пользователя новую дату дедлайна
    # в формате "DD/MM/YYYY"
    if current_date:
        info = bot.send_message(
            message.chat.id,
            f"Cейчас по этой работе стоит дедлайн <b>{current_date}</b>.\nВведи новую дату в формате\nDD/MM/YY",
            parse_mode="HTML",
        )
    # Если же такой даты нет, то бот отправляет сообщение об ошибке
    elif action == "Редактировать дедлайн":
        info = bot.send_message(
            message.chat.id,
            "Такой работы нет (пока). Попробуй еще раз",
        )
        bot.register_next_step_handler(info, update_subject_deadline, action)
        return
    else:
        info = bot.send_message(message.chat.id, "Введи дату дедлайна в формате\nDD/MM/YY")
    # функция сохраняет номер выбранной работы в переменную COL и регистрирует следующий шаг
    # обработки ввода - обновление ячейки с новым дедлайном в таблице.
    COL += int(message.text) + 1
    bot.register_next_step_handler(info, update_cell_datetime)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    # функция вызывает функцию access_current_sheet, которая получает данные из текущей Google-таблицы,
    # а именно: рабочий лист (ws) и pandas-датафрейм (df), содержащий информацию о предметах и дедлайнах
    table_data = access_current_sheet()
    ws = table_data[0]
    df = table_data[2]
    # проверяем, что введенный предмет не совпадает с предметом из спискаву
    if message.text in df.Subject.values.tolist():
        info = bot.send_message(
            message.chat.id,
            "Такой предмет уже есть. Попробуй еще раз",
        )
        bot.register_next_step_handler(info, add_new_subject)
        return

    # добавляем новую строку в таблицу, содержащую только название предмета,
    # которое пользователь ввел в сообщении
    else:
        ws.append_row([message.text])
        # просим ввести полную ссылку на таблицу с баллами по этому предмету и регистрируем обработчик
        # следующего сообщения с помощью bot.register_next_step_handler, который будет вызван,
        # когда пользователь отправит ссылку
        info = bot.send_message(message.chat.id, "Введи полную ссылку на таблицу с баллами по этому предмету")
        bot.register_next_step_handler(info, add_new_subject_url)


def add_new_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    # Если пользовательский ввод содержит "www." в первых четырех символах, функция добавляет "https://"
    # в начало строки ввода
    text = "https:///" + message.text if (len(message.text) > 3 and message.text[:4] == "www.") else message.text
    # функция проверяет, является ли результирующий URL допустимым, вызывая другую функцию is_valid_urlфункция
    # проверяет, является ли результирующий URL допустимым, вызывая другую функцию is_valid_url
    is_valid = is_valid_url(text)
    if not is_valid:
        new = bot.send_message(message.chat.id, "Cсылка не рабочая. Введи нормальную.")
        bot.register_next_step_handler(new, add_new_subject_url)
        return
    # Если URL-адрес действителен, функция вызывает функцию access_current_sheet для
    # получения рабочего листа и данных, который содержит список объектов и
    # соответствующие им URL-адреса листов
    table_data = access_current_sheet()
    ws = table_data[0]
    # извлекаем данные таблицы в переменную df
    df = table_data[2]
    # функция обновляет рабочий лист новым URL-адресом листа для новой темы,
    # добавляя новую строку к рабочему листу и вставляя URL-адрес во второй столбец
    ws.update_cell(df.shape[0] + 1, 2, text)
    bot.send_message(message.chat.id, "Предмет успешно добавлен")
    sleep(2)
    start(message)


def update_subject_title(message):
    """Обновляем информацию о предмете в Google-таблице"""
    # access_current_sheet() - возвращает данныее текущей таблицы
    table_data = access_current_sheet()
    ws = table_data[0]

    global ROW, COL
    # происходит поиск ячейки в таблице, содержащей текст сообщения
    # пользователя (cell = ws.find(message.text)).
    # Результат поиска записывается в переменную cell
    cell = ws.find(message.text)
    ROW = cell.row
    COL = cell.col
    new = bot.send_message(message.chat.id, "Введи новое название")

    # функция register_next_step_handler регистрирует следующую функцию
    # update_cell_data в качестве обработчика следующего шага.
    # Эта функция будет вызвана, когда пользователь введет новое название
    # предмета. Вторым параметром update_cell_data передается текст,
    # введенный пользователем в new.text.

    bot.register_next_step_handler(new, update_cell_data, new.text)


# аналогично предыдущей функции
def update_subject_url(message):
    """Обновляем ссылку на предмет в Google-таблице"""
    table_data = access_current_sheet()
    ws = table_data[0]
    global ROW, COL
    cell = ws.find(message.text)
    ROW = cell.row
    COL = cell.col + 1
    new = bot.send_message(message.chat.id, "Введи новую ссылку")
    bot.register_next_step_handler(new, update_cell_data, new.text)


def update_cell_data(message, action):
    if action == "Введи новую ссылку" or action == "Cсылка не рабочая. Введи нормальную.":
        # функция добавляет https:// к введенной ссылке, если пользователь не добавил этот
        # префикс и введенная ссылка начинается с www
        text = "https://" + message.text if (len(message.text) > 3 and message.text[:4] == "www.") else message.text
        # функция проверяет, является ли введенная ссылка действительной ссылкой с помощью библиотеки validators
        is_valid = validators.url(text)
        if not is_valid:
            new = bot.send_message(message.chat.id, "Cсылка не рабочая. Введи нормальную.")
            bot.register_next_step_handler(new, update_cell_data, new.text)
            return
        message.text = text
    global ROW, COL
    # функция получает данные текущей Google-таблицы с помощью функции access_current_sheet(),
    # выбирает первый лист таблицы (ws = table_data[0]), и обновляет ячейку с помощью метода
    # update_cell() для строки ROW и столбца COL с новым значением message.text
    table_data = access_current_sheet()
    ws = table_data[0]
    df = table_data[2]
    # проверяем, что введенный предмет не совпадает с предметом из списка
    if message.text in df.Subject.values.tolist():
        info = bot.send_message(
            message.chat.id,
            "Такой предмет уже есть. Попробуй еще раз",
        )
        bot.register_next_step_handler(info, update_cell_data, action)
        return
    else:
        ws.update_cell(ROW, COL, message.text)
        bot.send_message(message.chat.id, "Готово!")
        sleep(2)
        start(message)


def update_cell_datetime(message):
    # Если сообщение не соответствует формату даты или не имеет адекватных временных рамок,
    # то функция отправляет сообщение об ошибке
    if not is_valid_date(message.text):
        info = bot.send_message(
            message.chat.id,
            "Ошибочка. Дата должна соответствовать форматy DD/MM/YYYY и иметь адекватные временные рамки."
            "\nПопробуй ещё раз",
        )
        bot.register_next_step_handler(info, update_cell_datetime)
        return

    global ROW, COL
    # функция получает данные текущей Google-таблицы с помощью функции access_current_sheet(),
    # выбирает первый лист таблицы (ws = table_data[0]), и обновляет ячейку с помощью метода
    # update_cell() для строки ROW и столбца COL с новым значением message.text
    table_data = access_current_sheet()
    ws = table_data[0]
    # cипользуем replace, чтобы заменить разделитель, заданный пользователем
    ws.update_cell(ROW, COL, message.text.replace(find_divider(message.text), "/"))
    bot.send_message(message.chat.id, "Готово!")
    sleep(2)
    start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    # получаем данные текущей Google-таблицы с помощью функции access_current_sheet(),
    # выбирает первый лист таблицы (ws = table_data[0]), и ищет ячейку в листе, которая
    # содержит значение message.text, используя метод find(). Этот метод возвращает
    # объект ячейки, который содержит информацию о строке (cell.row) и столбце (cell.col) ячейки.
    table_data = access_current_sheet()
    ws = table_data[0]
    cell = ws.find(message.text)
    ws.delete_rows(cell.row)
    bot.send_message(message.chat.id, "Исполнено!")
    sleep(2)
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    table_data = access_current_sheet()
    ws = table_data[0]
    ws.clear()
    bot.send_message(message.chat.id, "Теперь таблица девственно чиста!")
    sleep(2)
    start(message)


@bot.message_handler(commands=["start"])
def greetings(message):
    bot.send_message(
        message.chat.id,
        "На связи Octobotus!\nСвоими 8 щупальцами помогу тебе разгрести дедлайны",
    )
    # функция вызывает функцию access_current_sheet(), чтобы получить данные текущей Google-таблицы
    table_data = access_current_sheet()
    # Если данные получены успешно (if table_data), функция извлекает информацию о предметах из третьего
    # листа таблицы (df = table_data[2]) и отправляет сообщение "Доступные предметы" пользователю с помощью
    # bot.send_message().
    if table_data:
        df = table_data[2]
        bot.send_message(message.chat.id, "Доступные предметы")
        # функция проходит по каждой строке данных о предметах
        # создаем строку, в которую сохраняем все наши предметы
        subjects = ""
        for i in range(df.shape[0]):
            # добавляем каждый предмет в строку
            subjects += f"<a href='{df.at[i, 'Link']}'> {df.at[i, 'Subject']} </a>" + "\n"
            # и отправляет сообщение пользователю с помощью bot.send_message().
            # Это сообщение содержит имя предмета в виде ссылки
            # В параметре parse_mode устанавливается значение "HTML",
            # чтобы ссылка была отображена как активная.
            # Также отключается предварительный просмотр веб-страницы,
            # чтобы ссылка не отображалась как изображение.
        bot.send_message(
            message.chat.id,
            subjects,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    start(message)


@bot.message_handler(commands=["start"])
def start(message):
    global table
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if table:
        start_markup.row("Подключить Google-таблицу")
        table = False
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Редактировать дедлайн")
    # start_markup.row("Внести новый дедлайн") несогласованность действий
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)
    pass


if __name__ == "__main__":
    bot.infinity_polling()
