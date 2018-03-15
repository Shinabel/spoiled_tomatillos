import unittest
import os
#from app import app as my_app
from config import Config
import pytest

@pytest.fixture
def app():
    pass
#    app = create

class MyTestClass(unittest.TestCase): 

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass 

    # clean up logic for the test suite declared in the test module
    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass 

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        pass
#        my_app.app.testing = True
#        self.app = my_app.app.test_client()

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    # test method
    def test_equal_numbers(self):
        self.assertEqual(2, 2) 
        
    

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()