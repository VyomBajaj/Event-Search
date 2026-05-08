import { useState } from "react";
import "../App.css";
import Hero from "../components/Hero";
import FormCard from "../components/FormCard";
import Navbar from "../components/Navbar";

export default function UserPage() {

  const [results, setResults] = useState([]);
  const [submitted, setSubmitted] = useState(false);

  const getRelativePath = (url) => {
    const parts = url.split("/static/");
    return parts[1]; // wedding1/me1.jpg
  };

  const scoreLabel = (score) => {
    if (score >= 0.8) return "strong";
    if (score >= 0.6) return "good";
    if (score >= 0.4) return "fair";
    return "low";
  };

  return (
    <div className="app">
      
      <Navbar />
      <Hero />

      {/* Form Card */}
      <main className="main">
        <FormCard
          setResults={setResults}
          setSubmitted={setSubmitted}
        />

        {/* Results */}
        {submitted && (
          <section className="results-section">
            <div className="results-header">
              <span className="results-label">RESULTS</span>
              <span className="results-count">{results.length} match{results.length !== 1 ? "es" : ""} found</span>
            </div>

            {results.length === 0 ? (
              <div className="no-results">
                <span className="no-results-icon">◯</span>
                <p>No matches found for this event.</p>
              </div>
            ) : (
              <div className="grid">
                {results.map((r, i) => (
                  <div className="photo-card" key={i}>
                    <div className="photo-wrap">
                      <img
                        src={r.image}
                        alt={`match-${i}`}
                        className="photo-img"
                        loading="lazy"
                      />
                      <div className="photo-overlay">
                        <div className="overlay-actions">
                          <a
                            href={r.image}
                            target="_blank"
                            rel="noreferrer"
                            className="view-link"
                          >
                            View ↗
                          </a>

                          <a
                            href={`http://127.0.0.1:8000/user/download?path=${encodeURIComponent(getRelativePath(r.image))}`}
                            className="download-link"
                            target="_blank"
                            rel="noreferrer"
                          >
                            Download ↓
                          </a>
                        </div>
                      </div>
                    </div>
                    <div className="photo-meta">
                      <span className="score-bar-wrap">
                        <span
                          className="score-bar-fill"
                          style={{ width: `${Math.round(r.score * 100)}%` }}
                        />
                      </span>
                      <div className="score-row">
                        <span className="score-value">{Math.round(r.score * 100)}%</span>
                        <span className={`score-tag tag-${scoreLabel(r.score)}`}>
                          {scoreLabel(r.score)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </main>

      <footer className="footer">
        <span>FACEMATCH · POWERED BY YOUR BACKEND</span>
      </footer>
    </div>
  );
}