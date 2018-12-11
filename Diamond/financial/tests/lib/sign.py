
from selenium.webdriver.remote.webdriver import WebDriver

from .driver import driver_util
from .driver import DriverConfig

# サインアップする


def signup(driver: WebDriver, name: str, password: str):
    driver.get(DriverConfig.default_url)
    driver.click_url("signup")
    input_dict = {"name": name, "password": password}
    driver.form_submit("signupForm", input_dict)


# サインインする

def signin(driver: WebDriver, name: str, password: str):
    driver.get(DriverConfig.default_url)
    driver.click_url("signin")
    input_dict = {"name": name, "password": password}
    driver.form_submit("signinForm", input_dict)


# サインアウトする

def signout(driver: WebDriver, name: str, password: str):
    driver.get(DriverConfig.default_url)
    driver.click_url("signout")
