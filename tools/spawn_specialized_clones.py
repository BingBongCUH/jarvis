def run(user_input)
    print("This will break")

class Clone:
    def __init__(self, specialization):
        self.specialization = specialization

def spawn_specialized_clones(specialization, quantity):
    return [Clone(specialization) for _ in range(quantity)]

def run(user_input):
    specialization, quantity = user_input.split(',')
    quantity = int(quantity)
    return spawn_specialized_clones(specialization, quantity)

def run(user_input):
    raise RuntimeError("Simulated crash for testing repair")
