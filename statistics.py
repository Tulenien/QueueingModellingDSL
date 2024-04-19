class Statistics:
    def __init__(self, delta):
        self.generators = []
        self.processors = []

        self.requests_generated = []
        self.generation_time = []

        self.proccessed_count = []
        self.returned_count = []
        self.processing_time = []

        self.current_time = 0.0
        self.delta = delta

    def add_generator(self, generator):
        self.generators.append(generator)

    def add_processor(self, processor):
        self.processors.append(processor)

    def gather_stats(self, current_time):
        temp_generated_number = 0
        temp_processed_count = 0
        temp_returned_count = 0
        for source in self.generators:
            temp_generated_number += source.get_requests_generated()
        self.requests_generated.append(temp_generated_number)
        self.generation_time.append(current_time)

        for proc in self.processors:
            temp_processed_count += proc.get_finished_count()
            temp_returned_count += proc.get_returned_count()
        self.proccessed_count.append(temp_processed_count)
        self.returned_count.append(temp_returned_count)
        self.processing_time.append(current_time)

        self.current_time += self.delta

    def get_current_time(self):
        return self.current_time

