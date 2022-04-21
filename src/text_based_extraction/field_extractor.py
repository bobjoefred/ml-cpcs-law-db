import sys
import re
import os
from os import walk, path
from .internal_unique_id_lookup import lookup
import pandas as pd

 
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
def get_suit_fields(complaint_lines, order_tokens, officer_roster_csv_path):
  # extract fields
  docket_num = extract_docket_num(order_tokens)

  agency = extract_agency(complaint_lines)

  officers, iuid_str = extract_officer_data(complaint_lines, officer_roster_csv_path)

  fields = { 'Docket Number': docket_num, 'Officer(s)': officers, 'Internal Unique ID (Officer)': iuid_str, 'Agency (from Officers)': agency }

  return fields


# input: list of lowered tokens
# output: docket number
def extract_docket_num(tokens):
  # docket number e.g. 1:16-cv-11865-WGY or 1184CV00961
  docket_num_regex = re.compile('[0-9]:?[0-9]*-?cv.*')
  docket_num = list(filter(docket_num_regex.match, tokens))[0].upper()

  return docket_num


def extract_agency(lines):
  agency_regex = re.compile('(?i)(city|town) of ([a-z]{3,40})[\., ]')
  agency_matches = [m.group(2) for m in (agency_regex.match(line) for line in lines) if m]
  agency_matches = list(set(agency_matches))
  agency_list = [town.title() + ' Police Department' for town in agency_matches]
  agency = ';'.join(agency_list)
  return agency


# pass in complaint lines, returns list of officers and list of internal uniquid IDs
def extract_officer_data(lines, officer_roster_csv_path):
  officer_roster = pd.read_csv(officer_roster_csv_path)

  officers_regex = re.compile('Defendant ([a-zA-Z\']{3,40})(?:\s[A-Z].)?\s([a-zA-Z\']{3,40}) (is|was)')

  # create list of tuples
  officer_names = [(m.group(1), m.group(2)) for m in (officers_regex.match(str(line)) for line in lines) if m]
  officer_names = list(set(officer_names))

  officers = '; '.join([last + ', ' + first for first, last in officer_names])

  # TODO: remove collisions from lookup with same name by using agency field too 
  iuid_list = [lookup(first + " " + last, officer_roster) for first, last in officer_names]
  iuid_str = '; '.join([iuid for iuid in iuid_list if iuid])

  return officers, iuid_str