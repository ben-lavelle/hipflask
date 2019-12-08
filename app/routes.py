from flask import render_template
from app import app

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
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
