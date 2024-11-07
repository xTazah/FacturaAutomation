from openai import OpenAI
from ai.response_format import Factura

client = OpenAI()

image_url = "test" # ToDo: upload the img somewhere to use it

with open('system_prompt.txt', 'r') as file:
  system_prompt = file.read()

response = client.chat.completions.create(
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
            "url": image_url
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
  response_format=Factura
)