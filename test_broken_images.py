import time

import pytest
import requests
from selenium.webdriver.common.by import By

from utils import HTTPS_ENTRY_LINK, chrome, wait_till_page_loaded


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{HTTPS_ENTRY_LINK}broken_images")
    wait_till_page_loaded(chrome)
    time.sleep(10)
    return chrome


def test_verify_images_are_not_broken(content):
    examples = content.find_element(By.XPATH, '/html/body/div[2]/div/div')
    images = examples.find_elements(By.TAG_NAME, 'img')
    broken_images = []
    for img in images:
        response = requests.get(img.get_attribute('src'), stream=True)
        if response.status_code != 200:
            broken_images.append(img.get_attribute('outerHTML'))
    assert 0 == len(broken_images), f"Broken images are present in page: {broken_images}"


def test_header_content(content):
    header = content.find_element(By.CSS_SELECTOR, 'h3')
    assert header.text == "Broken Images", "Header text is not as expected"


def test_github_ribbon_content(content):
    github_ribbon = content.find_element(By.XPATH, '//a[@href="https://github.com/tourdedave/the-internet"]')
    assert github_ribbon is not None, "GitHub ribbon is not found"


def test_footer_content(content):
    footer = content.find_element(By.CSS_SELECTOR, '#page-footer div')
    assert "Powered by Elemental Selenium" in footer.text, "Footer text is not as expected"
