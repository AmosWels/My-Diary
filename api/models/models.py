from flask import Flask
import psycopg2
import jwt
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, jwt_manager
from api.validate import Validate 
from datetime import datetime, timedelta
from api.App import views
import datetime

now = datetime.datetime.now()
# app = Flask(__name__)

class DiaryDatabase():
    def __init__(self):
        # self.conn_string = "host='localhost' dbname='mydiary' user='postgres' password='root'"
        DATABASE_URL = os.environ["DATABASE_URL"]
        self.conn_string = psycopg2.connect(DATABASE_URL, sslmode='require')

        self.conn = psycopg2.connect(self.conn_string)

        Users="""create table IF NOT EXISTS tusers (id serial primary key not null,username text not null,
                            password text not null)"""
        Entries="""create table IF NOT EXISTS tdiaryentries  (id serial primary key not null,name text not null,
                            due_date text not null, type text not null, purpose text not null, date_created text not null, user_id int)"""
        Userstest="""create table IF NOT EXISTS tusersTest (id serial primary key not null,username text not null,
                            password text not null)"""
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(Users,)
            self.cursor.execute(Entries,)
            self.cursor.execute(Userstest,)
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
            # print(result)
            response = jsonify({"MESSAGE":"WELCOME, YOU HAVE SUCCESFULLY LOGGED IN !!!", "YOUR TOKEN":access_token})
            response.status_code = 201
            return response 
        else:
            response = jsonify({"message":"wrong credentials"})
            response.status_code = 403
            return response  
    
    def create_user_entries(self,name,due_date,type1,purpose,user_id):
        today_date = now.strftime("%Y-%m-%d")
        self.cursor=self.conn.cursor()  
        self.cursor.execute("SELECT * FROM tdiaryentries where name = %s and type = %s and user_id = %s",(name,type1,user_id))
        self.conn.commit()
        result=self.cursor.rowcount
        if result>0:
            response = jsonify({"MESSAGE":"DUPLICATE ENTRY:> YOU HAVE PREVIOUSLY CREATED ENTRY WITH THAT SAME **TYPE** AND **NAME**!!"})
            response.status_code = 409
            return response
        else:   
            sql = "INSERT INTO tdiaryentries(name,due_date,type,purpose,date_created,user_id) VALUES (%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (name,due_date,type1,purpose,today_date,user_id))
            self.conn.commit()
            response = jsonify({"MESSAGE":"YOUR HAS ENTRY HAS BEEN SUCCESFULLY CREATED!"})
            response.status_code = 201
            return response
    
    def get_single_user_entry(self,user_id,entry_id):
        # sql = "SELECT * FROM tdiaryentries where user_id = %s",(user_id)
        self.cursor.execute("SELECT * FROM tdiaryentries where user_id = %s and id = %s ",[user_id,entry_id])
        self.conn.commit()
        entries =self.cursor.rowcount
        if entries > 0: 
            all_entry = self.cursor.fetchall()
            user_entry=[]
            for ent in all_entry:
                result={}
                result["id"]= ent[0]
                result["name"]=ent[1]
                result["due_date"]=ent[2]
                result["type"]=ent[3]
                result["purpose"]=ent[4]
                result["date_created"]=ent[5]
                result["user_id"]=ent[6]
                user_entry.append(result)
            return jsonify({"YOUR SINGLE ID SPECIFIC ENTRY!": user_entry})
        else:
            response = jsonify({"YOUR DONT HAVE A SPECIFIC ENTRY WITH THAT ID!"})
            response.status_code = 400
            return response 

    def get_all_user_entries(self,user_id):
        # sql = "SELECT * FROM tdiaryentries where user_id = %s",(user_id)
        self.cursor.execute("SELECT * FROM tdiaryentries where user_id = %s",[user_id])
        self.conn.commit()
        entries =self.cursor.rowcount
        if entries >=1: 
            all_entries = self.cursor.fetchall()
            user_entry_list=[]
            for ent in all_entries:
                result={}
                result["id"]= ent[0]
                result["name"]=ent[1]
                result["due_date"]=ent[2]
                result["type"]=ent[3]
                result["purpose"]=ent[4]
                result["date_created"]=ent[5]
                result["user_id"]=ent[6]
                user_entry_list.append(result)
            return jsonify({"YOUR ENTRIES SO FAR!": user_entry_list})
    
    def update_user_entryid(self,user_id,update_entry_id,name,due_date,type1,purpose):
        today_date = now.strftime("%Y-%m-%d")
        self.cursor.execute("SELECT  FROM tdiaryentries where user_id = %s and id = %s ",[user_id,update_entry_id])
        self.conn.commit()
        entries = self.cursor.rowcount
        if entries > 0: 
            all_entry_column = self.cursor.fetchone()
            # for column in all_entry_column:
            # if all_entry_column["date_created"] == today_date: 
            valid = Validate(name, purpose)
            if valid.validate_entry():
                self.cursor.execute("UPDATE tdiaryentries SET name = %s, due_date = %s, type = %s, purpose = %s WHERE id = %s", [name, due_date, type1,purpose, update_entry_id])
                self.conn.commit()
                response = jsonify({"MESSAGE": "MODIFIED YOUR ENTRY SUCCESFULLY!"})
                response.status_code = 200
                return response
            else:
                response = jsonify({"MESSAGE": "SHOULD PROVIDE VALID NAME AND PURPOSE OF ENTRY!"})
                response.status_code = 400
                return response
            # else:
            #     response = jsonify({"MESSAGE": "YOU CAN ONLY MODIFY TODAY'S ENTRIES!"})
            #     response.status_code = 400
        else:
            response = jsonify({"MESSAGE": "YOUR DONT HAVE A SPECIFIC ENTRY WITH THAT ID TO BE **MODIFIED**!"})
            response.status_code = 400
            return response


   