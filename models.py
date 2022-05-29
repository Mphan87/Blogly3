"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class Blogly(db.Model):
    __tablename__ = "bloglys"

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)

    first_name= db.Column(db.Text,
                       nullable=False,)

    last_name = db.Column(db.Text,
                        nullable=False,)

    image_url = db.Column(db.Text,
                        nullable=False,)

    posts = db.relationship("Post", backref="blogly", cascade="all, delete-orphan")                    


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                       primary_key=True)

    title = db.Column(db.Text,
                       nullable=False)

    content = db.Column(db.Text,
                       nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

    blogly_id = db.Column(db.Integer, db.ForeignKey('bloglys.id'), nullable=False)  

class PostTag(db.Model):
    __tablename__ = "postags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    __tablename__ = "tags"


    id = db.Column(db.Integer,
                       primary_key=True)

    name = db.Column(db.Text,
                       nullable=False)

    posts = db.relationship(
        'Post',
        secondary="postags",
        # cascade="all,delete",
        backref="tags",
    )



def connect_db(app):
    db.app = app
    db.init_app(app)
   