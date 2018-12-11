
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

# ドライバーの操作のショートカット


# リンクをクリックする

def click_url(self, partial_url: str):
    elements = self.find_elements_by_xpath(
        "//a[contains(@href, '" + partial_url + "')]")
    if (len(elements) == 0):
        raise NoSuchElementException('リンク ' + partial_url + ' が見つかりません.')
    elements[0].click()


# メソッドをWebDriverに追加
def __setattr(method):
    setattr(WebDriver, method.__name__, method)


__setattr(click_url)
