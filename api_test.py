# ADDED NOTES FRO GREESHMA

import requests # for sending request (ASR PART)
import base64 # for decoding audio (TTS PART)

#------------------------------------------------------------
# SAME AS ASR API >>
url = "https://projects.respark.iitm.ac.in:8000/api"
input_audio_path = './input.mp3'

# BUT NOW INSTEAD OF ONE LAGUAGE, WE NEED 2
source_language = 'hindi'
target_language = 'english'

headers = {}

# UPDATED PAYLOAD
payload={
    'wheelchair_id':1,
    'source_language':source_language,
    'target_language':target_language,
    }

# THIS REMAINS SAME AS ASR API
files=[('file',('input.mp3',open(input_audio_path,'rb'),'application/octet-stream'))] # audio file in binary format
response = requests.request("POST", url, headers=headers, data=payload, files=files, verify = False).json()
# ----------------------------------------------------------

# THE "response" WILL BE SIMILAR TO THE RESPONSE OF THE TTS API
# SO AFTER GETTING THE RESPONSE, PROCEED WITH THE TTS RESPONSE DECODING PART LIKE GIVEN BELOW
audio = response['audio']
file_name = "tts.mp3"
wav_file = open(file_name,'wb')
decode_string = base64.b64decode(audio)
wav_file.write(decode_string)
wav_file.close()