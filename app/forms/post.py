"""Post/article forms."""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """Create/edit post form."""
    title = StringField('Titre', validators=[
        DataRequired(),
        Length(max=200, message='Le titre ne doit pas dépasser 200 caractères.')
    ])
    body = TextAreaField('Contenu', validators=[DataRequired()])
    is_published = BooleanField('Publié', default=True)
    submit = SubmitField('Enregistrer')
