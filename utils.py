
import fitz  # PyMuPDF
import docx

TECH_SKILLS = [
    "python", "java", "c++", "html", "css", "javascript", "react", "node.js",
    "flask", "django", "sql", "mongodb", "git", "rest", "api", "docker",
    "data structures", "algorithms", "machine learning", "oop","dsa"
]
def extract_text_from_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)
