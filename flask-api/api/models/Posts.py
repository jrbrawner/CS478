from datetime import datetime
from os import abort
from flask import (
    Blueprint,
    redirect,
    render_template,
    flash,
    request,
    session,
    url_for,
    jsonify,
    Response,
)
from flask_login import login_required, logout_user, current_user, login_user
from api.models.db import db
from flask_login import logout_user
from flask import current_app as app
from sqlalchemy import engine, create_engine
import logging


post_bp = Blueprint("post_bp", __name__)

liked = db.relationship(
    "PostLike", db.ForeignKey("PostLike.user_id"), backref="user", lazy="dynamic"
)


class Post(db.Model):
    """Posts model."""

    __tablename__ = "Posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.String(), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    likes = db.relationship("PostLike", backref="Posts", lazy="dynamic")
    #comments = db.relationship("PostComment", backref="Posts", lazy="dynamic")

    def serialize(self):

        return {
            'post_id': self.id,
            'post_title': self.title,
            'post_content': self.content,
            'likes': [x.serialize() for x in self.likes]
        }




class PostLike(db.Model):
    __tablename__ = "post_like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("Posts.id"))

    def like_post(self, post, user):
        if not self.has_liked_post(post):
            like = PostLike(user_id=user.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return (
            PostLike.query.filter(
                PostLike.user_id == self.id, PostLike.post_id == post.id
            ).count()
            > 0
        )

    def serialize(self):
        return {
            'user_id': self.user_id
        }
