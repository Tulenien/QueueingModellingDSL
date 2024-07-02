from textx import LanguageDesc
from os.path import join, dirname
from backend import TextxModelExporter


def entity_metamodel():
    exporter = TextxModelExporter()
    data = None
    exporter.export_metamodel(join(dirname(__file__), '..\models\qsystem.tx'), data)
    return data


qmodelling_lang = LanguageDesc('QModelling',
                           pattern='*.qs',
                           description='Queue modelling DSL',
                           metamodel=entity_metamodel)