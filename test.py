import unittest
from App import app


class FlaskTest(unittest.TestCase):

    # Check for response 200 on index
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code

        self.assertEqual(statuscode, 200)

    # Check for Data returned
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/")

        self.assertTrue(b'Harry Potter i Insygnia Smierci' in response.data)

    # Check for json content
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/restapi?phrase=H")

        self.assertEqual(response.content_type, "application/json")

    # Check for Data in REST API
    def test_index_data_search(self):
        tester = app.test_client(self)
        response = tester.get("/restapi?phrase=H")

        self.assertTrue(b'Harry Potter i Insygnia Smierci' in response.data)

    # Check for response 200 on google
    def test_google(self):
        tester = app.test_client(self)
        response = tester.get("/google")
        statuscode = response.status_code

        self.assertEqual(statuscode, 200)

    # Check for Data returned
    def test_google_data_search(self):
        tester = app.test_client(self)
        response = tester.get("/google?search=harry+potter")

        self.assertTrue(b'Harry Potter i komnata tajemnic' in response.data)

    if __name__ == "__main__":
        unittest.main()
