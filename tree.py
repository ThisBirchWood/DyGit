class Tree_Entry():
    def __init__(self, _name: str, _hash: str, _tree: bool):
        self.name = _name
        self.hash = _hash
        self.tree = _tree

class Tree:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def __repr__(self):
        output = ''
        for child in self.children:
            if child.tree:
                output += f'tree {child.hash} {child.name}\n'
            else:
                output += f'blob {child.hash} {child.name}\n'
        return output

    def add_child(self, obj: Tree_Entry):
        self.children.append(obj)

    def remove_child(self, obj: Tree_Entry):
        self.children.remove(obj)