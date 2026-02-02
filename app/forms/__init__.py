"""Forms package."""

from app.forms.auth import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm
from app.forms.upload import UploadForm
from app.forms.post import PostForm

__all__ = ['LoginForm', 'RegisterForm', 'ProfileForm', 'ChangePasswordForm', 'UploadForm', 'PostForm']
