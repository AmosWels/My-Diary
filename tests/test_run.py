""" start tests module """
import unittest
from flask import json
from apprun import app

class TestStartAll(unittest.TestCase):
    """ Base class for view test class """

    app.app_context().push()
    client = app.test_client()