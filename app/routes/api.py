"""REST API routes blueprint."""

from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.extensions import db, csrf
from app.models import User, Post, Tag
from app.utils import admin_required

api_bp = Blueprint('api', __name__)

# Disable CSRF for API routes (they should use token-based auth in production)
csrf.exempt(api_bp)


# --- Helper ---

def error_response(status_code, message):
    """Return a JSON error response."""
    return jsonify({'error': message}), status_code


# --- Posts API ---

@api_bp.route('/posts', methods=['GET'])
def get_posts():
    """Get all published posts with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 50)  # Limit max per_page

    query = Post.query.filter_by(is_published=True)

    # Search filter
    search = request.args.get('q')
    if search:
        query = query.filter(
            Post.title.ilike(f'%{search}%') | Post.body.ilike(f'%{search}%')
        )

    # Tag filter
    tag = request.args.get('tag')
    if tag:
        query = query.filter(Post.tags.any(Tag.name == tag))

    posts = query.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'posts': [p.to_dict() for p in posts.items],
        'total': posts.total,
        'page': posts.page,
        'pages': posts.pages,
        'has_next': posts.has_next,
        'has_prev': posts.has_prev,
    })


@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a single post by ID."""
    post = Post.query.get_or_404(post_id)
    if not post.is_published:
        return error_response(404, 'Post non trouvé.')
    return jsonify(post.to_dict())


@api_bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    """Create a new post (authenticated)."""
    data = request.get_json()
    if not data:
        return error_response(400, 'Données JSON requises.')

    title = data.get('title')
    body = data.get('body')
    if not title or not body:
        return error_response(400, 'Le titre et le contenu sont requis.')

    post = Post(
        title=title,
        body=body,
        is_published=data.get('is_published', True),
        user_id=current_user.id
    )

    # Handle tags
    tag_names = data.get('tags', [])
    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@api_bp.route('/posts/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    """Update an existing post (owner or admin only)."""
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id and not current_user.is_admin():
        return error_response(403, 'Accès non autorisé.')

    data = request.get_json()
    if not data:
        return error_response(400, 'Données JSON requises.')

    post.title = data.get('title', post.title)
    post.body = data.get('body', post.body)
    post.is_published = data.get('is_published', post.is_published)

    db.session.commit()
    return jsonify(post.to_dict())


@api_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    """Delete a post (owner or admin only)."""
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id and not current_user.is_admin():
        return error_response(403, 'Accès non autorisé.')

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post supprimé.'}), 200


# --- Users API (admin only) ---

@api_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    """Get all users (admin only)."""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({'users': [u.to_dict() for u in users]})


@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def get_user(user_id):
    """Get a single user (admin only)."""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


# --- Tags API ---

@api_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags."""
    tags = Tag.query.order_by(Tag.name).all()
    return jsonify({'tags': [t.to_dict() for t in tags]})
