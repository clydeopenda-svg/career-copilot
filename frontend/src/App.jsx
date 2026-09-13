import { useState } from "react";

function App() {
  const [profile, setProfile] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [saved, setSaved] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleProfileChange(event) {
    setProfile(event.target.value);
    setSaved("");
    setAnalysis(null);
  }

  function handleJobDescriptionChange(event) {
    setJobDescription(event.target.value);
    setSaved("");
    setAnalysis(null);
  }

  function handleProfileSave() {
    if (!profile.trim()) {
      setSaved("Please enter your profile first.");
      return;
    }

    setSaved("Profile saved.");
  }

  function handleJobSave() {
    if (!jobDescription.trim()) {
      setSaved("Please enter a job description first.");
      return;
    }

    setSaved("Job description saved.");
  }

  async function analyzeJob() {
    if (!profile.trim() || !jobDescription.trim()) {
      setAnalysis({
        error: "Please enter both your profile and the job description.",
      });
      return;
    }

    setLoading(true);
    setAnalysis(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          profile,
          jobDescription,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setAnalysis({
          error: data.error || "Something went wrong.",
        });
        return;
      }

      setAnalysis(data);
    } catch (error) {
      setAnalysis({
        error: "Could not connect to the Career Copilot server.",
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="hero">
        <p className="eyebrow">CAREER COPILOT</p>

        <h1>
          Find out how well
          <span> you fit the job.</span>
        </h1>

        <p className="intro">
          Compare your skills with a job description and get practical
          feedback before you apply.
        </p>
      </header>

      <section className="workspace">
        <div className="card">
          <h2>Your profile</h2>

          <p>
            Tell us a little about your skills and experience.
          </p>

          <textarea
            value={profile}
            onChange={handleProfileChange}
            placeholder="Example: React, Python, Flask, Git, SQL..."
            rows="7"
          />

          <button onClick={handleProfileSave}>
            Save profile
          </button>
        </div>

        <div className="card">
          <h2>Job description</h2>

          <p>
            Paste the job description you want to analyze.
          </p>

          <textarea
            value={jobDescription}
            onChange={handleJobDescriptionChange}
            placeholder="Paste the job description here..."
            rows="7"
          />

          <button onClick={handleJobSave}>
            Save job
          </button>
        </div>
      </section>

      <section className="analysis">
        <button
          className="analyze-button"
          onClick={analyzeJob}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze my match"}
        </button>

        {analysis && (
          <div className="results">
            {analysis.error ? (
              <p className="error-message">
                {analysis.error}
              </p>
            ) : (
              <>
                <h2>Your match</h2>

                <p className="score">
                  {analysis.matchScore}%
                </p>

                <p className="summary">
                  {analysis.summary}
                </p>

                <h3>Skills you have</h3>

                {analysis.matchingSkills.length > 0 ? (
                  <p>
                    {analysis.matchingSkills.join(", ")}
                  </p>
                ) : (
                  <p>No matching skills found yet.</p>
                )}

                <h3>Skills to work on</h3>

                {analysis.missingSkills.length > 0 ? (
                  <p>
                    {analysis.missingSkills.join(", ")}
                  </p>
                ) : (
                  <p>No missing skills found.</p>
                )}
              </>
            )}
          </div>
        )}
      </section>

      {saved && (
        <p className="status-message">
          {saved}
        </p>
      )}
    </main>
  );
}

export default App;