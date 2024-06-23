from abc import ABC, abstractmethod
from textx import metamodel_from_file

class IModelReader(ABC):
    @abstractmethod
    def read_metamodel(self, path):
        pass
    
    @abstractmethod
    def read_model(self, path, metamodel):
        pass

class TextxModelReader(IModelReader):
    def read_metamodel(self, path):
        return metamodel_from_file(path)

    def read_model(self, path, metamodel):
        return metamodel.model_from_file(path)
