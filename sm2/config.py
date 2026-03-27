import json
import os
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "telemetry": {
        "provider": "local", 
        "project_id": "gsk-lab-of-the-future",
        "topic_name": "lotf-solvmate-events"
    },
    "mlops": {
        "provider": "local", 
        "project_id": "gsk-lab-of-the-future",
        "model_name": "solvmate-recommender"
    }
}

def load_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config, using defaults: {e}")
        return DEFAULT_CONFIG

def save_config(config_dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_dict, f, indent=4)
