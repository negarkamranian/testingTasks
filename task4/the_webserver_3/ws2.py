from flask import Flask, request, render_template
import datetime
import os
import random

app = Flask(__name__)

random_numbers = {}

def save_to_file(username, result):
    filename = f"{username}.txt"
    with open(filename, 'a') as file:
        file.write(f"Number: {result['number']}, Timestamp: {result['timestamp']}, Min Number: {result['min_number']}, Max Number: {result['max_number']}\n")

def read_from_file(username):
    filename = f"{username}.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    return []

@app.route('/', methods=['GET', 'POST'])
def random_number_generator():
    if request.method == 'POST':
        username = request.form.get('username')
        min_number = int(request.form.get('minNumber'))
        max_number = int(request.form.get('maxNumber'))

        if isinstance(min_number, int) and isinstance(max_number, int):
            random_number = random.randint(min_number, max_number)

            timestamp = datetime.datetime.now()
            result = {
                'number': random_number,
                'timestamp': timestamp,
                'min_number': min_number,
                'max_number': max_number
            }

            if username in random_numbers:
                random_numbers[username].append(result)
            else:
                random_numbers[username] = [result]

            save_to_file(username, result)

            return render_template('result.html', username=username, result=result, previous_numbers=random_numbers[username])
        else:
            return "Please enter valid numbers."

    return render_template('index.html', previous_numbers=read_from_file(request.args.get('username', '')))

if __name__ == '__main__':
    app.run()

