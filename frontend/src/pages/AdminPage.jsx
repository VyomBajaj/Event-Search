import "../AdminPage.css";
import Navbar from "../components/Navbar";
import { CreateEventCard } from "../components/CreateEventCard";
import { UploadZipCard } from "../components/UploadZipCard";

export default function AdminPage() {
  return (
    <div className="admin-app">
      <Navbar />
      <main className="admin-main">
        <div className="page-intro">
          <h1 className="page-heading">Event Management</h1>
          <p className="page-sub">Create events and upload photo collections for face recognition indexing.</p>
        </div>

        <div className="cards-stack">
          <CreateEventCard />
          <UploadZipCard />
        </div>
      </main>

      <footer className="admin-footer">
        FACEMATCH · ADMIN INTERFACE · INTERNAL USE ONLY
      </footer>
    </div>
  );
}