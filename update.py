import requests
import time
import voice
from win10toast import ToastNotifier

# URL для получения информации о файлах в репозитории
url = "https://api.github.com/repos/Xelbor/Aivis/contents"


# Функция для получения списка файлов в репозитории
def get_files():
    response = requests.get(url)
    response_json = response.json()

    if not isinstance(response_json, list):
        voice.va_speak("К сожалению, произошла проблема с api гитхаб. Проверяйте обновления программы в своем браузере")

    files = []
    for item in response_json:
        if isinstance(item, dict) and item.get("type") == "file":
            files.append(item["name"])
    return files


def get_updatings():
    # Инициализация объекта для отправки уведомлений
    toaster = ToastNotifier()

    # Получение списка файлов в репозитории перед запуском приложения
    initial_files = get_files()

    # Бесконечный цикл для проверки наличия обновлений
    while True:
        # Получение списка файлов в репозитории
        files = get_files()

        # Список новых файлов
        new_files = [f for f in files if f not in initial_files]

        # Если есть новые файлы, отправить уведомление
        if new_files:
            message = "Новые файлы были добавлены в репозитории Xelbor/Aivis:\n" + "\n".join(new_files)
            toaster.show_toast("Новое обновление!", message, duration=5, icon_path="Interface/Icon.ico")

        # Обновление списка файлов перед следующей проверкой
        initial_files = files[:]

        # Пауза на 1 минуту перед следующей проверкой
        time.sleep(60)
