"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get("/")
def get_homepage():
    """Redirect to list of users page."""
    return redirect("/users")


@app.get("/users")
def show_users():
    """Show user listing."""
    users = User.query.all()

    return render_template("home.html", users=users)


@app.get("/users/new")
def show_new_user_form():
    """Show new user form."""
    return render_template("user_form.html")


@app.post("/users/new")
def add_new_user():
    """Get form info and add new user to DB."""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form.get("image-url")

    if not image_url:
        new_user = User(first_name=first_name,
                        last_name=last_name)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:id>")
def show_user_details(id):
    """Show user details page."""
    user = User.query.get_or_404(id)
    posts = user.posts

    return render_template("user_detail.html", user=user, posts=posts)


@app.get("/users/<int:id>/edit")
def show_user_edit_page(id):
    """Show edit form for user details."""
    user = User.query.get_or_404(id)

    return render_template("user_form.html", user=user, edit=True)


@app.post("/users/<int:id>/edit")
def update_user(id):
    """Update user info in DB and redirect to homepage."""
    user = User.query.get_or_404(id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:id>/delete")
def delete_user(id):
    """Deletes user from database and redirects to homepage."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:id>/posts/new")
def show_post_form(id):
    """Display new post form."""
    user = User.query.get_or_404(id)

    return render_template("new_post_form.html", user=user)


@app.post("/users/<int:id>/posts/new")
def add_post(id):
    """Add post to DB and redirect to user detail page."""
    title = request.form["post-title"]
    content = request.form["post-content"]

    new_post = Post(title=title, content=content, user_id=id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{id}")


@app.get("/posts/<int:id>")
def show_post(id):
    """Display post."""
    post = Post.query.get_or_404(id)
    user = post.user

    return render_template("post_detail.html", user=user, post=post)


@app.get("/posts/<int:id>/edit")
def show_post_edit_form(id):
    """Display edit form for a post."""
    post = Post.query.get_or_404(id)
    user = post.user

    return render_template("edit_post.html", user=user, post=post)


@app.post("/posts/<int:id>/edit")
def update_post(id):
    """Updates post in DB and redirects to post detail page."""
    title = request.form["post-title"]
    content = request.form["post-content"]

    post = Post.query.get_or_404(id)

    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f"/posts/{id}")



@app.post("/posts/<int:id>/delete")
def delete_post(id):
    """Deletes post from DB and redirects to user detail page."""
    post = Post.query.get_or_404(id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")
