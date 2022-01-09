from flask import Flask, render_template, request, redirect, url_for, session
import random
from interact_with_DB import interact_db
from flask import jsonify
import requests


app = Flask(__name__)
app.secret_key = '1234' # this is for session, flask demands encryption


@app.route('/')
def home_fun():
    return render_template('index.html')


@app.route('/CV')
def cv_fun():
    return render_template('CV.html')


## assignment 8
@app.route('/assignment8')
def assignment_fun():
    return render_template('assignment8.html',
                           full_name='Noy Kasher',
                           hobbies=('Music', 'Programming', 'Plants', 'Yoga'),
                           flip=random.choice([True, False]))


## assignment 9
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


## assignment 10
from pages.assignment10.assignment10 import assignment10
app.register_blueprint(assignment10)


@app.route('/assignment11')
def assignment11_fun():
    return render_template('assignment11.html')

## assignment 11
@app.route('/assignment11/users')
def assignment11_users_fun():
    return_dict = {}
    query = 'select * from users;'
    users = interact_db(query=query, query_type='fetch')
    for user in users:
        return_dict[f'user_{user.id}'] = {
            'status': 'success',
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
    return jsonify(return_dict)


@app.route('/assignment11/outer_source')
def assignment11_outer_source_fun():
    return render_template('requests_outer_source.html')


def get_user(id):
    if (id != ""):
        user_id = int(id)
        return requests.get(f'https://reqres.in/api/users/{user_id}').json()

    users = []
    length = len(requests.get(f'https://reqres.in/api/users').json()['data'])

    for i in range(1, length+1):
        res = requests.get(f'https://reqres.in/api/users/{i}')
        res = res.json()
        users.append(res)
    return users


@app.route('/req_backend')
def req_backend():
    if "user_id" in request.args:
        user_id = request.args['user_id']
        if user_id == "":
            users = get_user(user_id)
            return render_template('requests_outer_source.html', users=users)
        else:
            user = get_user(user_id)
            return render_template('requests_outer_source.html', user=user)

    return render_template('requests_outer_source.html')


## assignment 12
@app.route('/assignment12')
def assignment12_func():
    return render_template("assignment12.html")


@app.route('/assignment12/restapi_users', defaults={'user_id': -1})
@app.route('/assignment12/restapi_users/<int:user_id>')
def get_user_func(user_id):
    if user_id == -1:
        return_dict = {}
        query = 'select * from users;'
        users = interact_db(query=query, query_type='fetch')
        for user in users:
            return_dict[f'user_{user.id}'] = {
                'status': 'success',
                'id': user.id,
                'name': user.name,
                'email': user.email,
            }
    else:
        query = 'select * from users where id=%s;' % user_id
        users = interact_db(query=query, query_type='fetch')
        if len(users) == 0:
            return_dict = {
                'status': 'failed',
                'message': 'user not found'
            }
        else:
            return_dict = {
                'status': 'success',
                'id': users[0].id,
                'name': users[0].name,
                'email': users[0].email,
            }

    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)
