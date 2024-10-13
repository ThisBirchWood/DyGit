class Commit:
    def __init__(self, tree_hash: str, message: str, author: str):
        self.tree_hash = tree_hash
        self.message = message
        self.author = author

