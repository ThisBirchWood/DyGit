from blob import Blob
import hash, database

class Tree_Entry():
    def __init__(self, _path: str, _hash: str, _tree: bool):
        self.path = _path
        self.hash = _hash
        self.tree = _tree

class Tree:
    def __init__(self, path: str):
        self.path = path
        self.children = []

    def _list_files(self, indent=0):
        for child in self.children:
            ind = indent
            i = "\t" * indent
            if child.tree:
                print(i + "dir----" + child.path)
                tree = database.Database().get_tree(child.hash)
                tree._list_files(indent=ind+1)
            else:
                print(i + "file---" + child.path)

    def add_child(self, obj: Tree_Entry):
        self.children.append(obj)

    def remove_child(self, obj: Tree_Entry):
        self.children.remove(obj)