import os
import json
from vosk import Model, KaldiRecognizer
import wave
from flask import Flask, render_template, request, jsonify
import pyaudio
import tempfile
import subprocess

app = Flask(__name__)
'''
def listen():
    """
    Записывает речь и преобразует в текст
    """
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer["text"]:
                return answer["text"]
           

def listen(audio_data):
    """
    Записывает речь и преобразует в текст
    """
    if (rec.AcceptWaveform(audio_data)) and (len(audio_data) > 0):
        answer = json.loads(rec.Result())
        if answer["text"]:
            return answer["text"]
'''

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    file = request.files['audio']

    # Создание временного файла для сохранения загруженного файла
    temp_file = tempfile.NamedTemporaryFile(suffix='.webm', delete=False)
    temp_file_path = temp_file.name
    temp_file.close()

    # Сохранение загруженного файла на диск
    file.save(temp_file_path)
    
    # Создание временного файла для сохранения преобразованного файла WAV
    wav_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False, overwrite=True)
    wav_file_path = wav_file.name
    wav_file.close()

    # Преобразование файла из формата WebM в WAV с использованием ffmpeg
    subprocess.run(['ffmpeg', '-i', temp_file_path, wav_file_path])

    print(f"File path: {wav_file_path}")
    print(f"File size: {os.path.getsize(wav_file_path)} bytes")

    # Открытие файла WAV с помощью библиотеки wave
    with wave.open(wav_file_path, 'rb') as wav_file:
        # Получение свойств аудиофайла
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Чтение аудиоданных
        audio_data = wav_file.readframes(num_frames)

        print(sample_rate, sample_width, num_channels, num_frames)

    rec.AcceptWaveform(audio_data)
    text = rec.Result()
    print(text)
    return text



if __name__ == '__main__':
    model = Model('vosk-model-small-ru-0.22')
    rec = KaldiRecognizer(model, 48000)
    p = pyaudio.PyAudio()


    app.run(debug=False)













