from flask import Flask, redirect, url_for, request, jsonify, render_template,Blueprint

view_users_blueprint = Blueprint('view_users',__name__)

def display_list(): 
    data=[
        {'name':'Audrin',},
        {'name': 'Stuvard'},
        {'name':'Eden',},
        {'name': 'Jonathan'},
        {'name':'Alex',},
        {'name': 'Dave'},
        {'name':'Dennis',},
        {'name': 'Enzo'},
    ]

    return render_template("users.html",result=data)
    # return '<h3>Rendered manually<h3>'


def display_user_log():
    # if i remember correctly arg , **args where args here are the data 
    # that can be reutrned so pwede multiple

    data = [
        {
            "user": "I think i lost my mind a while ago", 
            "bot": "cause I've been seeing some ghosts"
        },
        {
            "user": " and i'd be lying if i told you im not, cause i lie", 
            "bot": "these thoughts never speak out loud"
        },
        {
            "user": "Cause we've been driving so long i cant remember how we got here", 
            "bot": "Or how we survived for so long, try'na run from our pride till you set fire to the atmosphere"
        },
        {
            "user": "and I remember how we spent the 23rd feeling six feet under where im 30000 feet in the air", 
            "bot": "chasing the sun down so far east im west bound feeling like the edge of this world is near"
        }
    ]
    user_name = "Denis"

    return render_template("logs.html", logs=data , owner=user_name)

view_users_blueprint.add_url_rule('/users',view_func=display_list,methods=['GET'])
view_users_blueprint.add_url_rule('/user/log',view_func=display_user_log,methods=['GET'])