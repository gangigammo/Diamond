
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

# ドライバーの操作のショートカット


# リンクをクリックする

def click_url(self: WebDriver, partial_url: str):
    elements = self.find_elements_by_xpath(
        "//a[contains(@href, '" + partial_url + "')]")
    if (len(elements) == 0):
        raise NoSuchElementException('リンク ' + partial_url + ' が見つかりません.')
    elements[0].click()


# フォームを送信する

def form_submit(self: WebDriver, form_id: str, input_dict: dict):
    forms = self.find_elements_by_xpath("//form[@id='" + form_id + "']")
    if (len(forms) == 0):
        raise NoSuchElementException('フォーム ' + form_id + ' が見つかりません.')
    elif (len(forms) > 1):
        raise SyntaxWarning('フォーム ' + form_id + ' が複数あります.')
    form = forms[0]
    for name, value in input_dict.items():
        elements = form.find_elements_by_name(name)
        if (len(elements) == 0):
            raise NoSuchElementException('入力欄 ' + name + ' が見つかりません.')
        elif (len(elements) > 1):
            raise SyntaxWarning('入力欄 ' + name + ' が複数あります.')
        elements[0].send_keys(value)
    form.submit()


# ページに文字列が存在するか

def exists(self: WebDriver, string: str):
    elements = self.find_elements_by_xpath("//*[text()='" + string + "']")
    return (len(elements) > 0)



# メソッドをWebDriverに追加


def __setattr(method):
    setattr(WebDriver, method.__name__, method)


__setattr(click_url)
__setattr(form_submit)
__setattr(exists)
