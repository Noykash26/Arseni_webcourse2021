from flask import Blueprint, render_template, redirect, url_for, request, session
from interact_with_DB import interact_db

# about blueprint definition
assignment10 = Blueprint('assignment10', __name__,
                         static_folder='static',
                         template_folder='templates')


# Routes
@assignment10.route('/assignment10')
def assignment10_fun():
    query = 'select * from users;'
    users = interact_db(query=query, query_type='fetch')
    return render_template('assignment10.html', users=users)


@assignment10.route('/insert_user', methods=['POST'])
def insert_user_fun():
    session.clear()
    # get the data
    name = request.form['name']
    email = request.form['email']
    # TODO validation
    # insert to db
    if name != "" and email != "":
        query = "insert into users(name, email) VALUES('%s', '%s');" % (name, email)
        interact_db(query=query, query_type='commit')
        session['insert'] = True
        # come back to users
        return redirect('/assignment10')
    session['insert'] = False
    return redirect('assignment10')


@assignment10.route('/update_user', methods=['POST'])
def update_user_fun():
    session.clear()
    user_old_email = request.form['old_email']
    user_email = request.form['new_email']
    user_name = request.form['new_name']
    # TODO some validation
    if user_email != "" and user_name != "":
        query = "UPDATE users SET email='%s', name='%s' WHERE email='%s';" % (user_email, user_name, user_old_email)
        interact_db(query=query, query_type='commit')
        session['update'] = True
        return redirect('/assignment10')
    session['update'] = False
    return redirect('assignment10')

@assignment10.route('/delete_user',  methods=['POST'])
def delete_user_fun():
    session.clear()
    user_email = request.form['email']
    # TODO validation
    if user_email != "":
        query= "delete from users where email='%s';" % user_email
        interact_db(query=query, query_type='commit')
        session['delete'] = True
        return redirect('/assignment10')
    session['delete'] = False
    return redirect('/assignment10')

