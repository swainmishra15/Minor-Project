import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles.css"; // your custom CSS file for dashboard styling

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
