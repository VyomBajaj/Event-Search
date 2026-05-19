import { useState } from "react";
import { StatusMessage } from "./StatusMessage";
const BASE_URL = import.meta.env.VITE_BACKEND_URL;
const CREATE_EVENT_URL = `${BASE_URL}/admin/create-event`;
export function CreateEventCard({
  setSelectedEvent
}) {
  const [eventName, setEventName] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    if (!eventName.trim()) {
      setStatus({ type: "error", text: "Event name cannot be empty." });
      return;
    }

    setLoading(true);
    setStatus({ type: "loading", text: "Creating event…" });

    try {
      const form = new FormData();
      form.append("event", eventName.trim());

      const res = await fetch(CREATE_EVENT_URL, { method: "POST", body: form });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Request failed.");

      setSelectedEvent({
        event_id: data.event_id,
        event_name: eventName.trim()
      });

      setStatus({
        type: "success",
        text: data.message || "Event created successfully."
      });

      setEventName("");
    } catch (err) {
      setStatus({ type: "error", text: err.message || "Something went wrong." });
    } finally {
      setLoading(false);
    }
  };

  return (

    <div className="panel-card">

      <div className="card-header">
        <span className="card-index">01</span>
        <div>
          <h2 className="card-title">Create Event</h2>
          <p className="card-sub">Register a new event to group photos under.</p>
        </div>
      </div>

      <div className="card-body">
        <div className="field-group">
          <label className="field-label">EVENT NAME</label>
          <input
            className="field-input"
            type="text"
            placeholder="e.g. annual_meet_2025"
            value={eventName}
            onChange={(e) => { setEventName(e.target.value); setStatus(null); }}
            onKeyDown={(e) => e.key === "Enter" && handleCreate()}
          />
        </div>
        <button
          className="action-btn"
          onClick={handleCreate}
          disabled={loading}
        >
          {loading ? "Creating…" : "Create Event"}
        </button>
        <StatusMessage status={status} />
      </div>
    </div>
  );
}