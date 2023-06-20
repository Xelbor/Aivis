import subprocess
import sys
import datetime
from translate import Translator
import webbrowser
import urllib.request
import urllib.parse
import common
import voice
import random
from googlesearch import search
import pyjokes
import os
import time
import wikipedia
import requests
from bs4 import BeautifulSoup
import threading
from common import commands, translate_en, ui
import re
import number_converter
import json
import keyboard

translator_en = Translator(from_lang="ru", to_lang="en")
translator_ru = Translator(from_lang="en", to_lang="ru")

def translate_weather_description(description):
    translation_dict = {
        "clear sky": "ясное небо",
        "few clouds": "малооблачно",
        "scattered clouds": "рассеянные облака",
        "broken clouds": "облачно с прояснениями",
        "overcast clouds": "пасмурно",
        "shower rain": "ливень",
        "rain": "дождь",
        "thunderstorm": "гроза",
        "snow": "снег",
        "mist": "туман",
        "smoke": "дымка",
        "haze": "мгла",
        "sand/ dust whirls": "песчаные/пыльные вихри",
        "fog": "туман",
        "sand": "песок",
        "dust": "пыль",
        "volcanic ash": "вулканический пепел",
        "squalls": "шквалы",
        "tornado": "торнадо"
    }

    if description in translation_dict:
        return translation_dict[description]
    else:
        return description

def weather(city_name=None):
    if city_name is None:
        city_name = ui.comboBox_city.currentText()

    api_key = "e6ef80c94a54fc9d869f7f9796f984f2"  # Замените на свой API-ключ

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Получение температуры в градусах Цельсия
    }

    response = requests.get(base_url, params=params)
    data = json.loads(response.text)

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        translated_description = translate_weather_description(description)

        voice.va_speak(f"В городе {city_name} сейчас {temperature}°C, {translated_description}.")
    else:
        voice.va_speak("Не удалось получить данные о погоде в городе.")

def translate_ru_en():
    voice.va_speak("Скажите что хотите перевести")
    tranlatedtext = translator_en.translate(commands())
    voice.va_speak(tranlatedtext)

def translate_en_ru():
    voice.va_speak("Скажите что хотите перевести")
    tranlatedtext = translator_ru.translate(translate_en())
    voice.va_speak(tranlatedtext)

def joke():
    joke = pyjokes.get_joke()
    translatejoke = translator_ru.translate(joke)
    voice.va_speak(translatejoke)

def note():
    try:
        voice.va_speak("Что вы хотите записать в заметку?")
        text = commands()
        f = open("note.txt", "a")
        voice.va_speak("Я записал, что бы прочитать эту заметку скажите: прочитай заметку")
        note = text[len("запиши"):] + text
        f.write(note)
        f.close()

    except:
        voice.va_speak("Заметка не может быть пустой! Если хотите создать новую, скажите запомни и то что вы хотите сохранить.")
        print("Ошибка! Вы пытаетесь создать пустую заметку!")

def read_note():
    r = open("note.txt", "r")
    if r.read(1) == "":
        voice.va_speak("Похоже у вас еще нет заметок. Если хотите создать новую, скажите запомни и то что вы хотите сохранить.")
    else:
        writed = r.read()
        print(writed)
        voice.va_speak("И так вот что я записал:")
        voice.va_speak(writed)
        voice.va_speak("Если хотите их удалить, скажите удалить все заметки.")
        r.close()

def delete_note():
    print("Вы уверены?")
    voice.va_speak("Вы хотите удалить все заметки? Подтвердите пожайлуста.")
    answer = commands()
    if "да" or "подтверждаю" in answer or "конечно" in answer:
        print("Удаление...")
        f = open("note.txt", "w")
        f.write("")
        voice.va_speak("Удаление заметок завершено.")
    else:
        print("Отмена...")
        voice.va_speak("Подтверждение не получено, заметки не удалены. Ну вы меня и напугали...")

def browser():
    voice.va_speak("Открываю...")
    webbrowser.open('https://www.google.ru/')

def browser_youtube():
    voice.va_speak("Открываю...")
    webbrowser.open('https://www.youtube.com/')

def search_for_term_on_google(search_term=None):
    if search_term is None:
        voice.va_speak("Скажите, что вы хотите найти по запросу в Google")
        search_term = commands()

    voice.va_speak("Ищу в Google: " + search_term)

    # открываем ссылку на поисковик в браузере
    url = "https://google.com/search?q=" + search_term

    if ui.checkBox_open_results.isChecked():
        webbrowser.get().open(url)

    # получаем список ссылок на результаты поиска
    search_results = []
    # открываем первую ссылку из результатов поиска
    try:
        for _ in search(search_term,
                        tld="com",
                        num=1,
                        start=0,
                        stop=1,
                        pause=1.0,
                        ):
            search_results.append(_)
            if ui.checkBox_open_first_result.isChecked():
                webbrowser.get().open(_)

            response = requests.get(_)
            if ui.checkBox_read_text.isChecked():
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    text = soup.get_text()
                    sentences = text.split(".")
                    # озвучивание запроса
                    voice.va_speak(sentences[1] + ".")
    except:
        voice.va_speak("По запросу " + search_term + " в Google ничего не найдено")

def watch_youtube(search_query=None):
    if search_query is None:
        voice.va_speak("Что вы хотите найти на YouTube?")
        search_query = commands()

    voice.va_speak("Ищу на YouTube: " + search_query)
    search = urllib.parse.quote(search_query)
    youtube_search = "https://www.youtube.com/results?search_query=" + search
    html = urllib.request.urlopen(youtube_search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    if len(video_ids) > 0:
        video_url = "https://www.youtube.com/watch?v=" + video_ids[0]
        if ui.checkBox_first_video.isChecked():
            webbrowser.get().open(video_url)
        webbrowser.get().open(youtube_search)
    else:
        voice.va_speak("Извините, я не смог найти видео на YouTube по запросу: " + search_query)
        webbrowser.get().open(youtube_search)

def open_programm():
    fileName = ui.lineEdit_review.text()

    if not fileName:
        print("Путь к файлу не указан.")
        return

    if not os.path.exists(fileName):
        print("Указанный путь к файлу недействителен.")
        return

    try:
        print("Открываю...")
        subprocess.run(fileName)
    except Exception as e:
        print("Ошибка при открытии файла:", str(e))

def random_words():
    voice.va_speak("Скажите первое слово")
    word_one = commands()
    voice.va_speak("Скажите второе слово")
    word_two = commands()
    choose_words = [word_one, word_two]
    choise = random.choice(choose_words)
    print(choise)
    random_result = ["Случайное слово: ", "Мой выбор пал на слово: ", "Мой выбор пал на: ", "Результат: ", "Результат случайного слова: "]
    random_result = random.choice(random_result)
    voice.va_speak(random_result + choise)

def random_number_between(number1=None, number2=None):
    if number1 is None:
        voice.va_speak("скажите первое число")
        number1 = commands()
        number1 = number_converter.words_to_numbers(number1)
        number1 = int(number1)

    if number2 is None:
        voice.va_speak("скажите второе число")
        number2 = commands()
        number2 = number_converter.words_to_numbers(number2)
        number2 = int(number2)

    # Проверяем, что number1 меньше number2
    if number1 > number2:
        number1, number2 = number2, number1

    # Генерируем случайное число в заданном диапазоне
    random_number = random.randint(number1, number2)

    voice.va_speak(random_number)

def search_wikipedia(query):
    if not query:
        voice.va_speak("скажите, что хотите найти")
        query = commands()
        query = query.strip()

    query = query.strip()
    query_words = query.split()
    topic = " ".join(query_words)
    print("Запрос в Википедию: ", topic)
    try:
        page = wikipedia.page(topic)
        print("Найденная страница: ", page.title)
        summary = page.summary.split('.')
        for sentence in summary[:2]:
            translator_ru = Translator(from_lang="en", to_lang="ru")
            translated_text = translator_ru.translate(sentence)
            voice.va_speak(translated_text)
    except wikipedia.exceptions.PageError:
        voice.va_speak("К сожалению, я не смог найти информацию по вашему запросу")

timer_thread = None
remaining_time = 0
stop_flag = False

def end_timer(time_set):
    global remaining_time, stop_flag
    remaining_time = time_set
    start_time = time.time()

    while remaining_time > 0 and not stop_flag:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        remaining_time = time_set - elapsed_time

    remaining_time = 0
    if not stop_flag:
        voice.va_speak(f"Сработал таймер, который вы поставили на {time_set} секунд")
    stop_flag = False

def timer(time_set):
    try:
        global timer_thread

        if not time_set:
            voice.va_speak("На сколько времени поставить таймер?")
            time_set = commands()
            time_set = time_set.lower()
            time_set = number_converter.words_to_numbers(time_set)
        voice.va_speak(f"Поставлен таймер {time_set}")
        time_set = time_set.lower()
        time_set = number_converter.words_to_numbers(time_set)

        # Удаляем предлог "на"
        time_set = re.sub(r'\bна\b', '', time_set).strip()

        # Изменяем единицы времени на секунды
        if "секунд" in time_set:
            multiplier = 1
            time_set = time_set.replace("секунду", "").replace("секунд", "").strip()
        elif "минут" in time_set:
            multiplier = 60
            time_set = time_set.replace("минуту", "").replace("минуты", "").replace("минут", "").strip()
            print(time_set)
        elif "час" in time_set:
            multiplier = 3600
            time_set = time_set.replace("час", "").replace("часа", "").strip()
        else:
            multiplier = 1

        time_set = int(number_converter.words_to_numbers(time_set))
        time_set *= multiplier

        # Запускаем таймер в отдельном потоке
        timer_thread = threading.Thread(target=end_timer, args=(time_set,))
        timer_thread.start()

    except:
        voice.va_speak("Ошибка при конвертации чисел, попробуйте повторить время ещё раз")

def stop_timer():
    global timer_thread, stop_flag
    if timer_thread and timer_thread.is_alive():
        stop_flag = True
        timer_thread.join()
        voice.va_speak("Таймер остановлен.")

def get_remaining_time():
    return remaining_time

def print_remaining_time():
    global timer_thread
    remaining = get_remaining_time()
    if remaining > 0:
        voice.va_speak(f"Осталось {remaining:.0f} секунд до конца таймера.")
    else:
        voice.va_speak("Таймер уже завершен.")

reminder_thread = None
remaining_time_reminder = 0
stop_flag_reminder = False

def set_reminder(time_set, reminder_text):
    global remaining_time_reminder, stop_flag_reminder
    remaining_time_reminder = time_set
    start_time = time.time()

    while remaining_time_reminder > 0 and not stop_flag_reminder:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        remaining_time_reminder = time_set - elapsed_time

    remaining_time_reminder = 0
    if not stop_flag_reminder:
        voice.va_speak(f"Сработало напоминание {reminder_text}, которое вы поставили на {time_set} секунд")
    stop_flag_reminder = False

def reminder(time_set=None, reminder_text=None):
    try:
        global reminder_thread

        if not time_set:
            voice.va_speak("Через сколько времени вам напомнить?")
            time_set = commands()
            time_set = time_set.lower()

        if not reminder_text:
            voice.va_speak("О чем вам напомнить?")
            reminder_text = commands()

        # Удаляем предлог "через"
        time_set = re.sub(r'\bчерез\b', '', time_set).strip()

        # Изменяем единицы времени на секунды
        if "секунд" in time_set:
            multiplier = 1
            time_set = time_set.replace("секунду", "").replace("секунд", "").strip()
        elif "минут" in time_set:
            multiplier = 60
            time_set = time_set.replace("минуту", "").replace("минут", "").strip()
        elif "час" in time_set:
            multiplier = 3600
            time_set = time_set.replace("час", "").replace("часа", "").strip()
        else:
            multiplier = 1

        time_set = int(number_converter.words_to_numbers(time_set))
        time_set *= multiplier

        # Запускаем напоминание в отдельном потоке
        reminder_thread = threading.Thread(target=set_reminder, args=(time_set, reminder_text))
        reminder_thread.start()
        voice.va_speak(f"Вы поставили напоминание на {time_set} секунд {reminder_text}")
    except:
        voice.va_speak("Ошибка при конвертации чисел, попробуйте повторить время ещё раз")

def cancel_reminder():
    global reminder_thread, stop_flag_reminder
    if reminder_thread and reminder_thread.is_alive():
        stop_flag_reminder = True
        reminder_thread.join()
        voice.va_speak("Напоминание остановлено остановлен.")

def get_remaining_time_reminder():
    global remaining_time_reminder
    return remaining_time_reminder

def print_remaining_time_reminder():
    global remaining_time_reminder
    remaining = get_remaining_time_reminder()
    if remaining is not None and remaining > 0:
        voice.va_speak(f"Осталось {remaining:.0f} секунд до окончания напоминания.")
    else:
        voice.va_speak("Таймер уже завершен.")

def coin():
    z = ["Орёл", "Решка"]
    x = random.choice(z)
    voice.va_speak(x)

def sleep():
    key = ui.captured_key

    # Выполните действия для режима сна
    voice.va_speak("Хорошо, микрофон выключен. Для продолжения работы нажмите кнопку которую вы указали в интерфейсе программы")
    common.ui.label_aivis.setText("Aivis находится в состоянии сна")

    while True:
        if keyboard.read_key() == key:
            break

        time.sleep(0.1)  # Пауза в 0.1 секунды

    voice.va_speak("Я вышел из сна")

def shut_up():
    key = ui.captured_key

    common.ui.label_aivis.setText("Aivis находится в состоянии сна")

    while True:
        if keyboard.read_key() == key:
            break

        time.sleep(0.1)  # Пауза в 0.1 секунды

    voice.va_speak("Я вышел из сна")

def what_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    voice.va_speak(f"Время {strTime}")

def hello():
    z = ["Привет!", "Здравствуйте!", "Добрый День!"]
    x = random.choice(z)
    voice.va_speak(x)

def goodbye():
    z = ["До встречи!", "Ещё увидимся!"]
    x = random.choice(z)
    voice.va_speak(x)
    sys.exit()

def offpc():
    voice.va_speak("отключаю компьютер")
    os.system('shutdown /p /f')

def rebootpc():
    voice.va_speak("перезагружаю компьютер")
    os.system('shutdown -r -t 0')

def offBot():
    voice.va_speak("Отключаюсь, Пока!")
    sys.exit()

def work():
    voice.va_speak("Конечно")

def skills():
    voice.va_speak("следущее перечесление функций будет очень большое, потвердите что вы хотите это услышать")
    if 'да' or 'потверждаю' in commands():
        voice.va_speak('я умею запустить exe файл, выключить компьютер, перезагрузить компьютер, уйти в сон, рассказать анекдот, подбрасывать монетку, обновлять самого себя, называть рандомное число, повторять слова за вами, создавать заметку, переводить ваши предложения, гуглить, искать на ютубе, ну и говорить сколько время. Также у меня есть отдельная документация по моему исходному коду и умениям.')
    elif 'нет' in commands():
        pass
