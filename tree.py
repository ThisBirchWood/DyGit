from blob import Blob
import hash

class Tree_Entry():
    def __init__(self, _filepath: str, _obj):
        self.filepath = _filepath
        self.obj = _obj

        if isinstance(self.obj, Tree):
            self.tree = True
        elif isinstance(self.obj, Blob):
            self.tree = False
        else:
            raise TypeError(f"Tree Entry must take a Tree or Blob object type, not {type(self.obj)}")

class Tree:
    def __init__(self, path: str):
        self.path = path
        self.children = []

    def list_children(self):
        for child in self.children:
            child_hash = hash.sha1_hash(hash.serialize_object(child))
            if child.tree == True:
                print(f"tree {child_hash}")
            else:
                print(f"blob {child_hash}")

    def add_child(self, obj: Tree_Entry):
        self.children.append(obj)

    def remove_child(self, obj: Tree_Entry):
        self.children.remove(obj)