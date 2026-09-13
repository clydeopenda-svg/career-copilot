from flask import Flask, jsonify, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


COMMON_SKILLS = [
    "javascript",
    "react",
    "python",
    "flask",
    "sql",
    "git",
    "github",
    "html",
    "css",
    "node",
    "typescript",
    "api",
]


def contains_skill(text, skill):
    pattern = rf"\b{re.escape(skill)}\b"
    return re.search(pattern, text, re.IGNORECASE) is not None


@app.route("/")
def home():
    return jsonify({
        "message": "Career Copilot API is running"
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request data is required."
        }), 400

    profile = data.get("profile", "").strip()
    job_description = data.get("jobDescription", "").strip()

    if not profile or not job_description:
        return jsonify({
            "error": "Both profile and job description are required."
        }), 400

    required_skills = [
        skill
        for skill in COMMON_SKILLS
        if contains_skill(job_description, skill)
    ]

    matching_skills = [
        skill
        for skill in required_skills
        if contains_skill(profile, skill)
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if not contains_skill(profile, skill)
    ]

    if required_skills:
        match_score = round(
            (len(matching_skills) / len(required_skills)) * 100
        )
    else:
        match_score = 0

    return jsonify({
        "matchScore": match_score,
        "matchingSkills": matching_skills,
        "missingSkills": missing_skills,
    })


if __name__ == "__main__":
    app.run(debug=True)