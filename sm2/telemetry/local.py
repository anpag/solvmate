import json
from datetime import datetime
from sm2.telemetry.base import BaseTracker

class LocalTracker(BaseTracker):
    def log_event(self, request, solute_smiles, solvents, results, event_type, model_metadata=None):
        event_payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "scientist_email": "local_dev_user",
            "target_molecule_smiles": solute_smiles,
            "tested_solvents": solvents,
            "event_type": event_type,
            "results": json.dumps(results),
            "model_metadata": model_metadata or {}
        }
        print("====== [LOCAL TELEMETRY EVENT] ======")
        print(json.dumps(event_payload, indent=2))
        print("=====================================")
