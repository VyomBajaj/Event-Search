import { useState } from "react";
import { uploadImage, getPhotos } from "../utils/api";

export default function UploadForm({ setResults, setSubmitted }) {
  const [eventName, setEventName] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!eventName.trim()) return setError("Event name is required.");
    if (!file) return setError("Please select an image.");

    setLoading(true);
    setError("");

    try {
      const uploadData = await uploadImage(file, eventName);
      const matchData = await getPhotos(eventName, uploadData.filename);

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
        <input
          value={eventName}
          onChange={(e) => setEventName(e.target.value)}
          placeholder="Event name"
        />

        <input type="file" onChange={(e) => setFile(e.target.files[0])} />

        {error && <p>{error}</p>}

        <button onClick={handleSubmit}>
          {loading ? "Scanning..." : "Find My Photos"}
        </button>
      </div>
    </div>
  );
}