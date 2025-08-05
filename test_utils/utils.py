from selenium.common.exceptions import NoSuchElementException
from test_utils.logger import logger

def are_elements_displayed(driver, selectors):
    # Iterate over elements and check, if they are properly displayed
    for selector in selectors:
        try:
            el = driver.find_element(selector[0], selector[1])
            if not el.is_displayed():
                logger.error(f"Element with selector '{selector[1]}' was not displayed!")
                return False
        except NoSuchElementException:
            logger.error(f"Element with selector '{selector[1]}' not found!")
            return False
    return True
