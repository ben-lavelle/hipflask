from flask import render_template
from app import app
from app.forms import LoginForm

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

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

def post_length(blogPost):
    return len(blogPost['body'])
def post_unique_chars(blogPost):
    uniqueChars = set(blogPost['body'])
    return len(uniqueChars)
