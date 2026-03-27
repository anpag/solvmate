let currentConfig = {};

async function fetchSettings() {
    try {
        const response = await fetch('/config');
        currentConfig = await response.json();
        
        document.getElementById('telemetryProvider').value = currentConfig.telemetry.provider || 'local';
        document.getElementById('mlopsProvider').value = currentConfig.mlops.provider || 'local';
    } catch (error) {
        console.error("Error fetching config:", error);
    }
}

function showSettingsModal() {
    fetchSettings();
    document.getElementById('settingsModal').style.display = 'block';
}

function hideSettingsModal() {
    document.getElementById('settingsModal').style.display = 'none';
}

async function saveSettings() {
    const telemetryProvider = document.getElementById('telemetryProvider').value;
    const mlopsProvider = document.getElementById('mlopsProvider').value;

    currentConfig.telemetry.provider = telemetryProvider;
    currentConfig.mlops.provider = mlopsProvider;

    try {
        const response = await fetch('/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentConfig)
        });

        if (response.ok) {
            alert("Settings saved successfully! The backend has been reinitialized.");
            hideSettingsModal();
        } else {
            alert("Failed to save settings.");
        }
    } catch (error) {
        console.error("Error saving config:", error);
        alert("Error saving settings.");
    }
}
