from .driver import Driver

# サインアップする


def signup(driver: Driver):
    driver.click_url("signup")
