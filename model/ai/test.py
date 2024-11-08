import openai
from response_format import Factura
import base64
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "./test/test_small.png"
base64_image = encode_image(image_path)

with open('./ai/system_prompt.txt', 'r') as file:
  system_prompt = file.read()

openai.api_key = openai_api_key

response = openai.ChatCompletion.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": system_prompt 
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  temperature=0.63,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  response_format={
           'type': 'json_schema',
           'json_schema': 
              {
                "name":"factura", 
                "schema": Factura.model_json_schema()
              }
         } 
)

print(response)