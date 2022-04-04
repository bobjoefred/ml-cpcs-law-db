import sys
sys.path.append("..")

# Custom libraries
from ocr import extract_text
from officer_roster import lookup_builder
from suit_extraction import field_extraction

# Standard libraries
import pandas as pd
from os import walk, path

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

    _, _, filenames = next(walk(input_directory), (None, None, []))

    # Get the text tokens
    for filename in filenames:
        if ".pdf" not in filename:
            filenames.remove(filename)
    print(filenames)

    # Establish the initial text tokens
    text = []
    for filename in filenames:
        text.extend(extract_text.pdf_to_text(input_directory + "/" + filename))
    
    return text