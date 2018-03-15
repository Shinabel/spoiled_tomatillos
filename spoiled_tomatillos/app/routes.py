
from flask import render_template, flash, redirect, url_for, request, current_app, session
import datetime

from passlib.handlers.sha2_crypt import sha256_crypt
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.dbobjects import title_basic, user_info
from app.models import User

from app.token import generate_confirmation_token, confirm_token
from app.email import send_email

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
        if not user.confirmed:
            flash('Account needs to be verified', 'warning')
            return redirect(url_for('login'))

        if sha256_crypt.verify(str(form.password.data), user.password) and user.confirmed:
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            login_user(user)
            return redirect(url_for('index'))
    else:
        form.submit.error = 'Invalid username or password'
        return render_template('login.html', title='Sign In', form=form)
  return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data, False)

        db.session.add(user_info(username=user.username, email=user.email,
         password=user.password, register_date = datetime.datetime.now(),
         confirmed = False, confirmed_date = None))
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        flash('Registration Succeeded: ' + user.username)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    user = current_user
    return render_template('user_profile.html', user=user)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = user_info.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Email provided is already on use. Please login or register with different email.', 'success')
    else:
        user.confirmed = True
        user.confirmed_date = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Account confirmed. Thanks!', 'success')
    return redirect(url_for('login'))

