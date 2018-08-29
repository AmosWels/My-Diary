# from flask import Flask
import psycopg2
import jwt
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, jwt_manager
from api.validate import Validate
from datetime import datetime, timedelta
from ..App import views
import datetime
import os

now = datetime.datetime.now()

class DiaryDatabase():
    def __init__(self):
        Users = """create table IF NOT EXISTS tusers (id serial primary key not null,username text not null,
                            password text not null)"""
        Entries = """create table IF NOT EXISTS tdiaryentries  (id serial primary key not null,name text not null,
                            due_date text not null, type text not null, purpose text not null, date_created text not null, user_id int)"""
        Userprofile = """create table IF NOT EXISTS tuserprofile  (id serial primary key not null,surname text not null,
                           given_name text not null, email text not null, phone_number text not null, date_created text not null, user_id int)"""
        app_env = os.environ.get('app_env', default=None)
        if app_env == 'TESTING':
            self.conn_string = "host='localhost' dbname='diarytestdb' user='postgres' password='root'"
        elif app_env == 'heroku':
            DATABASE_URL = os.getenv('DATABASE_URL', default=None)
            self.conn_string = DATABASE_URL
        else:
            self.conn_string = "host='localhost' dbname='mydiary' user='postgres' password='root'"

        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(Users,)
            self.cursor.execute(Entries,)
            self.cursor.execute(Userprofile,)
            self.conn.commit()
        except:
            print("\n Tables Already Created!!\n")
            
    def signup(self, username, password):
        sql = "INSERT INTO tusers(username, password) VALUES (%s, %s)"
        self.cursor.execute(sql, (username, password))
        self.conn.commit()

    def signin(self, username, password):
        self.cursor.execute(
            "SELECT * FROM  tusers where username = %s and password = %s", (username, password))
        self.conn.commit()
        count = self.cursor.rowcount
        result = self.cursor.fetchone()
        if count == 1:
            expires = timedelta(minutes=60)
            loggedin_user = dict(
                user_id=result[0], username=result[1], password=result[2])
            access_token = create_access_token(
                identity=loggedin_user, expires_delta=expires)
            response = jsonify(
                {"Message": "welcome, you have succesfully logged in !!!", "token": access_token})
            response.status_code = 201
            return response
        else:
            response = jsonify(
                {"Message": "wrong credentials, Please check your credentials and Try again!!!"})
            response.status_code = 403
            return response

    def create_user_entries(self, name, due_date, type1, purpose, user_id):
        today_date = now.strftime("%Y-%m-%d")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "SELECT * FROM tdiaryentries where name = %s and type = %s and user_id = %s", (name, type1, user_id))
        self.conn.commit()
        result = self.cursor.rowcount
        if result > 0:
            return self.duplicateEntryMessage()
        else:
            sql = "INSERT INTO tdiaryentries(name,due_date,type,purpose,date_created,user_id) VALUES (%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(
                sql, (name, due_date, type1, purpose, today_date, user_id))
            self.conn.commit()
            response = jsonify(
                {"Message": "your entry has been succesfully created!"})
            response.status_code = 201
            return response

    def get_single_user_entry(self, user_id, entry_id):
        self.cursor.execute(
            "SELECT * FROM tdiaryentries where user_id = %s and id = %s ", [user_id, entry_id])
        self.conn.commit()
        all_entries = self.cursor.fetchall()
        user_entry_list = []
        self.entrylistloop(all_entries, user_entry_list)
        return jsonify({"entry": user_entry_list})

    def entrylistloop(self, all_entries, user_entry_list):
        for ent in all_entries:
            result = {}
            result["id"] = ent[0]
            result["name"] = ent[1]
            result["due_date"] = ent[2]
            result["type"] = ent[3]
            result["purpose"] = ent[4]
            result["date_created"] = ent[5]
            result["user_id"] = ent[6]
            user_entry_list.append(result)

    def get_all_user_entries(self, user_id):
        # sql = "SELECT * FROM tdiaryentries where user_id = %s",(user_id)
        self.cursor.execute(
            "SELECT * FROM tdiaryentries where user_id = %s", [user_id])
        self.conn.commit()
        entries = self.cursor.rowcount
        if entries >= 1:
            all_entries = self.cursor.fetchall()
            user_entry_list = []
            self.entrylistloop(all_entries, user_entry_list)
            return jsonify({"entries": user_entry_list})

    def update_user_entryid(self, user_id, update_entry_id, name, due_date, type1, purpose):
        self.cursor.execute("UPDATE tdiaryentries SET name = %s, due_date = %s, type = %s, purpose = %s WHERE id = %s", [
                            name, due_date, type1, purpose, update_entry_id])
        self.conn.commit()
        response = jsonify(
            {"Message": "modified your entry succesfully!"})
        response.status_code = 200
        return response
    
    def delete_user_entryid(self, user_id, delete_entry_id):
        self.cursor.execute("DELETE FROM tdiaryentries where user_id = %s and id = %s", [
                            user_id, delete_entry_id])
        self.conn.commit()
        response = jsonify(
            {"Message": "Deleted your entry succesfully!"})
        response.status_code = 200
        return response

    def get_user(self,userid):
        self.cursor.execute("SELECT * FROM tusers where id = %s ", (userid,))
        self.conn.commit()
        
        info = self.cursor.fetchall()
        user_lst = []
        for data in info:
            details = {}
            details["id"] = data[0]
            details["username"] = data[1]
            details["password"] = data[2]
            user_lst.append(details)
            response = jsonify({"user": user_lst})
            response.status_code = 200
        return response
    
    def get_entry_count(self,userid):
        self.cursor.execute("SELECT * FROM tusers join tdiaryentries on \
                    tusers.id = tdiaryentries.user_id where user_id = %s",(userid,))
        self.conn.commit()
        info = self.cursor.fetchall()
        entries = self.cursor.rowcount
        userentry_lst = [{"number" : entries}]
        
        response = jsonify({"entries" : userentry_lst})
        response.status_code = 200
        return response
    
    def create_user_prof(self, surname, given, email, phonenumber, user_id):
        today_date = now.strftime("%Y-%m-%d")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "SELECT * FROM tuserprofile where user_id = %s", (user_id,))
        self.conn.commit()
        result = self.cursor.rowcount
        if result > 0:
            return self.duplicateEntryMessage()
        else:
            sql = "INSERT INTO tuserprofile(surname,given_name,email,phone_number,date_created,user_id) VALUES (%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(
                sql, (surname, given, email, phonenumber,today_date, user_id))
            self.conn.commit()
            response = jsonify(
                {"Message": "succesfully changed your profile!"})
            response.status_code = 201
            return response

    def duplicateEntryMessage(self):
        response = jsonify(
            {"Message": "duplicate entry:> you have previously created entry with the app!!"})
        response.status_code = 409
        return response
    
    def update_user_prof(self, surname, given, email, phonenumber, user_id):
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "SELECT * FROM tuserprofile where user_id = %s", (user_id,))
        self.conn.commit()
        result = self.cursor.rowcount
        if result > 0:
            self.cursor.execute("UPDATE tuserprofile SET surname = %s, given_name = %s, email = %s, phone_number = %s WHERE user_id = %s", [
                            surname, given, email, phonenumber,user_id])
            self.conn.commit()
            response = jsonify(
                {"Message": "succesfully changed your profile!"})
            response.status_code = 201
            return response
        else:
            response = jsonify(
                {"Message": "You can't edit, please first Add your profile!!"})
            response.status_code = 400
            return response
            

    def get_user_profile(self,user):
        self.cursor.execute("SELECT * FROM tuserprofile where user_id = %s ", (user,))
        self.conn.commit()
        
        info = self.cursor.fetchall()
        user_lst = []
        for data in info:
            details = {}
            details["id"] = data[0]
            details["surname"] = data[1]
            details["given_name"] = data[2]
            details["email"] = data[3]
            details["phone_number"] = data[4]
            details["date_created"] = data[5]
            
            user_lst.append(details)
            response = jsonify({"user": user_lst})
            response.status_code = 200
        return response
