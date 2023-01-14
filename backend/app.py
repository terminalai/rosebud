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

@app.route("/")
def main():
    return "<h1>Hello</h1>"


@app.route("/verifyCode", methods=["GET"])
def verifyCode():
    print('received code')
    res = jsonify(dict(response = request.args.get("code", 123456, int) == 140123))
    res.headers.add('Access-Control-Allow-Origin','*')
    return res

@app.route("/processAudio", methods=["POST"])
def processAudio():
    global i
    i += 1
    #print(request.get("code"))
    audio = request.files["audio"]
    audio.save(f"temp.ogg")
    audio.close()

    x = AudioSegment.from_file("temp.ogg")
    x.export("temp.wav", format='wav')

    r = sr.Recognizer()
    #kw_model = KeyBERT()

    with sr.AudioFile("temp.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
    
    os.remove("temp.ogg")

    # text is still in memory :)

    #keywords = [i[0] for i in kw_model.extract_keywords(text)]

    #text = process_keywords(keywords)


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

    res = Response(generate(), mimetype="audio/x-wav")
    res.headers.add('Access-Control-Allow-Origin','*')
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
