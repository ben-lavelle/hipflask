from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'bjml'}
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
    return render_template('index.html', title='Home', user=user, posts=sortedPosts)


@app.route('/xmas')
def xmas():
    user = {'username': 'bjml'}
    greeting = "Merry Christmas"
    return render_template('xmas.html', user=user, greeting=greeting)


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
        return redirect(url_for('index'))
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
