# kot_selenium
To Be Updated

## Configure with Linux Cron
To Be Updated

## Run locally
Note that if you need to run program from your laptop, please confirm that Python 3.x is installed onto your system.
As initial release, Python 3.11.8 (virtualenv) has been tested.

```shell
# Clock-In
% export KOT_OPS='clock-in'
% export KOT_USERNAME='xxxxxxx'
% export KOT_PASSWORD='xxxxxxx'

# Run
# Note that password is hidden in stdout and the following outputs are omitted as examples
% python kot_selenium.py
>>> Precheck for user input
KOT_OPS: clock-out
KOT_USERNAME: trme3c3382413
KOT_PASSWORD: ******

>>> Waiting for 3 mintues to start, maximum wait time is 60 minutes.
OK, starting to Selenium operation

>>> Instantiating Webdriver and its utilities...
>>> Login and wait until page rendered
>>> Fillout ID and Password for login
>>> Registering the entries
Done, completed daily [ clock-in ] operations.
```
