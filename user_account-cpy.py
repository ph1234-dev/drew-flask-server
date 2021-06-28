from flask import Blueprint,jsonify,make_response
from flask import request

import json

from services.user_service import User_Service
from services.log_service import Log_Service
from services.database import db

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import re 
from datetime import datetime, timedelta
from functools import wraps

# Read for documentation
# https://realpython.com/flask-blueprint/#what-a-flask-application-looks-like
user_account_blueprint = Blueprint('user_account_blueprint',__name__)
     

user_service = User_Service()
log_service = Log_Service()


# read about this
# https://medium.datadriveninvestor.com/authentication-flask-api-using-json-web-tokens-50104f2f1533
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        print("\Headers:: ") 
        print(*request.headers)

        # X-Access-Token needs to be same captials in fetch api and server
        # X-Access-Token should be captial 
        # in both headers and servers..

        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return 'Unauthorized Access!', 401

        # try:
        #     coll = db[config.MONGO_AUTH]
        #     data = jwt.decode(token, config.SECRET_KEY)
        #     current_user = coll.find_one({'user_id': data['user_id']})
        #     if not current_user:
        #         return 'Unauthorized Access!', 401
        # except:
        #     return 'Unauthorized Access!', 401

        # try:
        #     token = request.headers['X-Access-Token']
        #     data = jwt.decode(token, 'key',algorithms=['HS256'])
        #     result = user_service.check_user_exist(data['user_id'])
        #     if ( result['user_id'] is None):
        #         return 'Unauthorized Access!', 401
        # except (Exception):
        #     return 'Unauthorized Access!', 401

        return f(*args, **kwargs)

    return decorated



@token_required
def log():
    response = {}
    json = request.get_json()
    response ['message'] = json['userMessage']
    response ['reply'] = json['botReply']
    
    print("Log Post request data:: ")
    print(json['userMessage'])

    # user_message = json['userMessage']
    # bot_reply = json['botReply']

    token = request.headers['X-Access-Token']
    data = jwt.decode(token, 'key',algorithms=['HS256'])

    print("X-Access-Token Parsin:: ")
    print(*data)


    response['token header id'] = data['id']

    user_id = data['id']
    user_message = json['userMessage']
    bot_response = json['botReply']
    result = log_service.log_conversation(user_id,user_message,bot_response)

    if result['success'] == True:
        response['success'] = True
    else:
        response['success'] = False
        response['error'] = result['error']

    return jsonify(response)

def check_user():
    json = request.get_json()
    id = json['id']
    
    result = user_service.check_userid_exist(id)
    # print(result)
    return result

def login():

    response = {}
    json = request.get_json()
    username = json['username']
    password = json['password']

    database_status = db.is_alive()
    response["Database is alive?"] = database_status

    if database_status == True:
        result = user_service.login_user(username,password)
    else:
        return response , 503

    # print("Login PY:: ")
    # print( *result)

    if result['success'] == True:
            
        # read the docs
        # https://pypi.org/project/PyJWT/1.4.0/
        response['name'] = result['name']
        response['token'] = jwt.encode({
                'id': result['id'],
                'exp': datetime.utcnow() + timedelta(hours=24)
                }, 
                'key',
                algorithm='HS256')

        # response["id"] = result['id']
        # response["message"] = "user has login successfully"
        response["success"] = True
    else:
        response['success'] = False
        # response['message'] = "unsuccessful login" 

    # deco = jwt.decode(token,'key',algorithms=['HS256'])

    # result["decoded"] = deco['user_id']

    # response["token"] = result['token']

    return response , 200

def logout():
    return "Logging out user"

def create_account(): 

    json = request.get_json()
    username = json['username']
    password = json['password']
    name =json['name']

    result = user_service.create_user(username,password,name)

    return (result)


def test_receive_account():
    json = request.get_json()
    
    response = {}
    username = json['username']
    password = json['password']
    name = json['name']

    result = user_service.check_username_exist(username)


    if result['exist']:
        response['error'] =  True
        response['error_message'] = 'username exist already' 
    else:
        response = user_service.create_user(username,password,name)
        response['error'] = False
        response['success_message'] = "successfully created user"    
    
    # print (response)

    return jsonify(response)
 
def test():
    return "<h2>Test of blueprinst<h2>"

def testDatabase():
    result = db.execute_query("SELECT * FROM USERS")
    return jsonify(result)

# https://flask.palletsprojects.com/en/2.0.x/api/
# add_url_rule(rule, endpoint=None, view_func=None, provide_automatic_options=None, **options)

# add_url_rule([route],[function_name] <-Optional if you set view_func,['view'],methods)
user_account_blueprint.add_url_rule('/login',view_func=login,methods=['POST'])
user_account_blueprint.add_url_rule('/register',view_func=create_account,methods=['POST'])
user_account_blueprint.add_url_rule('/log',view_func=log,methods=['POST'])
user_account_blueprint.add_url_rule('/check_user',view_func=check_user,methods=['POST'])

# testing purpose
user_account_blueprint.add_url_rule('/test_receive_account',view_func=test_receive_account,methods=['POST'])


user_account_blueprint.add_url_rule('/blueprint',view_func=test,methods=['get'])
user_account_blueprint.add_url_rule('/testDatabase',view_func=testDatabase,methods=['GET'])

"""
200 OK.The request was successfully completed.

201 Created. A new resource was successfully created.

400 Bad Request.The request was invalid.

401 Unauthorized.The request did not include an authentication token or the authentication token was expired.

403 Forbidden.The client did not have permission to access the requested resource.

404 Not Found. The requested resource was not found.

405 Method Not Allowed. The HTTP method in the request was not supported by the resource. For example, the DELETE method cannot be used with the Agent API.

409 Conflict. The request could not be completed due to a conflict. For example,  POST ContentStore Folder API cannot complete if the given file or folder name already exists in the parent location.

500 Internal Server Error.The request was not completed due to an internal error on the server side.

503 Service Unavailable.The server was unavailable.

"""