import hash, os, blob, zlib
from config_reader import config

HASH_DIRECTORY_SPLIT = 2

class Database:
    def __init__(self):
        self.config = config("config.env")
        self.object_directory = self.config.get_object_directory()
        self.commit_file = self.config.get_commit_file()

    ## Private Methods
    def _read_file_contents(self, file: str) -> bytes:
        """Reads a file and returns its contents in binary."""
        return open(file, "rb").read()

    def _create_file(self, directory: str, filename: str, data: bytes):
        """Creates a file in a given directory with the given data."""
        path = os.path.join(directory, filename)
        with open(path, "wb+") as file:
            file.write(data)

    def _create_directory(self, directory_path: str):
        """Creates a directory if it doesn't already exist."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def _split_hash(self, hash: str):
        """Splits the hash into the first two characters (directory) and the rest (filename)."""
        hash = str(hash)
        return hash[:HASH_DIRECTORY_SPLIT], hash[HASH_DIRECTORY_SPLIT:]

    def _hash_to_path(self, h: str):
        """Generates a path from a hash."""
        directory, filename = self._split_hash(h)
        return os.path.join(self.object_directory, directory, filename)

    def _add_data(self, data: bytes):
        """Adds data to the object store and returns its SHA-1 hash."""
        sha1_hash = hash.sha1_hash(data)

        directory, file_name = self._split_hash(sha1_hash)
        directory = os.path.join(self.object_directory, directory)

        compressed_data = self._compress(data)
        self._create_directory(directory)
        self._create_file(directory, file_name, compressed_data)

        return sha1_hash

    def _read_data(self, h: str):
        """Reads data from the object store based on the hash."""
        path = self._hash_to_path(h)
        compressed_data = self._read_file_contents(path)
        return self._decompress(compressed_data)

    def _add_commit_to_file(self, hash):
        """Adds a commit hash to the commit file."""
        with open(self.commit_file, "w") as f:
            f.write(hash + "\n")

    def _compress(self, data: bytes) -> bytes:
        """Compresses data using zlib."""
        return zlib.compress(data)

    def _decompress(self, compressed_data: bytes) -> bytes:
        """Decompresses zlib-compressed data."""
        return zlib.decompress(compressed_data)

    ## Public Methods
    def add_file(self, path) -> blob.Blob:
        """Adds a file to the object store."""
        data = self._read_file_contents(path)
        b = blob.Blob(data)
        self.add_blob(b)
        return b

    def add_blob(self, b: blob.Blob):
        """Adds a Blob object to the object store."""
        self._add_data(b.data)

    def add_tree(self, t):
        """Adds a serialized Tree object to the object store."""
        serialized_object = hash.serialize_object(t)
        return self._add_data(serialized_object)

    def add_commit(self, c):
        """Adds a serialized Commit object to the object store and writes its hash to the commit file."""
        serialized_object = hash.serialize_object(c)
        h = self._add_data(serialized_object)

        self._add_commit_to_file(h)
        return h

    def get_blob(self, h):
        """Retrieves a Blob object from the object store based on its hash."""
        data = self.get_blob_data(h)
        return blob.Blob(data)

    def get_blob_data(self, h) -> str:
        """Retrieves blob data as a string."""
        return self._read_data(h)

    def get_tree(self, h: str):
        """Retrieves a Tree object from the object store based on its hash."""
        serialized_tree = self._read_data(h)
        return hash.deserialize_object(serialized_tree)

    def get_commit(self, h: str):
        """Retrieves a Commit object from the object store based on its hash."""
        serialized_commit = self._read_data(h)
        return hash.deserialize_object(serialized_commit)
    
    def get_hash_of_file(self, path: str) -> str:
        data = self._read_file_contents(path)
        return hash.sha1_hash(data)
    
    def get_hash_of_object(self, obj) -> str:
        serialized_obj = hash.serialize_object(obj)
        return hash.sha1_hash(serialized_obj)

if __name__ == "__main__":
    d = Database()
    #tree1 = tree.Tree('osufihg')
    d.add_file("../p.py")
    d.add_file("../test")
