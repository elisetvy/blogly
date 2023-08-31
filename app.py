"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

DEFAULT_IMAGE_URL = "https://static.independent.co.uk/s3fs-public/thumbnails/image/2014/01/14/14/google.jpg?width=1200"

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
    image_url = request.form.get("image-url") or DEFAULT_IMAGE_URL
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:id>")
def show_user_details(id):
    """Show user details page."""
    user = User.query.get(id)

    return render_template("user_detail.html", user=user)


@app.get("/users/<int:id>/edit")
def show_user_edit_page(id):
    """Show edit form for user details."""
    user = User.query.get(id)

    return render_template("user_form.html", user=user, edit=True)


@app.post("/users/<int:id>/edit")
def edit_user(id):
    """Update user info in DB and redirect to homepage."""
    user = User.query.get(id)

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
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
