from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import url_for
import base64
import os


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(124), index= True, unique=True)
    password_hash= db.Column(db.String(128))
    bookmarks = db.relationship("Bookmark", backref="owner", lazy='dynamic')
    token = db.Column(db.String(32), index= True, unique=True)
    token_expiration = db.Column(db.DateTime)
    
    def __repr__(self):
        return f"User: {self.email}"
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return  check_password_hash(self.password_hash, password)
    def to_dictionary(self, include_email=False):
        data = {
            "id":self.id,
            "bookmark_count":self.bookmarks.count(),
            "_links": {
                "self": url_for("get_user", id=self.id)
            }
            
        }
        if include_email:
            data["email"] = self.email
        return data
    def from_dictionary(self, data, new_user = False):
            if "email" in data:
                setattr(self, "email", data["email"])
            
            if new_user and "password" in data:
                self.set_password(data["password"])
    def get_bookmarks(self):
        if self.bookmarks.count()>0:
            data = self.to_dictionary(include_email=True)
            data["bookmarks"] = []
            for bookmark in self.bookmarks:
                data["bookmarks"].append({
                    "bookmark_id": bookmark.id,
                    "bookmark_url":bookmark.url,
                    "saved":bookmark.timestamp.isoformat() + 'Z',
                    "headline":bookmark.headline if bookmark.headline else None,
                    "read_flag":bookmark.read_flag
                })
            return data
        return None
        
    def get_token(self, expires_in = 3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    def revoke_token(self):
        self.token_expiration = datetime.utcnow()+ timedelta(seconds = 1)
    @staticmethod   
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(240), index= True)
    headline = db.Column(db.String(300), index= True)
    read_flag = db.Column(db.Integer, default = 0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"Bookmark: {self.url}"
    def to_dictionary(self):
        data = {
            "id":self.id,
            "bookmark_url":self.url,
            "bookmark_headline":self.headline,
            "read_flag":self.read_flag,
            "saved": self.timestamp.isoformat()+'Z',
            "_links": {
                "self": url_for("get_bookmark", bookmark_id=self.id)
                }
                 
            }
            
        return data
    def from_dictionary(self, data):
        for field in ["url", "headline", "owner"]:
            if field in data:
                setattr(self, field, data[field])
            