# logic.py
import os
import random
import string
from translate import Translator
import gtts
from translate import Translator, exceptions

def translate_text(text, from_lang, to_lang):
    try:
        # Split the text into chunks of 1000 words
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
        return translated_text

    except exceptions.Exception as e:
        print(f"Translation error: {e}")
        return None

def generate_audio_from_text(text, language='mr'):
    try:
        # Generate a unique filename for each audio file
        audio_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.mp3'
        audio_path = os.path.join('static', audio_filename)

        # Convert the translated text to speech and save it
        tts = gtts.gTTS(text, lang=language)
        tts.save(audio_path)

        return audio_filename, audio_path
    except Exception as e:
        print(f"Audio generation error: {e}")
        return None, None

