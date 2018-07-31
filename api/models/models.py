from flask import Flask
import psycopg2
import jwt
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, jwt_manager
from api.validate import Validate 
from datetime import datetime, timedelta
from api.App import views
# app = Flask(__name__)

class DiaryDatabase:
    def __init__(self):
        self.conn_string = "host='localhost' dbname='My-Diary' user='postgres' password='root'"

        self.conn = psycopg2.connect(self.conn_string)

        Users="""create table IF NOT EXISTS tusers (id serial primary key not null,username text not null,
                            password text not null)"""
        Entries="""create table IF NOT EXISTS tdiaryentries  (id serial primary key not null,name text not null,
                            due_date text not null, type text not null, purpose text not null, date_created text not null, user_id int)"""

        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(Users,)
            self.cursor.execute(Entries,)
            self.conn.commit()
            # print("Created Succesfuly\n")
        except:
            print("Already Created\n")

    def signup(self,username,password):
        valid = Validate(username, password)
        if valid.validate_entry():
            sql = "INSERT INTO tusers(username, password) VALUES (%s, %s)"
            self.cursor.execute(sql, (username, password))
            self.conn.commit()
        else:
            return jsonify({"message": "username, invalid "})
        return jsonify({"message": "Account successfully created"})
        # hashed_password = generate_password_hash(password, method="sha256")
    # @jwt_refresh_token_required
    def signin(self, Lusername,Lpassword):
        self.cursor.execute("SELECT * FROM  tusers where username = %s and password = %s", (Lusername, Lpassword))   
        self.conn.commit()
        count = self.cursor.rowcount
        result = self.cursor.fetchone()
        if count == 1:
            expires = timedelta(minutes=120)
            loggedin_user=dict(user_id=result[0],username=result[1],password=result[2])
            access_token = create_access_token(identity=loggedin_user, expires_delta=expires)
            print(result)
            response = jsonify({"MESSAGE":"WELCOME, YOU HAVE SUCCESFULLY LOGGED IN!!!", "YOUR TOKEN":access_token})
            response.status_code = 201
            return response 
        else:
            response = jsonify({"message":"wrong credentials"})
            response.status_code = 403
            return response  
            
   