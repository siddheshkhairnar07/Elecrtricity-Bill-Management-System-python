import pytesseract
from PIL import Image
from datetime import date

# Set the path for Tesseract executable (make sure to change this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Function to extract text (meter reading) from the image using OCR
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


# Function to extract meter reading from the OCR text
def extract_meter_reading(text):
    lines = text.splitlines()
    for line in lines:
        if "Reading" in line:  # Look for a line containing 'Reading'
            reading = ''.join([ch for ch in line if ch.isdigit()])
            if reading:
                return int(reading)
    return None


# Function to calculate bill based on unit consumption and rate per unit
def calculate_bill(previous_reading, current_reading, rate_per_unit=0.12):
    if current_reading < previous_reading:
        raise ValueError("Current reading cannot be less than previous reading.")
    units_consumed = current_reading - previous_reading
    return units_consumed * rate_per_unit


# Get today's date
def get_today_date():
    return date.today().strftime('%Y-%m-%d')
