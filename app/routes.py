from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'john'},
            'body': "What a nice day for a walk."
        },
        {
            'author': {'username': 'steve'},
            'body': "How do you turn this thing on?"
        },
        {
            'author': {'username': 'mary'},
            'body': "I had a little lamb."
        }
    ]
    sortedPosts = sorted(posts, key=post_unique_chars)
    return render_template('index.html', title='Home', posts=sortedPosts)


@app.route('/xmas')
def xmas():
    greeting = "Merry Christmas"
    return render_template('xmas.html', greeting=greeting)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Whoops! Invalid username or password.")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)  # Defined by flask-login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # Checks that address is relative only for security
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def post_length(blogPost):
    return len(blogPost['body'])


def post_unique_chars(blogPost):
    uniqueChars = set(blogPost['body'])
    return len(uniqueChars)
