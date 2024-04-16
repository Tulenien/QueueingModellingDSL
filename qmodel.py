from os.path import dirname, join
import random
from abc import ABC, abstractmethod

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

class Request:
    def __init__(self, name, generation_time, status):
        self.name = name
        self.generation_time = generation_time
        self.start_processing_time = 0.0
        self.finish_processing_time = 0.0
        self.status = status
        
    def set_start_processing_time(self, time):
        self.start_processing_time = time
        
    def set_finish_processing_time(self, time):
        self.finish_processing_time = time
        
    def set_status(self, status):
        self.status = status

class RandomGenerator(ABC):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    @abstractmethod
    def generate_double(self):
        pass
        
class UniformDistribution(RandomGenerator):
    def generate_double(self):
        random_value = random.random()
        result = self.a + (self.b - self.a) * random_value
        return result
        
class NormalDistribution(RandomGenerator):
    def generate_double(self):
        result = 0.0
        for i in range(12):
            random_value = random.random()
            result += random_value

        result -= 6
        return abs(result * self.a * self.b)
        
class InformationSource:
    def __init__(self, random_generator, number, name_template):
        self.id = number
        self.requests_generated = 0
        self.current_time = 0.0
        self.previous_time = 0.0
        self.generator = random_generator
        self.requests_name_template = name_template
        
    def generate_request(self):
        self.requests_generated += 1
        name = self.requests_name_template + str(self.requests_generated)
        request = Request(name, self.current_time, "generated")
        return request
        
    def get_current_time(self):
        return self.current_time
        
    def get_previous_time(self):
        return self.previous_time
        
    def get_requests_generated(self):
        return self.requests_generated
        
    def generate_time(self):
        self.previous_time = self.current_time
        self.current_time += self.generator.generate_double()
        return self.current_time
        
    def get_id(self):
        return id
        
class ProcessingUnit:
    def __init__(self, generator, number, return_percent):
        self.id = number
        self.active = False
        self.return_percent = return_percent
        self.current_time = 0
        self.previous_time = 0
        self.return_count = 0
        self.finished_count = 0
        self.generator = generator
        self.connected_inf_sources = []
        
    def process_request(self, request):
        self.active = True
        request.set_start_processing_time(self.current_time)
        self.current_time += self.generator.generate_double()
        request.set_status("processed")
        request.set_finish_processing_time(self.current_time)
        self.finished_count += 1
        if self.return_percent > 0:
            percent = random.randrange(100)
            if percent < self.return_percent:
                self.return_count += 1
                return False
        return True
        
    def is_active(self):
        return self.active
        
    def get_current_time(self):
        return self.current_time
        
    def get_finished_count(self):
        return self.finished_count
        
    def get_return_count(self):
        return self.return_count
        
    def set_current_time(self, time):
        self.current_time = time
        
    def set_active(self, active):
        self.active = active
        
    def connect_inf_source(self, source):
        self.connected_inf_sources.append(source)
    
    def get_id(self):
        return id

class QSystem:
    INF_SOURCE = "INF_SOURCE"
    PROCESSOR = "PROCESSOR"
    DELTA = 1e-5
    def __init__(self):
        self.system_modules = dict()
        self.system_modules[QSystem.INF_SOURCE] = []
        self.system_modules[QSystem.PROCESSOR] = []
        self.time_constraint = 0.0
        self.requests_constraint = 0
        self.isTimed = False
        self.global_time = 0.0
        self.inf_source_seq = 0
        self.processors_seq = 0
        
    def interpret(self, model):
        for c in model.commands:
            if c.__class__.__name__ == "SetTimeConstraint":
                self.time_constraint = c.number
                self.isTimed = True
            elif c.__class__.__name__ == "SetRequestsConstraint":
                self.requests_constraint = c.number
            elif c.__class__.__name__ == "Generator":
                generator = self.create_generator(c.distribution)
                inf_source = InformationSource(generator, self.inf_source_seq, c.template)
                self.system_modules[QSystem.INF_SOURCE].append(inf_source)
                self.inf_source_seq += 1
            elif c.__class__.__name__ == "Processor":
                generator = self.create_generator(c.distribution)
                processor = ProcessingUnit(generator, self.processors_seq, c.percent, c.connected)
                self.processors_seq += 1
                flag = False
                for source in c.connected:
                    if flag:
                        break
                    for id in self.system_modules[QSystem.INF_SOURCE]:
                        if source.get_id() == id:
                            processor.connect_inf_source(source)
                            flag = True
                            break
                self.system_modules[QSystem.PROCESSOR].append(processor)
            
    def create_generator(self, type):
        if (type == "normal"):
            generator = NormalDistribution()
        elif(type == "uniform"):
            generator = UniformDistribution()
        return type

    def simulate(self):
        requests = []

        if self.isTimed:
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

        else:
            precessed_requests = 0
            while precessed_requests < self.requests_constraint:
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
                            precessed_requests += 1

                            if not is_processed:
                                requests.append(request)


def main(debug=False):

    this_folder = dirname(__file__)

    robot_mm = metamodel_from_file(join(this_folder, 'qsystem.tx'), debug=False)
    metamodel_export(robot_mm, join(this_folder, 'qsystem_meta.dot'))

# Example for adding commands
# Use later for statistics generation
    # Register object processor for MoveCommand
    #robot_mm.register_obj_processors({'MoveCommand': move_command_processor})

    qsystem_model = robot_mm.model_from_file(join(this_folder, 'program.qs'))
    model_export(qsystem_model, join(this_folder, 'program.dot'))

    system = QSystem()
    system.interpret(qsystem_model)


if __name__ == "__main__":
    main()
