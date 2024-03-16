import time

import pytest
import requests
from selenium.webdriver.common.by import By

from utils import HTTPS_ENTRY_LINK, chrome, wait_till_page_loaded


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{HTTPS_ENTRY_LINK}checkboxes")
    wait_till_page_loaded(chrome)
    time.sleep(10)
    return chrome


def test_checkboxes_presence(content):
    checkboxes = content.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")
    assert len(checkboxes) == 2, "There should be 2 checkboxes"


def test_toggle_checkboxes(content):
    checkboxes = content.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")
    for index, checkbox in enumerate(checkboxes, start=1):
        if not checkbox.is_selected():
            checkbox.click()
        assert checkbox.is_selected(), f"Checkbox {index} should be selected after clicking"

        checkbox.click()
        assert not checkbox.is_selected(), f"Checkbox {index} should be deselected after clicking again"


def test_header_content(content):
    header = content.find_element(By.CSS_SELECTOR, "#content .example h3")
    assert header.text == "Checkboxes", "The header text is not correct"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert footer_link.get_attribute('href') == "http://elementalselenium.com/", "Footer link URL is incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text is not correct"


def test_github_ribbon_content(content):
    github_ribbon = content.find_element(By.XPATH, '//a[@href="https://github.com/tourdedave/the-internet"]')
    assert github_ribbon is not None, "GitHub ribbon is not found"
