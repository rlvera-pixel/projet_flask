"""File upload forms."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class UploadForm(FlaskForm):
    """File upload form with validation."""
    file = FileField('Fichier', validators=[
        FileRequired(message='Veuillez sélectionner un fichier.'),
        FileAllowed(
            ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'doc', 'docx'],
            message='Type de fichier non autorisé.'
        )
    ])
    submit = SubmitField('Envoyer')
