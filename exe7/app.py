from flask import Flask, redirect, url_for
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello, World!"


# one use of redirect function
@app.route('/home')
def hello_home():
    return redirect('/')


# one use of redirect + url for function
@app.route('/about')
def hello_about():
    # DO SOMETHING WITH DB
    return redirect(url_for('hello_world'))


if __name__ == '__main__':
    app.run(debug=True)