import sys
sys.path.append("..")

# Custom libraries
from text_based_extraction import field_extractor
from text_based_extraction import internal_unique_id_lookup
from ml_based_extraction import text_extractor
from ml_based_extraction import case_name_generator
from ml_based_extraction import settlement_extractor
from ml_based_extraction import incident_tags_generator

# Standard libraries
from nltk.tokenize import word_tokenize
import nltk
import pickle
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

def generate_csv(input_directory, officer_roster_csv_path, output_file='output.csv', debug = False):
    df = pd.DataFrame(columns=data_columns)
    officer_data = pd.read_csv(officer_roster_csv_path)

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
    order_filenames = [fn for fn in filenames if 'Order' in fn or 'Judgment' in fn]
    order_filename = order_filenames[-1]
    print('Complaint: ' + complaint_filename + '\nOrder: ' + order_filename)

    # Use OCR for complaint document, which is scanned
    # complaint_lines is organized as a list of strings, each a single line of the document
    if not debug:
        complaint_lines = text_extractor.pdf_to_text(input_directory + complaint_filename)
        with open('complaint_lines.pkl', 'wb') as f:
            pickle.dump(complaint_lines, f)
    else:
        with open('complaint_lines.pkl', 'rb') as f:
            complaint_lines = pickle.load(f)

    # Use simple text extraction for order document, which is digitally created
    # order_tokens is a list of lowercase single-word tokens
    order_tokens = []
    with fitz.open(input_directory + order_filename) as doc:
        for page in doc:
            page_text = page.get_text().lower()
            page_tokens = word_tokenize(page_text)
            order_tokens += page_tokens
    
    fields = field_extractor.get_suit_fields(complaint_lines, order_tokens)

    # Populate dataframe with extracted fields
    df['Docket Number'] = fields['Docket Number']
    df['Internal Unique ID (Officer)'] = internal_unique_id_lookup.lookup(str(fields['Officer(s)']), officer_data)
    df['Case Name/Caption'] = case_name_generator.generate_case_name(complaint_lines)
    df['Officer(s)'] = fields['Officer(s)']
    # TODO: Add Agency (from Officers)
    # df['Agency (from Officers)'] = fields['Agency (from Officers)']
    df['Incident Tags'] = incident_tags_generator.generate_incident_tags(complaint_lines)
    # TODO: Add Courts
    # df['Courts'] = fields['Courts']
    # TODO: Add Disposition
    df['Disposition Type'] = None
    df['Disposition Date'] = None
    # TODO: Provide correct tokens that are relevant to settlement
    df['Settlement/Judgment Amount'] = settlement_extractor.get_settlement_amount(order_tokens)
    # TODO: Upload content to GDrive(?) and get shareable link
    df['Attachments'] = None
    df['Notes'] = None

    df.to_csv(output_file, index=False)

generate_csv(input_directory = '../../examples/Andro v. Brookline', officer_roster_csv_path = '../data/officer_roster.csv', debug = True)