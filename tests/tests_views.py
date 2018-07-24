from .test_run import TestStartAll
import unittest
from flask import json
from .test_entries import entry1, entry2, entry3


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
        response = self.client.get('/GET/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Lorem Ipsum', str(response.data))