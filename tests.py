from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        # Creates separate in-memory db for testing; doesn't change deployment
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='bjml')
        u.set_password('orange')
        self.assertFalse(u.check_password('purple'))
        self.assertTrue(u.check_password('orange'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=retro&s=128'))

    def test_follow(self):
        # Init users
        u1 = User(username='ben', email='ben@example.com')
        u2 = User(username='sara', email='sara@example2.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        # Follow/unfollow basics
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'sara')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'ben')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # Create four users
        u1 = User(username='donatello', email='don@tmnt.org')
        u2 = User(username='raphael', email='raf@tmnt.org')
        u3 = User(username='leonardo', email='leo@tmnt.org')
        u4 = User(username='michelangelo', email='mic@tmnt.org')
        db.session.add_all([u1, u2, u3, u4])

        # Write four posts, n.b. timed out of order
        now = datetime.utcnow()
        p1 = Post(body="Post from Don", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="Post from Raf", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="Post from Leo", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="Post from Mic", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # Set up followers
        u1.follow(u2)  # Donatello follows Raphael/Michelangelo
        u1.follow(u4)
        u2.follow(u3)  # Raphael follows Leonardo
        u3.follow(u4)  # Leonardo follows Michelangelo (OG)
        db.session.commit()

        # Check followed posts of each user, incl own, in order (recent first)
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
