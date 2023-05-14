from gradio_client import Client
import json
from bs4 import BeautifulSoup

client = Client("https://huggingfaceh4-open-llm-leaderboard.hf.space/")
#result = client.view_api(return_format="dict")
#print(result)

json_data = client.predict(
    fn_index=2
)


with open(json_data[0], 'r') as file:
    file_data = file.read()

# Load the JSON data
data = json.loads(file_data)

# Get the headers and the data
headers = data['headers']
data = data['data']

# Create a dictionary from the headers and the data
data_dict = [dict(zip(headers, d)) for d in data]

# Create a new dictionary with model->status
model_status_dict = {}

for d in data_dict:
    # Parse the HTML to get the model name
    soup = BeautifulSoup(d['Model'], 'html.parser')
    model_name = soup.a.string

    # Add the model name and status to the dictionary
    model_status_dict[model_name] = d['Average \u2b06\ufe0f']

print(model_status_dict)
