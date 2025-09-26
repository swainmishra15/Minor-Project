// API Base URL - your backend
const API_BASE = 'http://127.0.0.1:8000';

// Track user interactions and send to monitoring system
function trackClick(action) {
    console.log(`User clicked: ${action}`);
    
    // Send tracking data to your monitoring API
    fetch(`${API_BASE}/logs/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: `User interaction: ${action} clicked`,
            source: 'website_frontend'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Tracked:', data);
        updateStats();
    })
    .catch(error => console.error('Tracking error:', error));
}

// Generate test traffic
function generateTraffic() {
    console.log('Generating test traffic...');
    
    const actions = [
        'cloud-services',
        'ai-ml', 
        'monitoring',
        'enterprise',
        'page-view',
        'api-call'
    ];
    
    // Generate 10 random actions
    for (let i = 0; i < 10; i++) {
        setTimeout(() => {
            const randomAction = actions[Math.floor(Math.random() * actions.length)];
            trackClick(randomAction);
        }, i * 500); // 500ms delay between each
    }
}

// Test API connection
function testAPI() {
    console.log('Testing API connection...');
    
    fetch(`${API_BASE}/logs/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: 'API test from frontend',
            source: 'api_test'
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('API Connection Successful! ✅');
        console.log('API Response:', data);
    })
    .catch(error => {
        alert('API Connection Failed! ❌');
        console.error('API Error:', error);
    });
}

// Load dashboard
function loadDashboard() {
    // For now, just track the click
    trackClick('dashboard-access');
    alert('Dashboard will be implemented next! 📊');
}

// Update live stats from backend
function updateStats() {
    fetch(`${API_BASE}/logs/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalLogs').textContent = data.count || 0;
            
            // Calculate error rate (mock calculation)
            const errorRate = Math.floor(Math.random() * 5); // 0-5%
            document.getElementById('errorRate').textContent = `${errorRate}%`;
            
            // Mock response time
            const responseTime = Math.floor(Math.random() * 200) + 50; // 50-250ms
            document.getElementById('responseTime').textContent = `${responseTime}ms`;
        })
        .catch(error => {
            console.error('Stats update failed:', error);
        });
}

// Auto-update stats every 10 seconds
setInterval(updateStats, 10000);

// Initial stats load
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    console.log('TechCorp website loaded! 🚀');
});

// Track page views automatically
window.addEventListener('load', () => {
    trackClick('page-view-home');
});
