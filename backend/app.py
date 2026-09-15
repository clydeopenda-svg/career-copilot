from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import re

load_dotenv()

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


INTERVIEW_QUESTIONS = {
    "javascript": [
        "What is the difference between let, const, and var in JavaScript?",
        "How does asynchronous code work in JavaScript?",
    ],
    "react": [
        "What are React components and why are they useful?",
        "What is the difference between props and state in React?",
    ],
    "python": [
        "What are lists and dictionaries in Python?",
        "How do you handle errors in Python?",
    ],
    "flask": [
        "What is Flask and why would you use it to build an API?",
        "How would you validate data received by a Flask endpoint?",
    ],
    "sql": [
        "What is the difference between an INNER JOIN and a LEFT JOIN?",
        "How would you find duplicate records in a SQL table?",
    ],
    "git": [
        "What is the difference between git merge and git rebase?",
        "How do you resolve a Git merge conflict?",
    ],
    "github": [
        "How would you use a pull request in a team project?",
        "What makes a good GitHub repository?",
    ],
    "html": [
        "What is semantic HTML?",
        "Why is accessibility important when building web pages?",
    ],
    "css": [
        "What is the difference between Flexbox and CSS Grid?",
        "How would you make a website responsive?",
    ],
    "node": [
        "What is Node.js and why is it useful for backend development?",
        "How does asynchronous programming work in Node.js?",
    ],
    "typescript": [
        "What advantages does TypeScript provide over JavaScript?",
        "What is the purpose of TypeScript interfaces?",
    ],
    "api": [
        "What is a REST API?",
        "What is the difference between GET and POST requests?",
    ],
}


SKILL_PRIORITY = [
    "html",
    "css",
    "javascript",
    "typescript",
    "react",
    "node",
    "python",
    "flask",
    "sql",
    "api",
    "git",
    "github",
]


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


def get_learning_priority(missing_skills):
    ordered_skills = [
        skill
        for skill in SKILL_PRIORITY
        if skill in missing_skills
    ]

    return ordered_skills[:3]


def get_interview_questions(required_skills):
    questions = []

    for skill in required_skills:
        skill_questions = INTERVIEW_QUESTIONS.get(skill, [])

        for question in skill_questions:
            questions.append({
                "skill": skill,
                "question": question,
            })

    return questions[:6]


def get_ai_config():
    return {
        "provider": os.getenv("AI_PROVIDER", ""),
        "model": os.getenv("AI_MODEL", ""),
        "configured": bool(os.getenv("AI_API_KEY")),
    }


@app.route("/")
def home():
    return jsonify({
        "message": "Career Copilot API is running"
    })


@app.route("/api/ai-status")
def ai_status():
    config = get_ai_config()

    return jsonify({
        "provider": config["provider"],
        "model": config["model"],
        "configured": config["configured"],
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request data is required."
        }), 400

    profile = data.get("profile")
    job_description = data.get("jobDescription")

    if not isinstance(profile, str) or not isinstance(job_description, str):
        return jsonify({
            "error": "Both profile and job description are required."
        }), 400

    profile = profile.strip()
    job_description = job_description.strip()

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
    learning_priority = get_learning_priority(missing_skills)
    interview_questions = get_interview_questions(required_skills)

    return jsonify({
        "matchScore": match_score,
        "summary": summary,
        "matchingSkills": matching_skills,
        "missingSkills": missing_skills,
        "recommendations": recommendations,
        "learningPriority": learning_priority,
        "interviewQuestions": interview_questions,
    })


if __name__ == "__main__":
    app.run(debug=True)