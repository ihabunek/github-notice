from datetime import datetime
from email.mime.text import MIMEText
from pprint import pprint
import base64
import contextlib
import json
import os
import smtplib
import requests
import logging
import logging.config

# -- SETTINGS ------------------------------------------------------------------

# Path to the cache file
CACHE = 'cache.json'

from settings import *

# Authenticate if credentials are provided
if (GITHUB_USER and GITHUB_PASS):
    GITHUB_AUTH = (GITHUB_USER, GITHUB_PASS)
else:
    GITHUB_AUTH = None

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('notify.py')

# -- CODE ----------------------------------------------------------------------

def main():
    cache = load_cache()
    pull_requests = fetch_pull_requests()

    for request in pull_requests:
        number = str(request['number']) # str because of json
        updated = datetime.strptime(request['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

        # Skip closed issues, remove from cache
        if request['state'] != 'open':
            if number in cache:
                del cache[number]
            continue

        # In cache -> check if modified
        if number in cache:
            cache_updated = datetime.strptime(cache[number]['updated'], "%Y-%m-%dT%H:%M:%SZ")
            if updated > cache_updated:
                notify_modified(request)
                cache[number]['updated'] = request['updated_at']

        # Not in cache -> this is a new pull request
        else:
            notify_new(request)
            cache[number] = {
                'updated': request['updated_at']
            }

    save_cache(cache)

def notify_new(request):
    subject = "[Github] [Created] Pull request #%d: %s" % (request['number'], request['title'])
    message = format_pull_request(request)
    send_email(subject, message)

def notify_modified(request):
    subject = "[Github] [Updated] Pull request #%d: %s" % (request['number'], request['title'])
    message = format_pull_request(request)
    send_email(subject, message)

def format_pull_request(request):
    number = request['number']
    comments = fetch_comments(number)

    title = "#%d: %s" % (number, request['title'])

    msg = title + "\r\n";
    msg += '=' * len(title) + "\r\n"
    msg += request['body'] + "\r\n\r\n"
    msg += "URL: %s" % request['html_url']

    if (comments):
        msg += "\r\n\r\n"
        msg += "Comments:\r\n"
        msg += "-" * 50 + "\r\n"

    for comment in comments:
        user = comment['user']['login']
        time = comment['created_at']
        msg += comment['body'].strip() + "\r\n\r\n"
        msg += "Commented by %s at %s" % (user, time)
        msg += "\r\n" + ("-" * 50) +"\r\n"

    return msg

def fetch_pull_requests():
    url = 'https://api.github.com/repos/%s/pulls' % REPO
    return fetch_url(url)

def fetch_pull_request(number):
    url = 'https://api.github.com/repos/%s/pulls/%d' % (REPO, number)
    return fetch_url(url)

def fetch_comments(number):
    url = 'https://api.github.com/repos/%s/issues/%d/comments' % (REPO, number)
    return fetch_url(url)

def fetch_url(url):
    logger.info("Loading: %s", url)
    r = requests.get(url, auth = GITHUB_AUTH)
    r.raise_for_status()
    
    # Log API usage info
    limit = r.headers['x-ratelimit-limit']
    remaining = r.headers['x-ratelimit-remaining']
    logger.debug("Remaining %s out of %s requests for this hour", remaining, limit)
    
    return r.json()

def load_cache():
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            data = f.read()
        return json.loads(data)
    else:
        return {}

def save_cache(cache):
    cache_json = json.dumps(cache, indent=4)
    with open(CACHE, 'w') as f:
        f.write(cache_json)

def send_email(subject, message):
    logger.info("Sending email: %s", subject)

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = ",".join(MAIL_TO)

    print "Sending email: %s" % subject

    s = smtplib.SMTP(SMTP_HOST)
    s.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
    s.quit()

if __name__ == "__main__":
    main()
