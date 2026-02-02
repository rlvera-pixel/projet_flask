"""Dashboard routes blueprint - user dashboard, file upload, settings."""

import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, \
    current_app, send_from_directory, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Post, File
from app.forms import UploadForm, PostForm
from app.utils import save_file, allowed_file, admin_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard home - overview of user's content."""
    posts = current_user.posts.order_by(Post.created_at.desc()).limit(5).all()
    files = current_user.files.order_by(File.uploaded_at.desc()).limit(5).all()
    return render_template('dashboard/index.html', posts=posts, files=files)


# --- Post CRUD ---

@dashboard_bp.route('/posts')
@login_required
def posts():
    """List all posts by current user."""
    page = request.args.get('page', 1, type=int)
    user_posts = current_user.posts.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/posts.html', posts=user_posts)


@dashboard_bp.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """Create a new post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            is_published=form.is_published.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Article créé avec succès.', 'success')
        return redirect(url_for('dashboard.posts'))
    return render_template('dashboard/post_form.html', form=form, title='Nouvel article')


@dashboard_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing post."""
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.is_published = form.is_published.data
        db.session.commit()
        flash('Article mis à jour.', 'success')
        return redirect(url_for('dashboard.posts'))
    return render_template('dashboard/post_form.html', form=form, title='Modifier l\'article')


@dashboard_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Article supprimé.', 'info')
    return redirect(url_for('dashboard.posts'))


# --- File Upload ---

@dashboard_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """File upload page."""
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename, original, size, mime = save_file(file)
            file_record = File(
                filename=filename,
                original_filename=original,
                file_size=size,
                mime_type=mime,
                user_id=current_user.id
            )
            db.session.add(file_record)
            db.session.commit()
            flash(f'Fichier "{original}" envoyé avec succès.', 'success')
            return redirect(url_for('dashboard.files'))
        flash('Type de fichier non autorisé.', 'danger')

    return render_template('dashboard/upload.html', form=form)


@dashboard_bp.route('/files')
@login_required
def files():
    """List uploaded files."""
    page = request.args.get('page', 1, type=int)
    user_files = current_user.files.order_by(File.uploaded_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/files.html', files=user_files)


@dashboard_bp.route('/files/<int:file_id>/download')
@login_required
def download_file(file_id):
    """Download an uploaded file."""
    file_record = File.query.get_or_404(file_id)
    if file_record.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        file_record.filename,
        as_attachment=True,
        download_name=file_record.original_filename
    )


@dashboard_bp.route('/files/<int:file_id>/delete', methods=['POST'])
@login_required
def delete_file(file_id):
    """Delete an uploaded file."""
    file_record = File.query.get_or_404(file_id)
    if file_record.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    # Remove from disk
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file_record.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(file_record)
    db.session.commit()
    flash('Fichier supprimé.', 'info')
    return redirect(url_for('dashboard.files'))


# --- Settings ---

@dashboard_bp.route('/settings')
@login_required
def settings():
    """User settings page."""
    return render_template('dashboard/settings.html')


# --- Admin ---

@dashboard_bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    """Admin panel - manage users."""
    from app.models import User
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('dashboard/admin.html', users=users)
