import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def ABS_PATH(*args):
    return os.path.join(ROOT_DIR, *args)

# Github credentials
# If left blank, you will be limited to 50 requests per hour
GITHUB_USER = ''
GITHUB_PASS = ''

# The github repository for which to send reminders:
# <user>/<repo>
REPO = '<user>/<repo>'

# Mail to put in from field of email notifications
MAIL_FROM = 'sender@example.com'

# Destination email addresses for te notifications
MAIL_TO = [
    'person@example.com'
]

# The mail server
SMTP_HOST = 'localhost'

# Configure logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': ABS_PATH('notify.log'),
            'mode': 'a',
            'maxBytes': 10 * 1024**2,
            'backupCount': 1,
            'formatter': 'detailed'
        },
    },
    'loggers': {
        'notify.py': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    }
}