from hash import serialize_object, deserialize_object, sha1_hash
from zlib import compress as zcompress, decompress as zdecompress
from config_reader import ConfigReader
from file_manager import FileManager
from blob import Blob
from tree import Tree
from commit import Commit

HASH_DIRECTORY_SPLIT = 2

class ObjectDatabase:
    """
    Manages the Git object database (blobs, trees and commits)
    Inputs: Path to object directory
    """
    def __init__(self, dir):
        self.dir = dir
        self.file_manager = FileManager(self.dir)
        self.config = ConfigReader()

    ## Private Methods
    def _split_hash(self, hash: str):
        """Splits the hash into the first two characters (directory) and the rest (filename)."""
        return hash[:HASH_DIRECTORY_SPLIT], hash[HASH_DIRECTORY_SPLIT:]
    
    def _hash_to_path(self, hash: str):
        directory, file = self._split_hash(hash)
        return self.file_manager.join_paths(directory, file)
    
    def _add_data(self, data: bytes) -> str:
        hash = sha1_hash(data)
        directory, file = self._split_hash(hash)
        path = self._hash_to_path(hash)

        compressed_data = zcompress(data) 
        self.file_manager.create_directory(directory)
        self.file_manager.create_file(path, compressed_data)

        return hash
    
    def _get_data(self, h: str) -> bytes:
        path = self._hash_to_path(h)
        compressed_data = self.file_manager.read_file(path)
        return zdecompress(compressed_data)
    
    def _add_object(self, obj) -> str:
        serialized_object = serialize_object(obj)
        return self._add_data(serialized_object)
    
    def _get_object(self, h: str):
        serialized_object = self._get_data(h)
        return deserialize_object(serialized_object)
    
    ## Public Methods
    def add_blob(self, b: Blob) -> str:
        """ 
        Adds a blob to the object store, returns hash
        NOTE: Adding blobs only hashes the data, not the entire object
        """
        return self._add_data(b.data)
    
    def add_tree(self, t: Tree) -> str:
        """
        Adds a tree object to the object store, returns hash
        """
        return self._add_object(t)
    
    def add_commit(self, c: Commit) -> str:
        """
        Adds a commit object to object store, returns hash
        """
        return self._add_object(c)
    
    def get_blob(self, h: str) -> Blob:
        """
        Returns blob object from blob's data hash
        """
        blob_data = self._get_data(h)
        return Blob(blob_data)
    
    def get_tree(self, h: str) -> Tree:
        """
        Returns tree object from tree hash
        """
        return Tree(self._get_object(h))
    
    def get_commit(self, h: str) -> Commit:
        """
        Returns commit object from commit hash
        """
        return Commit(self._get_object(h))
    

if __name__ == "__main__":
    d = ObjectDatabase(r"C:\Users\Dylan De Faoite\Documents\Chord Gen\.git\objects")
    


    