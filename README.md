# kot_selenium
Snippets to automate operations of clock-in/clock-out with KOT, [KING OF TIME](https://www.kingoftime.jp). \
With configuring with Linux Cron, you can reduce your time for daily administration task.

Just cloning this Gist as general git repository onto your machine, where you would like to run script. \
Since Gist repository would be named with randomly hashed string, please be aware that you need to explicitly name cloned repo as `kot_selenium`.

```shell
# After SSH to remote machine, or just run on your local machine
% git clone https://gist.github.com/073279627e424bc555e7804f68cc32d1.git kot_selenium

# Install dependencies
% pip3 install -r requirements.txt
# in case you need to install packages separately, the packages required are: requests,icalendar,selenium
```

## Prerequisites
- `KOT_USERNAME` and `KOT_PASSWORD`

Firstly, for enabling to login to KOT by script, you need to prepare credentials to login KOT My Recorder URL. \
Also, since this snippet will interact with your Google Calendar, you need to check your personal Google Calandar link, before running the script.

- `GOOGLE_USER_CALENDAR_URL`

For obtaining your personal link, navigate to [Settings menu](https://calendar.google.com/calendar/u/0/r/settings) in Google Calendar UI, and scroll down to left tab `Settings for my calendars`. \
In detailed menu in your personal calendar, you can see `Secret address in iCal format` at the bottom.

![Secret URL Menu](https://gist.github.com/assets/25563897/0d97bdf1-2d13-4e8a-a522-954392ea0667)

- `GOOGLE_SPACE_WEBHOOK_URL` (optional)

Finally you need to configure Webhook URL in Google Space for making notifications of script operations. \
Please refer [the official documents of Google Workspace](https://developers.google.com/workspace/chat/quickstart/webhooks) for setting up Webhook URL, \
and please note that this operations requires permission as Space Manager.


## Examples of Ubuntu Crontab configuration
For running every weekday, the following crontab configurations might be used as examples. \
For applying it, you can simply run `crontab -e` as a general user (non-root user).

```shell
KOT_USERNAME='trme3c3382413'
KOT_PASSWORD='******'
GOOGLE_USER_CALENDAR_URL='https://calendar.google.com/calendar/ical/********'
GOOGLE_SPACE_WEBHOOK_URL='https://chat.googleapis.com/v1/spaces/****/messages?key=*****&token=******'
0 8 * * 1-5 KOT_OPS='clock-in' python3 /home/hwakabayashi/kot_selenium/kot_selenium.py
0 18 * * 1-5 KOT_OPS='clock-out' python3 /home/hwakabayashi/kot_selenium/kot_selenium.py
```

For avoiding increasing disk utilization, the stdout of script is disabled in crontab by default. \
In case you need to print out stdout of script for such as debugging, you can simply update your crontab commands like:

```shell
SHELL=/bin/bash
# (...)
0 8 * * 1-5 KOT_OPS='clock-in' python3 /home/hwakabayashi/kot_selenium/kot_selenium.py >> $(date "+\%Y/\%m/\%d_\%H:\%M:\%S")_kot.log
```

Note that please define running shell as `/bin/bash` in crontab, since Ubuntu will use `/usr/bin/dash` with cron by default, where we can not use shell redirection.

## Security Considerations
To be updated

## Run locally
Note that if you need to run program from your laptop, please confirm that Python 3.x is installed onto your system. \
As initial release, only `Python 3.11.8 (virtualenv)` and `Python 3.10.12 (Ubuntu packaged)` has been tested.

```shell
# When you start your work
% export KOT_OPS='clock-in'
# or, when you end your work
% export KOT_OPS='clock-out'

# Set your credentials for KOT
% export KOT_USERNAME='xxxxxxx'
% export KOT_PASSWORD='xxxxxxx'

# Set your Google Calendar URL (Secret URL)
% export GOOGLE_USER_CALENDAR_URL='https://calendar.google.com/calendar/ical/********'

# (optional) Set your Google Space URL
% export GOOGLE_SPACE_WEBHOOK_URL='https://chat.googleapis.com/v1/spaces/****/messages?key=*****&token=******'

# Run
# Note that password is hidden in stdout and the following outputs are intendedly omitted as in stdout
% python kot_selenium.py
>>> Precheck for user input
KOT_OPS: clock-out
KOT_USERNAME: trme3c3382413
KOT_PASSWORD: ******
GOOGLE_USER_CALENDAR_URL: ******
GOOGLE_SPACE_WEBHOOK_URL: ******
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
>>> Making notifications to Google Space
Done, completed daily [ clock-out ] operations.
```
