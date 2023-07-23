import time
import pytest
from selenium.webdriver.common.by import By
from BaseClass_flask import BaseClass


@pytest.mark.usefixtures("setup")
class Test_class(BaseClass):
    def test_signup(self, setup):
        global driver
        log = self.log_conf()
        driver = setup
        driver.get("http://35.84.189.43:5001/")
        sign_up = driver.find_element(By.CSS_SELECTOR, ".register_link")
        sign_up.click()
        name = 'sivan'
        user_name = driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Enter name"]').send_keys(name)
        password = driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Enter password"]').send_keys('1234')
        sign_up_button = driver.find_element(
            By.CSS_SELECTOR, 'input[value="sign-up"]').click()
        hello_user = driver.find_element(By.CSS_SELECTOR, '.hello_user').text
        time.sleep(5)
        try:
            assert hello_user == f"Hello {name}"
        except AssertionError as msg:
            log.error(msg)
            raise AssertionError(msg)
        else:
            log.info("Test Passed successfully")
