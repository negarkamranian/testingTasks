from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('translation.html')

@app.route('/translate', methods=['POST'])
def translate():
    word = request.form['word']

    translator = Translator()
    translation = translator.translate(word, dest='en')

    translated_word = translation.origin
    translated_meaning = translation.text
    
    return render_template('result.html', word=translated_word, meaning=translated_meaning)

if __name__ == '__main__':
    app.run(debug=True)
