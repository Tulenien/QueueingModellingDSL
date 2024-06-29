import random

class RandomGenerator():
    def __init__(self, func, args, distribution_name):
        self.generative_function = func
        self.args = args
        self.distribution = distribution_name

    def generate_double(self):
        return self.generative_function(*self.args)

    def get_distribution(self):
        return self.distribution

    def get_distribution_args(self):
        return self.args

class Distributions:
    def uniform(a, b):
        random_value = random.random()
        result = a + (b - a) * random_value
        return result

    def normal(a, b):
        result = 0.0
        for i in range(12):
            random_value = random.random()
            result += random_value
        result -= 6
        return abs(result * a * b)
        
    def increment(value):
        return value

    distribution_dict = {
        'uniform' : uniform,
        'normal' : normal,
        'increment' : increment
    }

    def get_distribution(name):
        for key in Distributions.distribution_dict:
            if (key == name):
                return Distributions.distribution_dict[key]
        return increment
