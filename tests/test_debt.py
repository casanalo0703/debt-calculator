import unittest
from src.models.debt import Debt

class TestDebt(unittest.TestCase):

    def setUp(self):
        self.debt = Debt(id=1, amount=100.0, due_date='2023-12-31')

    def test_debt_creation(self):
        self.assertEqual(self.debt.id, 1)
        self.assertEqual(self.debt.amount, 100.0)
        self.assertEqual(self.debt.due_date, '2023-12-31')

    def test_debt_amount_update(self):
        self.debt.amount = 150.0
        self.assertEqual(self.debt.amount, 150.0)

    def test_debt_due_date_update(self):
        self.debt.due_date = '2024-01-15'
        self.assertEqual(self.debt.due_date, '2024-01-15')

if __name__ == '__main__':
    unittest.main()