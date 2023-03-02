import requests

def update_assistent():
    file_url = "https://raw.githubusercontent.com/Xelbor/Aivis/main/update.py"
    r = requests.get(file_url)

    with open("update.py", "wb") as code:
        code.write(r.content)

    file_url = "https://raw.githubusercontent.com/Xelbor/Aivis/main/voice.py"
    r = requests.get(file_url)

    with open("voice.py", "wb") as code:
        code.write(r.content)

    file_url = "https://raw.githubusercontent.com/Xelbor/Aivis/main/app.py"
    r = requests.get(file_url)

    with open("app.py", "wb") as code:
        code.write(r.content)

    file_url = "https://raw.githubusercontent.com/Xelbor/Aivis/main/words.py"
    r = requests.get(file_url)

    with open("words.py", "wb") as code:
        code.write(r.content)

    file_url = "https://raw.githubusercontent.com/Xelbor/Aivis/main/skills.py"
    r = requests.get(file_url)

    with open("skills.py", "wb") as code:
        code.write(r.content)

    file_url = "https://raw.githubusercontent.com/Xelbor/Aivis/main/AivisCore.py"
    r = requests.get(file_url)

    with open("AivisCore.py", "wb") as code:
        code.write(r.content)