from flask import render_template
from flask import request

from app import app
from app.dbobjects import title_basic


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

#route for the search method
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        results = title_basic.query.filter(title_basic.title.like('%' + request.form['search'] + '%')).all()
        return render_template("results.html", allmovies=results)
    return render_template('search.html')
