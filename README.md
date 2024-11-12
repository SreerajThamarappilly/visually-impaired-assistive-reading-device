# visually-impaired-assistive-reading-device

This project is an Assistive Reading Device for the Visually Impaired. It is a backend service that accepts images containing text, processes the image to extract the text using Optical Character Recognition (OCR), converts the extracted text into speech, and returns an audio file.


## Features

- **Image Upload**: Accepts images via a RESTful API.
- **Asynchronous Processing**: Uses Celery and Redis for asynchronous task handling.
- **OCR Processing**: Extracts text from images using Tesseract OCR.
- **Text-to-Speech Conversion**: Converts extracted text into speech using `gTTS`.
- **Audio Response**: Returns the speech as an audio file.
- **Advanced Image Preprocessing**: Uses OpenCV for enhanced OCR accuracy.
- **Logging**: Tracks processing steps in a log file.
- **Dockerized Deployment**: Easily deployable using Docker for consistent environment replication.
- **Scalable Architecture**: Suitable for cloud deployment and scaling (GCP, AWS, etc.).


## Technologies Used

- **Python Flask**: Web framework for handling HTTP requests.
- **Celery**: Asynchronous task queue for managing background processing.
- **Redis**: Message broker for Celery, enabling asynchronous communication.
- **Tesseract OCR**: Optical Character Recognition (OCR) for extracting text from images.
- **gTTS (Google Text-to-Speech)**: For online text-to-speech conversion.
- **ffmpeg**: Used with gTTS to handle audio file formatting.
- **Pillow (PIL)**: For image handling and basic transformations.
- **OpenCV**: For advanced image preprocessing to improve OCR accuracy.
- **Gunicorn**: WSGI server for deploying Flask applications in production.
- **Docker & Docker Compose**: Containerization for easy deployment and scalability.
- **python-dotenv**: Loads environment variables from a `.env` file for secure configuration.
- **Logging**: Stores application logs in `logs/app.log` for monitoring and debugging.


## Directory Structure

```bash
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
└── logs/
    └── app.log

- **app.py**: The main Flask application.
- **celery_worker.py**: The Celery worker script.
- **config.py**: Configuration settings.
- **requirements.txt**: Python dependencies.
- **Dockerfile**: Docker image configuration.
- **docker-compose.yml**: Docker Compose configuration.
- **README.md**: Project documentation.
- **.env**: Environment variables.
- **utils/**: Utility modules for OCR and TTS.
- **static/uploads/**: Directory for uploaded images and audio files.
- **logs/app.log**: Log file for application logs.
```


## API Endpoints

### POST /api/v1/process_image
- **Description**:- Accepts an image file, processes it asynchronously to extract text, converts the text to speech, and returns an audio file.
- **Parameters**:- image (required): The image file containing text.
- **Responses**:-
    - 202 Accepted: Returns a task ID for status tracking.
    - 400 Bad Request: If the image is not provided or invalid.
    - 500 Internal Server Error: If an unexpected error occurs.

```bash
POST API : http://localhost:8000/api/v1/process_image
Sample Request Body form-data: image (File) = Welcome.jpg (uploaded file)
Sample Response BOdy: {
    "data": {
        "task_id": "be09d496-a892-4b4d-a523-38848ae80578"
    },
    "status": "success"
}
```

### GET /api/v1/task_status/<task_id>
- **Description**:- Checks the status of a background task.
- **Parameters**:- task_id (required): The ID of the task to check.
- **Responses**:-
    - 200 OK: Returns the status and result (if completed).
    - 404 Not Found: If the task ID is invalid.
    - 500 Internal Server Error: If an unexpected error occurs.

```bash
GET API : http://localhost:8000/api/v1/task_status/be09d496-a892-4b4d-a523-38848ae80578
Sample Response BOdy: {
    "data": {
        "download_url": "http://localhost:8000/static/uploads/static/uploads/Welcome.mp3",
        "result": "static/uploads/Welcome.mp3",
        "state": "SUCCESS",
        "status": "Task completed!"
    },
    "status": "success"
}
```


## Environmental Variables

- **FLASK_ENV**: The environment in which the app is running (`development`, `production`).
- **SECRET_KEY**: A secret key for securing sessions and cookies, used by Flask.
- **UPLOAD_FOLDER**: Directory for storing uploaded images (default: `static/uploads`).
- **ALLOWED_EXTENSIONS**: Allowed file extensions for upload (e.g., `png`, `jpg`, `jpeg`, `gif`).
- **LOG_FILE**: Path to the log file where application logs will be stored (default: `logs/app.log`).
- **BROKER_URL**: URL of the message broker (e.g., `redis://redis:6379/0` for Redis running in Docker).
- **RESULT_BACKEND**: Backend for storing task results (e.g., `redis://redis:6379/0` for Redis running in Docker).
- **TESSERACT_CMD**: The file path to the Tesseract OCR executable (e.g., `/usr/bin/tesseract` for Docker). This variable is required for the OCR processing component to locate Tesseract.


## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or bugs.


## License

This project is licensed under the MIT License.
