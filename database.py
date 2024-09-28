import hash, os, blob, tree
from config_reader import config

class database:
    def __init__(self):
        self.config = config("config.env")
        self.object_directory = self.config.get_object_directory()

    ## Private Methods
    def _read_file_contents(self, file):
        return open(file, "r", encoding="utf8").read()
    
    def _create_file(self, directory, filename, data):
        with open(os.path.join(directory, filename), "wb") as file:
            file.write(data)

    def _create_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def _add_object(self, obj):
        serialized_blob = hash.serialize_object(obj)
        sha1_hash = hash.sha1_hash(serialized_blob)

        directory, file_name = sha1_hash[:2], sha1_hash[2:]
        directory = os.path.join(self.object_directory, directory)

        self._create_directory(directory)
        self._create_file(directory, file_name, serialized_blob)

    def add_blob(self, b: blob.Blob):
        self._add_object(b)

    def add_tree(self, t: tree.Tree):
        self._add_object(t)

    
d = database()
d.add_blob(blob.Blob("I play pokemon go everyday "))
