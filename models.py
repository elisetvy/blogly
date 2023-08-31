"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
DEFAULT_IMAGE_URL = "https://static.independent.co.uk/s3fs-public/thumbnails/image/2014/01/14/14/google.jpg?width=1200"

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
