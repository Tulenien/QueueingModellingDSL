from backend.request import Request

class InformationSource:
    def __init__(self, random_generator, name):
        self.generator = random_generator
        self.name = name
        self.requests_generated = 0
        self.current_time = 0.0
        self.previous_time = 0.0

    def reset(self):
        self.requests_generated = 0
        self.current_time = 0.0
        self.previous_time = 0.0

    def generate_request(self):
        self.requests_generated += 1
        name = self.name + "_" + str(self.requests_generated)
        request = Request(name, self.current_time, "generated")
        self.generate_time()
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

    def get_name(self):
        return self.name

    def get_random_generator(self):
        return self.generator