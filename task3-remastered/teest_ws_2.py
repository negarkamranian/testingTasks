from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def random_number_generator():
    if request.method == 'POST':
        username = request.form.get('username')
        min_number = int(request.form.get('minNumber'))
        max_number = int(request.form.get('maxNumber'))

        if isinstance(min_number, int) and isinstance(max_number, int):
            import random
            random_number = random.randint(min_number, max_number)
            return render_template('result.html', username=username, random_number=random_number)
        else:
            return "Please enter valid numbers."

    return render_template('index.html')

if __name__ == '__main__':
    app.run()

