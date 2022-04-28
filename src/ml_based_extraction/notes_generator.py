"""
Library imports, import huggingface transformers library and torch
"""
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

MODEL_NAME = "google/pegasus-xsum"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = PegasusTokenizer.from_pretrained(MODEL_NAME)
model = PegasusForConditionalGeneration.from_pretrained(MODEL_NAME).to(DEVICE)

def generate_notes(text):
    """
    Generate summarization based on the google pegasus model
    """
    batch = tokenizer(text, truncation=True, padding="longest", return_tensors="pt").to(DEVICE)

    translated = model.generate(**batch)

    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    return tgt_text[0]
