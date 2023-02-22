import unittest
from methods import Token, Restricted

from flask import Flask


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'Ly8w3wjd7yXF64FiADFnxNs1ouPrGauB'
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.convert = Token()
        self.validate = Restricted()
        self.convert = Token()
        self.validate = Restricted()

    def tearDown(self):
        self.ctx.pop()

    def test_generate_token(self):
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzcyI6InNlY3JldCJ9._K-V6B0kanvSlJYH9r8mThdTWyuvaWKhhimvykuofNA', self.convert.generate_token('admin', 'secret'))

    def test_access_data(self):
        self.assertEqual('You are under protected data', self.validate.access_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzcyI6InNlY3JldCJ9._K-V6B0kanvSlJYH9r8mThdTWyuvaWKhhimvykuofNA'))


if __name__ == '__main__':
    unittest.main()
