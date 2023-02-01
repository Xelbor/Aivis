import voice
import requests
from clint.textui import progress

def update_assistant():
    voice.va_speak("После загрузки файла замените эту версию новой")
    url = 'https://github.com/Xelbor/Aivis'
    r = requests.get(url, stream=True)

    with open("voice.py" "app.py" "skills.py" "words.py", "wb") as Pypdf:
        total_length = int(r.headers.get('content-length'))

        for ch in progress.bar(r.iter_content(chunk_size=2391975),
                           expected_size=(total_length / 1024) + 1):
            if ch:
                Pypdf.write(ch)