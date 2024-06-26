from os.path import dirname, join
from model_exporter import *
from model_reader import *

class QModel:
    def import_textx_model(self, metamodel_path, model_path, this_folder=dirname(__file__)):
        reader = TextxModelReader()
        exporter = TextxModelExporter()

        qsystem_mm = reader.read_metamodel(metamodel_path)
        qsystem_model = reader.read_model(model_path, qsystem_mm)

        exporter.export_metamodel(join(this_folder, 'qsystem_meta.dot'), qsystem_mm)
        exporter.export_model(join(this_folder, 'program.dot'), qsystem_model)

        return qsystem_model