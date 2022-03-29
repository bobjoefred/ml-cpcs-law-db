from pdf2image import convert_from_path
from tqdm import tqdm
import easyocr
import numpy as np

def extract_text(img_path, ocr_engine):
    """
    Extract text from an image using OCR.
    """
    # Load the OCR engine

    # Extract the text
    text = ocr_engine.readtext(img_path)

    result = []

    for entry in text:
        for element in entry:
            if isinstance(element, str):
                result.append(element)

    # Return the text
    return result

def pdf_to_text(pdf_path):
    """
    Convert a pdf to a list of text.
    """
    # Convert pdf to images
    images = convert_from_path(pdf_path)

    # Convert them to numpy arrays
    np_arrays = []
    for image in images:
        np_arrays.append(np.asarray(image))
    
    print("Converted PDF to images.")
    
    result = []
    ocr = easyocr.Reader(['en'])
    # Extract the text
    for i in tqdm(range(len(np_arrays))):
        result.append(extract_text(np_arrays[i], ocr))

    return result

print(pdf_to_text('example.pdf'))