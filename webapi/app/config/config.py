import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "sqlite3.db")

SQLALCHEMY_RECORD_QUERIES = True

SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_ECHO = True
