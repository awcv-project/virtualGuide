import requests

url = "https://projects.respark.iitm.ac.in:8000/get_profile"

headers = {}

# UPDATED PAYLOAD
payload={
    'wheelchair_id':2,
    'language_selected':'english'
    }

response = requests.request("POST", url, headers=headers, data=payload, verify = False)
print(response.text)
