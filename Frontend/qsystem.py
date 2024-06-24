from statistics import *
from distribution import *
from information_source import *
from processing_unit import *
import request

class QSystem:
    INF_SOURCE = "INF_SOURCE"
    PROCESSOR = "PROCESSOR"
    DELTA = 1e-2#1e-5
    STAT_DELTA = 1e-3

    def __init__(self):
        self.hard_reset()

    def hard_reset(self):
        self.system_modules = dict()
        self.system_modules[QSystem.INF_SOURCE] = []
        self.system_modules[QSystem.PROCESSOR] = []
        self.delta = QSystem.DELTA
        self.time_constraint = 0.0
        self.requests_constraint = 0
        self.isTimed = False
        self.global_time = 0.0
        self.statistics = Statistics(QSystem.STAT_DELTA)

    def add_information_source(self, generator, name="gen"):
        inf_source = InformationSource(generator, name)
        self.system_modules[QSystem.INF_SOURCE].append(inf_source)
    
    def add_processing_unit(self, generator, name = "proc"):
        proc_unit = ProcessingUnit(generator, name)
        self.system_modules[QSystem.PROCESSOR].append(proc_unit)

    def interpret(self, model):
        for c in model.commands:
            if c.__class__.__name__ == "SetTimeConstraint":
                self.time_constraint = c.number
                self.isTimed = True

            elif c.__class__.__name__ == "SetRequestConstraint":
                self.requests_constraint = c.number
                self.isTimed = False

            elif c.__class__.__name__ == "Generator":
                function = Distributions.get_distribution(c.distribution.name)
                generator = RandomGenerator(function, c.distribution.args)
                self.add_information_source(generator, c.name)

            elif c.__class__.__name__ == "Processor":
                function = Distributions.get_distribution(c.distribution.name)
                generator = RandomGenerator(function, c.distribution.args)
                self.add_processing_unit(generator, c.name)

            elif c.__class__.__name__ == "Connect":
                flag = False
                for key in c.connection:
                    for source in self.system_modules[QSystem.INF_SOURCE]:
                        if key == source.get_name():
                            processor.connect_inf_source(source)
                            flag = True
                            break

    def time_simulation(self):
        self.global_time = 0.0
        requests = []
        finished_requests = []

        for source in self.system_modules[QSystem.INF_SOURCE]:
            source.generate_time()

        while self.global_time < self.time_constraint:
            self.global_time += QSystem.DELTA
            for source in self.system_modules[QSystem.INF_SOURCE]:
                if self.global_time > source.get_current_time():
                    requests.append(source.generate_request())

            for processor in self.system_modules[QSystem.PROCESSOR]:
                if processor.is_active() and self.global_time < processor.get_current_time():
                    processor.set_active(False)
                if requests:
                    if not processor.is_active():
                        processor.set_current_time(self.global_time)

                        request = requests.pop()
                        request = processor.process_request(request)
                        finished_requests.append(request)

        self.log_requests(finished_requests)

    def requests_simulation(self):
        processed_requests = 0
        self.global_time = 0.0
        requests = []
        finished_requests = []

        for source in self.system_modules[QSystem.INF_SOURCE]:
            source.generate_time()

        while processed_requests < self.requests_constraint:
            self.global_time += QSystem.DELTA
            for source in self.system_modules[QSystem.INF_SOURCE]:
                if self.global_time > source.get_current_time():
                    requests.append(source.generate_request())

            for processor in self.system_modules[QSystem.PROCESSOR]:
                if processor.is_active() and self.global_time < processor.get_current_time():
                    processor.set_active(False)
                    processed_requests += 1
                if requests:
                    if not processor.is_active():
                        processor.set_current_time(self.global_time)
                        processor.set_active(True)
                        request = requests.pop()
                        request = processor.process_request(request)
                        finished_requests.append(request)
                        print(request.get_name())

        self.log_requests(finished_requests)

    def simulate(self):
        if self.isTimed:
            self.time_simulation()
        else:
            self.requests_simulation()
        print("simulation finished!")

    def log_requests(self, requests):
        for r in requests:
            print("Name: {}\nGenerated: {}\nStarted processing: {}\nProcessed: {}\n".format(
                r.get_name(), r.get_generation_time(), r.get_start_processing_time(), r.get_finish_processing_time()))
