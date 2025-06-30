import spacy
from utils import TECH_SKILLS

nlp = spacy.load("en_core_web_sm")

def parse_resume(text):
    doc = nlp(text)
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), None)
    skills = [s for s in TECH_SKILLS if s in text.lower()]
    return {"name": name, "skills": skills, "text": text}
