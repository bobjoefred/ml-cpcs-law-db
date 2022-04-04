import sys
sys.path.append("..")
import re
import os
from os import walk, path

 
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


# takes in a list of lines from complaint doc and a list of tokens from order doc
# returns dictionary of extracted fields
def get_suit_fields(complaint_lines, order_tokens):
  # extract fields
  docket_num = extract_docket_num(order_tokens)

  officers = extract_officers(complaint_lines)

  fields = { 'Docket Number': docket_num, 'Officer(s)': officers }

  return fields


# input: list of lowered tokens
# output: docket number
def extract_docket_num(tokens):
  # docket number e.g. 1:16-cv-11865-WGY or 1184CV00961
  docket_num_regex = re.compile('[0-9]:?[0-9]*-?cv.*')
  docket_num = list(filter(docket_num_regex.match, tokens))[0].upper()

  return docket_num

# pass in complaint lines, returns list of officers
def extract_officers(lines):
  officers_regex = re.compile('Defendant ([a-zA-Z\']{3,40})(?:\s[A-Z].)?\s([a-zA-Z\']{3,40}) (is|was)')
  officers = [m.group(1) + ' ' + m.group(2) for m in (officers_regex.match(str(line)) for line in lines) if m]

  # remove duplicates
  officers = list(set(officers))

  return officers