from os.path import dirname, join
from qsystem import *
from model_exporter import *
from model_reader import *


def main(debug=False):
    this_folder = dirname(__file__)

    reader = TextxModelReader()
    exporter = TextxModelExporter()

    qsystem_mm = reader.read_metamodel(join(this_folder, 'qsystem.tx'))
    qsystem_model = reader.read_model(join(this_folder, 'program.qs'), qsystem_mm)

    exporter.export_metamodel(join(this_folder, 'qsystem_meta.dot'), qsystem_mm)
    exporter.export_model(join(this_folder, 'program.dot'), qsystem_model)

    system = QSystem()
    system.interpret(qsystem_model)
    system.simulate()


if __name__ == "__main__":
    main()
