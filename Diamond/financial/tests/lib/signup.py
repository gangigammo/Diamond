from .driver import driver_util

# サインアップする


def signup(driver):
    driver.click_url("signup")
    input_dict = {"name": "Taro", "password": "yahoo"}
    driver.form_input("signupForm", input_dict)
