"""
Needed library imports
"""
from lib2to3.pgen2 import token
import sys
import re
import os
from os import walk, path
from .internal_unique_id_lookup import lookup

import sys
sys.path.append("..")
from ml_based_extraction import notes_generator
from ml_based_extraction import incident_tags_generator
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
def get_suit_fields(complaint_lines, order_tokens, dir_name, officer_roster_csv_path):
    # extract fields
    docket_num = extract_docket_num(order_tokens)

    agency = extract_agency(complaint_lines)

    officers, iuid_str = extract_officer_data(complaint_lines, agency, officer_roster_csv_path)

    notes = notes_generator.generate_notes(" ".join(complaint_lines))

    incident_tag = incident_tags_generator.generate_incident_tags(" ".join(complaint_lines))

    court = extract_court(complaint_lines)

    disposition_type, disposition_date = extract_disposition_info(order_tokens)

    fields = { 'Docket Number': docket_num,
                'Internal Unique ID (Officer)': iuid_str,
                'Case Name/Caption': dir_name,
                'Officer(s)': officers,
                'Agency (from Officers)': agency,
                'Incident Tags': incident_tag,
                'Courts': court,
                'Disposition Type': disposition_type,
                'Disposition Date': disposition_date,
                'Notes': notes }

    return fields


# input: list of lowered tokens
# output: docket number
def extract_docket_num(tokens):
    """
    docket number e.g. 1:16-cv-11865-WGY or 1184CV00961
    """
    docket_num_regex = re.compile('[0-9]:?[0-9]*-?cv.*')
    try:
        docket_num = list(filter(docket_num_regex.search, tokens))[0].upper()
        return docket_num
    except:
        return ""


def extract_agency(lines):
    try:
        agency_regex = re.compile('(?i)(city|town) of ([a-z]{3,40})[\.,; ]')
        agency_matches = [m.group(2) for m in [agency_regex.search(line) for line in lines] if m]

        agency_list = [town.title() + ' Police Department' for town in agency_matches]
        agency_list = list(set(agency_list))
        agency = ';'.join(agency_list)
        return agency
    except:
        return ""


# pass in complaint lines, returns list of officers and list of internal unique IDs
def extract_officer_data(lines, agency, officer_roster_csv_path):
    try:
        officer_roster = pd.read_csv(officer_roster_csv_path)
        officers_regex = re.compile('Defendant ([a-zA-Z\']{3,40})(?:\s[A-Z].)?\s([a-zA-Z\']{3,40}) (is|was|ID)')
        # create list of tuples
        officer_names = [(m.group(1).title(), m.group(2).title()) for m in [officers_regex.search(str(line)) for line in lines] if m]
        officer_names = list(set(officer_names))

        officers = '; '.join([last + ', ' + first for first, last in officer_names])

        iuid_list = [lookup(first + " " + last, agency, officer_roster) for first, last in officer_names]
        iuid_str = '; '.join([iuid for iuid in iuid_list if iuid])

        return officers, iuid_str
    except:
        return ""


def extract_court(lines):
    # get court line and cut off string after "court" in case of extraneous parts of line
    court_list = [line[:line.lower().index("court") + len("court")] for line in lines if "court" in line.lower()]
    if court_list:
        return court_list[0].title()
    else:
        return ""


# returns settlement type, settlement amount (if applicable)
def extract_disposition_info(tokens):
    disposition_types = []

    combined_tokens = " ".join(tokens)
    settlement = False

    settlement_terms = ["shall recover", "interest at the rate of", "the amount of $"]

    if any(term in combined_tokens for term in settlement_terms):
        settlement = True
        disposition_types.append("Settled")

    # select either with prejudice, without prejudice, or generally dismissed where it is unclear
    if "with prejudice" in combined_tokens:
        disposition_types.append("Dismissed with Prejudice")
    elif "without prejudice" in combined_tokens:
        disposition_types.append("Dismissed without Prejudice")
    elif "dismissed" in combined_tokens:
        disposition_types.append("Dismissed")
    
    disposition_string = "; ".join(disposition_types)

    disposition_date_regex = re.compile('Filed ([0-9]{2}/[0-9]{2}/[0-9]{2})')
    date_match = re.search(disposition_date_regex, combined_tokens)
    date = date_match.group(1) if date_match else ""
    

    return disposition_string, date
    

