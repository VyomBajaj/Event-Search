import { useState } from "react";
const BASE_URL = import.meta.env.VITE_BACKEND_URL;
const UPLOAD_URL = `${BASE_URL}/user/upload`;
const GET_PHOTOS_URL = `${BASE_URL}/user/getPhotos`;

export default function FormCard({ setResults, setSubmitted }) {
  const [eventName, setEventName] = useState("");
  const [error, setError] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
  };

  const handleSubmit = async () => {
    if (!eventName.trim()) return setError("Event name is required.");
    if (!file) return setError("Please select an image.");

    setLoading(true);
    setError("");
    setSubmitted(false);

    try {
      // Upload
      const uploadForm = new FormData();
      uploadForm.append("file", file);
      uploadForm.append("event", eventName.trim());

      const uploadRes = await fetch(UPLOAD_URL, {
        method: "POST",
        body: uploadForm,
      });

      if (!uploadRes.ok) throw new Error("Upload failed");

      const uploadData = await uploadRes.json();
      console.log(uploadData);
      const eventId = uploadData.event_id;
      const imageUrl = uploadData.image_url;

// Match
      const matchForm = new FormData();

      matchForm.append("event_id", eventId);

      matchForm.append("image_url", imageUrl);
      

      const matchRes = await fetch(GET_PHOTOS_URL, {
        method: "POST",
        body: matchForm,
      });

      if (!matchRes.ok) throw new Error("Matching failed");

      const matchData = await matchRes.json();

      setResults(matchData.results || []);
      setSubmitted(true);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
          <div className="card-inner">
            <div className="field-group">
              <label className="field-label">EVENT NAME</label>
              <input
                className="field-input"
                type="text"
                placeholder="e.g. annual_meet_2025"
                value={eventName}
                onChange={(e) => { setEventName(e.target.value); setError(""); }}
              />
            </div>
 
            <div className="field-group">
              <label className="field-label">YOUR PHOTO</label>
              <label className="file-drop">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  style={{ display: "none" }}
                />
                <span className="file-icon">↑</span>
                <span className="file-text">
                  {file ? file.name : "Click to upload an image"}
                </span>
                {file && (
                  <span className="file-meta">
                    {(file.size / 1024).toFixed(1)} KB
                  </span>
                )}
              </label>
            </div>
 
            {error && (
              <div className="error-bar">
                <span className="error-dot">!</span>
                {error}
              </div>
            )}
 
            <button
              className={`submit-btn ${loading ? "loading" : ""}`}
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? (
                <span className="spinner-row">
                  <span className="spinner" />
                  Scanning…
                </span>
              ) : (
                "Find My Photos →"
              )}
            </button>
          </div>
        </div>
  );
}