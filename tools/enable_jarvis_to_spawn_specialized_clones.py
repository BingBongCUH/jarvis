
class Jarvis:
    def __init__(self, specialization):
        self.specialization = specialization

    def clone(self):
        return Jarvis(self.specialization)


def spawn_specialized_clones(specializations):
    jarvis = Jarvis("General")
    clones = []
    for specialization in specializations:
        clone = jarvis.clone()
        clone.specialization = specialization
        clones.append(clone)
    return clones


specializations = ["AI", "ML", "Data Science", "Web Development", "Mobile Development"]
clones = spawn_specialized_clones(specializations)

for clone in clones:
    print(f"Spawned a Jarvis clone specialized in {clone.specialization}")
