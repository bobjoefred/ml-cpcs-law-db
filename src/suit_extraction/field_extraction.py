import fitz # pymupdf

# Need to install tesseract in order to use OCR to extract text
# https://pymupdf.readthedocs.io/en/latest/installation.html

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import re
from os import walk, path
from ..ocr import extract_text

 
'''
data fields required for civil suits (database field name - spreadsheet field name - example):
docket_num - docket number - 1:16-cv-11865-WGY
iuid - internal unique ID (officer) - 010-00088536; 010-09145982; 010-04943462
case_name - case name/caption - Baez v. Brockton Police Deptartment, et al
officers - officer(s) - Khoury, George; Gomes, Emanuel; Sargo, Wayne
agency - agency (from Officers) - Brockton Police Department
tags - incident tags - False Testimony/Untruthfulness; Bias-based Profiling
courts - courts - United States District Court for the District of Massachusetts
disp_type - disposition type - Settled, Dismissed with Prejudice
disp_date - disposition date - [BLANK FIELD]
total_settlement - settlement/judgment amount - 69595
notes - notes - https://drive.google.com/drive/folders/191GkC8uPO4wJmrypBJVyRFYIxLZAL8v3
'''


# input: directory path containing files for a single civil suit
# output: dictionary with all data fields for the civil suit
def get_suit_fields(directory):

  # standardize path name
  directory = path.join(directory, '')

  # get all files in directory recursively
  _, _, filenames = next(walk(directory), (None, None, []))

  # search through filenames to find relevant complaint and order documents
  complaint_filenames = [fn for fn in filenames if 'Complaint' in fn]
  complaint_filename = complaint_filenames[-1]
  order_filenames = [fn for fn in filenames if 'Order' in fn or 'Judgment' in fn]
  order_filename = order_filenames[-1]
  print('Complaint: ' + complaint_filename + '\nOrder: ' + order_filename)

  # create combined lowered token list
  tokens = []

  # use OCR for complaint document, which is scanned
  # complaint_text = extract_text.pdf_to_text(complaint_filename)
  # print(complaint_text)

  # use simple text extraction for order document, which is digitally created


  for fn in [complaint_filename, order_filename]:
    with fitz.open(directory + fn) as doc:
      for page in doc:
        page_text = page.get_text().lower()
        page_tokens = word_tokenize(page_text)
        tokens += page_tokens

  # extract fields
  docket_num = extract_docket_num(tokens)
  print(docket_num)

  return { 'docket_num': docket_num }


# input: list of lowered tokens
# output: docket number
def extract_docket_num(tokens):

  # docket number e.g. 1:16-cv-11865-WGY or 1184CV00961
  docket_num_regex = re.compile('[0-9]:?[0-9]*-?cv.*')
  docket_num = list(filter(docket_num_regex.match, tokens))[0].upper()
  return docket_num