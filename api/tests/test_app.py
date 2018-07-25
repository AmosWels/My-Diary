""" start tests module """
import unittest
import json
from api.App.views import app

class TestStartAll(unittest.TestCase):
    """ Base class for view test class """

    app.app_context().push()
    client = app.test_client()