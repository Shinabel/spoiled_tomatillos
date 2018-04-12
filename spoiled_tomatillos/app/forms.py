from operator import and_
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from app.dbobjects import UserInfo
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    accept_tos = BooleanField(
        'I acknowledge that I have read and fully understand the terms and conditions of the site',
        [validators.Required()])

    def check_initial_validation(self, iv):
        if not iv:
            return False
        return True

    def check_username_registered(self, user):
        if user:
            self.username.errors.append("Username is already taken")
            return False
        return True

    def check_email_registered(self, email_address):
        if email_address:
            self.email.errors.append("Email already used")
            return False
        return True

    def validate(self):
    	iv = super(RegistrationForm, self).validate()
    	init_valid = self.check_initial_validation(iv)

    	user_name = UserInfo.query.filter_by(username=self.username.data).first()
    	check_username = self.check_username_registered(user_name)

    	email_address = UserInfo.query.filter_by(email=self.email.data).first()
    	check_email = self.check_email_registered(email_address)

    	return init_valid and check_username and check_email


class ResetForm(Form):
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])

    def check_initial_validation(self, iv):
        if not iv:
            return False
        return True

    def check_email_registered(self, user):
        if not user:
            self.email.errors.append("Email is not registered, please register")
            return False
        return True

    def validate(self):
        iv = super(ResetForm, self).validate()
        init_valid = self.check_initial_validation(iv)

        user = UserInfo.query.filter_by(email=self.email.data).first()
        check_email = self.check_email_registered(user)

        return init_valid and check_email


class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')


# form for editing a user's information
class EditProfileForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=255)])
    favorite_movies = TextAreaField('Favorite Movies', validators=[Length(min=0, max=255)])
    submit = SubmitField('Submit')

    def check_initial_validation(self, iv):
        if not iv:
            print('iv issue')
            return False
        return True

    # check if username is taken.
    def check_username_registered(self, user):
        if user:
            print('username issue')
            self.username.errors.append("Username is already taken")
            return False
        return True

    # overwrite validate function for form
    def validate(self):
        iv = super(EditProfileForm, self).validate()
        init_valid = self.check_initial_validation(iv)

        user_name = UserInfo.query.filter(and_(UserInfo.username == self.username.data, UserInfo.user_ID != current_user.user_ID)).first()
        check_username = self.check_username_registered(user_name)
        print('got here')
        return init_valid and check_username
