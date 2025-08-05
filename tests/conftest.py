import os
import sys
# Append path to PYTHON_PATH to run test from CMD directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_utils.capabilities import create_driver, quit_driver
from datetime import datetime
import pytest
import shutil
import base64

MEDIA_FOLDERS = {
    "screenshots": os.path.join(os.getcwd(), "screenshots"),
    "videos": os.path.join(os.getcwd(), "videos"),
    "html_report": os.path.join(os.getcwd(), "html_report"),
}

@pytest.fixture
def driver():
    app_package = "com.mentortools.academy"
    # TODO: Wonder how many parameters we will have, based on that we should decide if we want to set those up as ENV variables or store them in configuration file
    # Clear app data before each test to ensure clean test separation
    os.system(f"adb shell pm clear {app_package}")

    # Grant notifications permissions, so we are not bothered during testing with prompts
    os.system(f"adb shell pm grant {app_package} android.permission.POST_NOTIFICATIONS")

    driver = create_driver()
    yield driver

    quit_driver(driver)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    # Cleanup & setup before running tests
    for folder in MEDIA_FOLDERS.values():
        if os.path.exists(folder):
            print(f"Cleaning folder: {folder}")
            shutil.rmtree(folder)
        os.makedirs(folder)

@pytest.fixture(scope="function", autouse=True)
def capture_media(request, driver):
    # Start recording before every test
    driver.start_recording_screen()
    yield

    # Stop recording after tests are done with execution
    video_raw = driver.stop_recording_screen()

    # Get test outcome
    rep_call = getattr(request.node, "rep_call", None)
    failed = rep_call.failed if rep_call else False

    # Save recording and screenshot only if test failed
    if failed:
        test_name = request.node.name
        print(f"\nTest failed: '{test_name}' saving media...")

        # Save screenshot
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(MEDIA_FOLDERS["screenshots"], f"{test_name}_{timestamp}.png")

        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved: {screenshot_path}")

        # Save recording
        video_path = os.path.join(MEDIA_FOLDERS["videos"], f"{test_name}_{timestamp}.mp4")
        with open(video_path, "wb") as f:
            f.write(base64.b64decode(video_raw))
        print(f"\nVideo saved: {video_path}")

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def pytest_addoption(parser):
    parser.addoption("--email", action="store", default=None, help="Email for login")
    parser.addoption("--password", action="store", default=None, help="Password for login")

def pytest_generate_tests(metafunc):
    is_login_matrix_test = metafunc.definition.get_closest_marker("login_cred_matrix")
    cli_email = metafunc.config.getoption("email")
    cli_password = metafunc.config.getoption("password")

    if is_login_matrix_test:
        # If we want to test all the login combinations, create all combinations for parametrization
        default_cases = [
            ("wrong@email.com", "WrongPassword123!", True) # Wrong email, wrong password, expect failure message
        ]
        cases = default_cases

        if cli_email and cli_password:
            cases.append((cli_email, cli_password, False))  # Correct email, correct password, expect no failure message
            cases.append((cli_email, "WrongPassword123!", True)) # Correct email, wrong password, expect failure message
            cases.append(("wrong@email.com", cli_password, True)) # Wrong email, correct password, expect failure message

        metafunc.parametrize("email,password,expect_error", cases)
    elif cli_email and cli_password:
        # If we want to only pass login parameters
        metafunc.parametrize("email,password", [(cli_email, cli_password)])
