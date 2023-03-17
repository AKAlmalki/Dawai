import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

DB_PATH = os.environ['DATABASE_URL']

# IMPLEMENT DATABASE URL [done]
SQLALCHEMY_DATABASE_URI = DB_PATH

SQLALCHEMY_TRACK_MODIFICATIONS = False
