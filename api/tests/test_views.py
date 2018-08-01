from api.tests.test_app import TestStartAll
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import unittest
import json
from api.App.views import app, db_connect
from api.tests.test_entries import user1, user2, user3, userlogin, entry1, entry2, entry3

class TestDiaryEntries(TestStartAll):
    def setUp(self):
        #  """Define test variables and initialize app."""
        app.config['TESTING']=True
        self.app = app                     
        with app.test_request_context():
            self.loggedin_user=dict(user_id=1,username='amos',password='amos123')
            self.access_token=create_access_token(self.loggedin_user)
            self.access={'Authorization':'Bearer {}'.format(self.access_token)}
        # test = app.test_client(self)
        # test.post('/api/v1/users/signup', content_type='application/json', data=json.dumps(user2))
        # response2 = test.post('/api/v1/users/signin',
        #                           data=json.dumps(userlogin),
        #                           content_type='application/json')
        # self.access = response2.json
    
            
    def test_userSignup(self):
        """Creating a user supply right data"""
        test = app.test_client(self)
        response = test.post('/api/v1/users/signup', content_type='application/json', data=json.dumps(user2))
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code,201) 
    
    def test_userSignin(self):  
        test = app.test_client(self)
        test.post("/api/v1/users/signup",
                       data=json.dumps(user1), content_type="application/json")
        response = test.post('/api/v1/users/signin',content_type = "application/json", data=json.dumps(user1))
        response2 = test.post('/api/v1/users/signin',
                                  data=json.dumps(userlogin),
                                  content_type='application/json')
        self.assertEqual(response2.status_code,201) 
    
    # def test_duplicate_create_user_entry(self):
    #     '''Test API to create user entry'''
    #     test = app.test_client(self)
    #     response = test.post('/api/v1/users/create', headers=self.access, content_type='application/json', data=json.dumps(entry1))
    #     self.assertEqual(response.status_code, 409)

    def test_create_user_entry(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/users/create', headers=self.access, content_type='application/json', data=json.dumps(entry3))
        self.assertEqual(response.status_code, 201)
    
    def test_wrong_create_user_entry(self):
        '''Test API to create user entry'''
        test = app.test_client(self)
        response = test.post('/api/v1/users/create', headers=self.access, content_type='application/json',data=json.dumps(entry2))
        self.assertEqual(response.status_code, 400)
   
    # def test_get_all_entries(self):
    #     """Test API can view all entries."""
    #     test = app.test_client(self)
    #     response = test.get('/api/v1/users/allentries',content_type='application/json', headers=self.access, data=json.dumps(entry3))
    #     self.assertEqual(response.status_code, 200)

    def test_to_get_single_entry(self):
        """test to get a single entry content"""
        test = app.test_client(self)
        response = test.get('/api/v1/users/entry/1', headers=self.access, content_type="application/json", data=json.dumps(entry1))
        self.assertEqual(response.status_code, 400)

    def test_forwrongsingle_entry_endpoint(self):
        """test for wrong endpoint """
        test = app.test_client(self)
        response = test.get('/api/v1/users/entry/1hdjh', headers=self.access, content_type="application/json")
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
        self.assertEqual(response.status_code,201) 

    def test_entry_data(self):
        test = app.test_client(self)
        response=test.post('/api/v1/users/create', headers=self.access, data=json.dumps(entry2),content_type="application/json") 
        self.assertEqual(response.status_code,400) 

    def test_duplicate_username(self):
        test = app.test_client(self)
        response=test.post('/api/v1/users/signup',data=json.dumps(user3),content_type="application/json") 
        self.assertEqual(response.status_code,201) 
    
    def tearDown(self):
            users_table="""DELETE FROM tusers"""
            entries_table="""DELETE FROM tdiaryentries"""
            db_connect.cursor.execute(users_table)
            db_connect.cursor.execute(entries_table)
            db_connect.conn.commit()