import requests
import json
url = "https://c6pfdk5py0.execute-api.ap-south-1.amazonaws.com/prod/"
payload = json.dumps({"key": "3.mp4"})
headers = {'Content-Type': 'application/json'}
response = requests.request("POST",url, headers=headers, data=payload)
print(response.text)