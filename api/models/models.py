from flask import Flask
import psycopg2
import jwt
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
        if count == 1:
            return True
        else:
            response = jsonify({"message":"wrong credentials"})
            response.status_code = 403
            return response  
            
    def generate_token(self,username):
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': username
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                views.app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, views.app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"