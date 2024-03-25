import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from controller import ChromeDriver
from utils import ENTRY_LINK, chrome, wait_till_page_loaded, HTTPS_ENTRY_LINK

username = "admin"
password = "admin"
url_with_credentials = f"https://{username}:{password}@{ENTRY_LINK}basic_auth"


@pytest.fixture()
def content(chrome):
    chrome.get(url_with_credentials)
    wait_till_page_loaded(chrome)
    return chrome


def test_auth_header(content):
    auth_header = content.find_element(By.CSS_SELECTOR, '#content .example h3')
    assert auth_header.text == "Basic Auth", "The header text is not correct"


def test_auth_success_message(content):
    success_message = content.find_element(By.CSS_SELECTOR, '#content .example p')
    assert success_message.text == "Congratulations! You must have the proper credentials.", "The success message text is not correct"


def test_github_link(content):
    github_link = content.find_element(By.XPATH, '//a[@href="https://github.com/tourdedave/the-internet"]')
    assert github_link.get_attribute('href') == "https://github.com/tourdedave/the-internet", "The GitHub link is not correct"


def test_footer_link(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert footer_link.get_attribute('href') == "http://elementalselenium.com/", "The footer link URL is not correct"


url_without_credentials = f"{HTTPS_ENTRY_LINK}basic_auth"


def test_pege_is_inaccessible_without_credentials():
    driver = ChromeDriver()
    try:
        with pytest.raises(TimeoutException):
            driver.get(url_without_credentials)
            WebDriverWait(driver, 5).until(EC.alert_is_present())
    finally:
        driver.quit()
