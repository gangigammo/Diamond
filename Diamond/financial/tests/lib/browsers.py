
from selenium import webdriver


# ブラウザの定義


class Browser():
    def __init__(self, name, filename, factory_method, download_url):
        self.name = name
        self.filename = filename
        self.factory_method = factory_method
        self.download_url = download_url


# ブラウザの列挙
# テストしたいブラウザはここに追加
class Browsers():
    Chrome = Browser('Chrome', 'chromedriver', webdriver.Chrome,
                     'https://sites.google.com/a/chromium.org/chromedriver/downloads')

    Edge = Browser('Edge', 'MicrosoftWebDriver', webdriver.Edge,
                   'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')

    Firefox = Browser('Firefox', 'geckodriver', webdriver.Firefox,
                      'https://github.com/mozilla/geckodriver/releases')
