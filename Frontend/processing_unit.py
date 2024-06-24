class ProcessingUnit:
    name_template = "proc_"

    def __init__(self, random_generator, name):
        self.generator = random_generator
        self.name = name
        self.active = False
        self.current_time = 0.0
        self.previous_time = 0.0
        self.finished_count = 0

    def process_request(self, request):
        self.active = True
        request.set_status("processed")
        request.set_start_processing_time(self.current_time)
        self.current_time += self.generator.generate_double()
        request.set_finish_processing_time(self.current_time)
        self.finished_count += 1
        return request

    def get_name(self):
        return self.name

    def is_active(self):
        return self.active

    def get_current_time(self):
        return self.current_time

    def get_finished_count(self):
        return self.finished_count

    def set_current_time(self, time):
        self.current_time = time

    def set_active(self, active):
        self.active = active