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