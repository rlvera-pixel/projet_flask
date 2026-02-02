"""Main routes blueprint - home, about, and demo pages."""

from flask import Blueprint, render_template, request, make_response, redirect, url_for, flash
from app.models import Post

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page with recent published posts."""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=5, error_out=False)
    return render_template('main/index.html', posts=posts)


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html')


@main_bp.route('/hello/<name>')
def hello(name):
    """Greeting page with URL variable."""
    return render_template('main/index.html', greeting=f'Bonjour, {name} !')


# Cookie demonstration routes
@main_bp.route('/setcookie', methods=['GET', 'POST'])
def set_cookie():
    """Set a cookie with a user-provided value."""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '')
        resp = make_response(redirect(url_for('main.get_cookie')))
        resp.set_cookie('user_id', user_id, max_age=3600)
        flash('Cookie défini avec succès !', 'success')
        return resp
    return render_template('main/cookie_demo.html')


@main_bp.route('/getcookie')
def get_cookie():
    """Read and display a cookie value."""
    user_id = request.cookies.get('user_id', 'Non défini')
    return render_template('main/cookie_demo.html', cookie_value=user_id)


# Redirect demonstration
@main_bp.route('/user/<name>')
def user_redirect(name):
    """Demonstrate redirect() and url_for() based on user role."""
    if name == 'admin':
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('main.hello', name=name))
