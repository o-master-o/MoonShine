import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from controller import ChromeDriver
from data import expected_sections_list

ENTRY_POINT = 'https://the-internet.herokuapp.com/'


@pytest.fixture(scope='module')
def chrome():
    driver = ChromeDriver()
    try:
        yield driver
    finally:
        driver.close()


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(ENTRY_POINT)
    return chrome


def test_check_entry_page_content(content):
    welcome_header_path = '/html/body/div[2]/div/h1'
    sub_header_path = '/html/body/div[2]/div/h2'
    sections_path = '/html/body/div[2]/div/ul'
    header1 = WebDriverWait(content, timeout=10).until(EC.visibility_of_element_located((By.XPATH, welcome_header_path)))
    header2 = content.find_element(By.XPATH, sub_header_path)
    sections_list = content.find_element(By.XPATH, sections_path)
    sections = sections_list.find_elements(By.TAG_NAME, 'li')
    assert "Welcome to the-internet" == header1.text
    assert "Available Examples" == header2.text
    assert expected_sections_list == [element.text for element in sections]
#

