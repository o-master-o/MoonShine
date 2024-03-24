import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from utils import HTTPS_ENTRY_LINK, chrome, wait_till_page_loaded


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{HTTPS_ENTRY_LINK}drag_and_drop")
    wait_till_page_loaded(chrome)
    return chrome


def test_when_drag_col_a_to_col_b_columns_should_swap(content):
    col_a = content.find_element(By.ID, 'column-a')
    col_b = content.find_element(By.ID, 'column-b')

    init_a_text = col_a.find_element(By.TAG_NAME, 'header').text
    init_b_text = col_b.find_element(By.TAG_NAME, 'header').text

    actions = ActionChains(content)
    actions.drag_and_drop(col_a, col_b).perform()

    new_a_text = col_a.find_element(By.TAG_NAME, 'header').text
    new_b_text = col_b.find_element(By.TAG_NAME, 'header').text

    assert new_a_text == init_b_text, "Column A text did not swap correctly"
    assert new_b_text == init_a_text, "Column B text did not swap correctly"


def test_header_content(content):
    header = content.find_element(By.CSS_SELECTOR, '#content h3')
    assert header.text == "Drag and Drop", "Header text is not as expected"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert footer_link.get_attribute('href') == "http://elementalselenium.com/", "Footer link URL is incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text is not correct"


def test_github_ribbon_content(content):
    github_ribbon = content.find_element(By.XPATH, '//a[@href="https://github.com/tourdedave/the-internet"]')
    assert github_ribbon is not None, "GitHub ribbon is not found"
