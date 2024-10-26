import os
from dotenv import load_dotenv

# Load environment variables from .env file
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
    BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')
