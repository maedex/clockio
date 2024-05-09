# kot_selenium
Snippets to automate operations of clock-in/clock-out with KOT, KING OF TIME. \
With configuring with Linux Cron, you can reduce your time for daily administration task.

## Configure with Linux Cron
Example would be updated soon.

## Run locally
Note that if you need to run program from your laptop, please confirm that Python 3.x is installed onto your system. \
As initial release, only `Python 3.11.8 (virtualenv)` has been tested.

```shell
# Install dependencies
% pip install -r requirements.txt

# When you start your work
% export KOT_OPS='clock-in'
# or, when you end your work
% export KOT_OPS='clock-out'
```

```shell
# Add your credentials for KOT
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
