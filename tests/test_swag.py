
from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest
from time import sleep
from get_excel_data import login_form_parameters
from get_db_data import login_form_parameters
import logging
# ######common functions########

logging.basicConfig(filename= 'C:\Data-driven\logs\info.log',
                    encoding='utf-8',
                    level=logging.info,
                    force=True,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %P')

def launch_swaglabs():
    logging.info('Launching the swaglabs page')
    global driver
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.saucedemo.com/')

def valid_login_swaglabs():
    logging.info('Logging in')
    driver.find_element(By.ID, 'username').send_keys('standard_user')
    driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
    driver.find_element(By.CLASS_NAME, 'submit-button').click()

def capture_evidence():
    image_name = fr"C:\Data-driven\evidence\image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png"
    driver.save_screenshot(image_name)

def text_is_displayed(text):
    logging.info(f'Checking if [{text}] exists on the page')
    return text.lower() in driver.page_source.lower()

############### Test Cases ##############

def test_launch_login_page():
    launch_swaglabs()
    assert driver.title == 'Swag Labs'
    capture_evidence()
    driver.quit()


@pytest.mark.parametrize("username, password, checkpoint", login_form_parameters)
def test_login_invalid_credentials(username, password, checkpoint):
    launch_swaglabs()
    if username != None: driver.find_element(By.ID, 'user-name').send_keys(username)
    if password != None: driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'submit-button').click()
    sleep(5)
    assert text_is_displayed(checkpoint)
    capture_evidence()
    driver.quit()

##############BELOW TEST CASES PASS###############################
@pytest.fixture()
def setup(request):
    launch_swaglabs()
    valid_login_swaglabs()
   
    def teardown():
        capture_evidence()
        driver.quit()
    request.addfinalizer(teardown)

def test_login_valid_credentials(setup):
    assert text_is_displayed('products')
    

def test_view_product_details(setup):
   
    product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
    product_names[0].click()
    assert text_is_displayed('back to products')
   





