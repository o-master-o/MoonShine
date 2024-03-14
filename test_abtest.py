import pytest
from selenium.webdriver.common.by import By

from utils import ENTRY_POINT, chrome, wait_till_page_loaded


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{ENTRY_POINT}/abtest")
    wait_till_page_loaded(chrome)
    return chrome


def test_page_title(content):
    assert "The Internet" == content.title, "Page title does not match expected"


def test_scripts_and_stylesheets(content):
    expected_sources = [
        "/js/vendor/298279967.js",
        "/js/vendor/jquery-1.11.3.min.js",
        "/js/vendor/jquery-ui-1.11.4/jquery-ui.js",
        "/js/foundation/foundation.js",
        "/js/foundation/foundation.alerts.js",
        "/css/app.css",
        "/css/font-awesome.css"
    ]
    for source in expected_sources:
        assert content.find_elements(By.XPATH, f"//script[@src='{source}'] | //link[@href='{source}']"), f"Resource {source} not loaded"


def test_image_attributes(content):
    image = content.find_element(By.TAG_NAME, 'img')
    assert "https://github.com/tourdedave/the-internet" == image.get_attribute("href"), "Image link incorrect"
    assert "/img/forkme_right_green_007200.png" == image.get_attribute("src"), "Image source incorrect"
    assert "Fork me on GitHub" == image.get_attribute("alt"), "Image alt text incorrect"


def test_ab_test_variation_text(content):
    h3 = content.find_element(By.TAG_NAME, 'h3')
    p = content.find_element(By.TAG_NAME, 'p')
    assert "A/B Test Variation 1" == h3.text, "Heading text does not match expected"
    expected_paragraph_text = "Also known as split testing. This is a way in which businesses are able to simultaneously test and learn different versions of a page to see which text and/or functionality works best towards a desired outcome (e.g. a user action such as a click-through)."
    assert expected_paragraph_text == p.text, "Paragraph text does not match expected"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert "http://elementalselenium.com/" == footer_link.get_attribute("href"), "Footer link URL incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text does not match expected"
