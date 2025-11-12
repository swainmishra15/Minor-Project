// ============================================
// File 4: src/components/ChartsSection.jsx
// ============================================
import React from "react";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  ArcElement,
  BarElement,
  Legend,
  Tooltip,
} from "chart.js";
import { Line, Doughnut, Bar } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  ArcElement,
  BarElement,
  Legend,
  Tooltip
);

export default function ChartsSection({
  chartData,
  stats,
  chartsInitialized,
}) {
  // Line chart data
  const lineData = {
    labels: chartData.labels && chartData.labels.length > 0 ? chartData.labels : ["Waiting for data..."],
    datasets: [
      {
        label: "Total Logs (Last 10 intervals)",
        data: chartData.trendData && chartData.trendData.length > 0 ? chartData.trendData : [0],
        borderColor: "#3498db",
        backgroundColor: "rgba(52,152,219,0.1)",
        fill: true,
        tension: 0.4,
        pointRadius: 6,
        pointBackgroundColor: "#3498db",
        pointBorderColor: "#2980b9",
        pointBorderWidth: 2,
        borderWidth: 3,
      },
    ],
  };

  // Doughnut chart with 6 categories
  const doughnutData = {
    labels: ["Error", "Warning", "Info", "Security", "Performance", "Other"],
    datasets: [
      {
        data: [stats.error, stats.warning, stats.info, stats.security, stats.performance, stats.other],
        backgroundColor: ["#e74c3c", "#f39c12", "#3498db", "#e91e63", "#d2b3ebff", "#9b59b6"],
        borderWidth: 2,
        borderColor: "#fff",
      },
    ],
  };

  // Bar chart data
  const barData = {
    labels: chartData.sourceLabels && chartData.sourceLabels.length > 0 ? chartData.sourceLabels : ["No sources"],
    datasets: [
      {
        label: "Logs per Source",
        data: chartData.sourceData && chartData.sourceData.length > 0 ? chartData.sourceData : [0],
        backgroundColor: "#3498db",
        borderColor: "#2980b9",
        borderWidth: 2,
        borderRadius: 5,
      },
    ],
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 0,
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
    plugins: { 
      legend: { 
        labels: { color: "#333", font: { size: 12, weight: 'bold' } } 
      },
      filler: {
        propagate: true,
      }
    },
    scales: {
      x: { 
        ticks: { color: "#333", font: { size: 11 } },
        grid: { color: "rgba(0, 0, 0, 0.1)", drawBorder: true }
      },
      y: { 
        beginAtZero: true, 
        ticks: { color: "#333", font: { size: 11 }, stepSize: 1 },
        grid: { color: "rgba(0, 0, 0, 0.1)" }
      },
    },
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 0,
    },
    plugins: { 
      legend: { 
        labels: { color: "#333", font: { size: 12, weight: 'bold' } } 
      } 
    },
    scales: {
      x: { 
        ticks: { color: "#333", font: { size: 11 } },
        grid: { color: "rgba(0, 0, 0, 0.05)" }
      },
      y: { 
        beginAtZero: true, 
        ticks: { color: "#333", font: { size: 11 }, stepSize: 1 },
        grid: { color: "rgba(0, 0, 0, 0.1)" }
      },
    },
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 0,
    },
    plugins: { 
      legend: { 
        position: 'bottom',
        labels: { color: "#333", font: { size: 12, weight: 'bold' }, padding: 15 } 
      } 
    },
  };

  return (
    <section className="charts" style={{ padding: "20px" }}>
      <div style={{ 
        marginBottom: "20px", 
        background: "#fff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 4px 10px rgba(0, 0, 0, 0.05)"
      }}>
        <h2 style={{ marginTop: 0, color: "#333" }}>📈 Logs Trend (Real-Time)</h2>
        <div style={{ height: "350px", position: "relative" }}>
          <Line data={lineData} options={lineOptions} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
        <div style={{ 
          background: "#fff",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.05)"
        }}>
          <h2 style={{ marginTop: 0, color: "#333" }}>🧩 Log Classification Breakdown</h2>
          <div style={{ height: "350px", position: "relative" }}>
            <Doughnut data={doughnutData} options={doughnutOptions} />
          </div>
        </div>

        <div style={{ 
          background: "#fff",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.05)"
        }}>
          <h2 style={{ marginTop: 0, color: "#333" }}>🌐 Logs per Source</h2>
          <div style={{ height: "350px", position: "relative" }}>
            <Bar data={barData} options={barOptions} />
          </div>
        </div>
      </div>
    </section>
  );
}