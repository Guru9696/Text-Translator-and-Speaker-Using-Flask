import os
import random
import string
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from translate import Translator
import gtts
from playsound import playsound

app = Flask(__name__)
CORS(app)

# Set a higher limit for request size (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tourist_tongue')
def tourist_tongue():
    return render_template('tourist_tongue.html')



##start Text Tone Section

@app.route('/text_tone')
def text_tone():
    return render_template('text_tone.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data['text']
    from_lang = data['fromLang']
    to_lang = data['toLang']

    # Split the text into chunks of 200 words
    words = text.split()
    chunk_size = 1000
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

    # Translate each chunk and combine them
    translated_chunks = []
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    for chunk in chunks:
        chunk_text = ' '.join(chunk)
        translated_chunk = translator.translate(chunk_text)
        translated_chunks.append(translated_chunk)

    translated_text = ' '.join(translated_chunks)
    
    # Save the translated text for playback
    global translated_text_global
    translated_text_global = translated_text

    return jsonify({'translatedText': translated_text})

@app.route('/play', methods=['GET'])
def play():
    global translated_text_global

    if translated_text_global:
        # Generate a unique filename for each audio file
        audio_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.mp3'
        audio_file = os.path.join(app.static_folder, audio_filename)

        # Delete the previous audio file if it exists (to avoid outdated files)
        for f in os.listdir(app.static_folder):
            if f.endswith('.mp3') and f != audio_filename:
                os.remove(os.path.join(app.static_folder, f))

        # Convert the translated text to speech and save it as an mp3 file
        language = 'mr'  # Default to Marathi (mr)
        tts = gtts.gTTS(translated_text_global, lang=language)
        tts.save(audio_file)

        # Return the audio file URL (for client-side playback)
        audio_url = f'http://localhost:5000/static/{audio_filename}'
        return jsonify({'audioUrl': audio_url})

    return jsonify({'error': 'No translated text available for playback'}), 400


@app.route('/global_translate')
def global_translate():
    return render_template('global_translate.html')
    

@app.route('/digital')
def digital():
    return render_template('digital.html')

@app.route('/digital1', methods=['POST'])
def translate_text1():


    data = request.get_json()
    text = data['text']
    from_lang = data['fromLang']
    to_lang = data['toLang']

    # Split the text into chunks of 200 words
    words = text.split()
    chunk_size = 1000
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

    # Translate each chunk and combine them
    translated_chunks = []
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    for chunk in chunks:
        chunk_text = ' '.join(chunk)
        translated_chunk = translator.translate(chunk_text)
        translated_chunks.append(translated_chunk)

    translated_text = ' '.join(translated_chunks)
    
    # Save the translated text for playback
    global translated_text_global1
    translated_text_global1 = translated_text

    return jsonify({'translatedText': translated_text})




if __name__ == '__main__':
    app.run(debug=True)
