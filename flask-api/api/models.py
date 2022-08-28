"""Database models."""
from email.policy import default
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    website = db.Column(db.String(60), index=False, unique=False, nullable=True)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False,nullable=True)
    

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def set_creation_date(self):
        self.created_on = datetime.today()

    def set_last_login(self):
        self.last_login = datetime.today()
        db.session.commit()

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    """Posts model."""
# added FK relationship between user id and owner id 
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.String(), unique=False, nullable=False)
    owner = db.Column(db.String(16), db.ForeignKey(User.id),unique=False, nullable=False)
    
class Comment(db.Model):
    """
    Comments Model.
    """
    #FK relationship between commentsid and postid
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
    owner = db.Column(db.String(16), unique=False, nullable=False)
    text = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
   
class Likes(db.Model):
    """
    Likes Model.
    """
    #FK relationship betwee likesid and postid
    __tablename__= 'Likes'
    id = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
    owner = db.Column(db.String(16), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
   
