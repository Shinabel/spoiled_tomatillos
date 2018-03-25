from flask import render_template, flash, redirect, url_for, request, current_app, session
import datetime

from passlib.handlers.sha2_crypt import sha256_crypt
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetForm, ChangePasswordForm
from app.dbobjects import TitleBasic, UserInfo, Ratings, Roles, Actors, UserRatings, Crew
from app.models import User

from app.token import generate_confirmation_token, confirm_token
from app.email import send_email

from flask_login import login_user, logout_user, login_required, current_user

# getting movie posters
import requests
from bs4 import BeautifulSoup


@app.route('/')
def main():
    return redirect(url_for('login'))


@app.route('/index')
def index():
    # print current_app.root_path
    return render_template('index.html')


# route for the search method (so far we can search movies)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":

        # the movies with titles like the string provided
        results = TitleBasic.query.filter(TitleBasic.title.like('%' + str(request.form['search']) + '%')).all()
        data = []
        for r in results:
            # format the result, ensuring properties are strings
            data.append({"title": str(r.title) + ' (' + str(r.year) + ')', "id": r.id})

        return render_template("search.html", allmovies=data)
    return render_template('search.html')


# route for the login URL that creates a form and passes it to the template for rendering
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserInfo.query.filter(UserInfo.username == form.username.data).first()
        if user:
            if not user.confirmed:
                flash('Account needs to be verified', 'warning')
                return redirect(url_for('login'))

            if sha256_crypt.verify(str(form.password.data), user.password) and user.confirmed:
                login_user(user)  # login user to current user

                # testing if current user works
                print(current_user)

                flash('Login requested for user {}, remember_me={}'.format(
                    form.username.data, user.confirmed))

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

        # before adding into database, check if the email is already in the database.

        db.session.add(UserInfo(username=user.username, email=user.email,
                                password=user.password, register_date=datetime.datetime.now(),
                                confirmed=False, confirmed_date=None))
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


@app.route('/movie/<movie_id>', methods=['GET', 'POST'])
def movie_page(movie_id):
    current_user_rating = None
    current_user_rating_row = UserRatings.query.filter(
        UserRatings.movieId == movie_id and UserRatings.user_ID == current_user).first()

    if current_user.is_authenticated and current_user_rating_row is not None:
        current_user_rating = current_user_rating_row.ratings

    if request.method == "POST":
        if current_user.is_authenticated:
            original_rating = UserRatings.query.filter(
                UserRatings.movieId == movie_id and UserRatings.user_ID == current_user).first()
            if original_rating is None:
                db.session.add(
                    UserRatings(user_ID=current_user.get_id(), movieId=movie_id, ratings=request.form['user-rating']))
                db.session.commit()
            else:
                original_rating.ratings = request.form['user-rating']
                db.session.commit()
        else:
            flash('You must be signed in to rate movies.')

    movie = TitleBasic.query.filter_by(id=movie_id).first()
    rating = Ratings.query.filter_by(movieId=movie_id).first()

    # getting all the actors in a movie
    results = Roles.query.filter_by(movieId=movie_id).filter_by(category='actor').all()
    allActors = []
    for r in results:
        actor = Actors.query.filter_by(id=r.personID).first()
        allActors.append(actor.name)

    # getting directors for a movie
    dir_result = Crew.query.filter_by(movieId=movie_id).first()
    director_id = dir_result.directors
    director = Actors.query.filter_by(id=director_id).first()
    director_name = director.name

    # getting writers for a movie
    write_result = Crew.query.filter_by(movieId=movie_id).first()
    writer_id = dir_result.writers
    writer = Actors.query.filter_by(id=director_id).first()
    writer_name = writer.name

    user_ratings = UserRatings.query.filter_by(movieId=movie_id).all()
    counter = 0
    sum = 0
    for u in user_ratings:
        sum += u.ratings
        counter += 1
    if counter == 0:
        user_rating = 0
    else:
        user_rating = sum / counter

    base_url = "http://www.imdb.com/title/"
    url = base_url + movie_id
    response_data = requests.get(url).text[:]
    soup = BeautifulSoup(response_data, 'html.parser')
    image_link = soup.find("div", class_="poster")
    if image_link is None:
        image_link = "https://developersushant.files.wordpress.com/2015/02/no-image-available.png"
    else:
        image_link = image_link.find("img")['src']
    movie_description = soup.find("div", class_="summary_text").get_text().strip()
    if movie_description == "Add a Plot »":
        movie_description = "No description."

    return render_template('movie.html', movie=movie, image=image_link, desc=movie_description, allActors=allActors,
                           rating_count=rating.numVotes, user_rating=user_rating,
                           current_user_rating=current_user_rating,
                           rating=rating.average_rating, director_name=director_name, writer_name=writer_name)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = UserInfo.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Email provided is already on use. Please login or register with different email.', 'success')
    else:
        user.confirmed = True
        user.confirmed_date = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Account confirmed. Thanks!', 'success')
    return redirect(url_for('login'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetForm(request.form)
    if form.validate():
        user = UserInfo.query.filter(UserInfo.email == form.email.data).first()
        token = generate_confirmation_token(user.email)

        user.password_token = token
        db.session.commit()

        change_url = url_for('change_password', token=token, _external=True)

        html = render_template('reset.html',
                               username=user.email,
                               change_url=change_url)
        subject = "Reset your password"
        send_email(user.email, subject, html)

        flash('A password reset email has been sent via email.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


@app.route('/reset_password/new/<token>', methods=['GET', 'POST'])
def change_password(token):
    email = confirm_token(token)

    user = UserInfo.query.filter(UserInfo.email == email).first_or_404()

    if user.password_token is not None:
        form = ChangePasswordForm(request.form)
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(email=email).first()
            if user:
                user.password = sha256_crypt.encrypt(str(form.password.data))
                user.password_token = None
                db.session.commit()

                flash('Password successfully updated.', 'success')
                return redirect(url_for('login'))

            else:
                flash('Password change was unsuccessful.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Please enter your new password.', 'success')
            return render_template('change_password.html', form=form)
    else:
        flash('unable to reset the password, try again.', 'danger')

    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('user logged out.', 'success')
    return redirect(url_for('login'))
