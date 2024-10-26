import pytesseract
from PIL import Image
import cv2
import os
from config import Config

class OCRProcessor:
    """
    Class responsible for extracting text from images using OCR.
    """

    def __init__(self):
        """
        Initializes the OCRProcessor class.
        """
        # If TESSERACT_CMD is specified, set the tesseract command path
        if Config.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD

    def preprocess_image(self, image_path):
        """
        Preprocesses the image to improve OCR accuracy.
        :param image_path: Path to the image file
        :return: Preprocessed image
        """
        image = cv2.imread(image_path)
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # Save the preprocessed image temporarily
        temp_filename = f"{os.getpid()}.png"
        cv2.imwrite(temp_filename, gray)
        return temp_filename

    def extract_text(self, image_path):
        """
        Extracts text from the given image using OCR.
        :param image_path: Path to the image file
        :return: Extracted text as a string
        """
        # Preprocess the image
        temp_image = self.preprocess_image(image_path)
        # Perform OCR
        text = pytesseract.image_to_string(Image.open(temp_image))
        # Remove the temporary image file
        os.remove(temp_image)
        return text
