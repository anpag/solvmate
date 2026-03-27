import torch
import joblib
from pathlib import Path
from sm2.mlops.base import BaseLoader

class LocalLoader(BaseLoader):
    def load_model(self, model_path: str, model_metadata_path: str):
        """Loads a PyTorch model and joblib metadata from local disk."""
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Local model file not found: {model_path}")
            
        if torch.cuda.is_available():
            state_dict = torch.load(model_path)
        else:
            state_dict = torch.load(model_path, map_location=torch.device('cpu'))
            
        metadata = {}
        if Path(model_metadata_path).exists():
            metadata = joblib.load(model_metadata_path)
            
        # Add local origin metadata
        metadata["version"] = "local-v0.1"
        metadata["source"] = "local"
        
        return state_dict, metadata
