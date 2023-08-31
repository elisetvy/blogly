"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
DEFAULT_IMAGE_URL = '/static/images/catdefault.jpeg'

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(40),
        nullable=False
    )

    last_name = db.Column(
        db.String(40),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=True,
        default=DEFAULT_IMAGE_URL
    )

    posts = db.relationship("Post", backref="user")


class Post(db.Model):
    """Posts."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(75),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    post_tags = db.relationship("PostTag", backref="posts")


class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    posts = db.relationship("Post", secondary="post_tags", backref="tags")

    post_tags = db.relationship("PostTag", backref="tags")


class PostTag(db.Model):
    """PostTag."""

    __tablename__ = 'post_tags'

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )
