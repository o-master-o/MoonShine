import time

import pytest
from selenium.webdriver.common.by import By

from utils import ENTRY_POINT, chrome, wait_till_page_loaded


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{ENTRY_POINT}add_remove_elements/")
    wait_till_page_loaded(chrome)
    time.sleep(15)
    return chrome


def test_add_element(content):
    add_button = content.find_element(By.XPATH, '//button[contains(text(), "Add Element")]')
    add_button.click()  # Click the 'Add Element' button to add a new element

    # Verify that the new element has been added
    added_elements = content.find_elements(By.CLASS_NAME, 'added-manually')
    assert len(added_elements) > 0, "No new elements were added"


def test_delete_element(content):
    # Ensure there's at least one element to delete
    add_button = content.find_element(By.XPATH, '//button[contains(text(), "Add Element")]')
    add_button.click()

    # Get the count of elements before deletion
    initial_count = len(content.find_elements(By.CLASS_NAME, 'added-manually'))

    # Click the 'Delete' button on the first added element
    delete_button = content.find_element(By.CLASS_NAME, 'added-manually')
    delete_button.click()

    # Get the count of elements after deletion
    final_count = len(content.find_elements(By.CLASS_NAME, 'added-manually'))

    # Verify that one element has been removed
    assert final_count == initial_count - 1, "Element was not deleted"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert "http://elementalselenium.com/" == footer_link.get_attribute("href"), "Footer link URL incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text does not match expected"
