# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for Flask app and Celery settings.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    # Celery configuration
    BROKER_URL = os.getenv('BROKER_URL', 'redis://redis:6379/0')
    RESULT_BACKEND = os.getenv('RESULT_BACKEND', 'redis://redis:6379/0')
    broker_connection_retry_on_startup = True

    # Tesseract command path inside Docker container
    TESSERACT_CMD = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')
