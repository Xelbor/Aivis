import sys
import subprocess
import datetime
from translate import Translator
import webbrowser
import voice
import app
import random
from pygame import mixer
from googlesearch import search  # поиск в Google
import traceback
import pyjokes
import ctypes
import time
import os

mixer.init()
translator_en = Translator(from_lang="ru", to_lang="en")
translator_ru = Translator(from_lang="en", to_lang="ru")

def translate_ru_en():
    tranlatedtext = translator_en.translate(app.translate_ru())
    voice.va_speak(tranlatedtext)

def translate_en_ru():
    tranlatedtext = translator_ru.translate(app.translate_en())
    voice.va_speak(tranlatedtext)

def joke():
    joke = pyjokes.get_joke()
    translatejoke = translator_ru.translate(joke)
    voice.va_speak(translatejoke)

def lock_window():
    voice.va_speak("закрываю")
    ctypes.windll.user32.LockWorkStation()

def number():
    z = ["Один", "Два", "Три", "Четыре", "Пять", "Шесть", "Семь", "Восемь", "Девять", "Десять"]
    x = random.choice(z)
    voice.va_speak(x)

def timer():
    responce = app.commands()
    timing = time.time()
    if time.time() - timing > responce:
        timing = time.time()
        voice.va_speak("время прошло")

def note():
    try:
        an = app.commands()
        ca = 1
        f = open("note.txt", "a")
        voice.va_speak("Я запомнил, что бы прочитать эту заметку скажите: прочитай заметку")
        voice.engine.runAndWait()
        an45 = an[len("запомни"):] + an
        f.write(an45)
        f.close()

    except:
        voice.va_speak("Заметка не может быть пустой! Если хотите создать новую, скажите запомни и то что вы хотите сохранить.")
        voice.engine.runAndWait()
        print("Ошибка! Вы пытаетесь создать пустую заметку!")

def read_note():
    ca = 1
    f = open("note.txt", "r")
    if f.read(1) == "":
        voice.va_speak("Похоже у вас еще нет заметок. Если хотите создать новую, скажите запомни и то что вы хотите сохранить.")
        voice.engine.runAndWait()
    else:
        st = f.read()
        print(st)
        voice.va_speak("И так вот что я помню:")
        voice.engine.runAndWait()
        voice.va_speak(st)
        voice.engine.runAndWait()
        voice.va_speak("Если хотите их удалить, скажите удалить все заметки.")
        voice.engine.runAndWait()
        f.close()

def delete_note():
    ca = 1
    print("Вы уверены?")
    voice.va_speak("Вы хотите удалить все заметки? Подтвердите пожайлуста.")
    answer = app.commands()
    if "да" or "подтверждаю" in answer or "утверждаю" in answer:
        ca = 1
        print("Удаление...")
        f = open("note.txt", "w")
        f.write("")
        voice.va_speak("Удаление заметок завершено.")
        voice.engine.runAndWait()
    else:
        print("Отмена...")
        voice.va_speak("Подтверждение не получено, заметки не удалены. Ну вы меня и напугали...")
        voice.engine.runAndWait()

#def soundMute():
    #Sound.mute()
    #cur = Sound.current_volume()

#def volumeMax():
    #Sound.volume_max()

#def volumeUp():
    #Sound.volume_up()

#def volumeDown():
    #Sound.volume_down()

#def volumeSet1():
    #vol = int(input("10"))
    #Sound.volume_set(vol)

#def volumeSet2():
    #vol = int(input("20"))
    #Sound.volume_set(vol)

#def volumeSet3():
   #vol = int(input("30"))
    #Sound.volume_set(vol)

#def volumeSet4():
    #vol = int(input("40"))
    #Sound.volume_set(vol)

#def volumeSet5():
    #vol = int(input("50"))
    #Sound.volume_set(vol)

#def volumeSet6():
    #vol = int(input("60"))
    #Sound.volume_set(vol)

#def volumeSet7():
    #vol = int(input("70"))
    #Sound.volume_set(vol)

#def volumeSet8():
    #vol = int(input("80"))
    #Sound.volume_set(vol)

#def volumeSet9():
    #vol = int(input("90"))
    #Sound.volume_set(vol)

#def volumeSet10():
    #vol = int(input("100"))
    #Sound.volume_set(vol)

def repeat():
    listen = app.commands()
    voice.va_speak(listen)

def browser():
    webbrowser.open('https://www.youtube.com', new=2)

def search_for_term_on_google():

    search_term = app.search_internet()

    # открытие ссылки на поисковик в браузере
    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)

    # альтернативный поиск с автоматическим открытием ссылок на результаты (в некоторых случаях может быть небезопасно)
    search_results = []
    try:
        for _ in search(search_term,  # что искать
                        tld="com",  # верхнеуровневый домен
                        num=1,  # количество результатов на странице
                        start=0,  # индекс первого извлекаемого результата
                        stop=1,  # индекс последнего извлекаемого результата (я хочу, чтобы открывался первый результат)
                        pause=1.0,  # задержка между HTTP-запросами
                        ):
            search_results.append(_)
            webbrowser.get().open(_)

    # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    except:
        voice.va_speak("Кажется, у нас ошибка. Смотрите журналы для получения дополнительной информации")
        traceback.print_exc()
        return

    print(search_results)
    voice.va_speak("Вот что я нашел для запроса {} в Google".format(search_term))

def search_for_video_on_youtube():

    search_term = app.search_internet()
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    voice.va_speak("Вот что я нашел для {} на YouTube".format(search_term))

def coin():
    z = ["Орёл", "Решка"]
    x = random.choice(z)
    voice.va_speak(x)

def sleep():
    ca = 1
    voice.va_speak("Хорошо, микрофон выключен. Для продолжения работы нажмите энтр")
    voice.engine.runAndWait()
    an4925479864 = input("[ПАУЗА] Нажмите enter: ")
    voice.va_speak("Привет-привет, чем займемся?.")
    voice.engine.runAndWait()

def fastsleep():
    ca = 1
    voice.engine.runAndWait()
    an4925479864 = input("[ПАУЗА] Нажмите enter: ")
    voice.va_speak("Я вышел из сна")
    voice.engine.runAndWait()

def game():
    try:
        subprocess.Popen('E:/Unity/Unity Hub/Unity Hub.exe')
    except:
        voice.va_speak('Путь к файлу не найден, проверьте, правильный ли он')

def what_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    voice.va_speak(f"Время {strTime}")

def unity():
    try:
        subprocess.Popen('E:/Unity/Unity Hub/Unity Hub.exe')
    except:
        voice.va_speak('Путь к файлу не найден, проверьте, правильный ли он')

def hello():
    z = ["Привет!", "Здравствуйте!", "Добрый День!"]
    x = random.choice(z)
    voice.va_speak(x)

def goodbye():
    z = ["До встречи!", "Ещё увидимся!"]
    x = random.choice(z)
    voice.va_speak(x)
    sys.exit()

def discord():
    try:
        subprocess.Popen('E:/Unity/Unity Hub/Unity Hub.exe')
    except:
        voice.va_speak('Путь к файлу не найден, проверьте, правильный ли он')

def offpc():
    os.system('shutdown /p /f')
    print('пк был бы выключен, но команде # в коде мешает;)))')

def rebootpc():
    os.system('shutdown -r -t 0')
    print('пк был бы перезагружен, но команде # в коде мешает;)))')

def offBot():
    '''Отключает бота'''
    sys.exit()

def skills():
    if 'да' or 'потверждаю' in app.commands():
        voice.va_speak('я умею запустить exe файл, выключить пк, перезагрузить пк, уйти в сон, рассказать анекдот, подбрасывать монетку, обновлять самого себя, называть рандомное число, повторять слова за вами, создавать заметку, переводить ваши предложения, гуглить, искать на ютубе, ну и говорить сколько время')
    elif 'нет' in app.commands():
        pass

def passive():
    '''Функция заглушка при простом диалоге с ботом'''
    pass


