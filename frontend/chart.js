// Function to fetch metrics data from the FastAPI backend and update the chart
async function fetchAndRenderMetrics() {
    try {
        const response = await fetch('http://127.0.0.1:8000/metrics/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const metrics = await response.json();

        // Assuming metrics data is an array of objects like:
        // [{ "timestamp": "...", "name": "...", "value": 123 }]
        const labels = metrics.map(m => new Date(m.timestamp).toLocaleTimeString());
        const data = metrics.map(m => m.value);

        const metricsData = {
            labels: labels,
            datasets: [{
                label: 'Metrics Value',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };

        const config = {
            type: 'bar',
            data: metricsData,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            },
        };

        const metricsChart = new Chart(
            document.getElementById('metricsChart'),
            config
        );

    } catch (error) {
        console.error('Could not fetch metrics:', error);
    }
}

// Function to fetch log data from the FastAPI backend and populate the list
async function fetchAndRenderLogs() {
    try {
        const response = await fetch('http://127.0.0.1:8000/logs/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const logs = await response.json();
        const logList = document.getElementById('log-list');
        logList.innerHTML = ''; // Clear previous logs

        // Assuming logs data is an array of objects like:
        // [{ "timestamp": "...", "message": "...", "source": "..." }]
        logs.forEach(log => {
            const li = document.createElement('li');
            li.textContent = `[${log.timestamp}] [${log.source}] ${log.message}`;
            logList.appendChild(li);
        });

    } catch (error) {
        console.error('Could not fetch logs:', error);
    }
}

// Call the functions to fetch and render data when the page loads
fetchAndRenderMetrics();
fetchAndRenderLogs();

// Optional: You can set an interval to refresh the data periodically
// setInterval(fetchAndRenderMetrics, 5000); // Refresh every 5 seconds
// setInterval(fetchAndRenderLogs, 5000); // Refresh every 5 seconds