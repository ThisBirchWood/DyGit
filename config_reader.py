DEFAULT_CONFIG_FILENAME="config.env"
class ConfigReader:
    def __init__(self, file=DEFAULT_CONFIG_FILENAME):
        self.values = {}
        self._load_config(file)

    def _load_config(self, file):
        try:
            with open(file, "r") as f:
                for line in f:
                    line = line.strip()
                    # Ignore comments and blank lines
                    if line.startswith("#") or not line:
                        continue
                    try:
                        key, value = line.split("=", 1)
                        self.values[key.strip()] = value.strip()
                    except ValueError:
                        print(f"Warning: Malformed line in config: '{line}'")
        except FileNotFoundError:
            print(f"Error: Config file '{file}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def get(self, key, default=None):
        """ Returns the value of the given key, or default if key doesn't exist. """
        return self.values.get(key, default)

    def get_object_directory_name(self) -> str:
        return self.get("object_directory_name")
    
    def get_git_directory_name(self) -> str:
        return self.get("git_directory_name")
    
    def get_gitignore_file(self) -> str:
        return self.get("git_ignore_file")
    
    def get_commit_directory_name(self) -> str:
        return self.get("commit_directory_name")
    
    def get_current_branch_file(self) -> str:
        return self.get("current_branch_file")
    
    def get_default_branch_name(self) -> str:
        return self.get("default_branch_name")