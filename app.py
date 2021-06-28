from flask import Flask, redirect, url_for, request, jsonify, render_template
import uuid
from flask_mail import Mail, Message
from user_account import user_account_blueprint

from services.database import db
from blueprints.users import view_users_blueprint

# enable cors
from flask_cors import CORS

app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

# deploy flask
# https://dev.to/techparida/how-to-deploy-a-flask-app-on-heroku-heb

# you also need to add cors in blueprint
# reference:: 
"""
    # https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
    In case anyone is using blueprints, 
    you need to add the CORS() to each blueprint, 
    for example: my_blueprint = Blueprint('my_bp_name', name, url_prefix="/my-prefix") 
    CORS(my_blueprint) – BLang
"""

CORS(user_account_blueprint)

# CORS(user_account_blueprint)
# app.run(debug=True)

app.config['SECRET_KEY']='key'


@app.errorhandler(404)
def not_found(e):
    return render_template('notFound.html')


# https://medium.datadriveninvestor.com/authentication-flask-api-using-json-web-tokens-50104f2f1533
def start():
    response = {}
    response["Flask Server Response"] = "Flask App Running"
    response["Database is alive?"] = db.is_alive()
    
    return jsonify(response),200

def load_html():
    return render_template('index.html')

def display_about():
    return render_template('views/about.html')

# you need to specifiy view_func paramter.. 
app.add_url_rule('/about', view_func=display_about,methods=['GET'])

app.add_url_rule('/app', 'index',load_html,methods=['GET'])
app.register_blueprint(view_users_blueprint,endpoint="v",url_prefix="/view")

app.add_url_rule('/', 'index', load_html,methods=['GET'])

app.register_blueprint(user_account_blueprint,url_prefix="/api/user")


if __name__ == '__main__':
    # db = DatabaseManager()
    app.run(host='127.0.0.1', port=5000, debug=True)