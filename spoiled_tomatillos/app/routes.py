from flask import render_template
from flask import request

from app import app
from app.forms import LoginForm
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

#route for the login URL that creates a form and passes it to the template for rendering
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(
      form.username.data, form.remember_me.data))
    return redirect(url_for('search'))
  return render_template('login.html', title='Sign In', form=form)