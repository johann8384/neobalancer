from src.main import Compute
from twisted.trial import unittest

class ComputeTestCase(unittest.TestCase):
    def setUp(self):
        self.calc = Compute()

    def _test(self, operation, a, b, expected):
        result = operation(a, b)
        self.assertEqual(result, expected)

    def test_add(self):
        self._test(self.calc.add, 3, 8, 11)
