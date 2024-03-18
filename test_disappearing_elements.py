import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils import HTTPS_ENTRY_LINK, chrome, wait_till_page_loaded
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{HTTPS_ENTRY_LINK}disappearing_elements")
    wait_till_page_loaded(chrome)
    return chrome


def test_links_presence(content):
    expected_links_text = ['Home', 'About', 'Contact Us', 'Portfolio', 'Gallery']
    links = content.find_elements(By.CSS_SELECTOR, 'div#content ul li a')
    visible_links_texts = [link.text for link in links]

    for expected_text in expected_links_text:
        assert expected_text in visible_links_texts, f"{expected_text} link is not visible"


def test_links_functionality(content):
    expected_links_text = [link.text for link in content.find_elements(By.CSS_SELECTOR, '#content ul li a')]
    for link_text in expected_links_text:
        link = WebDriverWait(content, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
        href = link.get_attribute('href')
        link.click()
        WebDriverWait(content, 10).until(EC.url_to_be(href))
        content.back()
        WebDriverWait(content, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, expected_links_text[0])))


def test_header_content(content):
    header = content.find_element(By.CSS_SELECTOR, '#content h3')
    assert header.text == "Disappearing Elements", "Header text is not as expected"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert footer_link.get_attribute('href') == "http://elementalselenium.com/", "Footer link URL is incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text is not correct"


def test_github_ribbon_content(content):
    github_ribbon = content.find_element(By.XPATH, '//a[@href="https://github.com/tourdedave/the-internet"]')
    assert github_ribbon is not None, "GitHub ribbon is not found"
