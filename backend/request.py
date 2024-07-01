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

    def get_name(self):
        return self.name

    def get_finish_processing_time(self):
        return self.finish_processing_time

    def get_generation_time(self):
        return self.generation_time

    def get_start_processing_time(self):
        return self.start_processing_time