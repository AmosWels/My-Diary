from api.tests.test_app import TestStartAll
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import unittest
import json
from ..App.views import app
from .test_entries import user1, user2, user3, entry1, entry2

# jwt = JWTManager(app)
# app.config['SECRET_KEY'] = 'thisisasecretkey'

# auth_user=[user1]
# authuser = auth_user[0]
# auth_user["user_id"] = authuser["user_id"]
# id = auth_user["user_id"]
# access_token = create_access_token(user1["user_id"])
# access_header={'Authorization':'Bearer {}'.format(access_token)}

class TestDiaryEntries(TestStartAll):
    def setUp(self):
        pass
    
    def test_userSignup(self):
        """ Creating a user | supply right data  """
        test = app.test_client(self)
        response = test.post('/api/v1/users/signup',content_type='application/json', data=json.dumps(user1))
        self.assertEqual(response.status_code,400) 
    
    def test_userSignin(self):  
        test = app.test_client(self)
        response = test.post('/api/v1/users/signin',content_type = "application/json", data=json.dumps(user1))
        self.assertEqual(response.status_code,201) 
    
    def test_create_user_entry(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/users/create',content_type='application/json', data=json.dumps(entry1))
        self.assertEqual(response.status_code, 401)
    
    def test_wrong_create_user_entry(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/users/create',content_type='application/json',data=json.dumps(entry2))
        self.assertEqual(response.status_code, 401)
   
    def test_get_all_entries(self):
        """Test API can view all entries."""
        test = app.test_client(self)
        response = test.get('/api/v1/users/allentries',content_type='application/json',
                                      data=json.dumps(entry1))
        self.assertEqual(response.status_code, 401)

    def test_to_get_single_entry(self):
        """test to get a single entry content"""
        test = app.test_client(self)
        response = test.get('/api/v1/users/entry/1', content_type="application/json",data=json.dumps(entry2))
        self.assertEqual(response.status_code, 401)

    def test_forwrongsingle_entry_endpoint(self):
        """test for wrong endpoint """
        test = app.test_client(self)
        response = test.get('/api/v1/users/entry/1hdjh', content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_to_update_entry(self):
        """test to modify or update an entry"""
        test = app.test_client(self)
        response = test.put('/api/v1/users/modify/1', content_type='application/json', data=json.dumps(entry1))
        self.assertEqual(response.status_code,401)
    
    def test_forwrongupdate_entry_endpoint(self):
        """test for wrong endpoint """
        test = app.test_client(self)
        response = test.get('/api/v1/users/modify/2rrrrr', content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_unique_username(self):
        test = app.test_client(self)
        response=test.post('/api/v1/users/signup', data=json.dumps(user3),content_type="application/json") 
        self.assertEqual(response.status_code,400) 

    def test_entry_data(self):
        test = app.test_client(self)
        response=test.post('/api/v1/users/create', data=json.dumps(entry2),content_type="application/json") 
        self.assertEqual(response.status_code,401) 

    def test_duplicate_username(self):
        test = app.test_client(self)
        response=test.post('/api/v1/users/signup',data=json.dumps(user3),content_type="application/json") 
        self.assertEqual(response.status_code,400) 