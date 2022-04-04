import sys
sys.path.append("..")

# Custom libraries
from suit_extraction import field_extraction
from officer_roster import lookup_builder
from ocr import extract_text

# Standard libraries
from nltk.tokenize import word_tokenize
import nltk
import fitz # PyMuPDF
from os import walk, path
import pandas as pd
nltk.download('punkt')

data_columns = ['Docket Number',
                'Internal Unique ID (Officer)',
                'Case Name/Caption',
                'Officer(s)',
                'Agency (from Officers)'
                'Incident Tags',
                'Courts',
                'Disposition Type',
                'Disposition Date',
                'Settlement/Judgment Amount',
                'Attachments',
                'Notes']


def generate_csv(input_directory, output_file='output.csv'):
    df = pd.DataFrame(columns=data_columns)

    # Standardize path name
    input_directory = path.join(input_directory, '')

    _, _, filenames = next(walk(input_directory), (None, None, []))

    # Get PDF files 
    for filename in filenames:
        if ".pdf" not in filename:
            filenames.remove(filename)
    print(filenames)

    # Search through filenames to find relevant complaint and order documents
    complaint_filenames = [fn for fn in filenames if 'Complaint' in fn]
    complaint_filename = complaint_filenames[0]
    order_filenames = [
        fn for fn in filenames if 'Order' in fn or 'Judgment' in fn]
    order_filename = order_filenames[-1]
    print('Complaint: ' + complaint_filename + '\nOrder: ' + order_filename)

    # Use OCR for complaint document, which is scanned
    # complaint_lines is organized as a list of strings, each a single line of the document
    complaint_lines = extract_text.pdf_to_text(
        input_directory + complaint_filename)

    # Use simple text extraction for order document, which is digitally created
    # order_tokens is a list of lowercase single-word tokens
    order_tokens = []
    with fitz.open(input_directory + order_filename) as doc:
        for page in doc:
            page_text = page.get_text().lower()
            page_tokens = word_tokenize(page_text)
            order_tokens += page_tokens
    
    fields = field_extraction.get_suit_fields(complaint_lines, order_tokens) 
    print(fields)

    return fields

# generate_csv('../../examples/Andro v. Brookline')