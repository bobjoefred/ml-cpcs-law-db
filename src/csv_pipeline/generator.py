"""
Standard and custom libraries
"""
import re
from os import walk, path
import pickle
import fitz # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from text_based_extraction import field_extractor
from text_based_extraction import internal_unique_id_lookup
from ml_based_extraction import text_extractor
from ml_based_extraction import incident_tags_generator


def generate_fields(input_directory, dir_name, officer_roster_csv_path, debug = False):
    """
    Function generates the field CSV files to be used by the CPCS team
    """

    # Standardize path name
    input_directory = path.join(input_directory, '')

    _, _, filenames = next(walk(input_directory), (None, None, []))

    # Get PDF files 
    for filename in filenames:
        if ".pdf" not in filename:
            filenames.remove(filename)

    complaint_filename, order_filenames = select_filenames(filenames)
    print("Complaint file:", complaint_filename)
    print("Order filenames: ", order_filenames)

    # Use OCR for complaint document, which is scanned
    # complaint_lines is organized as a list of strings, each a single line of the document
    if not debug:
        complaint_lines = text_extractor.pdf_to_text(input_directory + complaint_filename)
        with open('data/complaint_lines_' + path.splitext(complaint_filename)[0] + '.pkl', 'wb') as file:
            pickle.dump(complaint_lines, file)
    else:
        with open('data/complaint_lines_' + path.splitext(complaint_filename)[0] + '.pkl', 'rb') as file:
            complaint_lines = pickle.load(file)

    # Use simple text extraction for order document, which is digitally created
    # order_tokens is a list of lowercase single-word tokens
    order_tokens = []
    try:
        for order_filename in order_filenames:
            with fitz.open(input_directory + order_filename) as doc:
                for page in doc:
                    page_text = page.get_text().lower()
                    page_tokens = word_tokenize(page_text)
                    order_tokens += page_tokens
    except:
        print("Order document not found.")
        order_tokens = word_tokenize((" ".join(complaint_lines)).lower())

    fields = field_extractor.get_suit_fields(complaint_lines, order_tokens, dir_name, officer_roster_csv_path)

    return fields


# Returns tuple of complaint filename, order filename 
def select_filenames(filenames):
    """
    Sort filenames by document number, with length of filename to break ties
    """
    try:
        filenames.sort(key=lambda fn: (int(re.search('\[([^]-]+)(\]|-)', fn).group(1)), len(fn)))
    except:
        print("Document number not found.")

    if not len(filenames):
        return None, None
    elif len(filenames) == 1:
        return filenames[0], None

    selected_complaint = None

    # Select complaints with priority to [1-main] document
    complaints = [fn for fn in filenames if 'complaint' in fn.lower() and 'answer' not in fn.lower()]
    complaint = [fn for fn in complaints if '[1-main]' in fn.lower()]
    if len(complaint):
        selected_complaint = complaint[0]
    elif len(complaints):
        selected_complaint = complaints[0]
    else:
        selected_complaint = filenames[0]

    order_terms = ['order', 'dismissal', 'settlement', 'docket', 'judgment']

    # Select first relevant order or last file
    orders = [fn for fn in filenames if any(term in fn.lower() for term in order_terms)]
    if not orders:
        orders = [filenames[-1]]

    return selected_complaint, orders
