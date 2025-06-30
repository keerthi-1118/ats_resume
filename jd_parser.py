from utils import TECH_SKILLS

def parse_jd(text):
    skills = [s for s in TECH_SKILLS if s in text.lower()]
    return {"jd_skills": skills, "text": text}
