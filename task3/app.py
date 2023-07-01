from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random', methods=['POST'])
def random_number():
    start = int(request.form['start'])
    end = int(request.form['end'])
    random_num = random.randint(start, end)
    return f"The random number between {start} and {end} is: {random_num}"

if __name__ == '__main__':
    app.run()
