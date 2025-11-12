// ============================================
// File 3: src/components/LogsTable.jsx
// ============================================
import React from "react";

export default function LogsTable({ logs, loading }) {
  return (
    <section className="logs-section" style={{ margin: "20px", padding: "20px", background: "#fff", borderRadius: "12px", boxShadow: "0 4px 10px rgba(0, 0, 0, 0.05)" }}>
      <div className="logs-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
        <h2 style={{ margin: 0 }}>Recent Logs</h2>
        <button
          style={{
            padding: "8px 16px",
            background: "#3498db",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Refresh
        </button>
      </div>

      {loading ? (
        <div style={{ textAlign: "center", padding: "20px" }}>Loading logs...</div>
      ) : logs.length === 0 ? (
        <div style={{ textAlign: "center", padding: "20px" }}>No logs found.</div>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #ddd", background: "#f9f9f9" }}>
              <th style={{ textAlign: "left", padding: "12px", fontWeight: "bold", color: "#333" }}>ID</th>
              <th style={{ textAlign: "left", padding: "12px", fontWeight: "bold", color: "#333" }}>Timestamp</th>
              <th style={{ textAlign: "left", padding: "12px", fontWeight: "bold", color: "#333" }}>Message</th>
              <th style={{ textAlign: "left", padding: "12px", fontWeight: "bold", color: "#333" }}>Source</th>
              <th style={{ textAlign: "left", padding: "12px", fontWeight: "bold", color: "#333" }}>Classification</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} style={{ borderBottom: "1px solid #eee", hover: { background: "#f5f5f5" } }}>
                <td style={{ padding: "12px", color: "#555" }}>#{log.id}</td>
                <td style={{ padding: "12px", color: "#555" }}>
                  {new Date(log.timestamp).toLocaleString()}
                </td>
                <td style={{ padding: "12px", color: "#555" }}>{log.message}</td>
                <td style={{ padding: "12px", color: "#555" }}>{log.source}</td>
                <td style={{ padding: "12px" }}>
                  <span
                    style={{
                      padding: "6px 12px",
                      borderRadius: "4px",
                      background:
                        log.classification === "error"
                          ? "#e74c3c"
                          : log.classification === "warning"
                          ? "#f39c12"
                          : log.classification === "info"
                          ? "#3498db"
                          : log.classification === "security"
                          ? "#e91e63"
                          : log.classification === "performance"
                          ? "#d2b3ebff"
                          : "#9b59b6",
                      color: "white",
                      fontSize: "0.85rem",
                      fontWeight: "bold",
                    }}
                  >
                    {log.classification?.toUpperCase() || "OTHER"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}