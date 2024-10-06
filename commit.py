import tree

class Commit:
    def __init__(self, tree: tree.Tree, message: str, author: str):
        self.root_tree = tree
        self.message = message
        self.author = author