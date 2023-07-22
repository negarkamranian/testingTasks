from flask import Flask, request, render_template
import datetime
import os
import random
import time

app = Flask(__name__)

random_numbers = {}
last_request_times = {}
requests_per_second = 1
max_requests_per_second = 1  

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

def is_request_allowed(username):
    current_time = time.time()
    last_request_info = last_request_times.get(username, (0, 0))  # (last_request_time, request_count)
    last_request_time, request_count = last_request_info
    
    if current_time - last_request_time >= 1:
        # reseting
        last_request_times[username] = (current_time, 1)
        return True
    
    if request_count < max_requests_per_second:
        last_request_times[username] = (current_time, request_count + 1)
        return True

    return False

@app.route('/', methods=['GET', 'POST'])
def random_number_generator():
    if request.method == 'POST':
        username = request.form.get('username')
        if not is_request_allowed(username):
            return f"Too many requests. Only {max_requests_per_second} requests per second are allowed. Please wait a moment before trying again."

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
