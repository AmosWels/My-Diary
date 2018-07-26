from api.tests.test_app import TestStartAll
import unittest
import json
from ..App.views import app
from api.tests.test_entries import entry1, entry2, entry3

class TestDiaryEntries(TestStartAll):
    def setUp(self):
        pass
    
    def test_create_entry(self):
        test = app.test_client(self)
        response = test.post('/POST/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))
        self.assertEqual(response.status_code, 201)
   
    def test_get_all_entries(self):
        """Test API can view all entries."""
        test = app.test_client(self)
        response = test.get('/GET/entries',content_type='application/json',
                                      data=json.dumps(entry1))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Lorem Ipsum', str(response.data))

    def test_to_get_single_entry(self):
        """test to get a single entry content"""
        test = app.test_client(self)
        response = test.get('/GET/entries/1', content_type="application/json",data=json.dumps(entry1))
        self.assertEqual(response.status_code, 200)

    def test_forwrong_endpoint(self):
        """test for wrong endpoint """
        test = app.test_client(self)
        response = test.get('/GET/entries/hhhhh', content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_to_update_entry(self):
        """test to modify or update an entry"""
        test = app.test_client(self)
        response = test.put('/PUT/entries/1', content_type='application/json', data=json.dumps(entry1))
        self.assertEqual(response.status_code,200)