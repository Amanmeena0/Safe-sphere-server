import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'aman-meena')
    # Default to SQLite if no DATABASE_URL is provided
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///crime.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
