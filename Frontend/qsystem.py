from statistics import *
from distribution import *
from information_source import *
from processing_unit import *
import request

class QSystem:
    INF_SOURCE = "INF_SOURCE"
    PROCESSOR = "PROCESSOR"
    DELTA = 1e-3
    STAT_DELTA = 1e-3

    def __init__(self):
        self.hard_reset()

    def hard_reset(self):
        self.system_modules = dict()
        self.system_modules[QSystem.INF_SOURCE] = []
        self.system_modules[QSystem.PROCESSOR] = []
        self.delta = QSystem.DELTA
        self.time_constraint = 10
        self.requests_constraint = 0
        self.isTimed = True
        self.global_time = 0.0
        self.statistics = Statistics(QSystem.STAT_DELTA)
    
    def soft_reset(self):
        generators = self.get_generators()
        processors = self.get_processors()
        for gen in generators:
            gen.reset()
        for proc in processors:
            proc.reset()

    def get_generators(self):
        return self.system_modules[QSystem.INF_SOURCE]

    def get_processors(self):
        return self.system_modules[QSystem.PROCESSOR]

    def get_time_constraint(self):
        return self.time_constraint

    def get_requests_constraint(self):
        return self.requests_constraint

    def get_delta(self):
        return self.delta

    def set_time_constraint(self, time):
        self.set_isTimed(True)
        self.time_constraint = time

    def set_requests_constaint(self, requests):
        self.set_isTimed(False)
        self.requests_constraint = requests

    def set_isTimed(self, value):
        self.isTimed = value

    def set_delta(self, delta):
        self.delta = delta

    def add_information_source(self, generator, name="gen"):
        inf_source = InformationSource(generator, name)
        self.system_modules[QSystem.INF_SOURCE].append(inf_source)

    def remove_information_source(self, name):
        generators = self.get_generators()
        for gen in generators:
            if name == gen.get_name():
                generators.remove(gen)
                break

    def remove_processing_unit(self, name):
        processors = self.get_processors()
        for proc in processors:
            if name == proc.get_name():
                processors.remove(proc)
                break
    
    def add_processing_unit(self, generator, name = "proc"):
        proc_unit = ProcessingUnit(generator, name)
        self.system_modules[QSystem.PROCESSOR].append(proc_unit)

    def prepare_information_sources(self):
        for source in self.system_modules[QSystem.INF_SOURCE]:
            source.generate_time()

    def handle_information_sources(self, requests):
        for source in self.system_modules[QSystem.INF_SOURCE]:
                if self.global_time > source.get_current_time():
                    requests.append(source.generate_request())

    def handle_processing_units(self, q_in, q_out):
        processed_number = 0
        for processor in self.system_modules[QSystem.PROCESSOR]:
                if processor.is_active() and self.global_time > processor.get_current_time():
                    processor.set_active(False)
                    processed_number += 1
                if q_in:
                    if not processor.is_active():
                        processor.set_current_time(self.global_time)
                        request = q_in.pop()
                        request = processor.process_request(request)
                        q_out.append(request)
        return processed_number


    def interpret(self, model):
        self.hard_reset()
        for c in model.commands:
            if c.__class__.__name__ == "SetTimeConstraint":
                self.time_constraint = c.number
                self.isTimed = True

            elif c.__class__.__name__ == "SetRequestConstraint":
                self.requests_constraint = c.number
                self.isTimed = False

            elif c.__class__.__name__ == "Generator":
                function = Distributions.get_distribution(c.distribution.name)
                generator = RandomGenerator(function, c.distribution.args, c.distribution.name)
                self.add_information_source(generator, c.name)

            elif c.__class__.__name__ == "Processor":
                function = Distributions.get_distribution(c.distribution.name)
                generator = RandomGenerator(function, c.distribution.args, c.distribution.name)
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

        self.prepare_information_sources()
        while self.global_time < self.time_constraint:
            self.global_time += QSystem.DELTA
            self.handle_information_sources(requests)
            self.handle_processing_units(requests, finished_requests)

        self.log_requests(finished_requests)

    def requests_simulation(self):
        processed_requests = 0
        self.global_time = 0.0
        requests = []
        finished_requests = []

        self.prepare_information_sources()
        while self.requests_constraint > processed_requests:
            self.global_time += QSystem.DELTA
            self.handle_information_sources(requests)
            processed_requests += self.handle_processing_units(requests, finished_requests)

        self.log_requests(finished_requests)

    def simulate(self):
        self.soft_reset()
        if self.isTimed:
            self.time_simulation()
        else:
            self.requests_simulation()
        print("simulation finished!")

    def log_requests(self, requests):
        for r in requests:
            print("Name: {}\nGenerated: {}\nStarted processing: {}\nProcessed: {}\n".format(
                r.get_name(), r.get_generation_time(), r.get_start_processing_time(), r.get_finish_processing_time()))
