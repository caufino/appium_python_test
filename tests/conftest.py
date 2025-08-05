import sys
import os
# Append path to PYTHON_PATH to run test from CMD directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_utils.capabilities import create_driver, quit_driver
import pytest


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
            cases.append((cli_email, "WrongPassword123!", True)) # Correct email, wrong password, expect failure message
            cases.append(("wrong@email.com", cli_password, True)) # Wrong email, correct password, expect failure message
            cases.append((cli_email, cli_password, False)) # Correct email, correct password, expect no failure message

        metafunc.parametrize("email,password,expect_error", cases)
    elif cli_email and cli_password:
        # If we want to only pass login parameters
        metafunc.parametrize("email,password", [(cli_email, cli_password)])
