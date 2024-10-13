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

        self.git_directory_path = self.config.get_git_directory_name()
        self.branches_directory_path = self.file_manager.join_paths(self.git_directory_path, self.config.get_branches_directory_name())
        self.object_directory_path = self.file_manager.join_paths(self.config.get_git_directory_name(), self.config.get_object_directory_name())
        self.current_branch_file_path = self.file_manager.join_paths(self.git_directory_path, self.config.get_current_branch_file())
        self.default_branch_file_path = self.file_manager.join_paths(self.branches_directory_path, self.config.get_default_branch_name())
        self.ignore_file_name = self.config.get_gitignore_file()

        self.object_database = ObjectDatabase(self.file_manager.join_paths(self.dir, self.object_directory_path))


    def init(self):
        self.current_branch = self.config.get_default_branch_name()

        self.file_manager.create_directory(self.git_directory_path)
        self.file_manager.create_directory(self.branches_directory_path)
        self.file_manager.create_directory(self.object_directory_path)
        self.file_manager.create_file(self.current_branch_file_path, self.current_branch.encode())
        self.file_manager.create_file(self.default_branch_file_path, b'')
        self.file_manager.create_file(self.ignore_file_name, b'')



if __name__ == "__main__":
    git = GitDatabase(r"C:\Users\Dylan De Faoite\Documents\Chord Gen")
    git.init()