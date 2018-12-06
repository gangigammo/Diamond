from django.test import TestCase
from selenium import webdriver
import os
import pathlib

# Create your tests here.``


class MyTests(TestCase):
	def test_sample(self):
		driverPath = pathlib.Path('../Diamond/tests/chromedriver.exe').resolve()
		print('driver:	', driverPath)
		print('exists?:	', os.path.exists(driverPath))
		browser = webdriver.Chrome(str(driverPath))
		browser.get('http://seleniumhq.org/')
