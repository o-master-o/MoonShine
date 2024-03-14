from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from chromedriver_py import binary_path


class ChromeDriver:

    def __new__(cls, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_experimental_option("detach", True)
        options.add_argument("--headless")
        return webdriver.Chrome(options=options, service=ChromeService(executable_path=binary_path))
