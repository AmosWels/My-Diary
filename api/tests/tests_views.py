from test_app import TestStartAll
import unittest
from flask import json
from test_entries import entry1, entry2, entry3

class TestDiaryEntries(TestStartAll):
    def setUp(self):
        pass
    
    def test_create_entry(self):
        response = self.client.post('/POST/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))
        self.assertEqual(response.status_code, 201)
   
    def test_get_all_entries(self):
        """Test API can view all entries."""
        response = self.client.get('/GET/entries',content_type='application/json',
                                      data=json.dumps(entry1))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Lorem Ipsum', str(response.data))

    def test_to_get_single_entry(self):
        """test to get a single entry content"""
        response = self.client.get('/GET/entries/1', content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_forwrong_endpoint(self):
        """test for wrong endpoint """
        response = self.client.get('/GET/entries/hhhhh', content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_to_update_entry(self):
        """test to modify or update an entry"""
        response = self.client.put('/PUT/entries/1', data=json.dumps(dict(purpose="Meet Peter")), content_type='application/json')
        self.assertEqual(response.status_code,400)