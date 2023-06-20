import os
import time
import threading

def get_triggers():
    with open('name.txt', 'r') as r:
        name = r.read()
        name = name.lower()
        word_list = name.split(', ')
        return set(word_list)

def watch_name_file_changes():
    last_modified = 0
    while True:
        if os.path.exists('name.txt'):
            modified_time = os.path.getmtime('name.txt')
            if modified_time > last_modified:
                TRIGGERS = get_triggers()
                last_modified = modified_time
        time.sleep(1)

# Запускаем функцию в отдельном потоке
watcher_thread = threading.Thread(target=watch_name_file_changes)
watcher_thread.start()

data_set = {
    'привет': 'skills.hello',
    'поздаровайся': 'skills.hello',
    'какая сейчас погода': 'skills.weather',
    'какая погода на улице': 'skills.weather',
    'что там на улице': 'skills.weather',
    'сколько градусов': 'skills.degrees',
    'сколько время': 'skills.what_time',
    'время': 'skills.what_time',
    'найди на ютубе': 'skills.watch_youtube',
    'ищи на ютубе': 'skills.watch_youtube',
    'поищи на ютубе': 'skills.watch_youtube',
    'ищи на ютуюбе': 'skills.watch_youtube',
    'поищи на ютуб': 'skills.watch_youtube',
    'найди на ютюб': 'skills.watch_youtube',
    'найди видео на ютуб': 'skills.watch_youtube',
    'включи': 'skills.watch_youtube',
    'включи видео': 'skills.watch_youtube',
    'запусти браузер': 'skills.browser',
    'открой браузер': 'skills.browser',
    'запусти ютуб': 'skills.browser_youtube',
    'запусти ютюб': 'skills.browser_youtube',
    'открой программу': 'skills.open_programm',
    'открой приложение': 'skills.open_programm',
    'открой игру': 'skills.open_programm',
    'подбрось монетку': 'skills.coin',
    'кинь монетку': 'skills.coin',
    'найди в гугле': 'skills.search_for_term_on_google',
    'найди в гугл': 'skills.search_for_term_on_google',
    'ищи в гугле': 'skills.search_for_term_on_google',
    'найди википедии': 'skills.search_wikipedia',
    'ищи в википедии': 'skills.search_wikipedia',
    'найди в википедии': 'skills.search_wikipedia',
    'найди статью': 'skills.search_wikipedia',
    'найди статью о': 'skills.search_wikipedia',
    'найди статью в википедии': 'skills.search_wikipedia',
    'найди статью википедии': 'skills.search_wikipedia',
    'что такое': 'skills.parse_wikipedia',
    'переведи текст на английский': 'skills.translate_ru_en',
    'переведи текст на русский': 'skills.translate_en_ru',
    'выключи компьютер': 'skills.offpc',
    'перезагрузи компьютер': 'skills.rebootpc',
    'перезагрузить компьютер': 'skills.rebootpc',
    'отключись': 'skills.offBot',
    'стоп': 'skills.sleep',
    'поставь таймер': 'skills.timer',
    'запусти таймер': 'skills.timer',
    'установи таймер': 'skills.timer',
    'таймер': 'skills.timer',
    'засеки': 'skills.timer',
    'останови таймер': 'skills.stop_timer',
    'сколько осталось до таймера': 'skills.print_remaining_time',
    'выбери рандомное слово': 'random_words',
    'выбери случайное слово': 'random_words',
    'рандомное слово': 'skills.random_words',
    'случайное слово': 'skills.random_words',
    'заткнись': 'skills.shut_up',
    'замолчи': 'skills.shut_up',
    'помолчи': 'skills.shut_up',
    'замолкни': 'skills.shut_up',
    'зайди в сон': 'skills.sleep',
    'уйди в сон': 'skills.sleep',
    'напомни':'skills.read_note',
    'напоминание':'skills.reminder',
    'создай напоминание':'skills.reminder',
    'сделай напоминания':'skills.reminder',
    'напомни мне':'skills.reminder',
    'сколько осталось до напоминания': 'skills.print_remaining_time_reminder',
    'сколько осталось до напоминание': 'skills.print_remaining_time_reminder',
    'останови напоминание': 'skills.cancel_reminder',
    'создай заметку':'skills.note',
    'прочитай заметку':'skills.read_note',
    'удалить все заметки':'skills.delete_note',
    'удали все заметки':'skills.delete_note',
    'случайное число':'skills.random_number_between',
    'случайные числа': 'skills.random_number_between',
    'рандомное число':'skills.random_number_between',
    'назови случайное число':'skills.number',
    'назови рандомное число ':'skills.number',
    'расскажи анекдот':'skills.joke',
    'расскажи шутку':'skills.joke',
    'обновить ассистента':'skills.updating',
    'обнови ассистента':'skills.updating',
    'обновись':'skills.updating',
    'работаешь':'skills.work',
    'ты тут':'skills.work',
    'что ты умеешь': 'skills.skills',
    'твои умения': 'skills.skills'
}
