import json
import os
import unittest

import jwt
import psycopg2
from flask_jwt_extended import create_access_token

from api.App.views import app, db_connect
from api.tests.test_app import TestStartAll
from api.tests.test_entries import (entry1, entry2, entry3, entry4, entry5,entry6, entry7, entry8, entry9, entry10,
                                    user1, user2, user3, user4, user5, user6,user7, user8, user9, userlogin,userprofile,userprofile1)

class TestDiaryEntries(TestStartAll):
    def setUp(self):
        """Define test variables and initialize app."""
        os.environ['app_env'] = 'TESTING'
        # db_connect
        self.app = app                     
        self.get_user_token()

    def get_user_token(self):
        test = app.test_client(self)
        test.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user2))
        response = test.post('/api/v1/auth/login', data=json.dumps(user2),content_type='application/json')
        token=response.json['token']
        access={'Authorization':'Bearer {}'.format(token)}
        return access
            
    def test_userSignup(self):
        """Creating a user supply right data"""
        test = app.test_client(self)
        response = test.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user1))
        self.assertEqual(response.status_code,201)
    
    def test_wrong_userSignup(self):
        """Creating a user supply right data"""
        test = app.test_client(self)
        response = test.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user6))
        self.assertNotIn('Not added',response.data.decode())
        self.assertEqual(response.status_code,201) 

    def test_short_userSignup(self):
        """Creating a user supply right data"""
        test = app.test_client(self)
        response = test.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user7))
        self.assertEqual(response.status_code,400) 
    
    def test_empty_username_userSignup(self):
        """Creating a user supply right data"""
        test = app.test_client(self)
        response = test.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user8))
        self.assertEqual(response.status_code,400) 
    
    def test_empty_password_userSignup(self):
        """Creating a user supply right data"""
        test = app.test_client(self)
        response = test.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user9))
        self.assertEqual(response.status_code,400) 
    
    def test_userSignin(self):  
        test = app.test_client(self)
        response = test.post('/api/v1/auth/login', data=json.dumps(user2),content_type='application/json')
        self.assertEqual(response.status_code,201)

    def test_wrong_userSignin(self):  
        test = app.test_client(self)
        test.post("/api/v1/auth/signup",
                       data=json.dumps(user1), content_type="application/json")
        response2 = test.post('/api/v1/auth/login',
                                  data=json.dumps(userlogin),
                                  content_type='application/json')
        self.assertEqual(response2.status_code,403) 

    def test_create_user_entry(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json', data=json.dumps(entry3))
        self.assertEqual(response.status_code, 201)
    
    def test_wrong_create_user_entry(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json',data=json.dumps(entry2))
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_create_user_date(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json',data=json.dumps(entry6))
        self.assertEqual(response.status_code, 400)
    
    def test_missing_purpose_data(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json',data=json.dumps(entry9))
        self.assertEqual(response.status_code, 400)
    
    def test_missing_name_data(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json',data=json.dumps(entry8))
        self.assertEqual(response.status_code, 400)
    
    def test_missing_create_user_data(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_create_user_data(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json',data=json.dumps(entry7))
        self.assertEqual(response.status_code, 400)
   
    def test_get_all_entries_when_empty(self):
        """Test API can view all entries if empty"""
        test = app.test_client(self)
        response = test.get('/api/v1/entries', headers=self.get_user_token(), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_entries(self):
        """Test API can view all entries."""
        test = app.test_client(self)
        result = self.get_id(test)
        response = test.get('/api/v1/entries', headers=self.get_user_token(), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_to_get_single_entry(self):
        """test to get a single entry content"""
        test = app.test_client(self)
        result = self.get_id(test)
        response = test.get(f'/api/v1/entries/{result[0]}', headers=self.get_user_token(), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def get_id(self, test):
        test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json', data=json.dumps(entry3))
        entries="""select id FROM tdiaryentries"""
        db_connect.cursor.execute(entries)
        db_connect.conn.commit()
        result = db_connect.cursor.fetchone()
        return result

    def test_forwrongsingle_entry_endpoint(self):
        """test for wrong endpoint """
        test = app.test_client(self)
        response = test.get('/api/v1/entries/1', headers=self.get_user_token(), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_to_update_entry(self):
        """test to modify or update an entry"""
        test = app.test_client(self)
        result = self.get_id(test)
        response = test.put(f'/api/v1/entries/{result[0]}', headers=self.get_user_token(), content_type='application/json', data=json.dumps(entry3))
        self.assertEqual(response.status_code,200)
    
    def test_to_delete_entry(self):
        """test to modify or update an entry"""
        test = app.test_client(self)
        result = self.get_id(test)
        response = test.delete(f'/api/v1/entries/{result[0]}', headers=self.get_user_token(), content_type='application/json')
        self.assertEqual(response.status_code,200)
    
    def test_to_delete_entry_wrong_id(self):
        """test to modify or update an entry"""
        test = app.test_client(self)
        response = test.delete(f'/api/v1/entries/1', headers=self.get_user_token(), content_type='application/json')
        self.assertEqual(response.status_code,400)

    def test_to_update_wrong_date_format(self):
        """test to modify or update an entry"""
        test = app.test_client(self)
        result = self.get_id(test)
        response = test.put(f'/api/v1/entries/{result[0]}', headers=self.get_user_token(), content_type='application/json', data=json.dumps(entry10))
        self.assertEqual(response.status_code,400)
    
    def test_to_update_wrong_data_format(self):
        """test to modify or update an entry"""
        test = app.test_client(self)
        result = self.get_id(test)
        response = test.put(f'/api/v1/entries/{result[0]}', headers=self.get_user_token(), content_type='application/json', data=json.dumps(entry7))
        self.assertEqual(response.status_code,400)
    
    def test_forwrongupdate_entry_endpoint(self):
        """test for wrong endpoint """
        test = app.test_client(self)
        response = test.get('/api/v1/entries/1', headers=self.get_user_token(), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_unique_username(self):
        test = app.test_client(self)
        self.get_user_token()
        response=test.post('/api/v1/auth/signup', data=json.dumps(user3),content_type="application/json") 
        self.assertEqual(response.status_code,201) 
    
    def test_duplicate_username(self):
        test = app.test_client(self)
        self.get_user_token()
        response=test.post('/api/v1/auth/signup', data=json.dumps(user2),content_type="application/json") 
        self.assertEqual(response.status_code,400) 

    def test_empty_entry_data(self):
        test = app.test_client(self)
        response=test.post('/api/v1/entries', headers=self.get_user_token(), data=json.dumps(entry2),content_type="application/json") 
        self.assertEqual(response.status_code,400) 
    
    def test_empty_password(self):
        test = app.test_client(self)
        response=test.post('/api/v1/auth/signup',data=json.dumps(user4),content_type="application/json") 
        self.assertEqual(response.status_code,400)
    
    def test_empty_password_field(self):
        test = app.test_client(self)
        response=test.post('/api/v1/auth/signup',data=json.dumps(user9),content_type="application/json") 
        self.assertEqual(response.status_code,400)
    
    def test_empty_username(self):
        test = app.test_client(self)
        response=test.post('/api/v1/auth/signup', data=json.dumps(user5),content_type="application/json") 
        self.assertEqual(response.status_code,400)
    
    def test_empty_username_field(self):
        test = app.test_client(self)
        response=test.post('/api/v1/auth/signup',data=json.dumps(user8),content_type="application/json") 
        self.assertEqual(response.status_code,400)
    
    def test_short_password_length(self):
        """test method for checking password length"""
        test = app.test_client(self)
        response = test.post('/api/v1/auth/signup', data=json.dumps(user7), content_type="application/json")
        self.assertEqual(response.status_code, 400)
    
    def test_get_user_details(self):
        test = app.test_client(self)
        self.get_user_token()
        response=test.get('/api/v1/authuser', headers=self.get_user_token(), content_type="application/json") 
        self.assertEqual(response.status_code,200)
    
    def test_create_user_profile(self):
        test = app.test_client(self)
        response = test.post('/api/v1/authuser/profile', headers=self.get_user_token(),content_type="application/json",data=json.dumps(userprofile))
        self.assertEqual(response.status_code,201)
    
    def test_create_duplicate_user_profile(self):
        test = app.test_client(self)
        test.post('/api/v1/authuser/profile', headers=self.get_user_token(),content_type="application/json",data=json.dumps(userprofile))
        response = test.post('/api/v1/authuser/profile', headers=self.get_user_token(),content_type="application/json",data=json.dumps(userprofile))
        self.assertEqual(response.status_code,409)
    
    def test_create_wrong_user_profile(self):
        test = app.test_client(self)
        response = test.post('/api/v1/authuser/profile', headers=self.get_user_token(),content_type="application/json",data=json.dumps(userprofile1))
        self.assertEqual(response.status_code,400)

    def test_get_user_profile(self):
        test = app.test_client(self)
        test.post('/api/v1/authuser/profile', headers=self.get_user_token(),content_type="application/json",data=json.dumps(userprofile))
        response=test.get('/api/v1/authuser/profile',headers=self.get_user_token(),content_type="application/json") 
        self.assertEqual(response.status_code,200)
        
    def test_get_no_user_profile(self):
        test = app.test_client(self)
        test.post('/api/v1/authuser/profile', headers=self.get_user_token(),content_type="application/json",data=json.dumps(userprofile1))
        response=test.get('/api/v1/authuser/profile',headers=self.get_user_token(),content_type="application/json") 
        self.assertEqual(response.status_code,400) 
    
    def test_get_user_entry_count(self):
        test = app.test_client(self)
        test.post('/api/v1/entries', headers=self.get_user_token(), content_type='application/json', data=json.dumps(entry3))
        response=test.get('/api/v1/authuser/countentry',headers=self.get_user_token(),content_type="application/json") 
        self.assertEqual(response.status_code,200) 
    
    def test_get_no_user_entry_count(self):
        test = app.test_client(self)
        response=test.get('/api/v1/authuser/countentry',headers=self.get_user_token(),content_type="application/json") 
        self.assertEqual(response.status_code,200) 
    
    def test_update_user_profile(self):
        test = app.test_client(self)
        test.post('/api/v1/authuser/profile', headers=self.get_user_token(),content_type="application/json",data=json.dumps(userprofile))
        response = test.put('/api/v1/authuser/profile', headers=self.get_user_token(), content_type='application/json', data=json.dumps(userprofile))
        self.assertEqual(response.status_code,201)
    
    def test_update_no_user_profile(self):
        test = app.test_client(self)
        response = test.put('/api/v1/authuser/profile', headers=self.get_user_token(), content_type='application/json', data=json.dumps(userprofile))
        self.assertEqual(response.status_code,400)

    def tearDown(self):
        users_table="""DELETE FROM tusers"""
        entries_table="""DELETE FROM tdiaryentries"""
        db_connect.cursor.execute(users_table)
        db_connect.conn.commit()
        db_connect.cursor.execute(entries_table)
        db_connect.conn.commit()
