"""Authentication forms."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class RegisterForm(FlaskForm):
    """User registration form."""
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(),
        Length(min=3, max=64, message='Le nom doit contenir entre 3 et 64 caractères.')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Adresse email invalide.')
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères.')
    ])
    password2 = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe ne correspondent pas.')
    ])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        """Check that username is not already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        """Check that email is not already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cette adresse email est déjà utilisée.')


class ProfileForm(FlaskForm):
    """User profile edit form."""
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Mettre à jour')


class ChangePasswordForm(FlaskForm):
    """Change password form."""
    old_password = PasswordField('Ancien mot de passe', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[
        DataRequired(),
        Length(min=6)
    ])
    new_password2 = PasswordField('Confirmer le nouveau mot de passe', validators=[
        DataRequired(),
        EqualTo('new_password', message='Les mots de passe ne correspondent pas.')
    ])
    submit = SubmitField('Changer le mot de passe')
