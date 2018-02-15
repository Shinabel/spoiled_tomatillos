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

#route for the search method (so far we can search movies)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        #the movies with titles like the string provided
        results = title_basic.query.filter(title_basic.title.like('%' + str(request.form['search']) + '%')).all()
        data = []
        for r in results:
            #format the result, ensuring properties are strings
            data.append(str(r.title) + ' (' + str(r.year) + ')')

        return render_template("search.html", allmovies=data)
    return render_template('search.html')
