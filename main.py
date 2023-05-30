import json
import sys
import vosk
import pyaudio
import requests
import pyttsx3

model = vosk.Model('vosk-model-small-ru-0.4')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels = 1, rate = 16000, input = True, frames_per_buffer = 8000)
stream.start_stream()

tts = pyttsx3.init()
rate = tts.getProperty('rate')
tts.setProperty('rate', rate - 40)
volume = tts.getProperty('volume')
tts.setProperty('volume', volume + 0.9)
voices = tts.getProperty('voices')
tts.setProperty('voice', 'ru')

api_data = None


def read_from_file():
    file = open('lessons.txt', encoding='utf-8')
    text = ''
    for line in file:
        text += line
    file.close()
    for voice in voices:
        if voice.name == 'Anna':
            tts.setProperty('voice', voice.id)
    tts.say(text)
    tts.runAndWait()


def listen():
    while True:
        data = stream.read(4000,exception_on_overflow=False)
        if(record.AcceptWaveform(data) and len(data)>0):
            ans=json.loads(record.Result())
            if(ans['text']):
                yield ans['text']

def lessons():
    url = "https://www.boredapi.com/api/activity"
    response = requests.get(url)
    lessons_data = response.json()
    return lessons_data

def write_to_file():
    file = open("lessons.txt","w",encoding='utf-8')
    file.write(str(api_data))
    file.close()


for text in listen():
    if text == 'пока':
        print("Прощайте")
        sys.exit(0)
    elif text == 'прочитай':
        read_from_file()
    elif text == 'сохранить' and api_data:
        write_to_file()
        print("Сохранено")
    elif text == 'случайный':
        api_data = lessons()
        print(f"Занятие:\nНазвание: {str(api_data['activity'])}\nТип: {str(api_data['type'])}\nКоличество участников: {api_data['participants']}\nЦена: {api_data['price']}\nСсылка: {str(api_data['link'])}\nПароль: {str(api_data['key'])}\nДоступность: {api_data['accessibility']}")
        tts.say(f"Занятие:\nНазвание: {str(api_data['activity'])}\nТип: {str(api_data['type'])}\nКоличество участников: {api_data['participants']}\nЦена: {api_data['price']}\nСсылка: {str(api_data['link'])}\nПароль: {str(api_data['key'])}\nДоступность: {api_data['accessibility']}")
        tts.runAndWait()
    elif text == 'название' and api_data:
        print(f"Название: {str(api_data['activity'])}")
        tts.say(f"Название: {str(api_data['activity'])}")
        tts.runAndWait()
    elif text == 'участники' and api_data:
        print(f"Количество участников: {api_data['participants']}")
        tts.say(f"Количество участников: {api_data['participants']}")
        tts.runAndWait()
    elif text == 'следующая':
        api_data = lessons()
        print(f"Занятие:\nНазвание: {str(api_data['activity'])}\nТип: {str(api_data['type'])}\nКоличество участников: {api_data['participants']}\nЦена: {api_data['price']}\nСсылка: {str(api_data['link'])}\nПароль: {str(api_data['key'])}\nДоступность: {api_data['accessibility']}")
        tts.say(f"Занятие:\nНазвание: {str(api_data['activity'])}\nТип: {str(api_data['type'])}\nКоличество участников: {api_data['participants']}\nЦена: {api_data['price']}\nСсылка: {str(api_data['link'])}\nПароль: {str(api_data['key'])}\nДоступность: {api_data['accessibility']}")
        tts.runAndWait()