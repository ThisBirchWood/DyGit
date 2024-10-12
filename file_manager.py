import os

class FileManager:
    def __init__(self, working_dir):
        self.dir = working_dir

    def create_file(self, path, data: bytes, overwrite=True) -> str:
        path = self.join_paths(self.dir, path)
        if not os.path.exists(path) and overwrite==True:
            with open(path, "wb+") as file:
                file.write(data)
            return path
        
    def create_directory(self, path) -> bool:
        path = self.join_paths(self.dir, path)
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return False
    
    def read_file(self, path: str) -> bytes:
        path = self.join_paths(self.dir, path)
        return open(path, "rb").read()
    
    def join_paths(self, *paths) -> str:
        return os.path.join(*paths)
    
    def get_basename(self, path) -> str:
        return os.path.basename(path)
    
    def scan(self, path='') -> list:
        path = self.join_paths(self.dir, path)
        return [self.join_paths(path, x) for x in os.listdir(path)]
