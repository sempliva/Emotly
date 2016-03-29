"""
Emotly Test Suite

Consider adding separate TestCase instance for different features.
KISS: Keep It Stupid Simple
"""
import unittest, emotly

# Empty test case.
class BasicEmotlyTestCase(unittest.TestCase):

    # Runs the test client.
    def setUp(self):
        self.app = emotly.app.test_client()

    def tearDown(self):
        pass

    def test_dummy(self):
        assert True

    def test_emotly_index(self):
        rv = self.app.get('/')
        assert rv.data == b'Ok'

    def test_emotly_echo(self):
        rv = self.app.get('/echo/hello')
        assert rv.data == b'Hello hello'

if __name__ == '__main__':
    unittest.main()
