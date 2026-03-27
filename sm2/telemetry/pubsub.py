import base64
import json
from datetime import datetime
from google.cloud import pubsub_v1
from sm2.telemetry.base import BaseTracker

class PubSubTracker(BaseTracker):
    def __init__(self, project_id, topic_name):
        self.project_id = project_id
        self.topic_name = topic_name
        self.publisher = None
        self.topic_path = None
        
        try:
            self.publisher = pubsub_v1.PublisherClient()
            self.topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
            print(f"Successfully initialized Pub/Sub client for {self.topic_path}")
        except Exception as e:
            print(f"Failed to initialize Pub/Sub client. Events will not be logged. Error: {e}")

    def _extract_user_identity(self, request) -> str:
        """Extracts email from IAP headers or the Authorization Bearer token."""
        iap_header = request.headers.get("X-Goog-Authenticated-User-Email")
        if iap_header: return iap_header.replace("accounts.google.com:", "")
        
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload_b64 = token.split(".")[1]
                payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
                decoded_payload = base64.b64decode(payload_b64).decode("utf-8")
                return json.loads(decoded_payload).get("email", "unknown_user@token.com")
            except: pass
        return "anonymous_or_unauthenticated_user"

    def log_event(self, request, solute_smiles, solvents, results, event_type, model_metadata=None):
        if not self.publisher or not self.topic_path:
            print(f"Skipping telemetry: PubSub not initialized.")
            return
            
        user_email = self._extract_user_identity(request)
        event_payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "scientist_email": user_email,
            "target_molecule_smiles": solute_smiles,
            "tested_solvents": solvents,
            "event_type": event_type,
            "results": json.dumps(results) if results else None,
            "model_version": model_metadata.get("version", "unknown") if model_metadata else None
        }
        
        try:
            future = self.publisher.publish(
                self.topic_path, 
                json.dumps(event_payload).encode("utf-8")
            )
            print(f"Knowledge Hub Event published. Message ID: {future.result()}")
        except Exception as e:
            print(f"Failed to publish Knowledge Hub event: {e}")
