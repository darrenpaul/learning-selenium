import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup():
    driver_path = '{0}/chromedriver'.format(os.path.dirname(os.path.realpath(__file__)))
    driver = webdriver.Chrome(
        executable_path=driver_path,
    )
    return driver
