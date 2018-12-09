from django.test import TestCase
from .lib import ui
# Create your tests here.``


class MyRootTests(TestCase):
    def test_sample(self):
        ui.test_sample()
