from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import pdfplumber
import os

from groq import Groq

from app.extensions import db
from app.models.resume_model import ResumeAnalysis

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text


@resume_bp.route("/analyze", methods=["POST"])
@jwt_required()
def analyze_resume():

    user_id = int(get_jwt_identity())

    file = request.files["resume"]

    print("analysing the reusme now...")
    resume_text = extract_text(file)
    print("resume analyzed...")

    prompt = f"""
    Analyze this resume.

    Provide:
    - ATS score (0–100)
    - Key strengths
    - Missing skills
    - Suggested improvements

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant"
    )

    result = response.choices[0].message.content

    analysis = ResumeAnalysis(user_id=user_id, resume_text=resume_text, analysis=result)

    db.session.add(analysis)
    db.session.commit()

    return jsonify({"analysis": result})
