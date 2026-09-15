import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Career Copilot API is running"
    }


def test_analyze_matching_skills():
    client = app.test_client()

    response = client.post(
        "/api/analyze",
        json={
            "profile": "I know React, Python, SQL and Git.",
            "jobDescription": (
                "We need a developer with React, Python, "
                "JavaScript, SQL and Git experience."
            ),
        },
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["matchScore"] == 80
    assert "react" in data["matchingSkills"]
    assert "python" in data["matchingSkills"]
    assert "sql" in data["matchingSkills"]
    assert "git" in data["matchingSkills"]
    assert "javascript" in data["missingSkills"]


def test_analyze_requires_profile_and_job_description():
    client = app.test_client()

    response = client.post(
        "/api/analyze",
        json={
            "profile": "",
            "jobDescription": "",
        },
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == (
        "Both profile and job description are required."
    )