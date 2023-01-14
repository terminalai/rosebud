from flask import Flask, request, jsonify, Response
import speech_recognition as sr
import os
from gtts import gTTS
from pydub import AudioSegment
from keybert import KeyBERT
from algorithm.web_scrape import process_keywords

i = 0

# Initiate Flask App
app = Flask(__name__)

r = sr.Recognizer()
kw_model = KeyBERT()

@app.route("/verifyCode", methods=["POST"])
def verifyCode():
    return request.get("code") == 140123

@app.route("/processAudio", methods=["POST"])
def processAudio():
    global i
    i += 1
    print(request.get("code"))
    audio = request.files["audio"]
    audio.save(f"{i}.wav")
    audio.close()

    with sr.AudioFile("temp.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
    
    os.remove("temp.wav")

    # text is still in memory :)

    keywords = [i[0] for i in kw_model.extract_keywords(text)]

    text = process_keywords(keywords)


    myobj = gTTS(text=text, lang="en", slow=False)

    myobj.save("temp.mp3")

    sound = AudioSegment.from_mp3("temp.mp3")
    sound.export("temp.wav", format="wav")

    def generate():
        with open("temp.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)

    return Response(generate(), mimetype="audio/x-wav")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
