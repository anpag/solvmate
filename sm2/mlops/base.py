from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def load_model(self, model_path: str, model_metadata_path: str):
        """
        Loads the model and its metadata.
        
        :param model_path: Expected local path or Vertex AI model name
        :param model_metadata_path: Expected metadata path
        :return: (model_state_dict, metadata_dict)
        """
        pass
