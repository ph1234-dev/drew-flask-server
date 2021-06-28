from flask import Flask, redirect, url_for, request, jsonify
import uuid
from flask_mail import Mail, Message
app = Flask(__name__)

class User:

    def __init__(self,id,name):
        self.id = id
        self.name = name

user_list = []

def start():
    return "Flask App Running %s" % user_list[0].id

def register():
    if request.method == 'POST':
        return "POST, Register "
    elif request.method== 'GET':
        return "GET , Register"
    else: 
        return "something went wrong"

def submit_survey_result():
    return "Survey"

def login():
    return "going to login2"
  
def login_user(user):
    return "going to login:: %s" % (user)  

def log_content():
    return "log dcontent:: "

def redirect_content():
    # redirect can use the 3 parameters of add url.. the path, the symbolic name, the function
    return redirect(url_for('log'))
    # return "x"

method_get = ['GET']

# app.add_url_rule('/mail', 'mail', send_mail)
app.add_url_rule('/', 'start', start,method_get)
app.add_url_rule('/login', 'login', login)
app.add_url_rule('/login/<user>', 'login_user', login_user)
app.add_url_rule('/log', 'log', log_content)
app.add_url_rule('/redirect','redirect',redirect_content)
app.add_url_rule('/register','register',register,methods=['POST','GET'])
app.add_url_rule('/submit_survey','submit_survey',submit_survey_result)

if __name__ == '__main__':
    user_list.append(User(str(uuid.uuid4()),"data1"))
    user_list.append(User(str(uuid.uuid4()),"data2"))
    app.run(host='127.0.0.1', port=5000, debug=True)