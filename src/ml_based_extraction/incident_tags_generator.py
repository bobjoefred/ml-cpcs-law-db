from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

def generate_incident_tags(input_lines):
    """
    Generate incident tags based on zero shot classification
    """
    candidate_labels = ['Violence', 'Integirty', 'None']
    result = classifier(input_lines, candidate_labels)
    print(result['labels'])
    print(result['scores'])
    return result
