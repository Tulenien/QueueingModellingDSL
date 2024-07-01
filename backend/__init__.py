# my_project/__init__.py

# Import submodules
from backend.distribution import RandomGenerator, Distributions
from backend.graph import make_plot
from backend.information_source import InformationSource
from backend.model_exporter import IModelExporter, TextxModelExporter
from backend.model_reader import IModelReader, TextxModelReader
from backend.processing_unit import ProcessingUnit
from backend.qsystem import QSystem
from backend.qmodel import QModel
from backend.request import Request


# Package metadata
__version__ = "0.1.0"