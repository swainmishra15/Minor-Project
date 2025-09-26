// API endpoint
const API_URL = 'http://127.0.0.1:8000/logs/';

// Chart variables
let lineChart, doughnutChart, barChart;

// Initialize Charts
function initCharts() {
    // Line Chart
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Total Logs',
                data: [],
                borderColor: '#3498db',
                backgroundColor: 'rgba(52,152,219,0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#333' }
                },
                x: {
                    ticks: { color: '#333' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#333' }
                }
            }
        }
    });

    // Doughnut Chart
    const doughnutCtx = document.getElementById('doughnutChart').getContext('2d');
    doughnutChart = new Chart(doughnutCtx, {
        type: 'doughnut',
        data: {
            labels: ['Error', 'Warning', 'Info', 'Other'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: ['#e74c3c', '#f39c12', '#3498db', '#9b59b6'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#333' }
                }
            }
        }
    });

    // Bar Chart
    const barCtx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Logs per Source',
                data: [],
                backgroundColor: '#3498db',
                borderColor: '#2980b9',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#333' }
                },
                x: {
                    ticks: { color: '#333' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#333' }
                }
            }
        }
    });
}

// Load Logs from API
async function loadLogs() {
    console.log('🔄 Loading logs from API...');
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('logTable').style.display = 'none';

    try {
        const response = await fetch(API_URL);
        console.log('📡 API Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('📊 API Data received:', data);

        if (data.logs && data.logs.length > 0) {
            console.log(`✅ Found ${data.logs.length} logs`);
            displayLogs(data.logs);
            updateStats(data.logs);
            updateCharts(data.logs);
            
            // Update last updated time
            document.getElementById('lastUpdated').textContent = `Last updated: ${new Date().toLocaleString()}`;
        } else {
            console.warn('⚠️ No logs found in response');
            document.getElementById('loading').textContent = 'No logs found. Try generating some logs first!';
        }

    } catch (error) {
        console.error('❌ Error loading logs:', error);
        document.getElementById('loading').textContent = `Error: ${error.message}. Make sure API is running on port 8000!`;
    }
}

// Display Logs in Table
function displayLogs(logs) {
    console.log('📋 Displaying logs in table...');
    
    const tbody = document.getElementById('logTableBody');
    tbody.innerHTML = '';

    logs.forEach((log, index) => {
        const row = document.createElement('tr');
        row.className = 'log-row';
        
        // Format timestamp
        const formattedTime = new Date(log.timestamp).toLocaleString();
        
        row.innerHTML = `
            <td>#${log.id || index + 1}</td>
            <td>${formattedTime}</td>
            <td>${log.message || 'N/A'}</td>
            <td>${log.source || 'unknown'}</td>
            <td><span class="classification-badge badge-${log.classification}">${(log.classification || 'other').toUpperCase()}</span></td>
        `;
        
        tbody.appendChild(row);
    });

    // Hide loading and show table
    document.getElementById('loading').style.display = 'none';
    document.getElementById('logTable').style.display = 'table';
    
    console.log('✅ Table updated successfully');
}

// Update Statistics
function updateStats(logs) {
    console.log('📈 Updating statistics...');
    
    const stats = { error: 0, warning: 0, info: 0, other: 0 };
    const sources = {};

    logs.forEach(log => {
        const classification = log.classification || 'other';
        const source = log.source || 'unknown';
        
        stats[classification] = (stats[classification] || 0) + 1;
        sources[source] = (sources[source] || 0) + 1;
    });

    // Update stat cards
    document.getElementById('errorCount').textContent = stats.error;
    document.getElementById('warningCount').textContent = stats.warning;
    document.getElementById('infoCount').textContent = stats.info;
    document.getElementById('totalCount').textContent = logs.length;

    // Update doughnut chart
    doughnutChart.data.datasets[0].data = [stats.error, stats.warning, stats.info, stats.other];
    doughnutChart.update();

    // Update bar chart
    const sourceLabels = Object.keys(sources);
    const sourceData = Object.values(sources);
    
    barChart.data.labels = sourceLabels;
    barChart.data.datasets[0].data = sourceData;
    barChart.update();
    
    console.log('✅ Stats updated:', stats);
}

// Update Line Chart
function updateCharts(logs) {
    const now = new Date().toLocaleTimeString();
    
    lineChart.data.labels.push(now);
    lineChart.data.datasets[0].data.push(logs.length);
    
    // Keep only last 10 data points
    if (lineChart.data.labels.length > 10) {
        lineChart.data.labels.shift();
        lineChart.data.datasets[0].data.shift();
    }
    
    lineChart.update();
}

// Auto refresh
function startAutoRefresh() {
    setInterval(() => {
        console.log('🔄 Auto-refreshing logs...');
        loadLogs();
    }, 5000); // Refresh every 5 seconds
}

// Manual refresh button
function refreshLogs() {
    console.log('🔄 Manual refresh triggered...');
    loadLogs();
}

// Initialize everything
window.addEventListener('load', () => {
    console.log('🚀 Dashboard loading...');
    console.log('📡 API URL:', API_URL);
    
    // Initialize charts
    initCharts();
    
    // Load initial data
    loadLogs();
    
    // Start auto refresh
    startAutoRefresh();
    
    console.log('✅ Dashboard initialized');
});

// Make functions available globally
window.loadLogs = loadLogs;
window.refreshLogs = refreshLogs;
