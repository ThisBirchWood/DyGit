import hash, tree, database, file_scanner, config_reader, os

class file_manager:
    def __init__(self):
        self.scanner = file_scanner.file_scanner()
        self.config = config_reader.config("config.env")
        self.exclude = set(["my_git", ".vscode"])
        self.database = database.Database()
        self.main_directory = self.config.get_main_directory()

    def _scan(self, directory):
        return [os.path.join(directory, x) for x in os.listdir(directory) if x not in self.exclude]

    def _get_last_commit(self):
        commit_file = self.config.get_commit_file()

        last_line = self._get_last_line_of_file(commit_file)
        return self.database.get_commit(last_line)

    def _get_last_line_of_file(self, file):
        with open(file, 'rb') as f:
            try:  # catch OSError in case of a one line file 
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            return f.readline().decode()
        
    def _generate_tree(self, directory):
        root_tree = tree.Tree(directory)

        for file in self._scan(directory):
            if os.path.isfile(file):
                h = self.database.get_hash_of_file(file)
                self.database.add_file(file)
                root_tree.add_child(tree.Tree_Entry(file, h, False))
            elif os.path.isdir(file):
                internal_tree = self._generate_tree(file)
                self.database.add_tree(internal_tree)
                h = self.database.get_hash_of_object(internal_tree)
                root_tree.add_child(tree.Tree_Entry(file, h, True))

        return root_tree
    
    def generate_tree(self) -> tree.Tree:
        return self._generate_tree(self.main_directory)

if __name__ == "__main__":
    f = file_manager()
    t = f.generate_tree()
    t._list_files()
    