// ============================================
// File 1: src/App.js
// ============================================
import React, { useEffect, useState } from "react";
import StatsGrid from "./components/StatsGrid";
import LogsTable from "./components/LogsTable";
import ChartsSection from "./components/ChartsSection";
import "./styles.css";

export default function App() {
  const [stats, setStats] = useState({
    error: 0,
    warning: 0,
    info: 0,
    other: 0,
    security: 0,
    performance: 0,
    total: 0,
  });
  const [logs, setLogs] = useState([]);
  const [chartData, setChartData] = useState({
    labels: [],
    trendData: [],
    sourceLabels: [],
    sourceData: [],
  });
  const [loading, setLoading] = useState(false);
  const [chartsInitialized, setChartsInitialized] = useState(false);

  const API_BASE = "http://127.0.0.1:8000";

  // Calculate stats from logs
  const calculateStatsFromLogs = (logsList) => {
    const statsObj = { error: 0, warning: 0, info: 0, other: 0, security: 0, performance: 0 };
    const sources = {};

    logsList.forEach((log) => {
      const classification = log.classification || "other";
      const source = log.source || "unknown";

      // Map classifications to categories
      if (classification === "security") {
        statsObj.security += 1;
      } else if (classification === "performance") {
        statsObj.performance += 1;
      } else {
        statsObj[classification] = (statsObj[classification] || 0) + 1;
      }

      sources[source] = (sources[source] || 0) + 1;
    });

    return {
      ...statsObj,
      total: logsList.length,
      sources,
    };
  };

  // Fetch all data
  const fetchAllData = async () => {
    try {
      const logsRes = await fetch(`${API_BASE}/logs/`);
      const logsData = await logsRes.json();

      if (logsData.logs && logsData.logs.length > 0) {
        setLogs(logsData.logs);

        const calculatedStats = calculateStatsFromLogs(logsData.logs);
        setStats(calculatedStats);

        setChartData((prevData) => {
          const sourceLabels = Object.keys(calculatedStats.sources);
          const sourceData = Object.values(calculatedStats.sources);
          const now = new Date().toLocaleTimeString();

          if (!chartsInitialized) {
            return {
              labels: [now],
              trendData: [logsData.logs.length],
              sourceLabels,
              sourceData,
            };
          }

          let newLabels = [...prevData.labels, now];
          let newTrendData = [...prevData.trendData, logsData.logs.length];

          if (newLabels.length > 10) {
            newLabels = newLabels.slice(-10);
            newTrendData = newTrendData.slice(-10);
          }

          return {
            labels: newLabels,
            trendData: newTrendData,
            sourceLabels,
            sourceData,
          };
        });

        if (!chartsInitialized) {
          setChartsInitialized(true);
        }
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 5000);
    return () => clearInterval(interval);
  }, [chartsInitialized]);

  return (
    <div className="container">
      <header className="header">
        <h1>Log Monitoring Dashboard</h1>
      </header>

      <StatsGrid stats={stats} />
      <ChartsSection
        logs={logs}
        chartData={chartData}
        stats={stats}
        chartsInitialized={chartsInitialized}
      />
      <LogsTable logs={logs} loading={loading} />
    </div>
  );
}