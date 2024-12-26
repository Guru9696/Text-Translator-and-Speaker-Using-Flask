from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from translate import Translator
import gtts
import os
from playsound import playsound

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data['text']
    from_lang = data['fromLang']
    to_lang = data['toLang']

    # Translate the text
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(text)

    # Save the translated text for playback
    global translated_text
    translated_text = translation
    return jsonify({'translatedText': translation})

@app.route('/play', methods=['GET'])
def play():
    global translated_text

    # Convert translated text to speech and save as mp3
    audio_file = 'static/translated_audio.mp3'
    tts = gtts.gTTS(translated_text, lang='mr')
    tts.save(audio_file)

    # Play the audio file (for server-side playback)
    playsound(audio_file)
    
    # Return the audio file URL (for client-side playback)
    audio_url = f'http://localhost:5000/{audio_file}'
    return jsonify({'audioUrl': audio_url})

if __name__ == '__main__':
    app.run(debug=True)
