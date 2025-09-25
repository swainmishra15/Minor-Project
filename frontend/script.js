// API endpoint
const API_URL = 'http://127.0.0.1:8000/logs/';

// Load logs from API
async function loadLogs() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('logTable').style.display = 'none';

    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        if (data.logs) {
            displayLogs(data.logs);
            updateStats(data.logs);
            document.getElementById('lastUpdated').textContent = 
                `Last updated: ${new Date().toLocaleString()}`;
        } else {
            console.error('No logs data received');
        }
    } catch (error) {
        console.error('Error loading logs:', error);
        document.getElementById('loading').textContent = 'Error loading logs. Make sure your API is running!';
    }
}

// Display logs in table
function displayLogs(logs) {
    const tbody = document.getElementById('logTableBody');
    tbody.innerHTML = '';

    logs.forEach(log => {
        const row = document.createElement('tr');
        row.className = 'log-row';
        
        const formattedTime = new Date(log.timestamp).toLocaleString();
        
        row.innerHTML = `
            <td>#${log.id}</td>
            <td>${formattedTime}</td>
            <td>${log.message}</td>
            <td>${log.source}</td>
            <td>
                <span class="classification-badge badge-${log.classification}">
                    ${log.classification.toUpperCase()}
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });

    document.getElementById('loading').style.display = 'none';
    document.getElementById('logTable').style.display = 'table';
}

// Update statistics
function updateStats(logs) {
    const stats = {
        error: 0,
        warning: 0,
        info: 0,
        other: 0
    };

    logs.forEach(log => {
        stats[log.classification] = (stats[log.classification] || 0) + 1;
    });

    document.getElementById('errorCount').textContent = stats.error || 0;
    document.getElementById('warningCount').textContent = stats.warning || 0;
    document.getElementById('infoCount').textContent = stats.info || 0;
    document.getElementById('totalCount').textContent = logs.length;
}

// Auto-refresh every 5 seconds
function startAutoRefresh() {
    setInterval(loadLogs, 5000);
}

// Load logs when page loads
window.addEventListener('load', () => {
    loadLogs();
    startAutoRefresh();
});

// Make refresh button work
window.loadLogs = loadLogs;
