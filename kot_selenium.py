import datetime
import os
import sys
import random
from time import sleep

import requests
from icalendar import Calendar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


# constants
KOT_URL = 'https://s3.ta.kingoftime.jp/independent/recorder2/personal'
MAX_UI_WAIT_TIME_SEC = 10
GOOGLE_HOLIDAY_CALENDAR_URL = 'https://calendar.google.com/calendar/ical/avagotech.com_bg0up3r3juf2lun6hm8rgbgq54%40group.calendar.google.com/public/basic.ics'

# user inputs
KOT_OPS = os.environ.get('KOT_OPS')
KOT_USERNAME = os.environ.get('KOT_USERNAME')
KOT_PASSWORD = os.environ.get('KOT_PASSWORD')
GOOGLE_USER_CALENDAR_URL = os.environ.get('GOOGLE_USER_CALENDAR_URL')
GOOGLE_SPACE_WEBHOOK_URL = os.environ.get('GOOGLE_SPACE_WEBHOOK_URL')
# randomize wait time
START_OFFSET_MIN = int(os.environ.get('START_OFFSET_MIN')) if os.environ.get('START_OFFSET_MIN') and int(os.environ.get('START_OFFSET_MIN')) <= 60 and int(os.environ.get('START_OFFSET_MIN')) >= 0 else random.randint(0, 60)

# Validations
print('>>> Precheck for user input')
if (KOT_OPS is None) or (KOT_USERNAME is None) or (KOT_PASSWORD is None) or (GOOGLE_USER_CALENDAR_URL is None):
    print('Required environmental variable(s) not provided, please set: KOT_OPS, KOT_USERNAME, KOT_PASSWORD, GOOGLE_USER_CALENDAR_URL\n')
    sys.exit(1)

if KOT_OPS.lower() not in ['clock-in', 'clock-out']:
    print('provided operation could not be accepted, only `clock-in` or `clock-out` can be used for KOT_OPS.\n')
    sys.exit(1)

print(f"KOT_OPS: {KOT_OPS}")
print(f"KOT_USERNAME: {KOT_USERNAME}")
print(f"KOT_PASSWORD: ******")
print(f"GOOGLE_USER_CALENDAR_URL: ******")
print(f"GOOGLE_SPACE_WEBHOOK_URL: {GOOGLE_SPACE_WEBHOOK_URL}")

# # weekdate validation can be implemented with cron
# print('>>> Determine weekday or not')
# if (datetime.date.today().weekday() == 5) or (datetime.date.today().weekday() == 6):
#     print('Today is weekend, need not to run script.\n')
#     sys.exit(0)
# print('Today is not weekday, continue to validation\n')

print('>>> Determine public holiday or not')
try:
    ctx = requests.get(GOOGLE_HOLIDAY_CALENDAR_URL).content
    ics = Calendar.from_ical(ctx)
    # Filter out Japan holiday
    holidays = [ve for ve in ics.walk('VEVENT') if 'Japan' in ve['SUMMARY']]
except Exception as e:
    print('Failed to fetch public holiday\n')
    sys.exit(1)

if datetime.date.today() in [h['DTSTART'].dt for h in holidays]:
    print('Today is public holiday, need not to run script.\n')
    sys.exit(0)
print('Today is not public holiday, continue to validation')

print('>>> Determine PTO or not')
try:
    ctx = requests.get(GOOGLE_USER_CALENDAR_URL).content
    ics = Calendar.from_ical(ctx)
    # Fetch only todays vEvent object with strformatting datetime.date/datetime.datetime at the same time
    events = [ve for ve in ics.walk('VEVENT') if ve['DTSTART'].dt.strftime('%Y/%m/%d') == datetime.date.today().strftime('%Y/%m/%d')]
except Exception as e:
    print('Failed to fetch events from user calendar URL.\n')
    sys.exit(1)

if 'PTO' in [e['SUMMARY'] for e in events]:
    print('Today is PTO, need not to run script.\n')
    sys.exit(1)
print('Today is not PTO, finishing validation.\n')


print(f'>>> Waiting for {START_OFFSET_MIN} mintues to start, maximum wait time is 60 minutes.')
sleep(START_OFFSET_MIN * 60)
print('OK, moving to Selenium operation\n')


# Selenium Operation
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--remote-debugging-pipe')

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
        text = '出勤'
    elif KOT_OPS.lower() == 'clock-out':
        element_clockout = driver.find_element(By.CLASS_NAME, 'record-clock-out').click()
        text = '退勤'
except Exception as e:
    print('Failed to click clock-in/clock-out button')
    sys.exit(1)

sleep(5)
driver.quit()

# notification features are an optional
if GOOGLE_SPACE_WEBHOOK_URL is not None:
    try:
        print('>>> Making notifications to Google Space')
        # build body
        username = GOOGLE_USER_CALENDAR_URL.split('/')[5].split('%')[0]
        rheader = {'Content-Type': 'application/json'}
        rbody = {
            "text": f"[ {username} ] さんが{text}しました。\n実際の業務時間はこの限りではない点にご注意ください。"
        }
        resp = requests.post(url=GOOGLE_SPACE_WEBHOOK_URL, headers=rheader, verify=False, json=rbody)
        print(resp)
    except Exception as e:
        print('Failed to post message to Google Space')
        print(e)
        sys.exit(1)

print(f'Done, completed daily [ {KOT_OPS} ] operations.\n')
