class Tree:
    tree_types = {"Sapling": {"Reproduction_chance": 0, "grow_age": 12, "lumber": 0, "total_number": 0},
                  "Tree": {"Reproduction_chance": 0.1, "grow_age": 120, "lumber": 1, "total_number": 0},
                  "Elder": {"Reproduction_chance": 0.2, "grow_age": -1, "lumber": 2, "total_number": 0}}

    tree_list = []

    def __init__(self, tree_type="Tree", position=None):
        assert position is not None, "Tree has to be initialized at a specific position!"

        self.position = position
        self.tree_type = tree_type

        Tree.tree_list.append(self)
        Tree.tree_types[tree_type]["total_number"] += 1

    def display(self):
        return "T"