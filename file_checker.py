import config_reader, os

class file_monitor:
    def __init__(self):
        self.config = config_reader.config("config.env")
        self.directory = self.config.get_main_directory()
        self.exclude = set(["my_git"])

    def scan(self):
        for root, dirs, files in os.walk(self.directory):
            dirs[:] = [d for d in dirs if d not in self.exclude]
            print(root)
            print(dirs)
            print(files)


if __name__ == "__main__":
    c = file_monitor()
    c.scan()        
