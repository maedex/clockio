# kot_selenium
Snippets to automate operations of clock-in/clock-out with KOT, KING OF TIME. \
With configuring with Linux Cron, you can reduce your time for daily administration task.

## Prerequisites
Firstly, for enabling to login to KOT by script, you need to prepare credentials of KOT My Recorder URL. \
Alos, since this snippet is integrated to your Google Calendar, you need to check your personal Google Calandar link, before running the script. \
For obtaining your personal link, navigate to [Settings menu](https://calendar.google.com/calendar/u/0/r/settings) in Google Calendar UI, and scroll down to left tab `Settings for my calendars`. \
In detailed menu, you can see the it.

![Secret URL Menu](https://gist.github.com/assets/25563897/0d97bdf1-2d13-4e8a-a522-954392ea0667)

## Examples of Ubuntu Crontab configuration
For running every weekday, the following crontab configurations might be used as examples. \
For applying it, you can simply run `crontab -e` as a general user (non-root user).

```shell
KOT_USERNAME='trme3c3382413'
KOT_PASSWORD='******'
GOOGLE_USER_CALENDAR_URL='https://calendar.google.com/calendar/ical/********'
0 8 * * 1-5 KOT_OPS='clock-in' python3 /home/hwakabayashi/kot_selenium/kot_selenium.py
0 18 * * 1-5 KOT_OPS='clock-out' python3 /home/hwakabayashi/kot_selenium/kot_selenium.py
```

For avoiding increasing disk utilization, the stdout of script is disabled in crontab by default. \
In case you need to print out stdout of script for such as debugging, you can simply update your crontab commands like:

```shell
0 8 * * 1-5 KOT_OPS='clock-in' python3 /home/hwakabayashi/kot_selenium/kot_selenium.py >> $(date "+\%Y/\%m/\%d_\%H:\%M:\%S")_kot.log
```

## Security Considerations
To be updated

## Run locally
Note that if you need to run program from your laptop, please confirm that Python 3.x is installed onto your system. \
As initial release, only `Python 3.11.8 (virtualenv)` and `Python 3.10.12 (Ubuntu packaged)` has been tested.

```shell
# Install dependencies
% pip install -r requirements.txt

# When you start your work
% export KOT_OPS='clock-in'
# or, when you end your work
% export KOT_OPS='clock-out'
```

```shell
# Set your credentials for KOT
% export KOT_USERNAME='xxxxxxx'
% export KOT_PASSWORD='xxxxxxx'

# Set your Google Calendar URL (Secret URL)
% export GOOGLE_USER_CALENDAR_URL='https://calendar.google.com/calendar/ical/********'

# Run
# Note that password is hidden in stdout and the following outputs are omitted as examples
% python kot_selenium.py
>>> Precheck for user input
KOT_OPS: clock-out
KOT_USERNAME: trme3c3382413
KOT_PASSWORD: ******
GOOGLE_USER_CALENDAR_URL: ******
>>> Determine public holiday or not
Today is not public holiday, continue to validation
>>> Determine PTO or not
Today is not PTO, finishing validation.

>>> Waiting for 3 mintues to start, maximum wait time is 60 minutes.
OK, starting to Selenium operation

>>> Instantiating Webdriver and its utilities...
>>> Login and wait until page rendered
>>> Fillout ID and Password for login
>>> Registering the entries
Done, completed daily [ clock-in ] operations.
```
