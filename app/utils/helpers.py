"""Utility helper functions."""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if a filename has an allowed extension."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_file(file):
    """Save an uploaded file with a unique name.

    Args:
        file: FileStorage object from request.files.

    Returns:
        Tuple of (saved_filename, original_filename, file_size, mime_type)
    """
    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_filename = f'{uuid.uuid4().hex}.{ext}' if ext else uuid.uuid4().hex

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)

    file_size = os.path.getsize(filepath)
    mime_type = file.content_type

    return unique_filename, original_filename, file_size, mime_type
