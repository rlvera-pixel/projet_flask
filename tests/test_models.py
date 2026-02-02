"""Tests for database models."""

from app.models import User, Post, Tag, File


class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self, db):
        user = User(username='john', email='john@example.com')
        user.set_password('secret')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'john'
        assert user.role == 'user'
        assert user.is_active is True

    def test_password_hashing(self, db):
        user = User(username='jane', email='jane@example.com')
        user.set_password('mysecret')
        assert user.password_hash != 'mysecret'
        assert user.check_password('mysecret') is True
        assert user.check_password('wrong') is False

    def test_is_admin(self, db):
        user = User(username='admin', email='admin@example.com', role='admin')
        user.set_password('admin')
        db.session.add(user)
        db.session.commit()

        assert user.is_admin() is True

        normal_user = User(username='normal', email='normal@example.com')
        normal_user.set_password('normal')
        assert normal_user.is_admin() is False

    def test_user_to_dict(self, sample_user):
        data = sample_user.to_dict()
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert 'password_hash' not in data

    def test_unique_username(self, db):
        user1 = User(username='unique', email='u1@example.com')
        user1.set_password('pass')
        db.session.add(user1)
        db.session.commit()

        user2 = User(username='unique', email='u2@example.com')
        user2.set_password('pass')
        db.session.add(user2)

        import sqlalchemy
        try:
            db.session.commit()
            assert False, "Should have raised IntegrityError"
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()


class TestPostModel:
    """Tests for the Post model."""

    def test_create_post(self, db, sample_user):
        post = Post(title='Test Post', body='Content here', user_id=sample_user.id)
        db.session.add(post)
        db.session.commit()

        assert post.id is not None
        assert post.author.username == 'testuser'
        assert post.is_published is True

    def test_post_with_tags(self, db, sample_user):
        tag = Tag(name='python')
        db.session.add(tag)

        post = Post(title='Tagged Post', body='Content', user_id=sample_user.id)
        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()

        assert len(post.tags) == 1
        assert post.tags[0].name == 'python'

    def test_post_to_dict(self, db, sample_user):
        post = Post(title='Dict Post', body='Body', user_id=sample_user.id)
        db.session.add(post)
        db.session.commit()

        data = post.to_dict()
        assert data['title'] == 'Dict Post'
        assert data['author'] == 'testuser'


class TestFileModel:
    """Tests for the File model."""

    def test_create_file(self, db, sample_user):
        file = File(
            filename='abc123.png',
            original_filename='photo.png',
            file_size=1024,
            mime_type='image/png',
            user_id=sample_user.id
        )
        db.session.add(file)
        db.session.commit()

        assert file.id is not None
        assert file.owner.username == 'testuser'
        assert file.to_dict()['filename'] == 'photo.png'
