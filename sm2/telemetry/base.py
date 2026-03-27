from abc import ABC, abstractmethod

class BaseTracker(ABC):
    @abstractmethod
    def log_event(self, request, solute_smiles, solvents, results, event_type, model_metadata=None):
        """
        Logs a scientific experiment event.
        
        :param request: The FastAPI request object (for identity extraction)
        :param solute_smiles: The target molecule SMILES string
        :param solvents: List of tested solvents
        :param results: The calculation output results
        :param event_type: A string identifying the type of event (e.g., 'solubility_ranking_requested')
        :param model_metadata: Metadata dict from the MLOps Loader
        """
        pass
