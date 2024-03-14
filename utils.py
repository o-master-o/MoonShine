import pytest

from controller import ChromeDriver

ENTRY_POINT = 'https://the-internet.herokuapp.com/'


@pytest.fixture(scope='session')
def chrome():
    driver = ChromeDriver()
    try:
        yield driver
    finally:
        driver.quit()
