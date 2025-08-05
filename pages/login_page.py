from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_utils.logger import logger


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Set the default wait for element
        # TODO: Only for demo purposes, this timeout won't be static in actual implementation if we decide to go with Python
        self.wait = WebDriverWait(driver, 5)

    def type_email(self, email):
        logger.debug(f"Waiting for 'Email field' to be displayed")
        email_field = self.wait.until(
            EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Your email")')))
        email_field.send_keys(email)

    def type_password(self, password):
        password_field = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                  'new UiSelector().text("Your password")')
        password_field.send_keys(password)

    def press_login_button(self):
        login_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")')
        login_button.click()

    def is_login_error_displayed(self, is_expected=False):
        try:
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login not successful")')))
            if is_expected:
                return True
            else:
                raise AssertionError("Login error popup was displayed when it should not be! Login failed!")
        except TimeoutException:
            if is_expected:
                raise
            else:
                return False
