# app.py

from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
import os
from utils.ocr import OCRProcessor
from utils.tts import TTSProcessor
from config import Config
import logging
from celery import Celery
from celery.result import AsyncResult
from uuid import UUID

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(filename=app.config['LOG_FILE'], level=logging.INFO)

# Function to initialize Celery with Flask app context
def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL'],
        backend=app.config['RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    # Ensure TESSERACT_CMD is set in the Celery worker environment
    if 'TESSERACT_CMD' in app.config:
        celery.conf.update({'TESSERACT_CMD': app.config['TESSERACT_CMD']})

    return celery

# Initialize Celery
celery = make_celery(app)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = set(app.config['ALLOWED_EXTENSIONS'].split(','))

def allowed_file(filename):
    """
    Check if the file has an allowed extension.
    :param filename: Name of the uploaded file
    :return: Boolean indicating if the file is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_task_id(task_id):
    """
    Validate if the provided task_id is a valid UUID.
    """
    try:
        UUID(task_id, version=4)
        return True
    except ValueError:
        return False

@app.route('/api/v1/process_image', methods=['POST'])
def process_image():
    """
    API endpoint to process the uploaded image asynchronously and return a task ID.
    """
    if 'image' not in request.files:
        logging.error('No image part in the request')
        return jsonify({"status": "error", "error": {"code": 400, "message": "No image part in the request"}}), 400

    file = request.files['image']

    if file.filename == '':
        logging.error('No selected file')
        return jsonify({"status": "error", "error": {"code": 400, "message": "No selected file"}}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        # Asynchronously process the image
        task = process_image_task.delay(image_path, filename)
        return jsonify({"status": "success", "data": {"task_id": task.id}}), 202
    else:
        logging.error('Invalid file type')
        return jsonify({"status": "error", "error": {"code": 400, "message": f"Invalid file type. Allowed types are {', '.join(ALLOWED_EXTENSIONS)}"}}), 400

@app.route('/api/v1/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    """
    API endpoint to get the status of a background task.
    """
    # Validate the task_id format
    if not validate_task_id(task_id):
        return jsonify({"status": "error", "error": {"code": 400, "message": "Invalid task ID format"}}), 400

    task_result = AsyncResult(task_id, app=celery)

    if task_result.state == 'PENDING':
        response = {
            "status": "success",
            "data": {
                "state": task_result.state,
                "status": "Pending..."
            }
        }
    elif task_result.state != 'FAILURE':
        response = {
            "status": "success",
            "data": {
                "state": task_result.state,
                "status": task_result.info.get('status', ''),
                "result": task_result.info.get('result', '')
            }
        }
        if 'result' in task_result.info:
            response["data"]['download_url'] = url_for('static', filename='uploads/' + task_result.info['result'], _external=True)
    else:
        response = {
            "status": "error",
            "error": {
                "code": 500,
                "message": str(task_result.info)
            }
        }
    return jsonify(response)

@celery.task(bind=True)
def process_image_task(self, image_path, filename):
    """
    Celery task to process the image and convert text to speech.
    """
    ocr_processor = OCRProcessor()
    tts_processor = TTSProcessor()

    try:
        # Initial state update
        self.update_state(state='PROGRESS', meta={'status': 'Starting task...'})

        # Extract text from image
        self.update_state(state='PROGRESS', meta={'status': 'Extracting text from image...'})
        extracted_text = ocr_processor.extract_text(image_path)
        logging.info(f'Extracted Text: {extracted_text}')

        # Convert text to speech
        self.update_state(state='PROGRESS', meta={'status': 'Converting text to speech...'})
        audio_filename = tts_processor.text_to_speech(extracted_text, filename)
        logging.info(f'Audio file created at: {audio_filename}')

        # Final state update
        return {'status': 'Task completed!', 'result': audio_filename}
    except Exception as e:
        logging.exception('Error processing the image')
        self.update_state(state='FAILURE', meta={'status': str(e)})
        raise e

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
