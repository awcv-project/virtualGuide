from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO
import requests
import json
import base64
import ssl
from bs4 import BeautifulSoup

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

# EXTRA ROUTES FOR THE TABLET APPLICATION------------------------------
 # default english language > english
@app.route('/get_profile', methods=['POST']) # sending available list of languages, easy to change/update at server side instead of app side
def get_profile():
    request_data = request.get_json(force=True, silent=True)
    if request_data is None:
        request_data = request.values
    wheelchair_id = request_data['wheelchair_id']
    # retrieve wheelchair profile
    
    profile = json.load(open('wheelchair_profile.json'))[str(wheelchair_id)]

    response = {
        'wheelchair_id':wheelchair_id,
        'wheelchair_profile' : profile,
        'available_languages' : {"தமிழ்":"tamil", "English":"english", "ಕನ್ನಡ":"telugu", "मराठी":"marathi", "हिन्दी":"hindi", "తెలుగు":"kannada", "ગુજરાતી":"gujarati"},
        # 'available_languages' : ['தமிழ்','English','ಕನ್ನಡ','मराठी', 'हिन्दी','తెలుగు', 'ગુજરાતી'],
        # 'available_destinations' : ['CEET','CBEEV','IC','5G','BUILDLAB','HTIC']
    }
    # print(response)
    return jsonify(response)


@app.route('/get_destinations', methods=['POST']) # sending available list of languages, easy to change/update at server side instead of app side
def get_destinations():
    
    request_data = request.get_json(force=True, silent=True)
    if request_data is None:
        request_data = request.values
    wheelchair_id = request_data['wheelchair_id']
    lang_selected = request_data['language_selected']

    profile = read_json('./wheelchair_profile.json')
    profile[str(wheelchair_id)] = lang_selected
    write_json('./wheelchair_profile.json', profile)

    if lang_selected=='english':
        response = {
            'wheelchair_id':wheelchair_id,
            'dest_heading':'Available Destinations:',
            'available_destinations' : ['CEET','CBEEV','IC','5G','BUILDLAB','HTIC'],
            'instruction_mic':'Press and hold to talk',
            'chat_heading':'Answer:'
        }
        return jsonify(response)
    
    elif lang_selected=='hindi':
        response = {
            'wheelchair_id':wheelchair_id,
            'dest_heading':'उपलब्ध स्थान:',
            'available_destinations' : ['सी.ई.ई.ट्','सी.बी.ई.ई.व्','आई.सी','५.जी','बिल्ड लैब','एच.टी.आई.सी'],
            'instruction_mic':'कृपया माइक को दबाने के बाद बोलें', 
            'chat_heading':'जवाब:'
        }
        return jsonify(response)
    
    elif lang_selected=='tamil':
        response = {
            'wheelchair_id':wheelchair_id,
            'dest_heading':'கிடைக்கும் இடம்:',
            'available_destinations' : ['சி.ஈ.ஈ.ட்', 'சி.பி.ஈ.ஈ.வ்', 'ஐ.சி', '5ஜி', 'பில்ட் லேப்', 'எச்.டி.ஐ.சி'],
            'instruction_mic':'பேசுவதற்கு இங்கே அழுத்தவும்', 
            'chat_heading':'பதில்:'
        }
        return jsonify(response)
    
    elif lang_selected=='kannada':
        response = {
            'wheelchair_id':wheelchair_id,
            'dest_heading':'ಲಭ್ಯವಿರುವ ಗುರುತುಗಳು:',
            'available_destinations' : ['ಸಿ.ಈ.ಈ.ಟಿ', 'ಸಿ.ಬಿ.ಈ.ಈ.ವಿ', 'ಐ.ಸಿ', '5.ಜಿ', 'ಬಿಲ್ಡ್ ಲೇಬ್', 'ಎಚ್.ಟಿ.ಐ.ಸಿ'],
            'instruction_mic':'ಮೈಕ್ ಒತ್ತುಮುಚ್ಚಿಕೊಂಡ ನಂತರ ಮಾತಾಡಿ', 
            'chat_heading':'ಉತ್ತರ:'
        }
        return jsonify(response)
    elif lang_selected=='marathi':
        response = {
            'wheelchair_id':wheelchair_id,
            'dest_heading':'उपलब्ध गंतव्य:',
            'available_destinations' : ['सी.ई.ई.टी', 'सी.बी.ई.ई.व्ही', 'आय.सी', '५जी', 'बिल्ड लेब', 'एच.टी.आय.सी'],
            'instruction_mic':'मायकवर दाबून बोला', 
            'chat_heading':'उत्तर:'
        }
        return jsonify(response)
    elif lang_selected=='telugu':
        response = {
            'wheelchair_id':wheelchair_id,
            'dest_heading':'అందుబాటులో గమ్యాంశాలు:',
            'available_destinations' :  ['సి.ఇ.ఇ.టి', 'సి.బి.ఇ.ఇ.వి', 'ఐ.సి', '5జి', 'బిల్డ్ లేబు', 'ఎచ్.టి.ఐ.సి'],
            'instruction_mic':'మైక్ను నొక్కి మాట్లాడండి', 
            'chat_heading':'సమాధానం:'
        }
        return jsonify(response)
    elif lang_selected=='gujarati':
        response = {
            'wheelchair_id':wheelchair_id,
            'dest_heading':'ઉપલબ્ધ ગંતવ્યો:',
            'available_destinations' :  ['સી.ઇ.ઇ.ટી', 'સી.બી.ઇ.ઇ.વી', 'આઈ.સી', '5જી', 'બિલ્ડ લેબ', 'એચ.ટી.આઈ.સી'],
            'instruction_mic':'માઇક દબાવીને બોલો', 
            'chat_heading':'જવાબ:'
        }
        return jsonify(response)
input_language = "english"
    
#-----------------------------------------------------------------------

@app.route('/play_voice', methods=['POST'])
def play_voice():
    # Convert audio to text
    input_language = request.form["language"]
    target_language = request.form["target_language"]
    clientID = request.form["clientId"]
    audio_file = request.files["audio"]
    # print(audio_file)
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
        chat_bot_response = chat_bot2(input_question).strip()
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

@app.route('/api', methods=['POST'])
def api():
    # getting input fields from payload
    request_data = request.get_json(force=True, silent=True)
    if request_data is None:
        request_data = request.values
    # print(request_data)
    source_language = request_data['source_language']
    target_language = request_data['target_language']
    wheelchair_id = request_data['wheelchair_id']
    # update wheelchair profile
    
    "*****************"
    # print("request data*****", source_language, target_language, wheelchair_id)

    # getting audio file
    files = request.files
    # print("files**********",files)
    input_file = None
    try:
        input_file = files.get('file')
        # print("input_file*********",input_file)
    except Exception as err:
        return jsonify(status='failure', reason=f"Unsupported input. {err}")

    # STT
    try:
        stt = json.loads(speech_to_text2(source_language, input_file))['transcript']
        socketio.emit("stt_response", stt)
    except Exception as e:
        error_message = "Speech To Text Error:"  + str(e)
        message_to_send = "Automatic Speech Recognition Error"
        print(message_to_send)
        socketio.emit("stt_response", message_to_send)
        return error_message

    # Translate to English
    src_language = source_language
    tgt_language = 'english'
    translation = mt(src_language, tgt_language, stt)

    # Get chatbot response
    try:
        input_question = translation
        chat_bot_response = chat_bot2(input_question).strip()
    except Exception as e:
        error_message = "Chat GPT ResponseError:" + str(e)
        return error_message
    
    # Translate chatbot response
    src_language = 'english'
    tgt_language = target_language
    translation = mt(src_language, tgt_language, chat_bot_response)

    # Capitalize the language string
    source_language = source_language.capitalize()

    # Convert chatbot response to speech
    gender = 'female'
    lang = target_language
    txt = translation
    output = text_to_speech(txt, gender, lang)
    output['caption'] = txt

    return output

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Write to JSON file
def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# STT2 for api
def speech_to_text2(input_language,input_file):
    # print("\nspeech_to_text function called")
    url = "https://asr.iitm.ac.in/asr/v2/decode"
    # url = "https://projects.respark.iitm.ac.in:1241/decode"
    payload={'vtt': 'true', 'language': input_language}
    files=[('file',('input.mp3',input_file,'application/octet-stream'))]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print('\n Speech to Text Response: '+response.text)
    # text = json.loads(response.text)
    # output = text["transcript"]
    return response.text

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

    response = requests.request("POST", url, headers=headers, data=payload)
    output = json.loads(response.text)['choices'][0]['text']
    print("\nChatbot response: ",response.text)
    return output

def google_search(query):
    query = query.replace(' ', '+')
    url = f'https://www.google.com/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser').text
    return soup

def chat_bot2(input_question):
    search_text = google_search(input_question)
    return chat_bot(search_text)

# TTS
def text_to_speech(text,gender,lang):
    # print("Text to Speech function called")
    # url = "https://asr.iitm.ac.in/ttsv2/tts"
    url = "https://projects.respark.iitm.ac.in:4000/tts"
    payload = json.dumps({
		"input": text,
		"gender": gender,
		"lang": lang,
		"alpha": 0.95,
		"segmentwise":"True"
	})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
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
    ssl_context.load_cert_chain('./ssl2023/iitm2022.crt',
                                './ssl2023/iitm2022.key')

    app.run(ssl_context=ssl_context,host='0.0.0.0', port=8000, debug=True)
