import "../AdminPage.css";
import Navbar from "../components/Navbar";
import { CreateEventCard } from "../components/CreateEventCard";
import { UploadZipCard } from "../components/UploadZipCard";
import { useState } from "react";

export default function AdminPage() {
  const [selectedEvent, setSelectedEvent] = useState(null);
  return (
    <div className="admin-app">
      <Navbar />
      <main className="admin-main">
        <div className="page-intro">
          <h1 className="page-heading">Event Management</h1>
          <p className="page-sub">Create events and upload photo collections for face recognition indexing.</p>
        </div>

        <div className="cards-stack">
          <CreateEventCard
  setSelectedEvent={setSelectedEvent}
/>
          <UploadZipCard
  selectedEvent={selectedEvent}
/>
        </div>
      </main>

      <footer className="admin-footer">
        FACEMATCH · ADMIN INTERFACE · INTERNAL USE ONLY
      </footer>
    </div>
  );
}