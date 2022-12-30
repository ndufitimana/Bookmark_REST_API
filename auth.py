from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from models import *
from errors import *

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status, message="user not registered")

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error_handler(status):
    msg = f'No Token or Token Expired. Get now token via {url_for("get_token")} endpoint'
    return error_response(status, message=msg)



