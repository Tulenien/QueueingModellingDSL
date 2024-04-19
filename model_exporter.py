from abc import ABC, abstractmethod
from textx.export import metamodel_export, model_export

class IModelExporter(ABC):
    @abstractmethod
    def export_metamodel(self, path, data):
        pass
    
    @abstractmethod
    def export_model(self, path, data):
        pass

class TextxModelExporter(IModelExporter):
    def export_metamodel(self, path, data):
        return metamodel_export(data, path)

    def export_model(self, path, data):
        return model_export(data, path)
