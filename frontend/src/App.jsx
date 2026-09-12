import { useState } from "react";

function App() {
  const [profile, setProfile] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [saved, setSaved] = useState("");

  function handleProfileChange(event) {
    setProfile(event.target.value);
    setSaved("");
  }

  function handleJobDescriptionChange(event) {
    setJobDescription(event.target.value);
    setSaved("");
  }

  function handleProfileSave() {
    setSaved("Profile saved.");
    console.log("Saved profile:", profile);
  }

  function handleJobSave() {
    setSaved("Job description saved.");
    console.log("Saved job description:", jobDescription);
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

      {saved && <p className="status-message">{saved}</p>}
    </main>
  );
}

export default App;