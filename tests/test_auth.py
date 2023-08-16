import os
import unittest

from flask import Flask
from werkzeug.exceptions import Forbidden

from root.auth import check_authorization


class TestAuthorization(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_valid_token(self):
        with self.app.test_request_context(
            headers={"Authorization": os.getenv("AUTH")}
        ):

            @check_authorization
            def test_route():
                return "Success access"

            self.assertEqual(test_route(), "Success access")

    def test_invalid_token(self):
        with self.app.test_request_context(headers={"Authorization": "invalid_token"}):

            @check_authorization
            def test_route():
                return "Success access"

            with self.assertRaises(Forbidden) as e:
                test_route()
            self.assertEqual(e.exception.code, 403)


if __name__ == "__main__":
    unittest.main()
