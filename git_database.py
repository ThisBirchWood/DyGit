from object_database import ObjectDatabase
from file_manager import FileManager
from config_reader import ConfigReader

class GitDatabase:
    """
    Database that manages the internal Git, commits and branches
    Input: Path to Git repository
    """
    def __init__(self, dir):
        self.dir = dir
        self.file_manager = FileManager(self.dir)
        self.config = ConfigReader()

        self.object_directory = self.file_manager.join_paths(self.dir, self.config.get_object_directory_name())
        self.object_database = ObjectDatabase(self.object_directory)

        self.current_branch = "main"