import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from controller import ChromeDriver
from data import expected_sections_data

ENTRY_POINT = 'https://the-internet.herokuapp.com/'


@pytest.fixture(scope='module')
def chrome():
    driver = ChromeDriver()
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(ENTRY_POINT)
    WebDriverWait(chrome, timeout=10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    return chrome


@pytest.fixture(scope='module')
def sections(content):
    sections_path = '/html/body/div[2]/div/ul'
    return content.find_element(By.XPATH, sections_path)


def test_check_entry_page_headers_consistence(content):
    welcome_header_path = '/html/body/div[2]/div/h1'
    sub_header_path = '/html/body/div[2]/div/h2'
    header1 = content.find_element(By.XPATH, welcome_header_path)
    header2 = content.find_element(By.XPATH, sub_header_path)
    assert "Welcome to the-internet" == header1.text
    assert "Available Examples" == header2.text


def test_check_sections_links(sections):
    items = sections.find_elements(By.TAG_NAME, 'li')
    sections_data = [(element.text, element.find_element(By.TAG_NAME, 'a').get_attribute("href")) for element in items]
    assert expected_sections_data == sections_data
