from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re
import spacy

app = Flask(__name__)
CORS(app)

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_courses_and_grades(text):
    # Adjust the regular expression to match your transcript format
    courses = re.findall(r"Course: (.*?)\s+Grade: (.*?)\n", text)
    print("Extracted Courses and Grades:", courses)  # Debug print
    return [{"course": course, "grade": grade} for course, grade in courses]

def extract_skills(text, course_name):
    doc = nlp(text)
    skills = []
    for sent in doc.sents:
        if course_name in sent.text:
            skills.append(sent.text.strip())
    return skills

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    text = extract_text_from_pdf(file)
    print("Extracted Text:", text)  # Debug print
    courses = extract_courses_and_grades(text)
    return jsonify({'courses': courses})

@app.route('/skills', methods=['GET'])
def get_skills():
    course_name = request.args.get('course')
    text = extract_text_from_pdf("path_to_transcript.pdf")  # Replace with actual handling
    skills = extract_skills(text, course_name)
    return jsonify({'skills': skills})

if __name__ == '__main__':
    app.run(debug=True)
