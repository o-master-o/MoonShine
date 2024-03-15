import time

import pytest
from selenium.webdriver.common.by import By

from utils import ENTRY_LINK, chrome, wait_till_page_loaded

username = "admin"
password = "admin"
url_with_credentials = f"https://{username}:{password}@{ENTRY_LINK}basic_auth"


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(url_with_credentials)
    wait_till_page_loaded(chrome)
    time.sleep(5)
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
