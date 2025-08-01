from pages.login_page import LoginPage
import pytest


@pytest.mark.login_cred_matrix
def test_login(driver, email, password, expect_error):
    # Initialize LoginPage POM
    login_page = LoginPage(driver)

    # Type in Email, Password & proceed with Login
    login_page.type_email(email)
    login_page.type_password(password)
    login_page.press_login_button()

    # Check for Login error if expected
    login_page.is_login_error_displayed(expect_error)

    if not expect_error:
        # If we successfully log in, check if we landed on dashboard correctly
        login_page.is_dashboard_loaded()
