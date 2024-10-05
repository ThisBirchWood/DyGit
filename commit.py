import tree

class Commit:
    def __init__(self, tree: tree.Tree, message):
        self.root_tree = tree
        self.message = message