from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = '1234' # this is for session, flask demands encryption


@app.route('/')
def home_fun():
    return render_template('index.html')

@app.route('/CV')
def cv_fun():
    return render_template('CV.html')


@app.route('/assignment8')
def assignment_fun():
    return render_template('assignment8.html',
                           full_name='Noy Kasher',
                           hobbies=('Music', 'Programming', 'Plants', 'Yoga'),
                           flip=random.choice([True, False]))


@app.route('/assignment9', methods=['GET', 'POST'])
def assignment9_fun():
    # DB
    users = {'stevie_wonder@gmail.com': {'full_name': 'Stevie Wonder', 'email': 'stevie_wonder@gmail.com'},
             'michael@gmail.com': {'full_name': 'Michael Jackson', 'email': 'michael@gmail.com'},
             'john@gmail.com': {'full_name': 'John Lennon', 'email': 'john@gmail.com'},
             'jimi@gmail.com': {'full_name': 'Jimi Hendrix', 'email': 'jimi@gmail.com'},
             'stevie_ray@gmail.com': {'full_name': 'Stevie Ray Vaughan', 'email': 'stevie_ray@gmail.com'}}

    if request.method == 'GET':
        # if user clicked 'Submit' - with or without filling the form
        if 'email' in request.args:
            email = request.args['email']
            return render_template('assignment9.html', email=email, users=users)

        # if user was reaching page directly from URL
        return render_template('assignment9.html')

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        # DB - insert to users (full_name, email)
        session['user'] = full_name
        session['userinside'] = True
        return redirect(url_for("assignment9_fun"))


@app.route('/logout')
def logout_fun():
    session['user'] = ""
    session['userinside'] = False
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
