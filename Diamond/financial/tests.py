from django.test import TestCase
from selenium import webdriver
from enum import Enum
import os
import pathlib

# Create your tests here.``

# ブラウザの列挙
class Browser(Enum):
		Chrome = 1
# ブラウザのドライバーを新しく取得する
class Drivers():
	# ドライバーがあるパスを指定
	dir = pathlib.Path('../Diamond/browsers')
	# ドライバー本体のファイル名を指定
	bin = {Browser.Chrome: 'chromedriver'}


class MyTests(TestCase):
	def test_sample(self):
		driverPath = pathlib.Path('../Diamond/tests/chromedriver.exe').resolve()
		print('driver:	', driverPath)
		print('exists?:	', os.path.exists(driverPath))
		browser = webdriver.Chrome(str(driverPath))
		browser.get('http://seleniumhq.org/')
