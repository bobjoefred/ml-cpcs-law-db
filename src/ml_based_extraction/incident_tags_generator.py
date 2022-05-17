"""
Import zero shot classifier pipeline
"""
from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large")

def generate_incident_tags(input_lines):
    """
    Generate incident tags based on zero shot classification
    """
    candidate_labels = ['Violence Problem', 'Integrity Problem', 'Other Problem']
    result = classifier(input_lines, candidate_labels)
    max_value_index = result['scores'].index(max(result['scores']))
    return result['labels'][max_value_index]
