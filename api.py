from flask import Flask, request
import pandas
from db import postgres, cur
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import exceptions




app = Flask(__name__)

def check_user(username,password):
    params = request.view_args
    new_u = params['username']
    credentials = cur.execute(f"SELECT * FROM users WHERE username = '{new_u}';")
    dbpass = credentials.one()[2]
    check_pass = check_password_hash(dbpass, params['password']) 

    return check_pass

@app.errorhandler(exceptions.NotFound)
def handle_bad_request(e):
    response = {
        "message": "Page not found",
        "Available urls":
          (
            "POST","/creatuser/<username>/<password>",
            "POST","/login/<username>/<password>",
            "POST","/events/<username>/<password>/<event_type>/<event_data>",
            "GET","/events/<username>/<password>",
            "GET","/events/<username>/<password>/<id>"
          )
    }
    return response, 404

@app.route("/createuser/<username>/<password>", methods = ["POST"])
def create_user(username,password):
    try:
        params = request.view_args
        cur.execute('CREATE TABLE IF NOT EXISTS users (id bigserial, username varchar UNIQUE, password varchar, createdat TIMESTAMP DEFAULT NOW(), updatedat TIMESTAMP  DEFAULT NOW());')
        new_user = [{
            "username": params["username"],
            "password": generate_password_hash(params["password"])
        }]
        df = pandas.DataFrame.from_dict(new_user)

        df.to_sql(name='users', con=postgres, if_exists='append', index=False)
        return "User saved", 201
    except:
        return "User already exists",400

@app.route("/users/<username>/<password>")
def retrieve_all_users(username,password):
    try:
        params = request.view_args
        loginuser = check_user(params['username'], params['password'])
        if loginuser is True:
            users = cur.execute('SELECT id, username,createdat,updatedat FROM users;')
            all_users = users.all()   
            response = [{"id":id, "username":username, "created_at":created_at, "updated_at":updated_at }for id,username,created_at,updated_at in all_users]

            return response
        else:
            return "An error occurred. Check your credentials",400
    except:
        return "Credentials not correct. Url must be in the form users/<username>/<password>"

@app.route("/login/<username>/<password>", methods = ["POST"])
def login(username,password):
    params = request.view_args
    credentials = check_user(params['username'], params['password'])
    if credentials is True:
        return "User logged in successfully",200
    else:
        return "User password incorrect",400

@app.route("/events/<username>/<password>/<event_type>/<event_data>", methods= ["POST"])
def log_event(username,password,event_type,event_data):
    params = request.view_args
    loginuser = check_user(params['username'], params['password'])
    if loginuser is True:
        cur.execute('CREATE TABLE IF NOT EXISTS events (id bigserial, event_type varchar, event_data jsonb, performed_by varchar, createdat TIMESTAMP DEFAULT NOW(), updatedat TIMESTAMP  DEFAULT NOW());')
        new_data = [{
            "event_type": params["event_type"],
            "event_data":params["event_data"],
            "performed_by": params["username"]
            }]
        df = pandas.DataFrame.from_dict(new_data)
        df.to_sql(name="events", con=postgres, if_exists='append', index=False)

        return "Event logged successfully",201
    else:
        return "An error occurred. Check your credentials",400

@app.route("/events/<username>/<password>")
def retrieve_all_events(username,password):
    try:
        params = request.view_args
        loginuser = check_user(params['username'], params['password'])
        if loginuser is True:
            events = cur.execute('SELECT * FROM events;')
            new_events = events.all()   
            response = [{"id":id, "event_type":event_type, "event_data": event_data, "user":users, "created_at":created_at, "updated_at":updated_at }for id,event_type,event_data,users,created_at,updated_at in new_events]

            return response
        else:
            return "An error occurred. Check your credentials",400
    except:
        return "Credentials not correct. Url must be in the form events/<username>/<password>"

@app.route("/events/<username>/<password>/<id>")
def get_event_by_id(username,password,id):
    try:
        params = request.view_args
        loginuser = check_user(params['username'], params['password'])
        if loginuser is True:
            index = request.view_args["id"]
            events = cur.execute(f'SELECT * FROM events WHERE "id" = {index};')
            new_event = events.one()
            columns = ("id", "event_type", "event_data", "users")
            response = dict(zip(columns,new_event))
            return response
        else:
            return "An error occurred. Check your credentials",400
    except:
        return "Either credentials are wrong or a matching query does not exist. Url must be in the form events/<username>/<password>/<id>"
