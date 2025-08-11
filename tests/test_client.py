import unittest
from src.models.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client(id=1, name="John Doe")

    def test_client_creation(self):
        self.assertEqual(self.client.id, 1)
        self.assertEqual(self.client.name, "John Doe")

    def test_client_name_update(self):
        self.client.name = "Jane Doe"
        self.assertEqual(self.client.name, "Jane Doe")

if __name__ == '__main__':
    unittest.main()