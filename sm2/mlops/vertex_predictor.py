import pandas as pd
from google.cloud import aiplatform
from sm2.mlops.base_predictor import BasePredictor

class VertexEndpointPredictor(BasePredictor):
    def __init__(self, project_id, endpoint_id, location="us-central1"):
        self.project_id = project_id
        self.endpoint_id = endpoint_id
        self.location = location
        try:
            aiplatform.init(project=self.project_id, location=self.location)
            self.endpoint = aiplatform.Endpoint(self.endpoint_id)
            print(f"Initialized Vertex AI Endpoint: {self.endpoint_id}")
        except Exception as e:
            print(f"Vertex AI Endpoint Init failed: {e}")

    def predict(self, solute_smiles: str, solvents: list, temps: list, facs: list):
        instances = [{
            "solute_smiles": solute_smiles,
            "solvents": solvents,
            "temps": temps,
            "facs": facs
        }]
        
        try:
            response = self.endpoint.predict(instances=instances)
            preds = response.predictions[0]
            dfo = pd.DataFrame(preds)
            dfo = dfo.rename(columns={"solvent_smiles": "solvent SMILES", "log_s": "log S"})
            metadata = {
                "source": "vertex_ai_endpoint", 
                "endpoint_id": self.endpoint_id,
                "version": f"vertex-endpoint-{self.endpoint_id}"
            }
            return dfo, metadata
        except Exception as e:
            print(f"Vertex AI prediction failed: {e}")
            raise e
