import os
import sys
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# constants
KOT_URL = "https://s3.ta.kingoftime.jp/independent/recorder2/personal"
MAX_UI_WAIT_TIME_SEC = 10

KOT_OPS = os.environ.get('KOT_OPS')
KOT_USERNAME = os.environ.get('KOT_USERNAME')
KOT_PASSWORD = os.environ.get('KOT_PASSWORD')

# randomize wait time
START_OFFSET_MIN = random.randint(0, 60)


print('>>> Precheck for user input')
if (KOT_OPS is None) or (KOT_USERNAME is None) or (KOT_PASSWORD is None):
    print('Required environmental variable(s) not provided, please set: KOT_OPS, KOT_USERNAME, KOT_PASSWORD')
    sys.exit(1)

if KOT_OPS.lower() not in ['clock-in', 'clock-out']:
    print('provided operation could not be accepted, only `clock-in` or `clock-out` can be used for KOT_OPS.')
    sys.exit(1)

print(f"KOT_OPS: {KOT_OPS}")
print(f"KOT_USERNAME: {KOT_USERNAME}")
print(f"KOT_PASSWORD: ******\n")

print(f'>>> Waiting for {START_OFFSET_MIN} mintues to start, maximum wait time is 60 minutes.')
sleep(START_OFFSET_MIN * 60)
print('OK, starting to Selenium operation\n')


# Selenium Operation
chrome_options = Options()
chrome_options.add_argument("--headless=new")

print('>>> Instantiating Webdriver and its utilities...')
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, MAX_UI_WAIT_TIME_SEC)

try:
    print('>>> Login and wait until page rendered')
    driver.get(KOT_URL)
    wait.until(expected_conditions.title_contains("My Recorder"))
    sleep(5)
except Exception as e:
    print('Failed to open URL.')
    print(e)
    sys.exit(1)

try:
    print('>>> Fillout ID and Password for login')
    element_id = driver.find_element(By.ID, 'id')
    element_id.send_keys(KOT_USERNAME)
    element_password = driver.find_element(By.ID, 'password')
    element_password.send_keys(KOT_PASSWORD)

    element_ok = driver.find_element(By.CLASS_NAME, 'btn-control-message').click()
except Exception as e:
    print('Failed to login KOT.')
    print(e)
    sys.exit(1)

# Wait and click button for clock-in/clock-out
sleep(5)

try:
    print('>>> Registering the entries')
    if KOT_OPS.lower() == 'clock-in':
        element_clockin = driver.find_element(By.CLASS_NAME, 'record-clock-in').click()
    elif KOT_OPS.lower() == 'clock-out':
        element_clockout = driver.find_element(By.CLASS_NAME, 'record-clock-out').click()
except Exception as e:
    print('Failed to click clock-in/clock-out button')
    sys.exit(1)

sleep(5)
driver.quit()

print(f'Done, completed daily [ {KOT_OPS} ] operations.\n')
