import time

import pytest
import requests
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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


def test_page_title(content):
    assert "The Internet" == content.title


def test_check_entry_page_header_consistence(content):
    welcome_header_path = '/html/body/div[2]/div/h1'
    header1 = content.find_element(By.XPATH, welcome_header_path)
    assert "Welcome to the-internet" == header1.text
    assert "heading" == header1.get_attribute("class")


def test_check_entry_page_sub_header_consistence(content):
    sub_header_path = '/html/body/div[2]/div/h2'
    header2 = content.find_element(By.XPATH, sub_header_path)
    assert "Available Examples" == header2.text


def test_check_sections_links_data(sections):
    items = sections.find_elements(By.TAG_NAME, 'li')
    sections_data = [(element.text, element.find_element(By.TAG_NAME, 'a').get_attribute("href")) for element in items]
    assert expected_sections_data == sections_data



# def test_links_are_accessible(sections):
#     items = sections.find_elements(By.TAG_NAME, 'li')
#     for item in items:
#         link = item.find_element(By.TAG_NAME, 'a')
#         href = link.get_attribute("href")
#         print(href)
#         response = requests.head(href, allow_redirects=True)
#         print(response.status_code)
#         print(response.content)
#         # assert response.status_code == 200


def test_image_source_and_alt(content):
    image = content.find_element(By.TAG_NAME, 'img')
    assert image.get_attribute("src").endswith("/img/forkme_right_green_007200.png")
    assert "Fork me on GitHub" == image.get_attribute("alt")


def test_image_position_top_right(content):
    image = content.find_element(By.TAG_NAME, 'img')
    location = image.location
    size = image.size
    window_size = content.get_window_size()

    margin = 15
    image_right_edge = location['x'] + size['width']
    assert window_size['width'] - image_right_edge <= margin, "Image is not at the right edge"

    assert location['y'] <= margin, "Image is not at the top"


def test_footer_content_and_link(content):
    footer_text_div = content.find_element(By.XPATH, '/html/body/div[3]/div/div')
    assert "Powered by Elemental Selenium" in footer_text_div.text
    footer_link = footer_text_div.find_element(By.TAG_NAME, 'a')
    assert footer_link.get_attribute("href") == "http://elementalselenium.com/"
