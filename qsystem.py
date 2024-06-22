from statistics import *
from distribution import *
from information_source import *
from processing_unit import *
import request

class QSystem:
    INF_SOURCE = "INF_SOURCE"
    PROCESSOR = "PROCESSOR"
    DELTA = 1e-5
    STAT_DELTA = 1e-3

    def __init__(self):
        self.reset()

    def hard_reset(self):
        self.system_modules = dict()
        self.system_modules[QSystem.INF_SOURCE] = []
        self.system_modules[QSystem.PROCESSOR] = []
        self.delta = QSystem.DELTA
        self.time_constraint = 0.0
        self.requests_constraint = 0
        self.isTimed = False
        self.global_time = 0.0
        self.inf_source_seq = 0
        self.processors_seq = 0
        self.statistics = Statistics(QSystem.STAT_DELTA)

    def add_information_source(self, generator, name="gen"):
        inf_source = InformationSource(generator, self.inf_source_seq, name + self.inf_source_seq)
        self.inf_source_seq += 1
        self.system_modules[QSystem.INF_SOURCE].append(inf_source)
    
    def add_processing_unit(self, generator, name = "proc"):
        proc_unit = ProcessingUnit(generator, self.processors_seq, name + self.processors_seq)
        self.processors_seq += 1
        self.system_modules[QSystem.PROCESSOR].append(proc_unit)

    def __init__(self, modules, statistics, isTimed, value, delta):
        self.system_modules = modules
        self.delta = delta
        self.isTimed = isTimed
        self.time_constraint = 0.0
        self.requests_constraint = 0
        if isTimed:
            self.time_constraint = value
        else:
            self.requests_constraint = value
        self.global_time = 0.0
        self.inf_source_seq = 0
        self.processors_seq = 0
        self.statistics = statistics

    def interpret(self, model):
        for c in model.commands:
            if c.__class__.__name__ == "SetTimeConstraint":
                self.time_constraint = c.number
                self.isTimed = True
            elif c.__class__.__name__ == "SetRequestsConstraint":
                self.requests_constraint = c.number
                self.isTimed = False
            elif c.__class__.__name__ == "Generator":
                generator = RandomGenerator(Distributions.get_distribution(c.distribution))
                add_information_source(generator)
            elif c.__class__.__name__ == "Processor":
                generator = RandomGenerator(Distributions.get_distribution(c.distribution))
                add_processing_unit(generator)
            elif c.__class__.__name__ == "Connect":
                flag = False
                
                for key in c.connection:
                    for source in self.system_modules[QSystem.INF_SOURCE]:
                        if key == source.get_name():
                            processor.connect_inf_source(source)
                            flag = True
                            break

            elif c.__class__.__name__ == "Statistics":
                self.attach_statistics(c.type, c.id)

    def attach_statistics(self, type, id):
        if type == "generator":
            self.statistics.add_generator(self.system_modules[QSystem.INF_SOURCE][id])
        else:
            self.statistics.add_processor(self.system_modules[QSystem.PROCESSOR][id])

    def simulate(self):
        requests = []

        if self.isTimed:
            self.statistics.gather_stats(self.global_time)
            while self.global_time < self.time_constraint:
                self.global_time += QSystem.DELTA
                for source in self.system_modules[QSystem.INF_SOURCE]:
                    if self.global_time > source.generate_time():
                        requests.append(source.generate_request())

                for processor in self.system_modules[QSystem.PROCESSOR]:
                    if requests:
                        if processor.is_active() and self.global_time < processor.get_current_time():
                            processor.set_active(False)
                        if not processor.is_active():
                            processor.set_current_time(self.global_time)
                            processor.set_active(True)
                            request = requests.pop()
                            is_processed = processor.process_request(request)

                            if not is_processed:
                                requests.append(request)
                if self.statistics.get_current_time() > self.global_time:
                    self.statistics.gather_stats(self.global_time)

        else:
            processed_requests = 0
            self.statistics.gather_stats(self.global_time)
            while processed_requests < self.requests_constraint:
                self.global_time += QSystem.DELTA
                for source in self.system_modules[QSystem.INF_SOURCE]:
                    if self.global_time > source.generate_time():
                        requests.append(source.generate_request())

                for processor in self.system_modules[QSystem.PROCESSOR]:
                    if requests:
                        if processor.is_active() and self.global_time > processor.get_current_time():
                            processor.set_active(False)
                        if not processor.is_active():
                            processor.set_active(True)
                            request = requests.pop()
                            is_processed = processor.process_request(request)
                            processed_requests += 1

                            if not is_processed:
                                requests.append(request)
                if self.statistics.get_current_time() > self.global_time:
                    self.statistics.gather_stats(self.global_time)
        print("simulation finished!")
