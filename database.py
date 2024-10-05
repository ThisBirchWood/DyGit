import hash, os, blob, tree, commit
from config_reader import config

class Database:
    def __init__(self):
        self.config = config("config.env")
        self.object_directory = self.config.get_object_directory()
        self.commit_file = self.config.get_commit_file()

    ## Private Methods
    def _read_file_contents(self, file):
        return open(file, "rb").read()
    
    def _create_file(self, directory, filename, data):
        path = os.path.join(directory, filename)
        with open(path, "wb+") as file:
            file.write(data)

    def _create_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def _split_hash(self, hash):
        hash = str(hash)
        return hash[:2], hash[2:]

    def _add_object(self, obj):
        serialized_blob = hash.serialize_object(obj)
        sha1_hash = hash.sha1_hash(serialized_blob)

        directory, file_name = self._split_hash(sha1_hash)
        directory = os.path.join(self.object_directory, directory)

        self._create_directory(directory)
        self._create_file(directory, file_name, serialized_blob)

        return sha1_hash
    
    def _read_hash_file(self, hash):
        path = self.convert_hash_to_path(hash)
        return self._read_file_contents(path)

    ## Public Methods
    def add_blob(self, b: blob.Blob):
        self._add_object(b)

    def add_tree(self, t: tree.Tree):
        self._add_object(t)

    def add_commit(self, c: commit.Commit):
        hash = self._add_object(c)

        with open(self.commit_file, "w") as f:
            f.write(hash + "\n")

    def convert_hash_to_path(self, hash):
        a, b = self._split_hash(hash)
        return os.path.join(self.object_directory, a, b)
    
    def retrieve_object(self, h):
        serialized_blob = self._read_hash_file(h)
        blob = hash.deserialize_object(serialized_blob)

        return blob
    
    def read_blob(self, h):
        return self.retrieve_object(h).data

if __name__ == "__main__":
    d = Database()
    d.add_blob(blob.Blob("I play pokemon go everyday "))
    d.add_blob(blob.Blob("bluh bluh bluh"))
    d.add_blob(blob.Blob("If you have the serialized object stored in a byte stream"))
    d.add_blob(blob.Blob("Security: Be careful when deserializing data from untrusted sources. pickle can execute arbitrary code during deserialization, which poses a security risk."))
    print(d.read_blob("55cbcab42f49e968e91a61c1cb2e98bee7a7de4f"))

