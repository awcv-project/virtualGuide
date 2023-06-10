import json
import requests

url = 'https://api.openai.com/v1/completions'

input_question = 'hello there'

payload = json.dumps({
"model": "text-davinci-003",
"prompt": input_question,
"max_tokens": 150,
"temperature": 0.9
})

headers = {
'Content-Type': 'application/json',
'Authorization': "Bearer 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"
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
