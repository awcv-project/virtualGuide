from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO
import requests
import json
import base64
import ssl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_user')
def handle_new_user(data):
    client_id = data['id']
    print('\n'+f"New user connected with ID: {client_id}")

@app.route('/play_voice', methods=['POST'])
def play_voice():
    # Convert audio to text

    input_language = request.form["language"]
    target_language = request.form["target_language"]
    clientID = request.form["clientId"]
    audio_file = request.files["audio"]
    input_audio_path = clientID+'.wav'

    # Save the audio file
    audio_file.save(input_audio_path)
    print('*************************************************************')
    print('\n'+'Client ID: '+clientID, ' | Input Language: ', input_language, ' | Target Language: ', target_language)
    try:
        stt = json.loads(speech_to_text(input_language, input_audio_path))['transcript']
        responseText = "Question : " + stt
        socketio.emit("response", responseText,room=clientID)
    except Exception as e:
        error_message = "Speech To Text Error:"  + str(e)
        print('\n'+error_message)
        socketio.emit("response", error_message,room=clientID)

    # Translate to English
    src_language = input_language
    tgt_language = 'english'
    translation = mt(src_language, tgt_language, stt)
    responseText = "Question in English: " + translation
    socketio.emit("response", responseText,room=clientID)

    # Get chatbot response
    try:
        input_question = translation
        chat_bot_response = chat_bot(input_question).strip()
        # print('\nChatbot response:', chat_bot_response)
        responseText = "Response in English: " + chat_bot_response
        socketio.emit("response", responseText,room=clientID)
    except Exception as e:
        error_message = "Chat GPT ResponseError:" + str(e)
        print('\n'+error_message)
        socketio.emit("response", error_message,room=clientID)

    # Translate chatbot response
    src_language = 'english'
    tgt_language = target_language
    translation = mt(src_language, tgt_language, chat_bot_response)
    # print('\nTranslated chatbot response:', translation)
    responseText = "Response in input language: " + translation
    socketio.emit("response", responseText,room=clientID)

    # Capitalize the language string
    input_language = input_language.capitalize()

    # Convert chatbot response to speech
    gender = 'female'
    lang = target_language
    txt = translation
    output = text_to_speech(txt, gender, lang)['audio']
    file_name = clientID + ".mp3"
    wav_file = open(file_name, 'wb')
    decode_string = base64.b64decode(output)
    wav_file.write(decode_string)
    wav_file.close()
    print('\nDone converting to speech')
    responseText = "Done converting to speech" 
    socketio.emit("response", responseText,room=clientID)
    
    print('\nPlaying audio')
    print('*************************************************************')
    return send_file(file_name, mimetype='audio/wav', as_attachment=False)


# STT
def speech_to_text(input_language,input_audio_path):
    # print("\nspeech_to_text function called")
    url = "https://asr.iitm.ac.in/asr/v2/decode"
    # url = "https://projects.respark.iitm.ac.in:1241/decode"
    audio_file = input_audio_path.split('/')[::-1][0]
    payload={'vtt': 'true', 'language': input_language}
    files=[('file',(audio_file,open(input_audio_path,'rb'),'application/octet-stream'))]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify = False)
    print('\n Speech to Text Response: '+response.text)
    # text = json.loads(response.text)
    # output = text["transcript"]
    return response.text


# MT (TTT)
def mt(src_language,tgt_language,transcript):
    # print("\nMachine Translation function called")
    payload = {'src_language':src_language,'tgt_language':tgt_language,'transcript': transcript,'source_vtt':None,'translator_choice':'meta_ai'}
    response = requests.post('https://asr.iitm.ac.in/test1/translate',data = payload).json()
    print("\nMachine Translation response: ",response)
    return response['mt_out']

# CHAT-GPT
def chat_bot(input_question):
    # print("chat bot function called")
    url = 'https://api.openai.com/v1/completions'
    
    payload = json.dumps({
    "model": "text-davinci-003",
    "prompt": input_question,
    "max_tokens": 100,
    "temperature": 0.1
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
    }

    #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 >> old key expired/deleted

    response = requests.request("POST", url, headers=headers, data=payload)
    output = json.loads(response.text)['choices'][0]['text']
    print("\nChatbot response: ",response.text)
    return output

# TTS
def text_to_speech(text,gender,lang):
    # print("Text to Speech function called")
    url = "https://asr.iitm.ac.in/ttsv2/tts"
    # url = "https://projects.respark.iitm.ac.in:4000/tts"
    payload = json.dumps({
		"input": text,
		"gender": gender,
		"lang": lang,
		"alpha": 0.95,
		"segmentwise":"True"
	})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload,verify=False).json()
    print("\nTTS Response status: ",response['status'])
    return response

# @app.errorhandler(Exception)
# def handle_error(e):
#     logging.exception('An error occurred during a request.')
#     return 'An internal server error occurred.', 500

@socketio.on('connect')
def handle_connect():
    print('\nClient connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('\nClient disconnected')


if __name__ == '__main__':
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('./certificate.pem',
                                './key.pem')

    app.run(ssl_context=ssl_context,host='0.0.0.0', port=8001, debug=True)
