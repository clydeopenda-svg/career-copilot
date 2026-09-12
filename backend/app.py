from flask import Flask, jsonify, request
from flask_cors import CORS

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

    profile_text = profile.lower()
    job_text = job_description.lower()

    required_skills = [
        skill for skill in COMMON_SKILLS
        if skill in job_text
    ]

    matching_skills = [
        skill for skill in required_skills
        if skill in profile_text
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in profile_text
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