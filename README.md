github-notice
=============

A simple script which sends email notifications for Github pull requests.

Deploy
------

1. Copy `settings.dist.py` to `settings.py`
2. Fill in the required settings in `settings.py`
3. Add script to cron

If you fill in the username and password for github, then the github api
allows 5000 queries per hour. Otherwise you're limited to 50 queries per hour
so be careful how often you run the script.
