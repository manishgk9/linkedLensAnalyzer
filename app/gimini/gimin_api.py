from google import genai
from dotenv import load_dotenv
import os
from app.utils import gimin_prompt
load_dotenv()
GIMINI_KEY=os.getenv('GIMINI_API_KEY')
client = genai.Client(api_key=GIMINI_KEY)

def get_gimini_response(resume_data_as_json):
    try:
        prompt=gimin_prompt.prompt(resume_data_as_json)
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt)
        if response:
            return response.text
    except Exception as e:
        return 'Exception found in gimin side.'

