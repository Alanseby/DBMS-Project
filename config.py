import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    
    # Get database URL from environment variable
    # Supports both PostgreSQL and MySQL
    database_url = os.environ.get('DATABASE_URL')
    
    # Fix for Heroku postgres:// to postgresql+pg8000:// (Windows-compatible)
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+pg8000://', 1)
    # Also handle postgresql:// to use pg8000 driver
    elif database_url and database_url.startswith('postgresql://') and 'pg8000' not in database_url:
        database_url = database_url.replace('postgresql://', 'postgresql+pg8000://', 1)
    
    # Default to local MySQL if no DATABASE_URL is set
    SQLALCHEMY_DATABASE_URI = database_url or 'mysql+pymysql://fprms_user:fprms_pass@localhost/fprms'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # This will show SQL queries in console
    
    # Additional settings for online databases
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using them
        'pool_recycle': 300,    # Recycle connections after 5 minutes
    }