import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.

        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(
            title="test post post title",
            content="testing blah blah content post blog",
            user_id = self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_user_form(self):
        """Test if new user page renders and contains form."""
        with self.client as c:
            resp = c.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)
            self.assertIn("Add", html)

    def test_user_details(self):
        """Test if user detail page renders."""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test1_first', html)
            self.assertIn('Edit', html)
            self.assertIn("Delete", html)

    def test_add_user(self):
        """Tests add user button; checks if redirect occurs."""
        with self.client as c:
            resp = c.post('/users/new', data={
                'first-name': 'Jay',
                'last-name': 'Catsby',
                'image-url': ''
            })

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

    def test_add_user_redirect(self):
        """Test if new user has been added to user list."""
        with self.client as c:
            resp = c.post('/users/new', data={
                'first-name': 'Jay',
                'last-name': 'Catsby',
                'image-url': ''
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jay Catsby', html)

    def test_new_post_form(self):
        """Test if new post page renders."""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add Post for', html)

    def test_show_post(self):
        """Test to show post."""
        with self.client as c:
            resp = c.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testing blah blah content post blog', html)

    def test_add_post(self):
        """Test to add post."""
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/posts/new', data={
                'post-title': 'i am cat',
                'post-content': 'jay is a cat meow'
            })

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{self.user_id}")

    def test_add_post_redirect(self):
        """Test if adding a post redirects to the user page."""
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/posts/new', data={
                'post-title': 'i am cat',
                'post-content': 'jay is a cat meow'},
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('i am cat', html)

    def test_delete_post(self):
        """Test delete post."""
        with self.client as c:
            resp = c.post(f'/posts/{self.post_id}/delete')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{self.user_id}")

    def test_delete_post_redirect(self):
        """Test if deleting a post redirects to user details page."""
        with self.client as c:
            resp = c.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('test post post title', html)
