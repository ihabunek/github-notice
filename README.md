github-notice
=============

A simple script which sends email notifications for Github pull requests.

Deploy
------

Install prerequisites into a virtual env:
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Copy empty settings file, and fill in the info.
```
cp settings.dist.py settings.py
vim settings.py
```

Add script to crontab, e.g. run every 10 minutes:
```
*/10 * * * * python /path/to/notify.py
```

If you fill in the username and password for github, then the Github API
allows 5000 queries per hour. Otherwise you're limited to 50 queries per hour
so be careful how often you run the script.
