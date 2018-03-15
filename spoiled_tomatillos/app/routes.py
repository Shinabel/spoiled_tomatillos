from flask import render_template, flash, redirect, url_for, request, current_app, session
from passlib.handlers.sha2_crypt import sha256_crypt
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.dbobjects import title_basic, user_info
from app.models import User


@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/index')
def index():
    #print current_app.root_path
    return render_template('index.html')

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
    user = user_info.query.filter(user_info.username == form.username.data).first()
    if user:
        if sha256_crypt.verify(str(form.password.data), user.password):
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            login_user(user)
            return redirect(url_for('index'))
    else:
        form.submit.error = 'Invalid username or password.'
        render_template('login.html', title='Sign In', form=form)
  return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user_info(username=user.username, email=user.email, password=user.password))
        db.session.commit()
        flash('Registration Succeeded: ' + user.username)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    user = current_user
    return render_template('user_profile.html', user=user)
