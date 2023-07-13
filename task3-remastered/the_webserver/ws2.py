from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

random_numbers = {}

@app.route('/', methods=['GET', 'POST'])
def random_number_generator():
    if request.method == 'POST':
        username = request.form.get('username')
        min_number = int(request.form.get('minNumber'))
        max_number = int(request.form.get('maxNumber'))

        if isinstance(min_number, int) and isinstance(max_number, int):
            import random
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

            return render_template('result.html', username=username, result=result, previous_numbers=random_numbers[username])
        else:
            return "Please enter valid numbers."

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
