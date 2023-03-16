import os
# SECRET_KEY = os.urandom(32)
SECRET_KEY = "Dawai-2000"
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database AND setting up the env variables
DB_HOST = os.getenv('DB_HOST', 'database-dawai.cyd5dayxhyym.me-south-1.rds.amazonaws.com:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Dawai-2000')
DB_NAME = os.getenv('DB_NAME', 'dawai')

DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

# IMPLEMENT DATABASE URL [done]
SQLALCHEMY_DATABASE_URI = DB_PATH

SQLALCHEMY_TRACK_MODIFICATIONS = False
