from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        # session.add not required because current_user callback performs
        # database query which puts target into session already


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        # Post/Redirect/Get pattern avoids refresh-related weirdness;
        # refresh reruns the last request so could double-post.
        return redirect(url_for('index'))
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
    return render_template('index.html', title='Home', form=form, posts=sortedPosts)


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
        login_user(user, remember=form.remember_me.data)
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("New user registered. Welcome, {}!".format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user,
            'body': "Example post #1 to fill space."},
        {'author': user,
            'body': "Wow another example post (#2) filling more space."}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        # If validation passes, update db with form contents (POST)
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()  # Again .add not needed since current_user called
        flash("Your changes have been saved.")
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        # If we're just doing a GET for the initial form pre-submit,
        # then pre-pop with current info.
        # Otherwise this is a POST with failed validation: don't do anything.
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit-profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself.')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return(redirect(url_for('index')))
    if user == current_user:
        flash('You cannot unfollow yourself.')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('No longer following {}.'.format(username))
    return redirect(url_for('user', username=username))


def post_length(blogPost):
    return len(blogPost['body'])


def post_unique_chars(blogPost):
    uniqueChars = set(blogPost['body'])
    return len(uniqueChars)
