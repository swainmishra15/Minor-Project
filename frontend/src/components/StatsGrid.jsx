// ============================================
// File 2: src/components/StatsGrid.jsx
// ============================================
import React from "react";

export default function StatsGrid({ stats }) {
  const styles = {
    container: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
      gap: "20px",
      margin: "20px",
      textAlign: "center",
    },
    card: {
      background: "#fff",
      padding: "20px",
      borderRadius: "12px",
      boxShadow: "0 4px 10px rgba(0, 0, 0, 0.05)",
      borderTop: "5px solid #ccc",
      transition: "transform 0.2s ease, box-shadow 0.2s ease",
    },
    number: {
      fontSize: "2rem",
      fontWeight: "bold",
      marginBottom: "5px",
    },
    label: {
      fontSize: "1rem",
      color: "#555",
    },
  };

  return (
    <section className="stats" style={styles.container}>
      <div style={{ ...styles.card, borderTopColor: "#e74c3c" }}>
        <div style={{ ...styles.number, color: "#e74c3c" }}>
          {stats.error || 0}
        </div>
        <div style={styles.label}>Errors</div>
      </div>

      <div style={{ ...styles.card, borderTopColor: "#f39c12" }}>
        <div style={{ ...styles.number, color: "#f39c12" }}>
          {stats.warning || 0}
        </div>
        <div style={styles.label}>Warnings</div>
      </div>

      <div style={{ ...styles.card, borderTopColor: "#3498db" }}>
        <div style={{ ...styles.number, color: "#3498db" }}>
          {stats.info || 0}
        </div>
        <div style={styles.label}>Info</div>
      </div>

      <div style={{ ...styles.card, borderTopColor: "#e91e63" }}>
        <div style={{ ...styles.number, color: "#e91e63" }}>
          {stats.security || 0}
        </div>
        <div style={styles.label}>Security</div>
      </div>

      <div style={{ ...styles.card, borderTopColor: "#ff9800" }}>
        <div style={{ ...styles.number, color: "#ff9800" }}>
          {stats.performance || 0}
        </div>
        <div style={styles.label}>Performance</div>
      </div>

      <div style={{ ...styles.card, borderTopColor: "#9b59b6" }}>
        <div style={{ ...styles.number, color: "#9b59b6" }}>
          {stats.other || 0}
        </div>
        <div style={styles.label}>Other</div>
      </div>

      <div style={{ ...styles.card, borderTopColor: "#95a5a6" }}>
        <div style={{ ...styles.number, color: "#95a5a6" }}>
          {stats.total || 0}
        </div>
        <div style={styles.label}>Total Logs</div>
      </div>
    </section>
  );
}