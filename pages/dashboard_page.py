from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_utils.utils import are_elements_displayed
import pytest


class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        # Set the default wait for element
        # TODO: Only for demo purposes, this timeout won't be static in actual implementation if we decide to go with Python
        self.wait = WebDriverWait(driver, 5)
        # TODO: Parametrize locators in separate locator files
        self.selectors = [
            (AppiumBy.ACCESSIBILITY_ID, 'My courses'),
            (AppiumBy.ACCESSIBILITY_ID, 'Paid'),
            (AppiumBy.ACCESSIBILITY_ID, 'Free'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("You haven’t started any courses yet.")')
        ]

    def is_dashboard_loaded(self):

        try:
            self.wait.until(EC.presence_of_element_located(self.selectors[0]))

            if not are_elements_displayed(self.driver, self.selectors):
                pytest.fail("User dashboard was not loaded! Login failed!")
        except TimeoutException:
            pytest.fail("User dashboard was not loaded (or failed to load in time)! Login failed!")
