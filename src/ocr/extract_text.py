import easyocr

def extract_text(img_path):
    """
    Extract text from an image using OCR.
    """
    # Load the OCR engine
    ocr = easyocr.Reader(['en'])

    # Extract the text
    text = ocr.readtext(img_path)

    result = []

    for entry in text:
        for element in entry:
            if isinstance(element, str):
                result.append(element)

    # Return the text
    return result