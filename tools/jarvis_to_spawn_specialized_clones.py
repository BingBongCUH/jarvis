
class Jarvis:
    def __init__(self, specialization):
        self.specialization = specialization

    def clone(self):
        return Jarvis(self.specialization)


def spawn_specialized_clones(specializations):
    jarvis = Jarvis(None)
    clones = []
    for specialization in specializations:
        clone = jarvis.clone()
        clone.specialization = specialization
        clones.append(clone)
    return clones
