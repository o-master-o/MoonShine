import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils import HTTPS_ENTRY_LINK, chrome
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='module')
def content(chrome):
    chrome.get(f"{HTTPS_ENTRY_LINK}dropdown")
    WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.ID, "dropdown")))
    return chrome


@pytest.fixture(scope='module')
def dropdown_menu_options(content):
    dropdown_menu = content.find_element(By.CSS_SELECTOR, 'select#dropdown')
    return dropdown_menu.find_elements(By.TAG_NAME, 'option')


def test_validate_dropdown_menu_options_text(dropdown_menu_options):
    expected_options_text = ["Please select an option", "Option 1", "Option 2"]
    assert expected_options_text == [opt.text for opt in dropdown_menu_options]


def test_validate_dropdown_menu_options_values(dropdown_menu_options):
    expected_options_values = ['', '1', '2']
    assert expected_options_values == [opt.get_attribute('value') for opt in dropdown_menu_options]


def test_validate_dropdown_menu_options_initial_selected_state(dropdown_menu_options):
    expected_selected_options = ['true', None, None]
    assert expected_selected_options == [opt.get_attribute('selected') for opt in dropdown_menu_options]


def test_validate_dropdown_menu_selectable_options_are_selected_state_when_clicked(dropdown_menu_options):
    for opt in dropdown_menu_options[1:]:
        opt.click()
        is_selected = opt.get_attribute("selected")
        assert is_selected, f"Option {opt.text} should be selected but is not."
        for other_opt in dropdown_menu_options:
            if other_opt != opt:
                assert other_opt.get_attribute("selected") is None, f"Option {other_opt.text} is incorrectly selected."


def test_when_dropdown_menu_option_1_is_clicked_initial_option_becomes_unselectable(dropdown_menu_options):
    option_1 = dropdown_menu_options[1]
    initial_option = dropdown_menu_options[0]
    assert initial_option.get_attribute("selected")
    assert not option_1.get_attribute("selected")

    option_1.click()
    assert not initial_option.get_attribute("selected")
    assert option_1.get_attribute("selected")

    initial_option.click()
    assert not initial_option.get_attribute("selected")
    assert option_1.get_attribute("selected")


def test_header_content(content):
    header = content.find_element(By.CSS_SELECTOR, '#content h3')
    assert header.text == "Dropdown List", "Header text is not as expected"


def test_footer_link_and_text(content):
    footer_link = content.find_element(By.XPATH, '//div[@id="page-footer"]//a')
    assert footer_link.get_attribute('href') == "http://elementalselenium.com/", "Footer link URL is incorrect"
    assert "Powered by Elemental Selenium" in footer_link.find_element(By.XPATH, '..').text, "Footer text is not correct"


def test_github_ribbon_content(content):
    github_ribbon = content.find_element(By.XPATH, '//a[@href="https://github.com/tourdedave/the-internet"]')
    assert github_ribbon is not None, "GitHub ribbon is not found"
