import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DISK_TOKEN = os.getenv(
        'DISK_TOKEN',
        'y0__xDC8oWfAhjvoTggwICZuxN4XbC8doE1J4S2cvC7EkMCq7jCGQ'
    )
