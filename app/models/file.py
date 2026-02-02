"""File upload model."""

from datetime import datetime
from app.extensions import db


class File(db.Model):
    """Uploaded file model."""
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    original_filename = db.Column(db.String(256), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(128))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        """Serialize file to dictionary (for API responses)."""
        return {
            'id': self.id,
            'filename': self.original_filename,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'uploaded_at': self.uploaded_at.isoformat(),
            'owner': self.owner.username if self.owner else None,
        }

    def __repr__(self):
        return f'<File {self.original_filename}>'
