import unittest
from distribution import *
from information_source import *
from processing_unit import *
from statistics import *
from qsystem import *

class TestQmodel(unittest.TestCase):
    def setUp(self):
        self.system_modules = dict()
        self.system_modules[QSystem.INF_SOURCE] = []
        self.system_modules[QSystem.PROCESSOR] = []

        generator = RandomGenerator.create_generator(1)
        generator1 = RandomGenerator.create_generator(5)
        source = InformationSource(generator1, 1, "gen1")
        processor = ProcessingUnit(generator, 1, 0)
        processor.connect_inf_source(source)
        self.system_modules[QSystem.INF_SOURCE].append(source)
        self.system_modules[QSystem.PROCESSOR].append(processor)
        self.statistics = Statistics(QSystem.STAT_DELTA)
        self.statistics.add_processor(processor)

        self.system = QSystem(self.system_modules, self.statistics, True, 10)

    def test_processed_requests_count_timed(self):
        self.system.simulate()
        self.assertEqual(self.statistics.get_processed_requests(), 2)

if __name__ == '__main__':
    unittest.main()