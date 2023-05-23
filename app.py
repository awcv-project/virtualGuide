from flask import Flask, render_template, request
from flask_socketio import SocketIO
import sounddevice as sd
import wavio as wv
import numpy as np
import requests
import json
import base64
from playsound import playsound



app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
socketio = SocketIO(app)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_recording', methods=['POST'])
def start_recording():
    print('recording')
    socketio.emit("record","Recording Started....")
    sampling_frequency=16000
    duration=5
    recording = sd.rec(int(duration * sampling_frequency),samplerate=sampling_frequency, channels=2)
    sd.wait()
    wv.write("input_prompt.wav", recording, sampling_frequency, sampwidth=2)
    print('recorded')
    playsound('./input_prompt.wav')
    return "Recording started"

@app.route('/play_voice', methods=['POST'])
def play_voice():
    # Convert audio to text
    audio_file = request.files["audio"]
    input_audio_path = './input_prompt.wav'

    # Save the audio file
    audio_file.save(input_audio_path)

    input_language = request.form["language"]
    target_language = request.form["target_language"]
    print(input_language)
    print(target_language)
    stt = json.loads(speech_to_text(input_language, input_audio_path))['transcript']
    responseText = "Question : " + stt
    socketio.emit("response", responseText)

    # Translate to English
    src_language = input_language
    tgt_language = 'english'
    translation = mt(src_language, tgt_language, stt)
    responseText = "Question in English: " + translation
    socketio.emit("response", responseText)

    # Get chatbot response
    input_question = translation
    chat_bot_response = chat_bot(input_question).strip()
    print('Chatbot response:', chat_bot_response)
    responseText = "Answer in English: " + chat_bot_response
    socketio.emit("response", responseText)

    # Translate chatbot response
    src_language = 'english'
    tgt_language = target_language
    translation = mt(src_language, tgt_language, chat_bot_response)
    print('Translated chatbot response:', translation)
    responseText = "Answer in input language: " + translation
    socketio.emit("response", responseText)

    # Capitalize the language string
    input_language = input_language.capitalize()

    # Convert chatbot response to speech
    gender = 'female'
    lang = target_language
    txt = translation
    output = text_to_speech(txt, gender, lang)['audio']
    file_name = "tts.mp3"
    wav_file = open(file_name, 'wb')
    decode_string = base64.b64decode(output)
    wav_file.write(decode_string)
    wav_file.close()
    print('Done converting to speech')
    responseText = "Done converting to speech" 
    socketio.emit("response", responseText)

    # Play the voice
    playsound('./tts.mp3')
    print('Playing sound using playsound')

    return "Voice played successfully."


# STT
def speech_to_text(input_language,input_audio_path):
    print("speech_to_text function called")
    url = "https://asr.iitm.ac.in/asr/v2/decode"
    audio_file = input_audio_path.split('/')[::-1][0]
    payload={'vtt': 'true', 'language': input_language}
    files=[('file',(audio_file,open(input_audio_path,'rb'),'application/octet-stream'))]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    # text = json.loads(response.text)
    # output = text["transcript"]
    return response.text


# MT (TTT)
def mt(src_language,tgt_language,transcript):
    # print(src_language,tgt_language,transcript)
    payload = {'src_language':src_language,'tgt_language':tgt_language,'transcript': transcript,'source_vtt':None,'translator_choice':'meta_ai'}
    response = requests.post('https://asr.iitm.ac.in/test1/translate',data = payload).json()
    return response['mt_out']


# CHAT-GPT
def chat_bot(input_question):
    url = 'https://api.openai.com/v1/completions'
    
    payload = json.dumps({
    "model": "text-davinci-003",
    "prompt": input_question,
    "max_tokens": 150,
    "temperature": 0.9
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    output = json.loads(response.text)['choices'][0]['text']
    print(response.text)
    return output


# TTS
def text_to_speech(text,gender,lang):
	url = "https://asr.iitm.ac.in/ttsv2/tts"
	payload = json.dumps({
		"input": text,
		"gender": gender,
		"lang": lang,
		"alpha": 0.95,
		"segmentwise":"True"
	})
	headers = {'Content-Type': 'application/json'}
	response = requests.request("POST", url, headers=headers, data=payload).json()
	return response

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5002)