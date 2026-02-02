"""Authentication routes blueprint - login, register, logout, profile."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Bienvenue, {user.username} !', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page - view and edit."""
    form = ProfileForm(obj=current_user)
    password_form = ChangePasswordForm()

    if form.validate_on_submit():
        # Check uniqueness for changed values
        if form.username.data != current_user.username:
            existing = User.query.filter_by(username=form.username.data).first()
            if existing:
                flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
                return render_template('auth/profile.html', form=form, password_form=password_form)

        if form.email.data != current_user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash('Cette adresse email est déjà utilisée.', 'danger')
                return render_template('auth/profile.html', form=form, password_form=password_form)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', form=form, password_form=password_form)


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change current user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Ancien mot de passe incorrect.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Mot de passe modifié avec succès.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')

    return redirect(url_for('auth.profile'))
