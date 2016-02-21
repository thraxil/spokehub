import unittest
from spokehub.invite.views import new_token


class TestNewToken(unittest.TestCase):
    def test_length(self):
        n = new_token()
        self.assertEqual(len(n), 20)
