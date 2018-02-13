from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Veronica'}
    posts = [
        {
            'author': {'username': 'Matt'},
            'body': 'Beautiful day in Boston!'
        },
        {
            'author': {'username': 'Jay'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
