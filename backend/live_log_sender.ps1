# Live Log Sender Script
# Continuously fetches logs from Mockaroo and sends them to FastAPI backend

$apiKey = "13eb01e0"
$mockarooUrl = "https://api.mockaroo.com/api/ab461960?count=5&key=$apiKey"
$backendUrl = "http://127.0.0.1:8000/logs/"  # Change IP if backend runs elsewhere

# Define random log sources
$sources = @("api", "auth", "database", "backend", "frontend", "system", "monitor")

Write-Host "🚀 Starting live log stream from Mockaroo to FastAPI..."
Write-Host "📡 Backend endpoint: $backendUrl"
Write-Host "--------------------------------------------"
Write-Host ""

while ($true) {
    try {
        # Fetch a small batch of fake logs
        $logs = Invoke-RestMethod -Uri $mockarooUrl

        foreach ($log in $logs) {
            # Pick a random source
            $source = Get-Random -InputObject $sources

            # Build final JSON payload with message + source
            $payload = @{
                message = $log.message
                source  = $source
            } | ConvertTo-Json -Compress

            # Send to FastAPI backend
            Write-Host "📤 Sending: $($log.message)"
            Invoke-RestMethod -Uri $backendUrl -Method Post -Body $payload -ContentType "application/json" | Out-Null

            Start-Sleep -Seconds 1  # Wait 1 second between each log
        }

        Write-Host ""
        Write-Host "⏳ Waiting 5 seconds for next batch..."
        Write-Host ""
        Start-Sleep -Seconds 5
    }
    catch {
        Write-Host "❌ Error sending logs: $_"
        Start-Sleep -Seconds 10
    }
}
