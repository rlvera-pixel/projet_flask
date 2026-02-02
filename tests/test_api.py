"""Tests for REST API routes."""

import json
from app.models import Post


class TestPostsAPI:
    """Tests for posts API endpoints."""

    def test_get_posts_empty(self, client, db):
        response = client.get('/api/v1/posts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['posts'] == []
        assert data['total'] == 0

    def test_get_posts_with_data(self, client, db, sample_user):
        post = Post(title='API Post', body='Content', user_id=sample_user.id, is_published=True)
        db.session.add(post)
        db.session.commit()

        response = client.get('/api/v1/posts')
        data = json.loads(response.data)
        assert data['total'] == 1
        assert data['posts'][0]['title'] == 'API Post'

    def test_get_single_post(self, client, db, sample_user):
        post = Post(title='Single', body='Body', user_id=sample_user.id, is_published=True)
        db.session.add(post)
        db.session.commit()

        response = client.get(f'/api/v1/posts/{post.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Single'

    def test_get_nonexistent_post(self, client, db):
        response = client.get('/api/v1/posts/999')
        assert response.status_code == 404

    def test_create_post_unauthenticated(self, client, db):
        response = client.post('/api/v1/posts',
                               data=json.dumps({'title': 'New', 'body': 'Body'}),
                               content_type='application/json')
        # Should redirect to login or return 401/302
        assert response.status_code in (302, 401)

    def test_create_post_authenticated(self, auth_client, db):
        response = auth_client.post('/api/v1/posts',
                                    data=json.dumps({'title': 'Auth Post', 'body': 'Content'}),
                                    content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Auth Post'

    def test_search_posts(self, client, db, sample_user):
        post = Post(title='Flask Tutorial', body='Learn Flask', user_id=sample_user.id, is_published=True)
        db.session.add(post)
        db.session.commit()

        response = client.get('/api/v1/posts?q=Flask')
        data = json.loads(response.data)
        assert data['total'] == 1

        response = client.get('/api/v1/posts?q=Django')
        data = json.loads(response.data)
        assert data['total'] == 0

    def test_pagination(self, client, db, sample_user):
        for i in range(15):
            db.session.add(Post(title=f'Post {i}', body='Body', user_id=sample_user.id, is_published=True))
        db.session.commit()

        response = client.get('/api/v1/posts?per_page=5')
        data = json.loads(response.data)
        assert len(data['posts']) == 5
        assert data['total'] == 15
        assert data['has_next'] is True


class TestTagsAPI:
    """Tests for tags API endpoints."""

    def test_get_tags_empty(self, client, db):
        response = client.get('/api/v1/tags')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['tags'] == []
