import requests
import json

# URL of the JSON data
url = 'https://opencompass.oss-cn-shanghai.aliyuncs.com/assets/large-language-model-data.json'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Load the data into a Python object
    data = json.loads(response.text)
else:
    print(f'Request failed with status code {response.status_code}')


print(data)