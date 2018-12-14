
from selenium import webdriver
from .browser import Browser

# ブラウザの列挙
# テストしたいブラウザはここに追加

Chrome = Browser('Chrome', 'chromedriver', webdriver.Chrome,
                 'https://sites.google.com/a/chromium.org/chromedriver/downloads')

Edge = Browser('Edge', 'MicrosoftWebDriver', webdriver.Edge,
               'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')

Firefox = Browser('Firefox', 'geckodriver', webdriver.Firefox,
                  'https://github.com/mozilla/geckodriver/releases')
