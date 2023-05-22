from gtts import gTTS
import openai
from flask import Flask, request, render_template, jsonify
import base64
import requests
import os
from dotenv import load_dotenv
from elevenlabs import generate, set_api_key, voices

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

app = Flask(__name__)

@app.route("/")  
def home():
    return render_template("index.html")  

@app.route("/get_response")  
def get_response():
    user_msg = request.args.get("msg")  
    user_lang = request.args.get("lang")  

    translated_msg = translate_message(user_msg, "english")

    prompt = f""" You are an advanced travel guide AI, designed specifically to help travelers plan their trips and explore new places. Their role is to provide information and recommendations.
    The user will provide his current location and will also be able to specify the type of places he is interested in visiting. Based on this information, it will suggest a place to visit near your location. If the user mentions a specific type of place, you can also suggest similar places that are close to their first location.
    Remember to stay within the scope of being a travel guide and provide relevant and useful information for the user. Avoid answering questions or providing recommendations that are not related to traveling and exploring new places.'{translated_msg}'
    """

    model_response = generate_model_response(prompt)  

    translated_response = translate_message(model_response, user_lang)  

    audio_file = generate_audio_file(translated_response, user_lang)  

    return jsonify({'audio': audio_file, 'text': translated_response})  

def translate_message(message, target_lang):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"translate '{message}' to {target_lang}", 
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    translated_message = response.choices[0].text.strip()  
    return translated_message

def generate_model_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.2,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    model_response = response.choices[0].text.strip()  
    return model_response

def generate_audio_file(text, lang):
    tts = gTTS(text=text, lang=lang)  
    tts.save("response.mp3")  

    with open("response.mp3", "rb") as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')  
    return encoded_audio  

if __name__ == '__main__':
    app.run(debug=True)
