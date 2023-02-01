#import sounddevice as sd
#import time
#import torch

#language = 'ru'
#model_id = 'v3_1_ru'
#sample_rate = 48000
#speaker = 'aidar'
#put_accent = True
#put_yo = True
#device = torch.device('cpu')
#text = "Приветствую дорогой друг"

#model, _= torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       #model='silero_tts',
                                       #language=language,
                                       #speaker=model_id)
#model.to(device)

#def va_speak(what: str):
    #audio = model.apply_tts(text=what+"..",
                            #speaker=speaker,
                            #sample_rate=sample_rate,
                            #put_accent=put_accent,
                            #put_yo=put_yo)

    #sd.play(audio, sample_rate * 1.05)
    #time.sleep((len(audio) / sample_rate) + 0.5)
    #sd.stop()



import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)				#скорость речи


def va_speak(text):
	engine.say(text)
	engine.runAndWait()