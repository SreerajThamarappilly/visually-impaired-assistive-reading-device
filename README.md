# visually-impaired-assistive-reading-device

This project is an Assistive Reading Device for the Visually Impaired. It is a backend service that accepts images containing text, processes the image to extract the text using Optical Character Recognition (OCR), converts the extracted text into speech, and returns an audio file.

## Features

Image Upload: Accepts images via a RESTful API.
Asynchronous Processing: Uses Celery and Redis for asynchronous task handling.
OCR Processing: Extracts text from images using OCR.
Text-to-Speech Conversion: Converts extracted text into speech.
Audio Response: Returns the speech as an audio file.
Dockerized Deployment: Easily deployable using Docker.
Scalable Architecture: Suitable for cloud deployment and scaling.


## Technologies Used

Python
Flask: Web framework for handling HTTP requests.
Celery: Asynchronous task queue.
Redis: Message broker for Celery.
Tesseract OCR: For text recognition.
pyttsx3: For offline text-to-speech conversion.
Pillow (PIL): For image processing.
OpenCV: For advanced image preprocessing.
Gunicorn: WSGI server for deployment.
Docker & Docker Compose: For containerization and orchestration.

## Directory Structure

'''bash
assistive_reading_device/
├── app.py
├── celery_worker.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── .env
├── utils/
│   ├── __init__.py
│   ├── ocr.py
│   └── tts.py
├── static/
│   └── uploads/
├── templates/
└── logs/
    └── app.log

app.py: The main Flask application.
celery_worker.py: The Celery worker script.
config.py: Configuration settings.
requirements.txt: Python dependencies.
Dockerfile: Docker image configuration.
docker-compose.yml: Docker Compose configuration.
README.md: Project documentation.
.env: Environment variables.
utils/: Utility modules for OCR and TTS.
static/uploads/: Directory for uploaded images and audio files.
logs/app.log: Log file for application logs.
'''

## API Endpoints

### POST /api/v1/process_image
Description:- Accepts an image file, processes it asynchronously to extract text, converts the text to speech, and returns an audio file.
Parameters:- image (required): The image file containing text.
Responses:-
202 Accepted: Returns a task ID for status tracking.
400 Bad Request: If the image is not provided or invalid.
500 Internal Server Error: If an unexpected error occurs.

### GET /api/v1/task_status/<task_id>
Description:- Checks the status of a background task.
Parameters:- task_id (required): The ID of the task to check.
Responses:-
200 OK: Returns the status and result (if completed).
404 Not Found: If the task ID is invalid.
500 Internal Server Error: If an unexpected error occurs.

## Environmental Variables

FLASK_ENV: The environment in which the app is running (development, production).
SECRET_KEY: A secret key for securing sessions and cookies.
UPLOAD_FOLDER: Directory for storing uploaded images (static/uploads).
ALLOWED_EXTENSIONS: Allowed file extensions for upload ('png', 'jpg', 'jpeg', 'gif').
LOG_FILE: Path to the log file (logs/app.log).
BROKER_URL: URL of the message broker (redis://redis:6379/0 for Docker).
RESULT_BACKEND: Backend for storing task results (redis://redis:6379/0 for Docker).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or bugs.

## License

This project is licensed under the MIT License.
