import time

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import HTTPS_ENTRY_LINK, chrome, wait_till_page_loaded


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{HTTPS_ENTRY_LINK}context_menu")
    wait_till_page_loaded(chrome)
    time.sleep(10)
    return chrome


def test_context_menu(content):
    context_menu_box = content.find_element(By.ID, 'hot-spot')
    actions = ActionChains(content)
    actions.context_click(context_menu_box).perform()
    WebDriverWait(content, 10).until(EC.alert_is_present())
    alert_popup = content.switch_to.alert

    assert alert_popup.text == "You selected a context menu", "Alert text is not as expected"
    alert_popup.accept()


def test_header_content(content):
    header = content.find_element(By.CSS_SELECTOR, '#content h3')
    assert header.text == "Context Menu", "Header text is not as expected"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert footer_link.get_attribute('href') == "http://elementalselenium.com/", "Footer link URL is incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text is not correct"


def test_github_ribbon_content(content):
    github_ribbon = content.find_element(By.XPATH, '//a[@href="https://github.com/tourdedave/the-internet"]')
    assert github_ribbon is not None, "GitHub ribbon is not found"
