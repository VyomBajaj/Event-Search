import { useState } from "react";
import { StatusMessage } from "./StatusMessage";
const BASE_URL = import.meta.env.VITE_BACKEND_URL;
const UPLOAD_FOLDER_URL = `${BASE_URL}/admin/upload-folder`;
export function UploadZipCard({
  selectedEvent
}) {
  const [zipFile, setZipFile] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!selectedEvent) {

      setStatus({
        type: "error",
        text: "Please create/select an event first."
      });

      return;
    }
    if (!zipFile) {
      setStatus({ type: "error", text: "Please select a ZIP file." });
      return;
    }
    if (!zipFile.name.endsWith(".zip")) {
      setStatus({ type: "error", text: "Only .zip files are accepted." });
      return;
    }

    setLoading(true);
    setStatus({ type: "loading", text: "Uploading ZIP file…" });

    try {
      const form = new FormData();
      form.append(
        "event_id",
        selectedEvent.event_id
      );
      form.append("zip_file", zipFile);

      // Simulate processing stage after a moment
      const uploadPromise = fetch(UPLOAD_FOLDER_URL, { method: "POST", body: form });

      // Show "Processing embeddings…" after 1.5s if still loading
      const processingTimer = setTimeout(() => {
        setStatus({ type: "loading", text: "Processing embeddings… this may take a moment." });
      }, 1500);

      const res = await uploadPromise;
      clearTimeout(processingTimer);

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed.");

      setStatus({ type: "success", text: data.message || "Images uploaded and embeddings created successfully." });
      setZipFile(null);
      // Reset file input visually
      const fileInput = document.getElementById("zip-file-input");
      if (fileInput) fileInput.value = "";
    } catch (err) {
      setStatus({ type: "error", text: err.message || "Something went wrong." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel-card">
      <div className="card-header">
        <span className="card-index">02</span>
        <div>
          <h2 className="card-title">Upload ZIP Folder</h2>
          <p className="card-sub">Upload a .zip of event photos. Embeddings will be generated automatically.</p>
        </div>
      </div>

      <div className="card-body">
        <div className="field-group">

          <label className="field-label">
            SELECTED EVENT
          </label>

          <div className="selected-event-box">

            {selectedEvent ? (
              <>
                <span>
                  {selectedEvent.event_name}
                </span>
              </>
            ) : (
              <span>
                No event selected
              </span>
            )}

          </div>

        </div>

        <div className="field-group">
          <label className="field-label">ZIP FILE</label>
          <label className="file-drop">
            <input
              id="zip-file-input"
              type="file"
              accept=".zip"
              style={{ display: "none" }}
              onChange={(e) => { setZipFile(e.target.files[0]); setStatus(null); }}
            />
            <span className="file-icon">⬆</span>
            <span className="file-text">
              {zipFile ? zipFile.name : "Click to select a .zip file"}
            </span>
            {zipFile && (
              <span className="file-meta">{(zipFile.size / (1024 * 1024)).toFixed(2)} MB</span>
            )}
          </label>
        </div>

        <button
          className="action-btn"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? (
            <span className="spinner-row">
              <span className="spinner" />
              Processing…
            </span>
          ) : (
            "Upload & Process"
          )}
        </button>
        <StatusMessage status={status} />
      </div>
    </div>
  );
}