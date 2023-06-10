import requests
input_audio_path ='mGHCnr0rTaFFaPtkAAAD.wav'
def speech_to_text(input_language,input_audio_path):
    print("speech_to_text function called")
    url = "https://asr.iitm.ac.in/asr/v2/decode"
    audio_file = input_audio_path.split('/')[::-1][0]
    print(audio_file)
    payload={'vtt': 'true', 'language': input_language}
    files=[('file',(audio_file,open(input_audio_path,'rb'),'application/octet-stream'))]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    # text = json.loads(response.text)
    # output = text["transcript"]
    return response.text

speech_to_text('english','S3zD7TpAg36vlAAXAABa.wav')
