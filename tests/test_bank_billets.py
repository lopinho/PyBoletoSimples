import sys
sys.path.append('../')

from unittest import TestCase

from boletosimples.managers import BankBillet


class BankBilletTestCase(TestCase):
    def setUp(self):
        self.object = BankBillet(token='123', password='456', user_agent='MyApp (myapp@example.com)')
