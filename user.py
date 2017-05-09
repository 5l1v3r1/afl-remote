from flask import Blueprint, render_template, abort, request, session, flash, redirect, url_for
from database import get_db, close_db

user_pages = Blueprint('user_pages', __name__, template_folder='templates')

@user_pages.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('main'))

    db = get_db()

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if len(username) == 0 or len(password) == 0:
            flash({ "title": "Empty Fields", "body": "Please make sure to fill in both the username and passsword fields." }, "danger")
        else:

            success, response = db.login(username, password)

            if success:
                session['username'] = username
                session['admin'] = response

                return redirect(url_for('main'))
            else:
                flash({ "title": "Invalid Credentials", "body": response }, "danger")
    elif not db.has_users():
        flash({ "title": "Setup Admin Account", "body": "Please create a user for your primary administrator account. This will be used for registering any further users, so make sure not to lose the credentials to this account"}, "primary")
        return redirect(url_for('user_pages.setup'))

    return render_template('login.html')

@user_pages.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('main'))

    pass

@user_pages.route('/setup', methods=['GET', 'POST'])
def setup():
    if session.get('username'):
        return redirect(url_for('main'))

    db = get_db()

    if db.has_users():
        return redirect(url_for('user_pages.login'))

    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(password_confirm) == 0:
            flash({ "title": "Empty Fields", "body": "Please make sure to fill in both the username and passsword fields." }, "danger")
        elif password != password_confirm:
            flash({ "title": "Mismatching Passwords", "body": "Please make sure that your password fields match." }, "danger")
        else:
            success, response = db.register(username, email, password)

            if success:
                session['username'] = username
                session['admin'] = response

                return redirect(url_for('main'))
            else:
                flash({ "title": "Failed to register", "body": response}, "danger")

    return render_template('setup.html')

@user_pages.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username', None)
        session.pop('admin', None)

        flash({ "title": "Logged Out", "body": "You have been logged out" }, "primary")

    return redirect(url_for('index'))
