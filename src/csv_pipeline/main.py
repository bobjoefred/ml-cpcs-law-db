import sys
sys.path.append("..")

# Custom libraries
from ocr import extract_text
from officer_roster import lookup_builder
from suit_extraction import field_extraction

# Standard libraries
import pandas as pd

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

df = pd.DataFrame(columns=data_columns)
print(df)