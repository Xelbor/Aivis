from common import samplerate, callback, q, model, device, commands, ui, app
import sounddevice as sd
import json
import voice
import vosk
import words
from win10toast import ToastNotifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import number_converter
import skills
import threading
import random
#import pymorphy2    удалено до версии 2.1 т.к из за него проблемы с компилированной версией
import update
import sys

def show_notif_update():
    if ui.checkBox_notifications.isChecked():
        update.get_updatings()

# Показ уведомления о том что программа полностью работает
def show_notification():
    toaster = ToastNotifier()
    toaster.show_toast(
        "Айвис готов к работе",
        "Программа запущена и готова к работе",
        icon_path="Interface/Icon.ico",
        duration=5
    )

def recognize(data, vectorizer, clf):
    search = ""
    #morph = pymorphy2.MorphAnalyzer()
    # проверяем есть ли имя бота в data, если нет, то return
    trg = words.get_triggers().intersection(data.split())

    # Если нет триггера, то продолжаем прослушивание
    if not trg:
        return

    # Проверка наличия дополнительных слов после триггера
    if any(word in data.lower() for word in trg):
        if len(data.split()) > len(trg):
            # удаляем имя бота из текста
            data = data.replace(list(trg)[0], '')

            # ищем команды для поиска в гугл, на ютубе и в википедии
            youtube_trigger = ['найди на ютубе', 'найди на ютуб', 'найди видео на ютуб', 'найди видео', 'ищи на ютубе', 'открой на ютубе', 'включи']
            google_trigger = ['найди в гугле', 'ищи в гугле', 'открой в гугле']
            wiki_trigger = ['найди википедии', 'ищи в википедии', 'открой википедию', 'найди в википедии',
                            'найди статью', 'найди статью о', 'найди статью в википедии', 'найди статью', 'что такое']
            timer_trigger = ['поставь таймер', 'запусти таймер', 'установи таймер', 'засеки']
            reminder_trigger = ['создай напоминание', 'сделай напоминание', 'напомни мне', 'напомни о']
            random_numbers_trigger = ['случайное число между', 'случайное число от', 'рандомное число от',
                                      'рандомное число между', 'генерируй случайное число от',
                                      'генерируй случайное число между']
            weather_trigger = ['какая сейчас погода в', 'какая сейчас погода в городе', 'какая погода на улице в', 'что там на улице в']

            # Проверка для youtube_trigger
            for trigger in youtube_trigger:
                if trigger in data.lower():
                    # проверяем, есть ли запрос на поиск после команды
                    search = data.lower().replace(trigger, '').strip()
                    if not search:
                        skills.watch_youtube(None)
                    # запускаем функцию для поиска видео на YouTube
                    skills.watch_youtube(search)
                    return

            # Проверка для google_trigger
            for trigger in google_trigger:
                if trigger in data.lower():
                    # получаем строку, которую нужно искать в Google
                    search = data.lower().replace(trigger, '').strip()
                    if not search:
                        skills.search_for_term_on_google(None)
                    # запускаем функцию для поиска на Google
                    skills.search_for_term_on_google(search)
                    return

            # Проверка для wiki_trigger
            for trigger in wiki_trigger:
                if trigger in data.lower():
                    # получаем строку, которую нужно искать в Википедии
                    query = data.lower().replace(trigger, '').strip()
                    if not query:
                        # если пользователь не указал запрос, запрашиваем его у пользователя
                        voice.va_speak("Что бы вы хотели найти в Википедии?")
                        query = commands().strip()
                    # запускаем функцию для поиска информации в Википедии
                    skills.search_wikipedia(query)
                    return

            # Проверка для timer_trigger
            for trigger in timer_trigger:
                if trigger in data.lower():
                    # проверяем, есть ли время для таймера после команды
                    time_set = data.lower().replace(trigger, '').strip()
                    if not time_set:
                        # если его нет, то спрашиваем пользователя, на сколько поставить таймер
                        voice.va_speak("На сколько вы хотите поставить таймер?")
                        time_set = commands()
                    # запускаем функцию таймера
                    skills.timer(time_set)
                    return

            # Проверка для reminder_trigger
            for trigger in reminder_trigger:
                if trigger in data.lower():
                    reminder_text = data.lower().replace(trigger, '').strip()
                    if reminder_text:
                        if 'через' in reminder_text:
                            text_time_list = reminder_text.split('через')
                            if len(text_time_list) == 2:
                                reminder_text = text_time_list[0].strip()
                                time_set = text_time_list[1].strip()
                                skills.reminder(time_set, reminder_text)
                                return
                            else:
                                voice.va_speak("Произошла ошибка в обработке напоминания, пожалуйста, укажите время.")
                        else:
                            skills.reminder(None, reminder_text)
                            return

            # Проверка для random_numbers_trigger
            for trigger in random_numbers_trigger:
                if trigger in data.lower():
                    # Получаем первое и второе число для генерации случайного числа в заданном диапазоне
                    numbers = data.lower().replace(trigger, '').strip()
                    if numbers:
                        numbers_list = numbers.split('и')
                        if len(numbers_list) == 2:
                            number1 = number_converter.words_to_numbers(numbers_list[0])
                            number1 = int(number1.strip())
                            number2 = number_converter.words_to_numbers(numbers_list[1])
                            number2 = int(number2.strip())
                            if number1 > number2:
                                number1, number2 = number2, number1
                            skills.random_number_between(number1, number2)
                            return
                        else:
                            voice.va_speak("Произошла ошибка в обработчике чисел, возможно вы указали больше чисел чем 2")

            # Это код полного распознавания речи функции погоды

            # Она сейчас отключена из за того что модуль pymorph
            # выдает ошибку в компилированной версии программы. Проблема будет исправленна в версии 2.1

            #for trigger in weather_trigger:
            #    if trigger in data.lower():
            #        # проверяем, есть ли запрос на поиск после команды
            #        city = data.lower().replace(trigger, '').strip()
            #        if not city:
            #            skills.weather(None)
            #        else:
            #            city_normalized = morph.parse(city)[0].normal_form
            #            skills.weather(city_normalized)
            #            return

            # получаем вектор полученного текста
            # сравниваем с вариантами, получая наиболее подходящий ответ
            text_vector = vectorizer.transform([data]).toarray()[0]
            answer = clf.predict([text_vector])[0]
            # получение имени функции из ответа из data_set
            func_name = answer.split()[0]
            # Довольно важные строки, они отвечают за выполнения команд
            if func_name == "watch_youtube":
                # Функции исключения команд, это если например после функции в скобках есть какой нибудь аргумент, то функция не будет включаться если вы не добавите в исключения
                exec(f"{func_name}('{search}')", globals(), locals())
            elif func_name == "search_for_term_on_google":
                exec(f"{func_name}('{search}')", globals(), locals())
            elif func_name == "search_wikipedia":
                exec(f"{func_name}('{search}')", globals(), locals())
            elif func_name == "timer":
                exec(f"{func_name}()", globals(), locals())
            elif func_name == "reminder":
                exec(f"{func_name}()", globals(), locals())
            elif func_name == "get_weather":
                exec(f"{func_name}()", globals(), locals())
            else:
                exec(f"{func_name}()", globals(), locals())

        else:
            # Если будет сказан только триггер, то он спросит что вы хотели? или что? или да?
            askings = ["Что?", "Да?", "Чем могу помочь?", "Чего нибудь хотели?", "Чем могу быть полезен?"]
            result = random.choice(askings)
            voice.va_speak(result)

            # если сработал только триггер, то дальше функция не выполняется
            if len(trg) == 1 and not data.strip():
                return

def main():
    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    ui.label_aivis.setText("Aivis Активен")

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            lineEdit_text = ui.lineEdit_name.text()

            if lineEdit_text == "":
                ui.lineEdit_name.setText("Айви, Айвис")

            with open("name.txt", "w") as w:
                w.write(lineEdit_text)

            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)
            else:
                # Преобразование строки в словарь
                input_string = rec.PartialResult()
                data_result = json.loads(input_string)

                # Извлечение слова "partial"
                result = data_result["partial"]

                # Выводим результат с микрофона
                print(result)
                # Выводим результат с микрофона на интерфейс
                ui.label_print_voice.setText(result)

if __name__ == "__main__":
    # Создаем потоки для прослушивания микрофона и отправки уведомления
    mic_thread = threading.Thread(target=main)
    notif_thread = threading.Thread(target=show_notification)
    update_notif_thread = threading.Thread(target=show_notif_update)

    # Запускаем потоки
    update_notif_thread.start()
    mic_thread.start()
    notif_thread.start()

    sys.exit(app.exec_())
