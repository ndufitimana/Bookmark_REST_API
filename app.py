from flask import Flask, jsonify, url_for , request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import validators


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Bookmark
from errors import *
from auth import *

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Bookmark": Bookmark}


""" HANDLING TOKENS """

@app.route("/tokens", methods = ['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({"token":token})

@app.route("/tokens", methods = ['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204


""" API ENDPOINTS """
@app.route("/users/<int:id>", methods= ['GET'])
@token_auth.login_required
def get_user(id):
    if token_auth.current_user().id == id:
        return jsonify(User.query.get_or_404(id).to_dictionary(include_email=True))
        
    return jsonify(User.query.get_or_404(id).to_dictionary())

@app.route("/users", methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if "email" not in data or "password" not in data:
        return bad_request("must include an email and password")
    if User.query.filter_by(email=data["email"]).first():
        return bad_request("Please specify a different email address")
    user = User()
    user.from_dictionary(data, new_user = True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dictionary(include_email=True))
    response.status_code = 201 
    response.headers['Location'] = url_for('get_user', id = user.id)
    return response

@app.route("/bookmark", methods= ['POST'])
@token_auth.login_required
def create_bookmark():
    data = request.get_json() or {}
    if "url" not in data or not(validators.url(data["url"])):
        return bad_request("must provide a a valid")
    data["owner"] = token_auth.current_user()
    bookmark = Bookmark()
    bookmark.from_dictionary(data)
    db.session.add(bookmark)
    db.session.commit()
    response = jsonify(bookmark.to_dictionary())
    response.status_code = 201 
    response.headers['Location'] = url_for('get_bookmark', bookmark_id = bookmark.id)
    return response
       
@app.route("/bookmarks", methods = ['GET'])
@token_auth.login_required
def get_all_bookmarks():
    data = token_auth.current_user().get_bookmarks()
    if data:
        return jsonify(data)
    else:
        return bad_request("No bookmarks saved!")
    
@app.route("/bookmark/<int:bookmark_id>", methods = ['GET'])
@token_auth.login_required
def get_bookmark(bookmark_id):
    try:
        bookmark = token_auth.current_user().bookmarks.filter(Bookmark.id==bookmark_id).one()
        return jsonify(bookmark.to_dictionary())
    except:
        msg = f'bookmark with id {bookmark_id} not found'
        return error_response(404, message=msg)

