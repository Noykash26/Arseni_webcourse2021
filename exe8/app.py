from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route('/')
def cv_fun():
    return render_template('CV.html')

@app.route('/assignment8')
def assignment_fun():
    return render_template('assignment8.html',
                           full_name='Noy Kasher',
                           hobbies=('Music', 'Programming', 'Plants', 'Yoga'),
                           flip=random.choice([True, False]))


if __name__ == '__main__':
    app.run(debug=True)
