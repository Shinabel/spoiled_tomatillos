from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, Length, EqualTo, Email
from app.dbobjects import UserInfo


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

    def validate(self):
    	initial_validation = super(RegistrationForm, self).validate()
    	if not initial_validation:
    		return False
    	user = UserInfo.query.filter_by(email=self.email.data).first()
    	if user:
    		self.email.errors.append("Email already used")
    		return False
    	return True


class ResetForm(Form):
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])

    def validate(self):
        initial_validation = super(ResetForm, self).validate()
        if not initial_validation:
            return False
        user = UserInfo.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("This email is not registered")
            return False
        return True


class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
