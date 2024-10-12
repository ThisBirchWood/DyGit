from hash import serialize_object, deserialize_object, sha1_hash
from zlib import compress as zcompress, decompress as zdecompress
from config_reader import ConfigReader
from file_manager import FileManager

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
    #def add_file(self, path: str) -> str:

    

if __name__ == "__main__":
    d = ObjectDatabase(r"C:\Users\Dylan De Faoite\Documents\Chord Gen\.git\objects")
    c = ConfigReader()
    j = d._add_object(c)
    print(d._get_object(j))
    


    