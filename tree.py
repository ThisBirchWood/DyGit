class Tree:
    def __init__(self, path):
        self.path = path
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def remove_child(self, obj):
        self.children.remove(obj)