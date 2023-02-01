from sklearn.feature_extraction.text import CountVectorizer  # pip install scikit-learn
from sklearn.linear_model import LogisticRegression
import sounddevice as sd  # pip install sounddevice
import vosk # pip install vosk

import speech_recognition as sr
from skills import *

import json
import queue
from dotenv import load_dotenv

import words
import voice

q = queue.Queue()
s_city = "Kurgan,RU"

model = vosk.Model('model_small')  # голосовую модель vosk нужно поместить в папку с файлами проекта
# https://alphacephei.com/vosk/
# https://alphacephei.com/vosk/models
device = sd.default.device  # <--- по умолчанию
# или -> sd.default.device = 1, 3, python -m sounddevice просмотр
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  # получаем частоту микрофона

def search_internet():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите что вы хотите найти: ")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="ru")
        print("Вы сказали: "+query)
        return query
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"

def commands():
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Скажите что вы хотите найти: ")
            audio = r.listen(source)
        try:
            our_speech = r.recognize_google(audio, language="ru")
            print("Вы сказали: " + our_speech)
            return our_speech
        except sr.UnknownValueError:
            return "ошибка"
        except sr.RequestError:
            return "ошибка"

def translate_ru():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        our_speech = r.recognize_google(audio, language="ru")
        print("Вы сказали: "+our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"


def translate_en():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        our_speech = r.recognize_google(audio, language="en")
        print("Вы сказали: "+our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"

def callback(indata, frames, time, status):
    '''
    Добавляет в очередь семплы из потока.
    вызывается каждый раз при наполнении blocksize
    в sd.RawInputStream'''

    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    '''
    Анализ распознанной речи
    '''
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return
    data.replace(list(trg)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    func_name = answer.split()[0]
    voice.va_speak(answer.replace(func_name, ''))
    exec(func_name + '()')


def q_callback(indata, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def find_rec():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
            else:
                print(rec.PartialResult())

#def weather():
    #city_name = s_city

    #try:
        # использование API-ключа, помещённого в .env-файл по примеру WEATHER_API_KEY = "01234abcd....."
       #weather_api_key = os.getenv("e6ef80c94a54fc9d869f7f9796f984f2")
       #open_weather_map = OWM(weather_api_key)

        # запрос данных о текущем состоянии погоды
       #weather_manager = open_weather_map.weather_manager()
       #observation = weather_manager.weather_at_place(city_name)
       #weather = observation.weather

        # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    #except:
        #voice.va_speak("Ошибка")
        #traceback.print_exc()
        #return

        # разбивание данных на части для удобства работы с ними
    #status = weather.detailed_status
    #temperature = weather.temperature('celsius')["temp"]
    #wind_speed = weather.wind()["speed"]
    #pressure = int(weather.pressure["press"] / 1.333)  # переведено из гПА в мм рт.ст.

    # вывод логов
    #print("Weather in " + city_name +
                 #":\n * Status: " + status +
                 #"\n * Wind speed (m/sec): " + str(wind_speed) +
                 #"\n * Temperature (Celsius): " + str(temperature) +
                 #"\n * Pressure (mm Hg): " + str(pressure), "yellow")

    # озвучивание текущего состояния погоды ассистентом (здесь для мультиязычности требуется дополнительная работа)
    #voice.va_speak(("It is {0} in {1}").format(status, city_name))
    #voice.va_speak(("The temperature is {} degrees Celsius").format(str(temperature)))
    #voice.va_speak(("The wind speed is {} meters per second").format(str(wind_speed)))
    #voice.va_speak(("The pressure is {} mm Hg").format(str(pressure)))


#def music():
    #voice.va_speak('какую хотите включить?')
    #mixer.music.play()
    #mixer.music.load('E:/Voice-Helper2.0/Music/' + commands() + '.mp3')
    #if 'стоп' in commands():
        #mixer.music.stop()

#def wikipedia():
    #voice.va_speak('Поиск в Википедии....')
    #our_speech = search_internet().query.replace('wikipedia', '')
    #results = wikipedia.summary(our_speech, sentences=5)
    #print(results)
    #voice.va_speak(results)

def random_number(command):
    ot = commands().command.find('от')
    do = commands().command.find('до')
    f_num = int(commands().command[ot + 3:do - 1])
    l_num = int(command[do + 3:])
    r = str(random.randint(f_num, l_num))
    print('Bot: ' + r)
    voice.va_speak(r)

def communication():
    z = ["У меня все хорошо,а как дела у вас?", "Всё Круто!Как Дела у вас?", "Отлично!Как дела у вас?",
         "У меня все отлично!Спасибо что интересуетесь,а как дела у вас?"]
    x = random.choice(z)
    voice.va_speak(x)

    if 'у меня всё хорошо' or 'у меня всё отлично' or 'у меня всё супер' or 'у меня всё нормально' or 'хорошо' or 'отлично' or 'супер' and 'нормально' in commands():
        z = ["Это прекрасно!", "Это хорошо!", "Отлично!", "Супер!", "Класс!"]
        x = random.choice(z)
        voice.va_speak(x)

    elif 'всё плохо' or 'так себе' or 'плохо' or 'не очень' and 'такое себе' in commands():
        z = ["Ничего страшного,поговорите со мной и всё будет хорошо"]
        x = random.choice(z)
        voice.va_speak(x)

def doing1():
    z = ["Ничего,а что делаете вы?","Да вот в интернете видео смотрел,а что делаете вы?","Смотрел картинки в интернете,а что делаете вы?","Играл в игры,а что делаете вы?"]
    x = random.choice(z)
    voice.va_speak(x)

    if 'ничего' or 'видео смотрел' or 'в интернете сидел' or 'фотки смотрел' or 'картинки смотрел' or 'в телефоне сидел' or 'в компьютере сидел' or 'телевизор смотрел' or 'сижу' or 'лежу' and 'общаюсь с тобой' in commands():
        z = ["Ясно", "Понятно"]
        x = random.choice(z)
        voice.va_speak(x)

def doing2():
    z = ["Ничем,а что делаете вы?", "Да вот в интернете видео смотрел,а что делаете вы?",
             "Смотрел картинки в интернете,а что делаете вы?", "Играл в игры,а что делаете вы?"]
    x = random.choice(z)
    voice.va_speak(x)

    if 'ничего' or 'видео смотрел' or 'в интернете сидел' or 'фотки смотрел' or 'картинки смотрел' or 'в телефоне сидел' or 'в компьютере сидел' or 'телевизор смотрел' or 'сижу' or 'лежу' and 'общаюсь с тобой' in commands():
        z = ["Ясно", "Понятно"]
        x = random.choice(z)
        voice.va_speak(x)

def main():
    '''
    Обучаем матрицу ИИ
    и постоянно слушаем микрофон
    '''

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())["text"]
                recognize(data, vectorizer, clf)
            else:
                print(rec.PartialResult())

#voice.speaker('Здравствуйте, я Айви, ваш помощник, то есть искусственный интеллект. Пожалуйста, скажите мне, как я могу вам помочь')

if __name__ == '__main__':
    load_dotenv()
    main()