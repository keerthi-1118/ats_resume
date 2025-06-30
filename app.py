from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import parse_resume
from jd_parser import parse_jd
from matcher import get_similarity
from utils import extract_text_from_pdf, extract_text_from_docx

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✔️ ATS Resume Checker API is live."

@app.route("/match", methods=["POST"])
def match_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "Resume file is missing"}), 400

        resume_file = request.files['resume']
        jd_file = request.files.get('job')
        jd_text_input = request.form.get('jd_text', '')

        resume_text = extract_text_from_pdf(resume_file)
        print("[DEBUG] Extracted resume text:", resume_text[:200])  # print sample

        if jd_file:
            if jd_file.filename.endswith('.pdf'):
                jd_text = extract_text_from_pdf(jd_file)
            elif jd_file.filename.endswith('.docx'):
                jd_text = extract_text_from_docx(jd_file)
            else:
                return jsonify({"error": "Unsupported JD file type"}), 400
        elif jd_text_input.strip():
            jd_text = jd_text_input
        else:
            return jsonify({"error": "No job description provided"}), 400

        print("[DEBUG] Extracted JD text:", jd_text[:200])  # print sample

        parsed_resume = parse_resume(resume_text)
        parsed_jd = parse_jd(jd_text)

        score = get_similarity(resume_text, jd_text)

        matched = list(set(parsed_resume["skills"]) & set(parsed_jd["jd_skills"]))
        missing = list(set(parsed_jd["jd_skills"]) - set(parsed_resume["skills"]))

        return jsonify({
            "semantic_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
        })

    except Exception as e:
        # Print error to console and return clean JSON error
        print("❌ Error in /match:", str(e))
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
