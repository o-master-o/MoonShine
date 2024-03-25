import pytest
from selenium.webdriver.support.wait import WebDriverWait

from controller import ChromeDriver

ENTRY_LINK = 'the-internet.herokuapp.com/'
HTTPS_ENTRY_LINK = f'https://{ENTRY_LINK}'


@pytest.fixture(scope='module')
def chrome():
    driver = ChromeDriver()
    try:
        yield driver
    finally:
        driver.quit()


def wait_till_page_loaded(chrome):
    WebDriverWait(chrome, timeout=10).until(lambda d: d.execute_script("return document.readyState") == "complete")
