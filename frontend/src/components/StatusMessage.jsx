export function StatusMessage({ status }) {
  if (!status) return null;
  return (
    <div className={`status-msg status-${status.type}`}>
      <span className="status-icon">
        {status.type === "success" && "✓"}
        {status.type === "error" && "✕"}
        {status.type === "loading" && <span className="dot-pulse" />}
      </span>
      <span>{status.text}</span>
    </div>
  );
}