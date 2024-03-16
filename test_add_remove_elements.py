import time

import pytest
from selenium.webdriver.common.by import By

from utils import HTTPS_ENTRY_LINK, chrome, wait_till_page_loaded


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{HTTPS_ENTRY_LINK}add_remove_elements/")
    wait_till_page_loaded(chrome)
    time.sleep(15)
    return chrome


def test_verify_that_the_exact_amount_of_the_new_elements_has_been_added(content):
    add_button = content.find_element(By.XPATH, '//button[contains(text(), "Add Element")]')

    add_button.click()
    added_elements = content.find_elements(By.CLASS_NAME, 'added-manually')
    assert len(added_elements) == 1, "No new elements were added"

    add_button.click()
    add_button.click()
    added_elements = content.find_elements(By.CLASS_NAME, 'added-manually')
    assert len(added_elements) == 3, "No new elements were added"


def test_verify_that_the_exact_amount_of_the_elements_has_been_deleted(content):
    add_button = content.find_element(By.XPATH, '//button[contains(text(), "Add Element")]')
    add_button.click()
    add_button.click()
    add_button.click()
    initial_count = len(content.find_elements(By.CLASS_NAME, 'added-manually'))

    delete_buttons = content.find_elements(By.CLASS_NAME, 'added-manually')
    delete_buttons[0].click()
    delete_buttons[1].click()
    final_count = len(content.find_elements(By.CLASS_NAME, 'added-manually'))

    assert final_count == initial_count - 2, "Element was not deleted"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert "http://elementalselenium.com/" == footer_link.get_attribute("href"), "Footer link URL incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text does not match expected"
