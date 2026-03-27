from abc import ABC, abstractmethod

class BasePredictor(ABC):
    @abstractmethod
    def predict(self, solute_smiles: str, solvents: list, temps: list, facs: list):
        """
        Executes the prediction logic and returns the resulting DataFrame and metadata.
        """
        pass
