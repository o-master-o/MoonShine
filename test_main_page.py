import pytest
import requests
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from controller import ChromeDriver
from data import expected_sections_data, authorization_required_resources

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
    return (content.find_element(By.XPATH, sections_path)
            .find_elements(By.TAG_NAME, 'li'))


@pytest.fixture(scope='module')
def sections_hrefs(sections):
    return [item.find_element(By.TAG_NAME, 'a').get_attribute("href") for item in sections]


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
    sections_data = [(element.text, element.find_element(By.TAG_NAME, 'a').get_attribute("href")) for element in sections]
    assert expected_sections_data == sections_data


def test_authorization_free_links_are_accessible(sections_hrefs):
    authorization_free_hrefs = list(filter(lambda x: x not in authorization_required_resources, sections_hrefs))
    for href in authorization_free_hrefs:
        response = requests.head(href, allow_redirects=True)
        assert response.status_code == 200


def test_authorization_required_links_are_not_accessible(sections_hrefs):
    authorization_required_hrefs = list(filter(lambda x: x in authorization_required_resources, sections_hrefs))
    for href in authorization_required_hrefs:
        response = requests.head(href, allow_redirects=True)
        assert response.status_code == 401


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
