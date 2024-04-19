import random
from abc import ABC, abstractmethod

class RandomGenerator(ABC):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __init__(self, value):
        self.value = value
        
    def create_generator(type, a, b):
        if (type == "normal"):
            generator = NormalDistribution(a, b)
        elif (type == "uniform"):
            generator = UniformDistribution(a, b)
        return generator

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