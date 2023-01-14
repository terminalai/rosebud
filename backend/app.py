from flask import Flask, request, jsonify, Response
import speech_recognition as sr
import os
from gtts import gTTS
from pydub import AudioSegment

# Initiate Flask App
app = Flask(__name__)

r = sr.Recognizer()

@app.route("/trivia", methods=["POST"])
def trivia():
    audio = request.files["audio"]
    audio.save("temp.wav")

    with sr.AudioFile("temp.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
    
    os.remove("temp.wav")

    # text is still in memory :)

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
