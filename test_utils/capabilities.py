from appium import webdriver
from appium.options.android import UiAutomator2Options
import os


def create_driver():
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("platformVersion", "16")
    options.set_capability("deviceName", "emulator-5554")
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("appPackage", "com.mentortools.academy")  # Refers to an already installed Mentortools app
    options.set_capability("appActivity", "com.mentortools.academy.MainActivity")
    options.set_capability("noReset", True)
    options.set_capability("fullReset", False)
    options.set_capability("autoGrantPermissions", True)

    # Connect to an application
    return webdriver.Remote("http://localhost:4723", options=options)

def quit_driver(driver):
    # Also close app by force-stopping it
    os.system("adb shell am force-stop com.mentortools.academy")

    driver.quit()
    return
