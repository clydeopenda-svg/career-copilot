from flask import Flask, jsonify, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


SKILL_RECOMMENDATIONS = {
    "javascript": "Practice JavaScript fundamentals and build a small project using functions, arrays, objects, and asynchronous code.",
    "react": "Build a React project using components, state, props, forms, and API requests.",
    "python": "Strengthen your Python fundamentals by building small programs that work with functions, lists, dictionaries, and files.",
    "flask": "Build a small Flask API with multiple routes, request validation, and JSON responses.",
    "sql": "Practice SQL queries involving filtering, joins, grouping, and database relationships.",
    "git": "Practice Git by creating branches, making meaningful commits, resolving conflicts, and working with pull requests.",
    "github": "Improve your GitHub workflow by maintaining a clear README, organized repositories, and useful commit history.",
    "html": "Practice semantic HTML by building accessible forms, navigation, and structured web pages.",
    "css": "Improve your CSS skills by practicing responsive layouts, Flexbox, Grid, spacing, and component styling.",
    "node": "Build a small Node.js API and practice working with packages, routes, and asynchronous operations.",
    "typescript": "Learn TypeScript fundamentals and gradually convert a small JavaScript project to TypeScript.",
    "api": "Practice working with REST APIs by building endpoints, sending requests, handling JSON, and validating responses.",
}


def contains_skill(text, skill):
    pattern = rf"\b{re.escape(skill)}\b"
    return re.search(pattern, text, re.IGNORECASE) is not None


def get_match_summary(match_score):
    if match_score >= 80:
        return "Strong match: you have most of the skills mentioned in this job description."
    elif match_score >= 50:
        return "Good starting point: you match several requirements, but there are some skills worth improving."
    else:
        return "Needs improvement: there are several important skills in the job description that are not in your profile yet."


def get_recommendations(missing_skills):
    recommendations = []

    for skill in missing_skills:
        recommendation = SKILL_RECOMMENDATIONS.get(skill)

        if recommendation:
            recommendations.append({
                "skill": skill,
                "recommendation": recommendation,
            })

    return recommendations


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
        for skill in SKILL_RECOMMENDATIONS
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

    summary = get_match_summary(match_score)
    recommendations = get_recommendations(missing_skills)

    return jsonify({
        "matchScore": match_score,
        "summary": summary,
        "matchingSkills": matching_skills,
        "missingSkills": missing_skills,
        "recommendations": recommendations,
    })


if __name__ == "__main__":
    app.run(debug=True)