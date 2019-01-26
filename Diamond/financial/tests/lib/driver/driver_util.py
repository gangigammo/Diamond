
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ドライバーの操作のショートカット


# クリック可能になるまで待つ
def __wait_xpath(self: WebDriver, xpath: str):
    return WebDriverWait(self, 1).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath))
    )


def __wait_name(self: WebDriver, name: str):
    return WebDriverWait(self, 1).until(
        EC.element_to_be_clickable(
            (By.NAME, name))
    )


# リンクをクリックする
def click_url(self: WebDriver, partial_url: str):
    elements = self.find_elements_by_xpath(
        "//a[contains(@href, '" + partial_url + "')]")
    if (len(elements) == 0):
        raise NoSuchElementException('リンク ' + partial_url + ' が見つかりません.')
    elements[0].click()


# フォームを見つける
def __findForm(self: WebDriver, form_id: str):
    forms = self.find_elements_by_xpath("//form[@id='" + form_id + "']")
    if (len(forms) == 0):
        raise NoSuchElementException('フォーム ' + form_id + ' が見つかりません.')
    elif (len(forms) > 1):
        raise SyntaxWarning('フォーム ' + form_id + ' が複数あります.')
    form = forms[0]
    return form


# フォームに入力する(送信はしない)
def form_input(self: WebDriver, form_id: str, input_dict: dict):
    form = self.__findForm(form_id)
    for name, value in input_dict.items():
        xpath = "//form[@id='%s']//input[@name='%s']" % (form_id, name)
        element = self.__wait_xpath(xpath)
        element.send_keys(value)
    return form


# フォームを送信する
def form_submit(self: WebDriver, form_id: str, input_dict: dict):
    form = self.form_input(form_id, input_dict)
    form.submit()


# フォームのボタンをクリックする
def form_click(self: WebDriver, form_id: str, name: str):
    xpath = "//form[@id='%s']//input[@name='%s']" % (form_id, name)
    elements = self.find_elements_by_xpath(xpath)
    if (len(elements) == 0):
        raise NoSuchElementException(
            "フォーム %s のボタン %s が見つかりません" % (form_id, name))
    elements[0].click()

# ページに文字列が存在するか


def exists(self: WebDriver, string: str):
    elements = self.find_elements_by_xpath("//*[text()='" + string + "']")
    return (len(elements) > 0)


# 選択フォームに選択肢が存在するかをチェック
def checkSelection(self: WebDriver, form_id: str, select_name: str, value: str):
    """
    選択フォームに選択肢が存在するかをチェック.
    存在しなければNoSuchElementExceptionを返す

    Parameters
    ----------
    form_id : str
        対象フォームのid
    select_name : str
        フォーム内の<select>のname
    value : str
        選択肢<option>のvalue
    """
    try:
        option = self.find_element_by_xpath(
            "//form[@id='%s']//select[@name='%s']/option[@value='%s']" % (form_id, select_name, value))
    except NoSuchElementException as ex:
        pass
        raise NoSuchElementException(
            "フォーム %s の %s 欄の選択肢 %s が存在しません." % (form_id, select_name, value))
    return True


# ボタンを押す
def pushButton(self: WebDriver, id: str):
    self.__wait_xpath(
        "//input[@type='button' and @id='%s']" % id).click()


# 選択メニューを押す
def pushSelect(self: WebDriver, form_id: str, name: str, value: str):
    selectXpath = "//form[@id='%s']//select[@name='%s']" % (form_id, name)
    element = self.find_element(By.XPATH, selectXpath)
    selectElement = Select(element)
    selectElement.select_by_value(value)


# 選択メニューを押す(表示テキストで選択)
def pushSelectByText(self: WebDriver, form_id: str, name: str, text: str):
    selectXpath = "//form[@id='%s']//select[@name='%s']" % (form_id, name)
    element = self.find_element(By.XPATH, selectXpath)
    selectElement = Select(element)
    selectElement.select_by_visible_text(text)


# メソッドをWebDriverに追加


def __setattr(method):
    setattr(WebDriver, method.__name__, method)


__setattr(__wait_name)
__setattr(__wait_xpath)
__setattr(click_url)
__setattr(__findForm)
__setattr(form_input)
__setattr(form_submit)
__setattr(form_click)
__setattr(checkSelection)
__setattr(exists)
__setattr(pushButton)
__setattr(pushSelect)
__setattr(pushSelectByText)
