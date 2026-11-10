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


def analyze(profile, job_description):
    response = app.test_client().post(
        "/api/analyze",
        json={"profile": profile, "jobDescription": job_description},
    )

    assert response.status_code == 200
    return response.get_json()


def test_analyze_recognises_common_skill_spellings():
    data = analyze(
        "JS, TS, ReactJS, NodeJS, PostgreSQL, REST APIs, HTML5 and CSS3.",
        "JavaScript, TypeScript, React, Node, SQL, API, HTML and CSS.",
    )

    assert data["missingSkills"] == []
    assert data["matchScore"] == 100


def test_analyze_finds_spelling_variants_in_the_job_description():
    data = analyze("I write Python.", "You will build REST APIs with MySQL.")

    assert data["missingSkills"] == ["sql", "api"]


def test_analyze_does_not_read_node_js_as_javascript():
    data = analyze("Node.js developer", "JavaScript and Node experience.")

    assert data["matchingSkills"] == ["node"]
    assert data["missingSkills"] == ["javascript"]


def test_analyze_does_not_read_nosql_as_sql():
    data = analyze("NoSQL databases", "Strong SQL skills.")

    assert data["missingSkills"] == ["sql"]
