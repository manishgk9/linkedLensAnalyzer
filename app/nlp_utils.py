import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_resume_sections(text: str):
    sections = {}
    current = None
    for line in text.splitlines():
        line = line.strip()
        if re.match(r'(summary|experience|education|skills)', line.lower()):
            current = line.lower()
            sections[current] = ""
        elif current:
            sections[current] += " " + line
    return sections

def extract_entities(text: str):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
s