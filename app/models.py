from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from urllib.parse import urlencode


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    # Note this is created as an aux table without a model class
    # When called, the .c. accesses a column (needed without model)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        # Link of LHS (parent) with association table (secondary)
        secondaryjoin=(followers.c.followed_id == id),
        # Link of RHS ('User') with association table
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
        # Backref is the inverse problem: find the followers of the RHS entity
        # Dynamic: do not run query until specifically requested
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        default = 'retro'
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        base = 'https://www.gravatar.com/avatar/' + digest
        return base + '?' + urlencode({'d': default, 's': str(size)})

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            # Access 'followed' like a list

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0  # \
        # filter_by() can only check equality with a constant

    def followed_posts(self):
        from_self = Post.query.filter_by(user_id=self.id)
        from_followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)  # \
        # Join authors' followers onto posts on condition it's the current \
        # user that is following them.
        # Executing on Post table means subset of Post is returned.
        return from_followed.union(from_self).order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
